# EditSimple

**English** · [Italiano](README.it.md)

A simple video editor made to build presentations from one or more videos and
to **explain a fact or show evidence**: a film-strip timeline with a video
track and audio tracks, cuts, freeze frames, fast forward or slow motion with a
clock, overlays (text, images, boxes, ovals, arrows) that can follow a subject,
a fixed logo and operator text, a zoom in a magnified box and a rectangular or
oval pixelation that follows a subject (a face, an object, a plate) and grows
as it comes closer. Where the tracking goes wrong, dragging the figure back
onto the subject creates a keyframe that corrects the path. The result is
exported to MP4 with ffmpeg. A project is a JSON file.

**Author: Andrea Cumini — [www.osintinfo.net](https://www.osintinfo.net) — andrea@osintinfo.net**

EditSimple is one of the tools of [Seity](https://www.seity.com), the author's
main project: the interface is written in CustomTkinter, with Seity's dark theme.

## User manual

The **user manual**, with screenshots of every feature, is in
[docs/manual](docs/manual/README.md) in 9 languages:
[English](docs/manual/manual.en.md) · [Italiano](docs/manual/manual.it.md) · [Deutsch](docs/manual/manual.de.md) · [Français](docs/manual/manual.fr.md) · [Español](docs/manual/manual.es.md) · [Nederlands](docs/manual/manual.nl.md) · [Polski](docs/manual/manual.pl.md) · [Ελληνικά](docs/manual/manual.el.md) · [Shqip](docs/manual/manual.sq.md).
This README covers installation, structure and how the program works inside.

The interface is available in the same 9 languages and can be switched at any
time, without restarting, from the *Language* box of the **Configure** page.

## Download

The standalone program for Windows 10/11 (64-bit) is on the
[Releases](https://github.com/tingon11/EditSimple/releases) page: unzip it
anywhere and run `EditSimple.exe`. Python is not needed.

## Requirements (from source)

- Windows 10/11 (64-bit). The program also runs on other systems, but the
  window without title bar and the automatic download of ffmpeg are Windows only.
- Python 3.11 with `tkinter`.
- The packages in `requirements.txt`: `customtkinter`, `pillow`, `numpy`,
  `opencv-python-headless`.
- **ffmpeg**, a separate program (see below): not included.

## Installation

```bash
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
```

The virtualenv must be created with the Python of this PC: if
`.venv\pyvenv.cfg` points to an interpreter that does not exist, the program
does not start (`No Python at ...`). In that case fix the `home` line or
recreate the virtualenv.

## Start

```bash
.venv\Scripts\python.exe EditSimple.py [project.json | video.mp4]
```

or double-click `Avvia.bat` (it uses `pythonw.exe`, without a console). A
project to open or a video to import can be passed as argument.

### Linux

Tested on Ubuntu 24.04 (X11) and Debian 13 (GNOME on Wayland, through XWayland). Install Tk, venv and ffmpeg with the package manager, create the virtualenv and start the program with `avvia.sh`:

```bash
sudo apt install python3-tk python3-venv ffmpeg
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
./avvia.sh [project.json | video.mp4]
```

`avvia.sh` uses `.venv/bin/python` when it exists, otherwise `python3`. ffmpeg is looked for in `tools/ffmpeg/ffmpeg` and then in the PATH; the **Download / Update** button works on Windows only. If the distribution's ffmpeg is older than 7 (Ubuntu 24.04 ships 6.1), a static release build can go in `tools/ffmpeg/ffmpeg`. The audio preview uses the first system player found among `pw-cat`, `paplay`, `aplay` and `ffplay`; without any of them the preview is silent. On Linux and macOS the alignment between sound and picture in the preview depends on the start delay of the system player: a fixed estimate per player is applied (about 0.15 s for `pw-cat` and `paplay`), so a small offset can remain.

## FFmpeg

ffmpeg is not included: it is a separate program with its own license and it
is neither in the package nor in the executable. It is looked for in
`tools\ffmpeg\ffmpeg.exe` next to the program and then in the PATH. At first
start, if it is not found, the **Configure** page opens: **Download / Update**
fetches the official Windows build ("release essentials") from
<https://www.gyan.dev/ffmpeg/builds/>, the one listed on the FFmpeg website,
and keeps only `ffmpeg.exe`, `LICENSE` and `README.txt` in `tools\ffmpeg\`. No
installation, no change to the PATH. The `tools\` folder is excluded from the
repository (`.gitignore`) and from the build.

A **release** of ffmpeg is needed (7.x or later, tested with 9.0.2). Avoid
development snapshots: the January 2024 one (`N-113347`) truncates the video at
the end of the first segment when the `concat` filter gets several inputs, and
the export comes out incomplete.

## VitTrack (tracking)

Tracking uses template matching and, when available, the help of
**VitTrack**: a trained model (vision transformer) from the official
[opencv_zoo](https://github.com/opencv/opencv_zoo/tree/main/models/object_tracking_vittrack)
repository, run by OpenCV itself. The two work together: when the template
match is confident it is right (and puts VitTrack back on the subject if it got
lost); when it is not confident or no longer finds the subject, for instance
behind a pole where it would stay stuck on the background, VitTrack is followed
and the template restarts from there. VitTrack alone is not enough: on a face
or on a box that contains little it drifts away, while template matching holds.
Like ffmpeg it is not included: on the **Configure** page, box
*Tracking (VitTrack)*, **Download** fetches the model (about 0.7 MB, checked
against its SHA-256 fingerprint) and its license into `tools\vittrack\`. The
model's license is **Apache 2.0**, compatible with the program's GPL 3 (the FSF
considers it compatible with GPL 3, not with GPL 2); in any case the model is
not distributed with the program. Without the model only template matching
(`cv2.matchTemplate`) remains, which behind an obstacle may stay stuck on the
background.

## Workflow

1. **Import video** (Ctrl+I). The first video sets size and frame rate of the
   project (the following ones are fitted with black bars if their aspect
   ratio differs). The imported file is split into its channels: the clip goes
   on the **Video** track, shown as a film strip of frames (zooming the
   timeline with Ctrl+wheel goes down to the single frame), and its audio
   appears on the **Original audio** track, which always follows the same
   cuts. Further videos are added at the end or at the cursor (the program
   asks).
2. **Move the cursor** by clicking the ruler, with ← → (one frame), Ctrl+← →
   (ten frames), Shift+← → (one second), Home/End, or by typing the time in
   the box. Space plays with sound, Shift+Space plays backwards (without sound).
3. **Mark IN and OUT** (keys I and O, or the buttons) to select a portion.
   - **Delete** (Del) removes the IN–OUT portion: what follows moves back.
   - **Cut** (S) splits the clip at the cursor; clips are **reordered by
     dragging** them on the timeline (effects stay at their time).
   - **Speed** (V) applies to the IN–OUT portion (or to the selected clip) a
     fast forward of 2x, 4x, 8x, 16x or 32x or a **slow motion** of 0.5x or
     0.25x, optionally showing a **clock icon** with turning hands and the
     speed written below. The timeline gets shorter or longer accordingly
     (the audio slows down too); 1x goes back to normal speed. Size, position
     and colour of the clock are set in the clip's panel.
4. **Freeze** (F): the frame at the cursor stays still for N seconds; what
   follows moves forward.
5. **Slide**: a slide at the start, at the cursor or at the end, with a solid
   colour or a background image fitted to the video; texts and images are put
   on top with the Text and Image tools.
6. **Audio**: adds a track (commentary, music) at the cursor. Every track has
   a name, position, portion of the file, **volume**, mute and **fades** in and
   out; it is moved by dragging it. A white line shows the volume on every
   track. Clicking the *Original audio* row name selects the whole original
   audio (volume, fades, removal); with IN and OUT marked, Del removes only
   the audio of that stretch. Transitions (from black, to black, cross-fade
   with the next clip) are in the clip's panel.
7. **Overlays**: press **Text** (T), **Image**, **Box** (R), **Oval** (E) or
   **Arrow** (A) and draw on the preview (a click for the text, a drag for the
   figures). The effect starts at the cursor and lasts the seconds set in
   Configure; start and end are changed in the panel or by dragging the bar on
   the timeline (the right edge changes the duration). In the panel: text on
   several lines, **font** (a picker that shows every font), size, colour,
   alignment, shadow, background with opacity and rounded corners; colour,
   thickness and fill of boxes, ovals and arrows. On the preview the selected
   item is moved by dragging it and resized from its handles (arrows from
   their two ends). **Time** and **Frames** write the elapsed time or the frame
   number where you click.
   - **Follow the subject**: boxes, ovals and arrows can track what they frame
     (the content of the figure is the template; for the arrow a rectangle is
     drawn around the subject and the tip stays on it). Where the tracking is
     wrong, drag the figure onto the subject: a **keyframe** is created, the
     path is corrected and tracking restarts from there. Boxes and ovals grow
     and shrink with the subject when it comes closer or moves away. If a
     moving subject disappears behind something, the figure goes on at its
     speed for up to 1.5 s waiting for it to reappear. If the subject leaves
     the frame, the figure follows it out at its speed and then the effect
     ends; if the subject is lost, the effect ends there. **Repeat tracking
     from the cursor** restarts from the current position; **Stop following**
     makes the figure still.
8. **Zoom** (Z): in two steps. Drag a rectangle over the object to magnify;
   then the **magnified box** with the real content appears under the mouse,
   and a click places it there. The magnification goes from **2x to 16x**: it
   is chosen while placing with the keys 2, 3, 4, 6, 8 or the mouse wheel, and
   changed later in the panel (the program remembers the last one). As soon
   as it is created, the zoom **follows the object** like boxes and arrows:
   the magnified area tracks it and grows or shrinks with it, the box stays
   where you put it and keeps its size; if the object leaves the frame the
   zoom ends. A **coloured outline** marks the object and a **line** links it
   to the magnified box (both can be turned off in the panel). Shift+Z makes an
   oval zoom.
9. **Pixel** (P rectangular, K oval): drag the box over the subject, set until
   when to track it and the pixel size. The program follows the subject in
   the following frames and saves the path as points. The box **also follows
   the size**: if the subject comes closer to the camera (a vehicle stopped at
   a stop sign that drives towards you) the pixelation grows to always cover
   it, if it moves away it shrinks. When the subject leaves the frame, the
   pixelation follows it out until it is completely gone; if it is lost, it
   ends at the last frame where it was seen. It never stays at the edge
   pixelating whatever passes by.
10. **Logo** (L): logo and operator text, **fixed in the chosen corner**. They
    are prepared once on the **Configure** page: *Load logo image...* (PNG
    with transparency, JPG...), the text (name, role, date...), the logo width
    in % of the video, the text height and the distance from the edges in % of
    the short side, the corner, the layout (text right, left or below the
    logo), the text colour and a background with opacity and rounded corners.
    The button places them over **the whole video** (even if it later gets
    longer or shorter) or only over the IN–OUT portion, if marked.
11. **Export MP4** (Ctrl+E): chooses the file and renders everything with
    ffmpeg (H.264 + AAC, quality and encoding speed in Configure). The
    progress window can be cancelled.

Undo/Redo: Ctrl+Z / Ctrl+Y. Save: Ctrl+S (Ctrl+Shift+S to save as).
On the timeline Ctrl+wheel zooms and the wheel scrolls (Shift+wheel, or the
wheel on the row names, scrolls audio and effects vertically); a right click on
an effect bar extends it to the cursor or stops it there, and the eye icon
hides or shows it. On the preview the wheel moves by one frame and Ctrl+wheel
zooms the view; the button at its top right **detaches** the preview into a
separate window. Esc cancels a drawing.

## The project file

A JSON file with the size and frame rate of the project, the clips in
sequence, the audio tracks, the effects and the information on the source
files (absolute paths):

```json
{
  "width": 1920, "height": 1080, "fps": 25,
  "original_volume": 1.0,
  "clock": {"size": 160, "corner": "top-right", "margin": 24, "color": "#FFFFFF"},
  "clips": [
    {"id": "a1", "kind": "video", "source": "C:/video/a.mp4", "in": 0.0, "out": 12.5,
     "audio": true, "speed": 1, "clock": false},
    {"id": "a2", "kind": "freeze", "source": "C:/video/a.mp4", "at": 12.5, "duration": 3.0},
    {"id": "a3", "kind": "video", "source": "C:/video/a.mp4", "in": 12.5, "out": 40.0,
     "audio": true, "speed": 8, "clock": true}
  ],
  "audio_tracks": [
    {"id": "t1", "name": "commentary", "source": "C:/audio/voice.mp3", "start": 2.0,
     "in": 0.0, "out": 30.0, "volume": 0.8, "muted": false}
  ],
  "effects": [
    {"id": "e1", "type": "text", "start": 1.0, "end": 5.0, "x": 80, "y": 60, "text": "Title",
     "font": "DejaVuSans-Bold.ttf", "size": 64, "color": "#FFFFFF", "bg": true,
     "bg_color": "#000000", "bg_alpha": 0.55, "shadow": true, "align": "left"},
    {"id": "e2", "type": "box", "start": 1.0, "end": 5.0, "x": 400, "y": 200, "w": 300, "h": 200,
     "color": "#FF3B30", "thickness": 5, "fill": false, "fill_alpha": 0.25, "radius": 0,
     "track": [[1.0, 400, 200], [2.4, 430, 190], [5.0, 520, 210]]},
    {"id": "e3", "type": "oval", "start": 1.0, "end": 5.0, "x": 900, "y": 300, "w": 200, "h": 260,
     "color": "#FFD700", "thickness": 5, "fill": false, "fill_alpha": 0.25},
    {"id": "e4", "type": "arrow", "start": 1.0, "end": 5.0, "x1": 100, "y1": 700, "x2": 400, "y2": 420,
     "color": "#FF3B30", "thickness": 8},
    {"id": "e5", "type": "zoom", "start": 6.0, "end": 9.0, "x": 300, "y": 150, "w": 200, "h": 150,
     "factor": 3, "bx": 1300, "by": 24, "color": "#FFFFFF", "thickness": 4, "outline": true,
     "track": [[6.0, 300, 150], [9.0, 420, 160]]},
    {"id": "e6", "type": "pixelate", "start": 3.0, "end": 8.0, "x": 500, "y": 120, "w": 160, "h": 160,
     "block": 16, "shape": "oval", "track": [[3.0, 500, 120, 1.0], [4.2, 540, 118, 1.2], [8.0, 700, 130, 2.1]]},
    {"id": "e7", "type": "logo", "start": 0.0, "end": 40.0, "full": true, "x": 1500, "y": 990,
     "logo": "C:/logos/agency.png", "w": 230, "text": "Op. John Smith", "size": 38, "color": "#FFFFFF",
     "layout": "right", "shadow": true, "corner": "bottom-right"}
  ],
  "sources": {"C:/video/a.mp4": {"duration": 40.0, "video_duration": 39.9, "fps": 25,
                                 "width": 1920, "height": 1080, "has_audio": true}}
}
```

Times are in seconds of the final video (timeline), coordinates in pixels of
the project. The duration of a clip is `(out - in) / speed` (`speed` from 0.25
to 32). `track` is the tracking path: every point is `[time, x, y, scale]`,
where x, y is the corner of the starting box centred on the subject (for the
arrow, the tip) and the scale its size relative to the first point (missing in
old projects: it means 1). `keys` holds the keyframes set by hand. Between two
points the values are interpolated. A logo with `full` always covers the whole
timeline. When a portion is deleted or something is inserted, the following
effects and audio tracks move accordingly; the points inside a deleted portion
are removed.

## How rendering works

`editsimple/render.py` builds one single ffmpeg filter graph (written to a file
and passed with `-/filter_complex`):

- every clip is an input of its own (`-ss`/`-t` on the source file) brought to
  the project size with `scale` + `pad`, `fps` and `format=yuv420p`; speed is
  `setpts=(PTS-STARTPTS)/N` on the video and a chain of `atempo` on the audio;
- a freeze frame (or a slide) is a PNG looped with `-loop 1 -t N`;
- pixelation is `split` → `crop` (with `x`/`y` given as a function of `t` that
  interpolates the tracking points) → `scale` down and up with
  `flags=neighbor` (for the oval, `geq` gives zero alpha outside the ellipse) →
  `overlay` at the same position, enabled only in its interval (`enable`).
  `crop` and `scale` have fixed sizes: if the subject changes size, the
  interval is split into stretches of constant size (6% steps, always just
  larger than the subject), each trimmed with `trim` on its own frames and
  overlaid with `eof_action=pass`. Long paths are written as nested `if`
  (a balanced tree), because ffmpeg refuses a sum of more than about a hundred
  terms;
- segments are joined with `concat` or, with a cross-fade, `xfade` (all with
  the same time base, `settb=AVTB`); on top go the zoom (`split` → `crop` →
  `scale` → `pad` for the border → `overlay`, with the outline and the link
  line as a PNG sequence, one per frame, because the line changes shape), the
  overlays (PNGs drawn with Pillow by `overlays.py`, the same as in the
  preview, with `overlay` and `enable`; if they follow a subject, `x` and `y`
  are functions of `t`), the elapsed time and frame number (PNG sequences) and
  the clock (a looped PNG sequence, one per speed);
- added audio tracks are delayed with `adelay` and mixed with `amix`;
- output H.264 (`libx264`, configurable CRF and preset) + AAC, `+faststart`.

The preview composes the same frame with Pillow (`overlays.compose`), so it
matches the result. Frames come from OpenCV already reduced to the size of the
view (`media.Frames`); during playback a thread keeps the decoder about ten
frames ahead of the cursor (never going back: a seek on a 4K video costs
hundreds of milliseconds) and prepares a second decoder on the next cut, so the
change of clip does not stop playback; backwards playback reads blocks of
frames in the background. The film-strip thumbnails pause during playback, so
as not to take CPU from the preview. Preview audio is the same mix as the
export, played through the Windows multimedia API.

Tracking (`tracking.py`) works on reduced grayscale frames with
`cv2.matchTemplate` and a template that updates slowly. At every frame it tries
five sizes around the expected one (object coming closer or moving away) and
compares them by bringing the found area back to the template size, against
both the updated and the original template: a template updating on its own
would absorb the size error and lag behind. When the subject reaches the edge
only the part of the template still inside the frame is searched (the template
never learns the edge, so it cannot stick to it), and tracking stops when the
box is half out, or more than a third out and moving away, or when the subject
is not found for 0.4 s; from there the figure goes on at its last speed until
it is completely out. The path is simplified (Douglas–Peucker). The film-strip
thumbnails are decoded by two threads (`timeline_view.Thumbs`), those near the
cursor first.

## Limits

- Backwards playback is without sound.
- Arrows follow the movements of the subject but keep their size. Sizes change
  in 6% steps, always just larger than the object.
- Without VitTrack, tracking compares an image template: a thin person in front
  of a rich background passing behind a pole can leave the figure on the pole.
  Even with VitTrack two people overlapping may swap for a moment. Draw the box
  tight on the subject; where the figure goes to the wrong subject, move the
  cursor there and drag it back (a keyframe), or use *Repeat tracking from the
  cursor*.
- Effects are tied to timeline times: when clips are reordered they stay where
  they are.
- Zoom and speed are not animated (no progressive zoom or speed ramps).

## Single executable

```bash
.venv\Scripts\python.exe scripts\build_exe.py
```

installs PyInstaller in the virtualenv if missing and builds
`dist\EditSimple.exe` (a single file, no console, "ES" icon). Inside are
Python, the libraries, logo, icon and the DejaVu fonts of `font\`.
**Third-party programs are not in the bundle**: ffmpeg stays in the `tools\`
folder next to the executable, downloaded by the program itself. With
`--release` it also writes `dist\EditSimple-<version>-windows-x64.zip` (exe,
LICENSE, NOTICE, README and the license files of the bundled software) and the
release notes taken from `CHANGELOG.md`. `scripts\make_brand.py` regenerates
logo and icon (it needs the Panchang font in `font\`).

## Structure

| File | Content |
| --- | --- |
| `EditSimple.py` | entry point |
| `editsimple/app.py` | main window: header, Editing and Configure pages, actions, tracking |
| `editsimple/project.py` | project model (clips, audio tracks, effects) and JSON file |
| `editsimple/render.py` | export: segments, ffmpeg filter graph, progress |
| `editsimple/overlays.py` | drawing of text, boxes, ovals, arrows, clock, time; zoom and pixelation; frame composition |
| `editsimple/tracking.py` | subject tracking (OpenCV, optional VitTrack) with exit and loss detection |
| `editsimple/media.py` | file information (ffmpeg), frames for the preview (OpenCV, read-ahead), times |
| `editsimple/timeline_view.py` | timeline: ruler, film strip, audio, effect lanes, dragging |
| `editsimple/preview_view.py` | preview with drawing and editing of overlays with the mouse, view zoom |
| `editsimple/panels.py` | properties panel of the selected item |
| `editsimple/fonts.py` | fonts of `font/` and of the system, picker with preview |
| `editsimple/tools.py` | finding, downloading and updating ffmpeg and VitTrack in `tools/` |
| `editsimple/audio.py` | audio playback in the preview (waveOut on Windows, a system player on Linux and macOS) |
| `editsimple/i18n.py`, `editsimple/locales/` | interface languages (Italian in the code, catalogs for the other 8) |
| `editsimple/theme.py`, `widgets.py`, `frameless.py` | dark theme, components and dialogs, window without title bar |
| `editsimple/procs.py`, `config.py` | child processes tied to the app; settings in `config.json` |
| `font/` | fonts shipped with the program (DejaVu; Panchang for the logo, not redistributed) |
| `scripts/build_exe.py`, `scripts/make_brand.py` | single executable and release zip; logo and icon |
| `scripts/check_i18n.py` | check of the language catalogs |
| `scripts/manual_screenshots.py` | rebuilds the example project step by step and takes the manual's screenshots |
| `docs/manual/` | user manual in 9 languages with screenshots |
| `tools/` | downloaded third-party programs (ffmpeg, VitTrack): outside the repository and the bundle |

## License and credits

EditSimple is free software under the GNU GPL version 3 with additional
attribution terms (see `LICENSE` and `NOTICE`).

Andrea Cumini — andrea@osintinfo.net — www.osintinfo.net
