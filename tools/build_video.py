#!/usr/bin/env python3
"""UI manifest-driven video builder.

Derived from MyAssistedLivingBusiness
`curriculum/production/tools/build_video.py` (MALB V2.3 standard) — the
proven generic renderer. See docs/PROVENANCE.md. Verbatim port: shot types,
validation, concat + duration-preflight mux + ASS caption burn are unchanged
so all certified behavior carries over.

Reads an external shot manifest (JSON) and renders every shot:
    still      — static PNG plate
    graphic    — narration-synchronized state animation (alpha-overlay fades at word times)
    presenter  — presenter clip full-screen (scrim) or framed inset
    reuse      — pass through an existing rendered segment
    broll      — video clip, in/out points, silent, aspect-preserved, optional fades
                 (also accepts a still image -> Ken-Burns zoom motion)

Then concats all segments in manifest order, muxes the narration track and burns
captions (when configured) into the export. Default output: 1920x1080, 25fps,
H.264 yuv420p, -an; final mux adds AAC 48kHz. For UI verticals set the
manifest to "width":1080, "height":1920 — no code change needed.

Usage:
    python build_video.py <manifest.json> [--only s06,s09] [--no-export] [--no-mux]

Determinism: identical manifest + identical inputs => identical segment files.
Manifest paths resolve against the manifest's directory; `fonts_dir`/`narration_wav`
may be repo-relative (auto-detects repo root by searching upward for `public/`,
`.git`, or `brand/`).
"""
import os, sys, json, subprocess, hashlib, shutil

REPO_ROOT_MARKERS = ("brand", ".git")

def find_repo_root(start):
    d = os.path.abspath(start)
    while True:
        if all(os.path.exists(os.path.join(d, m)) for m in REPO_ROOT_MARKERS):
            return d
        nxt = os.path.dirname(d)
        if nxt == d: return os.path.abspath(start)
        d = nxt

def fail(msg):
    print("FATAL:", msg); sys.exit(2)

def probe(path, entry="stream", extra=None):
    args = ["ffprobe","-v","error","-of","json"]
    if extra: args += extra
    args += ["-show_entries", entry, path]
    return json.loads(subprocess.run(args, capture_output=True, text=True).stdout)

def dur_of(path):
    r = probe(path, "format")
    return float(r["format"]["duration"])

def vdim(path):
    s = probe(path, "stream", ["-select_streams","v:0"])["streams"][0]
    return s["width"], s["height"]

