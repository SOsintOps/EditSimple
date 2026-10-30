# EditSimple — montaggio video per presentazioni.  Copyright (C) 2026 Andrea Cumini <andrea@osintinfo.net>
# SPDX-License-Identifier: GPL-3.0-only
# GNU GPL v3 con termini aggiuntivi (attribuzione dell'autore): vedi LICENSE e NOTICE.
"""Componenti riusati dall'interfaccia: riquadri, pulsanti, suggerimenti e dialoghi a tema."""

from __future__ import annotations

import tkinter as tk
from typing import Any, Callable

import customtkinter as ctk

from . import frameless, theme
from .i18n import N_, Text, again, tr, upper


class Card(ctk.CTkFrame):
    """Riquadro bordato con titolo in maiuscolo; il contenuto va dentro `body`."""

    def __init__(self, parent, title: str, fonts: theme.Fonts, **kwargs) -> None:
        super().__init__(parent, fg_color=theme.PANEL, border_width=1,
                         border_color=theme.BORDER, corner_radius=4, **kwargs)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        head = ctk.CTkFrame(self, fg_color="transparent", corner_radius=0)
        head.grid(row=0, column=0, sticky="ew", padx=theme.PAD, pady=(theme.PAD - 2, 0))
        ctk.CTkFrame(head, fg_color=theme.ACCENT, width=2, height=11, corner_radius=0).pack(
            side="left", padx=(0, 7))
        self._title = title
        self.title_label = ctk.CTkLabel(head, text=upper(title), font=fonts.title,
                                        text_color=theme.TEXT_DIM, anchor="w", height=14)
        self.title_label.pack(side="left", fill="x")
        self.head_right = ctk.CTkFrame(head, fg_color="transparent", corner_radius=0, width=1, height=1)
        self.head_right.pack(side="right")
        self.body = ctk.CTkFrame(self, fg_color="transparent", corner_radius=0)
        self.body.grid(row=1, column=0, sticky="nsew", padx=theme.PAD, pady=(theme.GAP, theme.PAD))

    def set_title(self, title: str) -> None:
        self._title = title
        self.title_label.configure(text=upper(title))

    def retranslate(self) -> None:
        """Il titolo in maiuscolo non ricorda la sua chiave: lo si ricompone nella lingua in uso."""
        self.title_label.configure(text=upper(again(self._title)))


def bind_wheel(widget, callback, modifier: str = "") -> None:
    """Lega la rotella del mouse a `callback(event)` su ogni sistema.

    Su Windows e macOS arriva <MouseWheel> con `event.delta`; su X11 (Linux)
    arrivano invece <Button-4> (su) e <Button-5> (giu') senza delta: qui si
    riempie `event.delta` con +120/-120, cosi' il gestore resta uno solo.
    `modifier` e' ad esempio "Control-" o "Shift-".
    """
    widget.bind(f"<{modifier}MouseWheel>", callback)

    def with_delta(delta: int):
        def handler(event):
            event.delta = delta
            return callback(event)
        return handler

    widget.bind(f"<{modifier}Button-4>", with_delta(120))
    widget.bind(f"<{modifier}Button-5>", with_delta(-120))


def button(parent, text: str, command, primary: bool = False, width: int = 0,
           danger: bool = False, **kwargs) -> ctk.CTkButton:
    """Pulsante principale (accento), secondario (neutro) o distruttivo (bordo rosso)."""
    if danger:
        kwargs.setdefault("fg_color", "transparent")
        kwargs.setdefault("hover_color", theme.HOVER)
        kwargs.setdefault("border_width", 1)
        kwargs.setdefault("border_color", theme.ERR)
        kwargs.setdefault("text_color", theme.ERR)
    elif not primary:
        kwargs.setdefault("fg_color", theme.NEUTRAL)
        kwargs.setdefault("hover_color", theme.NEUTRAL_HOVER)
        kwargs.setdefault("text_color", theme.TEXT)
    kwargs.setdefault("font", (theme.ui_font(), 12, "bold"))
    kwargs.setdefault("height", 30)
    if width:
        kwargs["width"] = width
    return ctk.CTkButton(parent, text=text, command=command, **kwargs)


