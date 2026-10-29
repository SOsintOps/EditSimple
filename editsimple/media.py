# EditSimple — montaggio video per presentazioni.  Copyright (C) 2026 Andrea Cumini <andrea@osintinfo.net>
# SPDX-License-Identifier: GPL-3.0-only
# GNU GPL v3 con termini aggiuntivi (attribuzione dell'autore): vedi LICENSE e NOTICE.
"""Lettura dei video: informazioni (ffmpeg), fotogrammi per l'anteprima (OpenCV), fotogrammi singoli.

ffmpeg sta in tools/ffmpeg/ (vedi tools.py). L'anteprima legge i fotogrammi con
OpenCV, che tiene aperto il file e decodifica in sequenza: scorrere avanti di
un fotogramma costa quasi niente, saltare altrove costa una decodifica dal
keyframe precedente. I fotogrammi letti di recente restano in una piccola cache.
"""

from __future__ import annotations

import os
import queue
import re
import subprocess
import threading
from collections import OrderedDict
from pathlib import Path

import cv2
import numpy as np
from PIL import Image

from . import procs, tools
from .i18n import tr

VIDEO_EXTENSIONS = "*.mp4 *.mov *.mkv *.avi *.webm *.m4v *.mts *.m2ts *.ts *.wmv *.flv *.3gp *.mpg *.mpeg"
AUDIO_EXTENSIONS = "*.mp3 *.wav *.m4a *.aac *.ogg *.flac *.wma *.opus *.mp4 *.mov *.mkv"


class MediaError(RuntimeError):
    """ffmpeg assente o file non leggibile."""


def ffmpeg_exe() -> str:
    path, _source = tools.find()
    if path is None:
        raise MediaError(tr("ffmpeg non trovato: scaricalo dalla pagina Configurazione."))
    return str(path)


def _run(cmd: list[str], check: bool = False) -> subprocess.CompletedProcess:
    result = procs.run(cmd)
    if check and result.returncode != 0:
        raise MediaError(result.stderr.decode("utf-8", "replace").strip()
                         or tr("ffmpeg: codice di uscita {code}").format(code=result.returncode))
    return result


# ------------------------------------------------------------ informazioni

_DURATION = re.compile(r"Duration:\s*(\d+):(\d+):(\d+(?:\.\d+)?)")
_VIDEO = re.compile(r"Stream #\d+:\d+.*?:\s*Video:\s*(.*)")
_AUDIO = re.compile(r"Stream #\d+:\d+.*?:\s*Audio:\s*(.*)")
_SIZE = re.compile(r",\s*(\d{2,5})x(\d{2,5})")
_FPS = re.compile(r"([\d.]+)\s*fps")
_TBR = re.compile(r"([\d.]+)\s*tbr")
_ROTATION = re.compile(r"rotation of (-?[\d.]+) degrees")


