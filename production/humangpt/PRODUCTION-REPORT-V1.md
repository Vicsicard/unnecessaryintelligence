# HumanGPT v1 — Production Report

First UI production, built end-to-end through the ported MALB pipeline on
`init/project-foundation`. No existing DIG project touched.

## Deliverables

| file | spec |
|---|---|
| `exports/humangpt_v1.mp4` | 23.56s, 1080×1920, 25fps, h264/yuv420p, AAC 48kHz, burned ASS captions — narration only |
| `exports/humangpt_v1_music.mp4` | same master + ducked corporate bed (video stream-copied, audio remixed) |
| `audio/n01..n04.wav` + `n*_chars.json` | Garret TTS beats w/ char timestamps |
| `presenter/vp1.mp4`, `vp4.mp4` | Brody Office 8 renders — **true 1080×1920 9:16** |
| `graphics/*.png` ×6 | title, claim_0–3, endcard (from `render_jobs.json`) |
| `captions/` | narration.ass (12 cues), .srt, .vtt, transcript.txt |
| `timestamps.json` | word map driving graphic state switches |
| `preview/qc_*.png` | frame proofs: presenter, claim plate, reveal line, endcard |

## Identity used

- Narrator: **Garret** `f49763c1a284420b8f25f16472d8738e` (public catalog,
  "Bold & Persuasive", en-US) — deadpan corporate-ad read.
- Steve: **Brody Office 8** `e0337c592ccd408c937337a6a33f9fee`
  (group `469ba809c9f6441ba74a580058d41c4b`) — public photo avatar.
- Bed: HeyGen catalog `01483ce1` "inspiring corporate tech-agency" 33s,
  sidechain-ducked −26dB under narration, fade in/out.

## Timeline (measured)

n01@2.5(4.99s) n02@7.9(3.20s) n03@11.5(4.65s) n04@16.6(4.61s); total 23.5.
Shots start exactly at beat starts (lip-sync rule); claim_1 lights at
"sits" (+2.0 into s02), claim_3 at "and" (+2.1 into s03); endcard 2.0s hold.

## Cost (actual, Developer API wallet)

| item | observed |
|---|---|
| TTS ×4 (Garret) | $0.00 shown (wallet 4.05 → 4.05 — sub-cent or included) |
| Avatar renders ×2 @1080p/9:16 | $0.33 (4.05 → 3.72) |
| Music / plates / captions / render | $0 |
| **Total** | **≈$0.33** (wallet remaining $3.72) |

## Verified notes

- Landscape-preferred photo avatar **does** render true 9:16 via
  `aspect_ratio:"9:16"` on /v3/videos — no crop fallback needed. Steve is
  letterboxed inside the portrait frame; reads as intentional.
- PREFLIGHT PASS on the locked look before any paid render.
- Duration preflight held: video 23.56s vs narration 23.50s (< 0.5 tol).
- Captions: cue on "HumanGPT. The future of" confirmed at reveal frame.
- Defects fixed during build: `mix_music_bed` `weights=1,1` filter parse.

## Outstanding polish candidates (v1.1)

- No cold-open gag — hook is tonal only.
- Steve's white letterbox bands could be replaced with brand plates if a
  portrait-native look is created later.
- Optional SFX sting on endcard.
- Meme companion (template ready: `brand/templates/meme.html`).
