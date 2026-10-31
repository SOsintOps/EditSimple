# EditSimple — montaggio video per presentazioni.  Copyright (C) 2026 Andrea Cumini <andrea@osintinfo.net>
# SPDX-License-Identifier: GPL-3.0-only
# GNU GPL v3 con termini aggiuntivi (attribuzione dell'autore): vedi LICENSE e NOTICE.
"""Anteprima del fotogramma composto, con disegno e modifica delle sovraimpressioni col mouse.

Il fotogramma arriva gia' composto (overlays.compose) alla misura della vista;
qui si disegna, si mostrano le maniglie dell'effetto selezionato e si
gestiscono le modalita' di disegno (riquadro, freccia, testo, zoom,
pixelatura). Le coordinate passate alle callback sono in pixel del progetto.
"""

from __future__ import annotations

import math
import sys
import tkinter as tk
from typing import Callable

import customtkinter as ctk
from PIL import Image, ImageTk

from . import overlays, theme, widgets
from .i18n import N_, tr

# cursori di ridimensionamento diagonale: i nomi "size_*" esistono solo su Windows e macOS,
# su X11 Tk rifiuta il cursore ("bad cursor spec") e il gestore del movimento fallisce
if sys.platform == "win32" or sys.platform == "darwin":
    NW_SE, NE_SW = "size_nw_se", "size_ne_sw"
else:
    NW_SE, NE_SW = "top_left_corner", "top_right_corner"

HANDLE = 6
HIT = 10
RECT_MODES = ("box", "oval", "zoom", "pixelate", "logo", "text", "image", "timer", "frames")   # figure con le maniglie agli angoli
SCALED_BLOCKS = ("logo", "text", "image", "timer", "frames")    # si ridimensionano in proporzione dagli angoli
KEYED_TYPES = ("box", "oval", "arrow", "zoom", "pixelate")   # figure che seguono un percorso con keyframe
MODE_HELP = {
    "box": N_("Trascina sull'anteprima per disegnare il riquadro"),
    "oval": N_("Trascina sull'anteprima per disegnare l'ovale"),
    "zoom": N_("Trascina sull'anteprima un rettangolo sull'oggetto da ingrandire"),
    "zoom_place": N_("Clicca dove far apparire il riquadro ingrandito  -  {factor}x  (rotellina o tasti 2, 3, 4, 6, 8)"),
    "pixelate": N_("Trascina sull'anteprima l'area da pixelare: verra' inseguita nei fotogrammi successivi"),
    "arrow": N_("Trascina dalla coda alla punta della freccia"),
    "arrow_target": N_("Trascina un rettangolo attorno al soggetto che la freccia deve seguire"),
    "text": N_("Clicca sull'anteprima dove mettere il testo"),
    "timer": N_("Clicca sull'anteprima dove mettere il tempo trascorso"),
    "frames": N_("Clicca sull'anteprima dove mettere il numero del fotogramma"),
}


MAX_VIEW_ZOOM = 16.0                    # ingrandimento massimo della vista (Ctrl+rotellina)