def probe(path: str | os.PathLike) -> dict:
    """Durata, frequenza, dimensioni e presenza di audio/video dal rapporto di `ffmpeg -i`."""
    path = Path(path)
    if not path.is_file():
        raise MediaError(tr("File non trovato: {path}").format(path=path))
    result = _run([ffmpeg_exe(), "-hide_banner", "-nostdin", "-i", str(path)])
    text = result.stderr.decode("utf-8", "replace")

    info = {"path": str(path), "duration": 0.0, "fps": 0.0, "width": 0, "height": 0,
            "has_video": False, "has_audio": bool(_AUDIO.search(text)), "rotation": 0, "codec": ""}
    duration_match = _DURATION.search(text)
    if duration_match is None:
        raise MediaError(tr("Durata sconosciuta (file danneggiato o non riconosciuto)."))
    h, m, s = duration_match.groups()
    info["duration"] = int(h) * 3600 + int(m) * 60 + float(s)

    stream = next((m for m in _VIDEO.finditer(text)), None)
    if stream is not None:
        line = stream.group(1)
        # le immagini di copertina degli mp3 compaiono come video "mjpeg": non sono un video
        if "(attached pic)" not in text[stream.start():stream.end() + 200]:
            fields = [f.strip() for f in re.split(r",(?![^(]*\))", line)]
            info["codec"] = re.split(r"[\s(]", fields[0], maxsplit=1)[0] if fields else "?"
            size = _SIZE.search(line)
            fps_match = _FPS.search(line) or _TBR.search(line)
            if size is not None and fps_match is not None:
                width, height = int(size.group(1)), int(size.group(2))
                rotation = 0
                rot = _ROTATION.search(text[stream.end():stream.end() + 600])
                if rot is not None:
                    rotation = int(round(float(rot.group(1)))) % 360
                    if rotation in (90, 270):
                        width, height = height, width
                info.update(width=width, height=height, fps=float(fps_match.group(1)),
                            rotation=rotation, has_video=True)
    if not info["has_video"] and not info["has_audio"]:
        raise MediaError(tr("Il file non contiene ne' video ne' audio riconoscibili."))
    if info["has_video"] and info["has_audio"]:
        # la traccia video puo' finire prima dell'audio: una clip che arriva alla fine del file
        # avrebbe il video piu' corto dell'audio e, nel montaggio, l'ultimo fotogramma resterebbe
        # fermo fino alla fine dell'audio. Si legge quindi la durata vera del video (senza decodificare).
        video_duration = _stream_length(path, "0:v:0")
        if video_duration > 0:
            info["video_duration"] = min(video_duration, info["duration"])
    return info


_TIME = re.compile(r"time=(\d+):(\d+):(\d+(?:\.\d+)?)")


def _stream_length(path: Path, stream: str) -> float:
    """Durata effettiva di uno stream, leggendo i pacchetti senza decodificarli."""
    result = _run([ffmpeg_exe(), "-hide_banner", "-nostdin", "-i", str(path), "-map", stream,
                   "-c", "copy", "-f", "null", "-"])
    text = result.stderr.decode("utf-8", "replace")
    times = _TIME.findall(text)
    if not times:
        return 0.0
    h, m, s = times[-1]
    return int(h) * 3600 + int(m) * 60 + float(s)


# ------------------------------------------------------------ fotogrammi

def grab_png(path: str, t: float, target: str) -> str:
    """Salva in PNG il fotogramma all'istante t (ricerca esatta al fotogramma)."""
    cmd = [ffmpeg_exe(), "-hide_banner", "-loglevel", "error", "-nostdin", "-y",
           "-ss", f"{max(0.0, t):.6f}", "-i", str(path), "-an", "-sn", "-dn", "-map", "0:v:0",
           "-frames:v", "1", "-sws_flags", "accurate_rnd+full_chroma_int", "-f", "image2", target]
    _run(cmd, check=True)
    if not os.path.isfile(target):
        raise MediaError(tr("ffmpeg non ha scritto il fotogramma."))
    return target


class _Cap:
    """Un decoder aperto sul file, con l'indice del fotogramma che il prossimo read() restituisce."""

    AHEAD = 8   # fotogrammi avanti raggiungibili scorrendo invece che con un seek

    def __init__(self, path: str) -> None:
        self.cap = cv2.VideoCapture(path, cv2.CAP_FFMPEG)
        if not self.cap.isOpened():
            raise MediaError(tr("Impossibile aprire il video: {path}").format(path=path))
        self.next_index = 0
        self.lock = threading.Lock()

    def read_locked(self, index: int, fps: float) -> np.ndarray | None:
        """Legge il fotogramma `index`; il chiamante tiene `lock`."""
        if index != self.next_index:
            # lettura sequenziale per pochi fotogrammi avanti: piu' veloce di un seek
            if 0 < index - self.next_index <= self.AHEAD:
                while self.next_index < index:
                    if not self.cap.grab():
                        break
                    self.next_index += 1
            else:
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, index)
                self.next_index = index
        ok, frame = self.cap.read()
        if not ok or frame is None:
            # fine del file o seek fallito: riprova con il tempo
            self.cap.set(cv2.CAP_PROP_POS_MSEC, max(0.0, (index / fps) * 1000.0 - 1.0))
            ok, frame = self.cap.read()
            self.next_index = index + 1 if ok else -1
            return frame if ok else None
        self.next_index = index + 1
        return frame

    def release(self) -> None:
        with self.lock:
            self.cap.release()


