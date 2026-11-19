# UI Episode 3 — BuyForMe AI: "Trump's Black Friday Wish List" (VIRAL REEL CUT)

**Status: ASSETS PREP — awaiting image handoff + manual Meta animation.**
Premise, dialogue, $250,000 price, and punchline are APPROVED — unchanged.
This revision is direction only: edit it like a Reel/TikTok comedy ad, not a
corporate spot. Hook inside 0.5s. Two exports from the same material.

## Revised scene plan (reel pacing)

| # | Time | Cut | Content | Audio |
|---|---|---|---|---|
| 1 | 0–3.0 | Hard open mid-gesture — no lead-in | Spokesperson line + `TRUMP'S BALLROOM GIFT WISH LIST` headline punches in @0.3s | `open_hit` @0.0 + `shop_bed` (ducked) |
| 2 | 3.0–5.4 | Rapid cut + punch-in | Chandelier luxury drift; `confirm_card` snaps in @+0.25s, `$250,000.00` gets `reveal_impact` | `checkout_blip` @cut + `reveal_impact` @price |
| 3 | 5.4–10.6 | Punch-in zoom on shout | "YOU SPENT A QUARTER MILLION DOLLARS?!" → `drop_sweep` + ~0.8s dead-air pause (bed ducks out) → AI cheerfully sincere: "Relax. We used your credit card." | `drop_sweep` into pause; bed returns under reply |
| 4 | 10.6–12.8 | Product card | "BuyForMe AI. Your money. Our decisions." VO | bed tail |
| 5R | 12.5–12.8 | **Reel:** 0.6s UI logo flash inside the card's tail; final 0.3s clean → loops | | `shop_bed` out |
| 5M | 12.8–14.6 | **Master:** standard 1.8s V4 endcard | | UI sting |

**Reel ≈ 13.0s · Master ≈ 14.6s** — both inside social spec.

## Captions (reel style)

Bold karaoke ASS — Inter-SemiBold white, heavy outline, bottom-safe.
Emphasis words in UI orange + ~15% larger:
**TRUMP**, **BLACK FRIDAY**, **$250,000**, **YOUR CREDIT CARD**.

## Sound design (all synthesized locally — `tools/make_ep3_sfx.py`)

`open_hit` 0.55s · `shop_bed` 16s electronic loop @128bpm ·
`checkout_blip` 0.35s · `reveal_impact` 0.9s · `drop_sweep` 0.5s ·
UI sting (existing). No licensed music — zero rights risk.
Mix via `mix_music_bed.py --sfx file@sec@gain` + `alimiter`.

## Performance notes (locked)

- AI reply = cheerful sincerity, NOT sarcasm.
- ~0.8s comedic dead-air before the AI reply — audio drops under it.
- Keep characters realistic; the joke is the money, not the faces.
- Fictional satire — never implied as a real transaction.

## Two exports (one build, two manifests)

- `ep3_reel` — `ui_endcard:false`, logo-flash layer @12.5s, loops into open.
- `ep3_master` — standard `endcard` shot + sting (permanent default untouched).
