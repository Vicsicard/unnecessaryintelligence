# UI Architecture

One render path, manifest-driven. Everything is a file in `production/<slug>/`;
tools are shared and production-agnostic.

```
                 ┌─────────────────────────┐
 script.json ──▶ │ gen_tts.py (paid)       │──▶ audio/n*.wav, n*_words.json
                 │   HeyGen Dev API TTS    │
 presenter_jobs ─▶│ render_presenter.py (paid) ─▶ presenter/vp*.mp4
                 │   uploads wav, renders  │
                 │   avatar clip, idempotent│
 brand/templates ─▶│ render_html.py (free) │──▶ graphics/*.png
                 │   Edge headless screenshot│
 pacing.json ────▶│ build_captions.py (free) ─▶ narration.wav,
                 │   adelay+amix, word cues │   timestamps.json, ASS/SRT/VTT
 manifest*.json ─▶│ build_video.py (free)  │──▶ exports/*.mp4
                 │   shots→segments→concat │
                 │   →preflight mux→captions│
 music ─────────▶│ mix_music_bed.py (free)│──▶ bed-ducked mix or remux
                 └─────────────────────────┘
```

## Production dir contract (`production/<slug>/`)

| file | role |
|---|---|
| `script.json` | `{beats:{id:text}, beat_order:[], transcript:{}, voice_id?}` — input to gen_tts + captions |
| `pacing.json` | `{beat: start_sec, ..., "total": s}` — manual pacing; written after narration is measured |
| `presenter_jobs.json` | `{look_id?, aspect_ratio, resolution, jobs:[[tag, wav], ...]}` |
| `audio/` | `n*.wav`, `n*_words.json`/`*_chars.json`, `narration.wav` (generated) |
| `graphics/` | PNG plates rendered from `brand/templates` |
| `presenter/` | `vp*.mp4` clips + `_jobs.json` idempotency registry |
| `captions/` | generated ASS/SRT/VTT/transcript |
| `manifest_vN.json` | shot list — versioned; never edit a certified one |
| `timestamps.json` | generated word-timing map (drives graphic states) |
| `exports/` | final mp4s (gitignored) |

## Shot types (build_video.py)

| type | use | source |
|---|---|---|
| `still` | title/end cards, static claims | PNG |
| `graphic` | narration-synced multi-state claim plates (word-timed fades) | ordered `[(png, t)]` |
| `presenter` | avatar clip — `fullscreen:true` for direct-to-camera, else inset card | MP4 + offset |
| `broll` | licensed clips/stills, in/out points, cover/contain, fades, scrim | MP4/PNG |
| `reuse` | pass a previously rendered segment straight through | MP4 segment |

## Adaptations vs MALB original

- `build_video.py`: verbatim port + one addition — `presenter` non-fullscreen
  inset width auto-widens to 78% on vertical canvas (was 620px for 16:9).
- `gen_tts.py`: was single-purpose MALB script; now reads beats from
  `script.json`, voice from `config/ui-presenter-lock.json`, `--dry-run` added.
- `render_presenter.py`: was `render_jonas.py` hardcoded to Jonas look id;
  now reads look from lock file or jobs JSON, `--dry-run` added.
- `verify_presenter.py`: same fail-closed gate, pointed at
  `config/ui-presenter-lock.json`; exits 3 until configured.
- `build_captions.py`: generalized from blueprint `_build_narr.py` —
  script/pacing-driven, outputs ASS/SRT/VTT/transcript at manifest canvas.
- `mix_music_bed.py`: CHM ducking pattern as generic `sidechaincompress`
  (no per-block timing needed).
- `render_html.py`: new small tool formalizing the Edge-screenshot pattern
  MALB used for state plates; batch mode via jobs JSON.
- `tools/r2-serve/`: CHM pattern minus the committed secret —
  `UPLOAD_KEY` is a Wrangler secret now.

## Publishing path (future, not built)

exports → `tools/r2-serve` worker (`ui-social-distribution` bucket) →
public URL → Metricool schedule (YouTube Shorts/TikTok/Reels). Requires:
bucket + worker deploy, UI Metricool brand, channel connections.
