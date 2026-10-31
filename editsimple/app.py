# EditSimple — montaggio video per presentazioni.  Copyright (C) 2026 Andrea Cumini <andrea@osintinfo.net>
# SPDX-License-Identifier: GPL-3.0-only
# GNU GPL v3 con termini aggiuntivi (attribuzione dell'autore): vedi LICENSE e NOTICE.
"""Finestra principale di EditSimple: intestazione, pagine Montaggio e Configurazione, piede.

La pagina Montaggio ha la barra dei comandi, l'anteprima con il pannello
delle proprieta', i controlli di riproduzione e la timeline. Ogni modifica
passa dal progetto (project.py) e poi da refresh(), che ridisegna timeline e
anteprima; prima di ogni modifica push_undo() salva uno stato per Annulla.
"""

from __future__ import annotations

import math
import os
import queue
import sys
import tempfile
import threading
import time
import tkinter as tk
from tkinter import filedialog

import customtkinter as ctk
from PIL import Image

from . import APP_NAME, COPYRIGHT, CREDITS, __version__, audio, frameless, i18n, media, overlays, procs, render, theme, tools, tracking, widgets
from .i18n import N_, again, tr, upper
from .config import Config
from .fonts import FontPicker, default_font
from .panels import PropertiesPanel
from .preview_view import PreviewView
from .project import EFFECT_NAMES, MIN_LEN, SPEEDS, TRACKABLE, Project, clip_duration, speed_text, speed_value
from .timeline_view import TimelineView
from .widgets import messagebox

# glifi di Segoe Fluent Icons (con un carattere di riserva se il font manca)
G = {
    "new": ("", "N"), "open": ("", "A"), "save": ("", "S"), "saveas": ("", "S+"),
    "import": ("", "+V"), "audio": ("", "+A"), "cut": ("", "|"), "delete": ("", "X"),
    "freeze": ("", "FI"), "speed": ("", "x2"), "text": ("", "T"), "box": ("", "[]"),
    "arrow": ("", "->"), "zoom": ("", "Z"), "pixel": ("", "#"), "export": ("", "MP4"),
    "logo": ("\uE8B9", "L"), "slide": ("\uE7F4", "SL"), "oval": ("", "O"), "pixelo": ("", "(#)"),
    "play": ("", ">"), "pause": ("", "||"), "first": ("", "|<"), "last": ("", ">|"),
    "prev": ("", "<"), "next": ("", ">"), "zin": ("", "+"), "zout": ("", "-"),
    "fit": ("", "[ ]"), "undo": ("", "U"), "redo": ("", "R"), "edit": ("", ""),
    "settings": ("", ""), "folder": ("", "..."),
}
LOGO_CORNERS = {"top-left": N_("In alto a sinistra"), "top-right": N_("In alto a destra"),
                "bottom-left": N_("In basso a sinistra"), "bottom-right": N_("In basso a destra")}
G["zoomo"] = (G["oval"][0], "ZO")    # zoom ovale: stessa icona dell'ovale
G["zoom"] = (G["box"][0], "Z")      # zoom rettangolare: stessa icona del riquadro
G["image"] = ("\uEB9F", "IMG")
G["timer"] = ("\uE916", "T0")
G["frames"] = ("\uE714", "#")
G["detach"] = ("\uE8A7", "^")     # apri in una finestra a parte
G["attach"] = ("\uE73F", "v")     # torna nella finestra principale
TIMELINE_MIN = 150      # altezze minime quando si sposta il divisore anteprima/timeline
PREVIEW_MIN = 140
PROJECT_TYPES = [(N_("Progetto EditSimple"), "*.json"), (N_("Tutti i file"), "*.*")]


def _filetypes(types) -> list[tuple[str, str]]:
    """Filtri dei dialoghi dei file con il nome nella lingua in uso."""
    return [(tr(name), pattern) for name, pattern in types]


