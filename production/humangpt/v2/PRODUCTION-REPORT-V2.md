# HumanGPT v2 — Production Report

Creative overhaul of v1 on the same pipeline — new script, dark keynote
typography system, directional motion graphics, portrait-native Steve.

## Deliverables

| file | spec |
|---|---|
| `exports/humangpt_v2_music.mp4` | **review master** — 26.9s, 1080×1920, 25fps, h264/AAC, bed mixed |
| `exports/humangpt_v2.mp4` | same cut, narration only |
| `audio/n01..n05.wav` + `n*_chars.json` | Garret beats w/ char timestamps |
| `presenter/vp1.mp4` (n02), `vp2.mp4` (n05) | Brody Office 8, 1080×1920 |
| `graphics/` ×10 | title_0/1, feature_0–3, warn_0–2, endcard |
| `captions/` + `timestamps.json` | 12 ASS cues + SRT/VTT/transcript |
| `preview/qc_*.png` | 8 frame proofs |

## Storyboard (measured)

| shot | window | content |
|---|---|---|
| s00 | 0–5.9 | Launch title: "AI replaced your employees." → line2 slides up at "Now" (3.32) |
| s01 | 5.9–9.2 | Steve tight-crop fullscreen: "HumanGPT. Powered by Steve." |
| s02 | 9.2–15.2 | Feature dashboard — rows slide up word-timed: hallucinations(0.51) / sarcasm(2.30) / meeting-aware(4.01) |
| s03 | 15.2–19.6 | Known-limitations panel — Coffee CRITICAL (0.81), management tolerance 41% (2.99) escalate in |
| s04 | 19.6–24.4 | Steve closeup delivers the punchline |
| s05 | 24.4–26.9 | UI endcard |

## Pipeline upgrades shipped in tools (reusable)

- `build_video.py` — `graphic` shots now accept `"transitions"` (any ffmpeg
  xfade: slideup/wipeleft/…) via chained-xfade rendering; `presenter` shots
  accept `"crop": "w:h:x:y"` (source crop before fill/inset — removes
  letterbox bands, enables portrait-native framing).
- New param-driven templates: `open_title.html`, `feature.html`,
  `warning.html` — reusable for ProsperityAI/FridgeWitness, no product text
  hardcoded.
- `mix_music_bed.py` — weights-syntax fix (first real use).

## Cost (actual, Developer API wallet)

| item | observed |
|---|---|
| TTS ×5 | $0.00 shown (3.72 → 3.72) |
| Avatar renders ×2 @1080p/9:16 | $0.25 (3.72 → 3.47) |
| Music (catalog `01483ce1`), plates, captions, render | $0 |
| **Incremental total** | **≈$0.25** |

## Improvements vs v1

- Script: stronger cold-open + escalations ("coffee: CRITICAL", "tolerance
  for management: 41%", "trained on 40,000 British sitcoms" sub-jokes).
- Typography: oversized editorial headlines, index/tag hierarchy, dark
  keynote field — vs light claim cards.
- Motion: directional slide-up reveals synced to narration words — vs
  static plates + alpha fades.
- Steve: `crop` fills the frame (portrait-native closeup) — vs letterboxed.
- Retention: meaningful visual change every ~3–5s; endcard holds 2.5s.

## Known limitations

- Transitions are directional wipes, not per-element kinetics (each state
  is a full-frame still — no independent row motion). If finer motion is
  wanted, options are video-rendered plates or a heavier tool — not needed
  for this bar.
- Music bed is a 33s catalog loop (fine at 26.9s).
- Meme companion still unproduced (template ready).