class PreviewView(ctk.CTkFrame):
    def __init__(self, master, on_draw: Callable[[str, dict], None], on_select: Callable[[dict | None], None],
                 on_edit_start: Callable[[dict], None], on_edit: Callable[[dict, bool], None],
                 on_wheel: Callable[[int], None], active_effects: Callable[[], list[dict]]) -> None:
        super().__init__(master, fg_color=theme.PANEL, corner_radius=4, border_width=1, border_color=theme.BORDER)
        self.canvas = tk.Canvas(self, bg=theme.BG, highlightthickness=0, bd=0, cursor="arrow")
        self.canvas.pack(fill="both", expand=True, padx=1, pady=1)
        self._on_draw = on_draw
        self._on_select = on_select
        self._on_edit_start = on_edit_start
        self._on_edit = on_edit
        self._on_wheel = on_wheel
        self._active_effects = active_effects
        self._image: Image.Image | None = None
        self._photo: ImageTk.PhotoImage | None = None
        self._project_size = (1920, 1080)
        self._scale = 1.0                   # pixel della tela per pixel del progetto
        self._img_scale = 1.0               # pixel dell'immagine composta per pixel del progetto
        self._ox = 0
        self._oy = 0
        # ingrandimento della vista (Ctrl+rotellina) e punto del progetto al centro della tela
        self.view_zoom = 1.0
        self._view_center: tuple[float, float] | None = None
        self._pan: tuple[int, int, float, float] | None = None
        self.mode: str | None = None
        self.selected: dict | None = None
        self._drag: dict | None = None
        self._rubber: tuple[float, float, float, float] | None = None
        self.placeholder = N_("Importa un video per vedere l'anteprima")   # tradotto quando si disegna
        self.on_resize: Callable[[], None] | None = None
        self.zoom_shape = "rect"            # forma dello zoom che si sta creando
        self.on_edit_text: Callable | None = None
        # keyframe dall'anteprima: (effetto, istante, centro x, centro y, scala, copia del percorso, definitivo)
        self.on_key: Callable | None = None
        self._resize_job: str | None = None
        # zoom: dopo il rettangolo sull'oggetto, un riquadro fantasma segue il mouse finche' si clicca
        self.zoom_factor = 2
        self._zoom_area: tuple[int, int, int, int] | None = None
        self._ghost_at: tuple[float, float] | None = None
        self._ghost_photo: ImageTk.PhotoImage | None = None

        self.canvas.bind("<Configure>", self._configured)
        self.canvas.bind("<ButtonPress-1>", self._press)
        self.canvas.bind("<B1-Motion>", self._motion)
        self.canvas.bind("<ButtonRelease-1>", self._release)
        self.canvas.bind("<Motion>", self._hover)
        widgets.bind_wheel(self.canvas, self._wheel)
        widgets.bind_wheel(self.canvas, self._zoom_wheel, "Control-")
        # spostare la vista ingrandita: tasto centrale o Alt+trascina; doppio clic centrale = adatta
        for press, motion, release in (("<ButtonPress-2>", "<B2-Motion>", "<ButtonRelease-2>"),
                                       ("<Alt-ButtonPress-1>", "<Alt-B1-Motion>", "<Alt-ButtonRelease-1>")):
            self.canvas.bind(press, self._pan_start)
            self.canvas.bind(motion, self._pan_move)
            self.canvas.bind(release, self._pan_end)
        self.canvas.bind("<Double-Button-2>", lambda _e: self.reset_view())
        self.canvas.bind("<Key>", self._key)
        self.canvas.bind("<Double-Button-1>", self._double)

    # ------------------------------------------------------------- stato

    def _fit_scale(self) -> float:
        cw, ch = max(16, self.canvas.winfo_width() - 8), max(16, self.canvas.winfo_height() - 8)
        W, H = self._project_size
        return min(cw / W, ch / H)

    def display_size(self) -> tuple[int, int]:
        """Misura (larghezza, altezza) con cui comporre il fotogramma per riempire la vista.

        Con la vista ingrandita il fotogramma si compone piu' grande (fino alla
        risoluzione del progetto, oltre non c'e' altro dettaglio) e se ne
        mostra solo la parte visibile.
        """
        W, H = self._project_size
        fit = self._fit_scale()
        scale = max(fit, min(fit * self.view_zoom, 1.0)) if self.view_zoom > 1 else fit
        return max(2, int(W * scale)), max(2, int(H * scale))

    # ------------------------------------------------------------- vista ingrandita

    def _zoom_wheel(self, event) -> str:
        step = 1.25 if event.delta > 0 else 1 / 1.25
        self.zoom_view(self.view_zoom * step, event.x, event.y)
        return "break"

    def zoom_view(self, zoom: float, cx: float | None = None, cy: float | None = None) -> None:
        """Ingrandisce la vista tenendo fermo sotto il mouse il punto (cx, cy) della tela."""
        zoom = min(MAX_VIEW_ZOOM, max(1.0, zoom))
        if abs(zoom - 1.0) < 0.05:
            zoom = 1.0
        if zoom == self.view_zoom:
            return
        cw, ch = self.canvas.winfo_width(), self.canvas.winfo_height()
        if cx is None:
            cx, cy = cw / 2, ch / 2
        W, H = self._project_size
        if self._scale > 0:
            px, py = (cx - self._ox) / self._scale, (cy - self._oy) / self._scale
        else:
            px, py = W / 2, H / 2
        ds = self._fit_scale() * zoom
        self.view_zoom = zoom
        self._view_center = (px - (cx - cw / 2) / ds, py - (cy - ch / 2) / ds) if zoom > 1 else None
        self._redraw()                       # subito con l'immagine che c'e', poi il fotogramma alla nuova misura
        if self.on_resize is not None:
            self.on_resize()

    def reset_view(self) -> None:
        self.zoom_view(1.0)

    def _pan_start(self, event) -> str:
        if self.view_zoom <= 1:
            return "break"
        W, H = self._project_size
        vx, vy = self._view_center or (W / 2, H / 2)
        self._pan = (event.x, event.y, vx, vy)
        self.canvas.configure(cursor="fleur")
        return "break"

    def _pan_move(self, event) -> str:
        if self._pan is None or self._scale <= 0:
            return "break"
        x0, y0, vx, vy = self._pan
        self._view_center = (vx - (event.x - x0) / self._scale, vy - (event.y - y0) / self._scale)
        self._redraw()
        return "break"

    def _pan_end(self, _event) -> str:
        if self._pan is not None:
            self._pan = None
            self.canvas.configure(cursor="crosshair" if self.mode else "arrow")
        return "break"

    def set_project_size(self, size: tuple[int, int]) -> None:
        self._project_size = size

    def set_frame(self, image: Image.Image | None) -> None:
        self._image = image
        self._redraw()

    def set_selected(self, fx: dict | None) -> None:
        self.selected = fx
        self._redraw()

    def set_mode(self, mode: str | None) -> None:
        self.mode = mode
        self.canvas.configure(cursor="crosshair" if mode else "arrow")
        self._rubber = None
        self._zoom_area = None
        self._ghost_at = None
        self._redraw()

    def set_zoom_factor(self, factor: int) -> None:
        self.zoom_factor = int(factor)
        if self.mode == "zoom_place":
            self._redraw()

    def _wheel(self, event) -> None:
        if self.mode == "zoom_place":
            factors = overlays.ZOOM_FACTORS
            i = factors.index(self.zoom_factor) if self.zoom_factor in factors else 0
            i = min(len(factors) - 1, i + 1) if event.delta > 0 else max(0, i - 1)
            self.set_zoom_factor(factors[i])
            return
        self._on_wheel(-1 if event.delta > 0 else 1)

    def _key(self, event) -> None:
        if self.mode == "zoom_place" and event.char in ("2", "3", "4", "6", "8"):
            self.set_zoom_factor(int(event.char))

    # ------------------------------------------------------------- coordinate

    def _to_canvas(self, x: float, y: float) -> tuple[float, float]:
        return self._ox + x * self._scale, self._oy + y * self._scale

    def _to_project(self, cx: float, cy: float) -> tuple[float, float]:
        if self._scale <= 0:
            return 0.0, 0.0
        W, H = self._project_size
        x = (cx - self._ox) / self._scale
        y = (cy - self._oy) / self._scale
        return min(max(0.0, x), W), min(max(0.0, y), H)

    def _configured(self, _event=None) -> None:
        if self._resize_job is not None:
            self.after_cancel(self._resize_job)
        self._resize_job = self.after(60, self._resized)

    def _resized(self) -> None:
        self._resize_job = None
        if self.on_resize is not None:
            self.on_resize()
        else:
            self._redraw()

    # ------------------------------------------------------------- disegno

    def _redraw(self) -> None:
        c = self.canvas
        c.delete("all")
        cw, ch = c.winfo_width(), c.winfo_height()
        if self._image is None:
            c.create_text(cw // 2, ch // 2, text=tr(self.placeholder), fill=theme.TEXT_FAINT,
                          font=(theme.ui_font(), 12))
            return
        W, H = self._project_size
        self._img_scale = self._image.width / W
        if self.view_zoom <= 1:
            self._scale = self._img_scale
            self._ox = (cw - self._image.width) // 2
            self._oy = (ch - self._image.height) // 2
            self._photo = ImageTk.PhotoImage(self._image)
            c.create_image(self._ox, self._oy, image=self._photo, anchor="nw")
            c.create_rectangle(self._ox - 1, self._oy - 1, self._ox + self._image.width, self._oy + self._image.height,
                               outline=theme.BORDER_STRONG)
        else:
            self._draw_zoomed(cw, ch)
        if self.selected is not None and self._active(self.selected):
            # la cornice di selezione solo mentre l'effetto si vede (fuori dal suo tempo non c'e' nulla da toccare)
            self._draw_selection(self.selected)
        if self._rubber is not None:
            x0, y0, x1, y1 = self._rubber
            if self.mode == "arrow":
                c.create_line(x0, y0, x1, y1, fill=theme.ACCENT, width=2, arrow="last", dash=(5, 3))
            else:
                c.create_rectangle(x0, y0, x1, y1, outline=theme.ACCENT, width=2, dash=(5, 3))
        if self.mode == "zoom_place" and self._zoom_area is not None:
            ax, ay, aw, ah = self._zoom_area
            x0, y0 = self._to_canvas(ax, ay)
            x1, y1 = self._to_canvas(ax + aw, ay + ah)
            c.create_rectangle(x0, y0, x1, y1, outline=theme.ACCENT, width=2)
            self._draw_ghost()
        if self.mode:
            # la scritta di aiuto ha uno sfondo e resta sopra a tutto (anche al riquadro fantasma dello zoom)
            item = c.create_text(cw // 2, max(0, self._oy) + 14, text=tr(MODE_HELP.get(self.mode, "")).format(factor=self.zoom_factor),
                                 fill=theme.ACCENT, font=(theme.ui_font(), 11, "bold"), tags="help")
            x0, y0, x1, y1 = c.bbox(item)
            back = c.create_rectangle(x0 - 8, y0 - 3, x1 + 8, y1 + 3, fill=theme.PANEL, outline=theme.BORDER, tags="help")
            c.tag_lower(back, item)

    def _draw_zoomed(self, cw: int, ch: int) -> None:
        """Solo la parte visibile del fotogramma, ingrandita, centrata su _view_center."""
        c = self.canvas
        W, H = self._project_size
        ds = self._fit_scale() * self.view_zoom
        vx, vy = self._view_center or (W / 2, H / 2)
        # la vista non esce dal fotogramma (se il fotogramma e' piu' piccolo della tela resta al centro)
        half_w, half_h = cw / (2 * ds), ch / (2 * ds)
        vx = W / 2 if W * ds <= cw else min(max(vx, half_w), W - half_w)
        vy = H / 2 if H * ds <= ch else min(max(vy, half_h), H - half_h)
        self._view_center = (vx, vy)
        self._scale = ds
        self._ox = int(round(cw / 2 - vx * ds))
        self._oy = int(round(ch / 2 - vy * ds))
        x0, y0 = max(0, self._ox), max(0, self._oy)
        x1, y1 = min(cw, self._ox + int(W * ds)), min(ch, self._oy + int(H * ds))
        if x1 - x0 < 2 or y1 - y0 < 2:
            return
        k = self._img_scale / ds             # pixel dell'immagine per pixel della tela
        box = ((x0 - self._ox) * k, (y0 - self._oy) * k, (x1 - self._ox) * k, (y1 - self._oy) * k)
        resample = Image.NEAREST if ds >= 3 else Image.BILINEAR   # molto vicino: si vedono i pixel veri
        region = self._image.resize((x1 - x0, y1 - y0), resample, box=box)
        self._photo = ImageTk.PhotoImage(region)
        c.create_image(x0, y0, image=self._photo, anchor="nw")
        c.create_rectangle(self._ox - 1, self._oy - 1, self._ox + int(W * ds), self._oy + int(H * ds),
                           outline=theme.BORDER_STRONG)
        item = c.create_text(cw - 10, ch - 8, anchor="se", fill=theme.TEXT_SOFT, font=(theme.ui_font(), 10),
                             text=tr("{zoom}% - trascina per spostarti, doppio clic centrale: adatta").format(
                                 zoom=int(round(ds * 100))), tags="viewzoom")
        bx0, by0, bx1, by1 = c.bbox(item)
        back = c.create_rectangle(bx0 - 6, by0 - 3, bx1 + 6, by1 + 3, fill=theme.PANEL, outline=theme.BORDER,
                                  tags="viewzoom")
        c.tag_lower(back, item)

    def _ghost_fx(self, cx: float, cy: float) -> dict:
        """Lo zoom che verrebbe creato cliccando in (cx, cy), pixel del progetto."""
        W, H = self._project_size
        ax, ay, aw, ah = self._zoom_area
        fx = {"x": ax, "y": ay, "w": aw, "h": ah, "factor": self.zoom_factor, "thickness": max(3, H // 270),
              "shape": self.zoom_shape, "color": "#FFD60A"}
        overlays.place_inset(fx, cx, cy, W, H)
        return fx

    def _draw_ghost(self) -> None:
        """Il riquadro ingrandito sotto il mouse, con il contenuto vero dell'area ingrandita."""
        c = self.canvas
        c.delete("ghost")
        if self._zoom_area is None or self._ghost_at is None or self._image is None:
            return
        W, H = self._project_size
        fx = self._ghost_fx(*self._ghost_at)
        x, y, w, h = overlays.zoom_rect(fx, W, H)
        bx, by, bw, bh = overlays.inset_rect(fx, W, H)
        s = self._scale
        si = self._img_scale
        t = max(1, int(round(overlays.zoom_border(fx) * s)))
        iw, ih = max(1, int(bw * s) - 2 * t), max(1, int(bh * s) - 2 * t)
        region = self._image.crop((int(x * si), int(y * si), max(int(x * si) + 1, int((x + w) * si)),
                                   max(int(y * si) + 1, int((y + h) * si))))
        self._ghost_photo = ImageTk.PhotoImage(region.resize((iw, ih), Image.BILINEAR))
        x0, y0 = self._to_canvas(bx, by)
        c.create_rectangle(x0, y0, x0 + bw * s, y0 + bh * s, fill="#FFFFFF", outline=theme.ACCENT, width=1, tags="ghost")
        c.create_image(x0 + t, y0 + t, image=self._ghost_photo, anchor="nw", tags="ghost")
        c.create_text(x0 + 8, y0 + 8, text=f"{self.zoom_factor}x", anchor="nw", fill=theme.ACCENT,
                      font=(theme.ui_font(), 12, "bold"), tags="ghost")
        c.tag_raise("help")

    def _draw_selection(self, fx: dict) -> None:
        c = self.canvas
        color = theme.FX_BORDERS.get(fx["type"], theme.ACCENT)
        if fx["type"] == "arrow":
            g = overlays.displaced(fx, self._current_time())     # dove l'inseguimento la mostra adesso
            x0, y0 = self._to_canvas(g["x1"], g["y1"])
            x1, y1 = self._to_canvas(g["x2"], g["y2"])
            c.create_line(x0, y0, x1, y1, fill=color, width=1, dash=(4, 3))
            for hx, hy in ((x0, y0), (x1, y1)):
                c.create_oval(hx - HANDLE, hy - HANDLE, hx + HANDLE, hy + HANDLE, fill=color, outline=theme.BG)
            return
        bx0, by0, bx1, by1 = self._selection_bbox(fx)
        x0, y0 = self._to_canvas(bx0, by0)
        x1, y1 = self._to_canvas(bx1, by1)
        c.create_rectangle(x0, y0, x1, y1, outline=color, width=2, dash=(6, 3))
        if fx["type"] in RECT_MODES:
            for hx, hy in ((x0, y0), (x1, y0), (x0, y1), (x1, y1)):
                c.create_rectangle(hx - HANDLE, hy - HANDLE, hx + HANDLE, hy + HANDLE, fill=color, outline=theme.BG)
        if fx.get("track") and fx["type"] != "pixelate":
            c.create_text(x0, y0 - 10, text=tr("segue il soggetto"), anchor="sw", fill=color, font=(theme.ui_font(), 9, "bold"))
        if fx["type"] == "zoom":
            # anche il riquadro ingrandito si sposta e si ridimensiona
            ix0, iy0, ix1, iy1 = self._inset_bbox(fx)
            x0, y0 = self._to_canvas(ix0, iy0)
            x1, y1 = self._to_canvas(ix1, iy1)
            c.create_rectangle(x0, y0, x1, y1, outline=color, width=2)
            if fx.get("factor"):
                c.create_text(x0 + 6, y0 + 6, text=f"{fx['factor']}x", anchor="nw", fill=color,
                              font=(theme.ui_font(), 11, "bold"))
            else:
                for hx, hy in ((x0, y0), (x1, y0), (x0, y1), (x1, y1)):
                    c.create_oval(hx - HANDLE, hy - HANDLE, hx + HANDLE, hy + HANDLE, fill=color, outline=theme.BG)

    def _inset_bbox(self, fx: dict) -> tuple[float, float, float, float]:
        W, H = self._project_size
        bx, by, bw, bh = overlays.inset_rect(fx, W, H)
        return bx, by, bx + bw, by + bh

    def _selection_bbox(self, fx: dict) -> tuple[float, float, float, float]:
        if fx["type"] == "pixelate":
            x, y, w, h = overlays.pixelate_rect(fx, self._current_time(), *self._project_size)
            return x, y, x + w, y + h
        if fx["type"] == "zoom":
            # l'area ingrandita resta dentro al fotogramma anche quando l'oggetto arriva al bordo
            x, y, w, h = overlays.zoom_rect(overlays.displaced(fx, self._current_time()), *self._project_size)
            return x, y, x + w, y + h
        return overlays.effect_bbox(overlays.displaced(fx, self._current_time()))

    def _track_offset(self, fx: dict) -> tuple[float, float]:
        """Di quanto l'inseguimento sposta la figura adesso (zero se non segue nulla)."""
        keys = fx.get("track")
        if not keys or fx["type"] == "pixelate":
            return 0.0, 0.0
        ax, ay = overlays.pixelate_position(fx, self._current_time())
        return ax - float(keys[0][1]), ay - float(keys[0][2])

    def _active(self, fx: dict) -> bool:
        """L'effetto si vede all'istante del cursore."""
        t = self._current_time()
        return (not fx.get("hidden")
                and float(fx.get("start", 0.0)) - 1e-6 <= t < float(fx.get("end", 0.0)) + 1e-6)

    def _current_time(self) -> float:
        return getattr(self, "time", 0.0)

    # ------------------------------------------------------------- mouse

    def _hit(self, cx: float, cy: float) -> str | None:
        """'nw'/'ne'/'sw'/'se' su una maniglia, 'p1'/'p2' sulle punte della freccia, 'move' dentro, None fuori."""
        fx = self.selected
        if fx is None or not self._active(fx):
            return None
        if fx["type"] == "arrow":
            g = overlays.displaced(fx, self._current_time())
            p1 = self._to_canvas(g["x1"], g["y1"])
            p2 = self._to_canvas(g["x2"], g["y2"])
            for name, (hx, hy) in (("p1", p1), ("p2", p2)):
                if abs(cx - hx) <= HIT and abs(cy - hy) <= HIT:
                    return name
            if _segment_distance(cx, cy, *p1, *p2) <= HIT:
                return "move"
            return None
        if fx["type"] == "zoom" and not fx.get("factor"):
            ix0, iy0, ix1, iy1 = self._inset_bbox(fx)
            x0, y0 = self._to_canvas(ix0, iy0)
            x1, y1 = self._to_canvas(ix1, iy1)
            for name, (hx, hy) in {"inw": (x0, y0), "ine": (x1, y0), "isw": (x0, y1), "ise": (x1, y1)}.items():
                if abs(cx - hx) <= HIT and abs(cy - hy) <= HIT:
                    return name
        bx0, by0, bx1, by1 = self._selection_bbox(fx)
        x0, y0 = self._to_canvas(bx0, by0)
        x1, y1 = self._to_canvas(bx1, by1)
        if fx["type"] in RECT_MODES:
            for name, (hx, hy) in {"nw": (x0, y0), "ne": (x1, y0), "sw": (x0, y1), "se": (x1, y1)}.items():
                if abs(cx - hx) <= HIT and abs(cy - hy) <= HIT:
                    return name
        if x0 - 2 <= cx <= x1 + 2 and y0 - 2 <= cy <= y1 + 2:
            return "move"
        if fx["type"] == "zoom":
            ix0, iy0, ix1, iy1 = self._inset_bbox(fx)
            x0, y0 = self._to_canvas(ix0, iy0)
            x1, y1 = self._to_canvas(ix1, iy1)
            if x0 - 2 <= cx <= x1 + 2 and y0 - 2 <= cy <= y1 + 2:
                return "imove"
        return None

    def _hover(self, event) -> None:
        if self.mode == "zoom_place" and self._zoom_area is not None and self._image is not None:
            self._ghost_at = self._to_project(event.x, event.y)
            self._draw_ghost()
            return
        if self.mode or self._drag or self._image is None:
            return
        hit = self._hit(event.x, event.y)
        cursor = {"nw": NW_SE, "se": NW_SE, "ne": NE_SW, "sw": NE_SW,
                  "inw": NW_SE, "ise": NW_SE, "ine": NE_SW, "isw": NE_SW,
                  "move": "fleur", "imove": "fleur", "p1": "hand2", "p2": "hand2"}.get(
            hit, "fleur" if self.view_zoom > 1 else "arrow")
        self.canvas.configure(cursor=cursor)

    def _press(self, event) -> None:
        self.canvas.focus_set()
        if self._image is None:
            return
        if self.mode == "zoom_place":
            if self._zoom_area is not None:
                fx = self._ghost_fx(*self._to_project(event.x, event.y))
                ax, ay, aw, ah = self._zoom_area
                cx, cy = overlays.inset_center(fx, *self._project_size)
                self._on_draw("zoom", {"x": ax, "y": ay, "w": aw, "h": ah, "factor": self.zoom_factor,
                                       "cx": int(cx), "cy": int(cy)})
            return
        if self.mode:
            self._drag = {"mode": "draw", "start": (event.x, event.y)}
            if self.mode in ("text", "timer", "frames"):
                x, y = self._to_project(event.x, event.y)
                self._drag = None
                self._on_draw(self.mode, {"x": int(x), "y": int(y)})
            return
        hit = self._hit(event.x, event.y)
        if hit is None:
            # clic su un altro effetto attivo: selezione
            px, py = self._to_project(event.x, event.y)
            for fx in reversed(self._active_effects()):
                if fx["type"] == "arrow":
                    g = overlays.displaced(fx, self._current_time())
                    p1 = self._to_canvas(g["x1"], g["y1"])
                    p2 = self._to_canvas(g["x2"], g["y2"])
                    inside = _segment_distance(event.x, event.y, *p1, *p2) <= HIT
                else:
                    x0, y0, x1, y1 = self._selection_bbox(fx)
                    inside = x0 <= px <= x1 and y0 <= py <= y1
                    if not inside and fx["type"] == "zoom":
                        x0, y0, x1, y1 = self._inset_bbox(fx)
                        inside = x0 <= px <= x1 and y0 <= py <= y1
                if inside:
                    self._on_select(fx)
                    return
            self._on_select(None)
            if self.view_zoom > 1:
                # vista ingrandita: clic e trascina su un punto vuoto sposta la vista
                self._pan_start(event)
                self._drag = {"mode": "pan"}
            return
        fx = self.selected
        self._on_edit_start(fx)
        t = self._current_time()
        if (self.on_key is not None and fx.get("track") and fx["type"] in KEYED_TYPES
                and fx["start"] <= t < fx["end"] and (hit in ("move", "nw", "ne", "sw", "se") or hit == "p2")):
            # la figura segue un percorso: spostarla o ridimensionarla qui mette un keyframe a questo istante
            cx, cy, s = overlays.figure_center(fx, t)
            self._drag = {"mode": "key_" + hit, "start": self._to_project(event.x, event.y), "t": t,
                          "center": (cx, cy), "scale": s,
                          "snap": ([list(k) for k in fx.get("track") or []], [list(k) for k in fx.get("keys") or []])}
            if fx["type"] != "arrow":
                g = overlays.displaced(fx, t)
                self._drag["rect"] = (float(g["x"]), float(g["y"]), float(g["w"]), float(g["h"]))
            return
        self._drag = {"mode": hit, "start": self._to_project(event.x, event.y), "orig": _copy_geometry(fx)}
        if fx["type"] == "zoom":
            self._drag["icenter"] = overlays.inset_center(fx, *self._project_size)
        if fx["type"] in SCALED_BLOCKS:
            self._drag.update(lbox=overlays.effect_bbox(fx), lw=float(fx.get("w") or 200), lsize=float(fx.get("size") or 40))

    def _motion(self, event) -> None:
        d = self._drag
        if d is None:
            return
        if d["mode"] == "pan":
            self._pan_move(event)
            return
        if d["mode"] == "draw":
            x0, y0 = d["start"]
            self._rubber = (x0, y0, event.x, event.y)
            self._redraw()
            return
        fx = self.selected
        if fx is None:
            return
        if d["mode"].startswith("key_"):
            self._key_motion(d, fx, event, final=False)
            return
        px, py = self._to_project(event.x, event.y)
        sx, sy = d["start"]
        dx, dy = px - sx, py - sy
        o = d["orig"]
        W, H = self._project_size
        mode = d["mode"]
        # con l'inseguimento la figura e' disegnata spostata: il mouse lavora sulla geometria di base
        off_x, off_y = self._track_offset(fx)
        px -= off_x
        py -= off_y
        if fx["type"] == "arrow":
            if mode == "move":
                fx["x1"], fx["y1"] = o["x1"] + dx, o["y1"] + dy
                fx["x2"], fx["y2"] = o["x2"] + dx, o["y2"] + dy
            elif mode == "p1":
                fx["x1"], fx["y1"] = px, py
            else:
                fx["x2"], fx["y2"] = px, py
            for key in ("x1", "y1", "x2", "y2"):
                fx[key] = int(round(fx[key]))
        elif fx["type"] in SCALED_BLOCKS and mode in ("nw", "ne", "sw", "se"):
            # logo, testo e immagine crescono in proporzione; l'angolo opposto a quello trascinato resta fermo
            x0, y0, x1, y1 = d["lbox"]
            ax = x1 if "w" in mode else x0
            ay = y1 if "n" in mode else y0
            ratio = max(0.05, abs(px - ax) / max(1.0, x1 - x0))
            if fx["type"] in ("logo", "image"):
                fx["w"] = max(8, int(round(d["lw"] * ratio)))
            if fx["type"] in ("logo", "text", "timer", "frames"):
                fx["size"] = max(6, int(round(d["lsize"] * ratio)))
            nb = overlays.effect_bbox(dict(fx, x=0, y=0))
            fx["x"] = int(round(ax - (nb[2] - nb[0]) if "w" in mode else ax))
            fx["y"] = int(round(ay - (nb[3] - nb[1]) if "n" in mode else ay))
        elif mode == "imove":
            _bx, _by, bw, bh = overlays.inset_rect(fx, W, H)
            fx["bx"] = int(round(min(max(o["bx"] + dx, 0), W - bw)))
            fx["by"] = int(round(min(max(o["by"] + dy, 0), H - bh)))
        elif mode in ("inw", "ine", "isw", "ise"):
            # il riquadro ingrandito mantiene le proporzioni dell'area
            x0, y0, x1, y1 = o["bx"], o["by"], o["bx"] + o["bw"], o["by"] + o["bh"]
            ratio = o["h"] / max(1, o["w"])
            if "w" in mode:
                x0 = min(px, x1 - 16)
            else:
                x1 = max(px, x0 + 16)
            bw = x1 - x0
            bh = bw * ratio
            if "n" in mode:
                y0 = y1 - bh
            else:
                y1 = y0 + bh
            fx["bx"], fx["by"] = int(round(x0)), int(round(y0))
            fx["bw"], fx["bh"] = max(16, int(round(bw))), max(16, int(round(bh)))
        elif mode == "move":
            if fx["type"] == "pixelate":
                fx["x"] = int(round(o["x"] + dx))
                fx["y"] = int(round(o["y"] + dy))
                if o.get("track"):
                    fx["track"] = [[k[0], k[1] + dx, k[2] + dy, *k[3:]] for k in o["track"]]
            else:
                w, h = (o.get("w", 0), o.get("h", 0))
                if fx["type"] in SCALED_BLOCKS:
                    bx0, by0, bx1, by1 = overlays.effect_bbox(fx)
                    w, h = bx1 - bx0, by1 - by0
                fx["x"] = int(round(min(max(o["x"] + dx, -w * 0.9), W - w * 0.1)))
                fx["y"] = int(round(min(max(o["y"] + dy, -h * 0.9), H - h * 0.1)))
        else:
            x0, y0, x1, y1 = o["x"], o["y"], o["x"] + o["w"], o["y"] + o["h"]
            MIN = 8
            if "w" in mode:
                x0 = min(px, x1 - MIN)
            else:
                x1 = max(px, x0 + MIN)
            if "n" in mode:
                y0 = min(py, y1 - MIN)
            else:
                y1 = max(py, y0 + MIN)
            fx["x"], fx["y"] = int(round(x0)), int(round(y0))
            fx["w"], fx["h"] = max(MIN, int(round(x1 - x0))), max(MIN, int(round(y1 - y0)))
            if fx["type"] == "zoom" and fx.get("factor"):
                # il riquadro ingrandito cambia misura con l'area e resta centrato dov'era
                overlays.place_inset(fx, *d["icenter"], W, H)
            elif fx["type"] == "zoom":
                # il riquadro ingrandito segue le proporzioni dell'area
                fx["bh"] = max(16, int(round(fx.get("bw", 100) * fx["h"] / fx["w"])))
            if fx["type"] == "pixelate" and o.get("track"):
                ddx, ddy = fx["x"] - o["x"], fx["y"] - o["y"]
                fx["track"] = [[k[0], k[1] + ddx, k[2] + ddy, *k[3:]] for k in o["track"]]
        self._on_edit(fx, False)

    def _release(self, event) -> None:
        d = self._drag
        self._drag = None
        if d is None:
            return
        if d["mode"] == "pan":
            self._pan_end(event)
            return
        if d["mode"] == "draw":
            self._rubber = None
            x0, y0 = d["start"]
            x1, y1 = event.x, event.y
            if abs(x1 - x0) < 4 and abs(y1 - y0) < 4 and self.mode != "arrow":
                self._redraw()
                return
            if self.mode == "arrow":
                ax, ay = self._to_project(x0, y0)
                bx, by = self._to_project(x1, y1)
                if math.hypot(bx - ax, by - ay) < 6:
                    bx, by = ax + 120, ay - 80
                self._on_draw("arrow", {"x1": int(ax), "y1": int(ay), "x2": int(bx), "y2": int(by)})
            else:
                ax, ay = self._to_project(min(x0, x1), min(y0, y1))
                bx, by = self._to_project(max(x0, x1), max(y0, y1))
                area = {"x": int(ax), "y": int(ay), "w": max(8, int(bx - ax)), "h": max(8, int(by - ay))}
                if self.mode == "zoom":
                    # secondo passo: un clic sceglie dove mettere il riquadro ingrandito
                    self.mode = "zoom_place"
                    self._zoom_area = (area["x"], area["y"], area["w"], area["h"])
                    self._ghost_at = self._to_project(event.x, event.y)
                    self._redraw()
                    return
                self._on_draw(self.mode, area)
            return
        if d["mode"].startswith("key_") and self.selected is not None:
            self._key_motion(d, self.selected, event, final=True)
            return
        if self.selected is not None:
            self._on_edit(self.selected, True)

    def _double(self, event) -> None:
        """Doppio clic su un testo: si riapre la finestra per scriverlo."""
        fx = self.selected
        if fx is not None and fx["type"] == "text" and self.on_edit_text is not None and not self.mode:
            x0, y0, x1, y1 = overlays.effect_bbox(fx)
            px, py = self._to_project(event.x, event.y)
            if x0 <= px <= x1 and y0 <= py <= y1:
                self._drag = None
                self.on_edit_text(fx)

    def _key_motion(self, d: dict, fx: dict, event, final: bool) -> None:
        """Nuova posizione (e misura, dagli angoli) della figura all'istante del keyframe."""
        px, py = self._to_project(event.x, event.y)
        dx, dy = px - d["start"][0], py - d["start"][1]
        mode = d["mode"][4:]
        cx, cy = d["center"]
        s = d["scale"]
        if mode in ("move", "p2"):
            cx, cy = cx + dx, cy + dy
        else:
            # dagli angoli: misura proporzionale, l'angolo opposto resta fermo
            x0, y0, w, h = d["rect"]
            ax = x0 + w if "w" in mode else x0
            ay = y0 + h if "n" in mode else y0
            ratio = max(0.1, abs(px - ax) / max(1.0, w))
            nw, nh = w * ratio, h * ratio
            cx = ax - nw / 2.0 if "w" in mode else ax + nw / 2.0
            cy = ay - nh / 2.0 if "n" in mode else ay + nh / 2.0
            s = s * ratio
        if self.on_key is not None:
            self.on_key(fx, d["t"], cx, cy, s, d["snap"], final)


def _copy_geometry(fx: dict) -> dict:
    out = {k: fx[k] for k in ("x", "y", "w", "h", "bx", "by", "bw", "bh", "x1", "y1", "x2", "y2") if k in fx}
    if fx.get("track"):
        out["track"] = [list(k) for k in fx["track"]]
    return out


def _segment_distance(px: float, py: float, x0: float, y0: float, x1: float, y1: float) -> float:
    dx, dy = x1 - x0, y1 - y0
    length2 = dx * dx + dy * dy
    if length2 <= 1e-9:
        return math.hypot(px - x0, py - y0)
    t = max(0.0, min(1.0, ((px - x0) * dx + (py - y0) * dy) / length2))
    return math.hypot(px - (x0 + t * dx), py - (y0 + t * dy))