class Builder:
    def __init__(self, manifest_path):
        self.mpath = os.path.abspath(manifest_path)
        self.mdir  = os.path.dirname(self.mpath)
        self.m     = json.load(open(self.mpath, encoding="utf-8"))
        self.root  = find_repo_root(self.mdir)
        self.W     = self.m.get("width", 1920)
        self.H     = self.m.get("height", 1080)
        self.fps   = self.m.get("fps", 25)
        self.xf    = self.m.get("xfade", 0.4)
        self.segdir = self.resolve(self.m["segments_dir"], must_exist=False)
        os.makedirs(self.segdir, exist_ok=True)

    def resolve(self, p, must_exist=True):
        """Manifest-relative first, then repo-relative."""
        for base in (self.mdir, self.root):
            cand = os.path.abspath(os.path.join(base, p))
            if os.path.exists(cand): return cand
        cand = os.path.abspath(os.path.join(self.mdir, p))
        if must_exist: fail(f"missing asset: {p} (looked in manifest dir + repo root)")
        return cand

    # ── shot builders ────────────────────────────────────────────────
    def still(self, png, d, name):
        out = os.path.join(self.segdir, name + ".mp4")
        subprocess.run(["ffmpeg","-y","-loop","1","-t",f"{d:.3f}","-i",png,
            "-vf",f"scale={self.W}:{self.H}:force_original_aspect_ratio=increase,crop={self.W}:{self.H},fps={self.fps}",
            "-c:v","libx264","-pix_fmt","yuv420p","-an",out],check=True,capture_output=True)
        return out

    def graphic(self, states, d, name):
        """states = [(png, start_sec)] ascending — narration-word-timed alpha-overlay fades."""
        if len(states) == 1:
            return self.still(states[0][0], d, name)
        inputs = ["-loop","1","-t",f"{d:.3f}","-i",states[0][0]]
        fc = ["[0:v]format=yuv420p[bg]"]
        prev = "bg"
        for i,(png,st) in enumerate(states[1:],1):
            inputs += ["-loop","1","-t",f"{d-st:.3f}","-i",png]
            fc.append(f"[{i}:v]format=rgba,setpts=PTS-STARTPTS+{st}/TB,"
                      f"fade=t=in:st={st}:d={self.xf}:alpha=1[o{i}]")
            nxt = "v" if i == len(states)-1 else f"b{i}"
            fc.append(f"[{prev}][o{i}]overlay=0:0[{nxt}]")
            prev = nxt
        out = os.path.join(self.segdir, name + ".mp4")
        subprocess.run(["ffmpeg","-y",*inputs,"-filter_complex",";".join(fc),
            "-map",f"[{prev}]","-t",f"{d:.3f}","-c:v","libx264","-pix_fmt","yuv420p","-an",out],
            check=True,capture_output=True)
        return out

    def presenter_fs(self, mp4, d, name, offset=0.0):
        """Full-screen presenter: source scaled-to-fill the whole canvas
        (no frame/margins), last frame held to shot duration, subtle bottom
        scrim for caption contrast."""
        vf = (f"scale={self.W}:{self.H}:force_original_aspect_ratio=increase,"
              f"crop={self.W}:{self.H},tpad=stop=-1:stop_mode=clone,"
              f"drawbox=y=ih-{(220 if self.H>=1080 else int(self.H*0.2))}:w=iw:h={(220 if self.H>=1080 else int(self.H*0.2))}:color=black@0.30:t=fill,"
              f"fps={self.fps},format=yuv420p")
        out = os.path.join(self.segdir, name + ".mp4")
        subprocess.run(["ffmpeg","-y","-ss",f"{offset:.3f}","-i",mp4,
            "-vf",vf,"-t",f"{d:.3f}","-c:v","libx264","-pix_fmt","yuv420p","-an",out],
            check=True,capture_output=True)
        return out

    def presenter(self, mp4, d, name, offset=0.0):
        """Presenter in a rounded-corner inset card on brand field — no badge."""
        w,h = vdim(mp4); aspect = w/h
        cw = 960 if aspect > 1 else 620
        if self.H > self.W:  # vertical canvas: widen the inset
            cw = int(self.W * 0.78)
        ch = round(cw/aspect)
        x0,y0 = (self.W-cw)//2 - 30, (self.H-ch)//2
        frame = os.path.join(self.segdir, f"frame_nb_{name}.png")
        if not os.path.exists(frame):
            from PIL import Image, ImageDraw
            img = Image.new("RGBA",(self.W,self.H),(16,24,40,255))
            dr = ImageDraw.Draw(img)
            dr.rounded_rectangle([x0-8,y0-8,x0+cw+8,y0+ch+8],radius=36,outline=(46,91,255,255),width=5)
            hole = Image.new("L",(self.W,self.H),255)
            ImageDraw.Draw(hole).rounded_rectangle([x0,y0,x0+cw,y0+ch],radius=28,fill=0)
            img.putalpha(hole); img.save(frame)
        vf = (f"color=0x101828:s={self.W}x{self.H}:r={self.fps}:d={d:.3f}[bg];"
              f"[0:v]scale={cw}:-2,format=rgba[c];"
              f"[bg][c]overlay={x0}:{y0}[o1];"
              f"[o1][1:v]overlay=0:0,format=yuv420p,fps={self.fps}")
        out = os.path.join(self.segdir, name + ".mp4")
        subprocess.run(["ffmpeg","-y","-ss",f"{offset:.3f}","-i",mp4,
            "-loop","1","-t",f"{d:.3f}","-i",frame,
            "-filter_complex",vf,"-t",f"{d:.3f}","-c:v","libx264","-pix_fmt","yuv420p","-an",out],
            check=True,capture_output=True)
        return out

    def broll(self, src, d, name, tin=0.0, tout=None, fade_in=0.0, fade_out=0.0, mode="cover", scrim=False):
        """Silent B-roll: video clip (in/out points) or still image (Ken-Burns), scaled to canvas.
        mode: cover = scale-to-fill + center crop (default, no bars) | contain = fit + pad."""
        ext = os.path.splitext(src)[1].lower()
        is_img = ext in (".png",".jpg",".jpeg",".webp")
        scale = (f"scale={self.W}:{self.H}:force_original_aspect_ratio=increase,crop={self.W}:{self.H}"
                 if mode == "cover" else
                 f"scale={self.W}:{self.H}:force_original_aspect_ratio=decrease,"
                 f"pad={self.W}:{self.H}:(ow-iw)/2:(oh-ih)/2:color=black")
        out = os.path.join(self.segdir, name + ".mp4")
        if is_img:
            vf = f"{scale},zoompan=z='min(zoom+0.0008,1.15)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s={self.W}x{self.H},fps={self.fps}"
            inputs = ["-loop","1","-t",f"{d:.3f}","-i",src]
        else:
            sdur = dur_of(src)
            end  = tout if tout is not None else tin + d
            if end > sdur + 0.05:
                fail(f"{name}: broll out point {end:.2f}s exceeds source duration {sdur:.2f}s")
            vf = f"{scale},fps={self.fps}"
            inputs = ["-ss",f"{tin:.3f}","-to",f"{end:.3f}","-i",src]
        fades = ""
        if scrim:
            sh = 220 if self.H>=1080 else int(self.H*0.2)
            fades += f",drawbox=y=ih-{sh}:w=iw:h={sh}:color=black@0.30:t=fill"
        if fade_in:  fades += f",fade=t=in:st=0:d={fade_in}"
        if fade_out: fades += f",fade=t=out:st={d-fade_out:.3f}:d={fade_out}"
        subprocess.run(["ffmpeg","-y",*inputs,
            "-vf",vf+fades+",format=yuv420p",
            "-t",f"{d:.3f}","-c:v","libx264","-pix_fmt","yuv420p","-an",out],
            check=True,capture_output=True)
        return out

    # ── validation ───────────────────────────────────────────────────
    def validate(self, shots):
        errs, total = [], 0.0
        for s in shots:
            t, sid = s["type"], s["id"]
            total += s["duration"]
            if t in ("still","reuse"):
                self.resolve(s["source"])
            elif t == "presenter":
                self.resolve(s["source"])
            elif t == "graphic":
                times = [st for _,st in s["states"]]
                for png,_ in s["states"]: self.resolve(png)
                if times != sorted(times): errs.append(f"{sid}: state times not ascending")
                if times and times[0] != 0: errs.append(f"{sid}: base state must start at 0")
                if times and times[-1] >= s["duration"]: errs.append(f"{sid}: last state >= duration")
            elif t == "broll":
                sp = self.resolve(s["source"])
                if os.path.splitext(sp)[1].lower() not in (".png",".jpg",".jpeg",".webp"):
                    end = s.get("out", s.get("in",0)+s["duration"])
                    if end > dur_of(sp) + 0.05:
                        errs.append(f"{sid}: broll needs {end:.1f}s but source is {dur_of(sp):.1f}s")
            else:
                errs.append(f"{sid}: unknown type '{t}'")
        return errs, total

    # ── pipeline ─────────────────────────────────────────────────────
    def build(self, only=None, do_export=True, do_mux=True):
        shots = self.m["shots"]
        if only:
            shots = [s for s in shots if s["id"] in only]
            if not shots: fail(f"--only matched no shots: {only}")
        errs, total = self.validate(shots)
        if errs:
            for e in errs: print("  x", e)
            fail(f"{len(errs)} validation error(s)")
        print(f"manifest ok — {len(shots)} shots, {total:.2f}s target")
        files = []
        for s in shots:
            d, sid, t = s["duration"], s["id"], s["type"]
            if   t == "still":     src = self.still(self.resolve(s["source"]), d, sid)
            elif t == "reuse":     src = self.resolve(s["source"])
            elif t == "presenter":
                pf = self.presenter_fs if s.get("fullscreen") else self.presenter
                src = pf(self.resolve(s["source"]), d, sid, s.get("offset",0.0))
            elif t == "graphic":   src = self.graphic([(self.resolve(png),st) for png,st in s["states"]], d, sid)
            elif t == "broll":     src = self.broll(self.resolve(s["source"]), d, sid,
                                        s.get("in",0.0), s.get("out"),
                                        s.get("fade_in",0.0), s.get("fade_out",0.0), s.get("mode","cover"),
                                        s.get("scrim",False))
            files.append((src,d))
            print(f"{sid:6s} {d:6.2f}s  {t}")
        print("segments done; total", round(total,2),"s")
        if not do_export:
            return files
        # concat (stream copy)
        lst = self.resolve(self.m["concat_list"], must_exist=False)
        with open(lst,"w") as f:
            for fp,_ in files: f.write(f"file '{fp.replace(os.sep,'/')}'\n")
        vonly = self.resolve(self.m["concat_out"], must_exist=False)
        subprocess.run(["ffmpeg","-y","-f","concat","-safe","0","-i",lst,"-c","copy",vonly],
            check=True,capture_output=True)
        print("concat:", vonly)
        if not do_mux:
            return files
        narr = self.resolve(self.m["narration_wav"])
        # PREFLIGHT: narration vs assembled video duration — never silently truncate content.
        vdur, adur = dur_of(vonly), dur_of(narr)
        tol = self.m.get("duration_tolerance", 0.5)
        if abs(vdur - adur) > tol:
            fail(f"duration mismatch: video {vdur:.2f}s vs narration {adur:.2f}s "
                 f"(tolerance {tol}s) — fix the manifest or narration, not -shortest")
        cap  = self.resolve(self.m["captions_ass"]).replace("\\","/").replace(":","\\:")
        fonts = self.resolve(self.m["fonts_dir"]).replace("\\","/").replace(":","\\:")
        out  = self.resolve(self.m["export"], must_exist=False)
        subprocess.run(["ffmpeg","-y","-i",vonly,"-i",narr,
            "-filter_complex",f"[0:v]subtitles='{cap}':fontsdir='{fonts}'[v]",
            "-map","[v]","-map","1:a","-c:v","libx264","-crf","18","-pix_fmt","yuv420p",
            "-c:a","aac","-b:a","160k","-ar","48000",out],
            check=True,capture_output=True)
        print("EXPORT:", out, round(dur_of(out),2),"s")
        return files

if __name__ == "__main__":
    args = sys.argv[1:]
    if not args: print(__doc__); sys.exit(1)
    mp = args[0]
    only = set(args[args.index("--only")+1].split(",")) if "--only" in args else None
    Builder(mp).build(only=only, do_export="--no-export" not in args, do_mux="--no-mux" not in args)