def fitted(frame: np.ndarray, fit: tuple[int, int] | None) -> Image.Image:
    """Il fotogramma BGR come immagine PIL RGB, ridotto a stare in `fit` (larghezza, altezza) se dato.

    La riduzione la fa OpenCV (INTER_AREA): su un 4K costa 5 ms contro i 20 di Pillow.
    """
    if fit is not None:
        h, w = frame.shape[:2]
        scale = min(fit[0] / w, fit[1] / h)
        if scale < 1.0:
            size = (max(2, int(round(w * scale))), max(2, int(round(h * scale))))
            frame = cv2.resize(frame, size, interpolation=cv2.INTER_AREA)
    return Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))


class _Source:
    """Un video: fino a due decoder, cosi' uno puo' prepararsi sul prossimo taglio mentre l'altro legge."""

    def __init__(self, path: str) -> None:
        self.path = path
        first = _Cap(path)
        self.caps: list[_Cap] = [first]
        self.main: _Cap = first                  # l'ultimo usato dall'anteprima
        self.fps = float(first.cap.get(cv2.CAP_PROP_FPS) or 0.0) or 25.0
        self.count = int(first.cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0)

    def choose(self, index: int) -> _Cap:
        """Il decoder gia' posizionato su `index` (o poco prima), altrimenti il principale."""
        for cap in self.caps:
            if cap.next_index == index:
                return cap
        for cap in self.caps:
            if 0 < index - cap.next_index <= _Cap.AHEAD:
                return cap
        return self.main

    def spare(self) -> _Cap:
        """Un decoder diverso da quello principale, da usare per prepararsi su un altro punto."""
        for cap in self.caps:
            if cap is not self.main:
                return cap
        cap = _Cap(self.path)
        self.caps.append(cap)
        return cap

    def release(self) -> None:
        for cap in self.caps:
            cap.release()


