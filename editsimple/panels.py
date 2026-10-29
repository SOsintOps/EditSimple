# EditSimple — montaggio video per presentazioni.  Copyright (C) 2026 Andrea Cumini <andrea@osintinfo.net>
# SPDX-License-Identifier: GPL-3.0-only
# GNU GPL v3 con termini aggiuntivi (attribuzione dell'autore): vedi LICENSE e NOTICE.
"""Pannello delle proprieta': i campi dell'elemento selezionato (clip, effetto, traccia audio).

Ogni modifica si applica subito e aggiorna anteprima e timeline (con un
breve ritardo per non ridisegnare a ogni tasto). Il primo cambiamento di ogni
campo salva uno stato per Annulla.
"""

from __future__ import annotations

import os
import tkinter as tk
from tkinter import colorchooser
from typing import Any, Callable

import customtkinter as ctk

from . import fonts as fontlib
from . import overlays, theme, widgets
from .media import format_time
from .i18n import N_, tr, upper
from .project import EFFECT_NAMES, SPEEDS, clip_duration, clip_label, speed_text, speed_value

CORNERS = {"top-left": N_("In alto a sinistra"), "top-right": N_("In alto a destra"),
           "bottom-left": N_("In basso a sinistra"), "bottom-right": N_("In basso a destra"), "center": N_("Al centro")}
ALIGNS = {"left": N_("Sinistra"), "center": N_("Centro"), "right": N_("Destra")}


def _options(labels: dict[str, str]) -> dict[str, str]:
    """Opzioni di un menu nella lingua in uso: {chiave interna: etichetta tradotta}."""
    return {key: tr(label) for key, label in labels.items()}


