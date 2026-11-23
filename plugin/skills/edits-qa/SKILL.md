---
name: edits-qa
description: "Quality check and export for Reels made in Instagram Edits for Mac — reviews rendered frames around every cut and at the start and end, checks the Instagram safe zone, caption collisions, framing and loudness, fixes issues in up to 3 passes, sets the export preset (1080×1920 SDR), exports, validates the file and writes an edit report for the creator. Use before delivering or exporting any Edits project, when the user says \"export\", \"check it\", \"is it ready\", \"review the edit\", or after any other edits-* skill finishes."
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
- Safe zone: get a frame file with `frameSheet(times="<t>", columns=1, cellWidth=1080)` (it returns the PNG path; `captureFrame` returns no file), then draw the Reels UI zones on it with ffmpeg (sizes are defined at 1080×1920 and scale to any 9:16 frame):
  ```
  ffmpeg -v error -y -i <frame.png> -vf "drawbox=x=0:y=0:w=iw:h=ih*210/1920:color=red@0.4:t=fill,drawbox=x=iw*980/1080:y=ih*210/1920:w=iw*100/1080:h=ih*1370/1920:color=red@0.4:t=fill,drawbox=x=0:y=ih*1500/1920:w=iw:h=ih*80/1920:color=yellow@0.4:t=fill,drawbox=x=0:y=ih*1580/1920:w=iw:h=ih*340/1920:color=red@0.4:t=fill" <zones.png>
  ```
  Red = blocked: header (top 210 px), action rail (right 100 px), caption + audio + buttons (bottom 340 px). Yellow = caution: a long caption expands into the 80 px above. Read `<zones.png>` and look for collisions. Nothing important (captions, hook, faces' eyes/mouth, on-screen UI being explained) may sit inside the red zones. Without ffmpeg, judge the same zones by eye on the frame.

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

All of resolutionType, aspectRatio and quality are required or the export never starts. Expect roughly 40–45 s of export time for a 30–35 s Reel at 1080p. Use 4K (`resolutionType="4K"`, `resolution="2160x3840"`) only if the user asks; Instagram recompresses anyway. Exports through the server have come out at 60 fps despite `frameRate=30` (Instagram accepts 60); flag it in the gate if 30 matters.

## 5. Validate the file

Run these four measurements on the export (ffmpeg and ffprobe must be on PATH):

```
ffprobe -v error -select_streams v:0 -show_entries stream=width,height,codec_name,avg_frame_rate -show_entries format=duration -of default=nw=1 <export.mp4>
ffprobe -v error -select_streams a -show_entries stream=codec_type -of csv=p=0 <export.mp4>
ffmpeg -hide_banner -nostats -i <export.mp4> -af ebur128=peak=true -f null - 2>&1 | sed -n '/Summary:/,$p' | grep -E 'I:|Peak:'
ffmpeg -hide_banner -nostats -i <export.mp4> -af volumedetect -f null - 2>&1 | grep mean_volume
```

Gate (report one line per check as PASS / WARN / FAIL):

| Check | PASS | WARN | FAIL |
|---|---|---|---|
| Frame | width/height within 0.01 of 9:16 and ≥ 1080×1920 | 9:16 but below 1080×1920 | not 9:16 |
| Duration | > 0 and ≤ 90 s (or the creator's limit) | over the limit | 0 or missing |
| Audio stream | the second command prints `audio` | — | prints nothing |
| Not silent | `mean_volume` > −50 dB | — | ≤ −50 dB (licensed music dropped in export?) |
| Loudness | `I:` within −14 ± 2 LUFS | outside that range | — |
| True peak | `Peak:` ≤ −1 dBFS | above −1 dBFS | — |
| Frame rate (only if 30 fps matters) | `avg_frame_rate` within 0.5 of 30 | otherwise | — |

Any FAIL blocks the handoff; WARNs go in the report. Without ffmpeg, say so and check what you can with `probeMedia(path)` and `loudness(path)` in Edits.

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
