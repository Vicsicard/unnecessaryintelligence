# ProsperityAI v1 — Production Report

**Campaign:** 002 — ProsperityAI · **Master:** `exports/prosperityai_v1_music.mp4`
**Runtime:** 31.6 s (target 28–32) · **Specs:** 1080×1920, 9:16, h264, aac 160k, 25 fps
**Review URL:** `http://127.0.0.1:8790/prosperityai/v1/exports/prosperityai_v1_music.mp4`

## Concept delivered

A sincere tech founder announces the end of poverty — via a $199/month
subscription — then "solves" affordability with $59.99/week financing that
costs more over time. Comedy lives in the contradiction; the founder never
acknowledges it.

## Founder identity (locked, reusable)

| | |
|---|---|
| Character key | `prosperityai_founder` in `config/ui-presenter-lock.json` |
| Avatar | **Sebastian Office 11** — look `f00a2f4b726e4808866d4740ede6e1e0` |
| Group | Sebastian `ea6b5b730b12471f9d21f583aa024713` |
| Voice | **Brock — Confident & Persuasive** `4fb113051a204040826fddb19f29c21c` |

Chosen over Dante (too young) and Dashiell (reads junior/casual). Mature,
blazer, polished keynote confidence. Preflight passed via the new
`verify_presenter.py --character` flag.

## Script & timing (as produced)

All five approved lines used verbatim. Brock TTS, word-level timestamps
extracted for layer triggers. Measured narration 31.60 s.

| Beat | Start | Dur | Line |
|---|---|---|---|
| n01 | 0.00 | 3.29 | "Today, we're announcing the end of poverty." |
| n02 | 4.20 | 5.21 | "Introducing ProsperityAI. Just $199 a month." |
| n03 | 10.20 | 4.94 | "Our AI analyzes your finances and tells you exactly how to become wealthy." |
| n04 | 16.60 | 2.39 | "Can't afford it? We've thought of that too." |
| n05 | 24.00 | 4.06 | "Because nobody should be too poor to afford the end of poverty." |

## Scene-by-scene (`manifest_v1.json`, 7 shots)

| Shot | Dur | Type | Content |
|---|---|---|---|
| s00 | 4.2 | composite (video base) | Founder closeup + **POVERTY ENDS TODAY** headline (slidedown @0.5s) |
| s01 | 6.0 | composite | Product reveal — INTRODUCING ProsperityAI™ / END POVERTY FOREVER, then $199/MO card slides up on "$199" |
| s02 | 6.4 | composite | Financial dashboard — MONTHLY INCOME $1,800 → DEEP ANALYSIS (ANALYZING) → ANALYSIS COMPLETE → **EARN MORE MONEY.** punch @5.3s (held ~1.1s to shot end) |
| s03 | 3.0 | presenter | Founder: "Can't afford it? We've thought of that too." |
| s04 | 4.4 | composite | FINANCIAL INCLUSION INITIATIVE — $59.99/WEEK card, "Financial freedom. Now with convenient weekly payments.", "Financing available to qualified applicants." disclaimer |
| s05 | 5.0 | composite (video base) | Founder closing line + staggered confetti (3 layers, slidedown 0.8/1.4/2.0s) |
| s06 | 2.6 | broll | UI V4 endcard — navy, zoom, UNNECESSARY INTELLIGENCE / "Advancing humanity against its will." |

## Audio

- Founder beats: Brock TTS ×5 → `audio/n0{1..5}.wav`, assembled `narration.wav`
- Music bed: HeyGen audio `310662767a134b208b6bf1eb21f03efa` (tech-keynote,
  33 s), −10 dB, sidechain-ducked under narration, faded tail
- Applause SFX: HeyGen `0a051ee00d11c49e` (3.36 s crowd applause), placed at
  9.4 s (post-$199 reveal) and 24.6 s (final line)
- Mix: `tools/mix_music_bed.py` — now supports reusable `--sfx file@seconds`
- Burned-in `.ass` captions throughout

## Pipeline additions this campaign (reusable)

- `build_video.py` — `composite` accepts **video base** (founder clip +
  animated layers) and **`base_crop`** ("w:h:x:y") to strip baked-in
  letterbox bands from avatar renders before filling frame
- `mix_music_bed.py` — `--sfx file@seconds` (each SFX added as ffmpeg input,
  `adelay`-placed, `amix`ed with narration + ducked bed)
- `verify_presenter.py --character` + `characters` map in presenter lock —
  multi-character locks (founder coexists with Steve)
- ProsperityAI graphics: `graphics/{reveal,dash,price,endcard}.png` plates,
  transparent layers `layers/{h1,tag199,inc,scan,done,punch,tag59,sub,disc}.png`,
  `graphics/confetti_{1..3}.png`

## Incremental cost

- 3 founder avatar renders (vp1/vp2/vp3): **~$0.36** (wallet 3.33 → 2.97)
- Brock TTS: $0.02
- Music/applause assets: included in plan
- **Total incremental: ~$0.38**

## Script deviations

None — all five approved lines delivered verbatim.

## Production notes & resolved defects

- **Letterbox on founder clips:** HeyGen renders ship white bands top/bottom.
  `base_crop 1080:800:0:620` on s00/s05 (and `crop` on s03) removes them —
  same treatment as HumanGPT v2/v3.
- **`sub.png` clipping/invisible:** first Edge render clipped the 42-px line
  horizontally; a retry with the single-shot CLI produced wrong output
  (single-shot mode takes no params), and a `--jobs` re-render produced a
  near-invisible alpha layer (small-height transparent renders are flaky on
  this machine — same symptom as v3's `disc.png`). Final `sub.png` was
  generated with PIL (Inter-SemiBold 30 px, centered, 846 px wide).
- `disc.png` likewise PIL-generated after repeated Edge hangs.

## Known limitations

- Keynote "stage" is Sebastian's office setting cropped tight — the scale
  of the venue is implied by graphics/confetti/applause rather than a
  literal wide stage shot (no stage-environment avatar look available).
- Confetti is a PNG layer drifting down over the founder closeup, not
  video-generated physics.
- End "sting" is the same corporate bed (no bespoke sting asset yet).
- Applause is one crowd clip used twice; the "standing ovation" is audio +
  confetti implication.

## QC frames

`preview/qc_*.png` — opening (1.5), reveal+$199 (5.5/9.0), dashboard +
EARN MORE MONEY (16.0), affordability line (17.8), $59.99/week + sub +
disclaimer (21.0/23.0), confetti finale (26.5), V4 endcard (30.5).
