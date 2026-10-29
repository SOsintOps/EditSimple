# EditSimple — montaggio video per presentazioni.  Copyright (C) 2026 Andrea Cumini <andrea@osintinfo.net>
# SPDX-License-Identifier: GPL-3.0-only
# GNU GPL v3 con termini aggiuntivi (attribuzione dell'autore): vedi LICENSE e NOTICE.
"""Esportazione: dalla timeline al grafo di filtri ffmpeg e all'mp4.

La timeline viene divisa in segmenti (una clip, o il pezzo di clip su cui vale
uno zoom); ogni segmento e' un trim della sorgente portato alla misura del
progetto, con pixelatura (crop + scale + overlay con posizione che segue
l'inseguimento) e zoom (crop + scale). I segmenti vengono concatenati, poi
sopra il video finale passano le sovraimpressioni (PNG disegnati da
overlays.py, filtro overlay con enable fra inizio e fine) e l'orologio
dell'avanzamento veloce (sequenza di PNG in ciclo). L'audio originale segue
gli stessi tagli (e la velocita' con atempo); le tracce aggiunte vengono
ritardate e mescolate con amix. Il grafo va in un file (-filter_complex_script)
perche' puo' essere lungo.
"""

from __future__ import annotations

import math
import os
import shutil
import subprocess
import tempfile
import threading
from dataclasses import dataclass, replace
from typing import Callable

from PIL import Image, ImageDraw

from . import media, overlays, procs
from .i18n import tr
from .project import EPS, Project, clip_duration

ProgressCb = Callable[[str, float], None]   # (messaggio, frazione 0..1)

AFMT = "aformat=sample_fmts=fltp:sample_rates=48000:channel_layouts=stereo"
PRESETS = ("ultrafast", "superfast", "veryfast", "faster", "fast", "medium", "slow", "slower")


class RenderError(RuntimeError):
    """Esportazione fallita."""


class Cancelled(Exception):
    """Esportazione interrotta dall'utente."""


@dataclass
class Segment:
    start: float            # timeline
    end: float
    kind: str               # "video" | "freeze"
    source: str
    src_in: float = 0.0
    src_out: float = 0.0
    speed: float = 1.0
    clock: bool = False
    audio: bool = True
    freeze_at: float = 0.0
    slide: dict | None = None
    index: int = 0          # posizione della clip nel progetto
    head: float = 0.0       # secondi in piu' prima dell'inizio (fusione con la clip precedente)
    tail: float = 0.0       # secondi in piu' dopo la fine (fusione con la successiva)
    fade_in: float = 0.0
    fade_out: float = 0.0

    @property
    def duration(self) -> float:
        return self.end - self.start


def build_segments(project: Project) -> list[Segment]:
    """Un segmento per clip (lo zoom e' un riquadro sovrapposto dopo il concat, non spezza le clip)."""
    segments: list[Segment] = []
    t = 0.0
    for index, clip in enumerate(project.clips):
        d = clip_duration(clip)
        if d <= EPS:
            continue
        seg = Segment(start=t, end=t + d, kind=clip["kind"], source=clip["source"], index=index)
        seg.head = project.xfade_after(index - 1) / 2.0
        seg.tail = project.xfade_after(index) / 2.0
        seg.fade_in, seg.fade_out = project.fades(clip)
        if clip["kind"] == "video":
            speed = float(clip.get("speed", 1) or 1)
            seg.speed = speed
            seg.src_in = float(clip["in"])
            seg.src_out = float(clip["out"])
            seg.clock = bool(clip.get("clock")) and abs(speed - 1) > 1e-9
            seg.audio = bool(clip.get("audio", True))
        elif clip["kind"] == "slide":
            seg.slide = clip
        else:
            seg.freeze_at = float(clip["at"])
        segments.append(seg)
        t += d
    return segments


def ff_color(color: str) -> str:
    """Colore per i filtri ffmpeg (0xRRGGBB)."""
    r, g, b = overlays.hex_to_rgb(color)
    return f"0x{r:02X}{g:02X}{b:02X}"


# ----------------------------------------------------------- espressioni

def _num(value: float) -> str:
    text = f"{float(value):.4f}".rstrip("0").rstrip(".")
    return text if text not in ("", "-", "-0") else "0"


