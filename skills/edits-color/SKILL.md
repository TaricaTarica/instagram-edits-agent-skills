---
name: edits-color
description: "Color corrects and grades Reels in Instagram Edits for Mac — fixes exposure, white balance and skin tones, matches clips from different cameras, applies LUTs and filters with restraint, and measures the result on rendered frames. Uses adjustment layers, setColorGrade, setColorWheel, setHSL, setCurve, applyLUT and applyFilter. Use whenever the user mentions color, grading, LUT, filter, \"too dark\", \"washed out\", \"looks orange/blue\", skin tones, warmer/cooler, cinematic look, or matching footage — or wants a consistent look across Reels."
---

# Color in Edits

Correct first (make it look right), then grade (make it look intentional). For talking heads the face is the reference: natural skin beats any look.

## 1. Look before touching

- `captureFrame(times="1,10,20")` (and per clip if several cameras). Note: is the face well exposed? are whites white? skin too orange/magenta? are blacks crushed or milky?
- `getColor(id)` reads current grade sliders, wheels, HSL and curves.
- HDR projects (Edits' default) look brighter than SDR exports; if delivering SDR, `setProjectDynamicRange("SDR")` **before** judging color.

## 2. Correct (per clip)

`setColorGrade(id, …)` — sliders are −1…1 (0 = untouched) except `saturation`, which is a multiplier (1 = normal). Start small; ±0.05–0.15 is usually enough.

| Problem | Move |
|---|---|
| Face underexposed | `exposure` +0.05…+0.15, `shadows` +0.1…+0.25 |
| Bright wall/window clipping | `highlights` −0.05…−0.15, `whites` −0.05 |
| Too cold (blue) / too warm (orange) | `temperature` ± 0.03…0.1 |
| Green/magenta cast | `tint` ± 0.02…0.05 |
| Flat, washed out | `contrast` +0.05, `blacks` −0.03…−0.06 |
| Dull skin | `vibrance` +0.05…+0.1 before touching saturation |

Keep `clarity` at 0 on faces (it ages skin). Avoid beauty smoothing unless the creator asks.

Finer tools: `setColorWheel(id, wheel="shadows"|"midtones"|"highlights"|"global", hue, intensity)`, `setHSL(id, band, hue, saturation, luminance)` (e.g. calm an orange skin band), `setCurve(id, channel, knots)`. Read back with `getColor`.

## 3. Grade the whole Reel once

- `addAdjustmentLayer(startSeconds=0, kind="adjust", durationSeconds=<reel length>)` and grade the layer, so one look covers every clip and later cuts don't lose it.
- LUTs: `applyLUT(table)` (16 built-in; `listCatalog(kind="lut")`) — applies to selected clips, else a selected adjustment layer, else creates one. Filters: `applyFilter(id, filter, intensity)` (77; `listFilters`). Keep intensity around 0.3–0.6; full-strength filters rarely flatter skin.
- Adjust or remove an applied filter/LUT with `updateCatalogItem(elementId, instanceId, intensity)` / `removeCatalogItem` — `getElement` lists instance ids.
- A safe starting look for talking heads: a touch more contrast, highlights pulled down slightly, blacks a hair deeper, saturation at or just under 1.0, a little warmth. Every value stays within ±0.1 — if you can name the effect at a glance, back it off.

## 4. Match cameras

Grade the best-looking clip first, `captureFrame` it next to each other clip, and adjust exposure/temperature/tint per clip until skin and whites match. Then put the shared look on the adjustment layer.

## 5. Measure, don't eyeball only

Use `frameSheet` (empty id = the edit) before and after. If the user has a reference Reel or target look, compare frames side by side. Useful targets for a bright, natural talking head on SDR: average face luminance clearly above the background, no clipped skin highlights, neutral whites. Record final settings in `edit-report.md` (and in `edits-style.md` if the user wants this look reused). `saveProject`.
