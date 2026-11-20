---
name: edits-clip-pick
description: Finds the best Reel-sized moments inside long footage (podcasts, interviews, lives, webinars, long talking-head takes) and cuts them into separate Reels in Instagram Edits for Mac — transcribes, scores candidate clips on hook, coherence, emotion, value and payoff, snaps boundaries to sentences, and builds the chosen ones. The in-Edits equivalent of AI clipping tools. Use whenever the user wants to "find the best parts", clip a podcast or long video into Reels, repurpose long-form content, get highlights, or asks which moments would go viral.
---

# Clip picking: long footage → Reels

The best clip is a complete thought with a strong first line — not the loudest moment. Scoring makes the choice explicit so the user can disagree with reasons.

## 1. Transcribe and map

1. Footage under `~/Movies/`. Put the long file on a timeline (`addMedia`) or reference it from the media bin.
2. `transcribeClip(id, language, mergeSplitWords=true)` — long recordings are transcribed in parallel 3-minute pieces; use the returned `lines` as sentence units.
3. Optional signals: `detectShots` (camera changes in multi-cam), `audioLevels` (energy, laughter peaks), `describeClip` (what's on screen).

## 2. Propose candidates

Find 8–12 candidates, each a self-contained segment of **15–55 s** (sweet spot 25–40 s; up to 90 s if the story needs it). For each, score 0–100:

| Criterion | Weight | Ask |
|---|---|---|
| Hook | 0.30 | Do the first ~5 words create tension or curiosity on their own? |
| Coherence | 0.25 | Does it make sense with zero context from the rest of the video? |
| Emotion | 0.20 | Surprise, conflict, humor, vulnerability, strong opinion? |
| Value density | 0.15 | Concrete insight, number, story or how-to per second? |
| Payoff | 0.10 | Does it land — a punchline, conclusion or reveal? |

Keep candidates scoring ≥60. Penalize segments that start with "and", "so", "like I said", pronouns without referents, or that end mid-thought.

**Boundaries:** start at a sentence start (snap if within ~1.5 s), end at a sentence end (extend up to ~3 s to finish the thought) plus ~0.3 s of tail. Land exact cut points with `quietPoint`.

Present the list as a table — rank, score, start–end, duration, first line, why it works, suggested on-screen hook — and let the user pick. Don't build all of them by default.

## 3. Build the chosen clips

For each pick:
1. `newProject` (or `duplicateProject` from a prepared base) → `setTitle("<topic>_clip-<n>")`.
2. `addMediaPanelItemsToTimeline(aliasIds=[…], sourceIn, sourceOut)` to place exactly that range, or `addMedia` + `trim` both sides.
3. If the source is 16:9, `setCanvas(aspect="9:16")` then `autoReframe(subject="largestFace", motion="follow", wideShotPolicy="stack2")` — wide two-person shots become a stacked split screen.
4. Continue the pipeline: `edits-rough-cut` → `edits-hook` → `edits-captions` → `edits-polish` → `edits-audio` → `edits-qa`.

## 4. Report

In `edit-report.md`: the candidate table, which were built, and the project names. Clips that scored well but weren't built are useful later — keep the list.
