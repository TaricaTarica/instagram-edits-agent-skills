---
name: edits-rough-cut
description: Builds the base cut of a talking-head Reel inside Instagram Edits for Mac — cut silences (like Edits' "Cut Silences" but word-accurate), remove filler words (um, uh, eh, o sea, tipo), drop false starts and bad takes (keep the last good take), tighten pacing to natural/fast/extra-fast and keep deliberate pauses before punchlines. Uses transcribeClip, findPauses, quietPoint and splitAt. Use whenever the user asks to cut silences, remove pauses or fillers, tighten, jump-cut, clean up a raw take, "make it snappier", or starts editing raw footage into a Reel in Edits.
---

# Rough cut in Edits: silences, fillers and bad takes

The rough cut decides how the Reel feels more than any effect. The goal is speech that flows like a confident conversation: no dead air, no stumbles, but breathing room where meaning needs it.

Read `edits-operate` first if you have not driven Edits in this session. If the project folder has an `edits-style.md`, its pace and pause values override the defaults here.

## 1. Inventory and transcript

1. Footage must be under `~/Movies/`. `addMedia(path, audioKind="")` puts a take on the main (magnetic) track.
2. `transcribeClip(id, language, mergeSplitWords=true)` → every word with `start`/`end` in timeline seconds, plus `lines` (phrases). A 34 s take transcribes in ~15 s.
3. `findPauses(id, path="", start=0, duration=<clip>, minDuration=0.3, thresholdDb=-35)` → near-silent stretches. Use it to cross-check the transcript: the last word of a phrase often carries trailing silence the transcript hides.
4. Spot-check one or two word timings with `captureFrame`/listening before trusting them across the whole clip.

## 2. Decide the cuts (plan before touching the timeline)

Build an edit decision list (EDL) in your head or in `edit-report.md`: keep-ranges in timeline seconds, with a one-line reason per removal.

**Pace presets** — gap length that gets cut, and how much air stays:

| Pace | Cut gaps longer than | Air left on each side | Feels like |
|---|---|---|---|
| natural | 0.6 s | ~0.15 s | conversational, calm topics |
| fast (default for Reels) | 0.3 s | ~0.1 s | energetic talking head |
| extra-fast | 0.15 s | ~0.05 s | rapid-fire lists, hype |

**Rules that keep it human:**
- Never cut inside a word. Land each cut point with `quietPoint(id, seconds, window=0.3)` — it returns the quietest 10 ms near your target.
- Pad cut edges 30–200 ms; timestamps can drift 50–100 ms, and clipped consonants sound robotic.
- Leave a deliberate 0.35–0.4 s pause right before a punchline, reveal or key number. Silence there is emphasis, not waste.
- Remove filler-only words: en "um, uh, like (as filler), you know", es "eh, em, este, o sea (cuando no aporta), tipo", pt "é, hum, tipo, né". Keep verbal tics that carry the creator's voice when `edits-style.md` says so.
- **False starts and repeated lines:** if a sentence is started and restarted, keep the last complete take — it is almost always the best delivery. Diff repeated phrases in the transcript to find them.
- Drop segments shorter than ~0.2 s after cutting; they read as glitches.
- The first spoken words should be the hook. If the strongest line is later in the take, flag it for `edits-hook` instead of reordering here.

Show the user the plan in 4–8 sentences (what goes, total duration before → after, any judgment calls like "removed the second explanation of X") and wait for approval before applying.

## 3. Apply

1. Compute all split times (both edges of every removed range) and call `splitAt(id, times=[...])` **once** — up to 1,000 times in one undo step. Default `snap: projectFrame` aligns to frames.
2. `clips` → map the new pieces to keep/remove by their start times.
3. `clearSelection`, then `selectById(firstToRemove, addToSelection=false)` and `selectById(next, addToSelection=true)` for the rest, then `delete`. The magnetic main track closes the gaps.
4. `clips` again: confirm total duration matches the plan (± a few frames).
5. `saveProject`.

Deleting a main-track clip ripples everything after it (captions, overlays, music). That is why the rough cut comes **before** captions, overlays and sound.

## 4. Check

- `transcribeClip` the result (or read captions if already generated) and scan for chopped words and doubled words at joins.
- `captureFrame(times=...)` at 3–4 joins: jump cuts on the same framing are fine for Reels; if a join looks like a glitch (head snaps), plan a punch-in there in `edits-polish` to hide it.
- Report: duration before/after, number of cuts, fillers removed, and anything left for the user to judge.

## Multiple takes

When the user recorded several takes of the same script, transcribe each, pick the best delivery per sentence (energy, no stumbles, clean audio), place them in order with `addMedia`, and trim with `trim(id, side, deltaSeconds)`. Tell the user which take each sentence came from.
