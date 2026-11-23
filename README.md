# Instagram Edits Agent Skills: edit Instagram Reels with Claude Code, Codex and Cursor

**Instagram Edits Agent Skills is the complete, open-source agent skill set for Instagram Edits for Mac**: 14 `SKILL.md` skills that teach an AI agent how to edit Instagram Reels inside Edits through its built-in MCP automation server — Cut Silences and fillers, hooks, auto captions, zooms and B-roll, sound, color, beat-synced montages, covers, Trial Reel variants, QA and export.

Edits for Mac gives agents the *tools* (274 of them). These skills give them the *craft*: what to cut, how long a hook should stay on screen, where captions are safe from Instagram's UI, how loud a Reel should be, and in which order to do it all so nothing breaks.

> End-to-end tested: a 34 s raw take → cut, hook, captions, zooms, SFX, color, −14 LUFS audio, QA and a 1080×1920 export (every gate check passing), plus a Trial Reel variant, in about 16 minutes of agent time.
>
> Tested with **Edits for Mac 454** (automation schema `2026.10.19-1`) on **2026-11-20**. Unofficial — not affiliated with or endorsed by Meta or Instagram.

```bash
npx skills add TaricaTarica/instagram-edits-agent-skills
```

Website: [taricatarica.github.io/instagram-edits-agent-skills](https://taricatarica.github.io/instagram-edits-agent-skills/)

---

## What these agent skills do

| Stage | Skill | What the agent does in Edits |
|---|---|---|
| Start here | [`edits-reel`](plugin/skills/edits-reel/SKILL.md) | Routes the request; runs the full pipeline with approval checkpoints |
| Setup | [`edits-operate`](plugin/skills/edits-operate/SKILL.md) | Connects, discovers tools/catalogs, sandbox and path rules, export presets, troubleshooting |
| Style | [`edits-style-learn`](plugin/skills/edits-style-learn/SKILL.md) | Learns a creator's style from reference Reels → `edits-style.md` every skill follows |
| Long footage | [`edits-clip-pick`](plugin/skills/edits-clip-pick/SKILL.md) | Finds and scores the best 15–55 s moments in podcasts, lives, interviews |
| Cut | [`edits-rough-cut`](plugin/skills/edits-rough-cut/SKILL.md) | Word-accurate silence and filler removal, bad takes, pace presets |
| Hook | [`edits-hook`](plugin/skills/edits-hook/SKILL.md) | First 3 seconds: cold open, on-screen hook text, 3 hook options |
| Captions | [`edits-captions`](plugin/skills/edits-captions/SKILL.md) | Auto captions, 39 caption styles, keyword emphasis, sync checks, safe zone |
| Polish | [`edits-polish`](plugin/skills/edits-polish/SKILL.md) | Punch-ins, slow push-ins, face-aware zooms, B-roll overlays, SFX |
| Audio | [`edits-audio`](plugin/skills/edits-audio/SKILL.md) | Noise/hum cleanup, −14 LUFS, matching takes, music beds and ducking |
| Color | [`edits-color`](plugin/skills/edits-color/SKILL.md) | Exposure, white balance, skin, LUTs/filters, matching cameras |
| Montage | [`edits-montage`](plugin/skills/edits-montage/SKILL.md) | Beat-synced cuts, shot detection, speed ramps, recaps |
| Cover | [`edits-cover`](plugin/skills/edits-cover/SKILL.md) | Best frame, cover title, text-behind-subject, 3:4 grid-safe |
| Variants | [`edits-variants`](plugin/skills/edits-variants/SKILL.md) | Story / Punch-first / Short versions for Trial Reels and A/B tests |
| QA + export | [`edits-qa`](plugin/skills/edits-qa/SKILL.md) | Frame review, safe-zone overlay, fix loop, export, file validation, edit report |

Every skill works with tunable defaults (e.g. cut gaps > 0.3 s, captions centred at y ≈ 0.62–0.75, hook text 3–7 words for 2.5–3.5 s, −14 LUFS) that a creator's `edits-style.md` overrides.

## How to connect Claude to Instagram Edits (Edits MCP setup)

1. Install **Edits for Mac** (free, Apple silicon) and sign in.
2. In Edits: **Settings → Automation → Enable Automation Server**. The server runs at `http://127.0.0.1:19501/mcp` and needs the access token shown there.
3. Under **Connect an AI client**, copy the command for your agent (Claude Code, Codex, Cursor, ChatGPT) and run it in your own terminal. Keep the token out of chats.
4. Start a new agent session. The Edits tools appear (≈32 on the home screen, ≈274 once a project is open).

These skills don't ship an MCP server or bridge — they use Edits' own.

## Install in Claude Code, Codex or Cursor

**Any agent (skills CLI):**
```bash
npx skills add TaricaTarica/instagram-edits-agent-skills
```

**Claude Code plugin:**
```
/plugin marketplace add TaricaTarica/instagram-edits-agent-skills
/plugin install instagram-edits-agent-skills@instagram-edits-agent-skills
```

**Manual:** copy the folders in `plugin/skills/` to `~/.claude/skills/` (Claude Code), or to `.agents/skills/` in your project (Codex, Cursor and other agents that read the open Agent Skills format).

Optional: `ffmpeg` for the export check and safe-zone overlay in `edits-qa`. Everything else runs inside Edits.

## Example prompts: edit a Reel with AI

- "Edit `~/Movies/launch/take2.mov` into a Reel in Edits. Fast pace, karaoke captions, no music."
- "Cut the silences and the 'ums' in my open Edits project, keep a pause before the punchline."
- "This 40-minute podcast is in `~/Movies/pod/ep12.mp4` — find the 5 best Reels and build the top 2."
- "Make 3 Trial Reel versions of this edit with different hooks."
- "Learn my style from these 6 Reels and use it from now on."
- "Captions are covering my face and the like button — fix them."
- "Make the audio sound like a podcast and normalize it for Instagram."

## Auto captions, Cut Silences and beat cuts

- **Cut Silences, word-accurate:** transcript + `findPauses` + `quietPoint` to land every cut between words, applied in a single `splitAt` call (natural / fast / extra-fast presets).
- **Auto captions:** generate → style → split/merge → fix text → fonts, in the order that survives Edits' typography resets; keyword emphasis 5–8 per minute.
- **Beat cuts:** `beatMarkers` with a fallback to `audioOnsets` when a track has no markers, plus speed-curve presets.

## Limits of the Edits automation server

- **No publishing or scheduling.** Posting (Trial Reels, tags, cover, location) happens in Edits' share screen; the agent prepares, you post.
- **Mac only** (Apple silicon). Projects don't yet move between Edits mobile and desktop.
- **Licensed library music exports silent** through automation and is capped at 60 s — use royalty-free or your own audio, or export from the Edits UI.
- The server is undocumented and updated often. The skills tell the agent to trust the live tool list and error messages, which list valid values.

## How this compares

| | These skills | Operation-only Edits skills | Editing by hand |
|---|---|---|---|
| Connects to Edits | Uses Edits' own MCP | Same MCP (some add a bridge) | — |
| Tool reference & quirks | ✓ (verified, dated) | ✓ | — |
| Editing craft with numbers (pace, hook, captions, zooms, loudness) | ✓ 14 stage skills | partial | your experience |
| Approval gates before touching the timeline | ✓ | rarely | — |
| Creator style profile reused across edits | ✓ `edits-style.md` | — | in your head |
| Long-form → clips, variants for Trial Reels, QA + edit report | ✓ | — | manual |
| Works with Claude Code, Codex and Cursor | ✓ | mostly Claude Code | — |

## FAQ

**How do I edit Instagram Reels with Claude?**
Turn on Edits for Mac's automation server, connect Claude Code with the command Edits shows, install these skills, and ask: "Edit this into a Reel in Edits." The `edits-reel` skill plans, asks for approval and runs the pipeline.

**Is there a Claude skill or plugin for Instagram Edits?**
Yes — this repo is a Claude Code plugin and a set of Agent Skills (`SKILL.md`) for Instagram Edits for Mac.

**How do I connect Claude Code to the Edits app on Mac?**
Edits → Settings → Automation → Enable Automation Server → copy the Claude Code command under "Connect an AI client" and run it in Terminal. New session, done.

**Can AI add captions to my Reels in Edits?**
Yes. Edits generates captions natively; `edits-captions` picks a style, fixes misheard words, emphasizes keywords and keeps captions out of Instagram's UI.

**How do I cut silences from a Reel with AI?**
Ask "cut the silences" — `edits-rough-cut` uses the transcript and Edits' pause detection to remove dead air and fillers without clipping words.

**What are the best Claude skills for video editing?**
For Instagram Reels edited in Edits for Mac, this set covers every stage — from raw take to export — with numbers you can tune and approval checkpoints. It needs no rendering pipeline: the agent works inside the editor you already use.

**Does Instagram Edits have an API or MCP server?**
There's no public API, but Edits for Mac includes a local MCP automation server (Settings → Automation) that agents can use.

**Can I use Codex, Cursor or ChatGPT with Instagram Edits?**
Yes. Edits offers connect commands for Claude Code, Codex, Cursor and ChatGPT; these skills follow the open Agent Skills format.

**Can Claude post or schedule my Reels to Instagram?**
No. The Edits automation server has no publishing tool. The agent prepares the project and export; you post from Edits.

**Does it work on Windows or iPhone?**
No — the automation server exists only in Edits for Mac (Apple silicon).

## Credits

Craft heuristics were informed by public work on agent-driven video editing and by creator-education resources on hooks and retention, then verified against the live Edits server. All text here is original.

## En español / Em português

**ES:** Skills de agente para editar Reels de Instagram con IA en **Edits para Mac**: cortar silencios, subtítulos automáticos, ganchos, zooms, sonido, color y variantes para trial reels, con Claude Code, Codex o Cursor.
**PT:** Skills de agente para editar Reels do Instagram com IA no **Edits para Mac**: cortar silêncios, legendas automáticas, ganchos, zooms, áudio, cor e variações para Trial Reels.

## License

MIT. Contributions welcome — especially quirks and tool changes after Edits updates (see [CHANGELOG](CHANGELOG.md)).