def _piecewise(keys: list[tuple[float, float]]) -> str:
    """Interpolazione lineare a tratti di (t, valore) come espressione ffmpeg nella variabile t.

    I tratti si scelgono con if annidati a meta' (albero bilanciato): una somma
    di tratti oltre il centinaio ffmpeg non la accetta piu' ("Missing ')' or too
    many args"), un albero regge migliaia di punti (percorsi lunghi inseguiti).
    """
    keys = sorted(keys)
    if not keys:
        return "0"
    if len(keys) == 1:
        return _num(keys[0][1])
    segments = []
    for (t0, v0), (t1, v1) in zip(keys, keys[1:]):
        if t1 - t0 < 1e-6:
            continue
        segments.append((t0, f"({_num(v0)}+{_num((v1 - v0) / (t1 - t0))}*(t-{_num(t0)}))"))
    if not segments:
        return _num(keys[0][1])

    def tree(lo: int, hi: int) -> str:
        if hi - lo == 1:
            return segments[lo][1]
        mid = (lo + hi) // 2
        return f"if(lt(t,{_num(segments[mid][0])}),{tree(lo, mid)},{tree(mid, hi)})"

    return (f"if(lt(t,{_num(keys[0][0])}),{_num(keys[0][1])},"
            f"if(gte(t,{_num(keys[-1][0])}),{_num(keys[-1][1])},{tree(0, len(segments))}))")


def _scale_spans(fx: dict, t0: float, t1: float, fps: float) -> list[tuple[float, float, float]]:
    """Tratti (inizio, fine, fattore di misura) a misura costante fra t0 e t1 (tempi della timeline).

    Il fattore e' il gradino di SCALE_STEP appena sopra la scala massima del
    tratto, cosi' la pixelatura copre sempre l'oggetto.
    """
    if t1 - t0 <= 1e-6:
        return [(t0, t1, 1.0)]
    step = 1.0 / max(1.0, fps)
    n = max(1, int(math.ceil((t1 - t0) / step)))
    levels = []
    for i in range(n):
        t = min(t1, t0 + (i + 0.5) * step)
        levels.append(overlays.scale_level(overlays.track_state(fx, t)[2]))
    if all(lv == 0 for lv in levels):
        return [(t0, t1, 1.0)]
    spans = []
    start = 0
    for i in range(1, n + 1):
        if i == n or levels[i] != levels[start]:
            spans.append((t0 + start * step, t0 + i * step if i < n else t1, overlays.SCALE_STEP ** levels[start]))
            start = i
    return spans


def _atempo(speed: float) -> str:
    parts = []
    remaining = float(speed)
    while remaining > 2.0 + 1e-9:
        parts.append("atempo=2")
        remaining /= 2.0
    while remaining < 0.5 - 1e-9:          # atempo accetta da 0.5 in su: il rallentatore si fa a passi
        parts.append("atempo=0.5")
        remaining /= 0.5
    if abs(remaining - 1.0) > 1e-6:
        parts.append(f"atempo={_num(remaining)}")
    return ",".join(parts)


def fit_chain(width: int, height: int, fps: float) -> str:
    return (f"scale={width}:{height}:force_original_aspect_ratio=decrease:flags=bicubic,"
            f"pad={width}:{height}:(ow-iw)/2:(oh-ih)/2:color=black,setsar=1,fps={_num(fps)},format=yuv420p")


# ----------------------------------------------------------- esportazione

