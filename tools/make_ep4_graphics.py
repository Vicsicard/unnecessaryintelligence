#!/usr/bin/env python3
"""EP4 StudyBro AI — deterministic graphics (hook overlay + product card).

    python tools/make_ep4_graphics.py --prod production/ep4

Outputs (inside <prod>/graphics/):
  hook.png          — 1080x460 alpha overlay "AI JUST REPLACED YOUR TEXTBOOKS?!"
  product_card.png  — 1080x1920 StudyBro AI card + tagline + UI footer

Palette: UI ink/paper from brand/palette.json; StudyBro purple accent.
Requires Pillow.
"""
import os, sys
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONT = os.path.join(HERE, "..", "brand", "fonts", "Inter-SemiBold.ttf")
PURPLE = (180, 92, 255)
INK = (16, 24, 40)
PAPER = (245, 247, 250)

def font(sz):
    return ImageFont.truetype(FONT, sz)

def draw_center(d, y, spans, stroke=6):
    widths = [d.textlength(t, font=f) for (t, c, f) in spans]
    x = (1080 - sum(widths)) / 2
    for (t, c, f), w in zip(spans, widths):
        d.text((x, y), t, font=f, fill=c, stroke_width=stroke, stroke_fill=(8, 12, 24))
        x += w

def main():
    out = sys.argv[sys.argv.index("--prod") + 1] if "--prod" in sys.argv else "."
    gdir = os.path.join(out, "graphics")
    os.makedirs(gdir, exist_ok=True)

    img = Image.new("RGBA", (1080, 460), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    f_big = font(104)
    draw_center(d, 40, [("AI", PURPLE, f_big), (" JUST ", PAPER, f_big), ("REPLACED", PURPLE, f_big)], stroke=7)
    draw_center(d, 185, [("YOUR TEXTBOOKS?!", PAPER, f_big)], stroke=7)
    img.save(os.path.join(gdir, "hook.png"))

    card = Image.new("RGB", (1080, 1920), INK)
    d = ImageDraw.Draw(card)
    f_word, f_tag, f_sub = font(150), font(72), font(38)
    w1, w2 = d.textlength("StudyBro", font=f_word), d.textlength(" AI", font=f_word)
    x = (1080 - w1 - w2) / 2
    d.text((x, 680), "StudyBro", font=f_word, fill=PAPER)
    d.text((x + w1, 680), " AI", font=f_word, fill=PURPLE)
    d.line([240, 900, 840, 900], fill=PURPLE, width=6)
    d.ellipse([520, 866, 560, 906], fill=PURPLE)
    for i, t in enumerate(["LESS STUDYING.", "MORE CONFIDENCE."]):
        tw = d.textlength(t, font=f_tag)
        d.text(((1080 - tw) / 2, 980 + i * 95), t, font=f_tag, fill=PAPER)
    s = "an  UNNECESSARY INTELLIGENCE  product"
    sw = d.textlength(s, font=f_sub)
    d.text(((1080 - sw) / 2, 1700), s, font=f_sub, fill=(102, 112, 133))
    card.save(os.path.join(gdir, "product_card.png"))
    print("wrote", gdir)

if __name__ == "__main__":
    main()