def icon_button(parent, glyph: str, fallback: str, command, fonts: theme.Fonts,
                width: int = 34, tooltip: str = "", **kwargs) -> ctk.CTkButton:
    """Pulsante quadrato con un glifo di Segoe Fluent Icons (o un carattere di riserva)."""
    has_icons = bool(theme.icon_font())
    kwargs.setdefault("fg_color", theme.NEUTRAL)
    kwargs.setdefault("hover_color", theme.NEUTRAL_HOVER)
    kwargs.setdefault("text_color", theme.TEXT)
    item = ctk.CTkButton(
        parent, text=glyph if has_icons else fallback, command=command, width=width, height=30,
        corner_radius=4, font=fonts.icon(13) if has_icons else fonts.bold, **kwargs,
    )
    if tooltip:
        Tooltip(item, tooltip, fonts)
    return item


def note(parent, text: str, fonts: theme.Fonts, wraplength: int = 0) -> ctk.CTkLabel:
    """Testo esplicativo attenuato."""
    return ctk.CTkLabel(parent, text=text, font=fonts.small, text_color=theme.TEXT_DIM,
                        anchor="w", justify="left", wraplength=wraplength)


def caption(parent, text: str, fonts: theme.Fonts, **kwargs) -> ctk.CTkLabel:
    """Etichetta maiuscola piccola sopra un campo."""
    kwargs.setdefault("text_color", theme.TEXT_FAINT)
    label = ctk.CTkLabel(parent, text=upper(text), font=fonts.caption, anchor="w", **kwargs)
    # Il maiuscolo perde la chiave del testo: al cambio di lingua lo si ricompone.
    label.retranslate = lambda: label.configure(text=upper(again(text)))
    return label


def rule(parent, horizontal: bool) -> ctk.CTkFrame:
    """Filetto di separazione da un pixel."""
    size = {"height": 1} if horizontal else {"width": 1}
    return ctk.CTkFrame(parent, fg_color=theme.BORDER, corner_radius=0, **size)


class Tooltip:
    """Suggerimento che compare sotto il widget al passaggio del mouse."""

    def __init__(self, widget, text: str, fonts: theme.Fonts, delay_ms: int = 500) -> None:
        self._widget = widget
        self._text = text
        self._fonts = fonts
        self._delay = delay_ms
        self._job: str | None = None
        self._tip: ctk.CTkToplevel | None = None
        widget.bind("<Enter>", self._schedule, add="+")
        widget.bind("<Leave>", self._hide, add="+")
        widget.bind("<ButtonPress>", self._hide, add="+")

    def _schedule(self, _event=None) -> None:
        self._cancel()
        self._job = self._widget.after(self._delay, self._show)

    def _cancel(self) -> None:
        if self._job is not None:
            self._widget.after_cancel(self._job)
            self._job = None

    def _show(self) -> None:
        self._job = None
        if self._tip is not None:
            return
        try:
            tip = ctk.CTkToplevel(self._widget)
            tip.overrideredirect(True)
            tip.attributes("-topmost", True)
            tip.configure(fg_color=theme.BORDER)
            ctk.CTkLabel(tip, text=f"  {again(self._text)}  ", font=self._fonts.small, text_color=theme.TEXT,
                         fg_color=theme.PANEL_2, corner_radius=0, height=24).pack(padx=1, pady=1)
            x = self._widget.winfo_rootx()
            y = self._widget.winfo_rooty() + self._widget.winfo_height() + 6
            tip.geometry(f"+{x}+{y}")
            self._tip = tip
        except tk.TclError:
            self._tip = None

    def _hide(self, _event=None) -> None:
        self._cancel()
        tip, self._tip = self._tip, None
        if tip is not None:
            try:
                tip.destroy()
            except tk.TclError:
                pass


# ----------------------------------------------------------------- lingua

