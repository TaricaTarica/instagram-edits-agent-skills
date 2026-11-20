---
name: edits-polish
description: Adds motion and retention polish to a Reel in Instagram Edits for Mac — punch-in zooms, slow push-ins and zoom-outs with keyframes, auto-reframe on the face, pattern interrupts, B-roll and screenshot overlays with entrance animation and dim scrims, cutout stickers, emoji, and subtle sound effects (whoosh, click) timed to visible events. Use whenever the user asks for zooms, punch-ins, "more dynamic", "it feels static", B-roll, overlays, images on screen, sound effects, SFX, transitions between shots, or "make it look like a pro editor did it".
---

# Polish: zooms, B-roll and sound effects

Polish exists to re-earn attention every few seconds and to show what words alone can't. The rule that keeps it professional: **if the effect is noticed as an effect, it's too much.** Every zoom, image and sound should be motivated by something said.

Do this after the rough cut and hook (cuts ripple keyframes) and before final captions placement checks. Values below are defaults; `edits-style.md` overrides them.

## 1. Plan the beats

From the transcript, mark: the hook word, each new idea, twists ("and then I realized"), numbers, lists, punchlines, emotional confessions. Assign one treatment per beat — not all of them get one.

- A change of framing every 5–10 s (zoom, cut, overlay). Never two zooms less than 2 s apart.
- Jump cuts from the rough cut already add motion; a punch-in on a jump cut also hides a visible head-snap.

## 2. Zooms on the main clip

| Move | Values | When |
|---|---|---|
| Punch-in (hard) | 1.00 → 1.08–1.15 instantly at a cut/word | emphasis, list items, the hook word |
| Big punch | → 1.20–1.25 | one-word punchline only, rarely |
| Slow push | 1.00 → 1.08–1.12 over 2–4 s, ease in-out | confession, emotional moment, tension build |
| Zoom-out | 1.12–1.15 → 1.00 over 1–2 s | a new idea or a list of actions starts |

**How:**
- Find the face: `detectSubjects(id, kinds=["face"], sampleEvery=0.5)` → box centre P = (px, py). For scale s, keep the face where it is by setting the clip centre to `x = 0.5 − s·(px − 0.5)`, `y = 0.5 − s·(py − 0.5)`, clamped to `0.5 ± (s − 1)/2` so no edge shows. Bias eyes into the upper third.
- Static zoom for a segment: split at the beat (`splitAt`), then `setTransform(id, keyframes="clear", x, y, scale, allowBeyondCanvas=false)` on that piece (`keyframes` is required: `clear`, `offsetAll` or `reject`). Avoid `focusX/focusY` — they have been observed to invert the y axis; set x/y yourself.
- **Split first, keyframe after.** `splitAt` on a clip that already has keyframes copies all of them to every piece, shifted (some to negative times). If you must split a keyframed clip, run `setTransform(keyframes="clear", …)` on each piece and re-add only what it needs.
- Prefer `setTransform` scale over `setCrop` for zooms: `setCrop` scales the content far more than its rect suggests (a 0.74 rect ≈ 1.8×).
- Cropping out burned-in text at the bottom of a phone take: scale ~1.3–1.4 with the centre raised (y ≈ 0.65–0.7) so the text leaves the frame; then re-check where the mouth lands before placing captions.
- Animated zoom: `setTransformKeyframe(id, time, scale, x, y)` twice (start and end), or `setTransformKeyframes(id, keyframes=JSON)` with clip-relative times; ease with `setKeyframeEasing(id, seconds, preset)` (on Edits 454: 2 = ease-out, 3 = ease-in-out). Keyframe times must fall inside the element; if rejected, the error lists valid times — read back with `getTransformKeyframes`.
- `autoReframe(ids, subject="largestFace", motion="follow")` keeps a moving subject centred (useful for 16:9 sources or walking shots) in one undo step.
- Verify every zoom with `captureFrame`: head not cut at the top, captions not on the mouth, no soft/blurry upscale (4K source tolerates ~1.25×, 1080p source ~1.12×).

## 3. B-roll, screenshots and cutouts

Use the creator's own media (screenshots, product shots, clips). Edits has no stock library through the MCP; generated images must be made outside and saved as PNG/MOV under `~/Movies/`.

- `addOverlay(path, startSeconds, x=0.5, y=0.5, scale)` — defaults to 3 s; adjust with `trim(id, side="right", deltaSeconds=−n)`. A full-frame transparent 1080×1920 PNG at x=0.5, y=0.5, scale=1 lands exactly as designed.
- After placing, `setTransform(id, keyframes="clear", …)` to reset any inherited motion, then add an entrance: scale 1.08 → 1.00 (or y slide 0.43 → 0.41) over ~0.3–0.5 s with ease-out. Transitions don't apply to overlays; fades on overlays aren't exposed — use scale/position keyframes plus a whoosh.
- Readability scrim behind an image: `addShape(x=0.5, y=0.5, width=1, height=1, color="#000000", opacity=0.35–0.45, startSeconds, duration)` then `moveToLayer(shapeId, 1)` so it sits under the image.
- 3–4 s per insert (≤12 s max), roughly one every 8–15 s on a talking head. Captions must stay readable — move them if the overlay covers their zone.
- `addStickerFromCutout(clipId)` cuts the person out (text-behind-subject looks, covers); `splitScreen(id, layout, panels, gap, background)` builds two-panel layouts (reaction, before/after).
- Alpha-friendly formats: PNG, ProRes 4444 MOV, HEVC with alpha.

## 4. Sound effects

- Search: `searchSoundEffects(query="whoosh" | "click" | "pop" | "riser", category)`; preview with `previewSoundEffect`.
- Place: `seek(seconds)` → `addSoundEffect(effect=<id or title>)` → `setVolume(id, 0.15–0.35)` (library SFX come in loud). Delete with `deleteSoundEffect(id)`.
- Tie each sound to something visible: image enters (whoosh ~0.15 s before), image leaves (softer whoosh), UI/tool on screen (single click), key number (soft tick). A low hit can close the final line.
- Density: calm talking head 3–4 per minute; energetic edits up to ~8 per 18 s. Twenty generic hits sounds like a template.
- Avoid notification pops, cartoon or game sounds unless the creator's style is comedic.

## 5. Transitions between main clips

Hard cuts are the default for talking heads. Use `addTransition(fromId, toId, filterId, durationSeconds)` (ids from `listTransitionsCatalog`) only for a scene/location change or a time jump, at most 1–2 per Reel, 0.3–0.5 s.

## 6. Check

`previewVideo(startSeconds, durationSeconds≤10, frameCount)` over each polished section to see motion, plus `captureFrame` at each overlay. Log what was added (time, type, reason) in `edit-report.md`. `saveProject`.
