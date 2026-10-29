# EditSimple — montaggio video per presentazioni.  Copyright (C) 2026 Andrea Cumini <andrea@osintinfo.net>
# SPDX-License-Identifier: GPL-3.0-only
# GNU GPL v3 con termini aggiuntivi (attribuzione dell'autore): vedi LICENSE e NOTICE.
"""Caratteri per le sovraimpressioni: la cartella font/ del programma e quelli di Windows.

Il carattere e' identificato dal nome del file (es. "DejaVuSans-Bold.ttf"):
prima si cerca in font/ accanto al programma, poi tra i caratteri di sistema.
La finestra di scelta mostra ogni carattere scrivendo con il carattere stesso
un testo di prova.
"""

from __future__ import annotations

import os
import sys
import tkinter as tk
from pathlib import Path
from typing import Callable

import customtkinter as ctk
from PIL import Image, ImageDraw, ImageFont

from . import theme, widgets
from .config import APP_DIR
from .i18n import tr

FONT_DIR = APP_DIR / "font"
BUNDLED_DIR = Path(getattr(sys, "_MEIPASS", "")) / "font"   # dentro l'eseguibile PyInstaller
SYSTEM_DIRS = [
    BUNDLED_DIR,
    Path(os.environ.get("WINDIR", r"C:\Windows")) / "Fonts",
    Path(os.environ.get("LOCALAPPDATA", "")) / "Microsoft" / "Windows" / "Fonts",
]
EXTENSIONS = (".ttf", ".otf")
DEFAULT_FONT = "DejaVuSans-Bold.ttf"
PREFERRED = ["segoeuib.ttf", "arialbd.ttf", "DejaVuSans-Bold.ttf"]

_paths: dict[str, str] = {}
_loaded: dict[tuple[str, int], ImageFont.FreeTypeFont] = {}


def _scan() -> dict[str, str]:
    if _paths:
        return _paths
    for folder in [FONT_DIR] + SYSTEM_DIRS:
        try:
            names = sorted(os.listdir(folder), key=str.lower)
        except OSError:
            continue
        for name in names:
            if name.lower().endswith(EXTENSIONS) and name.lower() not in {k.lower() for k in _paths}:
                _paths[name] = str(folder / name)
    return _paths


def list_fonts() -> list[str]:
    """Nomi dei file dei caratteri disponibili (prima quelli di font/, poi quelli di sistema)."""
    return sorted(_scan(), key=lambda n: (not n.lower().startswith("dejavu"), n.lower()))


def font_path(name: str) -> str:
    paths = _scan()
    if name in paths:
        return paths[name]
    lowered = {k.lower(): v for k, v in paths.items()}
    if name.lower() in lowered:
        return lowered[name.lower()]
    if os.path.isabs(name) and os.path.isfile(name):
        return name
    return paths.get(DEFAULT_FONT) or next(iter(paths.values()), "")


def default_font() -> str:
    names = {n.lower(): n for n in _scan()}
    for candidate in PREFERRED:
        if candidate.lower() in names:
            return names[candidate.lower()]
    return DEFAULT_FONT


def load_font(name: str, size: float) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    size = max(4, int(round(size)))
    key = (name, size)
    font = _loaded.get(key)
    if font is None:
        try:
            font = ImageFont.truetype(font_path(name), size, layout_engine=ImageFont.Layout.BASIC)
        except (OSError, ValueError):
            font = ImageFont.load_default(size)
        if len(_loaded) > 64:
            _loaded.clear()
        _loaded[key] = font
    return font


def display_name(name: str) -> str:
    return os.path.splitext(os.path.basename(name))[0]


# ----------------------------------------------------------- scelta