def retranslate_all(widget) -> None:
    """Porta nella lingua in uso i testi di `widget` e di tutto cio' che contiene.

    Un widget conserva il testo ricevuto: se viene da tr() ha con se' la propria
    chiave e basta ritradurlo. Chi il testo lo compone (titoli in maiuscolo,
    pulsanti con icona) espone un metodo retranslate().
    """
    for option in ("text", "placeholder_text"):
        try:
            value = widget.cget(option)
        except (ValueError, AttributeError, KeyError, tk.TclError):
            continue  # il widget non ha questa opzione
        if isinstance(value, Text):
            widget.configure(**{option: again(value)})
    own = getattr(widget, "retranslate", None)
    if callable(own):
        own()
    for child in widget.winfo_children():
        retranslate_all(child)


# ----------------------------------------------------------------- dialoghi

def style_dialog(window, logo: bool = True) -> None:
    """Barra del titolo scura, icona di EditSimple e (in alto a sinistra) il logo piccolo.

    Va chiamata prima di riempire la finestra: il logo si impacchetta per primo.
    """
    window.after(60, lambda: frameless.style_titlebar(window, theme.PANEL, theme.TEXT, theme.BORDER))
    # customtkinter mette la sua icona poco dopo l'apertura: la nostra va rimessa dopo
    window.after(260, lambda: theme.set_icon(window))
    if logo:
        image = theme.logo(11)
        if image is not None:
            ctk.CTkLabel(window, text="", image=image, anchor="w").pack(fill="x", padx=16, pady=(10, 0))


def _place(window, parent, width: int, height: int) -> None:
    try:
        px, py = parent.winfo_rootx(), parent.winfo_rooty()
        pw, ph = parent.winfo_width(), parent.winfo_height()
    except tk.TclError:
        px = py = 100
        pw, ph = width, height
    window.geometry(f"{width}x{height}+{max(0, px + (pw - width) // 2)}+{max(0, py + (ph - height) // 3)}")


_TAG = {"info": (N_("INFO"), theme.ACCENT), "question": (N_("CONFERMA"), theme.ACCENT),
        "warning": (N_("ATTENZIONE"), theme.WARN), "error": (N_("ERRORE"), theme.ERR)}


def _show(kind: str, title: str, message: str, buttons: list[tuple[str, Any, bool]], parent=None):
    """Dialogo modale a tema; `buttons` = [(testo, valore, principale)]. Restituisce il valore scelto."""
    parent = parent or tk._default_root
    win = ctk.CTkToplevel(parent)
    win.title(title)
    win.configure(fg_color=theme.BG)
    win.transient(parent)
    win.resizable(False, False)
    style_dialog(win)
    fonts = theme.Fonts()
    result = {"value": None}

    def close(value) -> None:
        result["value"] = value
        try:
            win.grab_release()
        except tk.TclError:
            pass
        win.destroy()

    box = ctk.CTkFrame(win, fg_color=theme.PANEL, border_width=1, border_color=theme.BORDER, corner_radius=4)
    box.pack(fill="both", expand=True, padx=14, pady=14)
    tag, color = _TAG.get(kind, _TAG["info"])
    head = ctk.CTkFrame(box, fg_color="transparent")
    head.pack(fill="x", padx=16, pady=(14, 4))
    ctk.CTkFrame(head, fg_color=color, width=2, height=11, corner_radius=0).pack(side="left", padx=(0, 7))
    ctk.CTkLabel(head, text=upper(tr(tag)), font=fonts.title, text_color=color).pack(side="left")
    ctk.CTkLabel(box, text=title, font=fonts.page, text_color=theme.TEXT, anchor="w",
                 justify="left").pack(fill="x", padx=16)
    ctk.CTkLabel(box, text=message, font=fonts.body, text_color=theme.TEXT_SOFT, anchor="w",
                 justify="left", wraplength=440).pack(fill="x", padx=16, pady=(8, 16))
    row = ctk.CTkFrame(box, fg_color="transparent")
    row.pack(fill="x", padx=16, pady=(0, 14))
    first = None
    for text, value, primary in reversed(buttons):
        item = button(row, text, lambda v=value: close(v), primary=primary, width=100)
        item.pack(side="right", padx=(8, 0))
        first = item
    win.bind("<Escape>", lambda _e: close(buttons[-1][1]))
    win.bind("<Return>", lambda _e: close(buttons[0][1]))
    win.update_idletasks()
    width = max(380, min(520, win.winfo_reqwidth()))
    _place(win, parent, width, win.winfo_reqheight())
    win.after(120, win.grab_set)
    if first is not None:
        first.focus_set()
    win.wait_window()
    return result["value"]


