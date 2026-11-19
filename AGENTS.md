# Unnecessary Intelligence (UI) — agent notes

Satirical fictional-product commercials. Built on the MALB manifest-driven
pipeline (ported to `tools/`); see `docs/ARCHITECTURE.md` and
`docs/PROVENANCE.md`.

## Hard gates

- **No paid calls** (HeyGen TTS/avatar renders, any API spend) without
  explicit owner authorization. `--dry-run` flags exist on `gen_tts.py` and
  `render_presenter.py` — use them to validate plans for free.
- **No publishing** — no Metricool scheduling, no R2 deploys, no website
  work — until the owner creates the UI brand/channels and approves.
- **No secrets in the repo.** `.env` is gitignored; `HEYGEN_API_KEY` is
  read from env only. The CHM `r2-serve` pattern's hardcoded-key defect is
  why `tools/r2-serve/worker.js` uses a Wrangler secret.
- **Presenter lock is fail-closed.** `tools/verify_presenter.py` exits
  non-zero until `config/ui-presenter-lock.json` has real look/voice ids.
  Never render an unlisted look; never reuse MALB Jonas/CHM Jerome assets.

## Environment

- ffmpeg/ffprobe on PATH (9.x verified), Python 3.11, PIL for test assets.
- Headless Edge at `C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe`
  for HTML→PNG plates (`tools/render_html.py`). Edge clamps `--window-size`
  to ≥500px — all UI plates are 1080×1920 so this is fine.
- `HEYGEN_API_KEY` must be supplied in the environment for any paid step.

## Validate changes

```
python -m py_compile tools/*.py
python tools/tests/make_test_assets.py     # free local assets
python tools/build_video.py tools/tests/test_manifest.json
```

Expected: `tools/tests/assets/test.mp4` — 1080×1920, 25fps, h264, aac.
