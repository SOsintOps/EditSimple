# EditSimple — montaggio video per presentazioni.  Copyright (C) 2026 Andrea Cumini <andrea@osintinfo.net>
# SPDX-License-Identifier: GPL-3.0-only
# GNU GPL v3 con termini aggiuntivi (attribuzione dell'autore): vedi LICENSE e NOTICE.
"""Riproduzione dell'audio nell'anteprima, con il lettore audio di Windows (winmm, nessuna libreria in piu').

L'audio da sentire e' il mix del progetto preparato da ffmpeg con lo stesso
grafo dell'esportazione (render.Exporter in modalita' solo audio), tenuto in
memoria come campioni a 16 bit. Si riproduce da qualunque istante passando a
waveOut la parte di memoria che serve, senza scrivere file; la posizione di
riproduzione fa da orologio all'anteprima, cosi' video e audio restano allineati.
Su Linux e macOS i campioni vengono passati in un flusso a un lettore del sistema
(pw-cat, paplay, aplay o ffplay, il primo che c'e'), e l'orologio e' quello del
processo; se non c'e' nessun lettore l'anteprima resta muta.
"""

from __future__ import annotations

import ctypes
import shutil
import subprocess
import sys
import threading
import time
import wave

import numpy as np

from .i18n import tr

RATE = 48000
CHANNELS = 2

if sys.platform == "win32":
    from ctypes import wintypes

    _winmm = ctypes.WinDLL("winmm")

    class _WAVEFORMATEX(ctypes.Structure):
        _fields_ = [("wFormatTag", wintypes.WORD), ("nChannels", wintypes.WORD),
                    ("nSamplesPerSec", wintypes.DWORD), ("nAvgBytesPerSec", wintypes.DWORD),
                    ("nBlockAlign", wintypes.WORD), ("wBitsPerSample", wintypes.WORD), ("cbSize", wintypes.WORD)]

    class _WAVEHDR(ctypes.Structure):
        _fields_ = [("lpData", ctypes.c_void_p), ("dwBufferLength", wintypes.DWORD),
                    ("dwBytesRecorded", wintypes.DWORD), ("dwUser", ctypes.c_size_t), ("dwFlags", wintypes.DWORD),
                    ("dwLoops", wintypes.DWORD), ("lpNext", ctypes.c_void_p), ("reserved", ctypes.c_size_t)]

    class _MMTIME(ctypes.Structure):
        _fields_ = [("wType", ctypes.c_uint), ("u", ctypes.c_uint32 * 2)]

    _WAVE_MAPPER = 0xFFFFFFFF
    _TIME_SAMPLES = 0x0002
    _winmm.waveOutOpen.argtypes = [ctypes.POINTER(ctypes.c_void_p), ctypes.c_uint, ctypes.POINTER(_WAVEFORMATEX),
                                   ctypes.c_size_t, ctypes.c_size_t, wintypes.DWORD]
    _winmm.waveOutPrepareHeader.argtypes = [ctypes.c_void_p, ctypes.POINTER(_WAVEHDR), ctypes.c_uint]
    _winmm.waveOutUnprepareHeader.argtypes = [ctypes.c_void_p, ctypes.POINTER(_WAVEHDR), ctypes.c_uint]
    _winmm.waveOutWrite.argtypes = [ctypes.c_void_p, ctypes.POINTER(_WAVEHDR), ctypes.c_uint]
    _winmm.waveOutReset.argtypes = [ctypes.c_void_p]
    _winmm.waveOutClose.argtypes = [ctypes.c_void_p]
    _winmm.waveOutGetPosition.argtypes = [ctypes.c_void_p, ctypes.POINTER(_MMTIME), ctypes.c_uint]


# lettori a riga di comando che leggono campioni grezzi (s16le, 48 kHz, stereo) dallo standard input
_PLAYERS: tuple[list[str], ...] = (
    ["pw-cat", "--playback", "--raw", "--format=s16", "--rate=48000", "--channels=2", "-"],
    ["paplay", "--raw", "--format=s16le", "--rate=48000", "--channels=2"],
    ["aplay", "-q", "-t", "raw", "-f", "S16_LE", "-r", "48000", "-c", "2", "-"],
    ["ffplay", "-nodisp", "-autoexit", "-loglevel", "quiet", "-f", "s16le", "-ar", "48000", "-ac", "2", "-i", "-"],
)
_player: list[str] | None = None


def _usable(cmd: list[str]) -> bool:
    """Il lettore c'e' e, per pw-cat, conosce --raw."""
    if not shutil.which(cmd[0]):
        return False
    if cmd[0] != "pw-cat":
        return True
    # le versioni di pw-cat prima dell'opzione --raw (per esempio quella di Ubuntu 24.04) rispondono
    # "unrecognized option" ed escono subito: senza --raw leggerebbe un contenitore WAV, non campioni
    # grezzi, quindi se l'aiuto non la cita si passa al lettore dopo
    try:
        out = subprocess.run([cmd[0], "--help"], capture_output=True, text=True, timeout=3)
    except (OSError, subprocess.SubprocessError):
        return False
    return "--raw" in (out.stdout or "") + (out.stderr or "")


