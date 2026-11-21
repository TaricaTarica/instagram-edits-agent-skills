---
name: edits-variants
description: "Turns one recording into several genuinely different Reel versions in Instagram Edits for Mac for A/B testing and Instagram Trial Reels — Story, Punch-first and Short cuts with different hooks, order, length and sound — using duplicateProject, then explains how to publish and compare them (3-second hold, watch time, shares, saves). Use whenever the user asks for variants, versions, A/B tests, trial reels, \"test different hooks\", multiple cuts of the same video, or repurposing one take into several Reels."
---

# Variants and Trial Reels

Instagram limits reach for content it has already seen, and Trial Reels are compared against other trials. So a variant must be a **new edit**, not the same file with a different caption: different hook, different order, different length and different sound.

## 1. Prerequisites

- A finished base edit (rough cut, color, audio, captions style) — that's the brand and stays identical across versions.
- Ideally the creator recorded 2–3 alternative first lines. Without them, variants can only reorder and shorten; say so.
- Hook options from `edits-hook`.

## 2. Three patterns

| | A · Story | B · Punch-first | C · Short |
|---|---|---|---|
| Hook | the planned opening (scene/confession) | the boldest or most debatable line, moved first | an alternative one-line claim |
| Structure | chronological, as recorded | payoff → "here's how I got there" → story | one idea, no extra context |
| Length | full (typically 45–90 s) | full or −10% | 20–40 s |
| Zooms | few, on turns only | punch-in on the hook and each key fact | many, fast rhythm |
| Sound | voice + subtle SFX, no music | low instrumental bed | trending/upbeat bed, more SFX |
| Ending | open question to the audience | same question | hard stop on the strongest line |

Adapt the patterns to the content; the point is that each version tests a different reason to keep watching.

## 3. Build

1. Home screen: `duplicateProject(id)` once per variant (keep the base untouched), `renameProject(id, name)` with a clear scheme: `YYYY-MM-DD_topic_A-story`, `_B-punch`, `_C-short`.
2. `openProject` each and change only what differs: reorder/cut (`reorderClip`, `splitAt`, `delete`), swap hook text, adjust zooms, music and SFX. Re-check caption timing after reordering (cuts ripple).
3. Run `edits-qa` on each. `saveProject`.
4. Swapping a hook clip in an existing variant: `replaceElementMedia(id, path)` resets the in-point and scrambles transform keyframes — re-slip with `slipClip`, then clear and re-add keyframes.

## 4. Publishing plan (the user posts; the MCP can't)

- One version goes to the profile as a normal Reel at a time the audience is awake — usually the one the creator believes in most. The others go as **Trial Reels** (shown first to non-followers; available on accounts that meet Instagram's eligibility).
- Don't post several versions the same hour; they compete with each other. Never post at 3 a.m. "to test".
- Don't delete and re-upload the same file — publish a new edit instead.

## 5. Compare (after 48–72 h)

Write a short table in `edit-report.md` per version: views, % still watching at 3 s (below ~60% = opening fails), average watch time vs. length, shares and saves per 1,000 views, follows. Decide which hook pattern won and record it in `edits-style.md` so the next edit starts from it.
