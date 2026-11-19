#!/usr/bin/env python3
"""UI narration assembly + caption chain.

Derived from the MALB blueprint-promo `_build_narr.py` pattern (see
docs/PROVENANCE.md). Genericized: beats, beat order, pacing and transcript
come from the production's `script.json` + `pacing.json` — no hardcoded text
or timings.

Inputs (all inside the production dir):
    script.json   {"beats": {"n01": "text", ...}, "beat_order": [...],
                    "transcript": {"n01": "full sentence", ...}}
    pacing.json   {"n01": 1.0, "n02": 7.5, ..., "total": 21.4}   (seconds)
    audio/n01.wav + audio/n01_words.json  (or n01_chars.json — chars are
                  grouped into words on whitespace)

Outputs:
    audio/narration.wav            beats placed at pacing offsets, amixed
    timestamps.json                {beat: {start, words:[{w,start,end}]}}
    captions/narration.ass         <=4-word grouped cues (PlayRes = canvas)
    captions/narration.srt         sentence-level cues
    captions/narration.vtt         web player track
    captions/transcript.txt

Usage:
    python ../../tools/build_captions.py --prod .
    python ../../tools/build_captions.py --prod . --width 1080 --height 1920
"""
import json, os, re, subprocess, sys, wave, contextlib

def die(msg, code=1):
    print("STOP:", msg); sys.exit(code)


