# EP3 Handoff — ChatGPT image prompts + Meta AI animation prompts

Minimize to **3 Meta generations** (S1, S2, S3). S4 product card + S2 order
confirmation are local deterministic graphics.

## PART 1 — ChatGPT image prompts (3 starting frames, 9:16)

All: "photorealistic, cinematic commercial still, premium tech-advertisement
lighting, vertical 9:16, no text, no logos, no watermarks"

**IMG-1 — Spokesperson (Scene 1)**
> Confident female corporate spokesperson in her 40s, tailored charcoal suit,
> standing in an opulent showroom with warm spotlights, presenting to camera
> with a delighted smile and open presenting gesture; behind her a large
> dark presentation display showing a golden chandelier silhouette;
> festive-but-elegant Black Friday atmosphere — deep blacks, gold accents;
> photorealistic cinematic commercial still, 9:16 vertical, no text, no logos

**IMG-2 — Chandelier (Scene 2)**
> Massive extravagant gold-and-crystal ballroom chandelier, hundreds of
> hanging crystals catching warm light, photographed slightly from below in
> a grand neoclassical ballroom with tall columns; shallow depth of field,
> premium luxury-product commercial lighting; photorealistic cinematic
> commercial still, 9:16 vertical, no text, no people, no logos

**IMG-3 — Customer (Scene 3)**
> Ordinary man in his 30s at a modern kitchen counter, staring at his phone
> in horror, mouth open, one hand gripping his hair; cool morning domestic
> light contrasted with the phone's glow on his shocked face; photorealistic
> cinematic commercial still, 9:16 vertical, phone screen facing away from
> camera (no screen content), no text, no logos

## PART 2 — Meta AI animation prompts (copy/paste per scene)

**GEN-1 (Scene 1, ~4s):**
> Animate: the spokesperson continues her presenting gesture and speaks
> directly to camera with warm corporate enthusiasm: "This Black Friday,
> BuyForMe AI found President Trump's ballroom gift wish list!" Slow subtle
> push-in, steady camera. Keep her face, suit, and background display
> consistent; no camera cuts; no text appearing; nothing else moves.

**GEN-2 (Scene 2, ~3.5s):**
> Animate: slow majestic camera drift under the chandelier, crystals
> shimmering and refracting light, gentle sparkle movement only. No people,
> no text, no camera cuts, chandelier stays centered and static in frame.

*(ORDER CONFIRMED / TRUMP BALLROOM CHANDELIER / $250,000.00 / recipient is a
local overlay on this clip — guarantees exact price spelling.)*

**GEN-3 (Scene 3, ~5.5s):**
> Animate: the man reacts in horror, shouting at his phone: "You spent a
> quarter million dollars?!" — shocked expression, hand still in hair. Then
> hold as an off-screen cheerful AI voice replies, calm and delighted:
> "Relax. We used your credit card." Keep the kitchen and his appearance
> consistent; phone screen never visible to camera; no text; no cuts.

## PART 3 — Local assembly plan (when clips land)

1. Drop clips → `production/ep3/source/` as `s01.mp4 s02.mp4 s03.mp4`.
2. `manifest_ep3.json`: composite shots — s01 (GEN-1 + headline layer),
   s02 (GEN-2 + deterministic order-confirm PNG), s03 (GEN-3 + word captions),
   s04 product card (still, 2.5s), s05 endcard (auto).
3. Narration = concat of each clip's embedded audio + tagline VO
   (source TBD — TTS or provided).
4. `tools/brand_clip.py` pattern: build via manifest, then mix + sting.
5. Optional: `--meta-qc --brief BRIEF.md` (paid — needs authorization).

## Checklist for you

- [ ] 3 ChatGPT images → Meta AI → 3 MP4s (est. 3 manual generations)
- [ ] Tagline VO source decision: TTS (free) vs provided recording
- [ ] Authorize optional paid Model API QC? (~cents)
