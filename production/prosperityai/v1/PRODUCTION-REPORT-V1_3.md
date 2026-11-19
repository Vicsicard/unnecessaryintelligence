# ProsperityAI v1.3 — Final Polish Report

**Master:** `exports/prosperityai_v1_3_music.mp4` · 31.6 s · 1080×1920, 9:16,
h264, aac 160k, 25 fps
**Review URL:** `http://127.0.0.1:8790/prosperityai/v1/exports/prosperityai_v1_3_music.mp4`
**Base:** v1.2 — same founder (Ricky, approved), script, narration, offers.
**Incremental cost: $0** — zero new paid generation; all local assets.

## Changes

| Area | Fix |
|---|---|
| **Finale composite** | `screen_hold` was the 1080×1920 source squashed to 980×551 (29% vertical distortion). Re-cropped to a true 16:9 window (1080×608 @ y340, head+torso) → correct proportions on the mega-screen. Confetti re-rendered as masked copies (`confetti_m1-3`) with a clear zone over the founder's face region — confetti still falls over the marquee, screen edges, and auditorium. |
| **$199 card** | Upscaled 1.15× + contrast 1.08 (`tag199_big.png`, 1076×482 — near full-width). Still lands third in the sequential reveal. |
| **Pacing** | Layer staggers tightened: name 0.3→0.15s, tagline 1.6→1.1s, price 3.0→2.5s; dashboard rows 1.4→1.1 / scanline 1.6→1.35 / scan 3.0→2.7 / done 4.5→4.1; pricing tag59 0.4→0.2 / sub 1.4→1.0 / disc 2.6→2.1. Punchline holds preserved (EARN MORE MONEY still lands 15.5 abs, holds ~1.1s; $59.99 hold unchanged). |
| **Endcard** | Re-rendered `endcard_v4.html?scale=990` — logo 880→990px (91% of frame width, inside safe area). Tagline, colors, duration, sting unchanged. |
| **Audio QC fix** | Applause SFX peaked at 0.0 dBFS (borderline clip). Added `--sfx file@sec@gain_db` to `mix_music_bed.py`; applause now -4dB. New peaks: -1.6/-1.8dB at applause, -0.3dB global max, -15.4dB mean. |

## Audio QC (volumedetect)

- Full file: mean -15.4 dB, max -0.3 dB — no clipping, no dead air.
- Spot checks: open -2.0, applause@9.6 -1.8, accent@15.6 -0.7, quiet gap@20 -10.0, applause@27.2 -1.6, sting@29.9 -0.5.
- Dialogue intact (narration.wav unchanged); sting transition unchanged from approved v1.2.

## QC frames

`preview/qc13_*.png` — reveal (9.8), dashboard (15.8), ovation+confetti+fixed
screen (27.8, 28.5, 29.2), bigger endcard (30.5). Founder identity, framing,
and lip-sync untouched.

## Unchanged / preserved

Ricky founder look `94e7ae7f` (owner-approved), all three A6T clips, script,
Brock narration wavs, dashboard joke, $59.99 financing + disclaimer, V4 logo
asset, UI sting, applause/applause timing, total runtime 31.6s. v1, v1.1,
v1.2 exports all preserved on disk.
