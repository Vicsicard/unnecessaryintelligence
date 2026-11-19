# EP3 Assembly — First Review Cut

**Reel:** `http://127.0.0.1:8790/ep3/exports/ep3_reel_v1.mp4` — **17.56s**
**Master:** `http://127.0.0.1:8790/ep3/exports/ep3_master_v1.mp4` — **18.76s**
Originals untouched in `source/`; all local, $0, no paid calls.

## Timeline (actual footage, not plan)

| Cut | Source window | Content |
|---|---|---|
| s01 | `s01.mp4` 0→3.9s | Spokesperson line; cut at the first natural dip @3.75 |
| s02 | `s02.mp4` 0→3.2s | Chandelier + `confirm_card` overlay @0.4 (TRUMP BALLROOM CHANDELIER / **$250,000.00** / Gift recipient: President Donald Trump) |
| s03a | `s03.mp4` 0.35→3.0s | Shout — 1.0→1.12 punch-in zoom (zoompan pre-render) |
| s03b | `s03.mp4` 3.0→7.0s | Baked 0.9s dead-air pause → "Relax. We used your credit card." → reaction tail |
| s04 | still | BuyForMe AI card 3.2s + tagline VO |
| s05 | endcard | Reel: `flash` 0.6s · Master: `standard` 1.8s |

## Sound map

`open_hit` @0 · `shop_bed` -12dB ducked · `checkout_blip` @3.9 ·
`reveal_impact` @4.3 · `drop_sweep` @9.7 · UI sting @16.9
(both versions — sting under the flash on reel). Peaks limited to -0.5dB.

## Findings from footage inspection

- **s01 contains ~6s of speech after the approved line** (continuous dialogue
  to ~9.5s). Cut at the first natural gap — flagged in case it's a second
  approved line rather than off-script filler.
- **s03's baked graphics** (YOU SPENT… / PURCHASE CONFIRMED $250,000 / Relax…
  YOUR CREDIT CARD) are already YouTube-native — no caption duplication added.
  Its baked card lacks "TRUMP" — covered by our deterministic s02 card.
- **s02 has no dialogue** — pure ambience; trimmed after the shimmer peak.
- Sources are 720×1280 → upscaled 1080×1920 (acceptable softness).

## Flags

- **Tagline VO is Windows SAPI (temporary)** — intelligible but robotic.
  Recommend a real VO or HeyGen TTS (paid, needs approval) for final.
- Spokesperson is male (brief said female) — cosmetic deviation from prompt,
  no cost to fix unless you want a regen.
- Reel's 0.6s brand flash = full V4 endcard plate (a logo chip collided with
  the tagline text — better, it's the approved card).

## Recommended (not done — awaiting your review)

1. Reveal what s01's second half says (transcribe → keep or drop confirmed).
2. Real VO for tagline.
3. Optional paid Model API QC pass (~cents).