def load(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def wav_dur(path):
    with contextlib.closing(wave.open(path)) as w:
        return w.getnframes() / float(w.getframerate())


def beat_words(audio_dir, b):
    wp = os.path.join(audio_dir, f"{b}_words.json")
    cp = os.path.join(audio_dir, f"{b}_chars.json")
    if os.path.exists(wp):
        raw = load(wp)
        return [{"w": x.get("text") or x.get("word") or x.get("w"),
                 "start": float(x.get("start_time") or x.get("start") or 0),
                 "end": float(x.get("end_time") or x.get("end") or 0)}
                for x in raw]
    if os.path.exists(cp):
        raw = load(cp)
        # group char entries into words on whitespace boundaries
        words, cur = [], ""
        for ch in raw:
            c = ch.get("character") or ch.get("char") or ch.get("text") or ""
            if not c.strip():
                if cur:
                    words.append(cur); cur = ""
                continue
            cur += c
            if c in (" ", "\t", "\n"):
                words.append(cur.strip()); cur = ""
        if cur:
            words.append(cur.strip())
        # chars may carry per-char start/end; rebuild timings if present
        timed, out, i = False, [], 0
        for w in words:
            n = len(w)
            seg = raw[i:i + n] if i + n <= len(raw) else []
            i += n + 1  # +1 for the consumed separator
            st = seg[0].get("start_time", seg[0].get("start")) if seg else None
            en = seg[-1].get("end_time", seg[-1].get("end")) if seg else None
            if st is not None and en is not None:
                timed = True
                out.append({"w": w, "start": float(st), "end": float(en)})
            else:
                out.append({"w": w, "start": None, "end": None})
        return out if timed else out
    return []


def fmt_ass(t):
    h = int(t // 3600); m = int((t % 3600) // 60); s = t % 60
    return f"{h}:{m:02d}:{s:05.2f}"

def fmt_srt(t):
    h = int(t // 3600); m = int((t % 3600) // 60); s = int(t % 60); ms = int(round((t % 1) * 1000))
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

def fmt_vtt(t):
    h = int(t // 3600); m = int((t % 3600) // 60); s = int(t % 60); ms = int(round((t % 1) * 1000))
    return f"{h:02d}:{m:02d}:{s:02d}.{ms:03d}"


def spread_words(words, wav_d, cap=8.0):
    """If a beat has no per-word times, spread words evenly over the wav."""
    if all(w["start"] is not None for w in words):
        return words
    n = max(1, len(words))
    step = min(wav_d, cap) / n
    return [{"w": w["w"], "start": i * step, "end": (i + 1) * step}
            for i, w in enumerate(words)]


def main():
    args = sys.argv[1:]
    prod = args[args.index("--prod") + 1] if "--prod" in args else "."
    W = int(args[args.index("--width") + 1]) if "--width" in args else 1080
    H = int(args[args.index("--height") + 1]) if "--height" in args else 1920
    audio = os.path.join(prod, "audio")
    cap_dir = os.path.join(prod, "captions")
    os.makedirs(cap_dir, exist_ok=True)

    spec = load(os.path.join(prod, "script.json"))
    pacing = load(os.path.join(prod, "pacing.json"))
    order = spec.get("beat_order") or sorted(spec["beats"])

    # ── timestamps + narration mix ────────────────────────────────
    ts, inputs, delays = {}, [], []
    for i, b in enumerate(order):
        wav = os.path.join(audio, f"{b}.wav")
        if not os.path.exists(wav):
            die(f"missing {wav} — run gen_tts.py first")
        start = float(pacing[b])
        d = wav_dur(wav)
        words = spread_words(beat_words(audio, b), d)
        ts[b] = {"start": start, "dur": round(d, 3),
                 "words": [{"w": w["w"],
                            "start": round(start + w["start"], 3),
                            "end": round(start + w["end"], 3)}
                           for w in words]}
        inputs += ["-i", wav]
        delays.append(f"[{i}:a]adelay={int(start*1000)}|{int(start*1000)}[a{i}]")
    mix = ";".join(delays) + ";" + "".join(f"[a{i}]" for i in range(len(order))) \
        + f"amix=inputs={len(order)}:normalize=0[m]"
    subprocess.run(["ffmpeg", "-y", *inputs, "-filter_complex", mix,
                    "-map", "[m]", "-ac", "1", "-ar", "48000",
                    os.path.join(audio, "narration.wav")], check=True,
                   capture_output=True)
    json.dump(ts, open(os.path.join(prod, "timestamps.json"), "w"), indent=1)

    # ── ASS: grouped <=4-word cues, safe bottom band ──────────────
    def cues():
        for b in order:
            ws = ts[b]["words"]
            for i in range(0, len(ws), 4):
                grp = ws[i:i + 4]
                yield grp[0]["start"], grp[-1]["end"], " ".join(w["w"] for w in grp)
    cues = list(cues())
    margin_v = int(H * 0.14)  # 9:16-safe bottom band above platform UI
    ass = "\n".join([
        "[Script Info]", "ScriptType: v4.00+", f"PlayResX: {W}", f"PlayResY: {H}",
        "", "[V4+ Styles]",
        "Format: Name, Fontname, Fontsize, PrimaryColour, OutlineColour, "
        "BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, "
        "Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, "
        "MarginR, MarginV, Encoding",
        f"Style: Default,Inter,{int(H*0.033)},&H00FFFFFF,&H000B1220,"
        f"&H800B1220,-1,0,0,0,100,100,0,0,3,{int(H*0.008)},0,2,60,60,{margin_v},1",
        "", "[Events]",
        "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, "
        "Effect, Text",
        *[f"Dialogue: 0,{fmt_ass(s)},{fmt_ass(e)},Default,,0,0,0,,{t}"
          for s, e, t in cues]])

    # ── SRT/VTT: sentence-level cues spanning each beat ───────────
    srt_rows, vtt_rows = [], []
    for i, b in enumerate(order, 1):
        s, e = ts[b]["start"], ts[b]["start"] + ts[b]["dur"]
        t = spec.get("transcript", {}).get(b) or spec["beats"][b]
        srt_rows.append(f"{i}\n{fmt_srt(s)} --> {fmt_srt(e)}\n{t}\n")
        vtt_rows.append(f"{fmt_vtt(s)} --> {fmt_vtt(e)}\n{t}\n")

    open(os.path.join(cap_dir, "narration.ass"), "w", encoding="utf-8").write(ass)
    open(os.path.join(cap_dir, "narration.srt"), "w", encoding="utf-8").write("\n".join(srt_rows))
    open(os.path.join(cap_dir, "narration.vtt"), "w", encoding="utf-8").write("WEBVTT\n\n" + "\n".join(vtt_rows))
    open(os.path.join(cap_dir, "transcript.txt"), "w", encoding="utf-8").write(
        "\n".join(spec.get("transcript", {}).get(b, spec["beats"][b]) for b in order))
    print(f"timestamps.json + narration.wav + ASS({len(cues)} cues)/SRT/VTT/transcript written")
    print(f"narration dur: {wav_dur(os.path.join(audio,'narration.wav')):.2f}s")


if __name__ == "__main__":
    main()
