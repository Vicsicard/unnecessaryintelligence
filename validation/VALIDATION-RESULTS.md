# Local Validation Results — UI foundation

Run on init day. **Zero paid API calls** — everything below ran on local
ffmpeg/Edge/Python only, or with paid paths stubbed via `--dry-run`.

## Passed

| check | command | result |
|---|---|---|
| Tool syntax | `python -m py_compile tools/*.py tools/tests/*.py` | OK — all 8 files compile |
| Test assets | `python tools/tests/make_test_assets.py` | plates + 4s/1080×1920 clip + wav + ASS generated |
| Full render | `python tools/build_video.py tools/tests/test_manifest.json` | 4 shots → segments → concat → duration preflight → mux+burned captions → `tools/tests/assets/test.mp4` |
| Export spec | `ffprobe test.mp4` | **h264, 1080×1920, 25fps, AAC, 9.000s** — target spec |
| HTML→PNG plates | `render_html.py endcard.html` (1080×1920) + `meme.html` (1080×1080) | `validation/out/endcard.png`, `meme.png` — fonts load, params work, endcard visually verified |
| Captions chain | `build_captions.py --prod tools/tests/assets` | `narration.wav` 8.50s (beat placed at pacing offset), `timestamps.json` word map, ASS 2 cues + SRT + VTT + transcript |
| Presenter lock | `verify_presenter.py --list-approved` | exit 3 — fail-closed until look/voice configured ✓ |
| TTS dry-run | `gen_tts.py --script production/humangpt/script.json --dry-run` | prints 4-beat plan + "voice NOT CONFIGURED (blocker #2)", **no API calls** |
| Render dry-run | `render_presenter.py --jobs presenter_jobs.json --dry-run` | prints 2-job plan + "look NOT CONFIGURED (blocker #1)", flags missing audio, **no API calls** |

## Fixed during validation

- `build_captions.py`: ffmpeg input index bug — used argv length as stream
  index; now enumerated per-beat (`[i:a]`). Caught by the smoke test.
- `gen_tts.py` / `render_presenter.py` `--dry-run`: previously hard-stopped
  on missing voice/look before showing the plan; dry-run now prints the
  plan with the blocker labeled.

## Exercised (proving the MALB port carries over)

- `still` shot type (title + endcard plates)
- `presenter` shot type, `fullscreen:true` (scrim band, hold to duration)
- `graphic` shot type (two-state word-timed alpha fade)
- concat → **duration preflight** → mux AAC → burned ASS captions
- 1080×1920 canvas via manifest config (no code change)

## Not exercised (need paid calls or configured identity — see docs/BLOCKERS.md)

- `gen_tts.py` live TTS + word timestamps
- `render_presenter.py` live avatar render
- `verify_presenter.py` live look verification
- `mix_music_bed.py` (no cleared track selected yet)
- `tools/r2-serve` deploy (no bucket/account yet — publishing gate)
