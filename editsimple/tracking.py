# EditSimple — montaggio video per presentazioni.  Copyright (C) 2026 Andrea Cumini <andrea@osintinfo.net>
# SPDX-License-Identifier: GPL-3.0-only
# GNU GPL v3 con termini aggiuntivi (attribuzione dell'autore): vedi LICENSE e NOTICE.
"""Inseguimento di un riquadro (volto, oggetto, targa) nei fotogrammi successivi.

Il contenuto del riquadro scelto fa da
modello e viene cercato in ogni fotogramma con la correlazione normalizzata
(cv2.matchTemplate) in una finestra attorno alla posizione prevista; il
modello si aggiorna lentamente, cosi' segue cambi di luce e di scala senza
perdere l'originale, e la posizione prevista tiene conto della velocita'. Si
lavora su fotogrammi in scala di grigi ridotti, per velocita'. Se in tools/vittrack c'e' il
modello VitTrack (rete addestrata di opencv_zoo) si usa quello, che ritrova il soggetto dopo un
ostacolo. Il risultato e'
una lista di punti (tempo sorgente, x, y) in pixel del progetto, poi
semplificata: fra un punto e l'altro si interpola linearmente.
"""

from __future__ import annotations

import math
import threading
from typing import Callable

import cv2
import numpy as np

from .i18n import tr
from .media import MediaError
from .overlays import fit_transform

SEARCH = 0.6          # raggio della finestra di ricerca, in frazione della misura del riquadro
MAX_SIDE = 640        # lato massimo del fotogramma ridotto su cui si cerca
GRACE = 0.4           # secondi di tolleranza senza ritrovare il soggetto prima di dichiararlo perso
MIN_PART = 8          # lato minimo (pixel ridotti) della parte di modello ancora visibile su cui si cerca
EXIT_PART = 1.0 / 3   # frazione del riquadro fuori dal bordo oltre la quale, se si allontana, e' uscito
EXIT_FOLLOW = 1.0     # secondi massimi in cui il riquadro prosegue da solo mentre il soggetto finisce di uscire
SCALE_STEPS = (1.0, 1.02, 1 / 1.02, 1.05, 1 / 1.05)
SCALE_BIAS = 0.99     # una scala diversa da quella prevista deve correlare almeno l'1% meglio
MIN_SCALE, MAX_SCALE = 0.3, 8.0
USE_VIT = True        # usa VitTrack se il modello e' stato scaricato (le prove possono spegnerlo)
VIT_SIDE = 960        # lato massimo del fotogramma ridotto dato a VitTrack
VIT_LOST = 0.3        # punteggio di VitTrack sotto il quale il soggetto e' nascosto o perso
VIT_FOUND = 0.4       # punteggio per ritrovarlo dopo che era nascosto
VIT_TRUST = 0.8       # punteggio del confronto a modello oltre il quale ha ragione lui
VIT_JUMP = 0.35       # salto massimo in un fotogramma (frazione del lato maggiore): oltre, e' un altro soggetto
LEARN = 0.6           # quanto il modello impara dal fotogramma nuovo
OCCLUSION = 1.5       # secondi per cui un soggetto in moto puo' restare nascosto (palo, persona, auto)
MOVING = 0.3          # velocita' (pixel ridotti per fotogramma) oltre la quale il soggetto "si muove"

ProgressCb = Callable[[int, int], None]
TRACE: list | None = None   # per le prove: se e' una lista, ogni fotogramma vi aggiunge (t, punteggio, x, y)


class Cancelled(Exception):
    """Inseguimento interrotto dall'utente."""


