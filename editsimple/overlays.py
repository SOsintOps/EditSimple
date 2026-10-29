# EditSimple — montaggio video per presentazioni.  Copyright (C) 2026 Andrea Cumini <andrea@osintinfo.net>
# SPDX-License-Identifier: GPL-3.0-only
# GNU GPL v3 con termini aggiuntivi (attribuzione dell'autore): vedi LICENSE e NOTICE.
"""Disegno delle sovraimpressioni e composizione del fotogramma.

Tutto cio' che si vede sopra il video (testo, riquadri, frecce, orologio) e'
disegnato con Pillow in immagini RGBA: l'anteprima le sovrappone al fotogramma
e l'esportazione le passa a ffmpeg come PNG per il filtro overlay. Cosi'
l'anteprima coincide con il risultato. Le coordinate sono sempre in pixel del
progetto (la misura del video finale).
"""

from __future__ import annotations

import json
import math
import os
import re
from typing import Iterable

from PIL import Image, ImageChops, ImageDraw, ImageFilter

from . import fonts
from .i18n import N_

SS = 2  # sovracampionamento per i disegni vettoriali (riquadri, frecce, orologio)

_cache: dict[str, tuple[Image.Image, int, int]] = {}


def hex_to_rgb(color: str) -> tuple[int, int, int]:
    color = (color or "#ffffff").lstrip("#")
    if len(color) != 6:
        return 255, 255, 255
    return int(color[0:2], 16), int(color[2:4], 16), int(color[4:6], 16)


def rgba(color: str, alpha: float = 1.0) -> tuple[int, int, int, int]:
    r, g, b = hex_to_rgb(color)
    return r, g, b, int(round(max(0.0, min(1.0, alpha)) * 255))


# ----------------------------------------------------------- adattamento

def fit_transform(src_w: int, src_h: int, width: int, height: int) -> tuple[float, float, float]:
    """(scala, offset x, offset y) con cui il fotogramma sorgente entra nel progetto (lettera-box)."""
    if src_w <= 0 or src_h <= 0:
        return 1.0, 0.0, 0.0
    scale = min(width / src_w, height / src_h)
    return scale, (width - src_w * scale) / 2.0, (height - src_h * scale) / 2.0


def fit_frame(image: Image.Image, width: int, height: int) -> Image.Image:
    """Fotogramma scalato a misura del progetto, con bande nere se le proporzioni differiscono."""
    if image.size == (width, height):
        return image
    scale, ox, oy = fit_transform(image.width, image.height, width, height)
    w = max(1, int(round(image.width * scale)))
    h = max(1, int(round(image.height * scale)))
    resized = image.resize((w, h), Image.BILINEAR)
    if (w, h) == (width, height):
        return resized
    canvas = Image.new("RGB", (width, height), (0, 0, 0))
    canvas.paste(resized, (int(round(ox)), int(round(oy))))
    return canvas


# ----------------------------------------------------------- testo

def _text_key(fx: dict) -> str:
    keys = ("text", "font", "size", "color", "bg", "bg_color", "bg_alpha", "bg_radius", "shadow", "align")
    return "text:" + json.dumps({k: fx.get(k) for k in keys}, sort_keys=True)


