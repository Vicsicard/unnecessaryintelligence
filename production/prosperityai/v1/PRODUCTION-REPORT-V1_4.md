# ProsperityAI v1.4 — Social Cuts Report

**Editorial master:** `exports/prosperityai_v1_4_music.mp4` · **28.09s**
**Social loop cut:** `exports/prosperityai_v1_4_loop_music.mp4` · **28.09s**
**Review URLs:**
`http://127.0.0.1:8790/prosperityai/v1/exports/prosperityai_v1_4_music.mp4`
`http://127.0.0.1:8790/prosperityai/v1/exports/prosperityai_v1_4_loop_music.mp4`
**Base:** v1.3 assets — zero new paid generation. **Incremental cost: $0.**

## Timeline re-edit (the real work)

`audio/narration_s.wav` — narration re-edited, dead air trimmed out of inter-line
gaps (silencedetect -35dB map): head 0.33→0.08s, post-n01 gap 1.50→0.55s,
applause gap 1.39→0.95s, punchline hold 2.01→1.55s, financing beat 5.62→4.32s,
tail kept for endcard. 31.6s → **28.09s**. All speech preserved; comedic pauses
kept (the EARN MORE MONEY hold stays 1.55s — enough to read the joke).

Captions re-timed programmatically to the new edit (`captions/narration_s.ass`)
— same white-on-dark-outline style, word-grouped, bottom safe-area.

## Shot map (new boundaries at line starts)

| Shot | Span | Content |
|---|---|---|
| s00 | 0–3.34 | Founder full-frame mid-gesture, POVERTY ENDS TODAY drops @0.95 |
| s01 | 3.34–8.85 | Sequential reveal name@0.15 / tagline@1.1 / **$199 card @2.6 (upscaled)**; applause @8.19 |
| s02 | 8.85–14.75 | Dashboard + scanline; **EARN MORE MONEY punch-in @5.0 (1.05× oversize snap)** + accent @13.85 |
| s03 | 14.75–17.07 | Founder + FINANCIAL INCLUSION INITIATIVE kicker |
| s04 | 17.07–20.96 | **$59.99 card punch-in @0.2 (upscaled + contrast)** + sub @1.0 + disclaimer @2.1; subtle accent @16.9 (-8dB) precedes the card |
| s05a | 20.96–23.76 | Founder closing line |
| s05b | 23.76–26.29 | Wide ovation + founder on mega-screen + masked confetti; applause @23.9 |
| s06 | 26.29–28.09 | **Editorial only:** standard 1.8s endcard (big logo) + sting @26.3 |

## Loop-cut differences

- No endcard shot (`ui_endcard: false` — permanent standard default unchanged).
- s05b extended 2.53→4.33s: second confetti fall + **UI logo flash @3.45 rel
  (~26.9 abs, 0.6s)** inside the ovation, sting @27.05. Last ~0.3s is clean
  celebration → loops into the founder open without a logo-to-founder cut.
- Applause/accent timings identical to editorial.

## Audio QC

Both exports: mean -15.0dB, **max -0.4dB** (added `alimiter=0.94` to the
mixer's output chain — kills the transient 0dBFS peaks the applause could
cause). Applause at -4dB, finance accent tested at -8dB (subtle). Music
ducking unchanged. No dead air, no abrupt cuts.

## Preserved

Ricky founder, all dialogue, $199/$59.99 offers, EARN MORE MONEY, ovation +
confetti, V4 logo + sting, endcard standard for other productions. v1/v1.1/
v1.2/v1.3 all preserved.

## Honest notes

- "Punch-in" is implemented as oversized layers + fast snap entrance
  (0.28–0.32s) — a true zoom animation isn't in the layer anim set; reads as
  punch-in at mobile scale.
- Loop point is celebration→founder cut, not a dissolve — standard for Reels/
  Shorts loops.