class FontPicker(ctk.CTkToplevel):
    """Finestra di scelta del carattere: ogni riga scrive il testo di prova con il carattere stesso.

    Le righe si costruiscono a blocchi, cosi' la finestra resta reattiva anche
    con centinaia di caratteri di sistema.
    """

    def __init__(self, parent, fonts: theme.Fonts, current: str, sample: str,
                 on_choose: Callable[[str], None]) -> None:
        super().__init__(parent)
        self.title(tr("Scegli il carattere"))
        self.geometry(f"640x680+{parent.winfo_rootx() + 220}+{parent.winfo_rooty() + 60}")
        self.configure(fg_color=theme.BG)
        self.transient(parent)
        widgets.style_dialog(self)
        self._fonts = fonts
        self._on_choose = on_choose
        self._sample = (sample.strip().splitlines() or [tr("Testo di prova")])[0][:40] or tr("Testo di prova")
        self._current = current
        self._rows: list[tuple[str, ctk.CTkFrame]] = []
        self._pending = iter(list_fonts())
        self._job: str | None = None
        self._images: list = []

        head = ctk.CTkFrame(self, fg_color="transparent")
        head.pack(fill="x", padx=14, pady=(14, 6))
        self._search = tk.StringVar()
        entry = ctk.CTkEntry(head, textvariable=self._search, placeholder_text=tr("Cerca carattere..."),
                             height=32, font=fonts.body)
        entry.pack(side="left", fill="x", expand=True)
        self._count = ctk.CTkLabel(head, text="", font=fonts.caption, text_color=theme.TEXT_DIM)
        self._count.pack(side="left", padx=(10, 0))
        ctk.CTkLabel(self, text=tr("Caratteri della cartella font/ e di Windows, mostrati con il testo "
                                   "\u00ab{sample}\u00bb. Clicca per scegliere.").format(sample=self._sample),
                     font=fonts.small, text_color=theme.TEXT_DIM, anchor="w", justify="left",
                     wraplength=600).pack(fill="x", padx=14)
        self._list = ctk.CTkScrollableFrame(self, fg_color=theme.PANEL, corner_radius=6)
        self._list.pack(fill="both", expand=True, padx=14, pady=(8, 14))

        self._search.trace_add("write", lambda *_: self._filter())
        self.bind("<Escape>", lambda _e: self.destroy())
        self.after(150, self.grab_set)
        entry.focus_set()
        self._build_some()

    def _preview(self, path: str, px: int = 26):
        size = px * 2
        face = ImageFont.truetype(path, size, layout_engine=ImageFont.Layout.BASIC)
        width = int(min(max(face.getlength(self._sample) + 24, 120), 1100))
        height = int(size * 1.55)
        image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        ImageDraw.Draw(image).text((12, int(height * 0.72)), self._sample, font=face,
                                   fill=theme.TEXT, anchor="ls")
        return ctk.CTkImage(light_image=image, dark_image=image, size=(width // 2, height // 2))

    def _make_row(self, name: str):
        try:
            image = self._preview(font_path(name))
        except Exception:  # noqa: BLE001 - carattere non leggibile da PIL
            return None
        selected = name == self._current
        row = ctk.CTkFrame(self._list, fg_color=theme.SELECT_BG if selected else theme.PANEL_2,
                           corner_radius=4, border_width=1,
                           border_color=theme.ACCENT if selected else theme.BORDER, cursor="hand2")
        label = ctk.CTkLabel(row, text=name, font=self._fonts.tiny, text_color=theme.TEXT_SOFT, anchor="w")
        label.pack(fill="x", padx=10, pady=(5, 0))
        picture = ctk.CTkLabel(row, text="", image=image, anchor="w")
        picture.pack(fill="x", padx=6, pady=(0, 4))
        self._images.append(image)
        for widget in (row, label, picture):
            widget.bind("<Button-1>", lambda _e, n=name: self._choose(n))
        return row

    def _matches(self, name: str) -> bool:
        query = self._search.get().strip().lower()
        return not query or query in name.lower()

    def _build_some(self) -> None:
        for _ in range(8):
            name = next(self._pending, None)
            if name is None:
                self._job = None
                self._update_count(loading=False)
                return
            row = self._make_row(name)
            if row is None:
                continue
            self._rows.append((name, row))
            if self._matches(name):
                row.pack(fill="x", padx=4, pady=3)
        self._update_count(loading=True)
        if self.winfo_exists():
            self._job = self.after(1, self._build_some)

    def _update_count(self, loading: bool) -> None:
        shown = sum(1 for name, _ in self._rows if self._matches(name))
        if loading:
            text = tr("{shown} / {total}  - caricamento...").format(shown=shown, total=len(self._rows))
        else:
            text = f"{shown} / {len(self._rows)}"
        self._count.configure(text=text)

    def _filter(self) -> None:
        for _, row in self._rows:
            row.pack_forget()
        for name, row in self._rows:
            if self._matches(name):
                row.pack(fill="x", padx=4, pady=3)
        self._update_count(loading=self._job is not None)

    def _choose(self, name: str) -> None:
        self._on_choose(name)
        self.destroy()

    def destroy(self) -> None:
        if self._job is not None:
            try:
                self.after_cancel(self._job)
            except tk.TclError:
                pass
            self._job = None
        super().destroy()