class messagebox:
    """Sostituti a tema di tkinter.messagebox."""

    @staticmethod
    def showinfo(title: str, message: str, parent=None) -> None:
        _show("info", title, message, [(tr("OK"), True, True)], parent)

    @staticmethod
    def showwarning(title: str, message: str, parent=None) -> None:
        _show("warning", title, message, [(tr("OK"), True, True)], parent)

    @staticmethod
    def showerror(title: str, message: str, parent=None) -> None:
        _show("error", title, message, [(tr("OK"), True, True)], parent)

    @staticmethod
    def askyesno(title: str, message: str, parent=None, yes: str | None = None, no: str | None = None) -> bool:
        yes, no = yes or tr("Si'"), no or tr("No")
        return bool(_show("question", title, message, [(yes, True, True), (no, False, False)], parent))

    @staticmethod
    def askyesnocancel(title: str, message: str, parent=None, yes: str | None = None, no: str | None = None):
        yes, no = yes or tr("Si'"), no or tr("No")
        return _show("question", title, message,
                     [(yes, True, True), (no, False, False), (tr("Annulla"), None, False)], parent)


class FormDialog(ctk.CTkToplevel):
    """Dialogo modale con alcuni campi; `result` e' il dizionario dei valori o None se annullato.

    Ogni campo e' un dizionario: key, label, kind ("float", "int", "text", "choice",
    "check"), default, options (per choice), help (nota sotto il campo), min, max.
    """

    def __init__(self, parent, title: str, fields: list[dict], fonts: theme.Fonts,
                 ok_text: str | None = None, intro: str = "") -> None:
        super().__init__(parent)
        ok_text = ok_text or tr("OK")
        self.title(title)
        self.configure(fg_color=theme.BG)
        self.transient(parent)
        self.resizable(False, False)
        style_dialog(self)
        self.result: dict | None = None
        self._fields = fields
        self._vars: dict[str, tk.Variable] = {}
        self._fonts = fonts

        box = ctk.CTkFrame(self, fg_color=theme.PANEL, border_width=1, border_color=theme.BORDER, corner_radius=4)
        box.pack(fill="both", expand=True, padx=14, pady=14)
        ctk.CTkLabel(box, text=title, font=fonts.page, text_color=theme.TEXT, anchor="w").pack(
            fill="x", padx=16, pady=(14, 2))
        if intro:
            ctk.CTkLabel(box, text=intro, font=fonts.small, text_color=theme.TEXT_DIM, anchor="w",
                         justify="left", wraplength=420).pack(fill="x", padx=16, pady=(0, 6))
        first_entry = None
        for field in fields:
            kind = field.get("kind", "text")
            key = field["key"]
            if kind == "check":
                var = tk.BooleanVar(value=bool(field.get("default", False)))
                ctk.CTkCheckBox(box, text=field["label"], variable=var, font=fonts.body).pack(
                    fill="x", padx=16, pady=(10, 0))
            elif kind == "choice":
                var = tk.StringVar(value=str(field.get("default", field["options"][0])))
                caption(box, field["label"], fonts).pack(fill="x", padx=16, pady=(10, 2))
                if len(field["options"]) <= 6:
                    row = ctk.CTkFrame(box, fg_color="transparent")
                    row.pack(fill="x", padx=16)
                    for option in field["options"]:
                        ctk.CTkRadioButton(row, text=str(option), variable=var, value=str(option),
                                           font=fonts.body, width=70).pack(side="left", padx=(0, 10))
                else:
                    ctk.CTkOptionMenu(box, variable=var, values=[str(o) for o in field["options"]],
                                      font=fonts.body).pack(fill="x", padx=16)
            else:
                var = tk.StringVar(value=str(field.get("default", "")))
                caption(box, field["label"], fonts).pack(fill="x", padx=16, pady=(10, 2))
                entry = ctk.CTkEntry(box, textvariable=var, font=fonts.body, height=32)
                entry.pack(fill="x", padx=16)
                if first_entry is None:
                    first_entry = entry
            if field.get("help"):
                note(box, field["help"], fonts, wraplength=420).pack(fill="x", padx=16, pady=(2, 0))
            self._vars[key] = var
        self._error = ctk.CTkLabel(box, text="", font=fonts.small, text_color=theme.ERR, anchor="w")
        self._error.pack(fill="x", padx=16, pady=(8, 0))
        row = ctk.CTkFrame(box, fg_color="transparent")
        row.pack(fill="x", padx=16, pady=(4, 14))
        button(row, ok_text, self._ok, primary=True, width=110).pack(side="right")
        button(row, tr("Annulla"), self._cancel, width=100).pack(side="right", padx=(0, 8))
        self.bind("<Return>", lambda _e: self._ok())
        self.bind("<Escape>", lambda _e: self._cancel())
        self.update_idletasks()
        _place(self, parent, max(420, self.winfo_reqwidth()), self.winfo_reqheight())
        self.after(120, self.grab_set)
        (first_entry or self).focus_set()
        if first_entry is not None:
            first_entry.after(150, lambda: first_entry.select_range(0, "end"))

    def _ok(self) -> None:
        values: dict[str, Any] = {}
        for field in self._fields:
            kind = field.get("kind", "text")
            raw = self._vars[field["key"]].get()
            if kind in ("float", "int"):
                try:
                    value = float(str(raw).replace(",", "."))
                    if kind == "int":
                        value = int(round(value))
                except ValueError:
                    self._error.configure(text=tr("{field}: inserisci un numero.").format(field=field["label"]))
                    return
                lo, hi = field.get("min"), field.get("max")
                if (lo is not None and value < lo) or (hi is not None and value > hi):
                    self._error.configure(text=tr("{field}: valore fra {min:g} e {max:g}.").format(
                        field=field["label"], min=lo, max=hi))
                    return
                values[field["key"]] = value
            elif kind == "choice":
                options = field["options"]
                chosen = next((o for o in options if str(o) == str(raw)), options[0])
                values[field["key"]] = chosen
            else:
                values[field["key"]] = raw
        self.result = values
        self._close()

    def _cancel(self) -> None:
        self.result = None
        self._close()

    def _close(self) -> None:
        try:
            self.grab_release()
        except tk.TclError:
            pass
        self.destroy()


