# EditSimple — montaggio video per presentazioni.  Copyright (C) 2026 Andrea Cumini <andrea@osintinfo.net>
# SPDX-License-Identifier: GPL-3.0-only
# GNU GPL v3 con termini aggiuntivi (attribuzione dell'autore): vedi LICENSE e NOTICE.
"""Modello del progetto: timeline di clip video, tracce audio, effetti.

Un progetto e' un file JSON. La timeline e' una sequenza di clip senza buchi:
ogni clip e' un pezzo di un video sorgente (con eventuale velocita') oppure un
fermo immagine. Gli effetti (testo, freccia, riquadro, zoom, pixelatura) e le
tracce audio aggiuntive sono posizionati in secondi della timeline, cioe' del
video finale.
"""

from __future__ import annotations

import copy
import json
import os
import uuid

from .i18n import N_, tr

SPEEDS = (0.25, 0.5, 1, 2, 4, 8, 16, 32)   # sotto 1 = rallentatore


def speed_value(value) -> float | int:
    """Velocita' da testo ("0.5x", "4x") o numero; intera quando lo e' (4 e non 4.0)."""
    if isinstance(value, str):
        value = value.strip().lower().rstrip("x").replace(",", ".")
    v = float(value or 1)
    v = min(32.0, max(0.25, v))
    return int(v) if abs(v - round(v)) < 1e-9 else v


def speed_text(value) -> str:
    """Etichetta della velocita': 0.25x, 0.5x, 2x..."""
    return f"{float(speed_value(value)):g}x"
EFFECT_TYPES = ("text", "box", "oval", "arrow", "zoom", "pixelate")
TRACKABLE = ("box", "oval", "arrow", "zoom", "pixelate")   # effetti che possono seguire un soggetto
MIN_LEN = 0.04          # durata minima di una clip o di un effetto, in secondi
EPS = 1e-6

# Etichette da mostrare con tr(EFFECT_NAMES[...]): il modulo si importa prima che la lingua sia scelta.
EFFECT_NAMES = {
    "text": N_("Testo"),
    "box": N_("Riquadro"),
    "oval": N_("Ovale"),
    "arrow": N_("Freccia"),
    "zoom": N_("Zoom"),
    "pixelate": N_("Pixelatura"),
    "logo": N_("Logo e operatore"),
    "image": N_("Immagine"),
    "timer": N_("Tempo trascorso"),
    "frames": N_("Fotogrammi"),
}

# Nome della slide secondo il ruolo: (da solo, con la prima riga del testo).
_SLIDE_LABELS = {
    "open": (N_("Slide di apertura"), N_("Slide di apertura: {text}")),
    "close": (N_("Slide di chiusura"), N_("Slide di chiusura: {text}")),
    "mid": (N_("Slide"), N_("Slide: {text}")),
}


def new_id() -> str:
    return uuid.uuid4().hex[:10]


