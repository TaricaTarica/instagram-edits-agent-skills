# Changelog

## 0.1.0 — 2026-11-20

Tested with Edits for Mac 454, automation schema `2026.10.19-1` (32 home tools, 274 editor tools).

- 14 skills: `edits-reel`, `edits-operate`, `edits-style-learn`, `edits-clip-pick`, `edits-rough-cut`, `edits-hook`, `edits-captions`, `edits-polish`, `edits-audio`, `edits-color`, `edits-montage`, `edits-cover`, `edits-variants`, `edits-qa`.
- QA helpers: `safe_zone_overlay.py`, `export_gate.py`.
- Verified on the live server: `transcriptJumpCut` is mentioned in tool descriptions but not exposed publicly (rough cut uses `splitAt` + `quietPoint`); `processAudio` chain steps and params; `addMedia` audio kinds (`music`, `soundEffect`, `voiceover`); `setCaptionHighlights` returns no highlights; new projects default to 2160×3840 60 fps HDR.
