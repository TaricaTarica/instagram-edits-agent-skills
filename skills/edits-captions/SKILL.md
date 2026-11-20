---
name: edits-captions
description: Adds and styles auto captions (subtitles) on Instagram Reels inside Instagram Edits for Mac — generate captions, pick one of 73 caption styles (one-word pop, karaoke word highlight, two-line phrase), emphasize keywords, fix misheard words and brand names, keep captions inside the Reels safe zone and readable on any background, bilingual captions. Use whenever the user mentions captions, subtitles, subtítulos, legendas, "words on screen", highlighting keywords, caption style or font, or captions covering the face or the Instagram UI — even if they don't say "Edits".
---

# Captions in Edits

Most Reels are watched muted at first. Captions carry the hook and keep people reading, so they must be accurate, readable in one glance and never under Instagram's UI.

Do captions **after** the rough cut (cuts ripple captions) and before overlays (so you can see collisions). If `edits-style.md` exists, use its archetype, fonts, colors and position.

## 1. Pick an archetype

| Archetype | Words per screen | Edits styles to start from | Use for |
|---|---|---|---|
| One-word punch | 1 | `Short Hard Cut`, `Short Pop` (+ numbered variants) | fast talking head, high energy |
| Karaoke highlight | 3–6, active word lit | `Word Highlight`, `Word Highlight Box`, `Highlighter` | most talking heads (default) |
| Phrase | 5–7 per line, max 2 lines | `Simple`, `Soft Lines`, `Fade In` | calm, story, educational |
| Themed | varies | `Retro future`, `Hot take`, `PRINT SHOP`, `Jazz club`… | personality pieces, sparingly |

Rules of thumb: 2–3 words for high energy, 3–5 conversational, 4–6 calm. A caption shorter than 0.35 s on screen can't be read. Full list: `listCaptionStyles` (73 entries: 39 caption styles plus text presets).

## 2. Build them — order matters

Several caption tools reset typography, so follow this order:

1. `generateCaptions(language, source="video", curseWords=false)` — ~10 s for 30 s of speech. Running it again creates a **second full set** on top; delete the old one with `deleteCaptions(id)` per caption (or no id for all) first.
2. `setCaptionStyle(style)` — no `id` restyles every caption; pass `id` to restyle one. Restyling resets fonts.
3. `splitCaption(id, time)` / `mergeCaptions(id, direction="left"|"right")` — fix phrase breaks: break on punctuation or pauses ≥0.15 s, never split a name or number. Splitting resets the font of both halves.
4. `editCaption(id, text)` on every caption that needs it (see §3). `editCaption` resets color and size, so it must come before step 5.
5. Fonts and colors last: `setTextFont(id, family)` (ids from `listCatalog(kind="font", query=...)`; `listFonts` returns only the first page), `setTextStyle(id, size, color, bold, alignment)`, `setEmphasis(id, style, color)` for outlines. Box-style caption presets (`Word Highlight Box`…) ignore `backgroundPill`; pick a box style instead.

## Check sync before styling

Caption timing comes from the composition audio. After a rough cut, word times can come out early (over a second has been seen on the first clip). Spot-check: `captureFrame` at the start time of 3–4 captions spread across the Reel and compare with the transcript's word times.

If a span is off:
- Delete those captions (`deleteCaptions(id)`) and run `generateCaptions` again **after** the cut is final — then delete the duplicates it creates elsewhere.
- If it is still off, rebuild that span with `addText` elements timed from `transcribeClip` word times and styled like the captions.
- Don't `move` or `trim` karaoke captions to fix timing: the word highlighting keeps the old word times (text vanishes outside them), and `trim` after `move` has extended captions by seconds.

`captions` lists every caption with id, text and times; `getElement(id)` shows the applied style, font, size and color.

## 3. Fix the text

- Read every caption against what was said. Auto captions mishear brand and technical names (e.g. "Claude" → "cloud"), names of people and places, and numbers.
- Decide case and punctuation once and apply everywhere: many creators use lowercase without commas or final periods; keep question/exclamation marks only if the style shows them well.
- Remove filler words that survived the rough cut; keep the creator's signature expressions if their style says so.
- Accents and spelling must be correct — a typo in a caption reads as carelessness.

## 4. Emphasize keywords (5–8 per minute)

Pick words that carry meaning: the twist, the number, the named thing, the feeling. Not articles, not every noun.

- `setCaptionHighlights(id, words)` and `setCaptionHighlightColor(color)` exist, but on Edits 454 highlights returned empty — verify with `getElement` and fall back if nothing changed.
- Reliable fallback: `splitCaption` so the keyword is its own caption, then style it differently with `setTextFont` / `setTextStyle(color, size ~1.3× body)` / `setEmphasis`. One accent color for all keywords; don't rainbow.

## 5. Placement and safe zone (1080×1920 reference)

Instagram covers the top ~210 px (header), bottom ~340–420 px (caption, audio, buttons) and right ~100 px (like/comment/share rail).

- Keep caption centres between **y ≈ 0.62 and 0.75** (normalized), x centred, line width ≤ ~78% of frame. Never below y ≈ 0.77.
- Edits' default caption position puts two-line captions right on the edge of the zone Instagram covers with long post captions — check with `edits-qa`'s overlay script and raise them (≈0.70) when lines wrap.
- Move them with `setTextPosition(id, x, y)` — apply to every caption.
- Never cover the mouth or eyes. If the subject sits low in frame, raise captions above the chest rather than lower.
- If captions must go to the top (e.g. burned-in text at the bottom), hide or shorten the captions that overlap the on-screen hook during its 2.5–3.5 s — never stack hook text and captions in the same band.
- Style flags like hiding punctuation don't always apply; remove punctuation in the text with `editCaption` if the style needs it.
- When an overlay or screen recording shows UI, move captions lower (still inside the zone) for that span so they don't hide what's being explained.
- On busy or light backgrounds (white shirt, bright wall) add `setEmphasis(style="outline")` or a pill background; white on white with a thin stroke is unreadable.

## 6. Verify

`captureFrame(times=...)` at 4–5 moments: first caption, a keyword, a long line, the densest moment. Check readability at phone size, no collisions with face or overlays, consistent font after splits. `saveProject`.

## Bilingual captions

Duplicate the caption text in a second language with `addText` per phrase (timed to each caption), smaller and in a second line above the main caption, or deliver a second project via `duplicateProject` with translated `editCaption`s. Claude translates; keep line length within the safe zone.
