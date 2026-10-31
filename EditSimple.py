# EditSimple — montaggio video per presentazioni.  Copyright (C) 2026 Andrea Cumini <andrea@osintinfo.net>
# SPDX-License-Identifier: GPL-3.0-only
# GNU GPL v3 con termini aggiuntivi (attribuzione dell'autore): vedi LICENSE e NOTICE.
"""EditSimple - punto di ingresso.

Montaggio video semplice per presentazioni: timeline con traccia video e
tracce audio, tagli, fermo immagine, avanzamento veloce, sovraimpressioni,
zoom e pixelatura con inseguimento del soggetto; esportazione in mp4 con ffmpeg.

    python EditSimple.py [progetto.json | video]
"""

from __future__ import annotations

import sys


def _fail(message: str) -> int:
    """Segnala un avvio impossibile anche senza console (Avvia.bat usa pythonw; su Linux zenity o xmessage)."""
    if sys.stderr is not None:
        print(message, file=sys.stderr)
    if sys.platform == "win32":
        import ctypes

        ctypes.windll.user32.MessageBoxW(None, message, "EditSimple", 0x10)
    elif message:
        # Linux e altri Unix: finestra con zenity o xmessage, se ci sono (nessuna dipendenza nuova)
        import shutil
        import subprocess

        for command in (
            ["zenity", "--error", "--no-markup", "--title=EditSimple", "--text=" + message],
            ["xmessage", "-center", message],
        ):
            if shutil.which(command[0]) is None:
                continue
            try:
                subprocess.run(command, check=False)
            except OSError:
                continue
            # basta il primo strumento che si e' avviato: chiuso con la X o con Esc non deve
            # ripetere il messaggio con lo strumento successivo
            break
    return 1


def main() -> int:
    try:
        from editsimple.app import run
    except ImportError as exc:  # pragma: no cover - ambiente incompleto
        try:
            from editsimple.i18n import tr
        except ImportError:
            def tr(text: str) -> str:
                return text
        return _fail(
            tr("Impossibile avviare l'interfaccia: {error}\n\n"
               "Installa le dipendenze con:\n"
               "    {command}").format(error=exc, command="python -m pip install -r requirements.txt")
        )
    run(sys.argv[1] if len(sys.argv) > 1 else None)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
