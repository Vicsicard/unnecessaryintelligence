#!/usr/bin/env python3
"""Generate free local test assets for the UI pipeline — no paid calls.

Creates under tools/tests/assets/:
    title.png, claim_0.png, claim_1.png, endcard.png   (1080x1920 plates)
    presenter.mp4                                     (4s test clip, 1080x1920)
    audio/n01.wav + n01_words.json                    (tone + fake word times)
    captions/test.ass                                 (2 cues)
    narration.wav                                     (6s bed tone)

Then `python tools/build_video.py tools/tests/test_manifest.json` renders a
full 1080x1920 export exercising still/graphic/presenter/mux/captions.
"""
import json, os, subprocess, sys, wave, struct, math

HERE = os.path.dirname(os.path.abspath(__file__))
A = os.path.join(HERE, "assets")
AUDIO = os.path.join(A, "audio")
os.makedirs(AUDIO, exist_ok=True)


def tone(path, dur=6.0, freq=440.0, vol=0.2, rate=48000):
    n = int(dur * rate)
    with wave.open(path, "w") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(rate)
        for i in range(n):
            v = int(32767 * vol * math.sin(2 * math.pi * freq * i / rate))
            w.writeframesraw(struct.pack("<h", v))


def plate(path, lines, bg="#F5F7FA", fg="#101828", accent="#2E5BFF"):
    from PIL import Image, ImageDraw, ImageFont
    img = Image.new("RGB", (1080, 1920), bg)
    d = ImageDraw.Draw(img)
    fonts_d = os.path.join(HERE, "..", "..", "brand", "fonts")
    try:
        f_big = ImageFont.truetype(os.path.join(fonts_d, "Inter-SemiBold.ttf"), 110)
        f_sm = ImageFont.truetype(os.path.join(fonts_d, "Inter.ttf"), 44)
    except OSError:
        f_big = f_sm = ImageFont.load_default()
    y = 760
    for i, ln in enumerate(lines):
        f, c = (f_big, accent) if i == 0 else (f_sm, fg)
        d.text((90, y), ln, font=f, fill=c)
        y += 150 if i == 0 else 90
    img.save(path)


def main():
    plate(os.path.join(A, "title.png"), ["HumanGPT", "A product of Unnecessary Intelligence"])
    plate(os.path.join(A, "claim_0.png"), ["It writes your emails."])
    plate(os.path.join(A, "claim_1.png"), ["It writes your emails.", "It sits in your meetings."], accent="#101828")
    plate(os.path.join(A, "endcard.png"), ["HumanGPT", "The future of AI is Steve."], bg="#101828", fg="#F5F7FA", accent="#F79009")

    # 4s 1080x1920 presenter stand-in (colored test clip)
    subprocess.run(["ffmpeg", "-y", "-f", "lavfi", "-i",
                    "testsrc2=size=1080x1920:rate=25:duration=4",
                    "-pix_fmt", "yuv420p", os.path.join(A, "presenter.mp4")],
                   check=True, capture_output=True)

    tone(os.path.join(AUDIO, "n01.wav"), dur=6.0)
    json.dump([
        {"w": "Meet", "start": 0.0, "end": 0.4},
        {"w": "HumanGPT", "start": 0.4, "end": 1.0},
        {"w": "the", "start": 1.0, "end": 1.2},
        {"w": "future", "start": 1.2, "end": 1.8},
        {"w": "is", "start": 1.8, "end": 2.0},
        {"w": "Steve", "start": 2.0, "end": 2.6},
    ], open(os.path.join(AUDIO, "n01_words.json"), "w"))

    os.makedirs(os.path.join(A, "captions"), exist_ok=True)
    open(os.path.join(A, "captions", "test.ass"), "w").write("""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Inter,64,&H00FFFFFF,&H000B1220,&H800B1220,-1,0,0,0,100,100,0,0,3,10,0,2,60,60,270,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 0,0:00:02.50,0:00:05.50,Default,,0,0,0,,Meet HumanGPT the future is Steve
Dialogue: 0,0:00:05.80,0:00:09.00,Default,,0,0,0,,TEST CAPTION CUE
""")
    tone(os.path.join(A, "narration.wav"), dur=9.0, freq=220.0, vol=0.15)
    print("test assets ready in", A)


if __name__ == "__main__":
    main()
