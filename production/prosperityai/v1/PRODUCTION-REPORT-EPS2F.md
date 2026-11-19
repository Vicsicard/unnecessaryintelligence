# ProsperityAI Episode 2 — Expanded Final Report

**Candidate master:** `exports/prosperityai_eps2_final_candidate.mp4` · **17.72s** · 1080×1920, 25fps, h264+aac
**Review URL:** `http://127.0.0.1:8790/prosperityai/v1/exports/prosperityai_eps2_final_candidate.mp4`
**Source:** `prosperityai_eps 2e.mp4` (owner-supplied, preserved untouched in `eps2e/source.mp4`)
**Incremental cost: $0** — zero new paid generation.

## What was added (eps2e 10.24s → 17.72s)

| Span | Content |
|---|---|
| 0–10.24 | **eps2e untouched** — globe/confetti keynote, $999 PER MONTH card, EARN MORE MONEY overlay, live crowd |
| 10.24–12.79 | Founder add-on: existing clip `r2_n04` — "Can't afford it? We've thought of that too." (Brock voice, A6T open-hand gesture) + word captions |
| 12.79–16.09 | Analysis card: **ANALYSIS COMPLETE** row @0.35 → giant **EARN MORE MONEY.** punch-in @1.25 + accent chime @14.05 |
| 16.09–17.72 | Standard **1.8s UI endcard** (big V4 logo, navy/cream/orange, tagline) + UI sting @16.05 |

## Pipeline fixes

- `composite` video bases lacked `fps=` conversion — a 24fps base produced a
  24fps segment that stream-copy concat stretched (~+0.75s phantom duration).
  Fixed: `fps={self.fps}` now applied to all composite bases.
- Mix wrote to its own input — worked around by exporting video then muxing.

## Identity note (honest)

The add-on uses the owner-approved API look `94e7ae7f` (Ricky stage — gray
blazer/turtleneck, blue LED grid). eps2e's founder is a **sibling look** —
same wardrobe and character family, slightly different face/hair render
(eps2e was produced outside this pipeline, so its exact look ID is unknown).
Same founder *character*; if a pixel-exact face match is required, supply
eps2e's look ID and I'll re-render the add-on on it (~$0.15, needs
authorization).

## Paid alternative not used

The spec's suggested exchange ("Can't afford it? Good news. Our AI
recommends earning more money.") would need one new A6T render (~4–5s,
est **$0.20–0.25**). Zero-cost path delivered the same joke structure with
existing audio — say the word and I'll render the exact wording.

## QC

Frames `preview/qf_*.png` + `eps2e/f_*.png`: hook intact at 0.5s, $999 card
preserved (no $199 assets anywhere in this manifest), add-on lip-sync on its
own audio, analysis punchline lands @14.0, endcard + sting clean, no black
frames. Audio: mean -17.1dB, max -0.5dB (alimiter), bed enters @10.1s under
the add-on only — eps2e's own music untouched.