def _player_command() -> list[str] | None:
    """Il primo lettore utilizzabile (cercato una volta sola)."""
    global _player
    if _player is None:
        _player = next((cmd for cmd in _PLAYERS if _usable(cmd)), [])
    return _player or None


def available() -> bool:
    if sys.platform == "win32":
        return True
    return _player_command() is not None


def load_wav(path: str) -> np.ndarray:
    """Campioni int16 interlacciati (stereo, 48 kHz) di un WAV scritto da ffmpeg."""
    with wave.open(path, "rb") as wf:
        if wf.getnchannels() != CHANNELS or wf.getframerate() != RATE or wf.getsampwidth() != 2:
            raise ValueError(tr("formato audio inatteso"))
        return np.frombuffer(wf.readframes(wf.getnframes()), dtype=np.int16).copy()


class AudioPlayer:
    """Riproduce un mix in memoria da un istante qualsiasi e dice a che punto e' arrivato."""

    def __init__(self) -> None:
        self.samples: np.ndarray | None = None
        self._hwo = None
        self._hdr = None
        self._buffer = None
        self._start = 0.0
        self._proc: subprocess.Popen | None = None      # lettore esterno (Linux, macOS)
        self._writer: threading.Thread | None = None
        self._t0 = 0.0

    @property
    def playing(self) -> bool:
        return self._hwo is not None or self._proc is not None

    def set_samples(self, samples: np.ndarray | None) -> None:
        self.stop()
        self.samples = samples

    def duration(self) -> float:
        return 0.0 if self.samples is None else len(self.samples) / (RATE * CHANNELS)

    def play(self, t: float) -> bool:
        """Parte dall'istante t (secondi della timeline). False se non c'e' nulla da sentire."""
        self.stop()
        if not available() or self.samples is None:
            return False
        first = max(0, int(t * RATE)) * CHANNELS
        if first >= len(self.samples):
            return False
        self._buffer = np.ascontiguousarray(self.samples[first:])
        if sys.platform != "win32":
            return self._play_external(t)
        fmt = _WAVEFORMATEX(1, CHANNELS, RATE, RATE * CHANNELS * 2, CHANNELS * 2, 16, 0)
        hwo = ctypes.c_void_p()
        if _winmm.waveOutOpen(ctypes.byref(hwo), _WAVE_MAPPER, ctypes.byref(fmt), 0, 0, 0) != 0:
            self._buffer = None
            return False
        hdr = _WAVEHDR()
        hdr.lpData = self._buffer.ctypes.data
        hdr.dwBufferLength = self._buffer.nbytes
        _winmm.waveOutPrepareHeader(hwo, ctypes.byref(hdr), ctypes.sizeof(hdr))
        _winmm.waveOutWrite(hwo, ctypes.byref(hdr), ctypes.sizeof(hdr))
        self._hwo, self._hdr, self._start = hwo, hdr, t
        return True

    def _play_external(self, t: float) -> bool:
        """Passa i campioni al lettore del sistema da un thread; il tempo e' contato da qui."""
        command = _player_command()
        if command is None:
            self._buffer = None
            return False
        try:
            proc = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL,
                                    stderr=subprocess.DEVNULL)
        except OSError:
            self._buffer = None
            return False
        data = self._buffer.tobytes()

        def feed() -> None:
            try:
                proc.stdin.write(data)
                proc.stdin.close()
            except (OSError, ValueError):
                pass                                  # fermato prima della fine: il tubo e' chiuso

        self._writer = threading.Thread(target=feed, daemon=True)
        self._writer.start()
        self._proc, self._t0, self._start = proc, time.perf_counter(), t
        return True

    def position(self) -> float | None:
        """Istante della timeline che si sta sentendo (None se non suona)."""
        if self._proc is not None:
            return self._start + (time.perf_counter() - self._t0)
        if self._hwo is None:
            return None
        mm = _MMTIME()
        mm.wType = _TIME_SAMPLES
        if _winmm.waveOutGetPosition(self._hwo, ctypes.byref(mm), ctypes.sizeof(mm)) != 0 or mm.wType != _TIME_SAMPLES:
            return None
        return self._start + mm.u[0] / RATE

    def stop(self) -> None:
        if self._proc is not None:
            proc, self._proc = self._proc, None
            try:
                proc.kill()
            except OSError:
                pass
            try:
                proc.stdin.close()
            except (OSError, ValueError):
                pass
            proc.wait()
            if self._writer is not None:
                self._writer.join(timeout=1)
                self._writer = None
            self._buffer = None
        if self._hwo is None:
            return
        _winmm.waveOutReset(self._hwo)
        _winmm.waveOutUnprepareHeader(self._hwo, ctypes.byref(self._hdr), ctypes.sizeof(self._hdr))
        _winmm.waveOutClose(self._hwo)
        self._hwo = self._hdr = self._buffer = None