class Exporter:
    def __init__(self, project: Project, output: str, crf: int = 20, preset: str = "medium",
                 audio_kbps: int = 192, progress: ProgressCb | None = None,
                 cancel: threading.Event | None = None, audio_only: bool = False) -> None:
        self.project = project
        self.audio_only = audio_only      # solo il mix audio, in WAV (per ascoltarlo nell'anteprima)
        self.output = output
        self.crf = int(crf)
        self.preset = preset if preset in PRESETS else "medium"
        self.audio_kbps = int(audio_kbps)
        self.progress = progress
        self.cancel = cancel
        self.inputs: list[list[str]] = []
        self.lines: list[str] = []
        self.command: list[str] = []
        self.script = ""

    # --- grafo

    def _add_input(self, args: list[str]) -> int:
        self.inputs.append(args)
        return len(self.inputs) - 1

    def _segment_input(self, seg: Segment) -> int:
        """Ogni segmento video e' un ingresso a se', con ricerca nel file (-ss) e durata (-t).

        Cosi' ffmpeg decodifica solo la parte che serve, e ogni ingresso viene
        usato da un solo trim: lo stesso stream collegato a piu' trim (anche
        con split) fa fermare questo ffmpeg prima della fine.
        """
        return self._add_input(["-ss", _num(seg.src_in), "-t", _num(seg.src_out - seg.src_in), "-i", seg.source])

    def _report(self, message: str, fraction: float) -> None:
        if self.cancel is not None and self.cancel.is_set():
            raise Cancelled()
        if self.progress is not None:
            self.progress(message, max(0.0, min(1.0, fraction)))

    def build(self, workdir: str) -> None:
        p = self.project
        W, H, fps = p.width, p.height, p.fps
        p.sync_full()
        segments = build_segments(p)
        if not segments:
            raise RenderError(tr("La timeline e' vuota: importa almeno un video."))
        fit = fit_chain(W, H, fps)
        pixelates = [fx for fx in p.shown_effects() if fx["type"] == "pixelate"]
        vlabels: list[str] = []
        for k, seg in enumerate(segments):
            self._report(tr("Preparazione dei segmenti"), 0.02 + 0.08 * k / len(segments))
            src_len = seg.src_out - seg.src_in
            # con una fusione il segmento video si allunga oltre il taglio (head prima, tail dopo): la
            # durata del video non cambia perche' xfade sovrappone proprio quei pezzi
            ext = seg.duration + seg.head + seg.tail
            if seg.kind == "video":
                limit = p.source_duration(seg.source) or (seg.src_out + seg.tail * seg.speed)
                # nella fusione la clip che esce resta ferma per tutta la fusione: il suo video si ferma a
                # meta' fusione prima del taglio e quel fotogramma si ripete (tail prima + tail dopo il taglio);
                # quella che entra comincia un poco prima del suo inizio
                want_in = seg.src_in - seg.head * seg.speed
                stop = seg.src_out - seg.tail * seg.speed
                lo, hi = max(0.0, want_in), min(limit, stop)
                pad_a = (lo - want_in) / seg.speed
                pad_b = 2 * seg.tail + (stop - hi) / seg.speed
                i = self._add_input(["-ss", _num(lo), "-t", _num(hi - lo), "-i", seg.source])
                pts = "PTS-STARTPTS" if abs(seg.speed - 1.0) < 1e-9 else f"(PTS-STARTPTS)/{_num(seg.speed)}"
                pad = ""
                if pad_a > 1e-3 or pad_b > 1e-3:
                    # il sorgente non ha fotogrammi oltre il taglio: si ripete il primo o l'ultimo
                    pad = (f",tpad=start_duration={_num(max(0.0, pad_a))}:stop_duration={_num(max(0.0, pad_b))}"
                           f":start_mode=clone:stop_mode=clone")
                if not self.audio_only:
                    self.lines.append(f"[{i}:v]trim=duration={_num(hi - lo)},setpts={pts},{fit}{pad}[s{k}]")
            elif not self.audio_only:
                png = os.path.join(workdir, f"freeze_{k}.png")
                if seg.slide is not None:
                    overlays.render_slide(seg.slide, W, H).save(png)     # la slide, gia' alla misura giusta
                else:
                    media.grab_png(seg.source, seg.freeze_at, png)
                j = self._add_input(["-loop", "1", "-framerate", _num(fps), "-t", _num(ext), "-i", png])
                self.lines.append(f"[{j}:v]trim=duration={_num(ext)},setpts=PTS-STARTPTS,{fit}[s{k}]")
            cur = f"s{k}"
            span = replace(seg, start=seg.start - seg.head, end=seg.end + seg.tail)
            for n, fx in enumerate(pixelates if not self.audio_only else []):
                if fx["end"] <= span.start + EPS or fx["start"] >= span.end - EPS:
                    continue
                cur = self._pixelate(cur, f"p{k}_{n}", fx, span)
            fades = []
            if seg.fade_in > 1e-3:
                fades.append(f"fade=t=in:st={_num(seg.head)}:d={_num(seg.fade_in)}")
            if seg.fade_out > 1e-3:
                fades.append(f"fade=t=out:st={_num(seg.head + seg.duration - seg.fade_out)}:d={_num(seg.fade_out)}")
            if fades and not self.audio_only:
                self.lines.append(f"[{cur}]{','.join(fades)}[f{k}]")
                cur = f"f{k}"
            if not self.audio_only:
                # stessa base dei tempi per tutti i pezzi: xfade rifiuta ingressi con basi diverse (dopo un
                # concat la base cambia, e una fusione dopo un taglio netto falliva)
                self.lines.append(f"[{cur}]settb=AVTB[t{k}]")
                cur = f"t{k}"
            vlabels.append(cur)
            # audio del segmento (senza allungamenti: nella fusione l'audio cala e risale attorno al taglio)
            info = p.source_info(seg.source)
            afades = []
            clip = p.clips[seg.index]
            a_in = max(seg.fade_in, seg.head, float(clip.get("afade_in") or 0.0))
            a_out = max(seg.fade_out, seg.tail, float(clip.get("afade_out") or 0.0))
            a_in, a_out = min(a_in, seg.duration), min(a_out, max(0.0, seg.duration - min(a_in, seg.duration)))
            if a_in > 1e-3:
                afades.append(f"afade=t=in:st=0:d={_num(a_in)}")
            if a_out > 1e-3:
                afades.append(f"afade=t=out:st={_num(max(0.0, seg.duration - a_out))}:d={_num(a_out)}")
            atail = ("," + ",".join(afades)) if afades else ""
            if seg.kind == "video" and seg.audio and info.get("has_audio") and p.original_volume > 0 and not p.original_muted:
                tempo = ("," + _atempo(seg.speed)) if abs(seg.speed - 1) > 1e-9 else ""
                self.lines.append(f"[{i}:a]atrim=start={_num(seg.src_in - lo)}:duration={_num(src_len)},"
                                  f"asetpts=PTS-STARTPTS{tempo},volume={_num(p.original_volume * float(clip.get('volume', 1.0)))},"
                                  f"{AFMT}{atail}[a{k}]")
            else:
                self.lines.append(f"anullsrc=r=48000:cl=stereo:d={_num(seg.duration)},{AFMT}[a{k}]")
        # video: tagli netti con concat, fusioni con xfade (che comincia meta' fusione prima del taglio)
        cur = vlabels[0]
        for k in range(1, len(segments) if not self.audio_only else 1):
            d = segments[k - 1].tail + segments[k].head
            if d > 1e-3:
                offset = segments[k].start - segments[k].head
                self.lines.append(f"[{cur}][{vlabels[k]}]xfade=transition=fade:duration={_num(d)}:offset={_num(offset)},"
                                  f"settb=AVTB[vx{k}]")
            else:
                self.lines.append(f"[{cur}][{vlabels[k]}]concat=n=2:v=1:a=0,settb=AVTB[vx{k}]")
            cur = f"vx{k}"
        self.lines.append("".join(f"[a{k}]" for k in range(len(segments)))
                          + f"concat=n={len(segments)}:v=0:a=1[acat0]")
        # dissolvenze dell'audio originale all'inizio e alla fine del video
        total = p.duration()
        ofi = max(0.0, min(float(p.original_fade_in or 0.0), total))
        ofo = max(0.0, min(float(p.original_fade_out or 0.0), total - ofi))
        ofades = ""
        if ofi > 1e-3:
            ofades += f",afade=t=in:st=0:d={_num(ofi)}"
        if ofo > 1e-3:
            ofades += f",afade=t=out:st={_num(total - ofo)}:d={_num(ofo)}"
        self.lines.append(f"[acat0]anull{ofades}[acat]")

        # zoom: l'area scelta, ingrandita in un riquadro bordato sopra il video (con il contorno dell'area)
        for n, fx in enumerate(fx for fx in p.shown_effects() if fx["type"] == "zoom" and not self.audio_only):
            x, y, w, h = overlays.zoom_rect(fx, W, H)
            bx, by, bw, bh = overlays.inset_rect(fx, W, H)
            t = overlays.zoom_border(fx)
            color = ff_color(fx.get("color", "#FFFFFF"))
            on = f"enable='between(t,{_num(fx['start'])},{_num(fx['end'])})'"
            keys = fx.get("track") or []
            oval = fx.get("shape") == "oval"
            zr = overlays.zoom_round(fx, bw, bh)
            masked = oval or zr > 0           # contenuto con alfa (ellisse o angoli arrotondati) + anello sopra
            alpha_expr = ("255*lte(pow((X+0.5-W/2)/(W/2),2)+pow((Y+0.5-H/2)/(H/2),2),1)" if oval
                          else overlays.rounded_alpha(max(0, zr - t)))
            # l'area segue l'oggetto (x e y funzioni del tempo, dentro il fotogramma) e ne segue la misura:
            # crop ha misure fisse, quindi a tratti di misura costante, ognuno sui propri fotogrammi
            spans = _scale_spans(fx, fx["start"], fx["end"], p.fps) if keys else [(fx["start"], fx["end"], 1.0)]
            if keys:
                w0, h0 = float(fx["w"]), float(fx["h"])
                base_x, base_y = float(keys[0][1]), float(keys[0][2])
                cxe = _piecewise([(float(k[0]), float(fx["x"]) + float(k[1]) - base_x + w0 / 2) for k in keys])
                cye = _piecewise([(float(k[0]), float(fx["y"]) + float(k[2]) - base_y + h0 / 2) for k in keys])
            outs = "".join(f"[zs{n}_{k}]" for k in range(len(spans)))
            self.lines.append(f"[{cur}]split={len(spans) + 1}[zb{n}]{outs}")
            insets = []
            for k, (ta, tb, factor) in enumerate(spans):
                if keys:
                    _x, _y, w, h = overlays.zoom_rect(dict(fx, w=float(fx["w"]) * factor, h=float(fx["h"]) * factor), W, H)
                    ax = f"'trunc(clip({cxe}-{_num(w / 2)},0,{W - w}))'"
                    ay = f"'trunc(clip({cye}-{_num(h / 2)},0,{H - h}))'"
                else:
                    ax, ay = str(x), str(y)
                head = f"[zs{n}_{k}]" if len(spans) == 1 else f"[zs{n}_{k}]trim=start={_num(ta)}:end={_num(tb)},"
                if masked:
                    # riquadro ovale o arrotondato: contenuto con alfa zero fuori (come le maschere dell'anteprima)
                    self.lines.append(f"{head}crop={w}:{h}:{ax}:{ay}:exact=1,scale={max(2, bw - 2 * t)}:{max(2, bh - 2 * t)}:flags=bicubic,"
                                      f"setsar=1,format=rgba,geq=r='r(X,Y)':g='g(X,Y)':b='b(X,Y)':"
                                      f"a='{alpha_expr}'[zi{n}_{k}]")
                else:
                    self.lines.append(f"{head}crop={w}:{h}:{ax}:{ay}:exact=1,scale={max(2, bw - 2 * t)}:{max(2, bh - 2 * t)}:flags=bicubic,"
                                      f"pad={bw}:{bh}:{t}:{t}:color={color},setsar=1[zi{n}_{k}]")
                insets.append(f"zi{n}_{k}")
            base = f"zb{n}"
            if fx.get("outline", True) or fx.get("link", True):
                # contorno sull'area e linea fino al riquadro: se l'area segue l'oggetto la linea cambia forma
                # a ogni fotogramma, quindi e' una sequenza di PNG (su una tela grande quanto basta) che parte
                # all'inizio dell'effetto; altrimenti un PNG solo
                self._report(tr("Disegno del contorno dello zoom"), 0.12)
                png, (cx0, cy0), frames = self._zoom_decor(fx, workdir, n)
                if frames > 1:
                    j = self._add_input(["-framerate", _num(p.fps), "-i", png])
                    self.lines.append(f"[{j}:v]setpts=PTS-STARTPTS+{_num(fx['start'])}/TB[zl{n}]")
                    self.lines.append(f"[{base}][zl{n}]overlay=x={cx0}:y={cy0}:{on}:eof_action=pass[zd{n}]")
                else:
                    j = self._add_input(["-i", png])
                    self.lines.append(f"[{base}][{j}:v]overlay=x={cx0}:y={cy0}:{on}:eof_action=repeat[zd{n}]")
                base = f"zd{n}"
            ix, iy = (bx + t, by + t) if masked else (bx, by)
            for k, label in enumerate(insets):
                tail = on if len(insets) == 1 else "eof_action=pass"
                self.lines.append(f"[{base}][{label}]overlay=x={ix}:y={iy}:{tail}[zo{n}_{k}]")
                base = f"zo{n}_{k}"
            if masked:
                ring = os.path.join(workdir, f"zring_{n}.png")
                overlays.zoom_ring(fx, bw, bh).save(ring)
                j = self._add_input(["-i", ring])
                self.lines.append(f"[{base}][{j}:v]overlay=x={bx}:y={by}:{on}:eof_action=repeat[zr{n}]")
                base = f"zr{n}"
            cur = base

        # sovraimpressioni: testo, riquadri, ovali, frecce (se seguono un soggetto, x e y sono funzioni di t)
        statics = [fx for fx in p.shown_effects() if fx["type"] in overlays.STATIC_TYPES and not self.audio_only]
        for n, fx in enumerate(statics):
            self._report(tr("Disegno delle sovraimpressioni"), 0.10 + 0.05 * n / max(1, len(statics)))
            if fx["type"] in overlays.SCALED_TYPES and fx.get("track"):
                spans = _scale_spans(fx, fx["start"], fx["end"], p.fps)
                if len(spans) > 1 or spans[0][2] != 1.0:
                    cur = self._scaled_figure(cur, fx, spans, workdir, n)
                    continue
            rendered = overlays.render_effect(fx)
            if rendered is None:
                continue
            image, x, y = rendered
            png = os.path.join(workdir, f"fx_{n}.png")
            image.save(png)
            j = self._add_input(["-i", png])
            keys = fx.get("track") or []
            if keys:
                base_x, base_y = float(keys[0][1]), float(keys[0][2])
                xe = _piecewise([(float(k[0]), x + float(k[1]) - base_x) for k in keys])
                ye = _piecewise([(float(k[0]), y + float(k[2]) - base_y) for k in keys])
                position = f"x='{xe}':y='{ye}':eval=frame"
            else:
                position = f"x={int(x)}:y={int(y)}"
            self.lines.append(f"[{cur}][{j}:v]overlay={position}:"
                              f"enable='between(t,{_num(fx['start'])},{_num(fx['end'])})':eof_action=repeat[o{n}]")
            cur = f"o{n}"

        # tempo trascorso: una immagine per ogni valore (al secondo, o al decimo), in sequenza
        for n, fx in enumerate(fx for fx in p.shown_effects() if fx["type"] in overlays.TIMER_TYPES and not self.audio_only):
            self._report(tr("Disegno del tempo trascorso"), 0.18)
            step = overlays.timer_step(fx)
            first = math.floor(float(fx["start"]) / step + 1e-9) * step
            count = max(1, int(math.ceil((float(fx["end"]) - first) / step - 1e-9)))
            folder = os.path.join(workdir, f"timer_{n}")
            os.makedirs(folder, exist_ok=True)
            for k in range(count):
                image, _x, _y = overlays.render_timer(fx, first + (k + 0.5) * step)
                overlays.with_opacity(image, float(fx.get("opacity", 1.0))).save(
                    os.path.join(folder, f"t_{k:05d}.png"), compress_level=1)
            j = self._add_input(["-framerate", _num(1.0 / step), "-i", os.path.join(folder, "t_%05d.png")])
            self.lines.append(f"[{j}:v]setpts=PTS-STARTPTS+{_num(first)}/TB[tmv{n}]")
            self.lines.append(f"[{cur}][tmv{n}]overlay=x={int(fx['x'])}:y={int(fx['y'])}:"
                              f"enable='between(t,{_num(fx['start'])},{_num(fx['end'])})':eof_action=pass[tm{n}]")
            cur = f"tm{n}"

        # orologio dell'avanzamento veloce: una sequenza di PNG per ogni velocita' usata
        ranges: dict[float, list[tuple[float, float]]] = {}
        for seg in segments:
            if seg.kind == "video" and seg.clock and not self.audio_only:
                ranges.setdefault(round(seg.speed, 4), []).append((seg.start, seg.end))
        for n, (speed, spans) in enumerate(sorted(ranges.items())):
            label = overlays.speed_label(speed)
            self._report(tr("Disegno dell'orologio {speed}").format(speed=label), 0.15 + 0.05 * n / len(ranges))
            folder = os.path.join(workdir, f"clock_{n}")
            os.makedirs(folder, exist_ok=True)
            frames = max(1, int(round(fps * overlays.CLOCK_LOOP)))
            size = int(p.clock.get("size", 160))
            color = p.clock.get("color", "#FFFFFF")
            image = None
            for f in range(frames):
                image = overlays.clock_image(size, f / fps, color, label, float(p.clock.get("bg_alpha", 0.5)),
                                             float(p.clock.get("radius", 18.0)))
                image.save(os.path.join(folder, f"c_{f:05d}.png"))
            x, y = overlays.clock_position(W, H, p.clock, image)
            j = self._add_input(["-loop", "1", "-framerate", _num(fps), "-i", os.path.join(folder, "c_%05d.png")])
            enable = "+".join(f"between(t,{_num(a)},{_num(b)})" for a, b in spans)
            self.lines.append(f"[{cur}][{j}:v]overlay=x={x}:y={y}:enable='{enable}':eof_action=repeat[c{n}]")
            cur = f"c{n}"

        # tracce audio aggiunte
        mix: list[str] = []
        for n, track in enumerate(p.audio_tracks):
            if track.get("muted") or float(track.get("volume", 1.0)) <= 0:
                continue
            if not p.source_info(track["source"]).get("has_audio", True):
                continue
            j = self._add_input(["-i", track["source"]])
            delay = max(0, int(round(float(track["start"]) * 1000)))
            length = max(0.0, float(track["out"]) - float(track["in"]))
            fi = max(0.0, min(float(track.get("fade_in") or 0.0), length))
            fo = max(0.0, min(float(track.get("fade_out") or 0.0), length - fi))
            tfades = ""
            if fi > 1e-3:
                tfades += f",afade=t=in:st=0:d={_num(fi)}"
            if fo > 1e-3:
                tfades += f",afade=t=out:st={_num(length - fo)}:d={_num(fo)}"
            self.lines.append(f"[{j}:a]atrim=start={_num(track['in'])}:end={_num(track['out'])},"
                              f"asetpts=PTS-STARTPTS,volume={_num(track['volume'])},{AFMT}{tfades},"
                              f"adelay=delays={delay}:all=1[t{n}]")
            mix.append(f"t{n}")
        if mix:
            self.lines.append("[acat]" + "".join(f"[{m}]" for m in mix)
                              + f"amix=inputs={len(mix) + 1}:duration=first:dropout_transition=0:normalize=0[aout]")
            alabel = "aout"
        else:
            alabel = "acat"

        self.script = ";\n".join(self.lines) + "\n"
        script_path = os.path.join(workdir, "filters.txt")
        with open(script_path, "w", encoding="utf-8") as fh:
            fh.write(self.script)
        total = p.duration()
        cmd = [media.ffmpeg_exe(), "-hide_banner", "-nostdin", "-y", "-loglevel", "error",
               "-progress", "pipe:1", "-nostats"]
        for args in self.inputs:
            cmd += args
        # il grafo sta in un file: con ffmpeg >= 7 si carica con "-/filter_complex file",
        # con i precedenti con "-filter_complex_script file" (tolto in ffmpeg 8)
        tail = ["-map", f"[{cur}]", "-map", f"[{alabel}]",
                "-c:v", "libx264", "-preset", self.preset, "-crf", str(self.crf), "-pix_fmt", "yuv420p",
                "-r", _num(fps), "-c:a", "aac", "-b:a", f"{self.audio_kbps}k", "-ar", "48000",
                "-movflags", "+faststart", "-t", _num(total), self.output]
        if self.audio_only:
            tail = ["-map", f"[{alabel}]", "-c:a", "pcm_s16le", "-ar", "48000", "-ac", "2",
                    "-t", _num(total), "-f", "wav", self.output]
        self.command = cmd + ["-/filter_complex", script_path] + tail
        self.command_legacy = cmd + ["-filter_complex_script", script_path] + tail

    def _scaled_figure(self, cur: str, fx: dict, spans: list, workdir: str, n: int) -> str:
        """Riquadro o ovale che segue un oggetto e ne segue la misura: un PNG per tratto di misura costante,
        centrato sul percorso dell'inseguimento."""
        keys = fx["track"]
        w0, h0 = float(fx["w"]), float(fx["h"])
        base_x, base_y = float(keys[0][1]), float(keys[0][2])
        cxs = [(float(k[0]), float(fx["x"]) + float(k[1]) - base_x + w0 / 2) for k in keys]
        cys = [(float(k[0]), float(fx["y"]) + float(k[2]) - base_y + h0 / 2) for k in keys]
        for k, (ta, tb, factor) in enumerate(spans):
            w, h = w0 * factor, h0 * factor
            image, ox, oy = overlays.render_effect(dict(fx, x=0, y=0, w=w, h=h, track=[]))
            png = os.path.join(workdir, f"fx_{n}_{k}.png")
            image.save(png)
            j = self._add_input(["-i", png])
            # come in anteprima: angolo = int(centro - misura/2) piu' il margine del disegno
            xe = f"trunc({_piecewise(cxs)}-{_num(w / 2)})+{ox}"
            ye = f"trunc({_piecewise(cys)}-{_num(h / 2)})+{oy}"
            self.lines.append(f"[{cur}][{j}:v]overlay=x='{xe}':y='{ye}':eval=frame:"
                              f"enable='between(t,{_num(ta)},{_num(tb)})':eof_action=repeat[o{n}_{k}]")
            cur = f"o{n}_{k}"
        return cur

    def _zoom_decor(self, fx: dict, workdir: str, n: int) -> tuple[str, tuple[int, int], int]:
        """PNG (o sequenza di PNG) con contorno dell'area e linea verso il riquadro; restituisce il percorso
        da dare a ffmpeg, l'angolo della tela nel fotogramma e il numero di fotogrammi."""
        p = self.project
        W, H = p.width, p.height
        inset = overlays.inset_rect(fx, W, H)
        lw = overlays.zoom_line_width(fx)
        if fx.get("track"):
            count = max(1, int(math.ceil((fx["end"] - fx["start"]) * p.fps)) + 1)
            times = [fx["start"] + i / p.fps for i in range(count)]
        else:
            times = [fx["start"]]
        areas = [overlays.zoom_rect(overlays.displaced(fx, t), W, H) for t in times]
        # tela: unione delle aree nel tempo e del riquadro (la linea sta fra i due), dentro il fotogramma
        x0 = max(0, min([a[0] for a in areas] + [inset[0]]) - lw)
        y0 = max(0, min([a[1] for a in areas] + [inset[1]]) - lw)
        x1 = min(W, max([a[0] + a[2] for a in areas] + [inset[0] + inset[2]]) + lw)
        y1 = min(H, max([a[1] + a[3] for a in areas] + [inset[1] + inset[3]]) + lw)
        folder = os.path.join(workdir, f"zoom_{n}")
        os.makedirs(folder, exist_ok=True)
        for i, area in enumerate(areas):
            canvas = Image.new("RGBA", (max(1, x1 - x0), max(1, y1 - y0)), (0, 0, 0, 0))
            overlays.draw_zoom_decor(ImageDraw.Draw(canvas), fx, area, inset, (x0, y0))
            canvas.save(os.path.join(folder, f"z_{i:05d}.png"), compress_level=1)
        if len(areas) == 1:
            return os.path.join(folder, "z_00000.png"), (x0, y0), 1
        return os.path.join(folder, "z_%05d.png"), (x0, y0), len(areas)

    def _pixelate(self, cur: str, tag: str, fx: dict, seg: Segment) -> str:
        """Riquadro pixelato che segue l'inseguimento, nel tempo locale del segmento.

        Se l'oggetto si avvicina o si allontana il riquadro cambia misura; crop
        e scale di ffmpeg hanno pero' misure fisse, quindi l'intervallo si divide
        in tratti a misura costante (a gradini di SCALE_STEP, sempre un poco piu'
        grandi dell'oggetto): ogni tratto lavora solo sui propri fotogrammi.
        """
        W, H = self.project.width, self.project.height
        w0, h0 = float(fx["w"]), float(fx["h"])
        block = max(2, int(fx.get("block", 16)))
        keys = fx.get("track") or [[fx["start"], fx.get("x", 0), fx.get("y", 0)]]
        # posizione del centro (le chiavi sono il riquadro di partenza centrato sull'oggetto)
        cxs = [(float(k[0]) - seg.start, float(k[1]) + w0 / 2) for k in keys]
        cys = [(float(k[0]) - seg.start, float(k[2]) + h0 / 2) for k in keys]
        a = max(0.0, fx["start"] - seg.start)
        b = min(seg.duration, fx["end"] - seg.start)
        spans = _scale_spans(fx, seg.start + a, seg.start + b, self.project.fps)
        shape = ""
        if fx.get("shape") == "oval":
            # maschera ellittica: alfa pieno dentro l'ellisse inscritta nel riquadro, zero fuori
            shape = (",format=rgba,geq=r='r(X,Y)':g='g(X,Y)':b='b(X,Y)':"
                     "a='255*lte(pow((X+0.5-W/2)/(W/2),2)+pow((Y+0.5-H/2)/(H/2),2),1)'")
        round_pct = 0.0 if fx.get("shape") == "oval" else float(fx.get("radius", 0) or 0)
        outs = "".join(f"[{tag}s{n}]" for n in range(len(spans)))
        self.lines.append(f"[{cur}]split={len(spans) + 1}[{tag}b]{outs}")
        base = f"{tag}b"
        for n, (ta, tb, factor) in enumerate(spans):
            w = max(4, min(int(round(w0 * factor)), W))
            h = max(4, min(int(round(h0 * factor)), H))
            # il riquadro puo' sporgere dal fotogramma (il soggetto sta uscendo): si ritaglia da una copia
            # con un margine nero e si sovrappone a coordinate anche negative, che overlay ritaglia da se'
            xe = f"clip({_piecewise(cxs)}-{_num(w / 2)},{-w},{W})"
            ye = f"clip({_piecewise(cys)}-{_num(h / 2)},{-h},{H})"
            small_w, small_h = max(1, math.ceil(w / block)), max(1, math.ceil(h / block))
            if round_pct > 0:
                # angoli arrotondati: alfa zero fuori (stessa formula di overlays.rounded_mask)
                shape = (",format=rgba,geq=r='r(X,Y)':g='g(X,Y)':b='b(X,Y)':"
                         f"a='{overlays.rounded_alpha(overlays.round_px(w, h, round_pct))}'")
            la, lb = ta - seg.start, tb - seg.start
            if len(spans) == 1:
                head = f"[{tag}s{n}]"
                enable = f"enable='between(t,{_num(la)},{_num(lb)})'"
            else:
                # solo i fotogrammi del tratto (trim tiene i tempi: overlay li rimette al loro posto)
                head = f"[{tag}s{n}]trim=start={_num(la)}:end={_num(lb)},"
                enable = "eof_action=pass"
            self.lines.append(f"{head}pad={W + 2 * w}:{H + 2 * h}:{w}:{h}:color=black,"
                              f"crop={w}:{h}:'({xe})+{w}':'({ye})+{h}':exact=1,"
                              f"scale={small_w}:{small_h}:flags=area,scale={w}:{h}:flags=neighbor{shape}[{tag}p{n}]")
            self.lines.append(f"[{base}][{tag}p{n}]overlay=x='{xe}':y='{ye}':eval=frame:{enable}[{tag}o{n}]")
            base = f"{tag}o{n}"
        return base

    # --- esecuzione

    def run(self) -> str:
        workdir = tempfile.mkdtemp(prefix="editsimple-")
        try:
            self._report(tr("Preparazione"), 0.0)
            self.build(workdir)
            self._run_ffmpeg()
            self._report(tr("Completato"), 1.0)
            return self.output
        finally:
            shutil.rmtree(workdir, ignore_errors=True)

    def _run_ffmpeg(self) -> None:
        try:
            self._run_command(self.command)
        except RenderError as exc:
            if "Unrecognized option '/filter_complex'" not in str(exc):
                raise
            self._run_command(self.command_legacy)   # ffmpeg piu' vecchio di 7

    def _run_command(self, command: list[str]) -> None:
        total = max(self.project.duration(), 0.001)
        proc = procs.popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        errors: list[bytes] = []
        reader = threading.Thread(target=lambda: errors.append(proc.stderr.read()), daemon=True)
        reader.start()
        try:
            assert proc.stdout is not None
            for raw in proc.stdout:
                if self.cancel is not None and self.cancel.is_set():
                    proc.kill()
                    raise Cancelled()
                line = raw.decode("utf-8", "replace").strip()
                if line.startswith("out_time_us=") or line.startswith("out_time_ms="):
                    try:
                        done = int(line.split("=", 1)[1]) / 1_000_000.0
                    except ValueError:
                        continue
                    fraction = 0.2 + 0.8 * min(1.0, done / total)
                    self._report(tr("Codifica: {done} / {total}").format(
                        done=media.format_time(done, ms=False), total=media.format_time(total, ms=False)), fraction)
            proc.wait()
        finally:
            if proc.poll() is None:
                proc.kill()
            proc.wait()
            reader.join(timeout=3)
        if proc.returncode != 0:
            message = b"".join(errors).decode("utf-8", "replace").strip()
            raise RenderError(message[-3000:] or tr("ffmpeg: codice di uscita {code}").format(code=proc.returncode))
        if not os.path.isfile(self.output) or os.path.getsize(self.output) == 0:
            raise RenderError(tr("ffmpeg non ha scritto il file di uscita."))
