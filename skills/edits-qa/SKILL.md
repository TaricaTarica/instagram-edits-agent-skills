---
name: edits-qa
description: Quality check and export for Reels made in Instagram Edits for Mac — reviews rendered frames around every cut and at the start and end, checks the Instagram safe zone, caption collisions, framing and loudness, fixes issues in up to 3 passes, sets the export preset (1080×1920 SDR), exports, validates the file and writes an edit report for the creator. Use before delivering or exporting any Edits project, when the user says "export", "check it", "is it ready", "review the edit", or after any other edits-* skill finishes.
---

# QA, export and handoff

An edit isn't done when the tools return `ok` — it's done when the rendered Reel looks and sounds right. Check the output, not the plan.

## 1. Visual pass

- Read the timeline: `clips`, `captions`, `elements(limit=5000)` (default page is 200 rows; dense caption/sticker projects go past it silently).
- Render checks with `frameSheet(times=…, columns=4)` (empty id = the edit):
  - first 2 s (hook text, first frame) and last 2 s (ending, no black tail);
  - ±0.5 s around each cut (head snaps, doubled words, flash frames);
  - each overlay, zoom and title;
  - 2–3 random midpoints.
- Motion checks with `previewVideo(startSeconds, durationSeconds≤10, frameCount≤12)` on zooms, animated text and transitions.
- Safe zone: save a frame (`captureFrame(maxWidth=1080)` or the PNG path `frameSheet` returns) and run
  `python3 scripts/safe_zone_overlay.py <frame.png> <out.png>` — it draws the Reels UI zones (top 210, bottom 340, right 100 px at 1080×1920; bottom 420 px "caution" band) so you can see collisions. Nothing important (captions, hook, faces' eyes/mouth, on-screen UI being explained) may sit inside them.

Checklist: captions readable and spelled right · nothing covers eyes or mouth · no caption under an overlay · zooms don't cut the head or go soft · consistent fonts after caption splits · no leftover temporary elements · ending lands.

## 2. Audio pass

- `loudness(id)` per main clip and `audioLevels` around the hook; music doesn't mask speech; SFX audible but subtle.
- `licensedMusicStatus` — any licensed song will be silent in an automation export (see `edits-audio`).

## 3. Fix loop

Fix what you found, re-check only what changed, and stop after **3 passes**. Anything still off goes to the report as "fix by hand in Edits" rather than looping forever.

## 4. Export

```
setProjectDynamicRange("SDR")                     # if not already; HDR exports look washed out on many phones
setExportSettings(resolutionType="HD", resolution="1080x1920", aspectRatio="nineBySixteen",
                  quality="High", frameRate=30, dynamicRange="SDR")
export(path="/Users/<name>/Movies/<project>/export/<name>.mp4")
exportStatus  (poll until complete)
```

All of resolutionType, aspectRatio and quality are required or the export never starts. Use 4K (`resolutionType="4K"`, `resolution="2160x3840"`) only if the user asks; Instagram recompresses anyway. Exports through the server have come out at 60 fps despite `frameRate=30` — the gate below reports it.

## 5. Validate the file

```
python3 scripts/export_gate.py /path/to/export.mp4 [--max-seconds 90] [--target-lufs -14]
```

Checks with ffprobe/ffmpeg: 9:16 vertical at ≥1080×1920, video and audio streams present, audio not silent, duration within limits, integrated loudness and true peak near target, codec and frame rate reported. Exit code 0 = pass; it prints one line per check. Requires ffmpeg on PATH; if missing, say so and check what you can with `probeMedia(path)` and `loudness(path)` in Edits.

## 6. Handoff report

Write `edit-report.md` next to the export:

```
# <project> — edit report
Status: ready to post | needs manual fixes
Export: <path> · <duration> · <resolution> · <LUFS>
Done: rough cut (−Xs, N cuts) · hook · captions (<style>) · polish (N zooms, N overlays, N SFX) · color · audio
Not possible via MCP: <e.g. licensed music in export, fades on overlays>
Fix by hand in Edits: <list>
Variants: <names, if any>
Posting: open the project in Edits → Share (cover, tags, location, Trial Reel). The agent did not publish.
Learned: <quirks or tool changes worth reporting>
```

`saveProject`, then tell the user the project names so they can open them in Edits.
