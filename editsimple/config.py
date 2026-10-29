# EditSimple — montaggio video per presentazioni.  Copyright (C) 2026 Andrea Cumini <andrea@osintinfo.net>
# SPDX-License-Identifier: GPL-3.0-only
# GNU GPL v3 con termini aggiuntivi (attribuzione dell'autore): vedi LICENSE e NOTICE.
"""Impostazioni salvate in config.json accanto al programma."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


def app_dir() -> Path:
    """Cartella base dell'applicazione: accanto all'eseguibile se impacchettata con PyInstaller.

    In un bundle --onefile __file__ sta in una cartella temporanea che sparisce
    alla chiusura: config.json e tools/ devono invece restare accanto all'exe.
    """
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parent.parent


APP_DIR = app_dir()
CONFIG_FILE = APP_DIR / "config.json"

DEFAULTS: dict[str, Any] = {
    "geometry": "",
    "language": "it",             # lingua dell'interfaccia (codici in locales/)
    "last_video_dir": "",
    "last_audio_dir": "",
    "last_project_dir": "",
    "last_export_dir": "",
    "recent": [],                 # ultimi progetti aperti
    # esportazione
    "export_crf": 20,             # qualita' H.264 (piu' basso = migliore, file piu' grande)
    "export_preset": "medium",
    "export_audio_kbps": 192,
    # valori proposti nei dialoghi
    "freeze_seconds": 3.0,
    "effect_seconds": 4.0,
    "speed_clock": True,
    "speed_last": 4,
    # pixelatura
    "pixel_block": 16,
    "track_min": 0.45,
    "zoom_factor": 2,
    "timeline_height": 250,       # altezza della timeline (divisore fra anteprima e timeline)
    "preview_window": "",         # posizione e misura della finestra dell'anteprima staccata
    # logo e testo dell'operatore (pulsante "Logo")
    "logo_path": "",
    "logo_width": 12.0,           # larghezza del logo in % della larghezza del video
    "operator_text": "",
    "operator_size": 3.5,         # altezza del testo in % del lato corto del video
    "operator_color": "#FFFFFF",
    "logo_corner": "bottom-right",
    "logo_layout": "right",
    # angoli arrotondati proposti ai nuovi effetti (% del lato corto, 0 = angoli vivi)
    "round_text": 25.0,
    "round_box": 0.0,
    "round_zoom": 0.0,
    "round_pixel": 0.0,
    "logo_bg": False,             # sfondo arrotondato sotto logo e scritta
    "logo_bg_color": "#000000",
    "logo_bg_alpha": 0.5,
    "logo_bg_radius": 25.0,       # angoli: % del lato corto dello sfondo
    "logo_margin": 3.0,           # distanza dai bordi in % del lato corto
    "last_logo_dir": "",
    # slide di apertura e chiusura
    "slide_seconds": 4.0,
    "slide_bg": "#0B1220",
    "slide_text_color": "#FFFFFF",
    # stile dell'ultimo testo scritto (proposto per il prossimo)
    "text_align": "center",
    "text_size": 0,
    "text_color": "#FFFFFF",
    "text_shadow": True,
    "text_bg": False,
    "text_center": False,
    "last_image_dir": "",
}


class Config:
    def __init__(self) -> None:
        self._data = dict(DEFAULTS)
        try:
            loaded = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
            if isinstance(loaded, dict):
                self._data.update({k: v for k, v in loaded.items() if k in DEFAULTS})
        except (OSError, ValueError):
            pass

    def get(self, key: str) -> Any:
        return self._data.get(key, DEFAULTS.get(key))

    def set(self, key: str, value: Any) -> None:
        self._data[key] = value

    def add_recent(self, path: str, limit: int = 8) -> None:
        recent = [p for p in self._data.get("recent", []) if p != path]
        self._data["recent"] = [path] + recent[:limit - 1]

    def save(self) -> None:
        try:
            CONFIG_FILE.write_text(json.dumps(self._data, indent=2, ensure_ascii=False),
                                   encoding="utf-8")
        except OSError:
            pass
