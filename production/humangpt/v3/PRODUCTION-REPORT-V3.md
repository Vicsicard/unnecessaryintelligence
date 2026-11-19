# HumanGPT v3 — Production Report

Creative overhaul #2: breaking-news hook, per-element motion graphics,
SaaS pricing gag, **Steve speaks his own closing line**, and the new V4
UI brand card. Built on the same pipeline — no engine rebuild.

## Deliverables

| file | spec |
|---|---|
| `exports/humangpt_v3_music.mp4` | **review master** — 31.8s, 1080×1920, 25fps, h264/AAC, bed mixed |
| `exports/humangpt_v3.mp4` | same cut, narration only |
| `audio/n01..n06.wav` + `n*_chars.json` | Garret ×5 + Keanu ×1, char timestamps |
| `presenter/vp3.mp4` | Brody Office 8 speaking n06 (Keanu voice), 1080×1920 |
| `graphics/` ×6 + `graphics/steve_frame.png` | base plates (navy V4 identity) |
| `layers/` ×12 | transparent animated elements (headlines, feature rows, price card/lines, disclaimer, steve card) |
| `captions/` + `timestamps.json` | 15 ASS cues + SRT/VTT/transcript |
| `preview/qc_*.png` | 11 frame proofs |

## Storyboard (measured, 31.8s)

| shot | window | content |
|---|---|---|
| s00 | 0.0–4.6 | BREAKING bug + 3 stacked headlines slide up: JOBS AUTOMATED (0.4), ERRORS MULTIPLY (2.05), **HUMANS REQUIRED** in orange (3.05) |
| s01 | 4.6–10.5 | "INTRODUCING HumanGPT" title; STEVE™ UNIT 01 product card slides up on "actually a person" (shot-rel 4.3) |
| s02 | 10.5–16.5 | Feature dashboard — cards slide up word-timed: SARCASM DETECTION/PRE-INSTALLED (1.0), LIE DETECTION/SUSPICIOUS (1.95), MEETING PARTICIPATION/PHYSICALLY PRESENT (3.6) |
| s03 | 16.5–22.5 | NO MONTHLY SUBSCRIPTION → $84,000/YEAR enterprise card (2.3) → +HEALTH INSURANCE (3.25) +PAID TIME OFF (4.1) +UNLIMITED COFFEE (4.7) → "Emotional support sold separately." (4.75) |
| s04 | 22.5–26.1 | "THE NEXT GENERATION OF artificial intelligence is…" + Steve card fade-in (0.4) |
| s05 | 26.1–29.3 | **Steve speaks:** "Me… Steve. HumanGPT." (Keanu voice, tight crop, lip-synced) |
| s06 | 29.3–31.8 | V4 brand card, slow ken-burns zoom |

## New reusable components (pipeline additions)

- `build_video.py` → **`composite` shot type**: base plate + transparent-PNG
  layers, each with `start`/`anim` (slideup/slidedown/slideleft/slideright/
  fadein)/`travel`/`dur`, quadratic ease-out + alpha ramp — real
  per-element motion, not whole-frame swaps.
- `render_html.py` → `"transparent": true` job flag (Edge
  `--default-background-color=00000000`) for alpha layers.
- New param-driven templates (zero hardcoded product text):
  `breaking_base`, `reveal_base`, `dash_base`, `price_base`,
  `layer_headline`, `layer_feature`, `layer_pricetag`, `layer_price`,
  `layer_disclaimer`, `steve_card`, `endcard_v4`.
- `brand/assets/ui-logo-v4.png` — approved V4 logo (navy/cream/orange).
  `endcard_v4.html` keeps logo asset / background / animation separate.
- `ui-presenter-lock.json` → `steve_voice` block: **Keanu**,
  `80f988d41e454baa8d20e0e0ddfe050d` (en-US, Crisp & Approachable).
- `broll` image → ken-burns used for the endcard (existing capability).

## Identity / voices

- Narrator: Garret `f49763c1a284420b8f25f16472d8738e` (unchanged)
- Steve on-camera: Brody Office 8 `e0337c592ccd408c937337a6a33f9fee` (unchanged)
- Steve voice: Keanu `80f988d41e454baa8d20e0e0ddfe050d` (new, locked)
- n06 rendered via `script_steve.json` before `script.json` so the Garret
  pass skips the existing wav (idempotent no-rebill).

## Cost (actual, Developer API wallet)

| item | observed |
|---|---|
| TTS ×6 | $0.00 shown (3.47 → 3.47) |
| Avatar render ×1 @1080p/9:16 (vp3) | $0.12 (3.47 → 3.35) |
| Music, plates, captions, render | $0 |
| **Incremental total** | **≈$0.12** |

## vs v2

- First-second hook (breaking-news headline stack vs slow title).
- Per-element motion: each row/line/price animates independently (v2 was
  whole-plate xfade swaps).
- Pricing gag as sequential reveal; disclaimer lands last.
- Steve speaks his own line in a distinct voice — the punchline.
- V4 logo endcard with broadcast-style zoom (reusable for every UI ad).

## Limitations

- Reveal/tease use a still frame of Steve inside a product card (the live
  clip exists only for his spoken line). If a moving Steve is wanted in the
  reveal, that is one extra paid render (~$0.12).
- "Triumphant sting" is the same corporate bed, not a bespoke sting track.
- Feature-row title "MEETING PARTICIPATION" wraps to two lines inside its
  card — readable, retained.
- Meme companion still unproduced (template exists).