def render_text(fx: dict) -> tuple[Image.Image, int, int]:
    """Immagine RGBA del testo (con eventuale fondo) e la sua posizione in alto a sinistra."""
    key = _text_key(fx)
    hit = _cache.get(key)
    if hit is not None:
        return hit[0], int(fx["x"]), int(fx["y"])
    text = str(fx.get("text") or " ")
    size = max(6, int(fx.get("size", 48)))
    font = fonts.load_font(fx.get("font") or fonts.default_font(), size)
    align = fx.get("align", "left")
    pad = int(round(size * 0.35)) if fx.get("bg") else int(round(size * 0.15))
    probe = ImageDraw.Draw(Image.new("RGBA", (4, 4)))
    spacing = int(round(size * 0.25))
    bbox = probe.multiline_textbbox((0, 0), text, font=font, spacing=spacing, align=align)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    # le misure del carattere possono avere la virgola: la tela vuole interi
    width, height = int(math.ceil(tw + 2 * pad + 2)), int(math.ceil(th + 2 * pad + 2))
    image = Image.new("RGBA", (max(1, width), max(1, height)), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    if fx.get("bg"):
        radius = int(round(min(width, height) * max(0.0, min(50.0, float(fx.get("bg_radius", 25.0)))) / 100))
        draw.rounded_rectangle((0, 0, width - 1, height - 1), radius=radius,
                               fill=rgba(fx.get("bg_color", "#000000"), float(fx.get("bg_alpha", 0.6))))
    origin = (pad - bbox[0] + 1, pad - bbox[1] + 1)
    if fx.get("shadow", True):
        shadow = Image.new("RGBA", image.size, (0, 0, 0, 0))
        off = max(1, size // 18)
        ImageDraw.Draw(shadow).multiline_text((origin[0] + off, origin[1] + off), text, font=font,
                                              fill=(0, 0, 0, 200), spacing=spacing, align=align)
        shadow = shadow.filter(ImageFilter.GaussianBlur(max(1, size / 20)))
        image.alpha_composite(shadow)
        draw = ImageDraw.Draw(image)
    draw.multiline_text(origin, text, font=font, fill=rgba(fx.get("color", "#FFFFFF")),
                        spacing=spacing, align=align)
    _remember(key, image)
    return image, int(fx["x"]), int(fx["y"])


# ----------------------------------------------------------- riquadro e freccia

def _vector_key(kind: str, fx: dict, keys: Iterable[str]) -> str:
    return kind + ":" + json.dumps({k: fx.get(k) for k in keys}, sort_keys=True)


def render_box(fx: dict) -> tuple[Image.Image, int, int]:
    """Riquadro con bordo (e riempimento facoltativo); l'immagine comprende il bordo."""
    key = _vector_key("box", fx, ("w", "h", "color", "thickness", "fill", "fill_alpha", "radius"))
    thick = max(1, int(fx.get("thickness", 4)))
    margin = thick
    hit = _cache.get(key)
    if hit is None:
        w, h = max(2, int(fx["w"])), max(2, int(fx["h"]))
        radius = round_px(w, h, fx.get("radius", 0))
        big = Image.new("RGBA", ((w + 2 * margin) * SS, (h + 2 * margin) * SS), (0, 0, 0, 0))
        draw = ImageDraw.Draw(big)
        box = (margin * SS, margin * SS, (margin + w) * SS - 1, (margin + h) * SS - 1)
        fill = rgba(fx.get("color", "#FF0000"), float(fx.get("fill_alpha", 0.25))) if fx.get("fill") else None
        draw.rounded_rectangle(box, radius=radius * SS, fill=fill,
                               outline=rgba(fx.get("color", "#FF0000")), width=thick * SS)
        image = big.resize((w + 2 * margin, h + 2 * margin), Image.LANCZOS)
        _remember(key, image)
    else:
        image = hit[0]
    return image, int(fx["x"]) - margin, int(fx["y"]) - margin


def render_oval(fx: dict) -> tuple[Image.Image, int, int]:
    """Ellisse inscritta nel rettangolo (x, y, w, h), con bordo e riempimento facoltativo."""
    key = _vector_key("oval", fx, ("w", "h", "color", "thickness", "fill", "fill_alpha"))
    thick = max(1, int(fx.get("thickness", 4)))
    margin = thick
    hit = _cache.get(key)
    if hit is None:
        w, h = max(2, int(fx["w"])), max(2, int(fx["h"]))
        big = Image.new("RGBA", ((w + 2 * margin) * SS, (h + 2 * margin) * SS), (0, 0, 0, 0))
        draw = ImageDraw.Draw(big)
        box = (margin * SS, margin * SS, (margin + w) * SS - 1, (margin + h) * SS - 1)
        fill = rgba(fx.get("color", "#FF0000"), float(fx.get("fill_alpha", 0.25))) if fx.get("fill") else None
        draw.ellipse(box, fill=fill, outline=rgba(fx.get("color", "#FF0000")), width=thick * SS)
        image = big.resize((w + 2 * margin, h + 2 * margin), Image.LANCZOS)
        _remember(key, image)
    else:
        image = hit[0]
    return image, int(fx["x"]) - margin, int(fx["y"]) - margin


def render_arrow(fx: dict) -> tuple[Image.Image, int, int]:
    """Freccia da (x1, y1) a (x2, y2) con la punta in (x2, y2)."""
    x1, y1, x2, y2 = (float(fx[k]) for k in ("x1", "y1", "x2", "y2"))
    thick = max(1, int(fx.get("thickness", 6)))
    head = thick * 3 + 10
    margin = head + thick
    x0, y0 = int(math.floor(min(x1, x2))) - margin, int(math.floor(min(y1, y2))) - margin
    key = _vector_key("arrow", fx, ("color", "thickness")) + f":{x1 - x0:.1f},{y1 - y0:.1f},{x2 - x0:.1f},{y2 - y0:.1f}"
    hit = _cache.get(key)
    if hit is not None:
        return hit[0], x0, y0
    w = int(math.ceil(abs(x2 - x1))) + 2 * margin
    h = int(math.ceil(abs(y2 - y1))) + 2 * margin
    big = Image.new("RGBA", (max(1, w * SS), max(1, h * SS)), (0, 0, 0, 0))
    draw = ImageDraw.Draw(big)
    color = rgba(fx.get("color", "#FF0000"))
    ax, ay, bx, by = (x1 - x0) * SS, (y1 - y0) * SS, (x2 - x0) * SS, (y2 - y0) * SS
    length = math.hypot(bx - ax, by - ay)
    if length < 1:
        draw.ellipse((bx - thick * SS, by - thick * SS, bx + thick * SS, by + thick * SS), fill=color)
    else:
        ux, uy = (bx - ax) / length, (by - ay) / length
        hl = min(head * SS, length * 0.6)
        tip_x, tip_y = bx, by
        base_x, base_y = bx - ux * hl, by - uy * hl
        draw.line((ax, ay, base_x + ux * thick * SS * 0.5, base_y + uy * thick * SS * 0.5),
                  fill=color, width=thick * SS)
        draw.ellipse((ax - thick * SS / 2, ay - thick * SS / 2, ax + thick * SS / 2, ay + thick * SS / 2), fill=color)
        hw = hl * 0.55
        draw.polygon([(tip_x, tip_y), (base_x - uy * hw, base_y + ux * hw), (base_x + uy * hw, base_y - ux * hw)],
                     fill=color)
    image = big.resize((w, h), Image.LANCZOS)
    _remember(key, image)
    return image, x0, y0


# ----------------------------------------------------------- logo e testo dell'operatore

# Etichette da mostrare con tr(): chi confronta la scelta deve farlo sulle etichette tradotte.
LOGO_LAYOUTS = {"right": N_("Testo a destra del logo"), "left": N_("Testo a sinistra del logo"),
                "below": N_("Testo sotto il logo")}
_logo_files: dict[str, Image.Image] = {}


def load_logo(path: str) -> Image.Image | None:
    """L'immagine del logo in RGBA (None se manca); ricaricata se il file cambia."""
    if not path:
        return None
    try:
        stamp = f"{path}|{os.path.getmtime(path)}"
    except OSError:
        return None
    image = _logo_files.get(stamp)
    if image is None:
        try:
            with Image.open(path) as src:
                image = src.convert("RGBA")
        except (OSError, ValueError):
            return None
        if len(_logo_files) > 8:
            _logo_files.clear()
        _logo_files[stamp] = image
    return image


def render_logo(fx: dict) -> tuple[Image.Image, int, int]:
    """Logo (largo `w` pixel, proporzioni originali) con accanto o sotto il testo dell'operatore."""
    path = fx.get("logo") or ""
    try:
        stamp = os.path.getmtime(path) if path else 0
    except OSError:
        stamp = -1
    key = _vector_key("logo", fx, ("logo", "w", "text", "size", "color", "layout", "shadow", "font",
                                   "bg", "bg_color", "bg_alpha", "bg_radius")) + f"|{stamp}"
    hit = _cache.get(key)
    if hit is not None:
        return hit[0], int(fx["x"]), int(fx["y"])
    logo = load_logo(path)
    if logo is not None:
        w = max(4, int(round(float(fx.get("w") or 200))))
        h = max(1, int(round(logo.height * w / max(1, logo.width))))
        logo = logo.resize((w, h), Image.LANCZOS)
    label = None
    text = str(fx.get("text") or "").strip()
    if text:
        label = render_text({"text": text, "size": fx.get("size", 40), "color": fx.get("color", "#FFFFFF"),
                             "font": fx.get("font"), "shadow": fx.get("shadow", True), "bg": False,
                             "align": "center" if fx.get("layout") == "below" else "left", "x": 0, "y": 0})[0]
    if logo is None and label is None:
        image = Image.new("RGBA", (8, 8), (0, 0, 0, 0))
    elif label is None:
        image = logo
    elif logo is None:
        image = label
    else:
        size = max(6, int(fx.get("size", 40)))
        layout = fx.get("layout", "right")
        if layout == "below":
            gap = int(round(size * 0.15))
            width, height = max(logo.width, label.width), logo.height + gap + label.height
            image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
            image.alpha_composite(logo, ((width - logo.width) // 2, 0))
            image.alpha_composite(label, ((width - label.width) // 2, logo.height + gap))
        else:
            gap = int(round(size * 0.4))
            width, height = logo.width + gap + label.width, max(logo.height, label.height)
            image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
            lx = 0 if layout == "right" else label.width + gap
            tx = logo.width + gap if layout == "right" else 0
            image.alpha_composite(logo, (lx, (height - logo.height) // 2))
            image.alpha_composite(label, (tx, (height - label.height) // 2))
    if fx.get("bg"):
        # sfondo colorato sotto logo e scritta, con margine e angoli arrotondati (radius in % del lato corto)
        size = max(6, int(fx.get("size", 40)))
        pad = max(4, int(round(size * 0.45)))
        w, h = image.width + 2 * pad, image.height + 2 * pad
        radius = int(round(min(w, h) * max(0.0, min(50.0, float(fx.get("bg_radius", 25)))) / 100))
        big = Image.new("RGBA", (w * SS, h * SS), (0, 0, 0, 0))
        ImageDraw.Draw(big).rounded_rectangle((0, 0, w * SS - 1, h * SS - 1), radius=radius * SS,
                                              fill=rgba(fx.get("bg_color", "#000000"), float(fx.get("bg_alpha", 0.5))))
        back = big.resize((w, h), Image.LANCZOS)
        back.alpha_composite(image, (pad, pad))
        image = back
    _remember(key, image)
    return image, int(fx["x"]), int(fx["y"])


SLIDE_FITS = {"cover": N_("Riempi (taglia i bordi)"), "contain": N_("Intera (bande del colore)"), "stretch": N_("Stira")}


def render_slide(clip: dict, width: int, height: int) -> Image.Image:
    """La slide: colore di fondo ed eventuale immagine di sfondo adattata alla misura del video.

    Testi e immagini si mettono sopra con gli effetti.
    """
    width, height = max(2, int(width)), max(2, int(height))
    path = clip.get("bg_image") or ""
    source = load_logo(path) if path else None
    if source is None:
        return Image.new("RGB", (width, height), hex_to_rgb(clip.get("bg") or "#000000"))
    fit = clip.get("bg_fit") or "cover"
    key = f"slidebg:{path}|{os.path.getmtime(path)}|{fit}|{clip.get('bg')}|{width}x{height}"
    hit = _cache.get(key)
    if hit is not None:
        return hit[0]
    image = Image.new("RGB", (width, height), hex_to_rgb(clip.get("bg") or "#000000"))
    if fit == "stretch":
        layer = source.resize((width, height), Image.LANCZOS)
        image.paste(layer, (0, 0), layer)
    else:
        k = max(width / source.width, height / source.height) if fit == "cover" else min(width / source.width, height / source.height)
        w, h = max(1, int(round(source.width * k))), max(1, int(round(source.height * k)))
        layer = source.resize((w, h), Image.LANCZOS)
        image.paste(layer, ((width - w) // 2, (height - h) // 2), layer)   # centrata (fuori quadro si taglia)
    _remember(key, image)
    return image


def render_image(fx: dict) -> tuple[Image.Image, int, int]:
    """Immagine (PNG, JPG...) larga `w` pixel con le sue proporzioni, con l'opacita' scelta."""
    path = fx.get("image") or ""
    try:
        stamp = os.path.getmtime(path) if path else 0
    except OSError:
        stamp = -1
    key = _vector_key("image", fx, ("image", "w", "opacity", "radius")) + f"|{stamp}"
    hit = _cache.get(key)
    if hit is not None:
        return hit[0], int(fx["x"]), int(fx["y"])
    source = load_logo(path)
    if source is None:
        image = Image.new("RGBA", (max(8, int(fx.get("w") or 8)), max(8, int(fx.get("w") or 8) // 2)), (128, 128, 128, 90))
    else:
        w = max(4, int(round(float(fx.get("w") or source.width))))
        h = max(1, int(round(source.height * w / max(1, source.width))))
        image = source.resize((w, h), Image.LANCZOS)
        radius = int(round(min(w, h) * max(0.0, min(50.0, float(fx.get("radius", 0.0)))) / 100))
        if radius > 0:
            # angoli arrotondati: maschera sovracampionata moltiplicata per la trasparenza dell'immagine
            big = Image.new("L", (w * SS, h * SS), 0)
            ImageDraw.Draw(big).rounded_rectangle((0, 0, w * SS - 1, h * SS - 1), radius=radius * SS, fill=255)
            mask = big.resize((w, h), Image.LANCZOS)
            image = image.copy()
            image.putalpha(ImageChops.multiply(image.getchannel("A"), mask))
        alpha = max(0.0, min(1.0, float(fx.get("opacity", 1.0))))
        if alpha < 1.0:
            image = image.copy()
            image.putalpha(image.getchannel("A").point(lambda v: int(v * alpha)))
    _remember(key, image)
    return image, int(fx["x"]), int(fx["y"])


# ----------------------------------------------------------- tempo trascorso

TIMER_FORMATS = {"mmss": N_("minuti:secondi (01:23)"), "hhmmss": N_("ore:minuti:secondi (00:01:23)"),
                 "mmss_d": N_("con i decimi (01:23.4)")}
TIMER_ORIGINS = {"video": N_("dall'inizio del video"), "effect": N_("dall'inizio dell'effetto")}
TIMER_TYPES = ("timer", "frames")     # tempo trascorso e numero del fotogramma: stesso disegno e stessa esportazione


def timer_step(fx: dict) -> float:
    """Ogni quanto cambia la scritta: un secondo, un decimo con i decimi, un fotogramma per il contatore."""
    if fx.get("type") == "frames":
        return 1.0 / max(1.0, float(fx.get("fps") or 25))
    return 0.1 if fx.get("format") == "mmss_d" else 1.0


def timer_label(fx: dict, t: float) -> str:
    """La scritta del tempo trascorso all'istante t (timeline), con l'eventuale testo davanti."""
    origin = float(fx.get("start", 0.0)) if fx.get("origin") == "effect" else 0.0
    v = max(0.0, t - origin) + 1e-6
    fmt = fx.get("format", "mmss")
    if fx.get("type") == "frames":
        # numero del fotogramma della timeline (il primo e' 0, o 1 se si conta da uno)
        body = str(int(v * max(1.0, float(fx.get("fps") or 25)) + 1e-4) + int(fx.get("first", 0)))
    elif fmt == "hhmmss":
        body = f"{int(v // 3600):02d}:{int(v % 3600 // 60):02d}:{int(v % 60):02d}"
    elif fmt == "mmss_d":
        tenths = int(v * 10)
        body = f"{tenths // 600 % 60:02d}:{tenths // 10 % 60:02d}.{tenths % 10}"
        if v >= 3600:                     # oltre l'ora compaiono le ore (1:00:00.0)
            body = f"{int(v // 3600)}:{body}"
    else:
        body = f"{int(v // 60 % 60):02d}:{int(v % 60):02d}"
        if v >= 3600:
            body = f"{int(v // 3600)}:{body}"
    prefix = str(fx.get("prefix") or "").strip()
    return f"{prefix} {body}" if prefix else body


def timer_template(fx: dict) -> str:
    """La scritta piu' lunga dell'effetto con le cifre a zero: fissa la misura dello sfondo."""
    return re.sub(r"\d", "0", timer_label(fx, float(fx.get("end", 0.0))))


def render_timer(fx: dict, t: float) -> tuple[Image.Image, int, int]:
    """Il tempo trascorso come un testo, su uno sfondo di misura fissa (non cambia a ogni secondo)."""
    label = timer_label(fx, t)
    template = timer_template(fx)
    key = _vector_key("timer", fx, ("size", "color", "font", "shadow", "bg", "bg_color", "bg_alpha", "bg_radius",
                                    "prefix", "format", "type")) + f"|{label}|{template}"
    hit = _cache.get(key)
    if hit is not None:
        return hit[0], int(fx["x"]), int(fx["y"])
    box_w, box_h = render_text(dict(fx, text=template, align="center", bg=True))[0].size
    text = render_text(dict(fx, text=label, align="center", bg=False))[0]
    w, h = max(box_w, text.width), max(box_h, text.height)
    image = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    if fx.get("bg"):
        radius = int(round(min(w, h) * max(0.0, min(50.0, float(fx.get("bg_radius", 25.0)))) / 100))
        ImageDraw.Draw(image).rounded_rectangle((0, 0, w - 1, h - 1), radius=radius,
                                                fill=rgba(fx.get("bg_color", "#000000"), float(fx.get("bg_alpha", 0.55))))
    image.alpha_composite(text, ((w - text.width) // 2, (h - text.height) // 2))
    _remember(key, image)
    return image, int(fx["x"]), int(fx["y"])


def with_opacity(image: Image.Image, alpha: float) -> Image.Image:
    if alpha >= 0.999:
        return image
    faded = image.copy()
    faded.putalpha(image.getchannel("A").point(lambda v: int(v * max(0.0, alpha))))
    return faded


def corner_position(image: Image.Image, corner: str, width: int, height: int, margin: int) -> tuple[int, int]:
    """Angolo in alto a sinistra per mettere l'immagine nell'angolo scelto, a `margin` pixel dai bordi."""
    if corner == "center":
        return (width - image.width) // 2, (height - image.height) // 2
    x = margin if "left" in corner else width - image.width - margin
    y = margin if "top" in corner else height - image.height - margin
    return int(x), int(y)


def render_effect(fx: dict) -> tuple[Image.Image, int, int] | None:
    """La sovraimpressione disegnata, con la sua opacita' (l'immagine la applica da se')."""
    rendered = _render_effect(fx)
    alpha = float(fx.get("opacity", 1.0))
    if rendered is None or fx.get("type") == "image" or alpha >= 0.999:
        return rendered
    image, x, y = rendered
    faded = image.copy()            # copia: l'originale resta nella cache dei disegni
    faded.putalpha(image.getchannel("A").point(lambda v: int(v * max(0.0, alpha))))
    return faded, x, y


def _render_effect(fx: dict) -> tuple[Image.Image, int, int] | None:
    kind = fx.get("type")
    if kind == "text":
        return render_text(fx)
    if kind == "box":
        return render_box(fx)
    if kind == "oval":
        return render_oval(fx)
    if kind == "arrow":
        return render_arrow(fx)
    if kind == "logo":
        return render_logo(fx)
    if kind == "image":
        return render_image(fx)
    return None


STATIC_TYPES = ("text", "box", "oval", "arrow", "logo", "image")   # sovraimpressioni disegnate come immagini


def anchor_of(fx: dict) -> tuple[float, float]:
    """Il punto della figura che segue il soggetto: la punta per la freccia, l'angolo in alto a sinistra per le altre."""
    if fx.get("type") == "arrow":
        return float(fx["x2"]), float(fx["y2"])
    return float(fx.get("x", 0)), float(fx.get("y", 0))


SCALE_STEP = 1.06      # gradino di misura delle figure che crescono o calano con l'oggetto
SCALED_TYPES = ("box", "oval", "zoom", "pixelate")   # figure che cambiano misura con l'oggetto


def scale_level(s: float) -> int:
    """Il gradino di SCALE_STEP appena sopra la scala s (0 = misura originale)."""
    return int(math.ceil(math.log(max(s, 1e-3)) / math.log(SCALE_STEP) - 1e-6))


def quant_scale(s: float) -> float:
    """Scala arrotondata al gradino superiore: anteprima ed esportazione usano le stesse misure, e la
    figura e' sempre appena piu' grande dell'oggetto."""
    return SCALE_STEP ** scale_level(s)


def displaced(fx: dict, t: float) -> dict:
    """La figura spostata (e ingrandita o ridotta) dove la porta l'inseguimento all'istante t.

    Le chiavi di `track` sono il riquadro di partenza centrato sull'oggetto,
    con la sua scala; la geometria salvata corrisponde alla prima chiave.
    Riquadri, ovali e area dello zoom crescono e calano attorno al centro;
    il riquadro ingrandito dello zoom resta della sua misura (`iw`, `ih`).
    """
    keys = fx.get("track")
    if not keys or fx.get("type") == "pixelate":
        return fx
    ax, ay, s = track_state(fx, t)
    dx, dy = ax - float(keys[0][1]), ay - float(keys[0][2])
    sq = quant_scale(s) if fx.get("type") in SCALED_TYPES else 1.0
    if abs(dx) < 0.5 and abs(dy) < 0.5 and sq == 1.0:
        return fx
    out = dict(fx)
    if fx.get("type") == "arrow":
        for key in ("x1", "x2"):
            out[key] = fx[key] + dx
        for key in ("y1", "y2"):
            out[key] = fx[key] + dy
    else:
        w0, h0 = float(fx.get("w", 0)), float(fx.get("h", 0))
        out["x"] = fx["x"] + dx - w0 * (sq - 1) / 2.0
        out["y"] = fx["y"] + dy - h0 * (sq - 1) / 2.0
        if sq != 1.0:
            out["w"], out["h"] = w0 * sq, h0 * sq
            if fx.get("type") == "zoom":
                out["iw"], out["ih"] = fx.get("iw", w0), fx.get("ih", h0)
    return out


def effect_bbox(fx: dict) -> tuple[float, float, float, float]:
    """Rettangolo (x0, y0, x1, y1) occupato dall'effetto, in pixel del progetto."""
    kind = fx.get("type")
    if kind in TIMER_TYPES:
        image, x, y = render_timer(fx, float(fx.get("start", 0.0)))
        return x, y, x + image.width, y + image.height
    if kind in ("text", "logo", "image"):
        image, x, y = {"text": render_text, "logo": render_logo, "image": render_image}[kind](fx)
        return x, y, x + image.width, y + image.height
    if kind == "arrow":
        return (min(fx["x1"], fx["x2"]), min(fx["y1"], fx["y2"]),
                max(fx["x1"], fx["x2"]), max(fx["y1"], fx["y2"]))
    if kind == "pixelate":
        x, y = fx.get("x", 0), fx.get("y", 0)
        return x, y, x + fx["w"], y + fx["h"]
    return fx["x"], fx["y"], fx["x"] + fx["w"], fx["y"] + fx["h"]


def _remember(key: str, image: Image.Image) -> None:
    if len(_cache) > 96:
        _cache.clear()
    _cache[key] = (image, 0, 0)


# ----------------------------------------------------------- orologio

MINUTE_PERIOD = 1.0     # secondi per un giro della lancetta dei minuti
CLOCK_LOOP = 12.0       # dopo 12 giri dei minuti anche la lancetta delle ore ha fatto un giro


def clock_image(size: int, t: float, color: str, label: str, bg_alpha: float = 0.5,
                radius: float = 18.0) -> Image.Image:
    """Orologio con le lancette all'istante t e, sotto, la scritta della velocita' (es. "4x"),
    su un quadrato nero trasparente (opacita' bg_alpha, angoli arrotondati: radius % del lato)."""
    size = max(24, int(size))
    rgb = hex_to_rgb(color)
    pad = max(4, int(round(size * 0.14)))           # margine dentro il quadrato
    gap = max(2, int(round(size * 0.08)))           # spazio fra orologio e scritta
    font = fonts.load_font(fonts.default_font(), max(8, int(size * 0.36))) if label else None
    if label:
        # la scritta si misura davvero (ascendenti e discendenti), cosi' non viene tagliata
        x0, y0, x1, y1 = font.getbbox(label)
        text_w, text_h = x1 - x0, y1 - y0
    else:
        x0 = y0 = text_w = text_h = 0
    content_w = max(size, text_w)
    content_h = size + (gap + text_h if label else 0)
    side = max(content_w, content_h) + 2 * pad      # quadrato
    big = Image.new("RGBA", (side * SS, side * SS), (0, 0, 0, 0))
    draw = ImageDraw.Draw(big)
    draw.rounded_rectangle((0, 0, side * SS - 1, side * SS - 1),
                           radius=int(side * SS * max(0.0, min(50.0, float(radius))) / 100),
                           fill=(0, 0, 0, int(round(255 * max(0.0, min(1.0, float(bg_alpha)))))))
    top = (side - content_h) / 2.0
    cx, cy = side * SS / 2.0, (top + size / 2.0) * SS
    r = size * SS / 2.0 * 0.92
    ring = max(2, int(size * SS / 16))
    draw.ellipse((cx - r, cy - r, cx + r, cy + r), outline=rgb + (255,), width=ring)
    for i in range(12):
        ang = math.radians(i * 30 - 90)
        inner = r * (0.74 if i % 3 == 0 else 0.82)
        width = max(1, int(size * SS / (22 if i % 3 == 0 else 40)))
        draw.line((cx + math.cos(ang) * inner, cy + math.sin(ang) * inner,
                   cx + math.cos(ang) * r * 0.9, cy + math.sin(ang) * r * 0.9), fill=rgb + (255,), width=width)
    minute = (t / MINUTE_PERIOD) * 2 * math.pi - math.pi / 2
    hour = (t / (MINUTE_PERIOD * 12.0)) * 2 * math.pi - math.pi / 2
    for ang, length, width in ((hour, 0.5, size * SS / 11), (minute, 0.76, size * SS / 17)):
        draw.line((cx - math.cos(ang) * r * 0.12, cy - math.sin(ang) * r * 0.12,
                   cx + math.cos(ang) * r * length, cy + math.sin(ang) * r * length),
                  fill=rgb + (255,), width=max(2, int(width)))
    dot = max(2, int(size * SS / 14))
    draw.ellipse((cx - dot, cy - dot, cx + dot, cy + dot), fill=rgb + (255,))
    image = big.resize((side, side), Image.LANCZOS)
    if label:
        # la scritta alla misura finale (piu' nitida che rimpicciolita)
        d = ImageDraw.Draw(image)
        tx = (side - text_w) / 2.0 - x0
        ty = top + size + gap - y0
        d.text((tx, ty), label, font=font, fill=rgb + (255,))
    return image


def speed_label(speed) -> str:
    return f"{float(speed):g}x"


def clock_position(width: int, height: int, clock: dict, image: Image.Image) -> tuple[int, int]:
    margin = int(clock.get("margin", 24))
    corner = clock.get("corner", "top-right")
    x = margin if "left" in corner else width - image.width - margin
    y = margin if "top" in corner else height - image.height - margin
    if corner == "center":
        x, y = (width - image.width) // 2, (height - image.height) // 2
    return x, y


# ----------------------------------------------------------- zoom e pixelatura

def zoom_rect(fx: dict, width: int, height: int) -> tuple[int, int, int, int]:
    """L'area ingrandita (sorgente), dentro il fotogramma e con misure pari."""
    w = max(8, min(int(fx["w"]), width))
    h = max(8, min(int(fx["h"]), height))
    w -= w % 2
    h -= h % 2
    x = max(0, min(int(fx["x"]), width - w))
    y = max(0, min(int(fx["y"]), height - h))
    return x, y, w, h


ZOOM_FACTORS = (2, 3, 4, 6, 8, 10, 12, 14, 16)


def inset_rect(fx: dict, width: int, height: int) -> tuple[int, int, int, int]:
    """Il riquadro in cui l'area ingrandita viene mostrata, dentro il fotogramma e con misure pari.

    Con `factor` (2, 3, 4) il contenuto del riquadro e' l'area ingrandita di
    quel fattore (ridotto se non ci sta nel fotogramma); senza, la misura e'
    quella salvata in `bw`/`bh` (progetti precedenti).
    """
    x, y, w, h = zoom_rect(fx, width, height)
    if fx.get("iw"):
        # area ingrandita o ridotta dall'inseguimento: il riquadro resta quello dell'area di partenza
        x, y, w, h = zoom_rect(dict(fx, w=fx["iw"], h=fx["ih"]), width, height)
    if fx.get("factor"):
        t = zoom_border(fx)
        f = float(fx["factor"])
        bw, bh = w * f + 2 * t, h * f + 2 * t
        k = min(1.0, width / bw, height / bh)
        bw, bh = max(16, int(bw * k)), max(16, int(bh * k))
    else:
        bw = max(16, min(int(fx.get("bw") or width * 0.42), width))
        bh = max(16, min(int(fx.get("bh") or bw * h / max(1, w)), height))
    bw -= bw % 2
    bh -= bh % 2
    bx = max(0, min(int(fx.get("bx", width - bw - 24)), width - bw))
    by = max(0, min(int(fx.get("by", 24)), height - bh))
    return bx, by, bw, bh


def place_inset(fx: dict, cx: float | None, cy: float | None, width: int, height: int) -> None:
    """Mette il riquadro ingrandito centrato in (cx, cy), dentro il fotogramma; senza punto, nell'angolo
    piu' lontano dall'area."""
    _x, _y, bw, bh = inset_rect(dict(fx, bx=0, by=0), width, height)
    if cx is None or cy is None:
        margin = max(12, width // 60)
        ax, ay = fx.get("x", 0) + fx.get("w", 0) / 2, fx.get("y", 0) + fx.get("h", 0) / 2
        cx = margin + bw / 2 if ax > width / 2 else width - margin - bw / 2
        cy = margin + bh / 2 if ay > height / 2 else height - margin - bh / 2
    fx["bx"] = int(round(max(0, min(cx - bw / 2, width - bw))))
    fx["by"] = int(round(max(0, min(cy - bh / 2, height - bh))))


def inset_center(fx: dict, width: int, height: int) -> tuple[float, float]:
    bx, by, bw, bh = inset_rect(fx, width, height)
    return bx + bw / 2, by + bh / 2


def zoom_border(fx: dict) -> int:
    return max(1, int(fx.get("thickness", 4)))


def round_px(w: float, h: float, pct) -> int:
    """Raggio degli angoli in pixel: pct (0..50) % del lato corto."""
    return int(round(min(w, h) * max(0.0, min(50.0, float(pct or 0.0))) / 100))


def rounded_mask(w: int, h: int, r: int) -> Image.Image:
    """Maschera del rettangolo w x h con angoli di raggio r: la stessa formula di rounded_alpha (export)."""
    import numpy as np
    r = max(0, min(int(r), w // 2, h // 2))
    ys, xs = np.mgrid[0:h, 0:w]
    dx = np.maximum(np.abs(xs + 0.5 - w / 2.0) - (w / 2.0 - r), 0)
    dy = np.maximum(np.abs(ys + 0.5 - h / 2.0) - (h / 2.0 - r), 0)
    return Image.fromarray(((dx * dx + dy * dy <= r * r) * 255).astype("uint8"), "L")


def rounded_alpha(r: int) -> str:
    """Espressione di alfa per il filtro geq di ffmpeg: angoli arrotondati di raggio r (come rounded_mask)."""
    r = max(0, int(r))
    return (f"255*lte(pow(max(abs(X+0.5-W/2)-(W/2-{r}),0),2)+pow(max(abs(Y+0.5-H/2)-(H/2-{r}),0),2),{r * r})")


def apply_zoom(image: Image.Image, fx: dict) -> Image.Image:
    """Disegna il riquadro ingrandito dentro al fotogramma (e il contorno dell'area, se richiesto)."""
    width, height = image.size
    x, y, w, h = zoom_rect(fx, width, height)
    bx, by, bw, bh = inset_rect(fx, width, height)
    t = zoom_border(fx)
    color = rgba(fx.get("color", "#FFFFFF"))
    region = image.crop((x, y, x + w, y + h)).resize((max(1, bw - 2 * t), max(1, bh - 2 * t)), Image.BICUBIC)
    draw = ImageDraw.Draw(image)
    draw_zoom_decor(draw, fx, (x, y, w, h), (bx, by, bw, bh))
    if fx.get("shape") == "oval":
        # riquadro ovale: il contenuto dentro un'ellisse, con l'anello del bordo sopra
        image.paste(region, (bx + t, by + t), oval_mask(region.width, region.height))
        ring = zoom_ring(fx, bw, bh)
        image.paste(ring, (bx, by), ring)
        return image
    if zoom_round(fx, bw, bh) > 0:
        # riquadro con gli angoli arrotondati: contenuto con la maschera, bordo sopra
        image.paste(region, (bx + t, by + t), rounded_mask(region.width, region.height, max(0, zoom_round(fx, bw, bh) - t)))
        ring = zoom_ring(fx, bw, bh)
        image.paste(ring, (bx, by), ring)
        return image
    draw.rectangle((bx, by, bx + bw - 1, by + bh - 1), fill=color)
    image.paste(region, (bx + t, by + t))
    return image


def oval_mask(w: int, h: int) -> Image.Image:
    """Maschera dell'ellisse inscritta in w x h: la stessa formula del filtro geq dell'esportazione."""
    import numpy as np
    ys, xs = np.mgrid[0:h, 0:w]
    inside = ((xs + 0.5 - w / 2.0) / (w / 2.0)) ** 2 + ((ys + 0.5 - h / 2.0) / (h / 2.0)) ** 2 <= 1.0
    return Image.fromarray((inside * 255).astype("uint8"), "L")


def zoom_round(fx: dict, bw: int, bh: int) -> int:
    """Raggio degli angoli del riquadro ingrandito rettangolare (0 = angoli vivi)."""
    return 0 if fx.get("shape") == "oval" else round_px(bw, bh, fx.get("radius", 0))


def zoom_ring(fx: dict, bw: int, bh: int) -> Image.Image:
    """Bordo del riquadro ingrandito ovale o con gli angoli arrotondati (bw x bh, spessore del bordo), RGBA."""
    t = zoom_border(fx)
    r = zoom_round(fx, bw, bh)
    key = _vector_key("zring", fx, ("color", "thickness", "shape")) + f"|{bw}x{bh}|{t}|{r}"
    hit = _cache.get(key)
    if hit is not None:
        return hit[0]
    big = Image.new("RGBA", (bw * SS, bh * SS), (0, 0, 0, 0))
    if fx.get("shape") == "oval":
        ImageDraw.Draw(big).ellipse((0, 0, bw * SS - 1, bh * SS - 1), outline=rgba(fx.get("color", "#FFFFFF")),
                                    width=max(1, int(t * SS * 1.15)))
    else:
        ImageDraw.Draw(big).rounded_rectangle((0, 0, bw * SS - 1, bh * SS - 1), radius=r * SS,
                                              outline=rgba(fx.get("color", "#FFFFFF")), width=max(1, int(t * SS)))
    image = big.resize((bw, bh), Image.LANCZOS)
    _remember(key, image)
    return image


def zoom_line_width(fx: dict) -> int:
    """Spessore del contorno sull'area e della linea che la unisce al riquadro ingrandito."""
    return max(2, int(round(zoom_border(fx) * 0.75)))


def zoom_link(area: tuple, inset: tuple, oval: bool = False) -> tuple[float, float, float, float] | None:
    """Il tratto della retta fra i centri di area e riquadro che sta fuori da entrambi (None se si toccano).

    Con `oval` area e riquadro sono ellissi: la retta si ferma sul loro bordo.
    """
    ax, ay, aw, ah = area
    bx, by, bw, bh = inset
    cax, cay = ax + aw / 2.0, ay + ah / 2.0
    cbx, cby = bx + bw / 2.0, by + bh / 2.0
    dx, dy = cbx - cax, cby - cay
    if abs(dx) < 1e-6 and abs(dy) < 1e-6:
        return None

    def reach(hw: float, hh: float) -> float:
        # frazione di (dx, dy) per uscire da un rettangolo (o da un'ellisse) di semiassi hw, hh dal centro
        if oval:
            return 1.0 / math.sqrt((dx / max(hw, 1e-6)) ** 2 + (dy / max(hh, 1e-6)) ** 2)
        return min(hw / abs(dx) if abs(dx) > 1e-6 else math.inf, hh / abs(dy) if abs(dy) > 1e-6 else math.inf)

    sa, sb = reach(aw / 2.0, ah / 2.0), reach(bw / 2.0, bh / 2.0)
    if sa + sb >= 1.0:
        return None
    return cax + dx * sa, cay + dy * sa, cbx - dx * sb, cby - dy * sb


def draw_zoom_decor(draw: ImageDraw.ImageDraw, fx: dict, area: tuple, inset: tuple,
                    offset: tuple[float, float] = (0.0, 0.0)) -> None:
    """Contorno colorato sull'oggetto ingrandito e linea che lo unisce al riquadro dello zoom."""
    color = rgba(fx.get("color", "#FFFFFF"))
    lw = zoom_line_width(fx)
    ox, oy = offset
    x, y, w, h = area
    oval = fx.get("shape") == "oval"
    if fx.get("outline", True):
        if oval:
            draw.ellipse((x - ox, y - oy, x + w - 1 - ox, y + h - 1 - oy), outline=color, width=lw)
        else:
            draw.rounded_rectangle((x - ox, y - oy, x + w - 1 - ox, y + h - 1 - oy), radius=round_px(w, h, fx.get("radius", 0)),
                                   outline=color, width=lw)
    if fx.get("link", True):
        seg = zoom_link(area, inset, oval)
        if seg is not None:
            x0, y0, x1, y1 = seg
            draw.line((x0 - ox, y0 - oy, x1 - ox, y1 - oy), fill=color, width=lw)


def key_scale(key) -> float:
    """Scala di un punto dell'inseguimento (1 per i punti salvati prima che la misura seguisse l'oggetto)."""
    return float(key[3]) if len(key) > 3 else 1.0


def track_state(fx: dict, t: float) -> tuple[float, float, float]:
    """(x, y, scala) all'istante t, interpolando i punti dell'inseguimento.

    x, y e' l'angolo del riquadro di partenza centrato sul soggetto; la scala
    e' relativa a quella del primo punto (che corrisponde a w e h salvati).
    """
    keys = fx.get("track") or []
    if not keys:
        return float(fx.get("x", 0)), float(fx.get("y", 0)), 1.0
    s0 = key_scale(keys[0]) or 1.0
    if t <= keys[0][0]:
        return float(keys[0][1]), float(keys[0][2]), 1.0
    if t >= keys[-1][0]:
        return float(keys[-1][1]), float(keys[-1][2]), key_scale(keys[-1]) / s0
    lo, hi = 0, len(keys) - 1
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if keys[mid][0] <= t:
            lo = mid
        else:
            hi = mid
    a, b = keys[lo], keys[hi]
    if b[0] - a[0] <= 1e-9:
        return float(a[1]), float(a[2]), key_scale(a) / s0
    k = (t - a[0]) / (b[0] - a[0])
    sa, sb = key_scale(a), key_scale(b)
    return (float(a[1] + (b[1] - a[1]) * k), float(a[2] + (b[2] - a[2]) * k), (sa + (sb - sa) * k) / s0)


def base_key(fx: dict) -> list[float]:
    """La chiave che corrisponde alla figura com'e' salvata (all'inizio dell'effetto)."""
    if fx.get("type") == "arrow":
        return [float(fx["start"]), float(fx["x2"]), float(fx["y2"]), 1.0]
    return [float(fx["start"]), float(fx.get("x", 0)), float(fx.get("y", 0)), 1.0]


def key_for(fx: dict, t: float, cx: float, cy: float, s_rel: float) -> list[float]:
    """La chiave del percorso che mette la figura con il centro in (cx, cy) e scala s_rel all'istante t.

    Per la freccia (cx, cy) e' la punta. La scala e' relativa alla misura salvata.
    """
    keys = fx.get("track") or [base_key(fx)]
    k0 = keys[0]
    s_abs = round(max(0.05, s_rel) * key_scale(k0), 4)
    if fx.get("type") == "arrow":
        return [t, round(float(k0[1]) + cx - float(fx["x2"]), 1), round(float(k0[2]) + cy - float(fx["y2"]), 1), 1.0]
    w0, h0 = float(fx.get("w", 0)), float(fx.get("h", 0))
    if fx.get("type") == "pixelate":
        return [t, round(cx - w0 / 2.0, 1), round(cy - h0 / 2.0, 1), s_abs]
    return [t, round(float(k0[1]) + cx - w0 / 2.0 - float(fx["x"]), 1),
            round(float(k0[2]) + cy - h0 / 2.0 - float(fx["y"]), 1), s_abs]


def figure_center(fx: dict, t: float) -> tuple[float, float, float]:
    """Centro (la punta per la freccia) e scala relativa della figura all'istante t."""
    if fx.get("type") == "arrow":
        g = displaced(fx, t)
        return float(g["x2"]), float(g["y2"]), 1.0
    x, y, s = track_state(fx, t) if fx.get("track") else (float(fx.get("x", 0)), float(fx.get("y", 0)), 1.0)
    w0, h0 = float(fx.get("w", 0)), float(fx.get("h", 0))
    if fx.get("type") == "pixelate":
        return x + w0 / 2.0, y + h0 / 2.0, s
    k0 = (fx.get("track") or [base_key(fx)])[0]
    return float(fx["x"]) + x - float(k0[1]) + w0 / 2.0, float(fx["y"]) + y - float(k0[2]) + h0 / 2.0, s


def pixelate_position(fx: dict, t: float) -> tuple[float, float]:
    """Posizione (angolo del riquadro di partenza centrato sul soggetto) all'istante t."""
    x, y, _s = track_state(fx, t)
    return x, y


def pixelate_rect(fx: dict, t: float, width: int, height: int) -> tuple[int, int, int, int]:
    """Il riquadro pixelato all'istante t; puo' sporgere dal fotogramma (il soggetto sta uscendo).

    Cresce e cala con l'oggetto (scala dell'inseguimento), restando centrato su di lui.
    """
    x, y, s = track_state(fx, t)
    s = quant_scale(s)
    w0, h0 = float(fx["w"]), float(fx["h"])
    x -= w0 * (s - 1) / 2.0
    y -= h0 * (s - 1) / 2.0
    w = max(4, min(int(round(w0 * s)), width))
    h = max(4, min(int(round(h0 * s)), height))
    x = int(round(max(-w, min(x, width))))
    y = int(round(max(-h, min(y, height))))
    return x, y, w, h


def apply_pixelate(image: Image.Image, fx: dict, t: float) -> Image.Image:
    width, height = image.size
    x, y, w, h = pixelate_rect(fx, t, width, height)
    block = max(2, int(fx.get("block", 16)))
    region = image.crop((x, y, x + w, y + h))   # fuori dal fotogramma PIL mette nero, come il pad di ffmpeg
    small = region.resize((max(1, math.ceil(w / block)), max(1, math.ceil(h / block))), Image.BOX)
    coarse = small.resize((w, h), Image.NEAREST)
    if fx.get("shape") == "oval":
        mask = Image.new("L", (w, h), 0)
        ImageDraw.Draw(mask).ellipse((0, 0, w - 1, h - 1), fill=255)
        image.paste(coarse, (x, y), mask)
    elif round_px(w, h, fx.get("radius", 0)) > 0:
        image.paste(coarse, (x, y), rounded_mask(w, h, round_px(w, h, fx.get("radius", 0))))
    else:
        image.paste(coarse, (x, y))
    return image


# ----------------------------------------------------------- composizione

def compose(project, t: float, base: Image.Image, clip: dict | None, scale: float = 1.0) -> Image.Image:
    """Il fotogramma finito all'istante t: adattamento, pixelatura, zoom, sovraimpressioni, orologio.

    `scale` < 1 compone a risoluzione ridotta (anteprima): tutte le coordinate
    vengono scalate di conseguenza.
    """
    width, height = project.width, project.height
    if scale != 1.0:
        width = max(2, int(round(width * scale)))
        height = max(2, int(round(height * scale)))
    frame = fit_frame(base, width, height)
    if frame is base:
        frame = base.copy()
    active = project.effects_at(t)
    for fx in active:
        if fx["type"] == "pixelate":
            frame = apply_pixelate(frame, _scaled(fx, scale), t)
    for fx in active:
        if fx["type"] == "zoom":
            frame = apply_zoom(frame, _scaled(displaced(fx, t), scale))
    for fx in active:
        if fx["type"] in TIMER_TYPES:
            image, x, y = render_timer(_scaled(fx, scale), t)
            image = with_opacity(image, float(fx.get("opacity", 1.0)))
            frame.paste(image, (int(x), int(y)), image)
            continue
        if fx["type"] in STATIC_TYPES:
            rendered = render_effect(_scaled(displaced(fx, t), scale))
            if rendered is not None:
                image, x, y = rendered
                frame.paste(image, (int(x), int(y)), image)
    if clip is not None and clip.get("kind") == "video" and clip.get("clock") and abs(float(clip.get("speed", 1)) - 1) > 1e-9:
        cfg = dict(project.clock)
        cfg["size"] = max(12, int(cfg.get("size", 160) * scale))
        cfg["margin"] = int(cfg.get("margin", 24) * scale)
        image = clock_image(cfg["size"], t, cfg.get("color", "#FFFFFF"), speed_label(clip["speed"]),
                            float(cfg.get("bg_alpha", 0.5)), float(cfg.get("radius", 18.0)))
        x, y = clock_position(width, height, cfg, image)
        frame.paste(image, (x, y), image)
    return frame


def _scaled(fx: dict, scale: float) -> dict:
    if scale == 1.0:
        return fx
    out = dict(fx)
    for key in ("x", "y", "w", "h", "iw", "ih", "bx", "by", "bw", "bh", "x1", "y1", "x2", "y2", "size", "thickness"):
        if key in out:
            out[key] = out[key] * scale
    if "block" in out:
        out["block"] = max(2, out["block"] * scale)
    if out.get("track"):
        out["track"] = [[k[0], k[1] * scale, k[2] * scale, *k[3:]] for k in out["track"]]
    for key in ("size", "thickness"):
        if key in out:
            out[key] = max(1, int(round(out[key])))
    return out
