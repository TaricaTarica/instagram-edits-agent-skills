---
name: edits-operate
description: Operating manual for driving Instagram Edits for Mac (Edits desktop) through its built-in MCP automation server — connecting, discovering tools and catalogs, the sandbox and path rules, time/canvas conventions, HDR vs SDR, export presets and the traps that make calls fail silently. Use this before the first Edits tool call in a session, whenever an Edits call errors ("not in current manifest", "Sandbox bookmark unavailable", 401/403, export never starts), or when the user asks what Edits can do, how to connect Claude/Codex/Cursor to Edits, or how to set up the Edits MCP. The other edits-* skills assume this one.
---

# Operating Instagram Edits for Mac through its MCP

Edits for Mac ships its own MCP server (Settings → Automation → **Enable Automation Server**). It listens on `http://127.0.0.1:19501/mcp` and needs the bearer token shown on that same page. There are no public docs: the live tool list, `getCapabilities` and the error messages are the manual. Treat everything below as tested defaults (verified on Edits 454, schema `2026.10.19-1`) and trust the live server when they disagree.

## Connect (once per machine)

1. In Edits: Settings → Automation → turn on the server. The page has a "Connect an AI client" section with ready-made commands for Claude Code, Codex, Cursor and ChatGPT.
2. Let the user copy that command and run it in their own terminal. Never ask them to paste the token into the chat — it grants full control of their editor.
3. Tools appear in a **new** session. If calls return 401/403 later, the token was regenerated: remove and re-add the server with the new command.
4. The server only exists while Edits is open. "Connection refused" = Edits is closed or the toggle is off.

## The tool list follows the screen

- `appState` tells you the screen: `home`, `editor` or `loading`.
- Home has ~32 tools (projects, new/open/duplicate/delete, `.mcomp` import/export, catalogs). The editor has ~274 (timeline, text, captions, color, audio, analysis, export).
- To get editor tools: `projects` → `openProject(id)` or `newProject`. Some clients don't refresh the tool list on their own; if editor tools are missing after opening a project, re-list tools or start a new session.
- Calling a tool from the other screen returns `unknown tool (not in current manifest)`. Check `appState`, reopen the project and continue — element ids survive.
- Tool descriptions occasionally mention tools the public server does not expose (e.g. `transcriptJumpCut`). If a name is missing from the live list, it does not exist for you; use the composable route the other skills describe.

## Discover, don't guess

- `getCapabilities` → conventions, catalog kinds with counts, and recipes. Read it once per session.
- `listCatalogKinds` / `listCatalog(kind, query, category, cursor, limit)` / `getCatalogItem` → exact ids for filters (77), effects (148), LUTs (16), transitions (51), text animations (77), text presets, caption styles (73), fonts (380), emphasis styles (5), mask shapes (5), speed-curve presets (8).
- Wrong enum values return an error that lists the valid ones (e.g. `resolutionType must be one of ["720p","HD","2K","4K"]`). Use that instead of guessing twice.
- Many apply tools accept `dryRun: true` — validate before mutating when unsure.

## Conventions

- **Time:** seconds on the composition timeline, unless a param says `*SourceSeconds` or `*Ms`. Some keyframe tools use clip-relative or source time — the error usually returns the valid times.
- **Canvas:** normalized 0–1, origin top-left, +y down, x/y = element **centre**. Rotation in degrees clockwise. Colors `#RRGGBB` or `#RRGGBBAA`.
- **Volume:** `setVolume` is linear gain 0–10 (1 = 0 dB). `setSound(volumeDb, reduceNoise, enhanceVoice)` works in dB and 0–100.
- **New projects are 2160×3840, 60 fps, HDR (HLG).** Phone footage looks fine; for SDR delivery or screen recordings call `setProjectDynamicRange("SDR")` early.

## Files and the sandbox

- Edits is sandboxed. It reliably reads files under `~/Movies/` (and anything the user picked in its UI). `~/Documents`, `~/Downloads`, `~/Desktop` and temp folders fail with `Sandbox bookmark unavailable`.
- Copy footage and assets to `~/Movies/<project>/` first and pass **absolute** paths (`/Users/<name>/Movies/...`) — `~` is not expanded.
- Export into `~/Movies/` too, then move the file where the user wants it.
- Renders created by analysis tools (frame sheets, processed audio) land in Edits' container (`~/Library/Containers/com.burbn.basel.mac/Data/...`); the path is returned in the response and is readable.

## Working safely on the user's projects

- Before editing an existing project, `duplicateProject` on the home screen and work on the copy; name it clearly. The original stays untouched until the user approves.
- `undo` / `redo` exist and are cheap — use them to back out of a bad experiment rather than rebuilding.
- `saveProject` after each stage. Ask before `deleteProject`.
- **There is no publish, share or schedule tool.** Posting happens in Edits' own share screen (Trial Reels, tags, location, cover). Hand that step to the user; never claim a Reel was posted.

## Verify with rendered frames, not screenshots

- `captureFrame(atSeconds | times="1,4.5,9", maxWidth)` renders the exact edited frame. Fast; use it after every visual change.
- `frameSheet(times, columns, cellWidth)` with an empty `id` returns a labelled contact sheet of the edit (also saved as PNG).
- `previewVideo(startSeconds, durationSeconds ≤10, frameCount ≤12)` → poll `previewVideoStatus` → `previewVideoFrames(resultId)` for motion checks (zooms, animations).
- Screenshots of the app window go stale and miss overlays; avoid them.

## Export

`export` silently never starts unless a complete preset exists. Set it first:

```
setExportSettings(resolutionType="HD", resolution="1080x1920", aspectRatio="nineBySixteen",
                  quality="High", frameRate=30, dynamicRange="SDR")
export(path="/Users/<name>/Movies/<project>/export/<name>.mp4")  → poll exportStatus
```

- Licensed library music does **not** survive an automation export (silence where it plays) and is capped at 60 s. If a licensed song matters, the user exports or posts from the Edits UI. Royalty-free tracks and the user's own audio export fine.
- Check the file afterwards (duration, resolution, audio present) — `edits-qa` has a script for it.

## Quick troubleshooting

| Symptom | Fix |
|---|---|
| `unknown tool (not in current manifest)` | Wrong screen or tool not public. `appState`, open project, re-list tools. |
| `Sandbox bookmark unavailable` | Move the file under `~/Movies/`, absolute path. |
| 401 / 403 | Token regenerated; user re-adds the server. |
| Export never finishes / never starts | Missing preset fields; call `setExportSettings` with all of resolutionType, aspectRatio, quality. |
| Export is silent | Licensed music; export from the Edits UI or use royalty-free/own audio. |
| A param is rejected | Read the error: it lists valid values or valid keyframe times. |

Record anything new you learn (tool renamed, quirk fixed) in the project's `edit-report.md` so the user can report it upstream.
