"""brand_clip.py — UI intake: brand any finished MP4 with the UI endcard + sting.

Accepts an externally-produced MP4 (e.g. a Meta AI/Vibes render downloaded
by hand), preserves it untouched, wraps it in a generated manifest
(source -> standard UI endcard), then muxes the source audio with the UI
audio sting at the endcard cut.

Usage:
    python tools/brand_clip.py <input.mp4> [--name slug] [--out path]
        [--endcard brand/assets/endcard_v4.png] [--sting brand/assets/ui_sting.wav]
        [--endcard-duration 1.8] [--music bed.wav] [--qc-dir dir]

Output goes to production/_intake/<name>/<name>_branded.mp4 unless --out.
Zero paid calls; fully local ffmpeg + build_video pipeline.
"""
import os, sys, json, subprocess, argparse

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
INTAKE = os.path.join(ROOT, "production", "_intake")

def run(args, **kw):
    return subprocess.run(args, capture_output=True, text=True, **kw)

def probe_json(path, entry, extra=None):
    a = ["ffprobe","-v","error","-of","json"]
    if extra: a += extra
    a += ["-show_entries", entry, path]
    return json.loads(run(a).stdout)

def fail(msg):
    print("FATAL:", msg); sys.exit(2)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("--name")
    ap.add_argument("--out")
    ap.add_argument("--endcard", default="brand/assets/endcard_v4.png")
    ap.add_argument("--sting", default="brand/assets/ui_sting.wav")
    ap.add_argument("--endcard-duration", type=float, default=1.8)
    ap.add_argument("--music")
    ap.add_argument("--qc-dir")
    ap.add_argument("--brief", help="episode brief .txt/.md for optional Meta video QC")
    ap.add_argument("--meta-qc", action="store_true",
                    help="run Model API video QC on the BRANDED export (paid; needs MODEL_API_KEY)")
    ap.add_argument("--meta-qc-model", default="muse-ember-1.0")
    a = ap.parse_args()

    src = os.path.abspath(a.input)
    if not os.path.exists(src): fail(f"missing input: {src}")
    name = a.name or os.path.splitext(os.path.basename(src))[0].replace(" ", "_")

    if not os.path.exists(a.endcard): fail(f"missing endcard: {a.endcard}")

    # sting is gitignored media — regenerate from source if absent
    sting = os.path.abspath(a.sting)
    if not os.path.exists(sting):
        gen = os.path.join(HERE, "make_ui_sting.py")
        r = run([sys.executable, gen, "--out", os.path.dirname(sting),
                 "--sting", os.path.basename(sting)])
        if r.returncode or not os.path.exists(sting):
            fail(f"sting missing and regeneration failed: {sting}")

    dur = float(probe_json(src, "format")["format"]["duration"])
    vs = probe_json(src, "stream", ["-select_streams", "v:0"])["streams"][0]
    has_audio = bool(probe_json(src, "stream", ["-select_streams", "a:0"]).get("streams"))
    print(f"input: {vs['width']}x{vs['height']} {dur:.2f}s audio={'yes' if has_audio else 'NO'}")

    # ── preflight ────────────────────────────────────────────────────
    warns = []
    ar = vs["width"] / vs["height"]
    if abs(ar - 9 / 16) > 0.02:
        loss = max(0, (1 - (9 / 16) / ar) * 100)
        warns.append(f"aspect {ar:.3f} vs 9:16 target — center-crop loses ~{loss:.0f}% of width"
                     if ar > 9 / 16 else f"aspect {ar:.3f} — pillarboxed content loses height")
    if dur > 120: warns.append(f"long source {dur:.1f}s — endcard branding still applies, verify intent")
    dec = run(["ffmpeg", "-v", "error", "-i", src, "-f", "null", "-"])
    if dec.stderr.strip(): warns.append(f"decode errors: {dec.stderr.strip()[:160]}")
    if has_audio:
        vol = run(["ffmpeg", "-i", src, "-af", "volumedetect", "-f", "null", "-"]).stderr
        mm = [l for l in vol.splitlines() if "max_volume" in l]
        if mm and float(mm[0].split("max_volume:")[1].split("dB")[0]) > -0.2:
            warns.append("source audio near 0dBFS — output limiter will catch, but source may clip")
    for w in warns: print("  PREFLIGHT WARN:", w)

    work = os.path.join(INTAKE, name); os.makedirs(work, exist_ok=True)
    out = os.path.abspath(a.out) if a.out else os.path.join(work, f"{name}_branded.mp4")

    # source audio -> padded wav (or silence)
    nar = os.path.join(work, "src_audio.wav")
    pad = a.endcard_duration + 0.2   # nar = video + 0.2 — inside duration_tolerance
    if has_audio:
        r = run(["ffmpeg","-y","-v","error","-i",src,"-af",f"apad=pad_dur={pad}","-ar","48000",nar])
    else:
        r = run(["ffmpeg","-y","-v","error","-f","lavfi","-i",
                 f"anullsrc=r=48000:cl=stereo:d={dur+pad}",nar])
    if r.returncode: fail(r.stderr[-400:])

    # header-only captions (satisfies build_video's captions_ass lookup)
    ass = os.path.join(work, "empty.ass")
    open(ass,"w").write("[Script Info]\nScriptType: v4.00+\n"
        "PlayResX: 1080\nPlayResY: 1920\n\n[V4+ Styles]\n"
        "Format: Name, Fontname, Fontsize, PrimaryColour, OutlineColour, BackColour, Bold, Italic, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV\n"
        "Style: Default,Arial,64,&H00FFFFFF,&H00000000,&H80000000,-1,0,1,3,0,2,60,60,80\n\n"
        "[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n")

    manifest = {
        "slug": name, "version": "intake",
        "width": 1080, "height": 1920, "fps": 25, "xfade": 0.4,
        "duration_tolerance": 0.6, "ui_endcard": True,
        "segments_dir": "segments", "concat_list": "concat.txt",
        "concat_out": "concat.mp4", "narration_wav": "src_audio.wav",
        "fonts_dir": "brand/fonts", "export": out,
        "captions_ass": "empty.ass",
        "endcard_source": os.path.abspath(a.endcard),
        "shots": [
            {"id":"s00","type":"composite","duration":round(dur,2),
             "base": src, "layers": []},
            {"id":"s06","type":"endcard","source": os.path.abspath(a.endcard),
             "duration": a.endcard_duration, "variant":"standard"}
        ]}
    mpath = os.path.join(work, "manifest.json")
    json.dump(manifest, open(mpath,"w"), indent=2)

    r = run([sys.executable, os.path.join(HERE,"build_video.py"), mpath])
    print(r.stdout.strip()[-300:])
    if r.returncode: fail(r.stderr[-400:] or "build failed")
    if not os.path.exists(out): fail("build produced no export")

    # mux: source audio + sting at endcard cut (+ optional bed)
    vd = float(probe_json(out, "format")["format"]["duration"])
    sting_at = max(0.0, vd - a.endcard_duration - 0.05)
    tmp = out + ".tmp.mp4"
    fc = (f"[0:a]apad[n];"
          + (f"[2:a]adelay={int(sting_at*1000)}|{int(sting_at*1000)}[s];"
             "[n][s]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.94:level=false[m]")
         if not a.music else
          f"[0:a]apad[n];[2:a]adelay={int(sting_at*1000)}|{int(sting_at*1000)}[s];"
          f"[3:a]volume=-10.0dB[bed];[n][s][bed]amix=inputs=3:duration=first:normalize=0,alimiter=limit=0.94:level=false[m]")
    cmd = ["ffmpeg","-y","-v","error","-i",nar,"-i",out,"-i",sting]
    if a.music: cmd += ["-i", os.path.abspath(a.music)]
    cmd += ["-filter_complex",fc,"-map","1:v","-map","[m]","-c:v","copy",
            "-c:a","aac","-b:a","160k","-ar","48000","-shortest",tmp]
    r = run(cmd)
    if r.returncode: fail(r.stderr[-400:])
    os.replace(tmp, out)

    vol = run(["ffmpeg","-i",out,"-af","volumedetect","-f","null","-"]).stderr
    mean = [l for l in vol.splitlines() if "mean_volume" in l]
    mx = [l for l in vol.splitlines() if "max_volume" in l]
    qc = a.qc_dir or work
    os.makedirs(qc, exist_ok=True)
    run(["ffmpeg","-y","-v","error","-ss",f"{vd-0.9:.2f}","-i",out,
         "-frames:v","1",os.path.join(qc, f"qc_{name}_endcard.png")])

    print(f"\nBRANDED: {out}")
    print(f"runtime: {vd:.2f}s (source {dur:.2f} + endcard {a.endcard_duration}s)")
    print(f"audio:   {mean[0].strip() if mean else '?'} | {mx[0].strip() if mx else '?'}")
    print(f"sting @  {sting_at:.2f}s | QC frame: {qc}\\qc_{name}_endcard.png")

    # optional paid Model API QC — runs only when explicitly asked AND key present
    if a.meta_qc:
        key = os.environ.get("MODEL_API_KEY") or os.environ.get("META_MODEL_API_KEY")
        if not key:
            print("meta-qc: SKIPPED — MODEL_API_KEY not set (local pipeline unaffected)")
        else:
            r = run([sys.executable, os.path.join(HERE, "meta_provider.py"), "qc",
                     out, "--brief", a.brief or "", "--model", a.meta_qc_model, "--paid",
                     "--out", os.path.join(work, f"{name}_meta_qc.json")])
            print(r.stdout.strip()[:600])
            if r.returncode: print("meta-qc: FAILED —", r.stderr[:300])

if __name__ == "__main__":
    main()
