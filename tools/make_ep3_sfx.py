#!/usr/bin/env python3
"""EP3 social-reel soundscape — deterministic synthesis, zero licensing risk.

    python tools/make_ep3_sfx.py --out production/ep3/audio

Generates (48kHz WAV):
  open_hit.wav       — 0.55s attention whoosh-boom (reel opener)
  shop_bed.wav       — 16s upbeat electronic shopping-ad bed loop
  checkout_blip.wav  — 0.35s cheerful purchase-confirm ding
  reveal_impact.wav  — 0.9s dramatic orchestral-ish hit for $250,000
  drop_sweep.wav     — 0.5s filtered audio drop into the punchline
"""
import math, os, struct, sys, wave, random

SR = 48000
random.seed(3)


def env(t, a=0.005, dec=0.3):
    return (1 - math.exp(-t / a)) * math.exp(-t / dec)


def note(f, t):
    return (math.sin(2*math.pi*f*t) + 0.3*math.sin(2*math.pi*f*2*t)
            + 0.1*math.sin(2*math.pi*f*3*t))


def write(name, samples):
    os.makedirs(OUT, exist_ok=True)
    with wave.open(os.path.join(OUT, name), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes(b"".join(struct.pack("<h", int(max(-1, min(1, s)) * 32767)) for s in samples))
    print("wrote", name, f"{len(samples)/SR:.2f}s")


def lowpass(x, a=0.12):
    y = 0; out = []
    for s in x: y += a * (s - y); out.append(y)
    return out


OUT = "."
if "--out" in sys.argv: OUT = sys.argv[sys.argv.index("--out") + 1]

# open_hit: noise whoosh + sub boom
n = int(0.55 * SR)
_noise = lowpass([random.uniform(-1, 1) for _ in range(n)], 0.05)
write("open_hit.wav", [
    0.9*env(i/SR, 0.02, 0.5)*(note(52, i/SR) + 0.5*note(78, i/SR))
    + 0.35*env(i/SR, 0.08, 0.45)*_noise[i]
    for i in range(n)])

# shop_bed: 128bpm-ish loop — kick + hats + minor-key arp, 16s
n = int(16 * SR); bpm = 128; beat = 60 / bpm
ARP = [220, 261.63, 329.63, 392]  # Am add-flavor
s = []
for i in range(n):
    t = i / SR
    tb = (t % beat) / beat
    out = 0.0
    if int(t / beat) % 1 == 0:  # kick each beat
        out += 0.75 * env(tb*beat, 0.004, 0.09) * math.sin(2*math.pi*(120 - 80*tb)*t)
    if int(t / (beat/2)) % 2:   # offbeat hat
        out += 0.10 * env((t % (beat/2)) / (beat/2), 0.001, 0.05) * random.uniform(-1, 1)
    step = int(t / (beat/2)) % 8
    out += 0.16 * env((t % (beat/2)) / (beat/2), 0.004, 0.22) * note(ARP[step % 4] * (2 if step > 5 else 1), t)
    s.append(out)
write("shop_bed.wav", lowpass(s, 0.5))

# checkout_blip: two-note register ding
n = int(0.35 * SR)
write("checkout_blip.wav", [
    0.55*env(i/SR, 0.004, 0.28)*note(1318.5, i/SR)
    + 0.45*env((i/SR - 0.09 if i/SR > 0.09 else 0), 0.004, 0.24)*note(1760, i/SR)
    for i in range(n)])

# reveal_impact: low boom + dissonant brass stab + shimmer
n = int(0.9 * SR)
write("reveal_impact.wav", [
    0.9*env(i/SR, 0.006, 0.55)*(note(55, i/SR) + 0.4*note(82.5, i/SR))
    + 0.30*env(i/SR, 0.004, 0.35)*(note(233, i/SR) + note(311, i/SR) + 0.7*note(466, i/SR))
    for i in range(n)])

# drop_sweep: fading filtered noise + downward tone — the "everything stops" drop
n = int(0.5 * SR)
_dn = lowpass([random.uniform(-1, 1) for _ in range(n)], 0.1)
write("drop_sweep.wav", [
    0.4*env(i/SR, 0.15, 0.35)*_dn[i]
    + 0.3*env(i/SR, 0.1, 0.38)*note(220*(1 - 0.6*i/n), i/SR)
    for i in range(n)])
