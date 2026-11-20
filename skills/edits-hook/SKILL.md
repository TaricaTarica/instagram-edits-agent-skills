---
name: edits-hook
description: Designs and builds the first 3 seconds of an Instagram Reel in Instagram Edits for Mac — finds the strongest tension line in the transcript, moves it to the opening (cold open), adds on-screen hook text from frame 0, avoids slow or static openings and clickbait, and proposes 3 genuinely different hook options. Use whenever the user asks for a hook, a better opening, "people swipe away", low 3-second retention, a title or text at the start of the Reel, or wants to test different openings — even when they only say "make the start stronger".
---

# The hook: the first 3 seconds

Viewers decide in about a second whether to keep watching. A Reel whose opening doesn't say what is at stake loses half its audience before second 4, no matter how good the rest is. The hook is the spoken first line, the on-screen text and the first image working together.

## 1. Diagnose the current opening

Read the transcript (`transcribeClip` or `captions`) and `captureFrame(atSeconds=0)`.

- Does the first spoken sentence contain tension — something uncomfortable, surprising, contested or at stake — and words that place the topic? ("I stopped posting every day and my reach doubled" works; "Hi guys, today I want to talk about…" doesn't.)
- Is there a static or empty first frame (greeting, setup scene, logo)? Cut it.
- Is the payoff promised in the first 5–10 s?

## 2. Hook archetypes (pick what the material genuinely supports)

| Archetype | Shape | Example opening |
|---|---|---|
| Confession | admit something uncomfortable | "I've been lying to my clients about one thing." |
| Contrarian claim | a statement someone wants to argue with | "Cardio is the worst way to lose weight." |
| Scene in motion | drop into a moment, mid-action | "My landlord just texted me a photo of my door…" |
| Result first | show/say the outcome, then how | "This took 40 seconds instead of 2 hours." |
| Question with stakes | not yes/no; a real dilemma | "What happens to your savings if the bank fails?" |
| Contrast | before vs. after, X vs. Y | "Ten years as a chef — and I still can't do this." |

Never use a hook the video does not pay off. No fake urgency, "nobody tells you this", invented numbers or promises. A strong hook is literally true and the next 30 s prove it.

## 3. Cold open (move the strongest line first)

If the best tension line sits later in the take:

1. Find its word range in the transcript; land both edges with `quietPoint`.
2. `splitAt(id, [start, end])` around it, then `reorderClip(id, position=0)` for that piece (main track), or `duplicate(id, placement="atPlayhead")` at 0 if the line should also stay in context.
3. Bridge: the second sentence must make sense after the jump ("Let me back up." works when needed).
4. Do this **before** captions; reordering ripples everything.

## 4. On-screen hook text (from frame 0)

- 3–7 words, lowercase or the creator's case style, one idea. It **prepares** what is said — never repeats the spoken line word for word.
- On screen 2.5–3.5 s (about the length of the first spoken sentence), then gone.
- Position: upper area y ≈ 0.17–0.25, inside the safe zone, never on the face. One keyword in the accent font/color, rest plain.
- Build: `addText(atSeconds=0, text, duration=3)` → `setTextFont`, `setTextStyle(size, color)`, `setTextPosition(id, 0.5, 0.2)`; optional `setTextAnimation(id, "fadeIn" | "scaleIn")` — subtle, no bounces on serious topics. Two-line hooks: one text element with `\n`, not two stacked elements.
- `addText` size scale differs from captions; start around 60–70 for body and verify with `captureFrame(atSeconds=1)`.

## 5. First image

- Frame 0 should already show the face at speaking distance or the most interesting visual. If it's a slow intro shot, trim it.
- A punch-in (1.08–1.12) on the first word or a hard cut at ~1–1.5 s adds motion without gimmicks (see `edits-polish`).

## 6. Deliver 3 options

Always propose three hooks that differ in kind (e.g. confession vs. contrarian claim vs. scene), each with: spoken first line (from the transcript, or a re-record suggestion), on-screen text, and whether it needs a cold open. Build the chosen one; the others feed `edits-variants`.

If no line in the footage carries tension, say so plainly and suggest what to record (one sentence) rather than dressing up a weak opening with text.

## Measuring

After publishing, the Reel's insights show how many viewers are still watching at 3 s. Below ~60% means the opening fails; compare variants on that number first, then on average watch time, shares and saves.