class Result:
    """Esito dell'inseguimento."""

    def __init__(self, points: list[list[float]], examined: int, lost: int, lost_at: float | None,
                 reason: str = "", velocity: tuple[float, float] = (0.0, 0.0)) -> None:
        self.points = points        # [[t sorgente, x, y, scala], ...] solo fotogrammi in cui il soggetto c'era;
        #                             x, y = angolo del riquadro di partenza centrato sul soggetto
        self.examined = examined    # fotogrammi esaminati
        self.lost = lost            # fotogrammi senza soggetto (dentro la tolleranza)
        self.lost_at = lost_at      # istante (sorgente) in cui il soggetto e' sparito, None se seguito fino in fondo
        self.reason = reason        # "perso" o "uscito"
        self.velocity = velocity    # velocita' del soggetto all'ultimo avvistamento, pixel progetto al secondo


def track(path: str, t_start: float, t_end: float, box: tuple[float, float, float, float],
          project_size: tuple[int, int], min_score: float = 0.45,
          progress: ProgressCb | None = None, cancel: threading.Event | None = None) -> Result:
    """Segue `box` (x, y, w, h in pixel del progetto) da t_start a t_end del video sorgente.

    Il confronto a modello fa il lavoro; con il modello VitTrack scaricato in
    tools/vittrack, VitTrack gli lavora accanto e lo corregge quando non e'
    sicuro (soggetto dietro un palo, modello agganciato allo sfondo).
    """
    model = vit_model() if USE_VIT else None
    return _track_template(path, t_start, t_end, box, project_size, min_score, progress, cancel, model)


def vit_model():
    from . import tools
    return tools.vit_model()