class PropertiesPanel(ctk.CTkFrame):
    def __init__(self, master, fonts: theme.Fonts, app) -> None:
        super().__init__(master, fg_color="transparent", corner_radius=0, width=330)
        self.fonts = fonts
        self.app = app
        self.kind: str | None = None
        self.obj: dict | None = None
        self._vars: dict[str, tk.Variable] = {}
        self._job: str | None = None
        self._syncing = False
        self._touched: set[str] = set()
        self.grid_propagate(False)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.card = widgets.Card(self, tr("Proprieta'"), fonts)
        self.card.grid(row=0, column=0, sticky="nsew")
        self.body = ctk.CTkScrollableFrame(self.card.body, fg_color="transparent", corner_radius=0)
        self.body.pack(fill="both", expand=True)
        self.body.grid_columnconfigure(0, weight=1)
        self.show(None, None)

    # ------------------------------------------------------------- costruzione

    def show(self, kind: str | None, obj: dict | None) -> None:
        self.kind, self.obj = kind, obj
        self._vars.clear()
        self._choices: dict[str, dict] = {}
        self._touched.clear()
        self._color_buttons: dict[str, ctk.CTkButton] = {}
        if self._job is not None:
            self.after_cancel(self._job)
            self._job = None
        for child in self.body.winfo_children():
            child.destroy()
        if kind == "clip":
            kind_name = {"freeze": tr("fermo immagine"), "slide": tr("slide")}.get(obj["kind"], tr("video"))
            self.card.set_title(tr("Clip: {kind}").format(kind=kind_name))
            self._build_clip(obj)
        elif kind == "effect":
            self.card.set_title(tr("Effetto: {name}").format(name=tr(EFFECT_NAMES.get(obj["type"], obj["type"]))))
            self._build_effect(obj)
        elif kind == "audio":
            self.card.set_title(tr("Traccia audio"))
            self._build_audio(obj)
        elif kind == "oaudio":
            self.card.set_title(tr("Audio originale (un pezzo)"))
            self._build_oaudio(obj)
        elif kind == "oaudio_all":
            self.card.set_title(tr("Audio originale (tutto)"))
            self._build_oaudio_all()
        else:
            self.card.set_title(tr("Proprieta'"))
            self._build_empty()

    def retranslate(self) -> None:
        """Cambio di lingua: si ricostruiscono i campi (sezioni in maiuscolo, voci dei menu)."""
        self.show(self.kind, self.obj)

    def refresh(self) -> None:
        """Riporta nei campi i valori attuali (dopo un trascinamento su anteprima o timeline)."""
        if self.obj is None:
            return
        self._syncing = True
        try:
            for key, var in self._vars.items():
                if key.startswith("clock."):
                    value = self.app.project.clock.get(key[6:])
                elif key == "original_volume":
                    value = self.app.project.original_volume
                elif key.startswith("orig."):
                    value = self._value(key)
                elif key in self.obj:
                    value = self.obj[key]
                else:
                    continue
                if isinstance(var, tk.BooleanVar):
                    var.set(bool(value))
                elif isinstance(var, tk.DoubleVar):
                    var.set(float(value))
                elif key in getattr(self, "_choices", {}) and key not in ("corner", "align", "shape", "speed"):
                    var.set(self._choices[key].get(str(value), str(value)))
                elif key in ("corner", "align"):
                    var.set(tr({"corner": CORNERS, "align": ALIGNS}[key].get(value, value)))
                elif key == "shape":
                    var.set(tr("Ovale") if value == "oval" else tr("Rettangolare"))
                elif key == "speed":
                    var.set(speed_text(value))
                else:
                    text = f"{value:g}" if isinstance(value, float) else str(value)
                    if var.get() != text:
                        var.set(text)
            for key, widget in self._color_buttons.items():
                value = self.app.project.clock.get("color") if key == "clock.color" else self.obj.get(key)
                if value and widget.winfo_exists():
                    widget.configure(fg_color=value, hover_color=value, text=value.upper(), text_color=_contrast(value))
        finally:
            self._syncing = False

    # --- campi

    def _section(self, title: str) -> None:
        widgets.caption(self.body, upper(title), self.fonts).pack(fill="x", pady=(12, 2))

    def _label_row(self, label: str, value: str) -> None:
        row = ctk.CTkFrame(self.body, fg_color="transparent")
        row.pack(fill="x", pady=(2, 0))
        ctk.CTkLabel(row, text=label, font=self.fonts.small, text_color=theme.TEXT_DIM, anchor="w", width=110).pack(side="left")
        ctk.CTkLabel(row, text=value, font=self.fonts.small, text_color=theme.TEXT, anchor="w", justify="left",
                     wraplength=190).pack(side="left", fill="x", expand=True)

    def _entry(self, key: str, label: str, kind: str = "float", width: int = 90, row=None, on_apply=None) -> None:
        value = self._value(key)
        var = tk.StringVar(value=f"{value:g}" if isinstance(value, float) else str(value))
        self._vars[key] = var
        container = row or ctk.CTkFrame(self.body, fg_color="transparent")
        if row is None:
            container.pack(fill="x", pady=(4, 0))
        ctk.CTkLabel(container, text=label, font=self.fonts.small, text_color=theme.TEXT_SOFT, anchor="w",
                     width=110 if row is None else 0).pack(side="left", padx=(0, 6))
        entry = ctk.CTkEntry(container, textvariable=var, width=width, height=28, font=self.fonts.body)
        entry.pack(side="left")
        var.trace_add("write", lambda *_: self._schedule(key, kind, on_apply))

    def _value(self, key: str) -> Any:
        if key.startswith("clock."):
            return self.app.project.clock.get(key[6:], "")
        if key == "original_volume":
            return self.app.project.original_volume
        if key == "orig.on":
            return not self.app.project.original_muted
        if key.startswith("orig."):
            return getattr(self.app.project, "original_" + key[5:])
        if self.obj is not None and key in ("opacity", "bg_radius", "radius") and key not in self.obj:
            return {"opacity": 1.0, "bg_radius": 25.0, "radius": 0.0}[key]
        if self.obj is not None and key == "volume" and self.kind == "oaudio":
            return self.obj.get("volume", 1.0)
        return self.obj.get(key, "") if self.obj is not None else ""

    def _check(self, key: str, label: str, on_apply=None) -> None:
        var = tk.BooleanVar(value=bool(self._value(key)))
        self._vars[key] = var
        ctk.CTkCheckBox(self.body, text=label, variable=var, font=self.fonts.body,
                        command=lambda: self._apply(key, var.get(), on_apply)).pack(fill="x", pady=(8, 0))

    def _slider(self, key: str, label: str, lo: float, hi: float, fmt=lambda v: f"{v * 100:.0f} %",
                on_apply=None) -> None:
        var = tk.DoubleVar(value=float(self._value(key)))
        self._vars[key] = var
        row = ctk.CTkFrame(self.body, fg_color="transparent")
        row.pack(fill="x", pady=(6, 0))
        ctk.CTkLabel(row, text=label, font=self.fonts.small, text_color=theme.TEXT_SOFT, anchor="w").pack(side="left")
        value_label = ctk.CTkLabel(row, text=fmt(var.get()), font=self.fonts.mono, text_color=theme.TEXT_DIM, anchor="e")
        value_label.pack(side="right")

        def changed(value: float) -> None:
            value_label.configure(text=fmt(value))
            self._apply(key, float(value), on_apply, undo=False)

        slider = ctk.CTkSlider(self.body, from_=lo, to=hi, variable=var, command=changed, height=16)
        slider.pack(fill="x", pady=(2, 0))
        slider.bind("<ButtonPress-1>", lambda _e: self._touch(key), add="+")

    def _color(self, key: str, label: str, on_apply=None) -> None:
        row = ctk.CTkFrame(self.body, fg_color="transparent")
        row.pack(fill="x", pady=(6, 0))
        ctk.CTkLabel(row, text=label, font=self.fonts.small, text_color=theme.TEXT_SOFT, anchor="w", width=110).pack(side="left", padx=(0, 6))
        current = str(self._value(key) or "#FFFFFF")
        button = ctk.CTkButton(row, text=current.upper(), width=110, height=28, fg_color=current, hover_color=current,
                               text_color=_contrast(current), font=self.fonts.mono)
        button.pack(side="left")

        def pick() -> None:
            rgb, hexcolor = colorchooser.askcolor(color=str(self._value(key) or "#FFFFFF"), title=label, parent=self.app)
            if hexcolor:
                hexcolor = hexcolor.upper()
                button.configure(fg_color=hexcolor, hover_color=hexcolor, text=hexcolor, text_color=_contrast(hexcolor))
                self._apply(key, hexcolor, on_apply)

        button.configure(command=pick)
        self._color_buttons[key] = button

    def _choice(self, key: str, label: str, options: dict[str, str], on_apply=None) -> None:
        current = options.get(str(self._value(key)), next(iter(options.values())))
        self._choices[key] = options
        var = tk.StringVar(value=current)
        self._vars[key] = var
        row = ctk.CTkFrame(self.body, fg_color="transparent")
        row.pack(fill="x", pady=(6, 0))
        ctk.CTkLabel(row, text=label, font=self.fonts.small, text_color=theme.TEXT_SOFT, anchor="w", width=110).pack(side="left", padx=(0, 6))
        inverse = {v: k for k, v in options.items()}
        ctk.CTkOptionMenu(row, variable=var, values=list(options.values()), width=170, height=28, font=self.fonts.body,
                          command=lambda v: self._apply(key, inverse.get(v, v), on_apply)).pack(side="left")

    def _button(self, text: str, command, danger: bool = False, primary: bool = False) -> None:
        widgets.button(self.body, text, command, danger=danger, primary=primary).pack(fill="x", pady=(12, 0))

    def _time_row(self, key: str, label: str) -> None:
        row = ctk.CTkFrame(self.body, fg_color="transparent")
        row.pack(fill="x", pady=(4, 0))
        self._entry(key, label, "float", width=80, row=row)
        widgets.button(row, tr("= cursore"), lambda: self._set_from_playhead(key), width=84, height=28,
                       font=(theme.ui_font(), 11)).pack(side="left", padx=(6, 0))

    def _set_from_playhead(self, key: str) -> None:
        self._vars[key].set(f"{self.app.playhead:.3f}")

    # --- applicazione

    def _touch(self, key: str) -> None:
        if key not in self._touched:
            self._touched.add(key)
            self.app.push_undo()

    def _schedule(self, key: str, kind: str, on_apply) -> None:
        if self._syncing:
            return
        if self._job is not None:
            self.after_cancel(self._job)
        self._job = self.after(250, lambda: self._apply_entry(key, kind, on_apply))

    def _apply_entry(self, key: str, kind: str, on_apply) -> None:
        self._job = None
        raw = self._vars[key].get().strip().replace(",", ".")
        if kind in ("float", "int"):
            try:
                value = float(raw)
            except ValueError:
                return
            if kind == "int":
                value = int(round(value))
        else:
            value = raw
        self._apply(key, value, on_apply)

    def _apply(self, key: str, value: Any, on_apply=None, undo: bool = True) -> None:
        if self._syncing or self.obj is None and not key.startswith("clock.") and key != "original_volume":
            return
        if undo:
            self._touch(key)
        if key in ("start", "end") and self.obj is not None and self.obj.get("full"):
            self.obj["full"] = False          # tempi scelti a mano: non piu' "per tutto il video"
        if on_apply is not None:
            on_apply(key, value)
        elif key.startswith("clock."):
            self.app.project.clock[key[6:]] = value
        elif key == "original_volume":
            self.app.project.original_volume = float(value)
        elif key == "orig.on":
            self.app.project.original_muted = not bool(value)
        elif key.startswith("orig."):
            setattr(self.app.project, "original_" + key[5:], max(0.0, float(value)))
        else:
            self.obj[key] = value
        self.app.project.dirty = True
        self.app.refresh()

    # ------------------------------------------------------------- pannelli

    def _build_empty(self) -> None:
        text = tr("Nessun elemento selezionato.\n\n"
                "Clicca una clip, un effetto o una traccia audio nella timeline per vederne le proprieta'.\n\n"
                "Flusso di lavoro:\n"
                "1. Importa un video (Ctrl+I)\n"
                "2. Segna IN e OUT (tasti I e O) e taglia o elimina\n"
                "3. Aggiungi fermo immagine, velocita', testi, frecce, riquadri, zoom, pixelatura\n"
                "4. Esporta in mp4 (Ctrl+E)")
        widgets.note(self.body, text, self.fonts, wraplength=280).pack(fill="x", pady=(4, 0))

    def _build_clip(self, clip: dict) -> None:
        project = self.app.project
        self._label_row(tr("File"), clip_label(clip))
        self._label_row(tr("Durata"), format_time(clip_duration(clip)))
        index = project.clip_index(clip["id"])
        self._label_row(tr("Posizione"), format_time(project.clip_start(index)) if index >= 0 else "")
        if clip["kind"] == "slide":
            self._build_slide(clip)
            return
        self._build_transitions(clip)
        if clip["kind"] == "freeze":
            self._section(tr("Fermo immagine"))
            self._entry("at", tr("Istante sorgente (s)"), "float")
            self._entry("duration", tr("Durata (s)"), "float",
                        on_apply=lambda k, v: project.resize_freeze(clip["id"], v))
        else:
            self._section(tr("Taglio nel video sorgente"))
            self._entry("in", tr("Inizio (s)"), "float", on_apply=lambda k, v: project.set_clip_range(clip["id"], v, float(clip["out"])))
            self._entry("out", tr("Fine (s)"), "float", on_apply=lambda k, v: project.set_clip_range(clip["id"], float(clip["in"]), v))
            self._section(tr("Audio"))
            self._check("audio", tr("Audio originale di questa clip"), on_apply=lambda k, v: clip.__setitem__("audio", bool(v)))
            self._slider("original_volume", tr("Volume audio originale (tutto il progetto)"), 0.0, 2.0)
            self._section(tr("Velocita' (sotto 1x rallenta)"))
            self._choice("speed", tr("Velocita'"), {str(s): speed_text(s) for s in SPEEDS}, on_apply=self._apply_speed)
            self._check("clock", tr("Mostra orologio con la velocita'"), on_apply=lambda k, v: clip.__setitem__("clock", bool(v)))
            self._section(tr("Orologio (tutto il progetto)"))
            self._entry("clock.size", tr("Dimensione (px)"), "int")
            self._choice("clock.corner", tr("Posizione"), _options(CORNERS))
            self._color("clock.color", tr("Colore"))
            self._slider("clock.bg_alpha", tr("Opacita' sfondo"), 0.0, 1.0)
            self._slider("clock.radius", tr("Angoli arrotondati"), 0.0, 50.0, fmt=lambda v: f"{v:.0f} %")
        self._button(tr("Elimina clip"), lambda: self.app.delete_clip(clip["id"]), danger=True)

    def _build_transitions(self, clip: dict) -> None:
        project = self.app.project
        self._section(tr("Transizioni"))
        self._entry("fade_in", tr("Dal nero (s)"), "float")
        self._entry("fade_out", tr("Al nero (s)"), "float")
        index = project.clip_index(clip["id"])
        if 0 <= index < len(project.clips) - 1:
            self._entry("xfade", tr("Fusione con la succ. (s)"), "float")
        widgets.note(self.body, tr("Dal nero: la clip compare dal nero. Al nero: sparisce nel nero. Fusione: la clip "
                                "sfuma nella successiva, a cavallo del taglio (la durata del video non cambia). "
                                "Anche l'audio sale e scende. 0 = taglio netto."),
                     self.fonts, wraplength=280).pack(fill="x", pady=(4, 0))

    def _build_slide(self, clip: dict) -> None:
        project = self.app.project
        self._section({"close": tr("Slide di chiusura"), "mid": tr("Slide")}.get(clip.get("role"), tr("Slide di apertura")))
        self._entry("duration", tr("Durata (s)"), "float",
                    on_apply=lambda k, v: project.resize_freeze(clip["id"], max(0.2, float(v))))
        self._color("bg", tr("Colore sfondo"))
        row = ctk.CTkFrame(self.body, fg_color="transparent")
        row.pack(fill="x", pady=(6, 0))
        ctk.CTkLabel(row, text=tr("Immagine"), font=self.fonts.small, text_color=theme.TEXT_SOFT, anchor="w", width=110).pack(side="left", padx=(0, 6))
        name = os.path.basename(clip.get("bg_image") or "") or tr("nessuna")
        widgets.button(row, name if len(name) < 16 else name[:13] + "...", lambda: self._pick_slide_bg(clip),
                       width=120, height=28).pack(side="left")
        if clip.get("bg_image"):
            widgets.button(row, tr("Togli"), lambda: self._set_slide_bg(clip, ""), width=56, height=28).pack(side="left", padx=(6, 0))
            self._choice("bg_fit", tr("Adattamento"), _options(overlays.SLIDE_FITS))
        widgets.note(self.body, tr("La slide e' un fondo a tinta unita o un'immagine adattata alla misura del video. Testi e immagini si mettono sopra con gli "
                                "strumenti Testo e Immagine: con il cursore sulla slide durano quanto lei."),
                     self.fonts, wraplength=280).pack(fill="x", pady=(6, 0))
        self._build_transitions(clip)
        self._button(tr("Elimina slide"), lambda: self.app.delete_clip(clip["id"]), danger=True)

    def _pick_slide_bg(self, clip: dict) -> None:
        path = self.app.ask_image_file(clip.get("bg_image") or "")
        if path:
            self._set_slide_bg(clip, path)

    def _set_slide_bg(self, clip: dict, path: str) -> None:
        self._touch("bg_image")
        clip["bg_image"] = path
        clip.setdefault("bg_fit", "cover")
        self.app.project.dirty = True
        self.app.refresh()
        self.after(10, lambda: self.show("clip", clip))

    def _apply_speed(self, key: str, value: Any) -> None:
        clip = self.obj
        project = self.app.project
        index = project.clip_index(clip["id"])
        if index < 0:
            return
        factor = speed_value(value)
        a = project.clip_start(index)
        b = a + clip_duration(clip)
        project.set_speed(a, b, factor, bool(clip.get("clock")) or factor != 1 and self.app.config_store.get("speed_clock"))
        clip["speed"] = factor
        if factor == 1:
            clip["clock"] = False
        self.after(10, lambda: self.show("clip", clip))

    def _build_effect(self, fx: dict) -> None:
        kind = fx["type"]
        self._section(tr("Tempo"))
        self._time_row("start", tr("Inizio (s)"))
        self._time_row("end", tr("Fine (s)"))
        if kind == "text":
            self._section(tr("Testo"))
            box = ctk.CTkTextbox(self.body, height=70, font=self.fonts.body, wrap="word")
            box.pack(fill="x", pady=(2, 0))
            box.insert("1.0", fx.get("text", ""))
            box.bind("<KeyRelease>", lambda _e: self._text_changed(box))
            row = ctk.CTkFrame(self.body, fg_color="transparent")
            row.pack(fill="x", pady=(6, 0))
            ctk.CTkLabel(row, text=tr("Carattere"), font=self.fonts.small, text_color=theme.TEXT_SOFT, anchor="w", width=110).pack(side="left", padx=(0, 6))
            font_button = widgets.button(row, fontlib.display_name(fx.get("font") or fontlib.default_font()),
                                         lambda: None, width=170, height=28)
            font_button.pack(side="left")

            def chosen(name: str) -> None:
                font_button.configure(text=fontlib.display_name(name))
                self._apply("font", name)

            font_button.configure(command=lambda: self.app.pick_font(fx.get("font") or fontlib.default_font(),
                                                                     fx.get("text", ""), chosen))
            self._entry("size", tr("Dimensione (px)"), "int")
            self._color("color", tr("Colore"))
            self._choice("align", tr("Allineamento"), _options(ALIGNS))
            self._check("shadow", tr("Ombra"))
            self._slider("opacity", tr("Opacita' del testo"), 0.0, 1.0)
            self._check("bg", tr("Sfondo dietro il testo"))
            self._color("bg_color", tr("Colore sfondo"))
            self._slider("bg_alpha", tr("Opacita' sfondo"), 0.0, 1.0)
            self._slider("bg_radius", tr("Angoli arrotondati"), 0.0, 50.0, fmt=lambda v: f"{v:.0f} %")
            self._section(tr("Posizione"))
            row = ctk.CTkFrame(self.body, fg_color="transparent")
            row.pack(fill="x", pady=(4, 0))
            self._entry("x", "X", "int", width=70, row=row)
            self._entry("y", "  Y", "int", width=70, row=row)
            self._center_buttons(fx)
            self._button(tr("Modifica testo..."), lambda: self.app.edit_text(fx), primary=True)
            widgets.note(self.body, tr("Sull'anteprima: trascina per spostare, dagli angoli per ingrandire, doppio clic "
                                    "per riscriverlo."), self.fonts, wraplength=280).pack(fill="x", pady=(6, 0))
        elif kind in overlays.TIMER_TYPES:
            if kind == "frames":
                self._section(tr("Numero del fotogramma"))
                self._check("full", tr("Per tutto il video"), on_apply=self._apply_full)
                self._choice("origin", tr("Conta"), _options(overlays.TIMER_ORIGINS))
                self._choice("first", tr("Primo fotogramma"), {"0": "0", "1": "1"})
            else:
                self._section(tr("Tempo trascorso"))
                self._check("full", tr("Per tutto il video"), on_apply=self._apply_full)
                self._choice("format", tr("Formato"), _options(overlays.TIMER_FORMATS))
                self._choice("origin", tr("Conta"), _options(overlays.TIMER_ORIGINS))
            self._entry("prefix", tr("Testo davanti"), "str", width=170)
            self._entry("size", tr("Dimensione (px)"), "int")
            self._color("color", tr("Colore"))
            self._check("shadow", tr("Ombra"))
            self._slider("opacity", tr("Opacita'"), 0.0, 1.0)
            self._section(tr("Sfondo"))
            self._check("bg", tr("Sfondo dietro il tempo"))
            self._color("bg_color", tr("Colore sfondo"))
            self._slider("bg_alpha", tr("Opacita' sfondo"), 0.0, 1.0)
            self._slider("bg_radius", tr("Angoli arrotondati"), 0.0, 50.0, fmt=lambda v: f"{v:.0f} %")
            self._section(tr("Posizione"))
            row = ctk.CTkFrame(self.body, fg_color="transparent")
            row.pack(fill="x", pady=(4, 0))
            self._entry("x", "X", "int", width=70, row=row)
            self._entry("y", "  Y", "int", width=70, row=row)
            self._center_buttons(fx)
            widgets.note(self.body, tr("Sull'anteprima: trascinalo dove vuoi, dagli angoli per ingrandirlo."),
                         self.fonts, wraplength=280).pack(fill="x", pady=(6, 0))
        elif kind == "image":
            self._section(tr("Immagine"))
            row = ctk.CTkFrame(self.body, fg_color="transparent")
            row.pack(fill="x", pady=(6, 0))
            ctk.CTkLabel(row, text=tr("File"), font=self.fonts.small, text_color=theme.TEXT_SOFT, anchor="w", width=110).pack(side="left", padx=(0, 6))
            name = os.path.basename(fx.get("image") or "") or tr("nessuno")
            widgets.button(row, name if len(name) < 22 else name[:19] + "...", lambda: self._pick_image(fx),
                           width=170, height=28).pack(side="left")
            self._entry("w", tr("Larghezza (px)"), "int")
            self._slider("opacity", tr("Opacita'"), 0.0, 1.0)
            self._slider("radius", tr("Angoli arrotondati"), 0.0, 50.0, fmt=lambda v: f"{v:.0f} %")
            self._section(tr("Posizione"))
            row = ctk.CTkFrame(self.body, fg_color="transparent")
            row.pack(fill="x", pady=(4, 0))
            self._entry("x", "X", "int", width=70, row=row)
            self._entry("y", "  Y", "int", width=70, row=row)
            self._center_buttons(fx)
            widgets.note(self.body, tr("Sull'anteprima: trascina per spostarla, dagli angoli per ridimensionarla "
                                    "(le proporzioni restano quelle dell'immagine)."), self.fonts, wraplength=280).pack(fill="x", pady=(6, 0))
        elif kind in ("box", "oval"):
            self._section(tr("Riquadro") if kind == "box" else tr("Ovale"))
            row = ctk.CTkFrame(self.body, fg_color="transparent")
            row.pack(fill="x", pady=(4, 0))
            self._entry("x", "X", "int", width=70, row=row)
            self._entry("y", "  Y", "int", width=70, row=row)
            row = ctk.CTkFrame(self.body, fg_color="transparent")
            row.pack(fill="x", pady=(4, 0))
            self._entry("w", tr("Largh."), "int", width=70, row=row)
            self._entry("h", tr("  Alt."), "int", width=70, row=row)
            self._color("color", tr("Colore"))
            self._entry("thickness", tr("Spessore bordo"), "int")
            if kind == "box":
                self._slider("radius", tr("Angoli arrotondati"), 0.0, 50.0, fmt=lambda v: f"{v:.0f} %")
            self._check("fill", tr("Riempimento"))
            self._slider("fill_alpha", tr("Opacita' riempimento"), 0.0, 1.0)
            self._slider("opacity", tr("Opacita'"), 0.0, 1.0)
            self._build_follow(fx, tr("Il contenuto della figura fa da modello: la figura segue il soggetto nei "
                                   "fotogrammi successivi; quando esce dall'inquadratura l'effetto finisce."))
        elif kind == "arrow":
            self._section(tr("Freccia"))
            row = ctk.CTkFrame(self.body, fg_color="transparent")
            row.pack(fill="x", pady=(4, 0))
            self._entry("x1", tr("Coda X"), "int", width=70, row=row)
            self._entry("y1", "  Y", "int", width=70, row=row)
            row = ctk.CTkFrame(self.body, fg_color="transparent")
            row.pack(fill="x", pady=(4, 0))
            self._entry("x2", tr("Punta X"), "int", width=70, row=row)
            self._entry("y2", "  Y", "int", width=70, row=row)
            self._color("color", tr("Colore"))
            self._entry("thickness", tr("Spessore"), "int")
            self._slider("opacity", tr("Opacita'"), 0.0, 1.0)
            self._build_follow(fx, tr("Si disegna un rettangolo attorno al soggetto: la freccia lo segue nei "
                                   "fotogrammi successivi tenendo la punta su di lui; quando esce "
                                   "dall'inquadratura l'effetto finisce."))
            if fx.get("target"):
                self._button(tr("Scegli un altro soggetto"), lambda: self.app.pick_arrow_target(fx))
        elif kind == "zoom":
            self._section(tr("Area da ingrandire"))
            self._choice("shape", tr("Forma"), {"rect": tr("Rettangolare"), "oval": tr("Ovale")})
            self._slider("radius", tr("Angoli (rettangolare)"), 0.0, 50.0, fmt=lambda v: f"{v:.0f} %")
            row = ctk.CTkFrame(self.body, fg_color="transparent")
            row.pack(fill="x", pady=(4, 0))
            self._entry("x", "X", "int", width=70, row=row)
            self._entry("y", "  Y", "int", width=70, row=row)
            row = ctk.CTkFrame(self.body, fg_color="transparent")
            row.pack(fill="x", pady=(4, 0))
            self._entry("w", tr("Largh."), "int", width=70, row=row, on_apply=self._apply_zoom_area)
            self._entry("h", tr("  Alt."), "int", width=70, row=row, on_apply=self._apply_zoom_area)
            self._check("outline", tr("Contorno colorato sull'area ingrandita"))
            self._check("link", tr("Linea fra l'area e il riquadro"))
            self._section(tr("Riquadro ingrandito"))
            if fx.get("factor"):
                self._choice("factor", tr("Ingrandimento"), {str(f): f"{f}x" for f in overlays.ZOOM_FACTORS},
                             on_apply=self._apply_zoom_factor)
            row = ctk.CTkFrame(self.body, fg_color="transparent")
            row.pack(fill="x", pady=(4, 0))
            self._entry("bx", "X", "int", width=70, row=row)
            self._entry("by", "  Y", "int", width=70, row=row)
            if not fx.get("factor"):
                self._entry("bw", tr("Larghezza"), "int", on_apply=self._apply_zoom_width)
            self._color("color", tr("Colore"))
            self._entry("thickness", tr("Spessore bordo"), "int")
            widgets.note(self.body, tr("Il colore vale per il bordo del riquadro, il contorno dell'area e la linea. L'area scelta viene mostrata ingrandita nel riquadro, sopra il video, per la "
                                    "durata dell'effetto. Sull'anteprima: trascina l'area o il riquadro, "
                                    "ridimensiona l'area dagli angoli."), self.fonts, wraplength=280).pack(fill="x", pady=(6, 0))
            self._build_follow(fx, tr("L'area fa da modello: lo zoom segue l'oggetto nei fotogrammi successivi, "
                                   "il riquadro ingrandito resta dove l'hai messo. Se l'oggetto esce "
                                   "dall'inquadratura lo zoom finisce."))
        elif kind == "logo":
            self._section(tr("Logo e testo dell'operatore"))
            self._check("full", tr("Per tutto il video"), on_apply=self._apply_full)
            row = ctk.CTkFrame(self.body, fg_color="transparent")
            row.pack(fill="x", pady=(6, 0))
            ctk.CTkLabel(row, text=tr("Logo"), font=self.fonts.small, text_color=theme.TEXT_SOFT, anchor="w", width=110).pack(side="left", padx=(0, 6))
            name = os.path.basename(fx.get("logo") or "") or tr("nessuno")
            widgets.button(row, name if len(name) < 22 else name[:19] + "...", lambda: self._pick_logo(fx),
                           width=170, height=28).pack(side="left")
            self._entry("w", tr("Largh. logo (px)"), "int")
            self._entry("text", tr("Testo"), "str", width=170)
            self._entry("size", tr("Dimensione testo"), "int")
            self._color("color", tr("Colore testo"))
            self._choice("layout", tr("Disposizione"), _options(overlays.LOGO_LAYOUTS))
            self._check("shadow", tr("Ombra sotto il testo"))
            self._section(tr("Sfondo"))
            self._check("bg", tr("Sfondo sotto logo e scritta"))
            self._color("bg_color", tr("Colore sfondo"))
            self._slider("bg_alpha", tr("Opacita' sfondo"), 0.0, 1.0)
            self._slider("bg_radius", tr("Angoli arrotondati"), 0.0, 50.0, fmt=lambda v: f"{v:.0f} %")
            self._slider("opacity", tr("Opacita' di tutto"), 0.0, 1.0)
            self._section(tr("Posizione"))
            self._choice("corner", tr("Angolo"), _options(CORNERS), on_apply=self._apply_logo_corner)
            self._center_buttons(fx)
            row = ctk.CTkFrame(self.body, fg_color="transparent")
            row.pack(fill="x", pady=(4, 0))
            self._entry("x", "X", "int", width=70, row=row)
            self._entry("y", "  Y", "int", width=70, row=row)
            widgets.note(self.body, tr("Resta fermo nel punto scelto. Sull'anteprima trascinalo per spostarlo, tira un "
                                    "angolo per ingrandire o rimpicciolire logo e testo insieme. I valori proposti "
                                    "per i prossimi si cambiano in Configurazione."), self.fonts, wraplength=280).pack(fill="x", pady=(6, 0))
        elif kind == "pixelate":
            self._section(tr("Pixelatura"))
            points = len(fx.get("track") or [])
            self._label_row(tr("Inseguimento"), tr("{points} punti").format(points=points) if points else tr("fisso"))
            if fx.get("lost"):
                self._label_row(tr("Soggetto perso"), tr("{frames} fotogrammi").format(frames=fx["lost"]))
            self._choice("shape", tr("Forma"), {"rect": tr("Rettangolare"), "oval": tr("Ovale")})
            self._slider("radius", tr("Angoli (rettangolare)"), 0.0, 50.0, fmt=lambda v: f"{v:.0f} %")
            row = ctk.CTkFrame(self.body, fg_color="transparent")
            row.pack(fill="x", pady=(4, 0))
            self._entry("w", tr("Largh."), "int", width=70, row=row)
            self._entry("h", tr("  Alt."), "int", width=70, row=row)
            self._entry("block", tr("Grandezza pixel"), "int")
            widgets.note(self.body, tr("Ripeti l'inseguimento dopo aver cambiato inizio o fine."), self.fonts,
                         wraplength=280).pack(fill="x", pady=(6, 0))
            self._button(tr("Ripeti inseguimento dal cursore"), lambda: self.app.retrack(fx))
            self._build_keys(fx)
        self._button(tr("Elimina effetto"), lambda: self.app.delete_effect(fx["id"]), danger=True)

    def _build_follow(self, fx: dict, help_text: str) -> None:
        self._section(tr("Inseguimento del soggetto"))
        points = len(fx.get("track") or [])
        self._label_row(tr("Stato"), tr("segue il soggetto ({points} punti)").format(points=points) if points else tr("fermo"))
        widgets.note(self.body, help_text, self.fonts, wraplength=280).pack(fill="x", pady=(4, 0))
        self._button(tr("Ripeti inseguimento dal cursore") if points else tr("Segui il soggetto"),
                     lambda: self.app.retrack(fx), primary=not points)
        if points:
            self._button(tr("Non seguire piu'"), lambda: self.app.untrack(fx))
        self._build_keys(fx)

    def _build_keys(self, fx: dict) -> None:
        self._section(tr("Keyframe"))
        n = len(fx.get("keys") or [])
        self._label_row(tr("Keyframe"), str(n) if n else tr("nessuno"))
        widgets.note(self.body, tr("Dove l'inseguimento sbaglia: porta il cursore li' e trascina la figura sul soggetto "
                                "(dagli angoli per la misura). Diventa un keyframe: il tratto prima viene corretto e "
                                "l'inseguimento riparte da li' fino al keyframe successivo.\n"
                                "Nella timeline, sulla barra dell'effetto, i keyframe sono rombi e i punti "
                                "dell'inseguimento pallini. Clic: seleziona e porta il cursore; Maiusc+clic: "
                                "intervallo; Ctrl+clic: aggiunge o toglie. Canc o tasto destro: cancella i "
                                "selezionati (li' la figura va dritta fra i punti rimasti)."),
                     self.fonts, wraplength=280).pack(fill="x", pady=(4, 0))
        row = ctk.CTkFrame(self.body, fg_color="transparent")
        row.pack(fill="x", pady=(8, 0))
        widgets.button(row, tr("< Prec."), lambda: self.app.goto_key(fx, -1), width=80, height=28).pack(side="left")
        widgets.button(row, tr("Succ. >"), lambda: self.app.goto_key(fx, 1), width=80, height=28).pack(side="left", padx=(6, 0))
        self._button(tr("Keyframe qui (fissa la posizione)"), lambda: self.app.pin_key(fx))
        if n:
            self._button(tr("Togli keyframe al cursore"), lambda: self.app.delete_key_at(fx))
        if fx.get("track"):
            self._button(tr("Cancella i punti selezionati"), lambda: self.app.delete_selected_keys(fx))

    def _center_buttons(self, fx: dict) -> None:
        row = ctk.CTkFrame(self.body, fg_color="transparent")
        row.pack(fill="x", pady=(8, 0))
        widgets.button(row, tr("Centra orizz."), lambda: self.app.center_effect(fx, "x"), width=110, height=28).pack(side="left")
        widgets.button(row, tr("Centra vert."), lambda: self.app.center_effect(fx, "y"), width=110, height=28).pack(side="left", padx=(6, 0))

    def _pick_image(self, fx: dict) -> None:
        path = self.app.ask_image_file(fx.get("image") or "")
        if not path:
            return
        self._touch("image")
        fx["image"] = path
        self.app.project.dirty = True
        self.app.refresh()
        self.after(10, lambda: self.show("effect", fx))

    def _apply_full(self, key: str, value: Any) -> None:
        self.obj["full"] = bool(value)
        if value:
            self.app.project.sync_full()

    def _apply_logo_corner(self, key: str, value: Any) -> None:
        fx = self.obj
        fx["corner"] = value
        self.app.place_logo(fx)

    def _pick_logo(self, fx: dict) -> None:
        path = self.app.ask_logo_file(fx.get("logo") or "")
        if not path:
            return
        self._touch("logo")
        fx["logo"] = path
        if fx.get("corner"):
            self.app.place_logo(fx)
        self.app.project.dirty = True
        self.app.refresh()
        self.after(10, lambda: self.show("effect", fx))

    def _apply_zoom_width(self, key: str, value: Any) -> None:
        fx = self.obj
        fx["bw"] = max(16, int(value))
        fx["bh"] = max(16, int(round(fx["bw"] * fx["h"] / max(1, fx["w"]))))

    def _apply_zoom_area(self, key: str, value: Any) -> None:
        fx = self.obj
        W, H = self.app.project.width, self.app.project.height
        center = overlays.inset_center(fx, W, H)
        fx[key] = max(8, int(value))
        if fx.get("factor"):
            overlays.place_inset(fx, *center, W, H)    # stessa posizione, nuova misura
        else:
            fx["bh"] = max(16, int(round(fx.get("bw", 100) * fx["h"] / max(1, fx["w"]))))

    def _apply_zoom_factor(self, key: str, value: Any) -> None:
        fx = self.obj
        W, H = self.app.project.width, self.app.project.height
        center = overlays.inset_center(fx, W, H)
        fx["factor"] = int(value)
        overlays.place_inset(fx, *center, W, H)
        self.app.config_store.set("zoom_factor", fx["factor"])

    def _text_changed(self, box: ctk.CTkTextbox) -> None:
        text = box.get("1.0", "end-1c")
        if text != self.obj.get("text"):
            self._touch("text")
            self.obj["text"] = text
            self.app.project.dirty = True
            if self._job is not None:
                self.after_cancel(self._job)
            self._job = self.after(200, self._text_apply)

    def _text_apply(self) -> None:
        self._job = None
        self.app.refresh()

    def _build_oaudio_all(self) -> None:
        """Tutto l'audio originale dei video."""
        self._check("orig.on", tr("Audio originale attivo"))
        self._slider("original_volume", tr("Volume"), 0.0, 2.0)
        self._section(tr("Dissolvenze"))
        self._entry("orig.fade_in", tr("All'inizio (s)"), "float")
        self._entry("orig.fade_out", tr("Alla fine (s)"), "float")
        widgets.note(self.body, tr("Valgono per l'audio originale di tutto il video: sale all'inizio e scende alla "
                                "fine. Canc spegne tutto l'audio originale (il video resta). Per un solo pezzo "
                                "clicca la sua barra nella riga dell'audio."), self.fonts, wraplength=280).pack(fill="x", pady=(6, 0))
        self._button(tr("Elimina l'audio originale"), lambda: self.app.delete_selection(), danger=True)

    def _build_oaudio(self, clip: dict) -> None:
        """L'audio originale di un pezzo di video."""
        project = self.app.project
        index = project.clip_index(clip["id"])
        start = project.clip_start(index) if index >= 0 else 0.0
        self._label_row(tr("Pezzo"), f"{format_time(start)} - {format_time(start + clip_duration(clip))}")
        has_audio = project.source_info(clip["source"]).get("has_audio", False)
        if not has_audio:
            self._label_row(tr("Audio"), tr("il file non ha audio"))
            return
        self._check("audio", tr("Audio di questo pezzo"), on_apply=lambda k, v: clip.__setitem__("audio", bool(v)))
        self._slider("volume", tr("Volume di questo pezzo"), 0.0, 2.0)
        self._section(tr("Dissolvenze"))
        self._entry("afade_in", tr("Entrata (s)"), "float")
        self._entry("afade_out", tr("Uscita (s)"), "float")
        widgets.note(self.body, tr("Per togliere solo un tratto d'audio: segna IN e OUT (tasti I e O) e premi Canc con "
                                "l'audio selezionato: il video resta. Oppure taglia con S e seleziona il pezzo d'audio: "
                                "Canc lo elimina, qui ne regoli volume e dissolvenze."),
                     self.fonts, wraplength=280).pack(fill="x", pady=(6, 0))
        self._button(tr("Elimina audio di questo pezzo"), lambda: self.app.delete_clip_audio(clip["id"]), danger=True)

    def _build_audio(self, track: dict) -> None:
        self._label_row(tr("File"), track["source"])
        self._entry("name", tr("Nome"), "text", width=170)
        self._section(tr("Posizione"))
        self._time_row("start", tr("Inizio (s)"))
        self._section(tr("Porzione del file"))
        self._entry("in", tr("Dall'istante (s)"), "float")
        self._entry("out", tr("All'istante (s)"), "float")
        self._section(tr("Volume"))
        self._slider("volume", tr("Volume"), 0.0, 2.0)
        self._check("muted", tr("Muta"))
        self._section(tr("Dissolvenze"))
        self._entry("fade_in", tr("Entrata (s)"), "float")
        self._entry("fade_out", tr("Uscita (s)"), "float")
        widgets.note(self.body, tr("Il volume sale da zero all'inizio della traccia e scende a zero alla fine."),
                     self.fonts, wraplength=280).pack(fill="x", pady=(4, 0))
        self._button(tr("Elimina traccia"), lambda: self.app.delete_audio_track(track["id"]), danger=True)


def _contrast(color: str) -> str:
    color = color.lstrip("#")
    try:
        r, g, b = (int(color[i:i + 2], 16) / 255 for i in (0, 2, 4))
    except ValueError:
        return theme.TEXT
    return "#101418" if 0.2126 * r + 0.7152 * g + 0.0722 * b > 0.5 else "#f1f4fd"
