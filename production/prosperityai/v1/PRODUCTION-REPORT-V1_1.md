# ProsperityAI v1.1 — Production Report

**Master:** `exports/prosperityai_v1_1_music.mp4` · 31.6 s · 1080×1920, 9:16,
h264, aac 160k, 25 fps
**Review URL:** `http://127.0.0.1:8790/prosperityai/v1/exports/prosperityai_v1_1_music.mp4`
**Base:** v1 (`prosperityai_v1_music.mp4` preserved untouched)

## What changed from v1

| Requirement | Implementation |
|---|---|
| Keynote stage environment | New `keynote_stage.html` plate: dark auditorium, spotlight beams, LED mega-screen, deck + audience silhouettes (open / `ovation=1` raised-arms variants, marquee param). Founder clips now play **inside the LED mega-screen** via new composite **video layers** — the actual keynote convention (speaker on the giant screen). |
| Stronger opening | Stage plate opens the spot — "POVERTY ENDS TODAY" marquee + founder (A6T, open-hand gestures) on the mega-screen within the first second. |
| Sequential $199 reveal | `reveal_blank.png` plate + three separate animated layers: `name.png` (0.3s) → `tagline.png` (1.6s) → `tag199.png` (3.0s). Applause stays at 9.4s. |
| Dashboard punchline | Unchanged rows + new **scanline sweep** (slides down across rows on "analyzes", then fades out via new layer `out` param) + **accent chime** at 15.5s when "EARN MORE MONEY." lands. |
| Weekly financing | Founder returns on the mega-screen under "FINANCIAL INCLUSION INITIATIVE" marquee; full-screen pricing beat preserved (reads as cutting to the screen's content). |
| Standing ovation finale | `stage_ovation.png` — raised-arm silhouettes + confetti (staggered 1.2/1.8/2.4s) + applause at 26.0s + **5.8s hold** so the line lands before branding. |
| Permanent UI endcard | New `endcard` shot type (`standard`/`flash` variants, manifest-configurable, auto-append default `ui_endcard: true`) + **new synthesized UI sting** (`tools/make_ui_sting.py`) at 29.8s. 1.8s standard close. |

## Avatar 6 Turbo founder (new)

- `presenter_avatar6/vp1_a6t.mp4` (n01 — reused from the controlled test), `vp2_a6t` (n04), `vp3_a6t` (n05) — all `heygen-avatar-6-turbo` with a keynote motion prompt.
- Letterbox measured per-clip: content band rows 656–1263 → layer crop `1080:608:0:656` yields a clean 16:9 feed in the screen.
- **Identity preserved** — same Sebastian face/blazer; motion visibly upgraded (open-palm presenting gestures vs Avatar IV's static desk posture).

## Cost

- 2 new A6T renders (vp2 2.39s + vp3 4.06s): **$0.30** actual (wallet 2.82→2.52, ~$0.046/s)
- vp1_a6t reused from prior test ($0.15, already reported) — **v1.1 incremental: $0.30**
- Everything else local/free.

## Pipeline additions (reusable)

- `composite` **video layers** (`video`, `crop`, `w`, `h`, same anim/fade system) — any clip can play inside a graphic plate.
- Layer **`out`** param — fade-out at a shot-relative time (scanlines, flashes).
- `endcard` shot type + **`ui_endcard` auto-append** (back-compat detection: last shot referencing `endcard` counts; `ui_endcard: false` opts out). `standard` (≤2s, zoom+fade) and `flash` (≤1.5s) variants.
- `tools/make_ui_sting.py` — deterministic synthesized **sting + accent chime** (no deps, regenerable; wav output is gitignored media).
- `brand/templates/keynote_stage.html` — param-driven stage plate (marquee, ovation flag).

## QC

`preview/qc11_*.png` — stage open (1.8), sequential reveal (6.5/9.8), dashboard
punchline (15.8), inclusion stage (17.8), pricing (21.5), ovation + confetti
(27.0), V4 endcard (30.5). Audio spot-checks at 15.5/29.8s — clean peaks, no
clipping.

## Deviations & honest notes

- The founder is still a **seated office shot on the mega-screen** — no
  stage/standing look exists for Sebastian, and generated stage B-roll would
  violate the API-only billing rule (no Developer API text-to-video path in
  our tools). The screen-feed framing is a real keynote convention; a true
  on-stage wide shot remains the known limitation.
- "Cinematic camera movement" is represented by layer motion, confetti, and
  the endcard zoom — not a physical dolly.
- Audience is silhouettes; standing ovation = raised-arm variant + applause SFX.
- Sting/accent are synthesized tones (no licensed sting asset) — distinctive
  and reusable; replaceable later with a licensed sting if preferred.
