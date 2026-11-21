---
name: edits-cover
description: "Creates the cover (thumbnail) for an Instagram Reel from an Instagram Edits for Mac project — picks the strongest frame (clear expression, eyes open, readable action), hides captions, adds a short cover title, text-behind-subject looks with cutouts, and keeps everything inside the 3:4 profile-grid crop. Use whenever the user asks for a cover, thumbnail, portada, capa, \"the image people see on my profile grid\", or wants the grid to look consistent."
---

# Reel cover

The cover sells the Reel on the profile grid and in shares. It's shown in a 3:4 crop on the grid and 9:16 in the feed, so the important part must survive both.

## 1. Find the frame

- Sample candidates: `frameSheet(times="…", columns=4, cellWidth=270)` (empty id = the edit) every 1–2 s, or around the hook and the punchline.
- Choose a frame with a clear, expressive face (mouth not mid-word, eyes open), or the most legible visual of the topic. Avoid motion blur and transitions.
- Hide captions and overlays at that moment for a clean plate: `setTextVisibility(id, false)` on the captions/text at that time (restore after).

## 2. Title text

- 2–5 words that name the topic or the tension — not the full hook. Big, high contrast, one accent word at most.
- Keep text inside the 3:4 crop: vertically between y ≈ 0.13 and 0.85 of the 9:16 frame, horizontally ≥ 5% margin.
- Build with Edits' fonts so the grid matches the Reels: `addText`, `setTextFont`, `setTextStyle`, `setTextPosition`. Capture with `captureFrame(atSeconds, maxWidth=1080)`.

## 3. Text behind the subject (optional)

1. `addStickerFromCutout(clipId)` → a masked overlay of the person.
2. Place the title text, then `moveToLayer` so the cutout sits above the text — the person appears in front of the letters.
3. Capture the frame; then delete the temporary cutout/text so the Reel itself is unchanged.

If compositing needs pixel control (a mask, a layout across several frames), capture the frames with `captureFrame` and compose with an image tool outside Edits (e.g. Pillow), saving the cover under `~/Movies/<project>/export/`.

## 4. Deliver

- Save as JPG 1080×1920 (and a 1080×1440 3:4 preview so the user sees the grid crop).
- Restore any hidden text, remove temporary elements, `saveProject`.
- The cover is chosen in Edits' share screen (or Instagram's) when posting — tell the user where the file is; the MCP can't set it on the post.

## Grid consistency

If the user wants a recognizable grid, record the cover rules in `edits-style.md`: font, size, position, accent color, framing (e.g. face on the left third, title on the right).
