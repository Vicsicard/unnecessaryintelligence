# Episode 4 — StudyBro AI — Assembly Report V1 (First Review Cut)

**Status:** review candidate, awaiting user approval. No publication.
**Exports:**
- `exports/ep4_reel_v1.mp4` — 34.34 s (Social Reel, 0.6 s V4 flash)
- `exports/ep4_master_v1.mp4` — 35.54 s (Editorial Master, 1.8 s V4 endcard)
- Review: `http://127.0.0.1:8790/ep4/exports/ep4_reel_v1.mp4` / `.../ep4_master_v1.mp4`

## Source footage (all 720x1280 @ 24 fps, audio present, originals untouched)

| File | Length | Content | Speech bursts (silence-mapped) |
|---|---|---|---|
| `source/s01.mp4` | 10.24 s | Teacher + StudyBro AI deck + headphone students | 0–3.07 / 3.51–7.35 / 7.91–10.24 |
| `source/s02.mp4` | 10.24 s | Purple podcast studio, "StudyBro AI Podcast Studio" + "U.S. History Podcast" baked in | 0–3.95 / 4.45–6.49 / 6.71–10.24 |
| `source/s03.mp4` | 10.24 s | Classroom payoff, teacher stunned closeup | 0–2.05 / 3.16–3.42 / 3.94–4.50 / 5.12–5.90 / 6.93–7.65 / 8.29–9.83 |

Dialogue timing was measured by silence detection, not transcription — wording below is inferred from the approved script.

## Edit timeline (reel = master story track)

| Time | Source | Content |
|---|---|---|
| 0.00–9.41 | s01 `[0–3.07]+[3.35–7.35]+[7.7–10.24]` tightened | Teacher intro, all three lines kept; internal dead air trimmed 0.63 s. `graphics/hook.png` "AI JUST REPLACED YOUR TEXTBOOKS?!" overlays 0.25–2.65. |
| 9.41–19.65 | s02 `[0–10.24]` full | Podcast: Washington invented America → funding? → Series A / France → Brooooo. plug_blip transition SFX at 9.35. |
| 19.65–25.57 | s03a `[0–5.9]` | "Who funded the American Revolution?" → 1.1 s dead air → "France." → "Series A." (+ series_a_ding at 23.65) |
| 25.57–29.55 | s03b `[5.9–9.9]` | Teacher stunned hold — punch-in zoom 1.0→1.11. drop_sweep at 25.2. |
| 29.55–33.95 | `graphics/product_card.png` | StudyBro AI. LESS STUDYING. MORE CONFIDENCE. (SAPI temp VO) |
| 33.95–end | V4 endcard | Reel: 0.6 s flash / Master: 1.8 s standard + UI sting at 33.95 |

## Captions

`captions/ep4.ass` — Inter 58, white + dark outline, purple (&HFF5CB4) on REPLACED / GEORGE WASHINGTON / SERIES A / FRANCE. Line-level timing from silence map, not word-level karaoke.

## Audio

narration = s01+s02+s03a+s03b source audio + SAPI tagline VO (rate 1). Bed = shop_bed (128 bpm electronic) -12 dB, sidechain-ducked. SFX: open_hit @0, plug_blip @9.35, series_a_ding @23.65, drop_sweep @25.2, ui_sting @33.95. Peaks at limiter (~0 dBFS).

## Detected issues / flagged for review

1. **Runtime 34.3 s > 22–28 s target.** All approved dialogue + baked comedy pauses kept per "humor > runtime". Trim options below.
2. **s03 contains ~3.3 s of speech beyond the scripted Q&A** (bursts at src 5.12–5.90, 6.93–7.65, 8.29–9.83) — likely teacher stammer/reaction. Kept; verify it's intentional, not babble.
3. **Tagline VO is SAPI temp** (clear, robotic). HeyGen Wade (the ep3 voice) is one call away — held per "no paid calls" instruction.
4. Captions are line-level, not karaoke word-sync — word timing needs a transcript pass or manual timing.
5. No word-level verification of "Series A" ding timing (placed at measured "Series A." burst 23.59–24.15).

## Does the joke land?

Yes — structure reads cleanly: hook (0–9.4) → absurd podcast (9.4–19.6) → payoff with visible stunned teacher + baked dead-air (19.6–29.5) → tagline card. The teacher's reaction face is unobstructed during the punch-in.

## V2 options (awaiting review)

- **Hit ~30 s:** drop s01 line 3 ("learn without reading?" −2.3 s) and trim s03 tail to 8.4 (−1.5 s).
- **Hit ~28 s:** also shorten product card to 3.2 s (requires faster VO or Wade).
- HeyGen Wade tagline VO swap.
- Word-level karaoke captions (needs transcript timing).
- Optional paid Meta QC pass (~cents) for dialogue-vs-brief check.