def ask_form(parent, title: str, fields: list[dict], fonts: theme.Fonts, ok_text: str | None = None,
             intro: str = "") -> dict | None:
    dialog = FormDialog(parent, title, fields, fonts, ok_text=ok_text, intro=intro)
    dialog.wait_window()
    return dialog.result


# Valori da mostrare con tr(); la mappa inversa si costruisce sulle etichette tradotte.
ALIGN_NAMES = {"left": N_("Sinistra"), "center": N_("Centro"), "right": N_("Destra")}


class TextDialog(ctk.CTkToplevel):
    """Scrittura di un testo: piu' righe, allineamento, dimensione, colore, ombra, fondo, centratura.

    Invio va a capo; Ctrl+Invio (o il pulsante) conferma. `result` e' il
    dizionario dei valori o None se annullato.
    """

    def __init__(self, parent, fonts: theme.Fonts, values: dict, title: str | None = None) -> None:
        super().__init__(parent)
        title = title or tr("Testo")
        self.title(title)
        self.configure(fg_color=theme.BG)
        self.transient(parent)
        self.resizable(False, False)
        style_dialog(self)
        self.result: dict | None = None
        self._color = str(values.get("color") or "#FFFFFF").upper()
        box = ctk.CTkFrame(self, fg_color=theme.PANEL, border_width=1, border_color=theme.BORDER, corner_radius=4)
        box.pack(fill="both", expand=True, padx=14, pady=14)
        ctk.CTkLabel(box, text=title, font=fonts.page, text_color=theme.TEXT, anchor="w").pack(fill="x", padx=16, pady=(14, 2))
        note(box, tr("Invio va a capo, Ctrl+Invio conferma."), fonts, wraplength=460).pack(fill="x", padx=16)
        self.text = ctk.CTkTextbox(box, width=460, height=130, font=fonts.body, wrap="word")
        self.text.pack(fill="x", padx=16, pady=(8, 0))
        self.text.insert("1.0", str(values.get("text") or ""))
        caption(box, tr("Allineamento delle righe"), fonts).pack(fill="x", padx=16, pady=(10, 2))
        self.align = tk.StringVar(value=tr(ALIGN_NAMES.get(values.get("align"), ALIGN_NAMES["center"])))
        row = ctk.CTkFrame(box, fg_color="transparent")
        row.pack(fill="x", padx=16)
        for name in map(tr, ALIGN_NAMES.values()):
            ctk.CTkRadioButton(row, text=name, variable=self.align, value=name, font=fonts.body, width=70).pack(side="left", padx=(0, 10))
        row = ctk.CTkFrame(box, fg_color="transparent")
        row.pack(fill="x", padx=16, pady=(10, 0))
        ctk.CTkLabel(row, text=tr("Dimensione (px)"), font=fonts.small, text_color=theme.TEXT_SOFT).pack(side="left")
        self.size = tk.StringVar(value=str(int(values.get("size") or 48)))
        ctk.CTkEntry(row, textvariable=self.size, width=70, font=fonts.body).pack(side="left", padx=(6, 16))
        ctk.CTkLabel(row, text=tr("Colore"), font=fonts.small, text_color=theme.TEXT_SOFT).pack(side="left")
        self.color_button = ctk.CTkButton(row, text=self._color, width=96, height=28, font=fonts.mono, command=self._pick)
        self.color_button.pack(side="left", padx=(6, 0))
        self._show_color()
        self.shadow = tk.BooleanVar(value=bool(values.get("shadow", True)))
        self.bg = tk.BooleanVar(value=bool(values.get("bg", False)))
        self.center = tk.BooleanVar(value=bool(values.get("center", False)))
        row = ctk.CTkFrame(box, fg_color="transparent")
        row.pack(fill="x", padx=16, pady=(10, 0))
        ctk.CTkCheckBox(row, text=tr("Ombra"), variable=self.shadow, font=fonts.body).pack(side="left", padx=(0, 14))
        ctk.CTkCheckBox(row, text=tr("Fondo scuro"), variable=self.bg, font=fonts.body).pack(side="left", padx=(0, 14))
        ctk.CTkCheckBox(row, text=tr("Centra nel video"), variable=self.center, font=fonts.body).pack(side="left")
        self._error = ctk.CTkLabel(box, text="", font=fonts.small, text_color=theme.ERR, anchor="w")
        self._error.pack(fill="x", padx=16, pady=(6, 0))
        row = ctk.CTkFrame(box, fg_color="transparent")
        row.pack(fill="x", padx=16, pady=(4, 14))
        button(row, tr("OK"), self._ok, primary=True, width=110).pack(side="right")
        button(row, tr("Annulla"), self._cancel, width=100).pack(side="right", padx=(0, 8))
        self.bind("<Control-Return>", lambda _e: self._ok())
        self.bind("<Escape>", lambda _e: self._cancel())
        self.protocol("WM_DELETE_WINDOW", self._cancel)
        self.after(50, self.text.focus_set)
        self.grab_set()

    def _pick(self) -> None:
        from tkinter import colorchooser
        _rgb, hexcolor = colorchooser.askcolor(color=self._color, title=tr("Colore del testo"), parent=self)
        if hexcolor:
            self._color = hexcolor.upper()
            self._show_color()

    def _show_color(self) -> None:
        c = self._color.lstrip("#")
        r, g, b = int(c[0:2], 16), int(c[2:4], 16), int(c[4:6], 16)
        self.color_button.configure(text=self._color, fg_color=self._color, hover_color=self._color,
                                    text_color="#000000" if r * 0.299 + g * 0.587 + b * 0.114 > 150 else "#FFFFFF")

    def _ok(self) -> None:
        text = self.text.get("1.0", "end-1c").rstrip()
        if not text.strip():
            self._error.configure(text=tr("Scrivi il testo."))
            return
        try:
            size = int(float(self.size.get().replace(",", ".")))
        except ValueError:
            self._error.configure(text=tr("Dimensione non valida."))
            return
        inverse = {str(tr(v)): k for k, v in ALIGN_NAMES.items()}
        self.result = {"text": text, "align": inverse.get(self.align.get(), "center"), "size": max(6, min(1000, size)),
                       "color": self._color, "shadow": bool(self.shadow.get()), "bg": bool(self.bg.get()),
                       "center": bool(self.center.get())}
        self.destroy()

    def _cancel(self) -> None:
        self.result = None
        self.destroy()


