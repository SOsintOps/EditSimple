# EditSimple — montaggio video per presentazioni.  Copyright (C) 2026 Andrea Cumini <andrea@osintinfo.net>
# SPDX-License-Identifier: GPL-3.0-only
# GNU GPL v3 con termini aggiuntivi (attribuzione dell'autore): vedi LICENSE e NOTICE.
"""Screenshot del manuale: ricostruisce un progetto passo per passo e fotografa ogni passo.

Parte da un progetto di riferimento (un video, logo, zoom, freccia, riquadri e
pixelatura che seguono i soggetti, con i keyframe di correzione): lo rifa'
con gli strumenti del programma, uno alla volta, e alla fine lo rende identico
al riferimento (percorsi e keyframe compresi). Poi, sullo stesso video, mostra
le altre funzioni: slide, testo, immagine, tempo e fotogrammi, velocita',
tagli, fermo immagine, transizioni, tracce audio, anteprima ingrandita e
staccata, esportazione.

Le immagini vanno in <out>/<lingua>/NN_nome.webp (1600 px). Si lancia una volta per
lingua (la lingua dell'interfaccia e' quella della configurazione). La
finestra deve restare visibile e libera durante la ripresa: config.json viene
modificato (lingua, logo) e va salvato prima e rimesso dopo.

    .venv\\Scripts\\python.exe -X utf8 scripts\\manual_screenshots.py --lang it --video V.mp4 --logo logo.png
        --reference progetto.json --audio musica.wav --image fotogramma.png --out docs\\manual\\images
"""

from __future__ import annotations

import argparse
import copy
import json
import os
import sys
import time
import tkinter as tk
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from PIL import Image, ImageDraw, ImageGrab  # noqa: E402

HIGHLIGHT = (255, 159, 10)          # arancio: cio' di cui parla il manuale in quella figura

