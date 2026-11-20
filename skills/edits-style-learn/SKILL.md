---
name: edits-style-learn
description: Learns a creator's editing style from their best Reels or reference videos and writes it to edits-style.md, a style profile every other edits-* skill follows — caption archetype, fonts, colors and position, cut pace, zoom and SFX density, hook format, color look, music habits, length, and what performs on their account. Use when the user says "edit it like my other videos", "learn my style", "match this creator", shares reference Reels, wants consistent branding across Reels, or before the first edit for a new creator.
---

# Learn a creator's style → `edits-style.md`

Defaults in the edits-* skills produce a good generic Reel. A style profile makes them produce *this creator's* Reel. Build it from evidence (their videos, their numbers), not from adjectives.

## 1. Collect references

- 3–10 of the creator's own Reels they consider their best (ideally the best-performing ones), or reference creators they want to resemble. Exported MP4/MOV files under `~/Movies/<creator>/refs/`.
- If they have account insights (CSV or screenshots: views, 3-s hold, watch time, shares, saves), ask for them — style that performs beats style that's merely consistent.

## 2. Analyze each reference

Use Edits' analysis tools on the files (no need to place them on a timeline):

- `probeMedia(path)` → duration, fps, resolution.
- `sampleFrames(path, times, maxEdge=720)` every ~2 s → captions (font family look, weight, case, color, outline/box, position y, words per screen), framing (shot size, head position), overlays, color (warm/cool, contrast, saturation).
- `detectCuts(path, start=0, duration, sensitivity)` / `detectShots` → cut frequency.
- `findPauses(path, …)` and a transcript (place on a scratch timeline and `transcribeClip`) → speech pace (words/s), leftover pauses, how the first line is built.
- `loudness(path)` → loudness; listen for music and SFX habits (`audioLevels` shows a music bed under speech).

Measure, then summarize across references; note where they disagree (e.g. three caption styles alternating) instead of averaging into nonsense.

## 3. Write `edits-style.md`

Save it in the creator's working folder (and tell the user where). Template:

```markdown
# Edit style — <creator>
Updated: <date> · Based on: <n> references (<names>) · Performance data: yes/no

## Voice & pace
Speech rate: ~<x> words/s · Rough-cut pace: natural|fast|extra-fast · Pause before punchlines: <s>
Keep these expressions: <...> · Remove: <fillers>

## Hook
Pattern that works: <confession | contrarian | scene | result-first ...> · On-screen hook text: yes/no, <words>, <position>

## Captions
Archetype: <one-word | karaoke | phrase> · Edits style: <name> · Case: <lower/sentence> · Punctuation: <rule>
Font: <family id> <size> <color> · Keyword: <font> <color> <size> · Emphasis: <outline/pill/none> · y = <0.xx>

## Motion
Zooms: <punch %, slow push %, cadence> · Overlays: <type, length, entrance> · Transitions: <rule>

## Sound
SFX: <which, volume, per minute> · Music: <none | bed level, genre> · Target loudness: <LUFS>

## Color
<grade values or LUT + intensity> · Skin: <note>

## Format
Typical length: <s> · Ending: <question | hard stop | loop>

## What performs (if data)
<top patterns with numbers, and what underperforms>
```

Only write values you measured or the user confirmed. Mark guesses as `(guess)`.

## 4. Confirm and keep it alive

Show the profile to the user, ask for corrections, and save. After each published Reel or variant test (`edits-variants`), update "What performs". The other skills read this file first and treat its values as overriding their defaults.