def ask_text(parent, fonts: theme.Fonts, values: dict, title: str | None = None) -> dict | None:
    dialog = TextDialog(parent, fonts, values, title)
    dialog.wait_window()
    return dialog.result


class ProgressDialog(ctk.CTkToplevel):
    """Finestra di avanzamento con pulsante Annulla; `set()` si puo' chiamare dal thread principale."""

    def __init__(self, parent, title: str, fonts: theme.Fonts, on_cancel: Callable[[], None] | None = None) -> None:
        super().__init__(parent)
        self.title(title)
        self.configure(fg_color=theme.BG)
        self.transient(parent)
        self.resizable(False, False)
        style_dialog(self)
        self._on_cancel = on_cancel
        box = ctk.CTkFrame(self, fg_color=theme.PANEL, border_width=1, border_color=theme.BORDER, corner_radius=4)
        box.pack(fill="both", expand=True, padx=14, pady=14)
        ctk.CTkLabel(box, text=title, font=fonts.page, text_color=theme.TEXT, anchor="w").pack(
            fill="x", padx=16, pady=(14, 6))
        self._label = ctk.CTkLabel(box, text="", font=fonts.body, text_color=theme.TEXT_SOFT, anchor="w")
        self._label.pack(fill="x", padx=16)
        self._bar = ctk.CTkProgressBar(box, height=8)
        self._bar.pack(fill="x", padx=16, pady=(10, 4))
        self._bar.set(0)
        self._percent = ctk.CTkLabel(box, text="0 %", font=fonts.mono, text_color=theme.TEXT_DIM, anchor="e")
        self._percent.pack(fill="x", padx=16)
        row = ctk.CTkFrame(box, fg_color="transparent")
        row.pack(fill="x", padx=16, pady=(8, 14))
        self._cancel_btn = button(row, tr("Annulla"), self._cancel, width=100)
        self._cancel_btn.pack(side="right")
        self.protocol("WM_DELETE_WINDOW", self._cancel)
        self.update_idletasks()
        _place(self, parent, 460, self.winfo_reqheight())
        self.after(120, self.grab_set)

    def set(self, message: str, fraction: float) -> None:
        try:
            self._label.configure(text=message)
            self._bar.set(max(0.0, min(1.0, fraction)))
            self._percent.configure(text=f"{int(round(fraction * 100))} %")
        except tk.TclError:
            pass

    def _cancel(self) -> None:
        if self._on_cancel is not None:
            self._on_cancel()
        self._cancel_btn.configure(state="disabled", text=tr("Interruzione..."))

    def close(self) -> None:
        try:
            self.grab_release()
        except tk.TclError:
            pass
        try:
            self.destroy()
        except tk.TclError:
            pass
