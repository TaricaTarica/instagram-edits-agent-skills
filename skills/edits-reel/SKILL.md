---
name: edits-reel
description: Start here to edit an Instagram Reel end to end with Instagram Edits for Mac (Edits desktop) through its MCP automation server — turns raw footage into a finished, exported Reel: plan, rough cut and Cut Silences, hook, auto captions, zooms and B-roll, sound, color, cover, variants for Trial Reels, QA and an edit report, with approval checkpoints. Routes small requests to the right edits-* skill. Use whenever the user says "edit this into a Reel", "edit my reel", "make a Reel from this video", "use Edits", "do it in Edits", hands over raw takes, or asks Claude/Codex/Cursor to edit Instagram videos — even without naming the app.
---

# Edit a Reel in Instagram Edits (router + pipeline)

This skill decides what to do and in which order; the specialist skills hold the details. Read `edits-operate` first in any session that hasn't driven Edits yet.

## 1. Route by project state

| The user has / asks for | Do |
|---|---|
| One specific tweak ("bigger captions", "remove that pause", "add a whoosh at 0:12") | Only the matching skill. Don't re-run the pipeline. |
| Raw take(s) of a talking head | Full pipeline below. |
| Long recording (podcast, live, interview) | `edits-clip-pick` first, then the pipeline per chosen clip. |
| Many clips + music, no single speaker | `edits-montage`, then captions/color/audio/QA as needed. |
| "Make it look like my other Reels" / new creator | `edits-style-learn` first. |
| A finished edit to test | `edits-variants`. |
| "Is it ready?" / export | `edits-qa`. |

Specialists: `edits-rough-cut`, `edits-hook`, `edits-captions`, `edits-polish`, `edits-audio`, `edits-color`, `edits-montage`, `edits-cover`, `edits-variants`, `edits-qa`, `edits-clip-pick`, `edits-style-learn`, `edits-operate`.

## 2. Full pipeline

1. **Inventory.** Which files, how long, which language, target length, where it will be posted (Reel / Trial Reel), deadline. Copy footage to `~/Movies/<project>/`. If `edits-style.md` exists in the project or creator folder, read it — it overrides defaults everywhere.
2. **Transcribe and pre-scan.** Put the take on a timeline (`newProject` → `setTitle` → `addMedia(path, audioKind="")`), `transcribeClip`, `findPauses`, and `captureFrame` at a few times. Note the strongest line, stumbles, repeated takes, weak opening, and any burned-in text or captions in the source.
3. **Ask only what blocks you** (one message): goal of the Reel, must-keep moments, music yes/no, anything off-limits. Skip questions the style file or the request already answers.
4. **Plan — approval gate.** 4–8 sentences: the hook choice (and whether it needs a cold open), what gets cut, caption style, polish level, audio/music, target duration, variants if any. Wait for a yes. A wrong plan costs a sentence; a wrong edit costs the user's trust.
5. **Work on a copy.** If editing an existing project, `duplicateProject` first. Then in this order (each step ripples into the next):
   `edits-rough-cut` → `edits-hook` → `edits-color` → `edits-audio` (voice) → `edits-captions` → `edits-polish` → `edits-audio` (music/SFX levels) → `saveProject`.
6. **Sample — second gate.** Before finishing a long Reel, show 30–60 s (`previewVideo` frames + a short description, or let the user play it in Edits) and wait for approval. Adjust the approach, not just the sample.
7. **Finish.** Complete the rest, `edits-cover` if wanted, `edits-variants` if asked, then `edits-qa` (visual + audio pass, ≤3 fix passes, export, file validation, `edit-report.md`).
8. **Hand off.** Project names, export path, what to fix by hand, and the reminder that posting happens in Edits' share screen — the agent never publishes.

## 3. Principles that apply to every step

- **Subtle wins.** If an effect is noticed as an effect, it's too much. Retention comes from the story and the cut, polish only supports it.
- **The face stays real.** No beauty smoothing or clarity on skin unless asked.
- **Truthful hooks.** Never promise what the Reel doesn't deliver; never invent numbers, names or quotes for on-screen text. Ask when a fact is missing.
- **Verify on rendered frames** after every visual change (`captureFrame`, `frameSheet`, `previewVideo`), not by trusting `ok: true`.
- **Respect the creator's voice.** Keep their expressions and rhythm; cut fillers, not personality.
- **Undo is cheap** (`undo`/`redo`); deleting projects is not — ask first.
- **No publishing, no scheduling** through the MCP. Say so plainly if asked.

## 4. Typical timings (Edits 454, Apple silicon)

Transcription ~15 s per 30 s of speech · captions ~10 s per 30 s · a rough cut with dozens of cuts is one `splitAt` call · `captureFrame` near-instant · export ~40–45 s for a 33 s Reel at 1080p. A test run of the full pipeline on a 34 s talking head (cut, hook, color, audio to −14 LUFS, karaoke captions, 3 zooms, 2 SFX, QA, export, plus one variant) took about 16 minutes end to end. Most of that went to verifying captions and audio, which is the part worth spending time on.