# testi d'esempio scritti nel video, nella lingua del manuale
DEMO = {
    "it": {"title": "Analisi del video", "subtitle": "Via pedonale - 19 secondi", "note": "Esempio: zoom sulle mani",
           "middle": "Secondo esempio", "end": "Fine", "evidence": "Fotogramma 150"},
    "en": {"title": "Video analysis", "subtitle": "Pedestrian street - 19 seconds", "note": "Example: zoom on the hands",
           "middle": "Second example", "end": "The end", "evidence": "Frame 150"},
    "de": {"title": "Videoanalyse", "subtitle": "Fußgängerzone - 19 Sekunden", "note": "Beispiel: Zoom auf die Hände",
           "middle": "Zweites Beispiel", "end": "Ende", "evidence": "Frame 150"},
    "fr": {"title": "Analyse de la vidéo", "subtitle": "Rue piétonne - 19 secondes", "note": "Exemple : zoom sur les mains",
           "middle": "Deuxième exemple", "end": "Fin", "evidence": "Image 150"},
    "es": {"title": "Análisis del vídeo", "subtitle": "Calle peatonal - 19 segundos", "note": "Ejemplo: zoom sobre las manos",
           "middle": "Segundo ejemplo", "end": "Fin", "evidence": "Fotograma 150"},
    "nl": {"title": "Video-analyse", "subtitle": "Voetgangersstraat - 19 seconden", "note": "Voorbeeld: zoom op de handen",
           "middle": "Tweede voorbeeld", "end": "Einde", "evidence": "Frame 150"},
    "pl": {"title": "Analiza nagrania", "subtitle": "Deptak - 19 sekund", "note": "Przykład: zbliżenie dłoni",
           "middle": "Drugi przykład", "end": "Koniec", "evidence": "Klatka 150"},
    "el": {"title": "Ανάλυση βίντεο", "subtitle": "Πεζόδρομος - 19 δευτερόλεπτα", "note": "Παράδειγμα: ζουμ στα χέρια",
           "middle": "Δεύτερο παράδειγμα", "end": "Τέλος", "evidence": "Καρέ 150"},
    "sq": {"title": "Analiza e videos", "subtitle": "Rrugë këmbësorësh - 19 sekonda", "note": "Shembull: zmadhim i duarve",
           "middle": "Shembulli i dytë", "end": "Fund", "evidence": "Kuadri 150"},
}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lang", required=True)
    ap.add_argument("--video", required=True)
    ap.add_argument("--logo", required=True)
    ap.add_argument("--reference", required=True)
    ap.add_argument("--audio", required=True)
    ap.add_argument("--image", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--work", default=None, help="cartella per progetto e video esportati")
    args = ap.parse_args()

    from editsimple.config import Config
    cfg = Config()
    cfg.set("language", args.lang)
    cfg.set("logo_path", os.path.abspath(args.logo))
    cfg.set("operator_text", "www.osintinfo.net")
    cfg.set("zoom_factor", 4)
    cfg.set("speed_clock", True)
    cfg.set("speed_last", 4)
    cfg.set("slide_seconds", 3.0)
    cfg.set("geometry", "")
    cfg.set("timeline_height", 215)              # piu' spazio all'anteprima negli screenshot
    cfg.save()

    from editsimple import app as appmod, overlays, widgets
    from editsimple.i18n import tr

    out = Path(args.out) / args.lang
    out.mkdir(parents=True, exist_ok=True)
    work = Path(args.work or (out / "_work"))
    work.mkdir(parents=True, exist_ok=True)
    ref = json.load(open(args.reference, encoding="utf-8"))
    ref_fx = {fx["type"] + (f"{i}" if fx["type"] == "box" else ""): fx
              for i, fx in enumerate(ref["effects"])}
    boxes = [fx for fx in ref["effects"] if fx["type"] == "box"]
    demo = DEMO.get(args.lang, DEMO["en"])

    app = appmod.App(None)
    app.geometry("1900x1020+8+4")
    app.attributes("-topmost", True)
    errors: list = []
    app.report_callback_exception = lambda *a: errors.append(a[1])

    def pump(seconds: float) -> None:
        end = time.time() + seconds
        while time.time() < end:
            app.update()
            time.sleep(0.005)

    # ------------------------------------------------------------------ fotografie

    def screen_box(widget) -> tuple[int, int, int, int]:
        x, y = widget.winfo_rootx(), widget.winfo_rooty()
        return x, y, x + widget.winfo_width(), y + widget.winfo_height()

    def settle(timeout: float = 8.0) -> None:
        """Aspetta che l'anteprima mostri il fotogramma vero (non nero) e che le miniature siano pronte."""
        end = time.time() + timeout
        while time.time() < end:
            pump(0.15)
            _i, clip, local = app.project.locate(app.playhead)
            if clip is None or clip["kind"] == "slide":
                break
            dw, dh = app.preview.display_size()
            source_t = app.project.source_time(clip, local) if clip["kind"] == "video" else float(clip.get("at", 0.0))
            if app.frames.get(clip["source"], source_t, fit=(dw, dh), cached_only=True) is None:
                continue
            app.refresh_preview()
            pump(0.2)
            image = app.preview._image
            if image is not None and max(image.convert("L").getextrema()) > 40:
                break
        thumbs = app.timeline._thumbs
        while time.time() < end + 4 and getattr(thumbs, "_wanted", None):
            pump(0.15)
        app.timeline.redraw()
        pump(0.5)

    def grab(name: str, marks=(), window=None, extra=(), wait: bool = True) -> None:
        """Fotografa la finestra (o la zona che comprende anche `extra`) ed evidenzia `marks`."""
        if wait:
            settle()
        extra = [w for w in extra if w.winfo_exists()]
        x0, y0, x1, y1 = screen_box(window or app)
        for w in extra:
            bx = screen_box(w)
            x0, y0, x1, y1 = min(x0, bx[0]), min(y0, bx[1]), max(x1, bx[2]), max(y1, bx[3])
        image = ImageGrab.grab((x0, y0, x1, y1))
        draw = ImageDraw.Draw(image)
        for mark in marks:
            bx = mark if isinstance(mark, tuple) else screen_box(mark)
            draw.rounded_rectangle((bx[0] - x0 - 5, bx[1] - y0 - 5, bx[2] - x0 + 5, bx[3] - y0 + 5),
                                   radius=8, outline=HIGHLIGHT, width=4)
        if image.width > 1600:                    # leggere nel repository, testo ancora nitido
            image = image.resize((1600, round(image.height * 1600 / image.width)), Image.LANCZOS)
        image.convert("RGB").save(out / f"{name}.webp", "WEBP", quality=88, method=6)
        print("  ", name, flush=True)

    def canvas_box(canvas, x0, y0, x1, y1) -> tuple[int, int, int, int]:
        """Rettangolo in coordinate della tela -> schermo."""
        ox = canvas.winfo_rootx() - int(canvas.canvasx(0))
        oy = canvas.winfo_rooty() - int(canvas.canvasy(0))
        return int(x0 + ox), int(y0 + oy), int(x1 + ox), int(y1 + oy)

    def preview_box(x, y, w, h) -> tuple[int, int, int, int]:
        p = app.preview
        a = p._to_canvas(x, y)
        b = p._to_canvas(x + w, y + h)
        return canvas_box(p.canvas, a[0], a[1], b[0], b[1])

    def fx_bar(fx) -> tuple[int, int, int, int]:
        c = app.timeline.tracks
        items = [i for i in c.find_withtag("fx") if fx["id"] in c.gettags(i)]
        bb = c.bbox(*items)
        return canvas_box(c, *bb)

    def reveal(widget):
        """Fa scorrere il pannello delle proprieta' finche' `widget` e' in vista; restituisce il widget."""
        if widget is None:
            return app.panel
        body = app.panel.body
        canvas = body._parent_canvas
        app.update_idletasks()
        inner_h = max(1, body.winfo_height())
        y = widget.winfo_rooty() - body.winfo_rooty()
        canvas.yview_moveto(max(0.0, (y - 40) / inner_h))
        pump(0.3)
        return widget

    def find_button(root, text):
        for child in root.winfo_children():
            try:
                if str(child.cget("text")).strip().endswith(text):
                    return child
            except (tk.TclError, ValueError, AttributeError):
                pass
            found = find_button(child, text)
            if found is not None:
                return found
        return None

    # ------------------------------------------------------------------ finestre modali

    seen: set = set()

    def dialogs():
        return [w for w in app.winfo_children()
                if isinstance(w, tk.Toplevel) and w.winfo_exists() and not w.overrideredirect()
                and w is not app.preview_window and not isinstance(w, widgets.ProgressDialog)]

    def on_dialog(handler, name: str | None = None, marks=lambda d: ()) -> None:
        """Alla prossima finestra di dialogo: fotografia (se `name`) e poi `handler(dialog)`."""
        def poll() -> None:
            fresh = [d for d in dialogs() if str(d) not in seen]
            if not fresh:
                app.after(80, poll)
                return
            dialog = fresh[-1]
            seen.add(str(dialog))
            dialog.attributes("-topmost", True)

            def act() -> None:
                if name:
                    grab(name, marks(dialog), extra=(dialog,))
                handler(dialog)
            app.after(700, act)
        app.after(80, poll)

    def fill_form(values: dict):
        def handler(d) -> None:
            for key, value in values.items():
                d._vars[key].set(value)
            d._ok()
        return handler

    def fill_text(text: str, size: int = 64, **extra):
        def handler(d) -> None:
            d.text.delete("1.0", "end")
            d.text.insert("1.0", text)
            d.size.set(str(size))
            for key, value in extra.items():
                getattr(d, key).set(value)
            d._ok()
        return handler

    def close(d) -> None:
        d.destroy()

    def wait_tracking(timeout: float = 120.0) -> None:
        pump(0.3)
        end = time.time() + timeout
        while time.time() < end and any(isinstance(w, widgets.ProgressDialog) for w in app.winfo_children()):
            pump(0.1)
        pump(0.4)

    def adopt(fx: dict, model: dict) -> None:
        """L'effetto diventa identico a quello del progetto di riferimento (percorso e keyframe compresi)."""
        keep = fx["id"]
        fx.clear()
        fx.update(copy.deepcopy(model))
        fx["id"] = keep
        if fx["type"] == "logo":
            fx["logo"] = os.path.abspath(args.logo)
        app.project.dirty = True
        app.refresh()

    files = {"open": None, "save": None}
    appmod.filedialog.askopenfilename = lambda **kw: files["open"] or ""
    appmod.filedialog.asksaveasfilename = lambda **kw: files["save"] or ""

    # ================================================================== parte 1: il progetto di riferimento
    pump(1.0)
    app.show_page("edit")
    grab("01_start", (app.tool_buttons["import"],))

    app.show_page("settings")
    pump(0.6)
    grab("02_settings")
    app.settings_scroll._parent_canvas.yview_moveto(1.0)
    pump(0.4)
    grab("03_settings_more")
    app.settings_scroll._parent_canvas.yview_moveto(0.0)
    app.show_page("edit")

    files["open"] = os.path.abspath(args.video)
    app.import_video()
    pump(1.5)
    app.seek(4.0)
    pump(0.8)
    grab("04_import", (app.tool_buttons["import"], app.timeline))

    # logo e operatore
    app.add_logo()
    pump(0.4)
    logo = app.project.effects[-1]
    adopt(logo, ref_fx["logo"])
    app.select("effect", logo["id"])
    grab("05_logo", (app.tool_buttons["logo"], preview_box(*overlays.effect_bbox(logo)[:2],
                                                          *(lambda b: (b[2] - b[0], b[3] - b[1]))(overlays.effect_bbox(logo)))))

    # zoom che segue le mani
    zref = ref_fx["zoom"]
    app.seek(zref["start"])
    app.start_draw("zoom")
    pump(0.3)
    app.preview.mode = "zoom_place"
    app.preview._zoom_area = (zref["x"], zref["y"], zref["w"], zref["h"])
    bx, by, bw, bh = overlays.inset_rect(zref, app.project.width, app.project.height)
    app.preview._ghost_at = (bx + bw / 2, by + bh / 2)
    app.preview._redraw()
    grab("06_zoom_place", (app.tool_buttons["zoom"], preview_box(zref["x"], zref["y"], zref["w"], zref["h"])))
    app._on_drawn("zoom", {"x": zref["x"], "y": zref["y"], "w": zref["w"], "h": zref["h"], "factor": zref["factor"],
                           "cx": int(bx + bw / 2), "cy": int(by + bh / 2)})
    pump(0.5)
    tracking = [w for w in app.winfo_children() if isinstance(w, widgets.ProgressDialog)]
    if tracking:
        tracking[0].attributes("-topmost", True)
        grab("07_tracking", extra=tracking, wait=False)
    wait_tracking()
    zoom = next(fx for fx in app.project.effects if fx["type"] == "zoom")
    adopt(zoom, zref)
    app.select("effect", zoom["id"])
    key_t = sorted(k[0] for k in zoom["keys"])[len(zoom["keys"]) // 2]
    app.seek(key_t)
    pump(0.6)
    grab("08_keyframes", (fx_bar(zoom), reveal(find_button(app.panel, tr("Keyframe")))))

    # freccia che segue una persona
    aref = ref_fx["arrow"]
    app.seek(aref["start"])
    app._on_drawn("arrow", {"x1": aref["x1"], "y1": aref["y1"], "x2": aref["x2"], "y2": aref["y2"]})
    pump(0.3)
    arrow = app.project.effects[-1]
    app.retrack(arrow)
    pump(0.3)
    dx, dy, tw, th = aref["target"]
    a0 = app.preview._to_canvas(aref["x2"] + dx, aref["y2"] + dy)
    a1 = app.preview._to_canvas(aref["x2"] + dx + tw, aref["y2"] + dy + th)
    app.preview._rubber = (a0[0], a0[1], a1[0], a1[1])
    app.preview._redraw()
    grab("09_arrow_target", (app.mode_label,))
    app._on_drawn("arrow_target", {"x": aref["x2"] + dx, "y": aref["y2"] + dy, "w": tw, "h": th})
    wait_tracking()
    adopt(arrow, aref)
    app.select("effect", arrow["id"])
    app.seek(6.0)
    pump(0.6)
    grab("10_arrow_follow", (fx_bar(arrow),))

    # riquadri che seguono due persone
    for n, bref in enumerate(boxes):
        app.seek(bref["start"])
        pump(0.3)
        app._on_drawn("box", {"x": bref["x"], "y": bref["y"], "w": bref["w"], "h": bref["h"]})
        pump(0.4)
        box = app.project.effects[-1]
        if n == 0:
            grab("11_box", (reveal(find_button(app.panel, tr("Segui il soggetto"))),
                            preview_box(bref["x"], bref["y"], bref["w"], bref["h"])))
        app.retrack(box)
        wait_tracking()
        adopt(box, bref)

    # pixelatura ovale sul volto
    pref = ref_fx["pixelate"]
    app.seek(pref["start"])
    pump(0.3)
    app.start_draw("pixelate_oval")
    on_dialog(fill_form({"end": f"{pref['end']:.2f}", "block": str(pref["block"])}), "12_pixel_form")
    app._on_drawn("pixelate", {"x": pref["x"], "y": pref["y"], "w": pref["w"], "h": pref["h"]})
    wait_tracking()
    pixel = next(fx for fx in app.project.effects if fx["type"] == "pixelate")
    adopt(pixel, pref)
    app.select("effect", pixel["id"])
    app.seek(18.9)
    pump(0.6)
    grab("13_pixelate", (fx_bar(pixel), app.tool_buttons["pixelo"]))

    files["save"] = str(work / "progetto_manuale.json")
    app.save_project_as()
    pump(0.3)

    # ================================================================== parte 2: le altre funzioni
    # occhio: un effetto nascosto mentre si lavora
    app.select(None, None)
    first_box = next(fx for fx in app.project.effects if fx["type"] == "box")
    app.toggle_effect_visible(first_box["id"])
    app.seek(first_box["start"] + 1.0)
    pump(0.5)
    eye = fx_bar(first_box)
    grab("14_hide", ((eye[0], eye[1], eye[0] + 24, eye[3]),))
    app.toggle_effect_visible(first_box["id"])

    # anteprima ingrandita (Ctrl+rotellina)
    app.seek(5.0)
    pump(0.5)
    zx, zy, zw, zh = zref["x"], zref["y"], zref["w"], zref["h"]
    cx, cy = app.preview._to_canvas(zx + zw / 2, zy + zh / 2)
    app.preview.zoom_view(3.0, cx, cy)
    pump(1.2)
    grab("15_preview_zoom", (app.preview,))
    app.preview.reset_view()
    pump(0.6)

    # anteprima staccata
    app.toggle_preview_window()
    pump(1.5)
    win = app.preview_window
    win.attributes("-topmost", True)
    win.geometry(f"760x470+{app.winfo_rootx() + 820}+{app.winfo_rooty() + 120}")
    pump(1.2)
    grab("16_detached", (find_button(app.preview, "") or app.preview,), extra=(win,))
    app.toggle_preview_window()
    pump(1.0)

    # slide di apertura: titolo, sottotitolo e logo sopra
    app.seek(0.0)
    on_dialog(fill_form({"seconds": "3"}), "17_slide_form")
    app.add_slide()
    pump(0.6)
    on_dialog(fill_text(demo["title"] + "\n" + demo["subtitle"], 96), "18_text_form")
    app.seek(0.0)
    app.start_draw("text")
    app._on_drawn("text", {"x": app.project.width // 2, "y": app.project.height // 2})
    pump(0.6)
    text_fx = app.project.effects[-1]
    if text_fx["type"] == "text":
        app._center_fx(text_fx, "x")
        app._center_fx(text_fx, "y")
        app.refresh()
    app.seek(1.5)
    pump(0.6)
    grab("19_slide_opening", (app.tool_buttons["slide"], app.tool_buttons["text"]))

    # slide in mezzo e di chiusura
    app.seek(11.0)
    pump(0.3)
    on_dialog(fill_form({"role": tr("Al cursore ({time})").format(time=appmod.media.format_time(app.playhead)),
                         "seconds": "2"}))
    app.add_slide()
    pump(0.5)
    on_dialog(fill_text(demo["middle"], 96))
    app.start_draw("text")
    app._on_drawn("text", {"x": app.project.width // 2, "y": app.project.height // 2})
    pump(0.4)
    mid_text = app.project.effects[-1]
    app._center_fx(mid_text, "x")
    app._center_fx(mid_text, "y")
    on_dialog(fill_form({"role": tr("Chiusura (alla fine)"), "seconds": "2"}))
    app.add_slide()
    pump(0.5)
    on_dialog(fill_text(demo["end"], 120))
    app.start_draw("text")
    app._on_drawn("text", {"x": app.project.width // 2, "y": app.project.height // 2})
    pump(0.4)
    end_text = app.project.effects[-1]
    app._center_fx(end_text, "x")
    app._center_fx(end_text, "y")
    app.refresh()
    app.select(None, None)
    app.timeline.zoom_fit()
    app.seek(12.0)
    pump(0.8)
    grab("20_slides", (app.timeline,))

    # testo sopra il video e immagine (un fotogramma come prova)
    app.seek(5.0)
    on_dialog(fill_text(demo["note"], 60))
    app.start_draw("text")
    app._on_drawn("text", {"x": 420, "y": 120})
    pump(0.5)
    note_fx = app.project.effects[-1]
    files["open"] = os.path.abspath(args.image)
    app.seek(5.0)
    app.add_image()
    pump(0.4)
    image_fx = app.project.effects[-1]
    image_fx["w"] = 300
    image_fx["x"], image_fx["y"] = 60, 300
    image_fx["radius"] = 8.0
    app.refresh()
    app.select("effect", image_fx["id"])
    pump(0.6)
    grab("21_text_image", (app.tool_buttons["text"], app.tool_buttons["image"],
                           preview_box(*overlays.effect_bbox(note_fx)[:2], *(lambda b: (b[2] - b[0], b[3] - b[1]))(overlays.effect_bbox(note_fx)))))

    # tempo trascorso e numero del fotogramma
    app.select(None, None)
    app.seek(3.5)
    app.start_draw("timer")
    W, H = app.project.width, app.project.height
    app._on_drawn("timer", {"x": W - 130, "y": H - 150})          # in basso a destra, sopra il numero del fotogramma
    pump(0.4)
    app.start_draw("frames")
    app._on_drawn("frames", {"x": W - 130, "y": H - 70})
    pump(0.4)
    app.select("effect", app.project.effects[-1]["id"])
    app.seek(6.0)
    pump(0.6)
    grab("22_timer_frames", (app.tool_buttons["timer"], app.tool_buttons["frames"]))

    # velocita': porzione IN-OUT accelerata con l'orologio
    app.select(None, None)
    app.seek(14.0)
    app.mark_in_here()
    app.seek(17.0)
    app.mark_out_here()
    pump(0.4)
    on_dialog(fill_form({"speed": "4x", "clock": True}), "23_speed_form")
    app.set_speed()
    pump(0.6)
    app.seek(14.4)
    pump(0.8)
    grab("24_speed", (app.tool_buttons["speed"],))
    app.clear_marks()

    # taglio e fermo immagine
    app.seek(8.0)
    app.split_at_playhead()
    pump(0.3)
    on_dialog(fill_form({"seconds": "1.5"}))
    app.add_freeze()
    pump(0.5)
    app.seek(8.2)
    pump(0.5)
    grab("25_cut_freeze", (app.tool_buttons["cut"], app.tool_buttons["freeze"]))

    # transizioni: la prima clip compare dal nero e sfuma nella successiva
    index, clip, _l = app.project.locate(4.0)
    clip["fade_in"] = 0.0
    clip["xfade"] = 0.8
    app.project.dirty = True
    app.refresh()
    app.select("clip", clip["id"])
    pump(0.5)
    grab("26_transitions", (reveal(find_button(app.panel, tr("Fusione con la succ. (s)"))),))

    # traccia audio con entrata e uscita graduali
    app.seek(3.0)
    files["open"] = os.path.abspath(args.audio)
    app.add_audio()
    pump(0.6)
    track = app.project.audio_tracks[-1]
    track["fade_in"] = 2.0
    track["fade_out"] = 3.0
    track["volume"] = 0.8
    app.project.dirty = True
    app.refresh()
    app.select("audio", track["id"])
    pump(0.6)
    grab("27_audio", (app.tool_buttons["audio"],))

    # esportazione
    app.select(None, None)
    files["save"] = str(work / "video_manuale.mp4")
    on_dialog(close, "29_export_done")
    app.export()
    shot = False
    end = time.time() + 600
    while time.time() < end:
        pump(0.2)
        progress = [w for w in app.winfo_children() if isinstance(w, widgets.ProgressDialog)]
        if progress:
            progress[0].attributes("-topmost", True)
        if progress and not shot and progress[0]._bar.get() > 0.15:
            grab("28_export", extra=progress, wait=False)
            shot = True
        if not progress and os.path.exists(files["save"]) and os.path.getsize(files["save"]) > 0 and shot:
            break
    pump(2.0)

    # lingua
    app.show_page("settings")
    pump(0.6)
    app.settings_scroll._parent_canvas.yview_moveto(1.0)
    pump(0.4)
    grab("30_language", (app._language_buttons[args.lang],))

    print("errori Tk:", errors or "nessuno", flush=True)
    app.project.dirty = False
    app.destroy()
    return 0


if __name__ == "__main__":
    sys.exit(main())
