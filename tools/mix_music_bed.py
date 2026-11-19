#!/usr/bin/env python3
"""Mix a music bed under narration via ffmpeg sidechain ducking.

Ported pattern: CHM EP002 `episode-002/project/mix_music.py` (ducking
envelope; see docs/PROVENANCE.md) — reimplemented as a generic
`sidechaincompress` filter so it needs no per-block timing data.

    mix_music_bed.py narration.wav music.mp3 out.wav
        [--bed-db -26] [--attack 40] [--release 900] [--fade-out 1.2]
        [--music-start 0] [--video video.mp4 --export out.mp4]

Music is trimmed/looped to narration length, ducked while narration is
active (bed-db when talking), and faded at the tail. `--video` muxes the
mix onto an existing (silent or captioned) master instead of emitting WAV.

Licensing: supply only cleared music. CC-BY tracks (e.g. incompetech)
require attribution in the video description — record it in
ASSET-REQUIREMENTS.md. See docs/PROVENANCE.md.
"""
import argparse, json, subprocess, sys

def dur_of(p):
    r = subprocess.run(["ffprobe", "-v", "error", "-of", "json",
                        "-show_entries", "format", p],
                       capture_output=True, text=True)
    return float(json.loads(r.stdout)["format"]["duration"])

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("narration"); ap.add_argument("music"); ap.add_argument("out")
    ap.add_argument("--bed-db", type=float, default=-26.0)
    ap.add_argument("--peak-db", type=float, default=-10.0)
    ap.add_argument("--attack", type=int, default=40)
    ap.add_argument("--release", type=int, default=900)
    ap.add_argument("--fade-in", type=float, default=0.6)
    ap.add_argument("--fade-out", type=float, default=1.2)
    ap.add_argument("--music-start", type=float, default=0.0)
    ap.add_argument("--video"); ap.add_argument("--export")
    ap.add_argument("--sfx", action="append", default=[],
                    help="extra one-shot sound: 'path.wav@start_seconds[@gain_db]' (repeatable)")
    a = ap.parse_args()
    nd = dur_of(a.narration)
    sfx_parts, sfx_ins, sfx_labels = [], [], []
    base_idx = 3 if (a.video and a.export) else 2
    for i, spec in enumerate(a.sfx):
        parts = spec.rsplit("@", 2)
        if len(parts) == 3:
            path, t, gain = parts
        else:
            path, _, t = spec.rpartition("@")
            gain = "0"
        sfx_ins += ["-i", path]
        sfx_parts.append(f"[{base_idx + i}:a]adelay={int(float(t) * 1000)}|{int(float(t) * 1000)},volume={gain}dB[s{i}]")
        sfx_labels.append(f"[s{i}]")
    duck = f"sidechaincompress=threshold=0.02:ratio=8:attack={a.attack}:release={a.release}:makeup=1"
    fc = (f"[1:a]atrim=start={a.music_start},asetpts=PTS-STARTPTS,"
          f"aloop=loop=-1:size=2e9,atrim=0:{nd + a.fade_out},"
          f"volume={a.peak_db}dB,afade=t=in:st=0:d={a.fade_in},"
          f"afade=t=out:st={nd - a.fade_out if nd > a.fade_out else 0}:d={a.fade_out}[mus];"
          f"[mus][0:a]{duck}[ducked];"
          + (";".join(sfx_parts) + ";" if sfx_parts else "") +
          f"[0:a][ducked]{''.join(sfx_labels)}amix=inputs={2 + len(sfx_labels)}:duration=first:normalize=0[m]")
    if a.video and a.export:
        cmd = ["ffmpeg", "-y", "-i", a.narration, "-i", a.music, "-i", a.video,
               *sfx_ins,
               "-filter_complex", fc, "-map", "2:v", "-map", "[m]",
               "-c:v", "copy", "-c:a", "aac", "-b:a", "160k", "-ar", "48000",
               "-shortest", a.export]
    else:
        cmd = ["ffmpeg", "-y", "-i", a.narration, "-i", a.music, *sfx_ins,
               "-filter_complex", fc, "-map", "[m]",
               "-ac", "1", "-ar", "48000", a.out]
    subprocess.run(cmd, check=True)
    print("mixed:", a.export or a.out)

if __name__ == "__main__":
    main()