class App(ctk.CTk):
    def __init__(self, initial: str | None = None) -> None:
        theme.apply()
        super().__init__()
        self.title(APP_NAME)
        self.config_store = Config()
        i18n.set_language(self.config_store.get("language"))   # prima di costruire l'interfaccia
        self.fonts = theme.Fonts()
        self.project = Project()
        self.frames = media.Frames()
        self.playhead = 0.0
        self.mark_in: float | None = None
        self.mark_out: float | None = None
        self.selected_kind: str | None = None
        self.selected_id: str | None = None
        self.undo_stack: list[dict] = []
        self.redo_stack: list[dict] = []
        self.playing = False
        self.play_reverse = False           # riproduzione all'indietro in corso
        self._play_job: str | None = None
        self.player = audio.AudioPlayer()     # audio dell'anteprima
        self._mix_samples_key: str | None = None
        self._mix_job: str | None = None
        self._play_origin = (0.0, 0.0)
        self._prefetched: str | None = None
        self._preview_job: str | None = None
        self._page = "edit"
        self._has_icons = bool(theme.icon_font())
        self._posted: queue.Queue = queue.Queue()   # chiamate dai thread di lavoro verso l'interfaccia

        geometry = self.config_store.get("geometry") or "1380x860"
        self.geometry(geometry)
        self.minsize(1100, 700)
        theme.set_icon(self)
        self.frameless = frameless.make_frameless(self, theme.BORDER)
        self._build()
        self.protocol("WM_DELETE_WINDOW", self._on_close)
        self._bind_keys()
        if sys.platform != "win32":
            audio.warm_up()                 # la ricerca del lettore audio (pw-cat --help) non deve aspettare il primo Play
        self.after(50, self._pump_posted)
        self.after(200, lambda: self._startup(initial))

    def post(self, func, *args) -> None:
        """Esegue `func` nel thread dell'interfaccia (da chiamare dai thread di lavoro)."""
        self._posted.put((func, args))

    def _pump_posted(self) -> None:
        try:
            while True:
                func, args = self._posted.get_nowait()
                try:
                    func(*args)
                except tk.TclError:
                    pass
        except queue.Empty:
            pass
        self.after(40, self._pump_posted)

    # ================================================================ costruzione

    def _glyph(self, key: str) -> str:
        icon, fallback = G[key]
        return icon if self._has_icons else fallback

    def _build(self) -> None:
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self._build_header()
        widgets.rule(self, True).grid(row=1, column=0, sticky="ew")
        body = ctk.CTkFrame(self, fg_color=theme.BG, corner_radius=0)
        body.grid(row=2, column=0, sticky="nsew")
        body.grid_columnconfigure(2, weight=1)
        body.grid_rowconfigure(0, weight=1)
        self._build_rail(body)
        widgets.rule(body, False).grid(row=0, column=1, sticky="ns")
        self.pages: dict[str, ctk.CTkFrame] = {}
        self.tool_buttons: dict[str, ctk.CTkButton] = {}
        for key in ("edit", "settings"):
            page = ctk.CTkFrame(body, fg_color=theme.BG, corner_radius=0)
            page.grid(row=0, column=2, sticky="nsew")
            self.pages[key] = page
        self._build_edit_page(self.pages["edit"])
        self._build_settings_page(self.pages["settings"])
        self._build_footer()
        self.show_page("edit")

    def _build_header(self) -> None:
        header = ctk.CTkFrame(self, fg_color=theme.BG, corner_radius=0, height=50)
        header.grid(row=0, column=0, sticky="ew")
        header.grid_propagate(False)
        header.grid_columnconfigure(2, weight=1)
        header.grid_rowconfigure(0, weight=1)

        brand = ctk.CTkFrame(header, fg_color="transparent")
        brand.grid(row=0, column=0, sticky="w", padx=(18, 0))
        logo = theme.logo(17)
        if logo is not None:
            name = ctk.CTkLabel(brand, text="", image=logo)
        else:
            name = ctk.CTkLabel(brand, text=APP_NAME.upper(), font=(theme.mono_font(), 15, "bold"))
        name.pack(side="left")
        version = ctk.CTkLabel(brand, text=f"   v{__version__}", font=(theme.mono_font(), 10), text_color=theme.TEXT_DIM)
        version.pack(side="left", pady=(3, 0))
        dot = ctk.CTkLabel(brand, text="  ·  ", font=(theme.mono_font(), 10), text_color=theme.TEXT_FAINT)
        dot.pack(side="left", pady=(3, 0))
        subtitle = ctk.CTkLabel(brand, text=tr("montaggio video per presentazioni"), font=(theme.mono_font(), 10),
                                text_color=theme.TEXT_FAINT)
        subtitle.pack(side="left", pady=(3, 0))

        chip = ctk.CTkFrame(header, fg_color=theme.PANEL, corner_radius=4, border_width=1, border_color=theme.BORDER, height=32)
        chip.grid(row=0, column=1, sticky="w", padx=(20, 0))
        tag = ctk.CTkLabel(chip, text=tr("PROGETTO"), font=self.fonts.caption, text_color=theme.TEXT_FAINT)
        tag.pack(side="left", padx=(10, 6), pady=2)
        self.project_label = ctk.CTkLabel(chip, text=tr("nuovo"), font=self.fonts.bold, text_color=theme.WARN, anchor="w", width=220)
        self.project_label.pack(side="left", padx=(0, 4), pady=3)
        open_button = ctk.CTkButton(chip, text=self._glyph("folder"), width=28, height=24, corner_radius=4,
                                    fg_color="transparent", hover_color=theme.HOVER, text_color=theme.TEXT_DIM,
                                    font=self.fonts.icon(12), command=self.open_project)
        open_button.pack(side="left", padx=(0, 4))
        widgets.Tooltip(open_button, tr("Apri progetto... (Ctrl+O)"), self.fonts)

        spacer = ctk.CTkFrame(header, fg_color="transparent", height=1)
        spacer.grid(row=0, column=2, sticky="ew")
        right = ctk.CTkFrame(header, fg_color="transparent")
        right.grid(row=0, column=3, sticky="e", padx=(0, 12))
        self.state_dot = ctk.CTkLabel(right, text="●", font=(theme.mono_font(), 12), text_color=theme.TEXT_FAINT)
        self.state_dot.pack(side="left", padx=(0, 6))
        self.state_label = ctk.CTkLabel(right, text=tr("Nessun video"), font=self.fonts.bold, text_color=theme.TEXT_SOFT)
        self.state_label.pack(side="left")
        if self.frameless:
            self._window_buttons(header).grid(row=0, column=4, sticky="ne", padx=(4, 0))
            for widget in (header, brand, name, version, dot, subtitle, spacer, right, tag, chip,
                           self.project_label, self.state_dot, self.state_label):
                frameless.enable_drag(self, widget)

    def _window_buttons(self, master) -> ctk.CTkFrame:
        family = theme.icon_font()
        glyphs = ("", "", "") if family else ("—", "□", "✕")
        restore = "" if family else "❐"
        font = ctk.CTkFont(family=family or theme.ui_font(), size=10 if family else 13)
        box = ctk.CTkFrame(master, fg_color="transparent", corner_radius=0)
        buttons = []
        for glyph, command, hover in ((glyphs[0], self.iconify, theme.HOVER),
                                      (glyphs[1], lambda: frameless.toggle_maximize(self), theme.HOVER),
                                      (glyphs[2], self._on_close, theme.CLOSE_HOVER)):
            item = ctk.CTkButton(box, text=glyph, command=command, width=46, height=34, corner_radius=0,
                                 fg_color="transparent", hover_color=hover, text_color=theme.TEXT_DIM, font=font)
            item.pack(side="left")
            buttons.append(item)

        def sync(event=None) -> None:
            if event is not None and event.widget is not self:
                return
            try:
                glyph = restore if self.state() == "zoomed" else glyphs[1]
                if buttons[1].winfo_exists() and buttons[1].cget("text") != glyph:
                    buttons[1].configure(text=glyph)
            except tk.TclError:
                pass

        self.bind("<Configure>", sync, add="+")
        return box

    def _build_rail(self, body) -> None:
        rail = ctk.CTkFrame(body, fg_color=theme.PANEL, corner_radius=0, width=84)
        rail.grid(row=0, column=0, sticky="ns")
        rail.grid_propagate(False)
        ctk.CTkLabel(rail, text=tr("PAGINE"), font=self.fonts.caption, text_color=theme.TEXT_FAINT).pack(pady=(14, 6))
        self._rail_buttons: dict[str, tuple[ctk.CTkButton, ctk.CTkLabel]] = {}
        for key, label, glyph in (("edit", N_("Montaggio"), "edit"), ("settings", N_("Configura"), "settings")):
            box = ctk.CTkFrame(rail, fg_color="transparent", corner_radius=4, width=74, height=62)
            box.pack(pady=(0, 6), padx=5)
            box.pack_propagate(False)
            item = ctk.CTkButton(box, text=self._glyph(glyph) if self._has_icons else tr(label)[:1],
                                 width=74, height=36, corner_radius=4, fg_color="transparent",
                                 hover_color=theme.HOVER, text_color=theme.TEXT_DIM,
                                 font=self.fonts.icon(16) if self._has_icons else self.fonts.bold,
                                 command=lambda k=key: self.show_page(k))
            if not self._has_icons:
                # senza icone il pulsante mostra l'iniziale del nome della pagina, nella lingua in uso
                item.retranslate = lambda b=item, t=label: b.configure(text=tr(t)[:1])
            item.pack()
            text = ctk.CTkLabel(box, text=tr(label), font=self.fonts.tiny, text_color=theme.TEXT_DIM, cursor="hand2")
            text.pack()
            text.bind("<Button-1>", lambda _e, k=key: self.show_page(k))
            self._rail_buttons[key] = (item, text)

    def show_page(self, key: str) -> None:
        self._page = key
        self.pages[key].tkraise()
        for name, (item, text) in self._rail_buttons.items():
            item.configure(fg_color=theme.ACCENT_BG if name == key else "transparent",
                           text_color=theme.ACCENT if name == key else theme.TEXT_DIM)
            text.configure(text_color=theme.ACCENT if name == key else theme.TEXT_DIM)
        if key == "settings":
            self._refresh_ffmpeg_status()

    # --------------------------------------------------------------- montaggio

    def _tool(self, parent, key: str, text: str, command, tooltip: str = "", primary: bool = False) -> ctk.CTkButton:
        def compose() -> str:
            # icona e testo in un'unica scritta: al cambio di lingua si ricompone (retranslate)
            words = again(text) if text else ""
            return (self._glyph(key) + ("  " + words if words else "")) if self._has_icons else (words or G[key][1])

        item = widgets.button(parent, compose(), command, primary=primary, height=30, width=10,
                              font=ctk.CTkFont(family=theme.icon_font() or theme.ui_font(), size=12, weight="bold")
                              if self._has_icons else self.fonts.button)
        item.retranslate = lambda: item.configure(text=compose())
        item.pack(side="left", padx=(0, 4))
        self.tool_buttons[key] = item       # per chi deve ritrovarlo (screenshot del manuale)
        if tooltip:
            widgets.Tooltip(item, tooltip, self.fonts)
        return item

    def _group(self, parent, title: str) -> ctk.CTkFrame:
        box = ctk.CTkFrame(parent, fg_color="transparent")
        box.pack(side="left", padx=(0, 14))
        label = ctk.CTkLabel(box, text=upper(title), font=self.fonts.caption, text_color=theme.TEXT_FAINT, anchor="w")
        label.retranslate = lambda: label.configure(text=upper(again(title)))
        label.pack(fill="x")
        row = ctk.CTkFrame(box, fg_color="transparent")
        row.pack(fill="x", pady=(2, 0))
        return row

    def _build_edit_page(self, page) -> None:
        page.grid_columnconfigure(0, weight=1)
        page.grid_rowconfigure(1, weight=3)
        page.grid_rowconfigure(3, weight=0)

        bar = ctk.CTkFrame(page, fg_color=theme.PANEL, corner_radius=4, border_width=1, border_color=theme.BORDER)
        bar.grid(row=0, column=0, columnspan=2, sticky="ew", padx=theme.PAD, pady=(theme.PAD, theme.GAP))
        inner = ctk.CTkFrame(bar, fg_color="transparent")
        inner.pack(fill="x", padx=10, pady=(6, 8))
        row1 = ctk.CTkFrame(inner, fg_color="transparent")
        row1.pack(fill="x")
        row2 = ctk.CTkFrame(inner, fg_color="transparent")
        row2.pack(fill="x", pady=(6, 0))
        g = self._group(row1, tr("Progetto"))
        self._tool(g, "new", tr("Nuovo"), self.new_project, tr("Nuovo progetto (Ctrl+N)"))
        self._tool(g, "open", tr("Apri"), self.open_project, tr("Apri progetto (Ctrl+O)"))
        self._tool(g, "save", tr("Salva"), self.save_project, tr("Salva progetto (Ctrl+S)"))
        self._tool(g, "undo", "", self.undo, tr("Annulla (Ctrl+Z)"))
        self._tool(g, "redo", "", self.redo, tr("Ripeti (Ctrl+Y)"))
        g = self._group(row1, tr("Clip"))
        self._tool(g, "import", tr("Importa video"), self.import_video, tr("Importa un video in coda o al cursore (Ctrl+I)"))
        self._tool(g, "audio", tr("Audio"), self.add_audio, tr("Aggiungi una traccia audio (commento, musica) al cursore"))
        self._tool(g, "cut", tr("Taglia"), self.split_at_playhead, tr("Taglia la clip al cursore (S)"))
        self._tool(g, "delete", tr("Elimina"), self.delete_selection, tr("Elimina la porzione IN-OUT o l'elemento selezionato (Canc)"))
        self._tool(g, "freeze", tr("Fermo"), self.add_freeze, tr("Fermo immagine del fotogramma al cursore (F)"))
        self._tool(g, "slide", tr("Slide"), self.add_slide, tr("Inserisci una slide"))
        self._tool(g, "speed", tr("Velocita'"), self.set_speed, tr("Velocita' della porzione IN-OUT: piu' veloce o rallentata (V)"))
        g = self._group(row2, tr("Sovraimpressioni"))
        self._tool(g, "text", tr("Testo"), lambda: self.start_draw("text"), tr("Testo (T)"))
        self._tool(g, "image", tr("Immagine"), self.add_image, tr("Immagine sopra il video, da spostare e ridimensionare"))
        self._tool(g, "logo", tr("Logo"), self.add_logo, tr("Logo e testo dell'operatore, fermi in un angolo (L)"))
        self._tool(g, "timer", tr("Tempo"), lambda: self.start_draw("timer"),
                   tr("Tempo trascorso dall'inizio del video: clic dove metterlo, poi si sposta"))
        self._tool(g, "frames", tr("Fotogrammi"), lambda: self.start_draw("frames"),
                   tr("Numero del fotogramma dall'inizio del video: clic dove metterlo, poi si sposta"))
        self._tool(g, "box", tr("Riquadro"), lambda: self.start_draw("box"), tr("Riquadro (R): puo' seguire il soggetto"))
        self._tool(g, "oval", tr("Ovale"), lambda: self.start_draw("oval"), tr("Ovale (E): puo' seguire il soggetto"))
        self._tool(g, "arrow", tr("Freccia"), lambda: self.start_draw("arrow"), tr("Freccia (A): puo' seguire il soggetto"))
        self._tool(g, "zoom", tr("Zoom"), lambda: self.start_draw("zoom"), tr("Zoom rettangolare: l'area scelta in un riquadro ingrandito (Z)"))
        self._tool(g, "zoomo", tr("Zoom"), lambda: self.start_draw("zoom_oval"), tr("Zoom ovale: l'area scelta in un ovale ingrandito (Maiusc+Z)"))
        self._tool(g, "pixel", tr("Pixel"), lambda: self.start_draw("pixelate"), tr("Pixelatura rettangolare che insegue il soggetto (P)"))
        self._tool(g, "pixelo", tr("Pixel"), lambda: self.start_draw("pixelate_oval"), tr("Pixelatura ovale che insegue il soggetto (K)"))
        g = self._group(row2, tr("Uscita"))
        self._tool(g, "export", tr("Esporta MP4"), self.export, tr("Esporta il video finale (Ctrl+E)"), primary=True)

        # anteprima + proprieta'
        self._edit_page = page
        self.preview_window: ctk.CTkToplevel | None = None     # anteprima staccata in una finestra a parte
        self.preview = self._make_preview(page)
        self.preview.grid(row=1, column=0, sticky="nsew", padx=(theme.PAD, theme.GAP))
        self.panel = PropertiesPanel(page, self.fonts, self)
        self.panel.grid(row=1, column=1, sticky="nsew", padx=(0, theme.PAD))

        # trasporto
        transport = ctk.CTkFrame(page, fg_color=theme.PANEL, corner_radius=4, border_width=1, border_color=theme.BORDER)
        transport.grid(row=2, column=0, columnspan=2, sticky="ew", padx=theme.PAD, pady=(theme.GAP, theme.GAP))
        # divisore fra anteprima e timeline: trascinandolo in alto l'anteprima si riduce e la timeline cresce
        sash = tk.Frame(page, height=theme.GAP, bg=theme.BG, cursor="sb_v_double_arrow")
        sash.grid(row=2, column=0, columnspan=2, sticky="new", padx=theme.PAD)
        sash.bind("<Enter>", lambda _e: sash.configure(bg=theme.BORDER_STRONG))
        sash.bind("<Leave>", lambda _e: sash.configure(bg=theme.BG) if self._sash is None else None)
        sash.bind("<ButtonPress-1>", self._sash_press)
        sash.bind("<B1-Motion>", self._sash_move)
        sash.bind("<ButtonRelease-1>", lambda e: self._sash_release(e, sash))
        self._sash: tuple[int, int, int] | None = None
        row = ctk.CTkFrame(transport, fg_color="transparent")
        row.pack(fill="x", padx=10, pady=6)
        widgets.icon_button(row, self._glyph("first"), "|<", lambda: self.seek(0.0), self.fonts, tooltip=tr("Inizio (Home)")).pack(side="left", padx=(0, 3))
        tens = dict(width=40, height=30, font=self.fonts.bold)
        back10 = widgets.button(row, "-10", lambda: self.step_frames(-10), **tens)
        back10.pack(side="left", padx=(0, 3))
        widgets.Tooltip(back10, tr("10 fotogrammi indietro (Ctrl+Sinistra)"), self.fonts)
        widgets.icon_button(row, self._glyph("prev"), "<", lambda: self.step_frames(-1), self.fonts, tooltip=tr("Fotogramma precedente (Sinistra)")).pack(side="left", padx=(0, 3))
        # riproduzione all'indietro: un triangolo verso sinistra (senza audio)
        self.reverse_button = widgets.button(row, "◀", self.toggle_play_reverse, width=44, height=30, font=self.fonts.bold,
                                             fg_color=theme.NEUTRAL, hover_color=theme.NEUTRAL_HOVER)
        self.reverse_button.pack(side="left", padx=(0, 3))
        widgets.Tooltip(self.reverse_button, tr("Riproduci all'indietro / pausa (Maiusc+Spazio), senza audio"), self.fonts)
        self.play_button = widgets.icon_button(row, self._glyph("play"), ">", self.toggle_play, self.fonts, width=44,
                                               tooltip=tr("Riproduci / pausa (Spazio)"), fg_color=theme.BTN, hover_color=theme.BTN_HOVER,
                                               text_color=theme.BTN_TEXT)
        self.play_button.pack(side="left", padx=(0, 3))
        widgets.icon_button(row, self._glyph("next"), ">", lambda: self.step_frames(1), self.fonts, tooltip=tr("Fotogramma successivo (Destra)")).pack(side="left", padx=(0, 3))
        fwd10 = widgets.button(row, "+10", lambda: self.step_frames(10), **tens)
        fwd10.pack(side="left", padx=(0, 3))
        widgets.Tooltip(fwd10, tr("10 fotogrammi avanti (Ctrl+Destra)"), self.fonts)
        widgets.icon_button(row, self._glyph("last"), ">|", lambda: self.seek(self.project.duration()), self.fonts, tooltip=tr("Fine (Fine)")).pack(side="left", padx=(0, 12))
        self.time_var = tk.StringVar(value="00:00.000")
        self.time_entry = ctk.CTkEntry(row, textvariable=self.time_var, width=104, height=30, font=self.fonts.mono_big, justify="center")
        self.time_entry.pack(side="left")
        self.time_entry.bind("<Return>", self._time_entered)
        self.duration_label = ctk.CTkLabel(row, text=" / 00:00.000", font=self.fonts.mono, text_color=theme.TEXT_DIM)
        self.duration_label.pack(side="left", padx=(4, 14))
        widgets.button(row, "IN", self.mark_in_here, width=44, height=30, text_color=theme.MARK_IN).pack(side="left", padx=(0, 3))
        widgets.button(row, "OUT", self.mark_out_here, width=48, height=30, text_color=theme.MARK_OUT).pack(side="left", padx=(0, 3))
        self.range_label = ctk.CTkLabel(row, text="", font=self.fonts.mono, text_color=theme.TEXT_DIM)
        self.range_label.pack(side="left", padx=(6, 3))
        widgets.button(row, "x", self.clear_marks, width=28, height=30).pack(side="left")
        widgets.icon_button(row, self._glyph("fit"), "[ ]", lambda: self.timeline.zoom_fit(), self.fonts, tooltip=tr("Adatta la timeline")).pack(side="right")
        widgets.icon_button(row, self._glyph("zin"), "+", lambda: self.timeline.zoom_by(1.5), self.fonts, tooltip=tr("Ingrandisci la timeline (Ctrl+rotellina). Per spostarla: Alt+trascina, tasto centrale o rotellina")).pack(side="right", padx=(0, 3))
        widgets.icon_button(row, self._glyph("zout"), "-", lambda: self.timeline.zoom_by(1 / 1.5), self.fonts, tooltip=tr("Riduci la timeline")).pack(side="right", padx=(0, 3))
        self.mode_label = ctk.CTkLabel(row, text="", font=self.fonts.bold, text_color=theme.ACCENT)
        self.mode_label.pack(side="right", padx=(0, 14))

        # timeline
        self.timeline = TimelineView(page, self.fonts, self.project, on_seek=self.seek, on_select=self.select,
                                     on_changed=self._timeline_changed, on_edit_start=self.push_undo)
        self.timeline.grid(row=3, column=0, columnspan=2, sticky="nsew", padx=theme.PAD, pady=(0, theme.PAD))
        self.timeline.on_key_delete = self._timeline_key_delete
        self.timeline.on_fx_menu = self._effect_menu
        self.timeline.on_fx_visibility = self.toggle_effect_visible
        self.preview.on_key = self._preview_key
        self.preview.on_edit_text = self.edit_text
        self.timeline.configure(height=max(TIMELINE_MIN, int(self.config_store.get("timeline_height") or 250)))
        self.timeline.grid_propagate(False)

    # --------------------------------------------------------------- configurazione

    def _build_settings_page(self, outer) -> None:
        # la pagina scorre: con logo, angoli e crediti e' piu' alta della finestra
        outer.grid_columnconfigure(0, weight=1)
        outer.grid_rowconfigure(0, weight=1)
        page = self.settings_scroll = ctk.CTkScrollableFrame(outer, fg_color="transparent")
        page.grid(row=0, column=0, sticky="nsew")
        page.grid_columnconfigure(0, weight=1)
        page.grid_columnconfigure(1, weight=1)
        ctk.CTkLabel(page, text=tr("Configurazione"), font=self.fonts.page, anchor="w").grid(
            row=0, column=0, columnspan=2, sticky="ew", padx=theme.PAD + 4, pady=(theme.PAD, 4))

        left = ctk.CTkFrame(page, fg_color="transparent")
        left.grid(row=1, column=0, sticky="new", padx=(theme.PAD, theme.GAP), pady=(theme.GAP, 0))
        ff = widgets.Card(left, "FFmpeg", self.fonts)
        ff.pack(fill="x")
        self.ffmpeg_label = ctk.CTkLabel(ff.body, text="", font=self.fonts.body, anchor="w", justify="left", wraplength=420)
        self.ffmpeg_label.pack(fill="x")
        # fuori da Windows il download automatico non c'e': la nota spiega come avere ffmpeg
        if sys.platform == "win32":
            ffmpeg_note = tr("ffmpeg non e' incluso nel programma: e' un programma separato con la propria licenza. "
                             "Scarica / Aggiorna prende il build ufficiale per Windows (release essentials) da gyan.dev "
                             "e tiene solo ffmpeg.exe, LICENSE e README in tools/ffmpeg/. Nessuna installazione, "
                             "nessuna modifica al PATH.")
        else:
            ffmpeg_note = tr("ffmpeg non e' incluso nel programma: e' un programma separato con la propria licenza. "
                             "Su Linux e macOS si installa con il gestore di pacchetti del sistema "
                             "(per esempio sudo apt install ffmpeg) oppure si mette un eseguibile ffmpeg in "
                             "tools/ffmpeg/. Il download automatico vale solo per Windows.")
        widgets.note(ff.body, ffmpeg_note, self.fonts, wraplength=420).pack(fill="x", pady=(8, 0))
        row = ctk.CTkFrame(ff.body, fg_color="transparent")
        row.pack(fill="x", pady=(10, 0))
        download_state = "normal" if sys.platform == "win32" else "disabled"  # il download prende il build per Windows
        widgets.button(row, tr("Scarica / Aggiorna"), self.download_ffmpeg, primary=True, width=150, state=download_state).pack(side="left")
        widgets.button(row, tr("Apri cartella tools"), lambda: self._open_folder(tools.TOOLS_DIR), width=150).pack(side="left", padx=(8, 0))

        vt = widgets.Card(left, tr("Inseguimento (VitTrack)"), self.fonts)
        vt.pack(fill="x", pady=(theme.GAP, 0))
        self.vit_label = ctk.CTkLabel(vt.body, text="", font=self.fonts.body, anchor="w", justify="left", wraplength=420)
        self.vit_label.pack(fill="x")
        widgets.note(vt.body, tr("VitTrack e' un modello addestrato per seguire oggetti e persone: ritrova il soggetto "
                                 "dopo un palo o un passante e capisce quando e' perso. Viene dal repository ufficiale "
                                 "opencv_zoo (licenza Apache 2.0, compatibile con la GPL 3), circa 0,7 MB, in "
                                 "tools/vittrack/ con la sua licenza. Senza, l'inseguimento usa il confronto a modello."),
                     self.fonts, wraplength=420).pack(fill="x", pady=(8, 0))
        widgets.button(vt.body, tr("Scarica"), self.download_vit, primary=True, width=150).pack(anchor="w", pady=(10, 0))
        self._refresh_vit_status()

        ex = widgets.Card(page, tr("Esportazione"), self.fonts)
        ex.grid(row=1, column=1, sticky="new", padx=(0, theme.PAD), pady=(theme.GAP, 0))
        widgets.caption(ex.body, tr("Qualita' video (CRF, 15 = ottima, 28 = leggera)"), self.fonts).pack(fill="x")
        self.crf_var = tk.StringVar(value=str(self.config_store.get("export_crf")))
        ctk.CTkEntry(ex.body, textvariable=self.crf_var, width=80, font=self.fonts.body).pack(anchor="w", pady=(2, 8))
        widgets.caption(ex.body, tr("Velocita' di codifica (preset x264)"), self.fonts).pack(fill="x")
        self.preset_var = tk.StringVar(value=str(self.config_store.get("export_preset")))
        ctk.CTkOptionMenu(ex.body, variable=self.preset_var, values=list(render.PRESETS), font=self.fonts.body).pack(anchor="w", pady=(2, 8))
        widgets.caption(ex.body, tr("Audio (kbit/s)"), self.fonts).pack(fill="x")
        self.kbps_var = tk.StringVar(value=str(self.config_store.get("export_audio_kbps")))
        ctk.CTkEntry(ex.body, textvariable=self.kbps_var, width=80, font=self.fonts.body).pack(anchor="w", pady=(2, 8))
        widgets.caption(ex.body, tr("Durate proposte (secondi)"), self.fonts).pack(fill="x")
        row = ctk.CTkFrame(ex.body, fg_color="transparent")
        row.pack(fill="x", pady=(2, 8))
        ctk.CTkLabel(row, text=tr("fermo immagine"), font=self.fonts.small, text_color=theme.TEXT_SOFT).pack(side="left")
        self.freeze_var = tk.StringVar(value=f"{self.config_store.get('freeze_seconds'):g}")
        ctk.CTkEntry(row, textvariable=self.freeze_var, width=60, font=self.fonts.body).pack(side="left", padx=(6, 14))
        ctk.CTkLabel(row, text=tr("effetti"), font=self.fonts.small, text_color=theme.TEXT_SOFT).pack(side="left")
        self.effect_var = tk.StringVar(value=f"{self.config_store.get('effect_seconds'):g}")
        ctk.CTkEntry(row, textvariable=self.effect_var, width=60, font=self.fonts.body).pack(side="left", padx=(6, 0))
        widgets.caption(ex.body, tr("Pixelatura: grandezza dei pixel e soglia dell'inseguimento (0.2-0.9)"), self.fonts).pack(fill="x")
        row = ctk.CTkFrame(ex.body, fg_color="transparent")
        row.pack(fill="x", pady=(2, 8))
        self.block_var = tk.StringVar(value=str(self.config_store.get("pixel_block")))
        ctk.CTkEntry(row, textvariable=self.block_var, width=60, font=self.fonts.body).pack(side="left")
        self.track_min_var = tk.StringVar(value=f"{self.config_store.get('track_min'):g}")
        ctk.CTkEntry(row, textvariable=self.track_min_var, width=60, font=self.fonts.body).pack(side="left", padx=(8, 0))
        widgets.button(ex.body, tr("Salva impostazioni"), self._save_settings, primary=True, width=150).pack(anchor="w", pady=(6, 0))

        lg = widgets.Card(page, tr("Logo e testo dell'operatore"), self.fonts)
        lg.grid(row=2, column=0, columnspan=2, sticky="new", padx=theme.PAD, pady=(theme.GAP, 0))
        top = ctk.CTkFrame(lg.body, fg_color="transparent")
        top.pack(fill="x")
        self.logo_thumb = ctk.CTkLabel(top, text="", width=120, height=64, fg_color=theme.BG, corner_radius=4)
        self.logo_thumb.pack(side="left", padx=(0, 12))
        side = ctk.CTkFrame(top, fg_color="transparent")
        side.pack(side="left", fill="x", expand=True)
        self.logo_path_var = tk.StringVar(value=str(self.config_store.get("logo_path") or ""))
        self.logo_path_label = ctk.CTkLabel(side, text="", font=self.fonts.body, anchor="w", justify="left", wraplength=640)
        self.logo_path_label.pack(fill="x")
        row = ctk.CTkFrame(side, fg_color="transparent")
        row.pack(fill="x", pady=(6, 0))
        widgets.button(row, tr("Carica immagine del logo..."), self._settings_pick_logo, primary=True, width=190).pack(side="left")
        widgets.button(row, tr("Togli logo"), lambda: self._settings_set_logo(""), width=100).pack(side="left", padx=(8, 0))
        widgets.caption(lg.body, tr("Testo dell'operatore (nome, qualifica, data...)"), self.fonts).pack(fill="x", pady=(10, 0))
        self.operator_text_var = tk.StringVar(value=str(self.config_store.get("operator_text") or ""))
        ctk.CTkEntry(lg.body, textvariable=self.operator_text_var, font=self.fonts.body).pack(fill="x", pady=(2, 8))
        row = ctk.CTkFrame(lg.body, fg_color="transparent")
        row.pack(fill="x")
        self.logo_width_var = tk.StringVar(value=f"{self.config_store.get('logo_width'):g}")
        self.operator_size_var = tk.StringVar(value=f"{self.config_store.get('operator_size'):g}")
        self.logo_margin_var = tk.StringVar(value=f"{self.config_store.get('logo_margin'):g}")
        for text, var in ((tr("larghezza logo % del video"), self.logo_width_var),
                          (tr("altezza testo % del lato corto"), self.operator_size_var),
                          (tr("distanza dai bordi % del lato corto"), self.logo_margin_var)):
            ctk.CTkLabel(row, text=text, font=self.fonts.small, text_color=theme.TEXT_SOFT).pack(side="left")
            ctk.CTkEntry(row, textvariable=var, width=56, font=self.fonts.body).pack(side="left", padx=(6, 16))
        row = ctk.CTkFrame(lg.body, fg_color="transparent")
        row.pack(fill="x", pady=(8, 0))
        ctk.CTkLabel(row, text=tr("angolo"), font=self.fonts.small, text_color=theme.TEXT_SOFT).pack(side="left")
        self.logo_corner_menu = self._choice_menu(row, LOGO_CORNERS, self.config_store.get("logo_corner"), "bottom-right", 170)
        self.logo_corner_menu.pack(side="left", padx=(6, 16))
        ctk.CTkLabel(row, text=tr("disposizione"), font=self.fonts.small, text_color=theme.TEXT_SOFT).pack(side="left")
        self.logo_layout_menu = self._choice_menu(row, overlays.LOGO_LAYOUTS, self.config_store.get("logo_layout"), "right", 190)
        self.logo_layout_menu.pack(side="left", padx=(6, 16))
        ctk.CTkLabel(row, text=tr("colore testo"), font=self.fonts.small, text_color=theme.TEXT_SOFT).pack(side="left")
        self.operator_color = str(self.config_store.get("operator_color") or "#FFFFFF").upper()
        self.operator_color_button = ctk.CTkButton(row, text=self.operator_color, width=96, height=28, font=self.fonts.mono,
                                                   command=self._settings_pick_color)
        self.operator_color_button.pack(side="left", padx=(6, 0))
        self._show_operator_color()
        row = ctk.CTkFrame(lg.body, fg_color="transparent")
        row.pack(fill="x", pady=(8, 0))
        self.logo_bg_var = tk.BooleanVar(value=bool(self.config_store.get("logo_bg")))
        ctk.CTkCheckBox(row, text=tr("sfondo sotto logo e scritta"), variable=self.logo_bg_var, font=self.fonts.body).pack(side="left", padx=(0, 16))
        ctk.CTkLabel(row, text=tr("colore"), font=self.fonts.small, text_color=theme.TEXT_SOFT).pack(side="left")
        self.logo_bg_color = str(self.config_store.get("logo_bg_color") or "#000000").upper()
        self.logo_bg_button = ctk.CTkButton(row, text=self.logo_bg_color, width=96, height=28, font=self.fonts.mono,
                                            command=self._settings_pick_bg_color)
        self.logo_bg_button.pack(side="left", padx=(6, 16))
        self._show_logo_bg_color()
        self.logo_bg_alpha_var = tk.StringVar(value=f"{float(self.config_store.get('logo_bg_alpha')) * 100:g}")
        self.logo_bg_radius_var = tk.StringVar(value=f"{float(self.config_store.get('logo_bg_radius')):g}")
        for text, var in ((tr("opacita' %"), self.logo_bg_alpha_var), (tr("angoli arrotondati %"), self.logo_bg_radius_var)):
            ctk.CTkLabel(row, text=text, font=self.fonts.small, text_color=theme.TEXT_SOFT).pack(side="left")
            ctk.CTkEntry(row, textvariable=var, width=56, font=self.fonts.body).pack(side="left", padx=(6, 16))
        widgets.note(lg.body, tr("Il pulsante Logo (tasto L) mette logo e testo nell'angolo scelto, fermi per tutto il video "
                                 "(o solo nella porzione IN-OUT, se e' segnata). Nel progetto si possono poi spostare, "
                                 "ridimensionare e cambiare dal pannello a destra."), self.fonts, wraplength=800).pack(fill="x", pady=(8, 0))
        row = ctk.CTkFrame(lg.body, fg_color="transparent")
        row.pack(fill="x", pady=(8, 0))
        widgets.button(row, tr("Salva impostazioni"), self._save_settings, primary=True, width=150).pack(side="left")
        self._settings_set_logo(self.logo_path_var.get(), save=False)

        rc = widgets.Card(page, tr("Angoli arrotondati"), self.fonts)
        rc.grid(row=3, column=0, columnspan=2, sticky="new", padx=theme.PAD, pady=(theme.GAP, 0))
        widgets.caption(rc.body, tr("Proposti ai nuovi effetti, in % del lato corto (0 = angoli vivi, 50 = estremita' tonde); "
                                    "ogni effetto poi si regola nel suo pannello"), self.fonts).pack(fill="x")
        row = ctk.CTkFrame(rc.body, fg_color="transparent")
        row.pack(fill="x", pady=(6, 0))
        self.round_vars = {}
        for key, text in (("round_text", tr("sfondo del testo")), ("round_box", tr("riquadro")),
                          ("round_zoom", tr("zoom rettangolare")), ("round_pixel", tr("pixel rettangolare"))):
            var = tk.StringVar(value=f"{float(self.config_store.get(key)):g}")
            self.round_vars[key] = var
            ctk.CTkLabel(row, text=text, font=self.fonts.small, text_color=theme.TEXT_SOFT).pack(side="left")
            ctk.CTkEntry(row, textvariable=var, width=56, font=self.fonts.body).pack(side="left", padx=(6, 18))
        widgets.button(row, tr("Salva impostazioni"), self._save_settings, primary=True, width=150).pack(side="left")

        self._build_language_card(page, 4)
        credits = widgets.Card(page, tr("Crediti"), self.fonts)
        credits.grid(row=5, column=0, columnspan=2, sticky="new", padx=theme.PAD, pady=(theme.GAP, 0))
        ctk.CTkLabel(credits.body, text=CREDITS, font=self.fonts.mono, text_color=theme.ACCENT, anchor="w").pack(fill="x")
        widgets.note(credits.body, tr("{app} {version}. Montaggio video semplice per presentazioni: timeline, tagli, "
                                      "fermo immagine, avanzamento veloce, sovraimpressioni, zoom e pixelatura con inseguimento; "
                                      "esportazione mp4 con ffmpeg. Progetti in formato JSON.").format(
                         app=APP_NAME, version=__version__), self.fonts, wraplength=800).pack(fill="x", pady=(6, 0))
        widgets.note(credits.body, tr("{copyright}. Software libero: GNU General Public License versione 3 con termini "
                                      "aggiuntivi (attribuzione dell'autore, nome e logo), vedi i file LICENSE e NOTICE. "
                                      "Nessuna garanzia. Usa librerie e programmi di terze parti con le loro licenze "
                                      "(elencati in NOTICE).").format(copyright=COPYRIGHT), self.fonts, wraplength=800).pack(fill="x", pady=(6, 0))

    def _choice_menu(self, parent, labels: dict, key, fallback: str, width: int) -> ctk.CTkOptionMenu:
        """Menu con le etichette di `labels` (chiave interna -> testo N_) nella lingua in uso.

        La scelta si legge da `menu.choice_key`, la chiave interna, uguale in ogni lingua;
        al cambio di lingua il menu ritraduce voci e scelta corrente.
        """
        var = tk.StringVar()
        menu = ctk.CTkOptionMenu(parent, variable=var, values=[tr(v) for v in labels.values()], width=width,
                                 font=self.fonts.body,
                                 command=lambda choice: setattr(menu, "choice_key", next(
                                     (k for k, v in labels.items() if tr(v) == choice), menu.choice_key)))
        menu.choice_key = key if key in labels else fallback

        def retranslate() -> None:
            menu.configure(values=[tr(v) for v in labels.values()])
            var.set(tr(labels[menu.choice_key]))

        menu.retranslate = retranslate
        var.set(tr(labels[menu.choice_key]))
        return menu

    def _settings_pick_logo(self) -> None:
        path = self.ask_logo_file(self.logo_path_var.get())
        if path:
            self._settings_set_logo(path)

    def _settings_set_logo(self, path: str, save: bool = True) -> None:
        """Logo scelto in configurazione: miniatura, percorso e salvataggio immediato."""
        self.logo_path_var.set(path)
        image = overlays.load_logo(path) if path else None
        if image is not None:
            k = min(120 / image.width, 64 / image.height)
            size = (max(1, int(image.width * k)), max(1, int(image.height * k)))
            # la miniatura vecchia deve restare viva finche' l'etichetta non mostra la nuova: se Python la
            # libera prima, Tk si ritrova un'immagine cancellata ("image pyimage2 doesn't exist")
            thumb = ctk.CTkImage(light_image=image, dark_image=image, size=size)
            self.logo_thumb.configure(image=thumb, text="")
            self._logo_thumb_image = thumb
            self.logo_path_label.configure(text=f"{path}\n{image.width} x {image.height} px", text_color=theme.TEXT)
        else:
            # image=None non stacca l'immagine in customtkinter: si mette un pixel trasparente
            blank = Image.new("RGBA", (1, 1), (0, 0, 0, 0))
            thumb = ctk.CTkImage(light_image=blank, dark_image=blank, size=(1, 1))
            self.logo_thumb.configure(image=thumb, text=tr("nessun logo"))
            self._logo_thumb_image = thumb
            self.logo_path_label.configure(text=tr("File non trovato: {path}").format(path=path) if path else
                                           tr("Nessun logo: carica un'immagine (PNG con trasparenza, JPG...)."),
                                           text_color=theme.ERR if path else theme.TEXT_DIM)
        if save:
            self.config_store.set("logo_path", path)
            self.config_store.save()

    def _settings_pick_color(self) -> None:
        from tkinter import colorchooser
        _rgb, hexcolor = colorchooser.askcolor(color=self.operator_color, title=tr("Colore del testo"), parent=self)
        if hexcolor:
            self.operator_color = hexcolor.upper()
            self._show_operator_color()

    def _settings_pick_bg_color(self) -> None:
        from tkinter import colorchooser
        _rgb, hexcolor = colorchooser.askcolor(color=self.logo_bg_color, title=tr("Colore dello sfondo"), parent=self)
        if hexcolor:
            self.logo_bg_color = hexcolor.upper()
            self._show_logo_bg_color()

    def _show_logo_bg_color(self) -> None:
        c = self.logo_bg_color
        r, g, b = overlays.hex_to_rgb(c)
        self.logo_bg_button.configure(text=c, fg_color=c, hover_color=c,
                                      text_color="#000000" if r * 0.299 + g * 0.587 + b * 0.114 > 150 else "#FFFFFF")

    def _show_operator_color(self) -> None:
        c = self.operator_color
        r, g, b = overlays.hex_to_rgb(c)
        self.operator_color_button.configure(text=c, fg_color=c, hover_color=c,
                                             text_color="#000000" if r * 0.299 + g * 0.587 + b * 0.114 > 150 else "#FFFFFF")

    def ask_logo_file(self, current: str = "") -> str:
        path = filedialog.askopenfilename(
            title=tr("Immagine del logo"), parent=self,
            initialdir=os.path.dirname(current) if current else (self.config_store.get("last_logo_dir") or None),
            filetypes=[(tr("Immagini"), "*.png *.jpg *.jpeg *.webp *.bmp *.gif"), (tr("Tutti i file"), "*.*")])
        if not path:
            return ""
        if overlays.load_logo(path) is None:
            messagebox.showwarning(tr("Logo"), tr("Questa immagine non si apre."), self)
            return ""
        self.config_store.set("last_logo_dir", os.path.dirname(path))
        return path

    # --------------------------------------------------------------- lingua

    def _build_language_card(self, parent, row: int) -> None:
        card = widgets.Card(parent, tr("Lingua"), self.fonts)
        card.grid(row=row, column=0, columnspan=2, sticky="new", padx=theme.PAD, pady=(theme.GAP, 0))
        line = ctk.CTkFrame(card.body, fg_color="transparent")
        line.pack(fill="x")
        self._language_buttons: dict[str, ctk.CTkButton] = {}
        for code, name in i18n.LANGUAGES.items():
            item = ctk.CTkButton(line, text=name, width=96, height=28, corner_radius=3, font=self.fonts.body,
                                 command=lambda c=code: self.set_language(c))
            item.pack(side="left", padx=(0, 4))
            self._language_buttons[code] = item
        self._paint_language()
        widgets.note(card.body, tr("La lingua dell'interfaccia cambia subito, senza riavviare."), self.fonts,
                     wraplength=800).pack(fill="x", pady=(8, 0))

    def _paint_language(self) -> None:
        for code, item in self._language_buttons.items():
            on = code == i18n.language()
            item.configure(fg_color=theme.ACCENT_BG if on else "transparent", hover_color=theme.ACCENT_BG if on else theme.HOVER,
                           text_color=theme.ACCENT if on else theme.TEXT_DIM)

    def set_language(self, code: str) -> None:
        """Cambia lingua a programma aperto: i testi a schermo vengono ritradotti subito."""
        if code == i18n.language():
            return
        code = i18n.set_language(code)
        self.config_store.set("language", code)
        self.config_store.save()
        self._paint_language()
        widgets.retranslate_all(self)
        # cio' che si costruisce da capo: pannello delle proprieta', timeline, anteprima, stato
        self.panel.show(self.selected_kind, self._selected_obj())
        self.timeline.schedule()
        self.schedule_preview()
        if self.preview.mode:
            self.start_draw(self.preview.mode)
        self.refresh()

    def _save_settings(self) -> None:
        try:
            self.config_store.set("export_crf", max(10, min(35, int(self.crf_var.get()))))
            self.config_store.set("export_preset", self.preset_var.get())
            self.config_store.set("export_audio_kbps", max(64, min(320, int(self.kbps_var.get()))))
            self.config_store.set("freeze_seconds", max(0.1, float(self.freeze_var.get().replace(",", "."))))
            self.config_store.set("effect_seconds", max(0.1, float(self.effect_var.get().replace(",", "."))))
            self.config_store.set("pixel_block", max(2, int(self.block_var.get())))
            self.config_store.set("track_min", max(0.1, min(0.95, float(self.track_min_var.get().replace(",", ".")))))
            self.config_store.set("logo_width", max(1.0, min(90.0, float(self.logo_width_var.get().replace(",", ".")))))
            self.config_store.set("operator_size", max(0.5, min(30.0, float(self.operator_size_var.get().replace(",", ".")))))
            self.config_store.set("logo_margin", max(0.0, min(30.0, float(self.logo_margin_var.get().replace(",", ".")))))
            self.config_store.set("operator_text", self.operator_text_var.get())
            self.config_store.set("operator_color", self.operator_color)
            self.config_store.set("logo_path", self.logo_path_var.get())
            self.config_store.set("logo_corner", self.logo_corner_menu.choice_key)
            self.config_store.set("logo_layout", self.logo_layout_menu.choice_key)
            for key, var in self.round_vars.items():
                self.config_store.set(key, max(0.0, min(50.0, float(var.get().replace(",", ".")))))
            self.config_store.set("logo_bg", bool(self.logo_bg_var.get()))
            self.config_store.set("logo_bg_color", self.logo_bg_color)
            self.config_store.set("logo_bg_alpha", max(0.0, min(1.0, float(self.logo_bg_alpha_var.get().replace(",", ".")) / 100)))
            self.config_store.set("logo_bg_radius", max(0.0, min(50.0, float(self.logo_bg_radius_var.get().replace(",", ".")))))
        except ValueError:
            messagebox.showwarning(tr("Valore non valido"), tr("Controlla i numeri inseriti."), self)
            return
        self.config_store.save()
        self.status(tr("Impostazioni salvate."))

    def _refresh_ffmpeg_status(self) -> None:
        def work() -> None:
            status = tools.status()
            self.post(lambda: show(status))

        def show(status: tools.Status) -> None:
            if status.present:
                where = {"tools": tr("cartella tools/ffmpeg"), "path": tr("PATH di sistema")}.get(status.source, status.source)
                self.ffmpeg_label.configure(text=tr("ffmpeg trovato ({where})\n{path}\nversione {version}").format(
                                                where=where, path=status.path, version=status.version),
                                            text_color=theme.TEXT)
            else:
                if sys.platform == "win32":
                    missing = tr("ffmpeg NON trovato: scaricalo con il pulsante qui sotto.")
                else:
                    missing = tr("ffmpeg NON trovato: installalo con il gestore di pacchetti del sistema (per esempio sudo apt install ffmpeg) oppure metti un eseguibile ffmpeg in tools/ffmpeg/.")
                self.ffmpeg_label.configure(text=missing, text_color=theme.ERR)

        self.ffmpeg_label.configure(text=tr("Controllo in corso..."), text_color=theme.TEXT_DIM)
        threading.Thread(target=work, daemon=True).start()

    def download_ffmpeg(self) -> None:
        cancel = threading.Event()
        dialog = widgets.ProgressDialog(self, tr("Download di ffmpeg"), self.fonts, on_cancel=cancel.set)

        def progress(label: str, done: int, total: int) -> None:
            fraction = done / total if total else 0.0
            text = (tr("{label}: {done:.1f} MB / {total:.1f} MB").format(label=label, done=done / 1e6, total=total / 1e6)
                    if total else tr("{label}: {done:.1f} MB").format(label=label, done=done / 1e6))
            self.post(lambda: dialog.set(text, fraction))

        def work() -> None:
            try:
                tools.install(progress, cancel)
                self.post(lambda: done(None))
            except tools.Cancelled:
                self.post(lambda: done("annullato"))
            except Exception as exc:  # noqa: BLE001
                message = str(exc)        # exc sparisce alla fine del blocco except
                self.post(lambda: done(message))

        def done(error: str | None) -> None:
            dialog.close()
            self._refresh_ffmpeg_status()
            if error is None:
                messagebox.showinfo("ffmpeg", tr("ffmpeg scaricato in tools/ffmpeg."), self)
            elif error != "annullato":
                messagebox.showerror(tr("Download fallito"), error, self)

        threading.Thread(target=work, daemon=True).start()

    def _refresh_vit_status(self) -> None:
        model = tools.vit_model()
        if model is not None:
            self.vit_label.configure(text=tr("VitTrack presente: l'inseguimento lo usa.\n{model}").format(model=model),
                                    text_color=theme.TEXT)
        else:
            self.vit_label.configure(text=tr("VitTrack non scaricato: l'inseguimento usa il confronto a modello, "
                                             "che puo' perdere il soggetto dietro un ostacolo."), text_color=theme.WARN)

    def download_vit(self) -> None:
        cancel = threading.Event()
        dialog = widgets.ProgressDialog(self, tr("Download di VitTrack"), self.fonts, on_cancel=cancel.set)

        def progress(label: str, done: int, total: int) -> None:
            fraction = done / total if total else 0.0
            text = (tr("{label}: {done:.2f} MB / {total:.2f} MB").format(label=label, done=done / 1e6, total=total / 1e6)
                    if total else tr("{label}: {done:.2f} MB").format(label=label, done=done / 1e6))
            self.post(lambda: dialog.set(text, fraction))

        def work() -> None:
            try:
                tools.install_vit(progress, cancel)
                self.post(lambda: done(None))
            except tools.Cancelled:
                self.post(lambda: done("annullato"))
            except Exception as exc:  # noqa: BLE001
                message = str(exc)        # exc sparisce alla fine del blocco except
                self.post(lambda: done(message))

        def done(error: str | None) -> None:
            dialog.close()
            self._refresh_vit_status()
            if error is None:
                messagebox.showinfo("VitTrack", tr("Modello scaricato in tools/vittrack: l'inseguimento ora lo usa."), self)
            elif error != "annullato":
                messagebox.showerror(tr("Download fallito"), error, self)

        threading.Thread(target=work, daemon=True).start()

    def _open_folder(self, path) -> None:
        try:
            os.makedirs(path, exist_ok=True)
            tools.open_folder(path)
        except OSError as exc:
            messagebox.showerror(tr("Cartella"), str(exc), self)

    # --------------------------------------------------------------- piede

    def _build_footer(self) -> None:
        footer = ctk.CTkFrame(self, fg_color=theme.BG, corner_radius=0, height=26)
        footer.grid(row=3, column=0, sticky="ew")
        footer.grid_propagate(False)
        footer.grid_columnconfigure(0, weight=1)
        footer.grid_rowconfigure(0, weight=1)
        self.status_label = ctk.CTkLabel(footer, text=tr("Pronto."), font=self.fonts.small, text_color=theme.TEXT_SOFT, anchor="w")
        self.status_label.grid(row=0, column=0, sticky="ew", padx=(16, 8))
        self._hints_label = ctk.CTkLabel(footer, text=tr("Spazio riproduci  ·  ← → fotogramma  ·  I / O segna  ·  S taglia  ·  "
                                                         "Canc elimina  ·  Ctrl+Z annulla  ·  Esc annulla disegno"),
                                         font=self.fonts.tiny, text_color=theme.TEXT_FAINT)
        self._hints_label.grid(row=0, column=1, sticky="e", padx=(0, 16))
        self._credits_label = ctk.CTkLabel(footer, text=CREDITS, font=self.fonts.tiny, text_color=theme.TEXT_DIM)
        self._credits_label.grid(row=0, column=2, sticky="e", padx=(0, 16))
        self._footer = footer

    def status(self, text: str) -> None:
        """Messaggio nella barra in basso, accorciato allo spazio libero prima delle scorciatoie."""
        try:
            free = (self._footer.winfo_width() - self._hints_label.winfo_reqwidth()
                    - self._credits_label.winfo_reqwidth() - 16 - 8 - 32 - 16)
            font = self.fonts.small
            if free > 60 and font.measure(text) > free:
                cut = str(text)
                while cut and font.measure(cut + "…") > free:
                    cut = cut[:-1]
                text = cut.rstrip() + "…"
        except (AttributeError, tk.TclError):
            pass
        self.status_label.configure(text=text)

    # ================================================================ avvio e chiusura

    def _startup(self, initial: str | None) -> None:
        path, _source = tools.find()
        if path is None:
            self.show_page("settings")
            if sys.platform == "win32":
                message = tr("ffmpeg non e' stato trovato. Scaricalo dal riquadro FFmpeg della pagina "
                             "Configurazione: senza, non si possono importare ne' esportare video.")
            else:
                message = tr("ffmpeg non e' stato trovato. Installalo con il gestore di pacchetti del sistema "
                             "(per esempio sudo apt install ffmpeg) o copia un eseguibile ffmpeg in "
                             "tools/ffmpeg/: senza, non si possono importare ne' esportare video.")
            messagebox.showwarning("ffmpeg", message, self)
        if initial:
            if initial.lower().endswith(".json"):
                self._load_project(initial)
            elif os.path.isfile(initial):
                self._import_path(initial, at_end=True)
        self.refresh()

    def _on_close(self) -> None:
        if not self._confirm_discard():
            return
        self.stop_play()
        try:
            self.config_store.set("geometry", self.geometry())
            self.config_store.save()
        except tk.TclError:
            pass
        procs.kill_all()
        self.frames.close()
        self.destroy()

    def _confirm_discard(self) -> bool:
        if not self.project.dirty:
            return True
        answer = messagebox.askyesnocancel(tr("Progetto non salvato"), tr("Salvare le modifiche al progetto?"), self,
                                           yes=tr("Salva"), no=tr("Non salvare"))
        if answer is None:
            return False
        if answer:
            return self.save_project()
        return True

    # ================================================================ tastiera

    def _bind_keys(self) -> None:
        def key(event, handler, *args):
            widget = self.focus_get()
            if isinstance(widget, (tk.Entry, tk.Text, ctk.CTkEntry, ctk.CTkTextbox)) or \
                    widget.__class__.__name__ in ("Entry", "Text"):
                return None
            handler(*args)
            return "break"

        self.bind("<space>", lambda e: key(e, self.toggle_play))
        self.bind("<Shift-space>", lambda e: key(e, self.toggle_play_reverse))
        self.bind("<Control-Left>", lambda e: key(e, self.step_frames, -10))
        self.bind("<Control-Right>", lambda e: key(e, self.step_frames, 10))
        self.bind("<Left>", lambda e: key(e, self.step_frames, -1))
        self.bind("<Right>", lambda e: key(e, self.step_frames, 1))
        self.bind("<Shift-Left>", lambda e: key(e, self.step_seconds, -1.0))
        self.bind("<Shift-Right>", lambda e: key(e, self.step_seconds, 1.0))
        self.bind("<Home>", lambda e: key(e, self.seek, 0.0))
        self.bind("<End>", lambda e: key(e, lambda: self.seek(self.project.duration())))
        self.bind("<i>", lambda e: key(e, self.mark_in_here))
        self.bind("<o>", lambda e: key(e, self.mark_out_here))
        self.bind("<s>", lambda e: key(e, self.split_at_playhead))
        self.bind("<f>", lambda e: key(e, self.add_freeze))
        self.bind("<v>", lambda e: key(e, self.set_speed))
        self.bind("<t>", lambda e: key(e, self.start_draw, "text"))
        self.bind("<r>", lambda e: key(e, self.start_draw, "box"))
        self.bind("<e>", lambda e: key(e, self.start_draw, "oval"))
        self.bind("<k>", lambda e: key(e, self.start_draw, "pixelate_oval"))
        self.bind("<a>", lambda e: key(e, self.start_draw, "arrow"))
        self.bind("<z>", lambda e: key(e, self.start_draw, "zoom"))
        self.bind("<Z>", lambda e: key(e, self.start_draw, "zoom_oval"))
        self.bind("<p>", lambda e: key(e, self.start_draw, "pixelate"))
        self.bind("<l>", lambda e: key(e, self.add_logo))
        self.bind("<Delete>", lambda e: key(e, self.delete_selection))
        self.bind("<Escape>", lambda e: self.cancel_mode())
        self.bind("<Control-z>", lambda e: key(e, self.undo))
        self.bind("<Control-y>", lambda e: key(e, self.redo))
        self.bind("<Control-s>", lambda e: self.save_project())
        self.bind("<Control-Shift-S>", lambda e: self.save_project_as())
        self.bind("<Control-o>", lambda e: self.open_project())
        self.bind("<Control-n>", lambda e: self.new_project())
        self.bind("<Control-i>", lambda e: self.import_video())
        self.bind("<Control-e>", lambda e: self.export())

    # ================================================================ stato e ridisegno

    def push_undo(self) -> None:
        self.undo_stack.append(self.project.snapshot())
        if len(self.undo_stack) > 60:
            self.undo_stack.pop(0)
        self.redo_stack.clear()

    def undo(self) -> None:
        if not self.undo_stack:
            self.status(tr("Niente da annullare."))
            return
        self.redo_stack.append(self.project.snapshot())
        self.project.restore(self.undo_stack.pop())
        self._after_restore()

    def redo(self) -> None:
        if not self.redo_stack:
            return
        self.undo_stack.append(self.project.snapshot())
        self.project.restore(self.redo_stack.pop())
        self._after_restore()

    def _after_restore(self) -> None:
        self.playhead = min(self.playhead, self.project.duration())
        self.select(None, None)
        self.refresh()

    def refresh(self, preview: bool = True) -> None:
        """Ridisegna timeline, anteprima ed etichette dopo una modifica del progetto."""
        self.project.sync_full()
        total = self.project.duration()
        if self.playhead > total:
            self.playhead = total
        self.timeline.project = self.project
        self.timeline.set_range(self.mark_in, self.mark_out)
        self.timeline.schedule()
        self.duration_label.configure(text=f" / {media.format_time(total)}")
        self.project_label.configure(text=(os.path.basename(self.project.path) if self.project.path else tr("nuovo"))
                                     + (" *" if self.project.dirty else ""))
        self.project_label.configure(text_color=theme.WARN if self.project.dirty or not self.project.path else theme.TEXT)
        if self.project.clips:
            self.state_dot.configure(text_color=theme.OK)
            self.state_label.configure(text=tr("{width}x{height}  {fps:g} fps  {clips} clip  {duration}").format(
                width=self.project.width, height=self.project.height, fps=self.project.fps,
                clips=len(self.project.clips), duration=media.format_time(total, ms=False)))
        else:
            self.state_dot.configure(text_color=theme.TEXT_FAINT)
            self.state_label.configure(text=tr("Nessun video"))
        if self.mark_in is not None or self.mark_out is not None:
            a = media.format_time(self.mark_in, ms=False) if self.mark_in is not None else tr("inizio")
            b = media.format_time(self.mark_out, ms=False) if self.mark_out is not None else tr("fine")
            self.range_label.configure(text=f"{a} - {b}")
        else:
            self.range_label.configure(text="")
        # l'elemento selezionato puo' essere sparito
        if self.selected_kind and self._selected_obj() is None:
            self.select(None, None)
        elif self.selected_kind:
            self.panel.refresh()
        if preview:
            self.schedule_preview()

    def _selected_obj(self) -> dict | None:
        if self.selected_kind == "clip":
            return self.project.clip_by_id(self.selected_id)
        if self.selected_kind == "effect":
            return self.project.effect_by_id(self.selected_id)
        if self.selected_kind == "audio":
            return self.project.audio_track_by_id(self.selected_id)
        if self.selected_kind == "oaudio":
            return self.project.clip_by_id(self.selected_id)
        if self.selected_kind == "oaudio_all":
            return {"id": "orig"} if self.project.clips else None
        return None

    def select(self, kind: str | None, item_id: str | None, seek: bool = True) -> None:
        self.selected_kind, self.selected_id = kind, item_id
        obj = self._selected_obj()
        if obj is None:
            self.selected_kind = self.selected_id = None
        self.timeline.set_selection(self.selected_kind, self.selected_id)
        self.panel.show(self.selected_kind, obj)
        self.preview.set_selected(obj if self.selected_kind == "effect" else None)
        # il cursore si porta sull'effetto solo se e' davvero fuori (sulla fine, dopo allunga/interrompi, resta li')
        eps = 0.5 / max(1.0, self.project.fps)
        if seek and self.selected_kind == "effect" and obj is not None and                 not (obj["start"] - eps <= self.playhead <= obj["end"] + eps):
            self.seek(obj["start"])

    # --------------------------------------------------------------- anteprima: divisore e finestra a parte

    def _make_preview(self, master) -> PreviewView:
        """L'anteprima con i suoi collegamenti e il pulsante per staccarla o riattaccarla."""
        preview = PreviewView(master, on_draw=self._on_drawn, on_select=self._on_preview_select,
                              on_edit_start=lambda fx: self.push_undo(), on_edit=self._on_preview_edit,
                              on_wheel=self.step_frames, active_effects=lambda: self.project.effects_at(self.playhead))
        preview.on_resize = self.schedule_preview
        preview.on_key = self._preview_key
        preview.on_edit_text = self.edit_text
        detached = master is not self._edit_page
        button = widgets.icon_button(
            preview, self._glyph("attach" if detached else "detach"), G["attach" if detached else "detach"][1], self.toggle_preview_window, self.fonts,
            width=30, tooltip=tr("Riattacca l'anteprima alla finestra principale") if detached
            else tr("Stacca l'anteprima in una finestra a parte (piu' spazio per la timeline)"))
        button.place(relx=1.0, x=-6, y=6, anchor="ne")
        return preview

    def toggle_preview_window(self) -> None:
        """Stacca l'anteprima in una finestra sua, o la rimette al suo posto."""
        self.cancel_mode()
        old = self.preview
        state = (old.selected, old.zoom_shape, old.zoom_factor, old.view_zoom, old._view_center)
        page = self._edit_page
        if self.preview_window is None:
            win = ctk.CTkToplevel(self)
            win.title(f"{APP_NAME} - " + tr("Anteprima"))
            win.configure(fg_color=theme.BG)
            widgets.style_dialog(win)
            geometry = str(self.config_store.get("preview_window") or "")
            if not geometry:
                w, h = max(480, old.winfo_width()), max(320, old.winfo_height())
                geometry = f"{w}x{h + 40}+{self.winfo_rootx() + 60}+{self.winfo_rooty() + 60}"
            win.geometry(geometry)
            win.minsize(320, 240)
            win.protocol("WM_DELETE_WINDOW", self.toggle_preview_window)
            # le scorciatoie della finestra principale valgono anche qui
            for sequence in self.bind():
                win.bind(sequence, self.bind(sequence))
            self.preview_window = win
            self.preview = self._make_preview(win)
            self.preview.pack(fill="both", expand=True, padx=theme.PAD, pady=(6, theme.PAD))
            # senza anteprima la riga di sopra si stringe e la timeline prende lo spazio
            page.grid_rowconfigure(1, weight=1)
            page.grid_rowconfigure(3, weight=3)
            self.status(tr("Anteprima in una finestra a parte: chiudila o usa il pulsante in alto a destra per riattaccarla."))
        else:
            win = self.preview_window
            self.config_store.set("preview_window", win.geometry())
            self.preview_window = None
            self.preview = self._make_preview(page)
            self.preview.grid(row=1, column=0, sticky="nsew", padx=(theme.PAD, theme.GAP))
            page.grid_rowconfigure(1, weight=3)
            page.grid_rowconfigure(3, weight=0)
            win.destroy()
            self.status(tr("Anteprima riattaccata."))
        old.destroy()
        new = self.preview
        new.selected, new.zoom_shape, new.zoom_factor, new.view_zoom, new._view_center = state
        new.set_project_size((self.project.width, self.project.height))
        self.after(80, self.refresh_preview)

    def _sash_press(self, event) -> None:
        room = self.preview.winfo_height() if self.preview_window is None else 0
        self._sash = (event.y_root, self.timeline.winfo_height(), room)

    def _sash_move(self, event) -> None:
        if self._sash is None or self.preview_window is not None:
            return
        y0, h0, room = self._sash
        scale = ctk.ScalingTracker.get_widget_scaling(self.timeline)
        h = h0 + (y0 - event.y_root)
        h = min(max(h, TIMELINE_MIN * scale), h0 + max(0, room - PREVIEW_MIN * scale))
        self.timeline.configure(height=int(h / scale))

    def _sash_release(self, _event, sash) -> None:
        if self._sash is not None:
            self._sash = None
            sash.configure(bg=theme.BG)
            scale = ctk.ScalingTracker.get_widget_scaling(self.timeline)
            self.config_store.set("timeline_height", int(self.timeline.winfo_height() / scale))
            self.config_store.save()

    def _timeline_changed(self) -> None:
        fx = self._selected_obj() if self.selected_kind == "effect" else None
        if fx is not None and fx.get("full") and (fx["start"] > 1e-3 or abs(fx["end"] - self.project.duration()) > 1e-3):
            fx["full"] = False      # spostato o accorciato a mano sulla timeline
        self.refresh()

    def _on_preview_select(self, fx: dict | None) -> None:
        self.select("effect" if fx else None, fx["id"] if fx else None)

    def _on_preview_edit(self, fx: dict, final: bool) -> None:
        self.project.dirty = True
        if final:
            self.refresh()
        else:
            self.panel.refresh()
            self.schedule_preview()

    # --------------------------------------------------------------- anteprima

    def schedule_preview(self) -> None:
        if self._preview_job is None:
            self._preview_job = self.after(8, self.refresh_preview)

    def refresh_preview(self) -> None:
        self._preview_job = None
        self.time_var.set(media.format_time(self.playhead))
        self.preview.time = self.playhead
        if not self.project.clips:
            self.preview.set_frame(None)
            return
        index, clip, local = self.project.locate(self.playhead)
        if clip is None:
            self.preview.set_frame(None)
            return
        self.preview.set_project_size((self.project.width, self.project.height))
        dw, dh = self.preview.display_size()
        src_t = self.project.source_time(clip, local)
        if clip["kind"] == "slide":
            base = overlays.render_slide(clip, dw, dh)
        elif self.playing and self.play_reverse and clip["kind"] == "video":
            # all'indietro: i fotogrammi li legge a blocchi il thread di servizio; se questo non e' ancora
            # pronto l'anteprima resta un istante sul precedente invece di bloccarsi in un seek
            fps_src = float(self.project.source_info(clip["source"]).get("fps") or self.project.fps or 25)
            count = max(8, int(fps_src * 0.8))
            self.frames.read_back(clip["source"], src_t, (dw, dh), count)
            # il blocco dopo si prepara mentre si mostra questo (se questo e' gia' in cache)
            self.frames.read_back(clip["source"], max(0.0, src_t - count / fps_src), (dw, dh), count)
            base = self.frames.get(clip["source"], src_t, fit=(dw, dh), cached_only=True)
            if base is None:
                return
        else:
            base = self.frames.get(clip["source"], src_t, fit=(dw, dh), forward_only=self.playing and not self.play_reverse)
        if base is not None:
            base = self._with_transitions(index, clip, local, base, dw, dh)
        if base is None:
            self.preview.set_frame(None)
            self.status(tr("Fotogramma non leggibile: {file}").format(file=os.path.basename(clip["source"])))
            return
        if self.playing and not self.play_reverse and clip["kind"] == "video":
            self.frames.read_ahead(clip["source"], src_t, fit=(dw, dh))
        scale = dw / self.project.width
        try:
            image = overlays.compose(self.project, self.playhead, base, clip, scale=scale)
        except Exception as exc:  # noqa: BLE001 - un effetto con valori strani non deve bloccare l'anteprima
            self.status(tr("Anteprima: {error}").format(error=exc))
            image = overlays.fit_frame(base, dw, dh)
        self.preview.set_frame(image)

    def _clip_frame(self, clip: dict, local: float, dw: int, dh: int):
        """Fotogramma di una clip a `local` secondi dal suo inizio, anche fuori dai suoi limiti (fusioni)."""
        if clip["kind"] == "slide":
            return overlays.render_slide(clip, dw, dh)
        if clip["kind"] == "freeze":
            return self.frames.get(clip["source"], float(clip["at"]), fit=(dw, dh))
        speed = float(clip.get("speed", 1) or 1)
        limit = self.project.source_duration(clip["source"]) or float(clip["out"])
        fps = max(1.0, float(self.project.source_info(clip["source"]).get("fps") or self.project.fps or 25))
        # oltre la fine la clip resta ferma sul suo ultimo fotogramma (la clip che esce in una fusione)
        limit = min(limit, float(clip["out"]))
        src_t = min(max(0.0, float(clip["in"]) + local * speed), max(0.0, limit - 1.0 / fps))
        return self.frames.get(clip["source"], src_t, fit=(dw, dh))

    def _hold_local(self, clip: dict, local: float) -> float:
        """Il fotogramma su cui la clip che esce resta ferma: l'ultimo prima di `local` (come nell'export)."""
        if clip["kind"] != "video":
            return local
        fps = max(1.0, float(self.project.source_info(clip["source"]).get("fps") or self.project.fps or 25))
        return max(0.0, local - 1.0 / (fps * float(clip.get("speed", 1) or 1)))

    def _with_transitions(self, index: int, clip: dict, local: float, base, dw: int, dh: int):
        """Fusione con la clip vicina e dissolvenze dal/al nero, come nell'esportazione."""
        from PIL import Image
        p = self.project
        dur = clip_duration(clip)
        base = base.convert("RGB")
        d_prev, d_next = p.xfade_after(index - 1), p.xfade_after(index)
        other, weight = None, 0.0
        # la clip che esce resta ferma per tutta la fusione, sul fotogramma di inizio fusione
        if d_prev > 0 and local < d_prev / 2:
            prev = p.clips[index - 1]
            other = self._clip_frame(prev, self._hold_local(prev, clip_duration(prev) - d_prev / 2), dw, dh)
            weight = 0.5 - local / d_prev                        # peso della clip precedente
        elif d_next > 0 and local > dur - d_next / 2:
            if clip["kind"] == "video":
                base = self._clip_frame(clip, self._hold_local(clip, dur - d_next / 2), dw, dh).convert("RGB")
            other = self._clip_frame(p.clips[index + 1], local - dur, dw, dh)
            weight = (local - (dur - d_next / 2)) / d_next        # peso della successiva
        if other is not None and weight > 0:
            other = other.convert("RGB")
            if other.size != base.size:
                other = other.resize(base.size)
            base = Image.blend(base, other, max(0.0, min(1.0, weight)))
        fi, fo = p.fades(clip)
        k = 1.0
        if fi > 0 and local < fi:
            k = local / fi
        if fo > 0 and local > dur - fo:
            k = min(k, (dur - local) / fo)
        if k < 1.0:
            base = Image.blend(Image.new("RGB", base.size, (0, 0, 0)), base, max(0.0, k))
        return base

    def seek(self, t: float) -> None:
        fps = max(1.0, self.project.fps)
        total = self.project.duration()
        self.playhead = min(max(0.0, round(t * fps) / fps), total)
        self.timeline.set_playhead(self.playhead)
        self.timeline.ensure_visible(self.playhead)
        if self.playing:
            # salto durante la riproduzione: orologio e audio ripartono da qui
            self._play_origin = (time.perf_counter(), self.playhead)
            if self._mix_ready_for_play():
                self.player.play(self.playhead)
        self.schedule_preview()

    def step_frames(self, n: int) -> None:
        self.stop_play()
        self.seek(self.playhead + n / max(1.0, self.project.fps))

    def step_seconds(self, s: float) -> None:
        self.stop_play()
        self.seek(self.playhead + s)

    def _time_entered(self, _event=None) -> None:
        value = media.parse_time(self.time_var.get())
        if value is not None:
            self.seek(value)
        self.focus_set()

    def toggle_play(self) -> None:
        if self.playing:
            self.stop_play()
        else:
            self.start_play()

    def toggle_play_reverse(self) -> None:
        if self.playing:
            self.stop_play()
        else:
            self.start_play(reverse=True)

    def start_play(self, reverse: bool = False) -> None:
        if not self.project.clips:
            return
        if not reverse and self.playhead >= self.project.duration() - 1e-6:
            self.playhead = 0.0
        if reverse and self.playhead <= 1e-6:
            self.playhead = self.project.duration()
        self.playing = True
        self.play_reverse = reverse
        self.timeline.set_playing(True)
        pause = self._glyph("pause") if self._has_icons else "||"
        if reverse:
            self.reverse_button.configure(text="❚❚")
        else:
            self.play_button.configure(text=pause)
        self._play_origin = (time.perf_counter(), self.playhead)
        if not reverse:
            self._start_audio()             # all'indietro niente audio
        self._tick()

    def stop_play(self) -> None:
        if self._play_job is not None:
            self.after_cancel(self._play_job)
            self._play_job = None
        self.player.stop()
        if self.playing:
            self.playing = False
            self.frames.read_ahead(None)
            self.timeline.set_playing(False)
            self.play_button.configure(text=self._glyph("play") if self._has_icons else ">")
            self.reverse_button.configure(text="◀")
        self.play_reverse = False

    def _tick(self) -> None:
        self._play_job = None
        if not self.playing:
            return
        started, origin = self._play_origin
        reverse = self.play_reverse
        t = origin + (time.perf_counter() - started) * (-1.0 if reverse else 1.0)
        heard = None if reverse else self.player.position()
        if heard is not None:
            t = heard                       # l'audio fa da orologio: immagini e suono restano insieme
        elif not reverse and self._mix_ready_for_play():
            self.player.play(t)             # il mix e' pronto ora: l'audio si aggancia da qui
        total = self.project.duration()
        if reverse and t <= 0.0:
            self.playhead = 0.0
            self.timeline.set_playhead(self.playhead)
            self.refresh_preview()
            self.stop_play()
            return
        if t >= total:
            self.playhead = total
            self.timeline.set_playhead(self.playhead)
            self.refresh_preview()
            self.stop_play()
            return
        fps = max(1.0, self.project.fps)
        self.playhead = round(t * fps) / fps
        self.timeline.set_playhead(self.playhead)
        self.timeline.ensure_visible(self.playhead)
        before = time.perf_counter()
        self.refresh_preview()
        spent = time.perf_counter() - before
        frame_time = 1.0 / fps
        if spent > 0.12:
            # un seek (cambio di clip) ha fermato tutto: l'orologio non deve saltare avanti
            self._play_origin = (started + spent - frame_time, origin)
        if not reverse:
            self._prefetch_next_clip()
        self._play_job = self.after(max(1, int((frame_time - min(spent, frame_time)) * 1000)), self._tick)

    # --------------------------------------------------------------- audio dell'anteprima

    def _mix_key(self) -> str:
        """Quello che cambia il suono: clip, tracce audio, volumi e dissolvenze dell'audio originale."""
        import json
        p = self.project
        return json.dumps([p.clips, p.audio_tracks, p.original_volume, p.original_muted, p.original_fade_in,
                           p.original_fade_out], sort_keys=True, default=str)

    def _mix_ready_for_play(self) -> bool:
        return self.playing and self._mix_samples_key == self._mix_key() and self.player.samples is not None

    def _start_audio(self) -> None:
        """Avvia l'audio dal cursore; se il mix non e' aggiornato lo prepara in background (ffmpeg)."""
        if not audio.available():
            return
        key = self._mix_key()
        if self._mix_samples_key == key and self.player.samples is not None:
            self.player.play(self.playhead)
            return
        if self._mix_job == key:
            return                                   # gia' in preparazione
        self._mix_job = key
        snapshot = Project.from_dict(self.project.to_dict())
        snapshot.sync_full()
        folder = os.path.join(tempfile.gettempdir(), "editsimple-audio")
        os.makedirs(folder, exist_ok=True)
        path = os.path.join(folder, f"mix_{os.getpid()}.wav")

        def work() -> None:
            try:
                render.Exporter(snapshot, path, audio_only=True).run()
                samples = audio.load_wav(path)
                self.post(lambda: done(samples, None))
            except Exception as exc:  # noqa: BLE001 - l'anteprima resta muta, il montaggio continua
                message = str(exc)        # exc sparisce alla fine del blocco except
                self.post(lambda: done(None, message))

        def done(samples, error) -> None:
            if self._mix_job == key:
                self._mix_job = None
            if error:
                self.status(tr("Audio dell'anteprima non disponibile: {error}").format(error=error[:120]))
                return
            self.player.set_samples(samples)
            self._mix_samples_key = key

        threading.Thread(target=work, daemon=True).start()

    def _prefetch_next_clip(self) -> None:
        """Vicino alla fine della clip, prepara in background il primo fotogramma della successiva."""
        index, clip, local = self.project.locate(self.playhead)
        if clip is None or index is None or index + 1 >= len(self.project.clips):
            return
        remaining = clip_duration(clip) - local
        if remaining > 1.5:
            return
        nxt = self.project.clips[index + 1]
        if nxt["id"] == self._prefetched or nxt["kind"] == "slide":
            return
        self._prefetched = nxt["id"]
        self.frames.prefetch(nxt["source"], self.project.source_time(nxt, 0.0), fit=self.preview.display_size())

    # ================================================================ progetto

    def new_project(self) -> None:
        if not self._confirm_discard():
            return
        self.stop_play()
        self.project = Project()
        self.undo_stack.clear()
        self.redo_stack.clear()
        self.playhead = 0.0
        self.mark_in = self.mark_out = None
        self.frames.close()
        self.timeline.set_project(self.project)
        self.select(None, None)
        self.refresh()
        self.status(tr("Nuovo progetto."))

    def open_project(self) -> None:
        if not self._confirm_discard():
            return
        path = filedialog.askopenfilename(title=tr("Apri progetto"), filetypes=_filetypes(PROJECT_TYPES), parent=self,
                                          initialdir=self.config_store.get("last_project_dir") or None)
        if path:
            self._load_project(path)

    def _load_project(self, path: str) -> None:
        try:
            project = Project.load(path)
        except (OSError, ValueError, KeyError) as exc:
            messagebox.showerror(tr("Progetto"), tr("Impossibile aprire il progetto:\n{error}").format(error=exc), self)
            return
        missing = [s for s in {c["source"] for c in project.clips} | {t["source"] for t in project.audio_tracks}
                   if s and not os.path.isfile(s)]
        self.stop_play()
        self.project = project
        self.undo_stack.clear()
        self.redo_stack.clear()
        self.playhead = 0.0
        self.mark_in = self.mark_out = None
        self.frames.close()
        self.timeline.set_project(project)
        self.select(None, None)
        self.config_store.set("last_project_dir", os.path.dirname(path))
        self.config_store.add_recent(path)
        self.config_store.save()
        self.refresh()
        self.status(tr("Progetto aperto: {file}").format(file=os.path.basename(path)))
        if missing:
            messagebox.showwarning(tr("File mancanti"), tr("Questi file non si trovano piu':\n\n{files}").format(
                files="\n".join(missing)), self)

    def save_project(self) -> bool:
        if not self.project.path:
            return self.save_project_as()
        try:
            self.project.save()
        except OSError as exc:
            messagebox.showerror(tr("Salvataggio"), str(exc), self)
            return False
        self.refresh(preview=False)
        self.status(tr("Progetto salvato: {path}").format(path=self.project.path))
        return True

    def save_project_as(self) -> bool:
        initial = os.path.dirname(self.project.path) if self.project.path else (self.config_store.get("last_project_dir") or None)
        path = filedialog.asksaveasfilename(title=tr("Salva progetto"), defaultextension=".json", filetypes=_filetypes(PROJECT_TYPES),
                                            parent=self, initialdir=initial,
                                            initialfile=os.path.basename(self.project.path) if self.project.path else "progetto.json")
        if not path:
            return False
        self.project.path = path
        self.config_store.set("last_project_dir", os.path.dirname(path))
        self.config_store.add_recent(path)
        self.config_store.save()
        return self.save_project()

    # ================================================================ clip

    def import_video(self) -> None:
        path = filedialog.askopenfilename(title=tr("Importa video"), parent=self,
                                          filetypes=[(tr("Video"), media.VIDEO_EXTENSIONS), (tr("Tutti i file"), "*.*")],
                                          initialdir=self.config_store.get("last_video_dir") or None)
        if not path:
            return
        self.config_store.set("last_video_dir", os.path.dirname(path))
        self.config_store.save()
        at_end = True
        if self.project.clips:
            answer = messagebox.askyesnocancel(tr("Dove inserire il video?"),
                                               tr("{file}\n\nAggiungerlo in coda alla timeline "
                                                  "oppure inserirlo al cursore ({time})?").format(
                                                   file=os.path.basename(path), time=media.format_time(self.playhead)),
                                               self, yes=tr("In coda"), no=tr("Al cursore"))
            if answer is None:
                return
            at_end = bool(answer)
        self._import_path(path, at_end=at_end)

    def _import_path(self, path: str, at_end: bool) -> None:
        self.status(tr("Lettura del video..."))
        self.update_idletasks()
        try:
            info = media.probe(path)
        except media.MediaError as exc:
            messagebox.showerror(tr("Importazione"), str(exc), self)
            self.status(tr("Pronto."))
            return
        if not info.get("has_video"):
            messagebox.showerror(tr("Importazione"), tr("Il file non contiene video. Per l'audio usa il pulsante Audio."), self)
            return
        self.push_undo()
        self.project.add_source(path, info)
        if not self.project.clips:
            self.project.width, self.project.height = int(info["width"]), int(info["height"])
            self.project.fps = float(info["fps"]) if info["fps"] > 0 else 25.0
        clip = self.project.new_video_clip(path)
        if at_end or not self.project.clips:
            self.project.append_clips([clip])
        else:
            self.project.insert_clips(self.playhead, [clip])
        self.refresh()
        self.timeline.zoom_fit()
        self.select("clip", clip["id"])
        imported = (tr("Importato {file}: {width}x{height}, {fps:g} fps, {duration}") if info["has_audio"] else
                    tr("Importato {file}: {width}x{height}, {fps:g} fps, {duration}, senza audio"))
        self.status(imported.format(file=os.path.basename(path), width=info["width"], height=info["height"],
                                    fps=info["fps"], duration=media.format_time(info["duration"], ms=False)))

    def add_audio(self) -> None:
        if not self.project.clips:
            messagebox.showinfo(tr("Audio"), tr("Importa prima un video."), self)
            return
        path = filedialog.askopenfilename(title=tr("Aggiungi traccia audio"), parent=self,
                                          filetypes=[(tr("Audio"), media.AUDIO_EXTENSIONS), (tr("Tutti i file"), "*.*")],
                                          initialdir=self.config_store.get("last_audio_dir") or None)
        if not path:
            return
        self.config_store.set("last_audio_dir", os.path.dirname(path))
        self.config_store.save()
        try:
            info = media.probe(path)
        except media.MediaError as exc:
            messagebox.showerror(tr("Audio"), str(exc), self)
            return
        if not info.get("has_audio"):
            messagebox.showerror(tr("Audio"), tr("Il file non contiene audio."), self)
            return
        self.push_undo()
        track = self.project.add_audio_track(path, self.playhead, info)
        self.refresh()
        self.select("audio", track["id"])
        self.status(tr("Traccia audio aggiunta: {name} ({duration})").format(
            name=track["name"], duration=media.format_time(info["duration"], ms=False)))

    def split_at_playhead(self) -> None:
        if not self.project.clips:
            return
        self.push_undo()
        before = len(self.project.clips)
        self.project.split_at(self.playhead)
        if len(self.project.clips) == before:
            self.undo_stack.pop()
            self.status(tr("Il cursore e' gia' su un confine fra clip."))
            return
        self.refresh()
        if self.selected_kind == "oaudio":
            # si lavora sull'audio: resta selezionato l'audio del pezzo al cursore
            _i, clip, _l = self.project.locate(self.playhead)
            if clip is not None and clip["kind"] == "video":
                self.select("oaudio", clip["id"])
        self.status(tr("Clip tagliata a {time}.").format(time=media.format_time(self.playhead)))

    def delete_audio_range(self, a: float, b: float) -> None:
        """Toglie solo l'audio originale fra a e b (il video resta): taglia ai due estremi e spegne i pezzi."""
        self.push_undo()
        ia = self.project.split_at(a)
        ib = self.project.split_at(b)
        pieces = [c for c in self.project.clips[ia:ib] if c["kind"] == "video"]
        for clip in pieces:
            clip["audio"] = False
        self.project.dirty = True
        self.mark_in = self.mark_out = None
        self.refresh()
        if pieces:
            self.select("oaudio", pieces[0]["id"])
        self.status(tr("Audio originale tolto fra {start} e {end} (il video resta).").format(
            start=media.format_time(a), end=media.format_time(b)))

    def delete_selection(self) -> None:
        if (self.selected_kind in ("oaudio", "oaudio_all") and self.mark_in is not None and self.mark_out is not None
                and self.mark_out > self.mark_in):
            # con l'audio selezionato, IN-OUT toglie solo l'audio di quel tratto
            self.delete_audio_range(self.mark_in, self.mark_out)
            return
        fx_id, chosen = self.timeline.key_sel
        if chosen and self.selected_kind == "effect" and self.selected_id == fx_id:
            fx = self.project.effect_by_id(fx_id)
            if fx is not None:
                self.delete_keys(fx, sorted(float(t) for t in chosen))
                return
        if self.mark_in is not None and self.mark_out is not None and self.mark_out > self.mark_in:
            a, b = self.mark_in, self.mark_out
            self.push_undo()
            self.project.delete_range(a, b)
            self.mark_in = self.mark_out = None
            self.playhead = min(a, self.project.duration())
            self.select(None, None)
            self.refresh()
            self.status(tr("Eliminata la porzione {start} - {end}.").format(start=media.format_time(a), end=media.format_time(b)))
            return
        if self.selected_kind == "clip":
            self.delete_clip(self.selected_id)
        elif self.selected_kind == "oaudio":
            self.delete_clip_audio(self.selected_id)
        elif self.selected_kind == "oaudio_all":
            self.push_undo()
            self.project.original_muted = True
            self.project.dirty = True
            self.refresh()
            self.select("oaudio_all", "orig")
            self.status(tr("Audio originale spento (il video resta): riaccendilo dal pannello o con Ctrl+Z."))
        elif self.selected_kind == "effect":
            self.delete_effect(self.selected_id)
        elif self.selected_kind == "audio":
            self.delete_audio_track(self.selected_id)
        else:
            self.status(tr("Segna IN e OUT (tasti I e O) oppure seleziona un elemento da eliminare."))

    def delete_clip_audio(self, clip_id: str) -> None:
        """Toglie l'audio originale di un pezzo (il video resta): per un tratto, prima si taglia con S."""
        clip = self.project.clip_by_id(clip_id)
        if clip is None or clip["kind"] != "video":
            return
        self.push_undo()
        clip["audio"] = False
        self.project.dirty = True
        self.refresh()
        self.select("oaudio", clip_id)
        self.status(tr("Audio di questo pezzo eliminato (il video resta). Ctrl+Z per riaverlo."))

    def delete_clip(self, clip_id: str) -> None:
        index = self.project.clip_index(clip_id)
        if index < 0:
            return
        self.push_undo()
        self.project.delete_clip(index)
        self.select(None, None)
        self.refresh()
        self.status(tr("Clip eliminata."))

    def delete_effect(self, effect_id: str) -> None:
        self.push_undo()
        self.project.remove_effect(effect_id)
        self.select(None, None)
        self.refresh()

    def delete_audio_track(self, track_id: str) -> None:
        self.push_undo()
        self.project.remove_audio_track(track_id)
        self.select(None, None)
        self.refresh()

    def add_slide(self) -> None:
        """Slide di apertura o di chiusura: sfondo a tinta unita, logo e testo; il resto nel pannello."""
        if not self.project.clips:
            messagebox.showinfo(tr("Slide"), tr("Importa prima un video: la slide prende la sua misura."), self)
            return
        cfg = self.config_store
        # le opzioni si riconoscono per uguaglianza con queste etichette, non dal testo: valgono in ogni lingua
        opening_option = tr("Apertura (all'inizio)")
        cursor_option = tr("Al cursore ({time})").format(time=media.format_time(self.playhead))
        closing_option = tr("Chiusura (alla fine)")
        fields = [
            {"key": "role", "label": tr("Dove"), "kind": "choice",
             "options": [opening_option, cursor_option, closing_option], "default": opening_option},
            {"key": "seconds", "label": tr("Durata (secondi)"), "kind": "float", "default": f"{cfg.get('slide_seconds'):g}",
             "min": 0.2, "max": 600},
        ]
        result = widgets.ask_form(self, tr("Slide"), fields, self.fonts, ok_text=tr("Crea"),
                                  intro=tr("La slide e' un fondo a tinta unita (il colore si sceglie nel pannello). "
                                           "Testi e immagini si aggiungono sopra con gli strumenti Testo e Immagine."))
        if not result:
            return
        closing = result["role"] == closing_option
        at = self.playhead if result["role"] == cursor_option else None
        slide = {"duration": max(0.2, float(result["seconds"])), "bg": str(cfg.get("slide_bg") or "#0B1220")}
        self.stop_play()
        self.push_undo()
        self.project.insert_slide(slide, closing, at)
        cfg.set("slide_seconds", slide["duration"])
        cfg.save()
        self.refresh()
        self.select("clip", slide["id"])
        self.seek(self.project.clip_start(self.project.clip_index(slide["id"])))
        if closing:
            self.status(tr("Slide di chiusura aggiunta alla fine: regolala nel pannello a destra."))
        elif at is not None:
            self.status(tr("Slide aggiunta a {time}: regolala nel pannello a destra.").format(time=media.format_time(at)))
        else:
            self.status(tr("Slide di apertura aggiunta all'inizio: regolala nel pannello a destra."))

    def add_freeze(self) -> None:
        if not self.project.clips:
            return
        result = widgets.ask_form(self, tr("Fermo immagine"), [
            {"key": "seconds", "label": tr("Durata (secondi)"), "kind": "float", "default": f"{self.config_store.get('freeze_seconds'):g}",
             "min": 0.1, "max": 600, "help": tr("Il fotogramma a {time} resta fermo per questo tempo; "
                                                "cio' che segue scorre in avanti.").format(time=media.format_time(self.playhead))}],
            self.fonts, ok_text=tr("Inserisci"))
        if not result:
            return
        self.push_undo()
        freeze = self.project.insert_freeze(self.playhead, result["seconds"])
        self.config_store.set("freeze_seconds", result["seconds"])
        self.config_store.save()
        self.refresh()
        if freeze is not None:
            self.select("clip", freeze["id"])
        self.status(tr("Fermo immagine di {seconds:g} s inserito.").format(seconds=result["seconds"]))

    def set_speed(self) -> None:
        if not self.project.clips:
            return
        a, b = self.mark_in, self.mark_out
        if a is None or b is None or b <= a:
            if self.selected_kind == "clip":
                index = self.project.clip_index(self.selected_id)
                a = self.project.clip_start(index)
                b = a + clip_duration(self.project.clips[index])
            else:
                messagebox.showinfo(tr("Velocita'"), tr("Segna prima la porzione con IN e OUT (tasti I e O), "
                                                        "oppure seleziona una clip."), self)
                return
        last = speed_text(self.config_store.get("speed_last") or 4)
        result = widgets.ask_form(self, tr("Velocita'"), [
            {"key": "speed", "label": tr("Velocita'"), "kind": "choice", "options": [speed_text(s) for s in SPEEDS], "default": last},
            {"key": "clock", "label": tr("Mostra l'icona dell'orologio con le lancette e la velocita' sotto"), "kind": "check",
             "default": bool(self.config_store.get("speed_clock"))}],
            self.fonts, ok_text=tr("Applica"),
            intro=tr("Porzione {start} - {end}. Da 2x in su accelera, 0.5x e 0.25x "
                     "rallentano (la porzione dura il doppio o il quadruplo); con 1x si torna alla velocita' normale.").format(
                start=media.format_time(a), end=media.format_time(b)))
        if not result:
            return
        factor = speed_value(result["speed"])
        self.push_undo()
        self.project.set_speed(a, b, factor, bool(result["clock"]))
        self.config_store.set("speed_clock", bool(result["clock"]))
        self.config_store.set("speed_last", factor)
        self.config_store.save()
        self.mark_in = a
        self.mark_out = a + (b - a) / factor
        self.select(None, None)
        self.refresh()
        self.status(tr("Velocita' {speed} applicata fra {start} e {end}.").format(
            speed=speed_text(factor), start=media.format_time(a), end=media.format_time(b)))

    # --------------------------------------------------------------- segnaposto

    def mark_in_here(self) -> None:
        self.mark_in = self.playhead
        if self.mark_out is not None and self.mark_out <= self.mark_in:
            self.mark_out = None
        self.refresh(preview=False)

    def mark_out_here(self) -> None:
        self.mark_out = self.playhead
        if self.mark_in is not None and self.mark_in >= self.mark_out:
            self.mark_in = None
        self.refresh(preview=False)

    def clear_marks(self) -> None:
        self.mark_in = self.mark_out = None
        self.refresh(preview=False)

    # ================================================================ effetti

    def start_draw(self, mode: str) -> None:
        if not self.project.clips:
            messagebox.showinfo(tr("Effetti"), tr("Importa prima un video."), self)
            return
        self.stop_play()
        self._pixel_shape = "oval" if mode == "pixelate_oval" else "rect"
        if mode == "pixelate_oval":
            mode = "pixelate"
        self._zoom_shape = "oval" if mode == "zoom_oval" else "rect"
        if mode == "zoom_oval":
            mode = "zoom"
        self.preview.zoom_shape = self._zoom_shape
        if mode == "zoom":
            factor = int(self.config_store.get("zoom_factor") or 2)
            self.preview.set_zoom_factor(factor if factor in overlays.ZOOM_FACTORS else 2)
        self.preview.set_mode(mode)
        name = tr(EFFECT_NAMES.get(mode, mode))
        if mode == "pixelate":
            name = tr("Pixel ovale") if self._pixel_shape == "oval" else tr("Pixel rettangolare")
        if mode == "zoom":
            name = (tr("Zoom ovale (rettangolo sull'oggetto, poi clic dove mettere il riquadro)") if self._zoom_shape == "oval"
                    else tr("Zoom (rettangolo sull'oggetto, poi clic dove mettere il riquadro)"))
        self.mode_label.configure(text=tr("Disegna: {effect}  (Esc annulla)").format(effect=name))

    def add_logo(self) -> None:
        """Logo e testo dell'operatore dalla configurazione, fermi nell'angolo scelto.

        Senza porzione IN-OUT coprono tutto il video (anche se poi si allunga o si accorcia).
        """
        if not self.project.clips:
            messagebox.showinfo(tr("Logo"), tr("Importa prima un video."), self)
            return
        cfg = self.config_store
        path = str(cfg.get("logo_path") or "")
        text = str(cfg.get("operator_text") or "").strip()
        if overlays.load_logo(path) is None:
            path = ""
        if not path and not text:
            messagebox.showinfo(tr("Logo"), tr("Carica l'immagine del logo e scrivi il testo dell'operatore nella pagina "
                                               "Configura, poi premi di nuovo Logo."), self)
            self.show_page("settings")
            return
        self.stop_play()
        W, H = self.project.width, self.project.height
        a, b = self.mark_in, self.mark_out
        full = a is None or b is None or b - a < MIN_LEN
        start, end = (0.0, self.project.duration()) if full else (a, b)
        fx = {"type": "logo", "start": start, "end": end, "full": full, "x": 0, "y": 0,
              "logo": path, "w": max(8, int(round(W * float(cfg.get("logo_width") or 12) / 100))),
              "text": text, "size": max(8, int(round(min(W, H) * float(cfg.get("operator_size") or 3.5) / 100))),
              "color": str(cfg.get("operator_color") or "#FFFFFF"), "layout": str(cfg.get("logo_layout") or "right"),
              "shadow": True, "font": default_font(), "corner": str(cfg.get("logo_corner") or "bottom-right"),
              "bg": bool(cfg.get("logo_bg")), "bg_color": str(cfg.get("logo_bg_color") or "#000000"),
              "bg_alpha": float(cfg.get("logo_bg_alpha")), "bg_radius": float(cfg.get("logo_bg_radius"))}
        self.place_logo(fx)
        self.push_undo()
        self.project.add_effect(fx)
        self.refresh()
        self.select("effect", fx["id"])
        if full:
            self.status(tr("Logo e operatore aggiunti per tutto il video: trascinali sull'anteprima o regolali nel pannello."))
        else:
            self.status(tr("Logo e operatore aggiunti fra {start} e {end}: trascinali sull'anteprima o regolali nel pannello.")
                        .format(start=media.format_time(a), end=media.format_time(b)))

    def place_logo(self, fx: dict) -> None:
        """Mette logo e testo nell'angolo `corner` dell'effetto, alla distanza dai bordi della configurazione."""
        W, H = self.project.width, self.project.height
        margin = int(round(min(W, H) * float(self.config_store.get("logo_margin") or 3.0) / 100))
        image, _x, _y = overlays.render_logo(fx)
        room_w, room_h = W - 2 * margin, H - 2 * margin
        if image.width > room_w or image.height > room_h:
            # testo lungo o video verticale: logo e testo si riducono insieme per stare nel fotogramma
            k = min(room_w / image.width, room_h / image.height)
            fx["w"] = max(8, int(fx["w"] * k))
            fx["size"] = max(6, int(fx["size"] * k))
            image, _x, _y = overlays.render_logo(fx)
        fx["x"], fx["y"] = overlays.corner_position(image, fx.get("corner") or "bottom-right", W, H, margin)

    # --------------------------------------------------------------- testo e immagine

    def _text_values(self) -> dict:
        cfg = self.config_store
        return {"text": "", "align": cfg.get("text_align") or "center",
                "size": int(cfg.get("text_size") or max(24, self.project.height // 18)),
                "color": cfg.get("text_color") or "#FFFFFF", "shadow": bool(cfg.get("text_shadow")),
                "bg": bool(cfg.get("text_bg")), "center": bool(cfg.get("text_center"))}

    def _remember_text_style(self, values: dict) -> None:
        cfg = self.config_store
        for key in ("align", "size", "color", "shadow", "bg", "center"):
            cfg.set("text_" + key, values[key])
        cfg.save()

    def _create_text(self, fx: dict) -> None:
        """Testo: si scrive in una finestra (piu' righe, allineamento, misura, colore), poi va dove si e' cliccato."""
        values = widgets.ask_text(self, self.fonts, self._text_values(), tr("Nuovo testo"))
        if not values:
            return
        self._remember_text_style(values)
        center = values.pop("center")
        fx.update(values, font=default_font(), bg_color="#000000", bg_alpha=0.55,
                  bg_radius=float(self.config_store.get("round_text")))
        if center:
            self._center_fx(fx, "x")
        self.push_undo()
        self.project.add_effect(fx)
        self.refresh()
        self.select("effect", fx["id"])
        self.status(tr("Testo aggiunto: trascinalo, ingrandiscilo dagli angoli, doppio clic per riscriverlo."))

    def edit_text(self, fx: dict) -> None:
        values = {k: fx.get(k) for k in ("text", "align", "size", "color", "shadow", "bg")}
        values["center"] = False
        result = widgets.ask_text(self, self.fonts, values, tr("Modifica testo"))
        if not result:
            return
        self.push_undo()
        center = result.pop("center")
        fx.update(result)
        if center:
            self._center_fx(fx, "x")
        self._remember_text_style(dict(result, center=center))
        self.project.dirty = True
        self.refresh()
        self.select("effect", fx["id"])

    def _create_timer(self, fx: dict) -> None:
        """Tempo trascorso dall'inizio del video, centrato dove si e' cliccato; per tutto il video o fra IN e OUT."""
        W, H = self.project.width, self.project.height
        a, b = self.mark_in, self.mark_out
        full = a is None or b is None or b - a < MIN_LEN
        cx, cy = fx.pop("x"), fx.pop("y")
        fx.update(start=0.0 if full else a, end=self.project.duration() if full else b, full=full,
                  format="mmss", origin="video", prefix="",
                  **({"fps": float(self.project.fps or 25), "first": 0} if fx["type"] == "frames" else {}), size=max(24, H // 20), color="#FFFFFF",
                  font=default_font(), shadow=False, bg=True, bg_color="#000000", bg_alpha=0.55,
                  bg_radius=float(self.config_store.get("round_text")), opacity=1.0, x=0, y=0)
        x0, y0, x1, y1 = overlays.effect_bbox(fx)
        fx["x"] = int(round(min(max(0, cx - (x1 - x0) / 2), W - (x1 - x0))))
        fx["y"] = int(round(min(max(0, cy - (y1 - y0) / 2), H - (y1 - y0))))
        self.push_undo()
        self.project.add_effect(fx)
        self.refresh()
        self.select("effect", fx["id"])
        self.status(tr("Numero del fotogramma aggiunto: trascinalo dove vuoi, regolalo nel pannello a destra.")
                    if fx["type"] == "frames" else
                    tr("Tempo trascorso aggiunto: trascinalo dove vuoi, regolalo nel pannello a destra."))

    def _center_fx(self, fx: dict, axis: str) -> None:
        x0, y0, x1, y1 = overlays.effect_bbox(dict(fx, x=0, y=0))
        if axis == "x":
            fx["x"] = int(round((self.project.width - (x1 - x0)) / 2 - x0))
        else:
            fx["y"] = int(round((self.project.height - (y1 - y0)) / 2 - y0))

    def center_effect(self, fx: dict, axis: str) -> None:
        self.push_undo()
        self._center_fx(fx, axis)
        self.project.dirty = True
        self.refresh()

    def ask_image_file(self, current: str = "") -> str:
        path = filedialog.askopenfilename(
            title=tr("Immagine"), parent=self,
            initialdir=os.path.dirname(current) if current else (self.config_store.get("last_image_dir") or None),
            filetypes=[(tr("Immagini"), "*.png *.jpg *.jpeg *.webp *.bmp *.gif *.tif *.tiff"), (tr("Tutti i file"), "*.*")])
        if not path:
            return ""
        if overlays.load_logo(path) is None:
            messagebox.showwarning(tr("Immagine"), tr("Questa immagine non si apre."), self)
            return ""
        self.config_store.set("last_image_dir", os.path.dirname(path))
        self.config_store.save()
        return path

    def add_image(self) -> None:
        """Immagine sopra il video: scelta del file, poi al centro; si sposta e si ridimensiona sull'anteprima."""
        if not self.project.clips:
            messagebox.showinfo(tr("Immagine"), tr("Importa prima un video."), self)
            return
        self.stop_play()
        path = self.ask_image_file()
        if not path:
            return
        W, H = self.project.width, self.project.height
        source = overlays.load_logo(path)
        w = W * 0.4
        if source.height * w / source.width > H * 0.6:          # immagini alte: entro il 60% dell'altezza
            w = H * 0.6 * source.width / source.height
        start, end = self._default_span()
        fx = {"type": "image", "start": start, "end": end, "image": path, "w": int(w), "opacity": 1.0, "radius": 0.0,
              "x": 0, "y": 0}
        self._center_fx(fx, "x")
        self._center_fx(fx, "y")
        self.push_undo()
        self.project.add_effect(fx)
        self.refresh()
        self.select("effect", fx["id"])
        self.status(tr("Immagine aggiunta: trascinala per spostarla, dagli angoli per ridimensionarla."))

    def cancel_mode(self) -> None:
        self.preview.set_mode(None)
        self.mode_label.configure(text="")
        self._arrow_pending = None

    def _default_span(self) -> tuple[float, float]:
        index, clip, _local = self.project.locate(self.playhead)
        if clip is not None and clip["kind"] == "slide":
            # sopra una slide l'effetto dura quanto la slide
            a = self.project.clip_start(index)
            return a, a + clip_duration(clip)
        seconds = float(self.config_store.get("effect_seconds") or 4.0)
        start = self.playhead
        end = min(self.project.duration(), start + seconds)
        if end - start < MIN_LEN:
            start = max(0.0, end - seconds)
        return start, max(end, start + MIN_LEN)

    def _on_drawn(self, mode: str, geometry: dict) -> None:
        pending = getattr(self, "_arrow_pending", None)
        self.cancel_mode()
        if mode == "arrow_target":
            if pending is not None:
                self._set_arrow_target(*pending, geometry)
            return
        start, end = self._default_span()
        fx = {"type": mode, "start": start, "end": end}
        fx.update(geometry)
        if mode == "text":
            self._create_text(fx)
            return
        elif mode in ("box", "oval"):
            fx.update(color="#FF3B30", thickness=max(3, self.project.height // 240), fill=False, fill_alpha=0.25,
                      radius=float(self.config_store.get("round_box")) if mode == "box" else 0.0)
        elif mode == "arrow":
            fx.update(color="#FF3B30", thickness=max(4, self.project.height // 180))
        elif mode == "zoom":
            self._create_zoom(fx)
            return
        elif mode in overlays.TIMER_TYPES:
            self._create_timer(fx)
            return
        elif mode == "pixelate":
            self._create_pixelate(fx)
            return
        self.push_undo()
        self.project.add_effect(fx)
        self.refresh()
        self.select("effect", fx["id"])
        self.status(tr("{effect} aggiunto: regola i valori nel pannello a destra o trascina sull'anteprima.").format(
            effect=tr(EFFECT_NAMES[mode])))

    def _create_zoom(self, fx: dict) -> None:
        """Zoom: l'area disegnata sull'oggetto, ingrandita 2x/3x/4x nel riquadro messo dove si e' cliccato.

        L'area segue subito l'oggetto (se sta su una clip video); il riquadro
        ingrandito resta dove e' stato messo.
        """
        W, H = self.project.width, self.project.height
        cx, cy = fx.pop("cx", None), fx.pop("cy", None)
        factor = int(fx.get("factor") or self.config_store.get("zoom_factor") or 2)
        fx.update(factor=factor if factor in overlays.ZOOM_FACTORS else 2, color="#FFD60A",
                  thickness=max(3, H // 270), outline=True, link=True, track=[],
                  shape=getattr(self, "_zoom_shape", "rect"), radius=float(self.config_store.get("round_zoom")))
        overlays.place_inset(fx, cx, cy, W, H)
        self.config_store.set("zoom_factor", fx["factor"])
        self.push_undo()
        self.project.add_effect(fx)
        self.refresh()
        self.select("effect", fx["id"])
        _index, clip, _local = self.project.locate(self.playhead)
        if clip is not None and clip["kind"] == "video":
            self.retrack(fx)
        else:
            self.status(tr("Zoom aggiunto (fermo: sul fermo immagine non c'e' nulla da inseguire)."))

    def _create_pixelate(self, fx: dict) -> None:
        index, clip, local = self.project.locate(self.playhead)
        if clip is None:
            return
        clip_end = self.project.clip_start(index) + clip_duration(clip)
        default_end = min(clip_end, self.playhead + float(self.config_store.get("effect_seconds") or 4.0) * 2)
        result = widgets.ask_form(self, tr("Pixelatura con inseguimento"), [
            {"key": "end", "label": tr("Fino all'istante (secondi della timeline)"), "kind": "float",
             "default": f"{default_end:.2f}", "min": self.playhead + 0.04, "max": self.project.duration(),
             "help": tr("L'inseguimento parte dal cursore ({start}) e segue il soggetto "
                        "fino a questo istante (al massimo la fine della clip: {clip_end}).").format(
                 start=media.format_time(self.playhead), clip_end=media.format_time(clip_end))},
            {"key": "block", "label": tr("Grandezza dei pixel"), "kind": "int", "default": str(self.config_store.get("pixel_block")),
             "min": 2, "max": 200}], self.fonts, ok_text=tr("Insegui"))
        if not result:
            return
        fx.update(block=int(result["block"]), start=self.playhead, end=min(float(result["end"]), clip_end), track=[],
                  shape=getattr(self, "_pixel_shape", "rect"), radius=float(self.config_store.get("round_pixel")))
        self.push_undo()
        self.project.add_effect(fx)
        self.refresh()
        self.select("effect", fx["id"])
        self.retrack(fx)

    # --------------------------------------------------------------- keyframe

    def _key_eps(self) -> float:
        return 0.5 / max(1.0, self.project.fps)

    def _preview_key(self, fx: dict, t: float, cx: float, cy: float, s: float, snap, final: bool) -> None:
        """Trascinamento sull'anteprima di una figura con percorso: keyframe all'istante t."""
        fx["track"] = [list(k) for k in snap[0]]
        fx["keys"] = [list(k) for k in snap[1]]
        if not final:
            # durante il trascinamento: solo la chiave, senza correzioni (si vede subito)
            key = overlays.key_for(fx, t, cx, cy, s)
            eps = self._key_eps()
            fx["track"] = sorted([k for k in fx["track"] if abs(k[0] - t) > eps] + [key], key=lambda k: k[0])
            self.project.dirty = True
            self.schedule_preview()
            return
        self.set_keyframe(fx, t, cx, cy, s, undo=False)

    def set_keyframe(self, fx: dict, t: float, cx: float, cy: float, s: float, undo: bool = True) -> None:
        """Keyframe: la figura all'istante t sta in (cx, cy) con scala s.

        Il tratto dal keyframe precedente viene corretto un poco alla volta per
        arrivarci; se la figura segue il soggetto, l'inseguimento riparte da qui
        fino al keyframe successivo (e arriva esattamente su quello).
        """
        if undo:
            self.push_undo()
        eps = self._key_eps()
        follow = fx.get("follow", bool(fx.get("track")))
        if not fx.get("track"):
            fx["track"] = [overlays.base_key(fx)]
        key = overlays.key_for(fx, t, cx, cy, s)
        old = overlays.key_for(fx, t, *overlays.figure_center(fx, t))
        err = [key[i] - old[i] for i in (1, 2, 3)]
        manual = sorted(fx.get("keys") or [], key=lambda k: k[0])
        tp = max([k[0] for k in manual if k[0] < t - eps] + [fx["track"][0][0]])
        tn = min([k[0] for k in manual if k[0] > t + eps], default=None)
        for k in fx["track"]:
            if tp < k[0] < t - eps and t - tp > 1e-9:
                f = (k[0] - tp) / (t - tp)
                k[1], k[2] = round(k[1] + err[0] * f, 1), round(k[2] + err[1] * f, 1)
                if len(k) > 3:
                    k[3] = round(k[3] + err[2] * f, 4)
            elif not follow and k[0] > t + eps and (tn is None or k[0] < tn - eps):
                # figura animata a mano: anche il tratto dopo si adatta
                f = 1.0 if tn is None else (tn - k[0]) / (tn - t)
                k[1], k[2] = round(k[1] + err[0] * f, 1), round(k[2] + err[1] * f, 1)
                if len(k) > 3:
                    k[3] = round(k[3] + err[2] * f, 4)
        fx["track"] = sorted([k for k in fx["track"] if abs(k[0] - t) > eps] + [key], key=lambda k: k[0])
        fx["keys"] = sorted([k for k in manual if abs(k[0] - t) > eps] + [list(key)], key=lambda k: k[0])
        if fx["type"] == "pixelate" and fx["track"]:
            fx["x"], fx["y"] = int(round(fx["track"][0][1])), int(round(fx["track"][0][2]))
        self.project.dirty = True
        self.refresh()
        self.select("effect", fx["id"])
        _index, clip, _local = self.project.locate(t)
        if follow and fx["type"] in TRACKABLE and clip is not None and clip["kind"] == "video":
            self.retrack(fx, start=t, undo=False)
        else:
            self.status(tr("Keyframe a {time}.").format(time=media.format_time(t)))

    def pin_key(self, fx: dict) -> None:
        """Keyframe al cursore con la posizione che la figura ha adesso."""
        t = self.playhead
        if not (fx["start"] <= t < fx["end"]):
            messagebox.showinfo(tr("Keyframe"), tr("Porta il cursore dentro l'effetto."), self)
            return
        self.push_undo()
        eps = self._key_eps()
        if not fx.get("track"):
            fx["track"] = [overlays.base_key(fx)]
        key = overlays.key_for(fx, t, *overlays.figure_center(fx, t))
        fx["track"] = sorted([k for k in fx["track"] if abs(k[0] - t) > eps] + [key], key=lambda k: k[0])
        fx["keys"] = sorted([k for k in fx.get("keys") or [] if abs(k[0] - t) > eps] + [list(key)], key=lambda k: k[0])
        self.project.dirty = True
        self.refresh()
        self.select("effect", fx["id"])
        self.status(tr("Keyframe a {time}: trascina la figura per correggerla.").format(time=media.format_time(t)))

    def delete_key_at(self, fx: dict) -> None:
        eps = self._key_eps() * 2
        near = [k[0] for k in fx.get("keys") or [] if abs(k[0] - self.playhead) <= eps]
        if not near:
            messagebox.showinfo(tr("Keyframe"), tr("Nessun keyframe al cursore: usa Prec. / Succ. per andarci."), self)
            return
        self.delete_keys(fx, near[:1])

    def delete_keys(self, fx: dict, times: list[float]) -> None:
        """Cancella punti del percorso (keyframe o punti dell'inseguimento): li' la figura va dritta fra i
        punti rimasti. Il primo punto resta: e' la posizione di partenza della figura."""
        eps = max(self._key_eps(), 6e-5)
        track = fx.get("track") or []
        first = track[0][0] if track else None
        drop = [t for t in times if first is None or abs(t - first) > eps]
        kept_first = len(drop) < len(times)
        if not drop:
            self.status(tr("Il primo punto del percorso non si cancella: e' la partenza della figura."))
            return
        self.push_undo()
        hit = lambda t: any(abs(t - d) <= eps for d in drop)  # noqa: E731
        fx["track"] = [k for k in track if not hit(k[0])]
        fx["keys"] = [k for k in fx.get("keys") or [] if not hit(k[0])]
        self.timeline.key_sel = (None, set())
        self.project.dirty = True
        self.refresh()
        self.select("effect", fx["id"])
        deleted = (tr("Cancellati {count} punti del percorso (il primo resta: e' la partenza della figura).") if kept_first
                   else tr("Cancellati {count} punti del percorso."))
        self.status(deleted.format(count=len(drop)))

    def delete_selected_keys(self, fx: dict) -> None:
        fx_id, chosen = self.timeline.key_sel
        if fx_id != fx["id"] or not chosen:
            messagebox.showinfo(tr("Keyframe"), tr("Seleziona prima dei punti sulla barra dell'effetto nella timeline "
                                                   "(clic, Maiusc+clic per un intervallo, Ctrl+clic per aggiungerne)."), self)
            return
        self.delete_keys(fx, sorted(float(t) for t in chosen))

    def _effect_menu(self, fx_id: str, x: int, y: int) -> None:
        """Tasto destro sulla barra di un effetto: allunga o interrompi al cursore."""
        fx = self.project.effect_by_id(fx_id)
        if fx is None:
            return
        self.select("effect", fx_id, seek=False)       # il cursore resta dov'e': e' il riferimento del menu
        eps = 0.5 / max(1.0, self.project.fps)
        menu = tk.Menu(self, tearoff=0, bg=theme.PANEL, fg=theme.TEXT, activebackground=theme.SELECT_BG,
                       activeforeground=theme.TEXT, disabledforeground=theme.TEXT_FAINT, bd=1, relief="solid")
        menu.add_command(label=tr("Allunga fino al cursore"), command=lambda: self.effect_to_cursor(fx),
                         state="normal" if self.playhead > fx["end"] + eps else "disabled")
        menu.add_command(label=tr("Interrompi al cursore"), command=lambda: self.effect_to_cursor(fx),
                         state="normal" if fx["start"] + eps < self.playhead < fx["end"] - eps else "disabled")
        try:
            menu.tk_popup(x, y)
        finally:
            menu.grab_release()

    def toggle_effect_visible(self, fx_id: str) -> None:
        """Occhio sulla barra: mostra o nasconde l'effetto in anteprima e nell'esportazione."""
        fx = self.project.effect_by_id(fx_id)
        if fx is None:
            return
        self.push_undo()
        if fx.get("hidden"):
            fx.pop("hidden", None)
        else:
            fx["hidden"] = True
        self.project.dirty = True
        self.refresh()
        name = tr(EFFECT_NAMES.get(fx["type"], fx["type"]))
        self.status((tr("{effect} nascosto: non compare in anteprima ne' nel video esportato.") if fx.get("hidden")
                     else tr("{effect} di nuovo visibile.")).format(effect=name))

    def effect_to_cursor(self, fx: dict) -> None:
        """Porta la fine dell'effetto al cursore: lo allunga se il cursore e' dopo, lo interrompe se e' dentro."""
        t = self.playhead
        if t <= fx["start"] + 1e-6 or abs(t - fx["end"]) < 1e-6:
            return
        self.push_undo()
        longer = t > fx["end"]
        fx["end"] = t
        fx["full"] = False
        if not longer:                    # i punti del percorso e i keyframe oltre la nuova fine non servono piu'
            for key in ("track", "keys"):
                if fx.get(key):
                    fx[key] = [k for k in fx[key] if k[0] <= t + 1e-6]
        self.project.dirty = True
        self.refresh()
        if longer and fx.get("follow") and fx.get("track") and fx.get("type") in TRACKABLE:
            # segue un soggetto: l'inseguimento continua dall'ultimo punto fino alla nuova fine
            self.retrack(fx, start=float(fx["track"][-1][0]), undo=False)
            return
        self.status((tr("{effect} allungato fino a {t:.2f} s.") if longer else
                     tr("{effect} interrotto a {t:.2f} s.")).format(effect=tr(EFFECT_NAMES.get(fx["type"], fx["type"])), t=t))

    def _timeline_key_delete(self, fx_id: str, times: list) -> None:
        fx = self.project.effect_by_id(fx_id)
        if fx is not None:
            self.delete_keys(fx, times)

    def goto_key(self, fx: dict, direction: int) -> None:
        times = sorted(k[0] for k in fx.get("keys") or [])
        eps = self._key_eps() * 2
        if direction > 0:
            nxt = [t for t in times if t > self.playhead + eps]
            target = nxt[0] if nxt else None
        else:
            prv = [t for t in times if t < self.playhead - eps]
            target = prv[-1] if prv else None
        if target is None:
            self.status(tr("Nessun altro keyframe in quella direzione."))
            return
        self.seek(target)

    def pick_arrow_target(self, fx: dict, start: float | None = None) -> None:
        """Per far seguire un soggetto alla freccia: si disegna un rettangolo attorno al soggetto.

        Il modello dell'inseguimento e' quel rettangolo (non quello che sta
        sotto la punta, che spesso e' lo sfondo: la punta tocca il soggetto ma
        non ci sta sopra). La punta resta agganciata al rettangolo.
        """
        if not self.project.clips:
            return
        self.stop_play()
        self.preview.set_mode("arrow_target")
        self._arrow_pending = (fx, start)
        self.mode_label.configure(text=tr("Disegna: {effect}  (Esc annulla)").format(effect=tr("soggetto della freccia")))
        self.status(tr("Trascina un rettangolo attorno al soggetto: la freccia lo seguira' tenendo la punta dov'e'."))

    def _set_arrow_target(self, fx: dict, start: float | None, area: dict) -> None:
        t = start if start is not None else (self.playhead if fx["start"] <= self.playhead < fx["end"] else fx["start"])
        tip = overlays.displaced(fx, t)
        # il rettangolo si ricorda rispetto alla punta: si sposta con lei (keyframe, inseguimenti successivi)
        fx["target"] = [round(area["x"] - float(tip["x2"]), 1), round(area["y"] - float(tip["y2"]), 1),
                        int(area["w"]), int(area["h"])]
        self.project.dirty = True
        self.retrack(fx, start=t)

    def untrack(self, fx: dict) -> None:
        """La figura torna ferma: la sua geometria diventa quella che aveva all'inizio dell'inseguimento."""
        self.push_undo()
        fx["track"] = []
        fx["keys"] = []
        fx["follow"] = False
        fx.pop("lost", None)
        self.project.dirty = True
        self.refresh()
        self.select("effect", fx["id"])

    def retrack(self, fx: dict, start: float | None = None, undo: bool = True) -> None:
        """Esegue (o ripete) l'inseguimento del soggetto per una pixelatura, un riquadro, un ovale o una freccia.

        Parte da `start` (o dal cursore, se dentro l'effetto, o dall'inizio
        dell'effetto) e arriva al keyframe successivo, se c'e', altrimenti alla
        fine dell'effetto o della clip. Verso un keyframe il percorso viene
        corretto per arrivarci esatto. Se il soggetto esce dall'inquadratura o
        viene perso (e non c'e' un keyframe dopo), l'effetto finisce li'.
        """
        if fx.get("type") not in TRACKABLE:
            return
        if start is None:
            start = self.playhead if fx["start"] <= self.playhead < fx["end"] else fx["start"]
        eps = self._key_eps()
        later = sorted(k for k in fx.get("keys") or [] if k[0] > start + eps)
        next_key = later[0] if later else None
        index, clip, local = self.project.locate(start)
        if clip is None or clip["kind"] != "video":
            messagebox.showinfo(tr("Inseguimento"), tr("L'inseguimento funziona solo su una clip video (non su un fermo "
                                                       "immagine): la figura resta ferma."), self)
            return
        clip_start = self.project.clip_start(index)
        clip_end = clip_start + clip_duration(clip)
        end = min(fx["end"], clip_end)
        if next_key is not None and next_key[0] < end:
            end = float(next_key[0])
        speed = float(clip.get("speed", 1) or 1)
        src_start = self.project.source_time(clip, start - clip_start)
        src_end = self.project.source_time(clip, end - clip_start)
        W, H = self.project.width, self.project.height
        shown = overlays.displaced(fx, start)
        s_start = 1.0                     # misura (scala) della figura alla partenza, se segue gia' l'oggetto
        if fx["type"] in ("pixelate", "box", "oval", "zoom"):
            # si parte dalla figura come appare adesso (anche ingrandita); le chiavi restano riferite a w, h
            x, y, s_start = overlays.track_state(fx, start)
            if not fx.get("track"):
                x, y = float(fx["x"]), float(fx["y"])
            if fx.get("track"):
                s_start *= overlays.key_scale(fx["track"][0])
            w_now, h_now = float(fx["w"]) * s_start, float(fx["h"]) * s_start
            box = (x - (w_now - float(fx["w"])) / 2, y - (h_now - float(fx["h"])) / 2, w_now, h_now)
            anchor_off = ((w_now - float(fx["w"])) / 2, (h_now - float(fx["h"])) / 2)
        elif fx["type"] == "arrow":
            # il modello e' il rettangolo disegnato attorno al soggetto (ricordato rispetto alla punta);
            # senza, prima si chiede di disegnarlo
            if not fx.get("target"):
                self.pick_arrow_target(fx, start)
                return
            dx, dy, tw, th = (float(v) for v in fx["target"])
            box = (float(shown["x2"]) + dx, float(shown["y2"]) + dy, tw, th)
            anchor_off = (-dx, -dy)                    # dall'angolo del rettangolo alla punta
        else:
            box = (float(shown["x"]), float(shown["y"]), float(fx["w"]), float(fx["h"]))
            anchor_off = (0.0, 0.0)
        bx = min(max(0.0, box[0]), max(0.0, W - box[2]))
        by = min(max(0.0, box[1]), max(0.0, H - box[3]))
        # se il modello e' stato spinto dentro l'immagine, l'ancora resta dov'era
        anchor_off = (anchor_off[0] + box[0] - bx, anchor_off[1] + box[1] - by)
        box = (bx, by, min(box[2], W), min(box[3], H))
        cancel = threading.Event()
        dialog = widgets.ProgressDialog(self, tr("Inseguimento del soggetto"), self.fonts, on_cancel=cancel.set)
        min_score = float(self.config_store.get("track_min") or 0.45)

        def progress(done: int, total: int) -> None:
            self.post(lambda: dialog.set(tr("Fotogramma {done} / {total}").format(done=done, total=total), done / max(1, total)))

        def work() -> None:
            try:
                result = tracking.track(clip["source"], src_start, src_end, box,
                                        (self.project.width, self.project.height), min_score,
                                        progress, cancel)
                self.post(lambda: done(result, None))
            except tracking.Cancelled:
                self.post(lambda: done(None, "annullato"))
            except Exception as exc:  # noqa: BLE001
                message = str(exc)        # exc sparisce alla fine del blocco except
                self.post(lambda: done(None, message))

        def to_timeline(t_source: float) -> float:
            return clip_start + (t_source - float(clip["in"])) / speed

        def done(result, error) -> None:
            dialog.close()
            if error == "annullato":
                self.status(tr("Inseguimento annullato."))
                return
            if error:
                messagebox.showerror(tr("Inseguimento"), error, self)
                return
            keys = [[to_timeline(p[0]), round(p[1] + anchor_off[0], 1), round(p[2] + anchor_off[1], 1),
                     round(overlays.key_scale(p) * s_start, 4)] for p in result.points]
            before = [k for k in fx.get("track", []) if k[0] < start - eps]
            # frase principale e aggiunte facoltative: ognuna e' un pezzo di frase completo da tradurre
            text = tr("Inseguimento completato: {frames} fotogrammi, {points} punti").format(
                frames=result.examined, points=len(keys))
            if next_key is not None:
                # verso il keyframe successivo: il percorso trovato viene corretto per arrivarci esatto;
                # se il soggetto e' stato perso prima, dall'ultimo punto buono si va dritti al keyframe
                after = [k for k in fx["track"] if k[0] >= next_key[0] - eps]
                keys = [k for k in keys if k[0] < next_key[0] - eps]
                if result.lost_at is None and len(keys) > 1:
                    tail = keys[-1]
                    err = [next_key[i] - (tail[i] if i < len(tail) else 1.0) for i in (1, 2, 3)]
                    span = max(1e-9, tail[0] - start)
                    for k in keys[1:]:
                        f = (k[0] - start) / span
                        k[1], k[2], k[3] = round(k[1] + err[0] * f, 1), round(k[2] + err[1] * f, 1), round(k[3] + err[2] * f, 4)
                elif result.lost_at is not None:
                    text += tr("; soggetto non trovato da {time} al keyframe").format(
                        time=media.format_time(to_timeline(result.lost_at)))
                fx["track"] = before + keys + after
            else:
                fx["track"] = before + keys
                if result.lost_at is not None:
                    # uscito o perso: l'inseguimento si ferma e l'effetto finisce li'
                    stop = to_timeline(result.lost_at) + 1.0 / max(1.0, self.project.fps)
                    ending = (tr("; soggetto uscito dall'inquadratura: l'effetto finisce a {time}") if result.reason == "uscito"
                              else tr("; soggetto perso: l'effetto finisce a {time}"))
                    text += ending.format(time=media.format_time(stop))
                    fx["end"] = max(fx["start"] + MIN_LEN, min(fx["end"], stop))
                elif result.lost:
                    text += tr(", non trovato in {frames} fotogrammi").format(frames=result.lost)
            fx["follow"] = True
            if fx["type"] == "pixelate" and fx["track"]:
                fx["x"], fx["y"] = int(round(fx["track"][0][1])), int(round(fx["track"][0][2]))
            fx["lost"] = result.lost
            self.project.dirty = True
            self.refresh()
            self.select("effect", fx["id"], seek=False)
            self.status(text + ".")

        threading.Thread(target=work, daemon=True).start()

    def pick_font(self, current: str, sample: str, callback) -> None:
        FontPicker(self, self.fonts, current, sample or tr("Testo di prova"), callback)

    # ================================================================ esportazione

    def export(self) -> None:
        if not self.project.clips:
            messagebox.showinfo(tr("Esportazione"), tr("La timeline e' vuota."), self)
            return
        self.stop_play()
        initial_dir = self.config_store.get("last_export_dir") or (os.path.dirname(self.project.path) if self.project.path else None)
        name = (os.path.splitext(os.path.basename(self.project.path))[0] if self.project.path else "video") + ".mp4"
        output = filedialog.asksaveasfilename(title=tr("Esporta MP4"), defaultextension=".mp4", parent=self,
                                              filetypes=[(tr("Video MP4"), "*.mp4")], initialdir=initial_dir, initialfile=name)
        if not output:
            return
        self.config_store.set("last_export_dir", os.path.dirname(output))
        self.config_store.save()
        cancel = threading.Event()
        dialog = widgets.ProgressDialog(self, tr("Esportazione in corso"), self.fonts, on_cancel=cancel.set)
        exporter = render.Exporter(self.project, output, crf=int(self.config_store.get("export_crf")),
                                   preset=str(self.config_store.get("export_preset")),
                                   audio_kbps=int(self.config_store.get("export_audio_kbps")),
                                   progress=lambda m, f: self.post(lambda: dialog.set(m, f)), cancel=cancel)
        started = time.perf_counter()

        def work() -> None:
            try:
                exporter.run()
                self.post(lambda: done(None))
            except render.Cancelled:
                self.post(lambda: done("annullato"))
            except Exception as exc:  # noqa: BLE001
                message = str(exc)        # exc sparisce alla fine del blocco except
                self.post(lambda: done(message))

        def done(error: str | None) -> None:
            dialog.close()
            if error == "annullato":
                try:
                    os.remove(output)
                except OSError:
                    pass
                self.status(tr("Esportazione annullata."))
                return
            if error:
                messagebox.showerror(tr("Esportazione fallita"), error, self)
                self.status(tr("Esportazione fallita."))
                return
            elapsed = time.perf_counter() - started
            size = os.path.getsize(output) / 1e6
            self.status(tr("Esportato {path} ({size:.1f} MB in {seconds:.0f} s).").format(path=output, size=size, seconds=elapsed))
            if messagebox.askyesno(tr("Esportazione completata"),
                                   tr("{path}\n\n{size:.1f} MB in {seconds:.0f} secondi.\n\nAprire la cartella?").format(
                                       path=output, size=size, seconds=elapsed),
                                   self, yes=tr("Apri cartella"), no=tr("Chiudi")):
                try:
                    tools.open_folder(output, select=True)
                except OSError:
                    pass

        threading.Thread(target=work, daemon=True).start()


def run(initial: str | None = None) -> None:
    app = App(initial)
    app.mainloop()
