---
name: edits-montage
description: Builds music-driven Reels in Instagram Edits for Mac — beat-synced montages, cut-to-the-beat B-roll, travel/product/event recaps, speed ramps (montage, hero, bullet, flash), shot detection on long clips, and picking the best moments by what's in each shot. Uses beatMarkers, audioOnsets, detectShots, describeClip, splitAt and setSpeedCurve. Use whenever the user wants a montage, edit to the beat, "sync to the music", a recap or highlight reel, trending-audio style edits, speed ramps or slow-motion moments — anything that isn't a single talking head.
---

# Montage and beat-synced Reels

A montage works when cuts land on the music and each shot earns its place. Choose shots first, then time them to the beat, then add motion — not the other way round.

## 1. Gather and understand the footage

- Copy clips under `~/Movies/<project>/`; `importToMediaBin(path)` keeps them in the media panel without placing them; `mediaBin` lists them.
- Long clips: `detectShots(id | aliasId, minShotSeconds=0.5, sensitivity)` gives exact shot boundaries; `detectCuts` groups shots by camera angle.
- What's in a shot: `describeClip(id, frames=6)` (on-device captions, topics, vibes, aesthetic score) and `sampleFrames`/`captureSourceFrames` to look at it. Rank shots by aesthetic score + relevance to the story; drop shaky, out-of-focus and duplicate angles.
- Plan an arc: opener (strongest visual, frame 0), build, peak, closer (a satisfying end frame or loop back to the start). Share the shot list with the user before assembling.

## 2. Music and beats

- Pick the song with the user (see `edits-audio` for library search and the licensed-music export caveat). Start on a `highlights` point.
- `beatMarkers(id)` on the music element lists visible markers; tune with `setBeatDensity(id, density="low"|"medium"|"high")` (`off`, `lowest` … `extreme`).
- If `beatMarkers` returns nothing on the user's own track, use `audioOnsets(id, path="", start, duration)` → onsets and best-fit tempo; place markers with `addBeatMarker(id, seconds)`.
- Cut on the downbeat for big changes, every beat or every 2 beats for energy. Don't make every cut metronomic: hold a beautiful shot for 2–4 beats, then rapid cuts on a build.

## 3. Assemble

1. Add clips in order: `addMedia(path, audioKind="")` per clip, or `addMediaPanelItemsToTimeline(aliasIds, sourceIn, sourceOut)` for exact source ranges.
2. Trim each to its beat window: `trim(id, side, deltaSeconds)` or `splitAt` + `delete`. Use `slipClip(id, deltaSeconds)` to change which moment plays without moving the cut.
3. `reorderClip(id, position)` to rearrange; `clips` to read back timings and confirm cut times match markers (± 1 frame at 30 fps ≈ 0.033 s).
4. Mute camera audio on B-roll if it fights the music (`setVolume(id, 0)`), or keep a little ambience at 0.1–0.2 for texture.

## 4. Motion and speed

- `setSpeedCurve(id, preset)` with `listSpeedCurvePresets`: `MONTAGE`, `HERO`, `BULLET`, `JUMP_CUT`, `FLASH_IN`, `FLASH_OUT`, `RAMP`, `STROBE`. Do not use `selectSpeedPanelPreset` or `dragSpeedPanelCurve` — deprecated, they have crashed the app.
- Constant slow-mo/fast: `setSpeed(id, 0.5 | 2)`; changing speed ripples later items and retimes captions inside the clip — re-check beat alignment after.
- Transitions: `addTransition(fromId, toId, filterId)` from `listTransitionsCatalog` — hard cuts by default, 1–2 stylized transitions on major moments, 0.2–0.5 s, landing on a beat.
- Subtle push-ins on static shots (1.00 → 1.06 over the shot) keep stills alive; see `edits-polish` for keyframes.
- Reverse for a loop or effect: `reverseClip(id)` (transcodes in the background; `operationEntries` shows progress).

## 5. Text and look

- Minimal on-screen text: a 3–7 word title in the first 2 s, optional location/date labels. Captions only if there's speech.
- One look for the whole piece (see `edits-color`) so shots from different cameras feel like one film.

## 6. Check

`previewVideo` across the whole Reel in ≤10 s windows: cuts on beat, no black frames, no accidental duplicate shots, energy rises toward the peak, ending lands on the music's end or a clean loop. Note the song and its license status in `edit-report.md`. `saveProject`.