class Frames:
    """Fotogrammi di uno o piu' video come immagini PIL RGB, con cache e lettura sequenziale.

    `fit` (larghezza, altezza) chiede il fotogramma gia' ridotto a quella
    misura: l'anteprima non ha bisogno del 4K intero. Un thread di servizio
    fa due cose: durante la riproduzione (read_ahead) tiene il decoder
    principale qualche fotogramma avanti al cursore, cosi' il thread
    dell'interfaccia trova i fotogrammi in cache; prefetch() posiziona un
    secondo decoder sul prossimo taglio, cosi' al cambio di clip non c'e' il
    tempo del seek. Nessuno dei due torna mai indietro col decoder: un seek
    all'indietro su un 4K costa centinaia di millisecondi.
    """

    CACHE_MAX = 160        # basta per un blocco della riproduzione all'indietro piu' i fotogrammi vicini
    AHEAD_FRAMES = 10      # quanti fotogrammi oltre il cursore tiene pronti il thread di servizio

    def __init__(self) -> None:
        self._sources: dict[str, _Source] = {}
        self._cache: OrderedDict[tuple, Image.Image] = OrderedDict()
        self._lock = threading.Lock()
        self._cond = threading.Condition(self._lock)
        self._ahead: tuple | None = None          # (percorso, indice del cursore, fit) in riproduzione
        self._seeks: list[tuple] = []             # richieste di prefetch (percorso, indice, fit)
        self._back: tuple | None = None           # blocco da leggere per la riproduzione all'indietro
        self._back_busy: tuple | None = None      # blocco in lettura (percorso, primo, ultimo, fit)
        threading.Thread(target=self._service_loop, name="es-frames", daemon=True).start()

    def _source(self, path: str) -> _Source:
        src = self._sources.get(path)
        if src is None:
            src = _Source(path)
            self._sources[path] = src
        return src

    def frame_index(self, path: str, t: float) -> int:
        src = self._source(path)
        index = int(round(t * src.fps))
        if src.count > 0:
            index = min(index, src.count - 1)
        return max(0, index)

    def _cached(self, key: tuple) -> Image.Image | None:
        image = self._cache.get(key)
        if image is not None:
            self._cache.move_to_end(key)
        return image

    def _store(self, key: tuple, image: Image.Image) -> None:
        self._cache[key] = image
        while len(self._cache) > self.CACHE_MAX:
            self._cache.popitem(last=False)

    def get(self, path: str, t: float, fit: tuple[int, int] | None = None,
            forward_only: bool = False, cached_only: bool = False) -> Image.Image | None:
        """Il fotogramma all'istante t (secondi del video sorgente); None se non leggibile.

        Con `forward_only` (riproduzione) il decoder non torna mai indietro: se
        ha gia' superato il fotogramma chiesto e quello non e' in cache, si
        prende il primo che il decoder puo' dare.
        """
        with self._lock:
            try:
                src = self._source(path)
            except MediaError:
                return None
            index = self.frame_index(path, t)
            key = (path, index, fit)
            image = self._cached(key)
            if image is not None:
                if any(c.next_index == index + 1 for c in src.caps):
                    src.main = src.choose(index + 1)
                return image
            if cached_only:
                return None                   # riproduzione all'indietro: lo legge il thread di servizio
            cap = src.choose(index)
            if forward_only and all(c.next_index > index for c in src.caps):
                cap = min(src.caps, key=lambda c: c.next_index)
                index = cap.next_index
                key = (path, index, fit)
                image = self._cached(key)
                if image is not None:
                    return image
            src.main = cap
        with cap.lock:
            with self._lock:
                image = self._cached(key)   # nel frattempo puo' averlo letto il thread di servizio
            if image is not None:
                return image
            frame = cap.read_locked(index, src.fps)
            if frame is None:
                return None
            # conversione e cache dentro il lucchetto del decoder: se restassero fuori, l'altro thread
            # troverebbe il decoder gia' avanzato e il fotogramma non ancora in cache, e farebbe un seek
            image = fitted(frame, fit)
            with self._lock:
                self._store(key, image)
        return image

    def read_ahead(self, path: str | None, t: float = 0.0, fit: tuple[int, int] | None = None) -> None:
        """Dice al thread di servizio dove sta il cursore: tiene pronti i fotogrammi successivi.

        Con `path` None la lettura anticipata si ferma (fine della riproduzione).
        """
        with self._cond:
            if path is None:
                self._ahead = None
                return
            try:
                index = self.frame_index(path, t)
            except MediaError:
                return
            self._ahead = (path, index, fit)
            self._cond.notify_all()

    def prefetch(self, path: str, t: float, fit: tuple[int, int] | None = None) -> None:
        """Prepara in background il fotogramma all'istante t con un secondo decoder (prossimo taglio)."""
        with self._cond:
            try:
                index = self.frame_index(path, t)
            except MediaError:
                return
            if (path, index, fit) in self._cache or (path, index, fit) in self._seeks:
                return
            self._seeks.append((path, index, fit))
            self._cond.notify_all()

    def read_back(self, path: str, t: float, fit: tuple[int, int] | None, count: int) -> None:
        """Riproduzione all'indietro: fa leggere in background i `count` fotogrammi prima di t.

        Il blocco si legge in avanti con un solo seek (un seek per fotogramma
        all'indietro costerebbe centinaia di millisecondi ciascuno su un 4K).
        """
        with self._cond:
            try:
                index = self.frame_index(path, t)
            except MediaError:
                return
            lo = max(0, index - max(1, count))
            for job in (self._back, self._back_busy):
                if job is not None and job[0] == path and job[3] == fit and job[1] <= lo and index <= job[2]:
                    return                    # gia' chiesto o in lettura
            if all((path, i, fit) in self._cache for i in range(lo, index + 1)):
                return
            if self._back is not None and self._back[0] == path and self._back[1] <= index <= self._back[2]:
                return                        # non sostituire un blocco piu' urgente gia' in coda
            self._back = (path, lo, index, fit)
            self._cond.notify_all()

    def _next_job(self) -> tuple | None:
        """Il prossimo lavoro del thread di servizio, scelto sotto il lucchetto; None se non c'e' niente."""
        if self._seeks:
            return ("seek",) + self._seeks.pop(0)
        if self._back is not None:
            job, self._back = self._back, None
            self._back_busy = job
            return ("back",) + job
        if self._ahead is None:
            return None
        path, index, fit = self._ahead
        src = self._source(path)
        cap = src.main
        nxt = cap.next_index
        if nxt > index + self.AHEAD_FRAMES or nxt < 0:
            return None                       # abbastanza avanti: si aspetta che il cursore avanzi
        target = max(nxt, index)              # mai indietro; se il decoder e' rimasto dietro, lo raggiunge
        if (path, target, fit) in self._cache:
            target = nxt + 1 if nxt >= index else index
            if (path, target, fit) in self._cache or target > index + self.AHEAD_FRAMES:
                return None
        return ("ahead", path, target, fit)

    def _service_loop(self) -> None:
        while True:
            with self._cond:
                job = self._next_job()
                if job is None:
                    self._cond.wait(timeout=0.02)
                    continue
            if job[0] == "back":
                try:
                    self._read_block(*job[1:])
                except Exception:  # noqa: BLE001 - una lettura fallita non deve fermare il thread
                    pass
                with self._cond:
                    self._back_busy = None
                continue
            kind, path, index, fit = job
            try:
                with self._lock:
                    src = self._source(path)
                    cap = src.spare() if kind == "seek" else src.main
                self._read_into_cache(src, cap, index, fit)
            except Exception:  # noqa: BLE001 - una lettura fallita non deve fermare il thread
                pass

    def _read_block(self, path: str, lo: int, hi: int, fit: tuple[int, int] | None) -> None:
        """Legge in avanti i fotogrammi lo..hi con il secondo decoder e li mette in cache."""
        with self._lock:
            src = self._source(path)
            cap = src.spare()
        with cap.lock:
            for index in range(lo, hi + 1):
                key = (path, index, fit)
                frame = cap.read_locked(index, src.fps)
                if frame is None:
                    break
                with self._lock:
                    if key not in self._cache:
                        self._store(key, fitted(frame, fit))

    def _read_into_cache(self, src: _Source, cap: _Cap, index: int, fit: tuple[int, int] | None) -> None:
        key = (src.path, index, fit)
        with cap.lock:
            with self._lock:
                if key in self._cache:
                    return
                if cap.next_index > index and cap is src.main:
                    return                    # il decoder principale non torna mai indietro
            frame = cap.read_locked(index, src.fps)
            if frame is not None:
                image = fitted(frame, fit)
                with self._lock:
                    self._store(key, image)

    def close(self, path: str | None = None) -> None:
        with self._lock:
            paths = [path] if path else list(self._sources)
            for p in paths:
                src = self._sources.pop(p, None)
                if src is not None:
                    src.release()
            self._cache = OrderedDict((k, v) for k, v in self._cache.items() if k[0] not in paths)


# ------------------------------------------------------------------ tempi

def format_time(seconds: float, ms: bool = True) -> str:
    """mm:ss.mmm (con le ore solo se servono)."""
    seconds = max(0.0, seconds)
    total_ms = int(round(seconds * 1000))
    h, rest = divmod(total_ms, 3_600_000)
    m, rest = divmod(rest, 60_000)
    s, milli = divmod(rest, 1000)
    text = f"{m:02d}:{s:02d}"
    if h:
        text = f"{h:d}:{text}"
    if ms:
        text += f".{milli:03d}"
    return text


def parse_time(text: str) -> float | None:
    """Da "1:02:03.456", "62.5" o "62,5" ai secondi; None se illeggibile."""
    text = text.strip().lower().replace(",", ".")
    if not text:
        return None
    parts = text.split(":")
    if len(parts) > 3:
        return None
    try:
        values = [float(p) if p else 0.0 for p in parts]
    except ValueError:
        return None
    seconds = 0.0
    for value in values:
        seconds = seconds * 60 + value
    return max(0.0, seconds)
