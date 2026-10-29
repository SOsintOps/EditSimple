# EditSimple — montaggio video per presentazioni.  Copyright (C) 2026 Andrea Cumini <andrea@osintinfo.net>
# SPDX-License-Identifier: GPL-3.0-only
# GNU GPL v3 con termini aggiuntivi (attribuzione dell'autore): vedi LICENSE e NOTICE.
"""Timeline: righello, traccia video, audio originale, tracce audio aggiunte e corsie degli effetti.

Due Canvas affiancati: a sinistra le etichette delle tracce (fisse), a
destra le tracce, che scorrono in orizzontale e si ingrandiscono con
Ctrl+rotellina. Le clip si trascinano per riordinarle, gli effetti e le tracce
audio per spostarli (il bordo destro degli effetti cambia la durata); un clic
sul righello o su uno spazio vuoto sposta il cursore. Le miniature delle clip
arrivano da un thread in background.
"""

from __future__ import annotations

import math
import threading
import tkinter as tk
from collections import OrderedDict
from tkinter import font as tkfont
from typing import Callable

import customtkinter as ctk
import cv2
from PIL import Image, ImageTk

from . import media, theme
from .i18n import tr, upper
from .project import EFFECT_NAMES, Project, clip_duration, clip_label

LABEL_W = 140
RULER_H = 26
BAND_H = 18          # fascia con il nome della clip, sopra la pellicola
STRIP_H = 64         # altezza delle miniature della pellicola
VIDEO_H = BAND_H + STRIP_H + 6
AUDIO_H = 30
FX_H = 24
ROW_GAP = 4
PAD_LEFT = 12
PAD_RIGHT = 160
MIN_PPS = 1.0
MAX_PPS = 3000.0
TICK_STEPS = (0.04, 0.1, 0.2, 0.5, 1, 2, 5, 10, 15, 30, 60, 120, 300, 600, 1800)
MAX_LANES = 64         # oltre, gli effetti si sovrappongono (le corsie scorrono in verticale)
EDGE = 7


class Thumbs:
    """Miniature della pellicola, decodificate in background con OpenCV.

    `want()` sostituisce ogni volta l'elenco delle miniature desiderate: i
    thread servono prima quelle vicine al cursore e lasciano perdere quelle
    uscite di scena. I fotogrammi vicini si leggono in sequenza da un solo
    seek. Le chiavi sono (percorso, indice del fotogramma sorgente).
    """

    WORKERS = 2
    CACHE_MAX = 2500
    PHOTO_MAX = 700
    RUN_GAP = 4       # fotogrammi non richiesti tollerati dentro un lotto sequenziale
    RUN_MAX = 48      # fotogrammi per lotto

    def __init__(self, height: int) -> None:
        self.height = height
        self._cond = threading.Condition()
        self._wanted: dict[tuple[str, int], None] = {}
        self._pending: set[tuple[str, int]] = set()
        self._images: OrderedDict[tuple[str, int], Image.Image] = OrderedDict()
        self._photos: OrderedDict[tuple, ImageTk.PhotoImage] = OrderedDict()
        self._failed: set[tuple[str, int]] = set()
        self._center: tuple[str, int] = ("", 0)
        self._generation = 0
        self._fresh = False
        self._paused = False
        for index in range(self.WORKERS):
            threading.Thread(target=self._loop, name=f"es-thumb-{index}", daemon=True).start()

    def pause(self, paused: bool) -> None:
        """In riproduzione le miniature aspettano: decodificare 4K in parallelo toglie fiato all'anteprima."""
        with self._cond:
            self._paused = paused
            self._cond.notify_all()

    def get(self, key: tuple[str, int], crop: int | None = None) -> ImageTk.PhotoImage | None:
        """La miniatura come PhotoImage (creata qui, nel thread dell'interfaccia); None se non ancora pronta."""
        with self._cond:
            image = self._images.get(key)
            if image is None:
                return None
            self._images.move_to_end(key)
        pkey = (key, crop)
        photo = self._photos.get(pkey)
        if photo is None:
            if crop is not None and crop < image.width:
                image = image.crop((0, 0, max(1, crop), image.height))
            photo = ImageTk.PhotoImage(image)
            self._photos[pkey] = photo
            while len(self._photos) > self.PHOTO_MAX:
                self._photos.popitem(last=False)
        else:
            self._photos.move_to_end(pkey)
        return photo

    def want(self, keys: list[tuple[str, int]], center: tuple[str, int]) -> None:
        with self._cond:
            self._wanted = {k: None for k in keys
                            if k not in self._images and k not in self._failed and k not in self._pending}
            self._center = center
            self._cond.notify_all()

    def poll(self) -> bool:
        """True se dall'ultima chiamata sono arrivate miniature nuove."""
        with self._cond:
            fresh, self._fresh = self._fresh, False
        return fresh

    def clear(self) -> None:
        with self._cond:
            self._wanted.clear()
            self._pending.clear()
            self._images.clear()
            self._photos.clear()
            self._failed.clear()
            self._generation += 1

    def _pick(self) -> list[tuple[str, int]]:
        """Il lotto da leggere: la chiave piu' vicina al centro e i fotogrammi voluti attorno."""
        path, center = self._center
        same = [k for k in self._wanted if k[0] == path]
        pool = same or list(self._wanted)
        first = min(pool, key=lambda k: abs(k[1] - center) if k[0] == path else 10 ** 9)
        ordered = sorted(k[1] for k in self._wanted if k[0] == first[0])
        lo = hi = ordered.index(first[1])
        while lo > 0 and ordered[lo - 1] >= ordered[lo] - self.RUN_GAP and ordered[hi] - ordered[lo - 1] < self.RUN_MAX:
            lo -= 1
        while hi < len(ordered) - 1 and ordered[hi + 1] <= ordered[hi] + self.RUN_GAP \
                and ordered[hi + 1] - ordered[lo] < self.RUN_MAX:
            hi += 1
        return [(first[0], i) for i in ordered[lo:hi + 1]]

    def _loop(self) -> None:
        caps: dict[str, cv2.VideoCapture] = {}
        while True:
            with self._cond:
                while not self._wanted or self._paused:
                    self._cond.wait()
                run = self._pick()
                generation = self._generation
                for key in run:
                    self._wanted.pop(key, None)
                    self._pending.add(key)
            path = run[0][0]
            results: dict[tuple[str, int], Image.Image] = {}
            try:
                cap = caps.get(path)
                if cap is None or not cap.isOpened():
                    # pochi thread di decodifica: le miniature non devono contendere la CPU all'anteprima
                    cap = caps[path] = cv2.VideoCapture(path, cv2.CAP_FFMPEG, [cv2.CAP_PROP_N_THREADS, 2])
                    if not cap.isOpened():
                        cap = caps[path] = cv2.VideoCapture(path, cv2.CAP_FFMPEG)
                first, last = run[0][1], run[-1][1]
                cap.set(cv2.CAP_PROP_POS_FRAMES, first)
                wanted = {k[1] for k in run}
                for index in range(first, last + 1):
                    if self._paused:
                        break           # e' partita la riproduzione: il resto del lotto puo' aspettare
                    ok, frame = cap.read()
                    if not ok or frame is None:
                        break
                    if index in wanted or index - first <= self.RUN_MAX:
                        h, w = frame.shape[:2]
                        tw = max(8, int(round(w * self.height / h)))
                        small = cv2.resize(frame, (tw, self.height), interpolation=cv2.INTER_AREA)
                        results[(path, index)] = Image.fromarray(cv2.cvtColor(small, cv2.COLOR_BGR2RGB))
            except Exception:  # noqa: BLE001 - le miniature restano vuote
                results = {}
            with self._cond:
                self._pending.difference_update(run)
                if generation != self._generation:
                    continue
                for key in run:
                    if key not in results:
                        if self._paused:
                            self._wanted[key] = None   # interrotta: si riprova a riproduzione finita
                        else:
                            self._failed.add(key)
                for key, image in results.items():
                    self._images[key] = image
                while len(self._images) > self.CACHE_MAX:
                    self._images.popitem(last=False)
                self._fresh = True