def default_inset(fx: dict, width: int, height: int) -> dict:
    """Riquadro ingrandito proposto per uno zoom: nell'angolo piu' lontano dall'area, largo il 42 %."""
    w, h = max(8, int(fx.get("w", width // 3))), max(8, int(fx.get("h", height // 3)))
    bw = int(width * 0.42)
    bh = int(round(bw * h / w))
    if bh > height * 0.6:
        bh = int(height * 0.6)
        bw = int(round(bh * w / h))
    margin = max(12, width // 60)
    cx = fx.get("x", 0) + w / 2
    cy = fx.get("y", 0) + h / 2
    bx = margin if cx > width / 2 else width - bw - margin
    by = margin if cy > height / 2 else height - bh - margin
    return {"bx": int(bx), "by": int(by), "bw": bw, "bh": bh, "color": fx.get("color", "#FFFFFF"),
            "thickness": fx.get("thickness", max(3, height // 270)), "outline": fx.get("outline", True)}


def clip_duration(clip: dict) -> float:
    """Durata della clip sulla timeline (la velocita' accorcia il pezzo)."""
    if clip["kind"] in ("freeze", "slide"):
        return max(0.0, float(clip["duration"]))
    speed = float(clip.get("speed", 1) or 1)
    return max(0.0, (float(clip["out"]) - float(clip["in"])) / speed)


def clip_label(clip: dict) -> str:
    if clip["kind"] == "slide":
        alone, with_text = _SLIDE_LABELS.get(clip.get("role"), _SLIDE_LABELS["open"])
        first = str(clip.get("text") or "").strip().splitlines()
        return tr(with_text).format(text=first[0]) if first else tr(alone)
    name = os.path.splitext(os.path.basename(clip["source"]))[0]
    if clip["kind"] == "freeze":
        return tr("Fermo immagine ({name})").format(name=name)
    speed = float(clip.get("speed", 1) or 1)
    return f"{name}  {speed_text(speed)}" if abs(speed - 1) > 1e-9 else name


class Project:
    VERSION = 1

    def __init__(self) -> None:
        self.path: str | None = None
        self.width = 1920
        self.height = 1080
        self.fps = 25.0
        self.clips: list[dict] = []
        self.audio_tracks: list[dict] = []
        self.effects: list[dict] = []
        self.original_volume = 1.0
        self.original_muted = False      # tutto l'audio originale spento
        self.original_fade_in = 0.0      # dissolvenze dell'audio originale all'inizio e alla fine del video
        self.original_fade_out = 0.0
        self.clock = {"size": 160, "corner": "top-right", "margin": 24, "color": "#FFFFFF", "bg_alpha": 0.5, "radius": 18.0}
        self.sources: dict[str, dict] = {}     # percorso -> informazioni del video (probe)
        self.dirty = False

    # ------------------------------------------------------------ file JSON

    def to_dict(self) -> dict:
        return {
            "version": self.VERSION,
            "width": self.width, "height": self.height, "fps": self.fps,
            "original_volume": self.original_volume,
            "original_muted": self.original_muted,
            "original_fade_in": self.original_fade_in,
            "original_fade_out": self.original_fade_out,
            "clock": dict(self.clock),
            "clips": copy.deepcopy(self.clips),
            "audio_tracks": copy.deepcopy(self.audio_tracks),
            "effects": copy.deepcopy(self.effects),
            "sources": copy.deepcopy(self.sources),
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Project":
        p = cls()
        p.width = int(data.get("width", 1920))
        p.height = int(data.get("height", 1080))
        p.fps = float(data.get("fps", 25))
        p.original_volume = float(data.get("original_volume", 1.0))
        p.original_muted = bool(data.get("original_muted", False))
        p.original_fade_in = float(data.get("original_fade_in", 0.0))
        p.original_fade_out = float(data.get("original_fade_out", 0.0))
        p.clock.update(data.get("clock") or {})
        p.clips = copy.deepcopy(data.get("clips") or [])
        p.audio_tracks = copy.deepcopy(data.get("audio_tracks") or [])
        p.effects = copy.deepcopy(data.get("effects") or [])
        p.sources = copy.deepcopy(data.get("sources") or {})
        for clip in p.clips:
            clip.setdefault("id", new_id())
            if clip["kind"] == "video":
                clip.setdefault("audio", True)
                clip.setdefault("speed", 1)
                clip.setdefault("clock", False)
        for fx in p.effects:
            fx.setdefault("id", new_id())
            if fx.get("type") == "zoom":
                fx.setdefault("link", True)
            if fx.get("type") == "zoom" and "bw" not in fx and "factor" not in fx:
                fx.update(default_inset(fx, p.width, p.height))   # progetti salvati con lo zoom a tutto schermo
        for track in p.audio_tracks:
            track.setdefault("id", new_id())
        return p

    def save(self, path: str | None = None) -> None:
        path = path or self.path
        if not path:
            raise ValueError(tr("Percorso del progetto mancante"))
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(self.to_dict(), fh, ensure_ascii=False, indent=2)
        self.path = path
        self.dirty = False

    @classmethod
    def load(cls, path: str) -> "Project":
        with open(path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
        p = cls.from_dict(data)
        p.path = path
        return p

    def snapshot(self) -> dict:
        return self.to_dict()

    def restore(self, data: dict) -> None:
        other = Project.from_dict(data)
        for name in ("width", "height", "fps", "original_volume", "original_muted", "original_fade_in",
                     "original_fade_out", "clock", "clips",
                     "audio_tracks", "effects", "sources"):
            setattr(self, name, getattr(other, name))
        self.dirty = True

    # ------------------------------------------------------------- sorgenti

    def add_source(self, path: str, info: dict) -> None:
        self.sources[path] = dict(info)

    def source_info(self, path: str) -> dict:
        return self.sources.get(path, {})

    def source_duration(self, path: str) -> float:
        info = self.source_info(path)
        return float(info.get("video_duration") or info.get("duration", 0.0))

    # ------------------------------------------------------------- timeline

    def duration(self) -> float:
        return sum(clip_duration(c) for c in self.clips)

    def starts(self) -> list[float]:
        out, t = [], 0.0
        for clip in self.clips:
            out.append(t)
            t += clip_duration(clip)
        return out

    def clip_start(self, index: int) -> float:
        return sum(clip_duration(c) for c in self.clips[:index])

    def clip_by_id(self, clip_id: str) -> dict | None:
        return next((c for c in self.clips if c["id"] == clip_id), None)

    def clip_index(self, clip_id: str) -> int:
        return next((i for i, c in enumerate(self.clips) if c["id"] == clip_id), -1)

    def locate(self, t: float):
        """(indice, clip, secondi dall'inizio della clip) per l'istante t della timeline.

        Oltre la fine restituisce l'ultima clip al suo ultimo istante; senza
        clip restituisce (None, None, 0).
        """
        if not self.clips:
            return None, None, 0.0
        start = 0.0
        last = len(self.clips) - 1
        for i, clip in enumerate(self.clips):
            d = clip_duration(clip)
            if t < start + d - EPS or i == last:
                local = min(max(0.0, t - start), max(0.0, d - 1.0 / max(self.fps, 1)))
                return i, clip, local
            start += d
        return None, None, 0.0

    @staticmethod
    def source_time(clip: dict, local: float) -> float:
        """Istante del video sorgente che corrisponde a `local` secondi dall'inizio della clip."""
        if clip["kind"] == "freeze":
            return float(clip["at"])
        if clip["kind"] == "slide":
            return 0.0
        return float(clip["in"]) + local * float(clip.get("speed", 1) or 1)

    def split_at(self, t: float) -> int:
        """Taglia la clip che contiene t. Restituisce l'indice della clip che inizia in t."""
        start = 0.0
        for i, clip in enumerate(self.clips):
            d = clip_duration(clip)
            if abs(t - start) <= EPS:
                return i
            if t < start + d - EPS:
                local = t - start
                if local < MIN_LEN:
                    return i
                if d - local < MIN_LEN:
                    return i + 1
                first, second = copy.deepcopy(clip), copy.deepcopy(clip)
                second["id"] = new_id()
                # le dissolvenze di fine (e la fusione con la successiva) restano al secondo pezzo,
                # quelle d'inizio al primo
                for key in ("fade_out", "afade_out", "xfade"):
                    first.pop(key, None)
                for key in ("fade_in", "afade_in"):
                    second.pop(key, None)
                if clip["kind"] in ("freeze", "slide"):
                    first["duration"] = local
                    second["duration"] = d - local
                else:
                    cut = self.source_time(clip, local)
                    first["out"] = cut
                    second["in"] = cut
                self.clips[i:i + 1] = [first, second]
                self.dirty = True
                return i + 1
            start += d
        return len(self.clips)

    def delete_range(self, a: float, b: float) -> None:
        """Elimina la porzione di timeline fra a e b; cio' che segue scorre indietro."""
        a, b = max(0.0, min(a, b)), min(self.duration(), max(a, b))
        if b - a < MIN_LEN:
            return
        ia = self.split_at(a)
        ib = self.split_at(b)
        del self.clips[ia:ib]
        length = b - a

        def remap(t: float) -> float:
            if t < a:
                return t
            if t < b:
                return a
            return t - length

        self._remap_times(remap, drop=(a, b))
        self.dirty = True

    def delete_clip(self, index: int) -> None:
        if 0 <= index < len(self.clips):
            a = self.clip_start(index)
            b = a + clip_duration(self.clips[index])
            self.delete_range(a, b)

    def move_clip(self, index: int, new_index: int) -> None:
        """Sposta la clip in un'altra posizione della sequenza (gli effetti restano dove sono)."""
        if not (0 <= index < len(self.clips)):
            return
        new_index = max(0, min(new_index, len(self.clips) - 1))
        if new_index == index:
            return
        clip = self.clips.pop(index)
        self.clips.insert(new_index, clip)
        self.dirty = True

    def insert_clips(self, t: float, clips: list[dict]) -> None:
        """Inserisce clip all'istante t (spezzando la clip che lo contiene); cio' che segue scorre avanti."""
        t = max(0.0, min(t, self.duration()))
        index = self.split_at(t)
        length = sum(clip_duration(c) for c in clips)
        self.clips[index:index] = clips
        self._remap_times(lambda x: x + length if x >= t - EPS else x)
        self.dirty = True

    def append_clips(self, clips: list[dict]) -> None:
        self.clips.extend(clips)
        self.dirty = True

    def insert_freeze(self, t: float, seconds: float) -> dict | None:
        """Fermo immagine del fotogramma all'istante t, lungo `seconds`, inserito in t."""
        i, clip, local = self.locate(t)
        if clip is None:
            return None
        at = self.source_time(clip, local)
        freeze = {"id": new_id(), "kind": "freeze", "source": clip["source"],
                  "at": at, "duration": float(seconds)}
        self.insert_clips(t, [freeze])
        return freeze

    # ------------------------------------------------------------- transizioni

    def xfade_after(self, index: int) -> float:
        """Durata della fusione fra la clip `index` e la successiva (0 se non c'e').

        La fusione e' centrata sul taglio: meta' prima e meta' dopo, quindi la
        durata del video non cambia; non puo' superare la clip piu' corta.
        """
        if index < 0 or index + 1 >= len(self.clips):
            return 0.0
        d = float(self.clips[index].get("xfade") or 0.0)
        if d <= 0:
            return 0.0
        return min(d, 0.9 * min(clip_duration(self.clips[index]), clip_duration(self.clips[index + 1])))

    @staticmethod
    def fades(clip: dict) -> tuple[float, float]:
        """(dissolvenza dal nero, dissolvenza al nero) della clip, in secondi, entro la sua durata."""
        d = clip_duration(clip)
        fi = max(0.0, min(float(clip.get("fade_in") or 0.0), d))
        fo = max(0.0, min(float(clip.get("fade_out") or 0.0), d - fi))
        return fi, fo

    def insert_slide(self, slide: dict, closing: bool = False, at: float | None = None) -> dict:
        """Slide di apertura (all'inizio), di chiusura (alla fine) o in mezzo (all'istante `at`, spezzando la
        clip che lo contiene); cio' che segue scorre avanti."""
        slide.setdefault("id", new_id())
        role = "close" if closing else ("mid" if at is not None else "open")
        slide.update(kind="slide", source="", role=role)
        if closing:
            self.append_clips([slide])
        else:
            self.insert_clips(0.0 if at is None else at, [slide])
        return slide

    def set_speed(self, a: float, b: float, factor: float, clock: bool) -> None:
        """Velocita' (0.25x..32x) sulle clip video fra a e b; la timeline si accorcia o si allunga."""
        factor = speed_value(factor)
        a, b = max(0.0, min(a, b)), min(self.duration(), max(a, b))
        if b - a < MIN_LEN:
            return
        ia = self.split_at(a)
        ib = self.split_at(b)
        old_len = b - a
        for clip in self.clips[ia:ib]:
            if clip["kind"] == "video":
                clip["speed"] = factor
                clip["clock"] = bool(clock) and factor != 1
        new_len = sum(clip_duration(c) for c in self.clips[ia:ib])
        ratio = new_len / old_len if old_len > 0 else 1.0

        def remap(t: float) -> float:
            if t < a:
                return t
            if t <= b:
                return a + (t - a) * ratio
            return t - (old_len - new_len)

        self._remap_times(remap)
        self.dirty = True

    def resize_freeze(self, clip_id: str, seconds: float) -> None:
        """Nuova durata di un fermo immagine; cio' che segue scorre di conseguenza."""
        index = self.clip_index(clip_id)
        if index < 0 or self.clips[index]["kind"] not in ("freeze", "slide"):
            return
        clip = self.clips[index]
        old = clip_duration(clip)
        end = self.clip_start(index) + old
        clip["duration"] = max(MIN_LEN, float(seconds))
        delta = clip_duration(clip) - old
        if abs(delta) > EPS:
            self._remap_times(lambda t: t + delta if t >= end - EPS else t)
        self.dirty = True

    def set_clip_range(self, clip_id: str, start: float, end: float) -> None:
        """Nuovi punti di inizio e fine (secondi del sorgente) di una clip video."""
        index = self.clip_index(clip_id)
        if index < 0 or self.clips[index]["kind"] != "video":
            return
        clip = self.clips[index]
        limit = self.source_duration(clip["source"]) or float("inf")
        start = max(0.0, min(start, limit))
        end = max(start + MIN_LEN, min(end, limit))
        old = clip_duration(clip)
        clip_end = self.clip_start(index) + old
        clip["in"], clip["out"] = start, end
        delta = clip_duration(clip) - old
        if abs(delta) > EPS:
            self._remap_times(lambda t: t + delta if t >= clip_end - EPS else t)
        self.dirty = True

    def new_video_clip(self, path: str, start: float | None = None, end: float | None = None) -> dict:
        info = self.source_info(path)
        duration = float(info.get("video_duration") or info.get("duration", 0.0))
        return {"id": new_id(), "kind": "video", "source": path,
                "in": float(start or 0.0), "out": float(end if end is not None else duration),
                "audio": bool(info.get("has_audio", True)), "speed": 1, "clock": False}

    # ------------------------------------------------------------- effetti

    def add_effect(self, effect: dict) -> dict:
        effect.setdefault("id", new_id())
        self.effects.append(effect)
        self.dirty = True
        return effect

    def remove_effect(self, effect_id: str) -> None:
        self.effects = [e for e in self.effects if e["id"] != effect_id]
        self.dirty = True

    def effect_by_id(self, effect_id: str) -> dict | None:
        return next((e for e in self.effects if e["id"] == effect_id), None)

    def sync_full(self) -> None:
        """Gli effetti "per tutto il video" (logo dell'operatore) coprono sempre tutta la timeline."""
        total = self.duration()
        for fx in self.effects:
            if fx.get("full"):
                fx["start"], fx["end"] = 0.0, total

    def effects_at(self, t: float, types=None) -> list[dict]:
        return [e for e in self.effects if e["start"] - EPS <= t < e["end"] + EPS
                and (types is None or e["type"] in types) and not e.get("hidden")]

    def shown_effects(self) -> list[dict]:
        """Gli effetti non nascosti con l'occhio della timeline (anteprima ed esportazione)."""
        return [e for e in self.effects if not e.get("hidden")]

    # ------------------------------------------------------------- audio

    def add_audio_track(self, path: str, start: float, info: dict) -> dict:
        track = {"id": new_id(), "name": os.path.splitext(os.path.basename(path))[0],
                 "source": path, "start": float(start), "in": 0.0,
                 "out": float(info.get("duration", 0.0)), "volume": 1.0, "muted": False}
        self.sources[path] = dict(info)
        self.audio_tracks.append(track)
        self.dirty = True
        return track

    def remove_audio_track(self, track_id: str) -> None:
        self.audio_tracks = [t for t in self.audio_tracks if t["id"] != track_id]
        self.dirty = True

    def audio_track_by_id(self, track_id: str) -> dict | None:
        return next((t for t in self.audio_tracks if t["id"] == track_id), None)

    @staticmethod
    def track_duration(track: dict) -> float:
        return max(0.0, float(track["out"]) - float(track["in"]))

    # ------------------------------------------------------------- interno

    def _remap_times(self, remap, drop: tuple[float, float] | None = None) -> None:
        """Applica una trasformazione dei tempi a effetti e tracce audio."""
        kept = []
        for fx in self.effects:
            fx["start"] = remap(float(fx["start"]))
            fx["end"] = remap(float(fx["end"]))
            if fx.get("track"):
                keys = []
                for key in fx.get("track", []):
                    t = float(key[0])
                    if drop is not None and drop[0] <= t < drop[1]:
                        continue
                    keys.append([remap(t), key[1], key[2], *key[3:]])
                fx["track"] = keys
            if fx.get("keys"):
                fx["keys"] = [[remap(float(k[0])), *k[1:]] for k in fx["keys"]
                              if drop is None or not drop[0] <= float(k[0]) < drop[1]]
            if fx["end"] - fx["start"] >= MIN_LEN:
                kept.append(fx)
        self.effects = kept
        for track in self.audio_tracks:
            track["start"] = remap(float(track["start"]))
