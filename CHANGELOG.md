# Changelog

The most recent section is used by `scripts/build_exe.py --release` as the
release notes: first the introduction, then the list of changes.

## Unreleased

- **Linux: mouse wheel**: the wheel now works on X11 in the preview and on the timeline, with its Ctrl and Shift variants; Tk delivers it there as buttons 4 and 5 instead of MouseWheel.
- **Linux and macOS: open folder**: "Open tools folder" and "Open folder" after an export use xdg-open (Linux) or open (macOS); before, the first raised an error and the second did nothing.
- **Linux and macOS: system fonts**: the font picker also lists the system fonts (/usr/share/fonts, /usr/local/share/fonts, ~/.local/share/fonts and ~/.fonts with their subfolders, and the macOS font folders).
- **Linux and macOS: preview sound**: the audio preview plays through the first system player found among pw-cat, paplay, aplay and ffplay; without one it stays silent as before.
- **Linux: pw-cat without --raw**: the preview sound skips a pw-cat that does not know the --raw option (Ubuntu 24.04) and uses the next player, instead of staying silent.
- **Linux and macOS: window icon**: the program icon is set with iconphoto, since iconbitmap does not read .ico files there.
- **Linux and macOS: resize cursors**: outside Windows the handles of the selected item use the portable X11 cursor names (the size_* names exist on Windows only); before, every hover raised a Tk error on X11.
- **ffmpeg outside Windows**: the Configure page and the start-up warning explain how to install ffmpeg with the system package manager or put it in tools/ffmpeg/, and the Download / Update button is disabled.
- **Start-up errors on Linux**: when the interface cannot start, the message is also shown with zenity or xmessage if one of them is installed.
- **Linux launcher**: avvia.sh starts the program with .venv/bin/python, or python3 when there is no virtualenv; new "Linux" section in the README.
- **SyntaxWarning at start**: fixed the invalid escape sequence in the docstring of editsimple/locales/__init__.py.
- **Linux and macOS: broken audio player**: when the system player exits right after starting (for example pw-cat without a running PipeWire, or aplay without a device), the preview switches to the next player and does not try the broken one again in the session; before, the preview ran silent.
- **Linux and macOS: audio/video alignment**: the preview clock allows for the start delay of the system player (a fixed estimate per player) and ffplay starts without buffering; a small offset can remain, see the Linux section of the README.
- **Linux and macOS: first Play**: the search for a system player (including the pw-cat check) runs in the background at start-up, so the first Play no longer waits for it.
- **Tidy-up in preview_view.py**: all imports are grouped above the cursor constants (no behaviour change).
- **Linux launcher through a symbolic link**: avvia.sh follows symbolic links to itself, so a link in ~/bin starts the program from the real folder.
- **Open folder**: xdg-open and open receive an absolute path; the tools.py description names tools/ffmpeg/ffmpeg on Linux and macOS.
- **Start-up errors on Linux, once**: after the first dialog tool that could start (zenity or xmessage) the other one is not tried, whatever the exit code, so closing the dialog with the window button no longer shows the message twice.

## 1.0.0

First release of EditSimple, a simple video editor made to explain a fact or show evidence in a video: import the footage, point at what matters, and arrows, boxes, zooms and pixelations follow the subject on their own; where the tracking goes wrong, drag the figure back onto the subject. In a few minutes you get an MP4 ready to show, with opening and closing slides, texts, logo and the operator's signature.

- **Subject tracking**: boxes, ovals, arrows, zooms and pixelations follow a person, a face, an object or a vehicle, grow and shrink with it when it comes closer or moves away, and end on their own when it leaves the frame (they follow it out until it is completely gone, so no frame is left uncovered). The optional VitTrack model (downloaded on request) helps find the subject again behind an obstacle.
- **Keyframes**: where the tracking is wrong, drag the figure onto the subject in the preview; the path is corrected before that point and tracking restarts from there to the next keyframe. Keyframes and tracking points can be selected and deleted on the timeline.
- **Arrow on a subject**: the arrow follows a rectangle drawn around the subject, keeping its tip on it.
- **Zoom** from 2x to 16x, rectangular or oval, in a box placed anywhere, with an outline and a line linking it to the object.
- **Pixelation**, rectangular or oval, for faces and plates.
- **Texts** on several lines (alignment, font, size, colour, shadow, background with opacity and rounded corners), **images** over the video, **logo and operator text** fixed in a corner, **elapsed time** and **frame number** written in the video.
- **Slides** at the start, at the end or in the middle, with a solid colour or a background image; texts and images go on top.
- **Speed** from 0.25x (slow motion) to 32x (fast forward), with an optional clock icon showing the speed.
- **Cut, delete, freeze frame**, clips reordered by dragging; **transitions**: from black, to black, cross-fade with the next clip.
- **Audio**: added tracks (commentary, music) with volume and fade in/out, original audio with volume, fades and removal of single stretches, a white line showing the volume on every track; preview playback with sound.
- **Timeline**: film strip down to single frames, effect lanes that scroll vertically, an eye to hide or show an effect, right-click menu to extend an effect to the cursor or stop it there, resizable split between preview and timeline.
- **Preview**: zoom with Ctrl+wheel and pan, playback backwards, ±10 frames, and a button to **detach** it into a separate window (and dock it back).
- **Export** to MP4 (H.264 + AAC) identical to the preview.
- **Interface in 9 languages** (English, Italian, German, French, Spanish, Dutch, Polish, Greek, Albanian), switched without restarting, and a **user manual** with screenshots in every language in `docs/manual`.
- ffmpeg and the VitTrack model are not included: the Configure page downloads them into the `tools` folder next to the program, with their licenses.
