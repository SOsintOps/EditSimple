# EditSimple — montaggio video per presentazioni.  Copyright (C) 2026 Andrea Cumini <andrea@osintinfo.net>
# SPDX-License-Identifier: GPL-3.0-only
# GNU GPL v3 con termini aggiuntivi (attribuzione dell'autore): vedi LICENSE e NOTICE.
"""Riproduzione dell'audio nell'anteprima, con il lettore audio di Windows (winmm, nessuna libreria in piu').

L'audio da sentire e' il mix del progetto preparato da ffmpeg con lo stesso
grafo dell'esportazione (render.Exporter in modalita' solo audio), tenuto in
memoria come campioni a 16 bit. Si riproduce da qualunque istante passando a
waveOut la parte di memoria che serve, senza scrivere file; la posizione di
riproduzione fa da orologio all'anteprima, cosi' video e audio restano allineati.
Su sistemi diversi da Windows l'anteprima resta muta.
"""

from __future__ import annotations

import ctypes
import sys
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


def available() -> bool:
    return sys.platform == "win32"


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

    @property
    def playing(self) -> bool:
        return self._hwo is not None

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

    def position(self) -> float | None:
        """Istante della timeline che si sta sentendo (None se non suona)."""
        if self._hwo is None:
            return None
        mm = _MMTIME()
        mm.wType = _TIME_SAMPLES
        if _winmm.waveOutGetPosition(self._hwo, ctypes.byref(mm), ctypes.sizeof(mm)) != 0 or mm.wType != _TIME_SAMPLES:
            return None
        return self._start + mm.u[0] / RATE

    def stop(self) -> None:
        if self._hwo is None:
            return
        _winmm.waveOutReset(self._hwo)
        _winmm.waveOutUnprepareHeader(self._hwo, ctypes.byref(self._hdr), ctypes.sizeof(self._hdr))
        _winmm.waveOutClose(self._hwo)
        self._hwo = self._hdr = self._buffer = None
