# Changelog

The most recent section is used by `scripts/build_exe.py --release` as the
release notes: first the introduction, then the list of changes.

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
