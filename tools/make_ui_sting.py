#!/usr/bin/env python3
"""UI brand sting + accent chime — deterministic synthesis, no dependencies.

The permanent Unnecessary Intelligence audio signature: a short, overly
triumphant corporate sting that closes every original UI video behind the
V4 endcard. Regenerable — run once per production dir (or point --out at
shared audio/). WAV output is gitignored media; this script is the source.

    python tools/make_ui_sting.py --out audio            # sting.wav + accent.wav
    python tools/make_ui_sting.py --out audio --sting ui_sting.wav --accent ui_accent.wav

sting (~1.35s): low boom -> rising major triad -> bright octave shimmer tail.
accent (~0.7s): single sparkle chime for punchline reveals.
"""
import math, os, struct, sys, wave

SR = 48000


def env(t, a=0.004, dec=0.35):
    """Fast attack, exponential decay."""
    return (1 - math.exp(-t / a)) * math.exp(-t / dec)


def note(freq, t):
    # fundamental + soft 2nd/3rd harmonics for a warmer "brass-chime" tone
    return (math.sin(2 * math.pi * freq * t)
            + 0.35 * math.sin(2 * math.pi * freq * 2 * t)
            + 0.12 * math.sin(2 * math.pi * freq * 3 * t))


def render(events, dur, out, peak=0.85):
    """events: [(start, freq, amp, decay)] summed into a mono wav."""
    n = int(SR * dur)
    buf = [0.0] * n
    for st, freq, amp, dec in events:
        i0 = int(st * SR)
        for i in range(i0, n):
            t = (i - i0) / SR
            buf[i] += amp * env(t, dec=dec) * note(freq, t)
    m = max(1e-9, max(abs(x) for x in buf))
    gain = peak / m
    tail = int(SR * 0.08)  # hard 80ms fade-out at the very end — no click
    for i in range(n - tail, n):
        buf[i] *= gain * max(0.0, (n - i) / tail)
    buf[: n - tail] = [x * gain for x in buf[: n - tail]]
    os.makedirs(os.path.dirname(os.path.abspath(out)) or ".", exist_ok=True)
    with wave.open(out, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes(b"".join(struct.pack("<h", int(max(-1, min(1, x)) * 32767)) for x in buf))
    return out


def sting(path):
    # C3 boom, then C-E-G rising stagger, resolving to a bright C6 shimmer.
    ev = [(0.00, 130.81, 0.9, 0.45),           # boom
          (0.06, 261.63, 0.5, 0.40),
          (0.10, 523.25, 0.55, 0.30),          # C5
          (0.22, 659.25, 0.55, 0.32),          # E5
          (0.34, 783.99, 0.60, 0.45),          # G5
          (0.34, 1567.98, 0.30, 0.50),         # G6 shimmer
          (0.50, 1046.50, 0.45, 0.60),         # C6 resolve
          (0.50, 2093.00, 0.18, 0.70)]         # C7 sparkle
    return render(ev, 1.35, path)


def accent(path):
    # Single quick chime for the "EARN MORE MONEY."-style punchline beat.
    ev = [(0.00, 1318.51, 0.5, 0.22),          # E6
          (0.00, 2637.02, 0.2, 0.30),          # E7 shimmer
          (0.10, 1975.53, 0.35, 0.35)]         # B7 tail
    return render(ev, 0.7, path)


if __name__ == "__main__":
    args = sys.argv[1:]
    out_d = args[args.index("--out") + 1] if "--out" in args else "audio"
    s = args[args.index("--sting") + 1] if "--sting" in args else "ui_sting.wav"
    a = args[args.index("--accent") + 1] if "--accent" in args else "ui_accent.wav"
    print("sting ->", sting(os.path.join(out_d, s)))
    print("accent ->", accent(os.path.join(out_d, a)))
