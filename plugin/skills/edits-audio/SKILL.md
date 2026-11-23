---
name: edits-audio
description: "Makes a Reel sound professional in Instagram Edits for Mac — voice first: noise reduction and voice enhance, hum and room fixes, loudness normalization to −14 LUFS, matching levels between takes, then music beds from the Edits library or the user's own tracks with ducking and fades, and the licensed-music export caveats. Uses getSound/setSound, processAudio, loudness, audioLevels, audioSpectrum, listMusicTracks, addSongToComposition and setDucking. Use whenever the user mentions audio, sound quality, noise, echo, hum, volume, \"too quiet/too loud\", loudness, LUFS, background music, music bed, ducking, or fades — or before exporting any Reel."
---

# Audio in Edits: voice first, then music

People forgive soft video; they swipe on bad audio. The voice must be clear, even and loud enough on a phone speaker; music supports it and never competes. All of this is native in Edits — no external tools needed.

## 1. Measure

- `loudness(id, path="")` → integrated LUFS and sample peak of a clip (or a file/library item).
- `audioLevels(id, path="", start, duration, hop)` → RMS envelope, noise floor and speech level. Its whole-clip noise-floor estimate is unreliable on short talking heads (it can read 8 dB below speech when the real floor is 30 dB below). Measure the floor **inside a real pause** from `findPauses` (start/duration of that pause). Clean up only if that floor is less than ~20–25 dB below speech.
- `audioSpectrum(id, path="", start, duration, minHz=40, maxHz=8000, limit=5, minProminenceDb=6, resolutionHz=5)` → steady tones (mains hum at 50/60 Hz and harmonics, fan whine).
- `getSound(id)` → current volume dB and Voice Enhance settings.

## 2. Clean the voice

Pick the lightest fix that works; listen-check by reading levels again after each step.

| Problem | Fix |
|---|---|
| Steady background noise (AC, street) | `setSound(id, volumeDb=0, reduceNoise=40–70, enhanceVoice=0–40)` |
| Thin or distant voice | `enhanceVoice` 30–60 |
| Hum / whine | `processAudio(id, mode="replace", chain='[{"type":"notch","hz":60}]')` (add harmonics if `audioSpectrum` shows them) |
| Rumble, handling noise | `{"type":"highpass","hz":80}` |
| Heavy room/background voices | `{"type":"isolation"}` (voice isolation; check it doesn't sound underwater) |
| Overall level | gain per clip (see "Reaching −14 LUFS" below); `{"type":"normalize","lufs":-16}` only for quiet, even speech |

`processAudio` renders a new audio version of the clip and keeps the picture; `chain` is a JSON array of steps: `highpass`, `lowpass`, `notch` and `eq` need `hz`; `gain` needs `db`; `normalize` takes `lufs`; `isolation` takes none. Missing params return an error naming them. Without `lufs`, normalize targets −16. `mode="add"` appends to the existing chain. Each call reports `beforeLufs`/`afterLufs`. Order steps: highpass → notch → isolation → eq → normalize last.

Two traps:
- **`normalize` has no limiter.** Normalizing a dynamic voice to −14 LUFS can push peaks above 0 dBFS (+5 dB has been seen) and clip on export. There is no `limiter` step; unknown keys are ignored silently.
- **`mode="replace"` re-renders from the previous render**, not the original audio, and `chain="[]"` doesn't revert. Use `undo` (then verify) to go back.

## Reaching −14 LUFS without clipping

1. Clean first (table above) — without normalize.
2. `loudness(id)` per clip → set `setSound(id, volumeDb = −14 − measured, reduceNoise, enhanceVoice)`. Voice Enhance (~30) adds density, which raises loudness without raising peaks much.
3. Export a short test (or the full Reel) and run the export gate in `edits-qa` (step 5): integrated −14 ± 1 and true peak ≤ −1 dBTP.
4. If peaks are hot, lower every clip by the overshoot (e.g. −1.5 dB) and accept −15/−16 LUFS — a clean −15 beats a clipped −14.
Delete test exports afterwards.

Over-processing is worse than mild noise: reduceNoise at 100 or isolation on a clean recording makes voices robotic.

## 3. Match takes

When the Reel mixes takes or recording days, measure each kept clip's LUFS with `loudness` and set `setSound(id, volumeDb = target − measured)` so they match within ~1 dB. Measure very short pieces (<1 s) over a wider window or match them to their neighbours.

## 4. Target loudness

Aim for **−14 LUFS integrated, true peak ≤ −1 dBTP** for the finished Reel — it matches what platforms normalize to and sounds full on phones. Set the voice level first (recipe above); music adds a little on top, so re-measure after mixing on the exported file (`edits-qa`).

## 5. Music

Ask the user before choosing music — taste and rights are theirs.

- Library: `listMusicTracks(license="royaltyFree" | "any", query, tab)` → tracks with `audioAssetId`, duration and `highlights` (good start points in seconds). `previewMusicTrack(track)` to audition. Add with `addSongToComposition(audioAssetId, track)`; pass the exact title as `track` — ids alone have added the wrong song.
- Own track: copy to `~/Movies/…` and `addMedia(path, audioKind="music")`.
- Start on a highlight: `trim(id, side="left", deltaSeconds=highlight)` then `move(id, 0)`.
- Level under speech: music bed −18 to −25 dB relative to voice (start `setSound(id, volumeDb=-23 … -31)` on the music element), duck with `setDucking(id, behavior, level)` on the music element (invalid values return the allowed list), fades `setFade(id, fadeIn=0.5–1, fadeOut=1.5–2)`.
- Make music quieter during the hook and stop or drop it on the final line for impact.
- Beat-synced edits: see `edits-montage`.

**Export caveat:** songs from Edits' library are often flagged licensed even when listed royalty-free; licensed audio comes out **silent** in automation exports and is capped at 60 s for export/share. Check `licensedMusicStatus`. If the song matters, the user exports or posts from the Edits window, or uses their own/royalty-free file. Say this in the handoff.

## 6. Sound effects and voiceover

- SFX placement and density live in `edits-polish`.
- Voiceover: `listTTSVoices` + `applyTextToSpeech(id=<text element>, voice)` generates narration from a text element; or record with the teleprompter tools. Normalize voiceover like the main voice.

## 7. Check

Re-run `loudness` on the main clips, `audioLevels` around the hook, and note in `edit-report.md`: final LUFS, cleanup applied, music title and license status. `saveProject`.