def _track_template(path: str, t_start: float, t_end: float, box: tuple[float, float, float, float],
                    project_size: tuple[int, int], min_score: float = 0.45,
                    progress: ProgressCb | None = None, cancel: threading.Event | None = None,
                    vit=None) -> Result:
    """Inseguimento con il confronto a modello (cv2.matchTemplate), con VitTrack (`vit`) come aiuto: segue `box` da t_start a t_end.

    Mentre il soggetto esce dal bordo si cerca solo la parte del modello
    ancora dentro al fotogramma, cosi' il riquadro continua a seguirlo invece
    di restare incollato al bordo. Si ferma quando il soggetto non si trova
    piu' per GRACE secondi (perso) o quando il riquadro e' per meta' fuori
    dal fotogramma, o per piu' di un terzo e in allontanamento (uscito): i
    punti arrivano fino a quel fotogramma, e la velocita' restituita serve a
    far scivolare la figura fuori del tutto.
    """
    cap = cv2.VideoCapture(path, cv2.CAP_FFMPEG)
    if not cap.isOpened():
        raise MediaError(tr("Impossibile aprire il video: {path}").format(path=path))
    try:
        fps = float(cap.get(cv2.CAP_PROP_FPS) or 0.0) or 25.0
        src_w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) or 0)
        src_h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) or 0)
        first = max(0, int(round(t_start * fps)))
        last = max(first, int(round(t_end * fps)))
        cap.set(cv2.CAP_PROP_POS_FRAMES, first)
        ok, frame = cap.read()
        if not ok or frame is None:
            raise MediaError(tr("Nessun fotogramma all'istante di partenza."))
        if src_w <= 0 or src_h <= 0:
            src_h, src_w = frame.shape[:2]
        # dal progetto ai pixel della sorgente, poi alla scala ridotta di lavoro
        fit, ox, oy = fit_transform(src_w, src_h, *project_size)
        work = min(1.0, MAX_SIDE / max(src_w, src_h))
        bx, by, bw, bh = box
        x = (bx - ox) / fit * work
        y = (by - oy) / fit * work
        tw = max(6, int(round(bw / fit * work)))
        th = max(6, int(round(bh / fit * work)))

        def small_gray(image: np.ndarray) -> np.ndarray:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            if work < 1.0:
                gray = cv2.resize(gray, None, fx=work, fy=work, interpolation=cv2.INTER_AREA)
            return gray

        gray = small_gray(frame)
        gh, gw = gray.shape
        tw, th = min(tw, gw), min(th, gh)
        rx = int(min(max(0, round(x)), gw - tw))
        ry = int(min(max(0, round(y)), gh - th))
        # modello alla misura di partenza; la scala attuale lo ingrandisce o lo riduce (oggetto che si
        # avvicina o si allontana)
        base = gray[ry:ry + th, rx:rx + tw].astype(np.float32)
        anchor = base.copy()              # il modello originale: non cambia, tiene ferma la misura
        tw0, th0 = tw, th
        scale = 1.0
        ds = 0.0                          # variazione di scala per fotogramma (logaritmica), prevista

        def to_project(px: float, py: float) -> tuple[float, float]:
            return (px / work * fit + ox, py / work * fit + oy)

        def key(t: float, cx: float, cy: float, sc: float) -> list[float]:
            # la chiave e' il riquadro di partenza centrato sul soggetto, piu' la scala
            qx, qy = to_project(cx, cy)
            return [t, qx - bw / 2.0, qy - bh / 2.0, sc]

        pcx, pcy = rx + tw / 2.0, ry + th / 2.0      # centro del riquadro, pixel ridotti
        points: list[list[float]] = [key(first / fps, pcx, pcy, 1.0)]
        vx = vy = 0.0
        lost = 0
        missing = 0                      # fotogrammi consecutivi senza soggetto
        grace = max(2, int(round(GRACE * fps)))
        hidden = 0                       # fotogrammi di fila passati dietro a un ostacolo
        hidden_max = max(grace, int(round(OCCLUSION * fps)))
        helper = None
        if vit is not None:
            try:
                helper = _VitHelper(vit, fit, ox, oy, src_w, src_h)
                qx, qy = to_project(pcx, pcy)
                helper.init(frame, qx, qy, bw, bh)
            except cv2.error:
                helper = None
        last_good = len(points) - 1      # indice in `points` dell'ultimo fotogramma con il soggetto
        lost_at: float | None = None
        reason = ""
        total = last - first + 1
        index = first
        max_scale = min(gw / tw0, gh / th0, MAX_SCALE)
        min_scale = max(MIN_PART / min(tw0, th0), MIN_SCALE)
        while index < last:
            if cancel is not None and cancel.is_set():
                raise Cancelled()
            ok, frame = cap.read()
            if not ok or frame is None:
                break
            index += 1
            gray = small_gray(frame)
            ccx, ccy = pcx + vx, pcy + vy
            moving = math.hypot(vx, vy) >= MOVING
            predicted = min(max(scale * math.exp(ds), min_scale), max_scale)
            score, best = 0.0, None
            # a cavallo del bordo la misura non si stima (l'oggetto e' tagliato): resta quella prevista
            pw, ph = tw0 * predicted, th0 * predicted
            inside = 0 <= ccx - pw / 2 and ccx + pw / 2 <= gw and 0 <= ccy - ph / 2 and ccy + ph / 2 <= gh
            if not inside:
                predicted = scale              # niente crescita a occhi chiusi
            for step in (SCALE_STEPS if inside else (1.0,)):
                sc = min(max(predicted * step, min_scale), max_scale)
                tw, th = max(MIN_PART, int(round(tw0 * sc))), max(MIN_PART, int(round(th0 * sc)))
                interp = cv2.INTER_AREA if sc < 1 else cv2.INTER_LINEAR
                template = base if (tw, th) == (tw0, th0) else cv2.resize(base, (tw, th), interpolation=interp)

                # dietro a un ostacolo si cerca solo attorno a dove il soggetto dovrebbe essere arrivato
                radius = int(round(max(tw, th) * (HIDDEN_SEARCH if hidden else SEARCH))) + 4
                cx0, cy0 = ccx - tw / 2.0, ccy - th / 2.0
                # Posizioni candidate attorno a quella prevista; il riquadro puo' sporgere dal bordo
                # fino a meta'. Per ogni candidata si confronta solo la parte del modello che li' sta
                # dentro al fotogramma: il modello non contiene mai il bordo e non puo' restarci
                # incollato, e il soggetto si trova anche se accelera verso il bordo.
                min_rows, min_cols = max(MIN_PART, th // 2), max(MIN_PART, tw // 2)
                y_lo, y_hi = max(min_rows - th, int(round(cy0)) - radius), min(gh - min_rows, int(round(cy0)) + radius)
                x_lo, x_hi = max(min_cols - tw, int(round(cx0)) - radius), min(gw - min_cols, int(round(cx0)) + radius)
                # cambiare misura costa un poco: senza prove chiare la scala resta quella prevista
                bias = 1.0 if step == 1.0 else SCALE_BIAS
                here, here_score = None, -2.0
                for ya, yb, r0, r1 in _groups(y_lo, y_hi, th, gh):
                    for xa, xb, c0, c1 in _groups(x_lo, x_hi, tw, gw):
                        part = template[r0:r1, c0:c1]
                        if part.shape[0] < MIN_PART or part.shape[1] < MIN_PART or float(part.std()) <= 1e-3:
                            continue
                        window = gray[ya + r0:yb + r1, xa + c0:xb + c1].astype(np.float32)
                        result = cv2.matchTemplate(window, part, cv2.TM_CCOEFF_NORMED)
                        result = np.nan_to_num(result, nan=-1.0, posinf=-1.0, neginf=-1.0)
                        _lo, hi_score, _lo_loc, loc = cv2.minMaxLoc(result)
                        if hi_score > here_score:
                            here_score, here = hi_score, (xa + loc[0], ya + loc[1], r0, r1, c0, c1, sc, tw, th)
                if here is None:
                    continue
                # le scale si confrontano alla stessa misura: la zona trovata riportata alla misura del
                # modello (un modello piu' piccolo correla meglio solo perche' contiene meno sfondo)
                # il modello aggiornato da solo si porta dietro gli errori di misura: conta anche l'originale
                fair = (0.5 * _fair_score(gray, base, here) + 0.5 * _fair_score(gray, anchor, here)
                        if here[2:6] == (0, th, 0, tw) else here_score)
                if best is None or fair * bias > score:
                    score, best = fair * bias, here
            found = best is not None and score >= min_score
            follow = None                # centro dato da VitTrack, quando e' lui ad avere ragione
            if helper is not None:
                seen = helper.update(frame)
                cur_w = best[7] if found else tw0 * scale
                cur_h = best[8] if found else th0 * scale
                tcx = best[0] + best[7] / 2.0 if found else None
                tcy = best[1] + best[8] / 2.0 if found else None
                sure = found and score >= VIT_TRUST
                if seen is not None:
                    vs, qx, qy = seen
                    vcx, vcy = (qx - ox) / fit * work, (qy - oy) / fit * work
                    far = tcx is None or math.hypot(vcx - tcx, vcy - tcy) > 0.5 * min(cur_w, cur_h)
                    if sure and far:
                        # il modello e' sicuro: VitTrack si e' perso dietro a un altro, si rimette sul soggetto
                        rx_, ry_ = to_project(tcx, tcy)
                        helper.init(frame, rx_, ry_, bw * scale, bh * scale)
                    elif not sure and far and vs >= VIT_FOUND:
                        # il modello non e' sicuro (o non trova) e VitTrack vede il soggetto altrove
                        follow = (vcx, vcy)
                elif sure and helper.gap > 2:
                    rx_, ry_ = to_project(tcx, tcy)
                    helper.init(frame, rx_, ry_, bw * scale, bh * scale)
            if TRACE is not None:
                TRACE.append((index / fps, round(score, 3), best[0] if best else None, best[1] if best else None))
            if follow is not None:
                # VitTrack ha ragione: il riquadro va li' e il modello riparte da li' (mescolato con
                # l'originale, cosi' dimentica lo sfondo che aveva imparato)
                tw, th = max(MIN_PART, int(round(tw0 * scale))), max(MIN_PART, int(round(th0 * scale)))
                ncx, ncy = follow
                vx, vy = 0.5 * vx + 0.5 * (ncx - pcx), 0.5 * vy + 0.5 * (ncy - pcy)
                pcx, pcy = ncx, ncy
                x0_, y0_ = int(round(pcx - tw / 2.0)), int(round(pcy - th / 2.0))
                if 0 <= x0_ and 0 <= y0_ and x0_ + tw <= gw and y0_ + th <= gh:
                    current = gray[y0_:y0_ + th, x0_:x0_ + tw].astype(np.float32)
                    if (tw, th) != (tw0, th0):
                        current = cv2.resize(current, (tw0, th0), interpolation=cv2.INTER_AREA)
                    base = 0.5 * current + 0.5 * anchor
                found = True
                hidden = 0
                missing = 0
            elif found:
                fx_, fy_, r0, r1, c0, c1, sc, tw, th = best
                ncx, ncy = fx_ + tw / 2.0, fy_ + th / 2.0
                vx, vy = 0.5 * vx + 0.5 * (ncx - pcx), 0.5 * vy + 0.5 * (ncy - pcy)
                ds = 0.5 * ds + 0.5 * math.log(sc / scale)
                pcx, pcy, scale = ncx, ncy, sc
                hidden = 0
                if (r0, r1, c0, c1) == (0, th, 0, tw):
                    # il modello impara solo quando il soggetto e' tutto dentro (riportato alla misura base)
                    current = gray[fy_:fy_ + th, fx_:fx_ + tw].astype(np.float32)
                    if current.shape == (th, tw):
                        if (tw, th) != (tw0, th0):
                            current = cv2.resize(current, (tw0, th0), interpolation=cv2.INTER_AREA)
                        base = LEARN * current + (1 - LEARN) * base
                missing = 0
            else:
                # non trovato: si prosegue sulla posizione prevista per un po'; se non ricompare,
                # il soggetto e' perso e l'inseguimento finisce
                tw, th = max(MIN_PART, int(round(tw0 * scale))), max(MIN_PART, int(round(th0 * scale)))
                pcx = float(min(max(-tw / 2.0, ccx), gw + tw / 2.0))
                pcy = float(min(max(-th / 2.0, ccy), gh + th / 2.0))
                if moving and (hidden or missing == 0):
                    # dietro a un ostacolo il soggetto prosegue con la sua velocita'
                    hidden += 1
                else:
                    vx *= 0.9
                    vy *= 0.9
                ds *= 0.5
                lost += 1
                missing += 1
            points.append(key(index / fps, pcx, pcy, scale))
            if found:
                last_good = len(points) - 1
            # uscito: il centro del riquadro e' fuori, oppure il riquadro e' fuori per piu' di un terzo
            # e si sta muovendo verso l'esterno (la parte visibile, sempre piu' piccola, finirebbe per
            # agganciarsi allo sfondo fermo)
            px, py = pcx - tw / 2.0, pcy - th / 2.0
            out_left, out_right = -px / tw, (px + tw - gw) / tw
            out_top, out_bottom = -py / th, (py + th - gh) / th
            outside = max(out_left, out_right, out_top, out_bottom)
            moving_out = ((out_left >= EXIT_PART and vx < -0.5) or (out_right >= EXIT_PART and vx > 0.5)
                          or (out_top >= EXIT_PART and vy < -0.5) or (out_bottom >= EXIT_PART and vy > 0.5))
            if outside >= 0.5 or moving_out:
                # il soggetto e' ancora in parte dentro: il riquadro prosegue con la sua velocita' finche'
                # non e' tutto fuori (una pixelatura che finisse qui lascerebbe scoperta la parte visibile)
                step_n = 0
                while step_n < EXIT_FOLLOW * fps and index + step_n < last:
                    px, py = pcx - tw / 2.0, pcy - th / 2.0
                    if px + tw <= 0 or px >= gw or py + th <= 0 or py >= gh or math.hypot(vx, vy) < MOVING:
                        break
                    step_n += 1
                    pcx, pcy = pcx + vx, pcy + vy
                    points.append(key((index + step_n) / fps, pcx, pcy, scale))
                last_good = len(points) - 1
                lost_at, reason = points[last_good][0], "uscito"
                break
            if missing >= (hidden_max if hidden else grace):
                lost_at, reason = points[last_good][0], "perso"
                break
            if progress is not None and (index - first) % 5 == 0:
                progress(index - first + 1, total)
        examined = len(points)
        if lost_at is not None:
            points = points[:last_good + 1]
        velocity = (vx / work * fit * fps, vy / work * fit * fps)
        return Result(simplify(points, size=max(bw, bh)), examined, lost, lost_at, reason, velocity)
    finally:
        cap.release()


class _VitHelper:
    """VitTrack accanto al confronto a modello: dice dov'e' il soggetto quando il modello non e' sicuro.

    Lavora in coordinate del progetto. Il riquadro di VitTrack ha una forma sua:
    se ne usa il centro, corretto dello scarto che aveva all'inizio. Un salto
    troppo grande da un fotogramma all'altro e' un altro soggetto (un passante)
    e viene ignorato.
    """

    def __init__(self, model, fit: float, ox: float, oy: float, src_w: int, src_h: int) -> None:
        self.params = cv2.TrackerVit_Params()
        self.params.net = str(model)
        self.fit, self.ox, self.oy = fit, ox, oy
        self.k = min(1.0, VIT_SIDE / max(src_w, src_h))
        self.tracker = None
        self.start = (0.0, 0.0)
        self.offset: tuple[float, float] | None = None
        self.prev: tuple[float, float] | None = None
        self.gap = 0
        self.size = 1.0

    def _image(self, frame: np.ndarray) -> np.ndarray:
        if self.k >= 1.0:
            return frame
        return cv2.resize(frame, None, fx=self.k, fy=self.k, interpolation=cv2.INTER_AREA)

    def init(self, frame: np.ndarray, cx: float, cy: float, w: float, h: float) -> None:
        image = self._image(frame)
        gh, gw = image.shape[:2]
        sw = max(4.0, min(w / self.fit * self.k, gw - 2))
        sh = max(4.0, min(h / self.fit * self.k, gh - 2))
        x0 = min(max(0.0, (cx - self.ox) / self.fit * self.k - sw / 2), gw - sw)
        y0 = min(max(0.0, (cy - self.oy) / self.fit * self.k - sh / 2), gh - sh)
        # OpenCV 5 avvisa in console che il nuovo motore dnn ignora la scelta del dispositivo: e' innocuo
        level = cv2.utils.logging.getLogLevel()
        cv2.utils.logging.setLogLevel(cv2.utils.logging.LOG_LEVEL_ERROR)
        try:
            self.tracker = cv2.TrackerVit_create(self.params)
        finally:
            cv2.utils.logging.setLogLevel(level)
        self.tracker.init(image, (int(x0), int(y0), int(sw), int(sh)))
        self.start, self.offset, self.prev, self.gap = (cx, cy), None, (cx, cy), 0
        self.size = max(w, h)

    def update(self, frame: np.ndarray) -> tuple[float, float, float] | None:
        """(punteggio, x, y del centro) nel progetto, o None se perso o saltato su un altro soggetto."""
        if self.tracker is None:
            return None
        ok, bb = self.tracker.update(self._image(frame))
        score = float(self.tracker.getTrackingScore()) if ok else 0.0
        if not ok or bb[2] <= 2 or bb[3] <= 2 or score < VIT_LOST:
            self.gap += 1
            return None
        cx = (bb[0] + bb[2] / 2.0) / self.k * self.fit + self.ox
        cy = (bb[1] + bb[3] / 2.0) / self.k * self.fit + self.oy
        if self.offset is None:
            self.offset = (self.start[0] - cx, self.start[1] - cy)
        cx, cy = cx + self.offset[0], cy + self.offset[1]
        if self.prev is not None:
            limit = VIT_JUMP * self.size * (1.0 + 0.5 * self.gap)
            if math.hypot(cx - self.prev[0], cy - self.prev[1]) > limit:
                self.gap += 1
                return None
        self.prev, self.gap = (cx, cy), 0
        return score, cx, cy


HIDDEN_SEARCH = 0.25   # raggio di ricerca (in frazione del riquadro) mentre il soggetto e' nascosto
def _fair_score(gray: np.ndarray, base: np.ndarray, hit: tuple) -> float:
    """Correlazione fra il modello e la zona trovata riportata alla misura del modello."""
    x, y, _r0, _r1, _c0, _c1, _sc, tw, th = hit
    patch = gray[y:y + th, x:x + tw].astype(np.float32)
    if patch.shape != (th, tw):
        return -1.0
    bh, bw = base.shape
    if (tw, th) != (bw, bh):
        patch = cv2.resize(patch, (bw, bh), interpolation=cv2.INTER_AREA if tw > bw else cv2.INTER_LINEAR)
    value = float(cv2.matchTemplate(patch, base, cv2.TM_CCOEFF_NORMED)[0, 0])
    return value if math.isfinite(value) else -1.0


def _groups(lo: int, hi: int, size: int, limit: int) -> list[tuple[int, int, int, int]]:
    """Raggruppa le posizioni candidate lo..hi (compresi) di un lato del modello lungo `size` in un
    fotogramma lungo `limit`, per parte di modello visibile: [(prima, ultima, da, a)].

    Le posizioni con il modello tutto dentro stanno in un gruppo solo (una
    ricerca sola, il caso normale). Quelle a cavallo del bordo vanno a
    gruppetti di posizioni vicine (un dodicesimo del lato), confrontando la
    parte di modello visibile in tutte: una ricerca per pixel costava migliaia
    di confronti a fotogramma vicino a un angolo.
    """
    chunk = max(1, size // 12)
    out = []
    p = lo
    while p <= hi:
        a, b = max(0, -p), min(size, limit - p)
        if a == 0 and b == size:
            q = min(hi, limit - size)
            out.append((p, q, 0, size))
            p = q + 1
            continue
        q = min(hi, p + chunk - 1, -1) if p < 0 else min(hi, p + chunk - 1)
        a, b = max(0, -p), min(size, limit - q)
        if b > a:
            out.append((p, q, a, b))
        p = q + 1
    return out


def simplify(points: list[list[float]], tolerance: float = 1.5, size: float = 0.0) -> list[list[float]]:
    """Riduce i punti tenendo solo quelli necessari a restare entro `tolerance` pixel (Douglas-Peucker).

    I punti possono avere la scala (quarto valore): conta come lo spostamento
    del bordo di un riquadro lungo `size`.
    """
    points = [list(p) + [1.0] * (4 - len(p)) for p in points]
    if len(points) <= 2:
        return [list(p) for p in points]
    keep = [False] * len(points)
    keep[0] = keep[-1] = True
    stack = [(0, len(points) - 1)]
    while stack:
        a, b = stack.pop()
        if b - a < 2:
            continue
        ta, xa, ya, sa = points[a]
        tb, xb, yb, sb = points[b]
        span = tb - ta or 1e-9
        worst, worst_err = -1, tolerance
        for i in range(a + 1, b):
            t, x, y, sc = points[i]
            k = (t - ta) / span
            err = max(abs(x - (xa + (xb - xa) * k)), abs(y - (ya + (yb - ya) * k)),
                      abs(sc - (sa + (sb - sa) * k)) * size / 2.0)
            if err > worst_err:
                worst, worst_err = i, err
        if worst >= 0:
            keep[worst] = True
            stack.append((a, worst))
            stack.append((worst, b))
    return [[p[0], round(p[1], 1), round(p[2], 1), round(p[3], 4)] for p, k in zip(points, keep) if k]