class TimelineView(ctk.CTkFrame):
    def __init__(self, master, fonts: theme.Fonts, project: Project,
                 on_seek: Callable[[float], None], on_select: Callable[[str | None, str | None], None],
                 on_changed: Callable[[], None], on_edit_start: Callable[[], None]) -> None:
        super().__init__(master, fg_color=theme.PANEL, corner_radius=4, border_width=1, border_color=theme.BORDER)
        self.fonts = fonts
        self.project = project
        self._on_seek = on_seek
        self._on_select = on_select
        self._on_changed = on_changed
        self._on_edit_start = on_edit_start
        self.pps = 40.0
        self.playhead = 0.0
        self.mark_in: float | None = None
        self.mark_out: float | None = None
        self.selection: tuple[str | None, str | None] = (None, None)
        self._drag: dict | None = None
        self._rows: list[dict] = []
        self._thumbs = Thumbs(STRIP_H)
        self._redraw_job: str | None = None
        self._tk_font = tkfont.Font(family=theme.ui_font(), size=9)
        self._tk_bold = tkfont.Font(family=theme.ui_font(), size=9, weight="bold")
        self._tk_mono = tkfont.Font(family=theme.mono_font(), size=8)

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.labels = tk.Canvas(self, bg=theme.PANEL, highlightthickness=0, bd=0, width=LABEL_W)
        self.labels.grid(row=0, column=0, sticky="ns", padx=(1, 0), pady=(1, 0))
        self.tracks = tk.Canvas(self, bg=theme.BG, highlightthickness=0, bd=0)
        self.tracks.grid(row=0, column=1, sticky="nsew", padx=(0, 1), pady=(1, 0))
        self.scroll = ctk.CTkScrollbar(self, orientation="horizontal", command=self._scrolled, height=12)
        self.scroll.grid(row=1, column=1, sticky="ew", padx=(0, 1), pady=(0, 1))
        self.tracks.configure(xscrollcommand=self.scroll.set)
        # righello e video restano fermi in alto; audio ed effetti scorrono in verticale sotto di loro
        self._vy = 0.0
        self._lower_total = 0.0
        self._reveal: str | None = None     # effetto selezionato da portare in vista (anche dall'anteprima)
        self._sticky_h = RULER_H + ROW_GAP + VIDEO_H + ROW_GAP
        self.vscroll = ctk.CTkScrollbar(self, orientation="vertical", command=self._vscrolled, width=12)
        self.vscroll.grid(row=0, column=2, sticky="ns", padx=(0, 1), pady=(self._sticky_h, 0))

        self.tracks.bind("<Configure>", lambda _e: self.schedule())
        self.tracks.bind("<ButtonPress-1>", self._press)
        self.tracks.bind("<ButtonPress-3>", self._right_press)
        # spostare la vista: Alt+trascina o trascina con il tasto centrale
        for press, motion, release in (("<Alt-ButtonPress-1>", "<Alt-B1-Motion>", "<Alt-ButtonRelease-1>"),
                                       ("<ButtonPress-2>", "<B2-Motion>", "<ButtonRelease-2>")):
            self.tracks.bind(press, self._pan_start)
            self.tracks.bind(motion, self._pan_move)
            self.tracks.bind(release, self._pan_end)
        self._pan: tuple[int, float] | None = None
        self.on_key_delete: Callable[[str, list], None] | None = None
        self.on_fx_menu: Callable[[str, int, int], None] | None = None
        self.on_fx_visibility: Callable[[str], None] | None = None
        self.key_sel: tuple[str | None, set] = (None, set())    # punti del percorso selezionati (effetto, tempi)
        self._key_anchor: str | None = None
        self.tracks.bind("<B1-Motion>", self._motion)
        self.tracks.bind("<ButtonRelease-1>", self._release)
        self.tracks.bind("<Motion>", self._hover)
        self.tracks.bind("<MouseWheel>", self._wheel)
        self.tracks.bind("<Control-MouseWheel>", self._wheel)
        self.tracks.bind("<Shift-MouseWheel>", self._vwheel)
        self.labels.bind("<MouseWheel>", self._vwheel)
        self.labels.bind("<ButtonPress-1>", self._label_press)
        self.after(150, self._poll_thumbs)

    # ------------------------------------------------------------- stato

    def set_project(self, project: Project) -> None:
        self.project = project
        self._thumbs.clear()
        self.zoom_fit()

    def set_playhead(self, t: float) -> None:
        self.playhead = t
        self._draw_playhead()

    def set_playing(self, playing: bool) -> None:
        """Durante la riproduzione le miniature non si decodificano (il decoder dell'anteprima ha la precedenza)."""
        self._thumbs.pause(playing)

    def set_range(self, a: float | None, b: float | None) -> None:
        self.mark_in, self.mark_out = a, b
        self.schedule()

    def set_selection(self, kind: str | None, item_id: str | None) -> None:
        if kind == "effect" and (kind, item_id) != self.selection:
            self._reveal = item_id
        self.selection = (kind, item_id)
        if self.key_sel[0] is not None and (kind != "effect" or item_id != self.key_sel[0]):
            self.key_sel = (None, set())
        self.schedule()

    def schedule(self) -> None:
        if self._redraw_job is None:
            self._redraw_job = self.after(16, self.redraw)

    def _poll_thumbs(self) -> None:
        if self._thumbs.poll():
            self.schedule()
        self.after(150, self._poll_thumbs)

    def _scrolled(self, *args) -> None:
        """Scorrimento orizzontale: le miniature visibili cambiano, quindi si ridisegna."""
        self.tracks.xview(*args)
        self.schedule()

    def _lower_view(self) -> float:
        """Altezza visibile per le righe che scorrono (sotto righello e video)."""
        return max(1.0, float(self.tracks.winfo_height()) - self._sticky_h)

    def _vscrolled(self, *args) -> None:
        """Barra verticale: sposta solo audio ed effetti."""
        total = max(1.0, self._lower_total)
        if args and args[0] == "moveto":
            self._vy = float(args[1]) * total
        elif args and args[0] == "scroll":
            step = self._lower_view() * 0.9 if args[2] == "pages" else FX_H + ROW_GAP
            self._vy += int(args[1]) * step
        self.redraw()

    def _vwheel(self, event) -> str:
        """Rotellina sui nomi delle righe (o Maiusc+rotellina): scorre audio ed effetti in verticale."""
        self._vy += (-1 if event.delta > 0 else 1) * 3 * (FX_H + ROW_GAP)
        self.redraw()
        return "break"

    # ------------------------------------------------------------- misure

    def x(self, t: float) -> float:
        return PAD_LEFT + t * self.pps

    def t(self, x: float) -> float:
        return max(0.0, (x - PAD_LEFT) / self.pps)

    def visible_width(self) -> int:
        return max(50, self.tracks.winfo_width())

    def zoom_fit(self) -> None:
        duration = max(self.project.duration(), 1.0)
        self.pps = max(MIN_PPS, min(MAX_PPS, (self.visible_width() - PAD_LEFT - 40) / duration))
        self.schedule()

    def zoom_by(self, factor: float, around_x: float | None = None) -> None:
        old = self.pps
        # l'istante sotto il mouse si legge PRIMA di cambiare la scala, poi resta li' sotto
        t_at = self.t(self.tracks.canvasx(around_x)) if around_x is not None else None
        self.pps = max(MIN_PPS, min(MAX_PPS, self.pps * factor))
        if t_at is not None and old != self.pps:
            self.redraw()
            new_x = self.x(t_at) - around_x
            total = max(1.0, self._scroll_width())
            self.tracks.xview_moveto(max(0.0, new_x / total))
        else:
            self.schedule()

    def ensure_visible(self, t: float) -> None:
        x = self.x(t)
        left = self.tracks.canvasx(0)
        width = self.visible_width()
        total = max(1.0, self._scroll_width())
        if x < left + 10 or x > left + width - 10:
            self.tracks.xview_moveto(max(0.0, (x - width * 0.3) / total))
            self.schedule()

    def _scroll_width(self) -> float:
        return self.x(self.project.duration()) + PAD_RIGHT

    # ------------------------------------------------------------- righe

    def _layout_rows(self) -> list[dict]:
        rows = [{"kind": "ruler", "y0": 0, "y1": RULER_H, "label": ""}]
        y = RULER_H + ROW_GAP
        rows.append({"kind": "video", "y0": y, "y1": y + VIDEO_H, "label": tr("Video")})
        y += VIDEO_H + ROW_GAP
        top = y
        y -= self._vy
        rows.append({"kind": "audio_orig", "y0": y, "y1": y + AUDIO_H, "label": tr("Audio originale")})
        y += AUDIO_H + ROW_GAP
        for track in self.project.audio_tracks:
            rows.append({"kind": "audio", "id": track["id"], "y0": y, "y1": y + AUDIO_H,
                         "label": track.get("name", tr("Audio"))})
            y += AUDIO_H + ROW_GAP
        lanes: list[float] = []   # fine dell'ultimo effetto in ogni corsia
        placement: dict[str, int] = {}
        for fx in sorted(self.project.effects, key=lambda e: (e["start"], e["end"])):
            lane = next((i for i, end in enumerate(lanes) if fx["start"] >= end - 1e-6), None)
            if lane is None:
                if len(lanes) < MAX_LANES:
                    lanes.append(fx["end"])
                    lane = len(lanes) - 1
                else:
                    lane = min(range(len(lanes)), key=lambda i: lanes[i])
                    lanes[lane] = fx["end"]
            else:
                lanes[lane] = fx["end"]
            placement[fx["id"]] = lane
        n_lanes = max(1, len(lanes))
        for i in range(n_lanes):
            rows.append({"kind": "fx", "lane": i, "y0": y, "y1": y + FX_H, "label": tr("Effetti") if i == 0 else ""})
            y += FX_H + ROW_GAP
        self._placement = placement
        # quanto e' alta la parte che scorre; se lo spostamento e' oltre la fine si rifa' il calcolo
        self._lower_total = y + self._vy - top
        limit = max(0.0, self._lower_total - self._lower_view())
        if self._vy > limit + 0.5 or self._vy < 0:
            self._vy = min(max(0.0, self._vy), limit)
            return self._layout_rows()
        self._height = y
        return rows

    def _row(self, kind: str, item_id: str | None = None, lane: int | None = None) -> dict | None:
        for row in self._rows:
            if row["kind"] != kind:
                continue
            if item_id is not None and row.get("id") != item_id:
                continue
            if lane is not None and row.get("lane") != lane:
                continue
            return row
        return None

    # ------------------------------------------------------------- disegno

    def redraw(self) -> None:
        self._redraw_job = None
        self._rows = self._layout_rows()
        if self._reveal is not None:
            lane = self._placement.get(self._reveal)
            self._reveal = None
            row = self._row("fx", lane=lane) if lane is not None else None
            top, bottom = self._sticky_h, self._sticky_h + self._lower_view()
            if row is not None and (row["y0"] < top or row["y1"] > bottom):
                self._vy += row["y0"] - top if row["y0"] < top else row["y1"] - bottom
                self._rows = self._layout_rows()
        c = self.tracks
        c.delete("all")
        lab = self.labels
        lab.delete("all")
        height = max(1, self.tracks.winfo_height())
        width = max(self._scroll_width(), self.visible_width())
        c.configure(scrollregion=(0, 0, width, height))
        view = self._lower_view()
        if self._lower_total > view + 0.5:
            self.vscroll.set(self._vy / self._lower_total, (self._vy + view) / self._lower_total)
        else:
            self.vscroll.set(0.0, 1.0)

        for row in self._rows:
            if row["kind"] == "ruler":
                continue
            c.create_rectangle(0, row["y0"], width, row["y1"], fill=theme.PANEL, outline="")
            if row["kind"] in ("audio", "audio_orig"):
                # il nome della riga seleziona tutta la traccia (cancellarla, dissolvenze, volume)
                chosen = (row["kind"] == "audio_orig" and self.selection[0] == "oaudio_all") or \
                    (row["kind"] == "audio" and self.selection == ("audio", row.get("id")))
                lab.create_rectangle(2, row["y0"] + 2, LABEL_W - 4, row["y1"] - 2,
                                     fill=theme.ACCENT_BG if chosen else theme.PANEL_2,
                                     outline=theme.ACCENT if chosen else theme.BORDER)
            if row["label"]:
                lab.create_text(12, (row["y0"] + row["y1"]) / 2, text=upper(row["label"]), anchor="w",
                                fill=theme.TEXT if row["kind"] in ("audio", "audio_orig") else theme.TEXT_DIM,
                                font=self._tk_mono, tags=("top",) if row["kind"] == "video" else ())
            if row["kind"] == "audio":
                track = self.project.audio_track_by_id(row["id"])
                if track is not None:
                    vol = int(round(float(track.get("volume", 1.0)) * 100))
                    text = upper(tr("muto")) if track.get("muted") else f"{vol} %"
                    lab.create_text(LABEL_W - 8, (row["y0"] + row["y1"]) / 2, text=text, anchor="e",
                                    fill=theme.TEXT_FAINT, font=self._tk_mono)
            if row["kind"] == "audio_orig":
                vol = int(round(self.project.original_volume * 100))
                lab.create_text(LABEL_W - 8, (row["y0"] + row["y1"]) / 2,
                                text=upper(tr("muto")) if self.project.original_muted else f"{vol} %", anchor="e",
                                fill=theme.TEXT_FAINT, font=self._tk_mono)
        # parte ferma (righello e video) sopra a quella che scorre
        lab.create_rectangle(0, 0, LABEL_W, self._sticky_h - ROW_GAP / 2, fill=theme.PANEL, outline="", tags=("top_bg",))
        lab.tag_raise("top_bg")
        lab.tag_raise("top")
        lab.create_line(LABEL_W - 1, 0, LABEL_W - 1, height, fill=theme.BORDER)

        self._draw_audio_tracks()
        self._draw_effects()
        c.create_rectangle(0, 0, width, self._sticky_h - ROW_GAP / 2, fill=theme.BG, outline="", tags=("top_bg",))
        video = self._row("video")
        c.create_rectangle(0, video["y0"], width, video["y1"], fill=theme.PANEL, outline="", tags=("top_bg",))
        self._draw_ruler(width)
        self._draw_clips()
        c.tag_raise("top_bg")
        c.tag_raise("top")
        if self._sticky_h + ROW_GAP / 2 < height:
            c.create_line(0, self._sticky_h - ROW_GAP / 2, width, self._sticky_h - ROW_GAP / 2, fill=theme.BORDER)
        self._draw_range(height)
        self._draw_playhead()

    def _draw_ruler(self, width: float) -> None:
        c = self.tracks
        top = ("top",)
        c.create_rectangle(0, 0, width, RULER_H, fill=theme.PANEL_2, outline="", tags=top)
        c.create_line(0, RULER_H - 1, width, RULER_H - 1, fill=theme.BORDER, tags=top)
        duration = self.project.duration()
        step = next((s for s in TICK_STEPS if s * self.pps >= 70), TICK_STEPS[-1])
        minor = step / 5 if step / 5 * self.pps >= 6 else None
        # solo la parte visibile (piu' un margine): a zoom alto la timeline e' lunga milioni di pixel e
        # disegnare tutte le tacche rallentava ogni ridisegno; scorrendo si ridisegna comunque
        left = self.tracks.canvasx(0) - 200
        right = self.tracks.canvasx(0) + self.visible_width() + 200
        end = min(max(duration, self.t(width)), self.t(right))
        t = max(0.0, math.floor(self.t(max(0.0, left)) / step) * step)
        while t <= end + 1e-9:
            x = self.x(t)
            c.create_line(x, RULER_H - 10, x, RULER_H, fill=theme.TEXT_DIM, tags=top)
            c.create_text(x + 3, 4, text=media.format_time(t, ms=step < 1), anchor="nw",
                          fill=theme.TEXT_SOFT, font=self._tk_mono, tags=top)
            if minor:
                m = t + minor
                while m < t + step - 1e-9:
                    mx = self.x(m)
                    c.create_line(mx, RULER_H - 5, mx, RULER_H, fill=theme.TEXT_FAINT, tags=top)
                    m += minor
            t += step
        if duration > 0:
            x = self.x(duration)
            c.create_line(x, RULER_H, x, max(self._height, self.tracks.winfo_height()), fill=theme.BORDER_STRONG,
                          dash=(2, 3))

    def _clip_text(self, text: str, max_width: float, font) -> str:
        if font.measure(text) <= max_width:
            return text
        while text and font.measure(text + "...") > max_width:
            text = text[:-1]
        return text + "..." if text else ""

    def _draw_clips(self) -> None:
        c = self.tracks
        row = self._row("video")
        arow = self._row("audio_orig")
        sel_kind, sel_id = self.selection
        view_left = self.tracks.canvasx(0) - 200
        view_right = view_left + self.visible_width() + 400
        wanted: list[tuple[str, int]] = []
        center_key: tuple[str, int] | None = None
        t = 0.0
        for clip in self.project.clips:
            d = clip_duration(clip)
            x0, x1 = self.x(t), self.x(t + d)
            y0, y1 = row["y0"] + 2, row["y1"] - 2
            if clip["kind"] == "slide":
                fill, border = theme.CLIP_SLIDE, theme.CLIP_SLIDE_BORDER
            elif clip["kind"] == "freeze":
                fill, border = theme.CLIP_FREEZE, theme.CLIP_FREEZE_BORDER
            elif abs(float(clip.get("speed", 1) or 1) - 1) > 1e-9:
                fill, border = theme.CLIP_SPEED, theme.CLIP_SPEED_BORDER
            else:
                fill, border = theme.CLIP_VIDEO, theme.CLIP_VIDEO_BORDER
            selected = sel_kind == "clip" and sel_id == clip["id"]
            tags = ("clip", clip["id"], "top")
            c.create_rectangle(x0, y0, x1, y1, fill=fill, outline=theme.TEXT if selected else border,
                               width=2 if selected else 1, tags=tags)
            # pellicola: una miniatura per ogni slot, fino al singolo fotogramma quando si ingrandisce
            if clip["kind"] == "slide":
                # niente pellicola: il colore di sfondo della slide
                c.create_rectangle(x0 + 1, y0 + BAND_H, x1 - 1, y1 - 1, fill=clip.get("bg") or "#000000",
                                   outline="", tags=tags)
                if clip.get("bg_image") and x1 - x0 > 60:
                    c.create_text(x0 + 6, y0 + BAND_H + 10, text=tr("immagine"), anchor="w", fill=theme.TEXT_SOFT,
                                  font=self._tk_mono, tags=tags)
            elif x1 > view_left and x0 < view_right:
                center_key = self._paint_strip(clip, t, d, x0, x1, y0 + BAND_H, view_left, view_right,
                                               wanted, tags) or center_key
            # fascia con il nome, sopra la pellicola
            c.create_rectangle(x0, y0, x1, y0 + BAND_H, fill=fill, outline="", tags=tags)
            label = self._clip_text(clip_label(clip) + "   " + media.format_time(d, ms=False)
                                    + ("   " + tr("orologio") if clip["kind"] == "video" and clip.get("clock") else ""),
                                    max(0, x1 - x0 - 10), self._tk_bold)
            if label:
                c.create_text(x0 + 5, y0 + BAND_H / 2, text=label, anchor="w", fill=theme.TEXT, font=self._tk_bold, tags=tags)
            # audio originale: segue le clip video
            ay0, ay1 = arow["y0"] + 3, arow["y1"] - 3
            if clip["kind"] == "video":
                # l'audio di ogni pezzo si seleziona da solo (volume, dissolvenze, eliminazione)
                atags = ("oaudio", clip["id"])
                asel = sel_kind == "oaudio" and sel_id == clip["id"]
                has_audio = self.project.source_info(clip["source"]).get("has_audio", False)
                on = bool(clip.get("audio", True)) and has_audio and self.project.original_volume > 0
                c.create_rectangle(x0, ay0, x1, ay1, fill=theme.CLIP_AUDIO if on else theme.CLIP_AUDIO_MUTED,
                                   outline=theme.TEXT if asel else (theme.CLIP_AUDIO_BORDER if on else theme.BORDER_STRONG),
                                   width=2 if asel else 1, tags=atags)
                # riga bianca del volume: dissolvenze, transizioni, volume del pezzo e di tutto l'audio originale
                self._envelope(t, t + d, ay0, ay1, self._orig_level(clip, t, d) if on else (lambda _t: 0.0),
                               atags, view_left, view_right)
                if x1 - x0 > 40:
                    vol = float(clip.get("volume", 1.0))
                    if not on:
                        text = tr("senza audio") if not has_audio else tr("muto")
                    elif abs(vol - 1) > 1e-6:
                        text = tr("audio {volume:.0f} %").format(volume=vol * 100)
                    else:
                        text = tr("audio")
                    c.create_text(x0 + 6, (ay0 + ay1) / 2, text=text, anchor="w",
                                  fill=theme.TEXT_SOFT if on else theme.TEXT_FAINT, font=self._tk_mono, tags=atags)
            else:
                c.create_rectangle(x0, ay0, x1, ay1, fill=theme.CLIP_AUDIO_MUTED, outline=theme.BORDER_STRONG,
                                   tags=tags[:2])
            # dissolvenze dal/al nero: una rampa sopra la clip
            fi, fo = Project.fades(clip)
            if fi > 0:
                c.create_line(x0, y1, x0 + fi * self.pps, y0 + BAND_H, fill=theme.TEXT, width=2, tags=tags)
            if fo > 0:
                c.create_line(x1 - fo * self.pps, y0 + BAND_H, x1, y1, fill=theme.TEXT, width=2, tags=tags)
            t += d
        # fusioni: una X a cavallo del taglio
        t = 0.0
        for i, clip in enumerate(self.project.clips):
            t += clip_duration(clip)
            xf = self.project.xfade_after(i)
            if xf > 0:
                xa, xb = self.x(t - xf / 2), self.x(t + xf / 2)
                ya, yb = row["y0"] + 2 + BAND_H, row["y1"] - 2
                c.create_line(xa, ya, xb, yb, fill=theme.ACCENT, width=2, tags=("top",))
                c.create_line(xa, yb, xb, ya, fill=theme.ACCENT, width=2, tags=("top",))
        if self._drag and self._drag.get("mode") == "clip" and self._drag.get("insert_x") is not None:
            ix = self._drag["insert_x"]
            c.create_line(ix, row["y0"], ix, row["y1"], fill=theme.WARN, width=3, tags=("top",))
        if center_key is None and self.project.clips:
            index, clip, local = self.project.locate(self.playhead)
            if clip is not None and clip["kind"] != "slide":
                center_key = self._thumb_key(clip, local)
        self._thumbs.want(wanted, center_key or ("", 0))

    def _thumb_key(self, clip: dict, local: float) -> tuple[str, int]:
        fps = float(self.project.source_info(clip["source"]).get("fps") or self.project.fps or 25.0)
        return clip["source"], max(0, int(round(self.project.source_time(clip, local) * fps)))

    def _paint_strip(self, clip: dict, start: float, d: float, x0: float, x1: float, y0: float,
                     view_left: float, view_right: float, wanted: list, tags: tuple) -> tuple[str, int] | None:
        """Le miniature di una clip, a slot di larghezza fissa; restituisce la chiave sotto il cursore."""
        c = self.tracks
        info = self.project.source_info(clip["source"])
        aspect = (info.get("width") or 16) / max(1, info.get("height") or 9)
        tw = max(10, int(round(STRIP_H * aspect)))
        fps = float(info.get("fps") or self.project.fps or 25.0)
        speed = float(clip.get("speed", 1) or 1)
        slot_dt = tw / self.pps                         # secondi di timeline per slot
        frame_dt = 1.0 / fps / speed                    # secondi di timeline per fotogramma sorgente
        frame_level = slot_dt < frame_dt
        if frame_level:
            slot_dt = frame_dt
        slot_px = slot_dt * self.pps
        y1 = y0 + STRIP_H
        center = None
        k0 = max(0, int(math.floor((view_left - x0) / slot_px)))
        k1 = int(math.ceil((min(x1, view_right) - x0) / slot_px))
        for k in range(k0, k1 + 1):
            sx0 = x0 + k * slot_px
            if sx0 >= x1 - 1:
                break
            sx1 = min(sx0 + slot_px, x1)
            local = k * slot_dt
            if clip["kind"] == "freeze":
                key = self._thumb_key(clip, 0.0)
            else:
                src_t = self.project.source_time(clip, local)
                key = (clip["source"], max(0, int(math.floor(src_t * fps + 1e-6))))
            if center is None and sx0 <= self.x(self.playhead) < sx1:
                center = key
            width = int(sx1 - sx0)
            if width <= 0:
                continue
            photo = self._thumbs.get(key, crop=width if width < tw else None)
            if photo is None:
                wanted.append(key)
                c.create_rectangle(sx0, y0, sx1, y1, fill=theme.PANEL_3, outline="", tags=tags)
                continue
            if frame_level and slot_px > tw + 2:
                c.create_image((sx0 + sx1) / 2, y0, anchor="n", image=photo, tags=tags)
                c.create_line(sx0, y0, sx0, y1, fill=theme.BORDER, tags=("top",))
            else:
                c.create_image(sx0, y0, anchor="nw", image=photo, tags=tags)
        return center

    def _draw_audio_tracks(self) -> None:
        c = self.tracks
        sel_kind, sel_id = self.selection
        for track in self.project.audio_tracks:
            row = self._row("audio", track["id"])
            if row is None:
                continue
            start = float(track["start"])
            x0, x1 = self.x(start), self.x(start + Project.track_duration(track))
            y0, y1 = row["y0"] + 3, row["y1"] - 3
            selected = sel_kind == "audio" and sel_id == track["id"]
            muted = bool(track.get("muted"))
            tags = ("atrack", track["id"])
            c.create_rectangle(x0, y0, x1, y1, fill=theme.CLIP_AUDIO_MUTED if muted else theme.CLIP_AUDIO,
                               outline=theme.TEXT if selected else theme.CLIP_AUDIO_BORDER,
                               width=2 if selected else 1, tags=tags)
            label = self._clip_text(track.get("name", tr("Audio")), max(0, x1 - x0 - 12), self._tk_font)
            if label:
                c.create_text(x0 + 6, (y0 + y1) / 2, text=label, anchor="w",
                              fill=theme.TEXT_FAINT if muted else theme.TEXT, font=self._tk_font, tags=tags)
            # riga bianca del volume della traccia (con le dissolvenze)
            length = Project.track_duration(track)
            vol = 0.0 if muted else float(track.get("volume", 1.0))
            tfi = max(0.0, min(float(track.get("fade_in") or 0.0), length))
            tfo = max(0.0, min(float(track.get("fade_out") or 0.0), length - tfi))

            def level(tt: float, start=start, length=length, vol=vol, tfi=tfi, tfo=tfo) -> float:
                local = tt - start
                r = 1.0
                if tfi > 0:
                    r = min(r, local / tfi)
                if tfo > 0:
                    r = min(r, (length - local) / tfo)
                return vol * max(0.0, r)

            left = self.tracks.canvasx(0)
            self._envelope(start, start + length, y0, y1, level, tags, left, left + self.visible_width())

    def _orig_level(self, clip: dict, start: float, dur: float):
        """Volume dell'audio originale di un pezzo nel tempo (0..), come nell'esportazione."""
        p = self.project
        index = p.clip_index(clip["id"])
        fi, fo = Project.fades(clip)
        a_in = max(fi, p.xfade_after(index - 1) / 2.0, float(clip.get("afade_in") or 0.0))
        a_out = max(fo, p.xfade_after(index) / 2.0, float(clip.get("afade_out") or 0.0))
        a_in = min(a_in, dur)
        a_out = min(a_out, max(0.0, dur - a_in))
        vol = p.original_volume * float(clip.get("volume", 1.0))
        total = p.duration()
        ofi = max(0.0, min(float(p.original_fade_in or 0.0), total))
        ofo = max(0.0, min(float(p.original_fade_out or 0.0), total - ofi))

        def level(t: float) -> float:
            local = t - start
            r = 1.0
            if a_in > 0:
                r = min(r, local / a_in)
            if a_out > 0:
                r = min(r, (dur - local) / a_out)
            if ofi > 0:
                r *= min(1.0, t / ofi)
            if ofo > 0:
                r *= min(1.0, (total - t) / ofo)
            return vol * max(0.0, r)

        return level

    def _envelope(self, t0: float, t1: float, y0: float, y1: float, level, tags: tuple,
                  view_left: float, view_right: float) -> None:
        """Riga bianca del volume sopra una barra audio: in basso = silenzio, 100 % a due terzi dell'altezza."""
        xa, xb = max(self.x(t0), view_left - 4), min(self.x(t1), view_right + 4)
        if xb - xa < 1:
            return
        n = max(2, min(600, int((xb - xa) / 3)))
        top, bottom = y0 + 2, y1 - 2
        points = []
        for k in range(n + 1):
            x = xa + (xb - xa) * k / n
            v = max(0.0, min(1.5, level(self.t(x))))
            points += [x, bottom - (bottom - top) * v / 1.5]
        self.tracks.create_line(*points, fill="#FFFFFF", width=1.5, tags=tags)

    def _draw_effects(self) -> None:
        c = self.tracks
        sel_kind, sel_id = self.selection
        for fx in self.project.effects:
            lane = self._placement.get(fx["id"], 0)
            row = self._row("fx", lane=lane)
            if row is None:
                continue
            x0, x1 = self.x(fx["start"]), self.x(fx["end"])
            y0, y1 = row["y0"] + 2, row["y1"] - 2
            selected = sel_kind == "effect" and sel_id == fx["id"]
            hidden = bool(fx.get("hidden"))
            tags = ("fx", fx["id"])
            c.create_rectangle(x0, y0, max(x1, x0 + 3), y1,
                               fill=theme.NEUTRAL if hidden else theme.FX_COLORS.get(fx["type"], theme.NEUTRAL),
                               outline=theme.TEXT if selected else theme.FX_BORDERS.get(fx["type"], theme.BORDER),
                               width=2 if selected else 1, dash=(3, 2) if hidden else (), tags=tags)
            eye_w = self._draw_eye(fx["id"], x0 + 4, (y0 + y1) / 2, hidden) if x1 - x0 >= 22 else 0
            name = tr(EFFECT_NAMES.get(fx["type"], fx["type"]))
            if fx["type"] == "text":
                name += ": " + (fx.get("text") or "").replace("\n", " ")
            elif fx["type"] == "pixelate":
                shape = tr("Pixel ovale") if fx.get("shape") == "oval" else tr("Pixel")
                if fx.get("track"):
                    name = tr("{name} ({points} punti)").format(name=shape, points=len(fx["track"]))
                else:
                    name = tr("{name} (fisso)").format(name=shape)
            elif fx.get("track"):
                name = tr("{name} (segue)").format(name=name)
            label = self._clip_text(name, max(0, x1 - x0 - 10 - eye_w), self._tk_font)
            if label:
                c.create_text(x0 + 5 + eye_w, (y0 + y1) / 2, text=label, anchor="w",
                              fill=theme.TEXT_DIM if hidden else theme.TEXT, font=self._tk_font, tags=tags)
            # punti del percorso: keyframe (rombi, su tutti gli effetti) e, sull'effetto selezionato, i punti
            # trovati dall'inseguimento (pallini). Clic = seleziona e porta il cursore; Maiusc = intervallo;
            # Ctrl = aggiunge/toglie; Canc o tasto destro = cancella i selezionati
            ym = (y0 + y1) / 2
            r = max(4, min(7, (y1 - y0) / 2 - 2))
            chosen = self.key_sel[1] if self.key_sel[0] == fx["id"] else set()
            manual = {_tkey(k[0]) for k in fx.get("keys") or []}
            if selected:
                for key in fx.get("track") or []:
                    tk = _tkey(key[0])
                    if tk in manual or not (fx["start"] - 1e-6 <= key[0] <= fx["end"] + 1e-6):
                        continue
                    kx = self.x(float(key[0]))
                    on = tk in chosen
                    rr = 4 if on else 2.5
                    c.create_oval(kx - rr, ym - rr, kx + rr, ym + rr, fill=theme.TEXT if on else theme.TEXT_DIM,
                                  outline=theme.ACCENT if on else "", width=2 if on else 1, tags=("kp", fx["id"], tk))
            for key in fx.get("keys") or []:
                tk = _tkey(key[0])
                kx = self.x(float(key[0]))
                on = tk in chosen
                rr = r + 2 if on else r
                c.create_polygon(kx, ym - rr, kx + rr, ym, kx, ym + rr, kx - rr, ym,
                                 fill=theme.TEXT if on else theme.ACCENT, outline=theme.ACCENT if on else theme.BG,
                                 width=2 if on else 1, tags=("kf", fx["id"], tk))

    def _draw_eye(self, fx_id: str, x: float, ym: float, hidden: bool) -> int:
        """Occhio a sinistra della barra: aperto = effetto visibile, barrato = nascosto. Restituisce la larghezza."""
        c = self.tracks
        tags = ("fxeye", fx_id)
        w, h = 14, 8
        color = theme.TEXT_DIM if hidden else theme.TEXT
        # area cliccabile piu' larga del disegno
        c.create_rectangle(x - 2, ym - h, x + w + 2, ym + h, fill="", outline="", tags=tags)
        c.create_oval(x, ym - h / 2, x + w, ym + h / 2, outline=color, width=1.5, tags=tags)
        c.create_oval(x + w / 2 - 2, ym - 2, x + w / 2 + 2, ym + 2, fill=color, outline="", tags=tags)
        if hidden:
            c.create_line(x, ym + h / 2 + 1, x + w, ym - h / 2 - 1, fill=theme.ERR, width=2, tags=tags)
        return w + 4

    def _draw_range(self, height: float) -> None:
        c = self.tracks
        if self.mark_in is None and self.mark_out is None:
            return
        a = self.mark_in if self.mark_in is not None else 0.0
        b = self.mark_out if self.mark_out is not None else self.project.duration()
        if b > a:
            c.create_rectangle(self.x(a), RULER_H, self.x(b), height, fill=theme.ACCENT, stipple="gray25",
                               outline="", tags=("range",))
        for value, color, tag in ((self.mark_in, theme.MARK_IN, "IN"), (self.mark_out, theme.MARK_OUT, "OUT")):
            if value is None:
                continue
            x = self.x(value)
            c.create_line(x, 0, x, height, fill=color, width=1, dash=(4, 2))
            c.create_text(x + (4 if tag == "IN" else -4), RULER_H - 12, text=tag, anchor="w" if tag == "IN" else "e",
                          fill=color, font=self._tk_mono)

    def _draw_playhead(self) -> None:
        c = self.tracks
        c.delete("playhead")
        x = self.x(self.playhead)
        height = max(self._height, self.tracks.winfo_height())
        c.create_line(x, 0, x, height, fill=theme.PLAYHEAD, width=2, tags=("playhead",))
        c.create_polygon(x - 6, 0, x + 6, 0, x, 8, fill=theme.PLAYHEAD, outline="", tags=("playhead",))

    # ------------------------------------------------------------- mouse

    def _item_under(self, event) -> tuple[str | None, str | None, int | None]:
        cx, cy = self.tracks.canvasx(event.x), self.tracks.canvasy(event.y)
        for item in reversed(self.tracks.find_overlapping(cx - 1, cy - 1, cx + 1, cy + 1)):
            tags = self.tracks.gettags(item)
            if not tags or tags[0] in ("playhead", "range"):
                continue
            if tags[0] == "top_bg":
                return None, None, None            # zona ferma: sotto c'e' una riga che e' scorsa via
            if tags[0] in ("clip", "fx", "fxeye", "atrack", "kf", "kp", "oaudio"):
                return tags[0], tags[1], item
        return None, None, None

    def _press(self, event) -> None:
        self.tracks.focus_set()
        kind, item_id, item = self._item_under(event)
        cx = self.tracks.canvasx(event.x)
        if kind == "clip":
            self._on_select("clip", item_id)
            self._drag = {"mode": "clip", "id": item_id, "start_x": cx, "insert_x": None, "moved": False}
            return
        if kind in ("kf", "kp"):
            self._key_click(item_id, self.tracks.gettags(item)[2], event.state)
            self._drag = None
            return
        if kind == "fxeye":
            self._drag = None
            if self.on_fx_visibility is not None:
                self.on_fx_visibility(item_id)
            return
        if kind == "oaudio":
            self._on_select("oaudio", item_id)
            self._drag = {"mode": "seek"}
            self._on_seek(self._snap(self.t(cx)))
            return
        if self.key_sel[1]:
            self.key_sel = (None, set())
        if kind == "fx":
            fx = self.project.effect_by_id(item_id)
            self._on_select("effect", item_id)
            if fx is None:
                return
            resize = cx >= self.x(fx["end"]) - EDGE
            self._drag = {"mode": "fx_resize" if resize else "fx_move", "id": item_id, "start_x": cx,
                          "orig": (fx["start"], fx["end"]), "moved": False,
                          "track": [list(k) for k in fx.get("track", [])],
                          "keys": [list(k) for k in fx.get("keys") or []]}
            return
        if kind == "atrack":
            track = self.project.audio_track_by_id(item_id)
            self._on_select("audio", item_id)
            if track is None:
                return
            self._drag = {"mode": "atrack", "id": item_id, "start_x": cx, "orig": float(track["start"]), "moved": False}
            return
        self._on_select(None, None)
        self._drag = {"mode": "seek"}
        self._on_seek(self._snap(self.t(cx)))

    def _label_press(self, event) -> None:
        """Clic sul nome di una riga audio: seleziona tutta la traccia."""
        y = self.labels.canvasy(event.y)
        for row in self._rows:
            if row["y0"] <= y <= row["y1"]:
                if row["kind"] == "audio_orig":
                    self._on_select("oaudio_all", "orig")
                elif row["kind"] == "audio":
                    self._on_select("audio", row["id"])
                return

    def _key_click(self, fx_id: str, tk: str, state: int) -> None:
        """Selezione dei punti del percorso: clic, Maiusc+clic (intervallo), Ctrl+clic (aggiunge/toglie)."""
        fx = self.project.effect_by_id(fx_id)
        if fx is None:
            return
        same = self.key_sel[0] == fx_id
        chosen = set(self.key_sel[1]) if same else set()
        if state & 0x0001 and same and self._key_anchor is not None:          # Maiusc: intervallo
            a, b = sorted((float(self._key_anchor), float(tk)))
            for k in list(fx.get("track") or []) + list(fx.get("keys") or []):
                if a - 1e-4 <= k[0] <= b + 1e-4:            # i tempi della selezione sono arrotondati
                    chosen.add(_tkey(k[0]))
        elif state & 0x0004:                                                  # Ctrl: aggiunge o toglie
            chosen ^= {tk}
            self._key_anchor = tk
        else:
            chosen = {tk}
            self._key_anchor = tk
        self.key_sel = (fx_id, chosen)
        self._on_select("effect", fx_id)
        self._on_seek(float(tk))
        self.schedule()

    def _pan_start(self, event) -> str:
        self._pan = (event.x, self.tracks.canvasx(0))
        self.tracks.configure(cursor="fleur")
        return "break"

    def _pan_move(self, event) -> str:
        if self._pan is None:
            return "break"
        x0, left0 = self._pan
        total = max(1.0, float(self._scroll_width()))
        left = min(max(0.0, left0 - (event.x - x0)), max(0.0, total - self.visible_width()))
        self.tracks.xview_moveto(left / total)
        self.schedule()
        return "break"

    def _pan_end(self, _event) -> str:
        self._pan = None
        self.tracks.configure(cursor="arrow")
        return "break"

    def _right_press(self, event) -> None:
        kind, item_id, item = self._item_under(event)
        if kind in ("kf", "kp") and self.on_key_delete is not None:
            tk = self.tracks.gettags(item)[2]
            times = self.key_sel[1] if self.key_sel[0] == item_id and tk in self.key_sel[1] else {tk}
            self.on_key_delete(item_id, sorted(float(t) for t in times))
        elif kind in ("fx", "fxeye") and self.on_fx_menu is not None:
            self.on_fx_menu(item_id, event.x_root, event.y_root)

    def _snap(self, t: float) -> float:
        fps = max(1.0, self.project.fps)
        return min(max(0.0, round(t * fps) / fps), self.project.duration())

    def _motion(self, event) -> None:
        d = self._drag
        if d is None:
            return
        cx = self.tracks.canvasx(event.x)
        if d["mode"] == "seek":
            self._on_seek(self._snap(self.t(cx)))
            return
        if abs(cx - d["start_x"]) < 3 and not d["moved"]:
            return
        if not d["moved"]:
            d["moved"] = True
            if d["mode"] != "clip":
                self._on_edit_start()
        dt = (cx - d["start_x"]) / self.pps
        if d["mode"] == "clip":
            d["insert_x"] = self.x(self._insert_time(cx))
            self.schedule()
        elif d["mode"] in ("fx_move", "fx_resize"):
            fx = self.project.effect_by_id(d["id"])
            if fx is None:
                return
            s0, e0 = d["orig"]
            total = max(self.project.duration(), e0)
            if d["mode"] == "fx_move":
                length = e0 - s0
                start = min(max(0.0, self._snap(s0 + dt)), max(0.0, total - length))
                fx["start"], fx["end"] = start, start + length
                shift = start - s0
                if d["track"]:
                    fx["track"] = [[k[0] + shift, k[1], k[2], *k[3:]] for k in d["track"]]
                if d["keys"]:
                    fx["keys"] = [[k[0] + shift, *k[1:]] for k in d["keys"]]
            else:
                fx["end"] = max(s0 + 0.1, min(total, self._snap(e0 + dt)))
            self.project.dirty = True
            self.schedule()
            self._on_changed()
        elif d["mode"] == "atrack":
            track = self.project.audio_track_by_id(d["id"])
            if track is None:
                return
            track["start"] = max(0.0, self._snap(d["orig"] + dt))
            self.project.dirty = True
            self.schedule()
            self._on_changed()

    def _insert_time(self, cx: float) -> float:
        """L'istante di inserimento piu' vicino (confine fra due clip) alla posizione del mouse."""
        t = self.t(cx)
        bounds = self.project.starts() + [self.project.duration()]
        return min(bounds, key=lambda b: abs(b - t))

    def _release(self, event) -> None:
        d = self._drag
        self._drag = None
        if d is None:
            return
        if d["mode"] == "clip" and d["moved"]:
            cx = self.tracks.canvasx(event.x)
            index = self.project.clip_index(d["id"])
            target_t = self._insert_time(cx)
            bounds = self.project.starts() + [self.project.duration()]
            target = bounds.index(target_t)
            if index >= 0:
                new_index = target if target <= index else target - 1
                if new_index != index:
                    self._on_edit_start()
                    self.project.move_clip(index, new_index)
                    self._on_changed()
            self.schedule()
        elif d["mode"] in ("fx_move", "fx_resize", "atrack") and d["moved"]:
            self._on_changed()

    def _hover(self, event) -> None:
        if self._drag is not None:
            return
        kind, item_id, _item = self._item_under(event)
        cursor = "arrow"
        if kind in ("kf", "kp", "fxeye"):
            cursor = "hand2"
        elif kind == "fx":
            fx = self.project.effect_by_id(item_id)
            if fx is not None and self.tracks.canvasx(event.x) >= self.x(fx["end"]) - EDGE:
                cursor = "sb_h_double_arrow"
            else:
                cursor = "fleur"
        elif kind in ("clip", "atrack"):
            cursor = "fleur"
        self.tracks.configure(cursor=cursor)

    def _wheel(self, event) -> None:
        if event.state & 0x0004:  # Ctrl: zoom
            self.zoom_by(1.25 if event.delta > 0 else 0.8, around_x=event.x)
        else:
            self.tracks.xview_scroll(-3 if event.delta > 0 else 3, "units")
            self.schedule()
        return "break"


def _tkey(t: float) -> str:
    """Identita' di un punto del percorso nella selezione: il suo tempo, arrotondato."""
    return f"{float(t):.4f}"
