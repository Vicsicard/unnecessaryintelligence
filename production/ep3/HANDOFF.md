# EP3 Handoff v2 — Viral Reel Edition

Still **3 Meta generations**; all graphics, captions, and sound are local.
Updated for social-ad pacing: faster delivery, bigger reactions, room for
punch-ins.

## PART 1 — ChatGPT image prompts (9:16, unchanged + tighter S3 framing)

All: "photorealistic, cinematic commercial still, premium lighting, vertical
9:16, no text, no logos, no watermarks"

**IMG-1 — Spokesperson**
> Confident female corporate spokesperson in her 40s, tailored charcoal suit,
> opulent showroom with warm spotlights, mid-gesture presenting DIRECTLY to
> camera with bright energetic smile; large dark presentation display behind
> her showing a golden chandelier silhouette; elegant Black Friday mood —
> deep blacks, gold accents; frame her waist-up with headroom for captions
> BELOW her chest; photorealistic, 9:16, no text, no logos

**IMG-2 — Chandelier**
> Massive extravagant gold-and-crystal ballroom chandelier, hundreds of
> crystals catching warm light, photographed slightly from below in a grand
> neoclassical ballroom, tall columns; shallow depth of field; leave clean
> dark space in the LOWER THIRD of frame for an overlaid purchase card;
> photorealistic, 9:16, no people, no text, no logos

**IMG-3 — Customer (revised for punch-in)**
> Ordinary man in his 30s at a modern kitchen counter, staring at his phone
> in shock; frame him CHEST-UP, centered, with clear space around his head
> for a zoom punch-in; cool domestic light, phone glow on his face; phone
> screen faces AWAY from camera; photorealistic, 9:16, no text, no logos

## PART 2 — Meta AI animation prompts (v2)

**GEN-1 (~3.5s) — brisk corporate-ad energy:**
> Animate: the spokesperson is already mid-presenting-gesture at frame one
> (no lead-in) and speaks directly to camera with brisk, bright
> corporate-ad enthusiasm: "This Black Friday, BuyForMe AI found President
> Trump's ballroom gift wish list!" Subtle push-in. Keep face, wardrobe and
> background consistent; no cuts; no on-screen text; nothing else moves.

**GEN-2 (~3s) — luxury-reveal drift:**
> Animate: slow majestic upward drift toward the chandelier, crystals
> shimmering and refracting warm light like a luxury car commercial.
> Chandelier stays centered; lower third stays clear of any objects; no
> people, no text, no cuts.

*(confirm_card.png overlays this clip locally — exact $250,000.00 guaranteed.)*

**GEN-3 (~5.5s) — shout, hold, cheerful reply:**
> Animate: the man jolts and shouts at his phone, genuinely horrified: "You
> spent a quarter million dollars?!" — then HOLDS the shocked expression in
> silence, hand gripping hair. After the beat, an off-screen AI voice
> replies with cheerful customer-service sincerity (not sarcasm): "Relax.
> We used your credit card." Keep his face centered and unobstructed for a
> punch-in zoom; kitchen unchanged; phone screen never visible; no text.

## PART 3 — Local assembly (revised)

1. `production/ep3/source/`: `s01.mp4 s02.mp4 s03.mp4`
2. `manifest_ep3_reel.json` + `manifest_ep3_master.json` — same shots:
   - s01 composite(GEN-1 + headline.png @0.3 punch-in + captions)
   - s02 composite(GEN-2 + confirm_card.png @0.25 snap-in + captions)
   - s03a composite(GEN-3 0–2.3s, zoompan punch-in on face) + shout captions
   - s03b composite(GEN-3 2.3–end) + reply captions (`YOUR CREDIT CARD` orange)
   - s04 product card 2.2s
   - s05: master = `endcard` shot; reel = logo-flash layer 0.6s + `ui_endcard:false`
3. Audio: concat clip audios → narration; mix via
   `mix_music_bed.py` — bed `shop_bed`, sfx `open_hit@0`, `checkout_blip@3.0`,
   `reveal_impact@3.3`, `drop_sweep@7.6`, `ui_sting@end`.
4. Punch-in: ffmpeg zoompan on the s03a segment (built into composite base
   chain if supported, else pre-render the crop-zoom clip).
5. Optional paid QC: `--meta-qc --brief BRIEF.md` (authorization required).

## Sound map

| t | event |
|---|---|
| 0.0 | `open_hit` + bed in (ducked) |
| ~3.0 | `checkout_blip` on the cut |
| ~3.3 | `reveal_impact` on $250,000 |
| ~7.6 | `drop_sweep` → 0.8s dead air → AI reply |
| end | UI sting (master) / bed tail (reel) |
