# Changelog

## 0.1.0 — 2026-11-20

Tested with Edits for Mac 454, automation schema `2026.10.19-1` (32 home tools, 274 editor tools).

- 14 skills: `edits-reel`, `edits-operate`, `edits-style-learn`, `edits-clip-pick`, `edits-rough-cut`, `edits-hook`, `edits-captions`, `edits-polish`, `edits-audio`, `edits-color`, `edits-montage`, `edits-cover`, `edits-variants`, `edits-qa`.
- QA helpers: `safe_zone_overlay.py`, `export_gate.py`.
- Verified on the live server: `transcriptJumpCut` is mentioned in tool descriptions but not exposed publicly (rough cut uses `splitAt` + `quietPoint`); `processAudio` chain steps and params; `addMedia` audio kinds (`music`, `soundEffect`, `voiceover`); `setCaptionHighlights` returns no highlights; new projects default to 2160×3840 60 fps HDR.
- End-to-end test on a 34 s talking head (cut → hook → color → audio → captions → polish → QA → export + one variant): export passed every gate check (1080×1920, −13.9 LUFS, −1.1 dBTP). Fixed 24 skill defects it surfaced, including: `processAudio` normalize has no limiter (new −14 LUFS recipe via clip gain + Voice Enhance), caption timing drift after cuts (sync check + fallback), `editCaption` resetting color/size, `mergeCaptions` directions, `splitAt` copying keyframes to every piece, required params (`addMedia.audioKind`, `setTransform.keyframes`, analysis `duration`), hook text size and animation, burned-in source captions, `frameSheet` for frame files, export timing, `--expect-fps` in the export gate.
- Demo montage built in Edits with the skills (8 licensed stock clips, beat grid from `audioOnsets` at 114.8 BPM, 16.8 s, −15.4 LUFS, all gate checks passing). Learned and documented: `beatMarkers` can stay empty even after `setBeatDensity`; `audioOnsets` returns `bpm`; `trim(side="right")` doesn't shorten main-track clips (use `splitAt` + `delete`); `splitAt` gives every piece a new id; short titles read best with no text animation and ~16–18 characters per line at size 32.
- README: demo GIF, skills.sh badge, license credits for demo media; removed third-party product names. Added CONTRIBUTING, issue templates and `maintainer/check_edits_tools.py` with an editor-screen snapshot.
