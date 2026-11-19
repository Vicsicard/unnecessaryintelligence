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
- **UI-HEYGEN-API-ONLY** (permanent, see `docs/UI-HEYGEN-API-ONLY.md`):
  all HeyGen generation goes through the Developer API wallet only —
  subscription/Studio/Playground/web credits are prohibited, no billing
  fallback ever. `render_presenter.py` refuses paid submits when the API
  wallet balance is unreadable; engines are allowlisted in
  `config/ui-heygen-policy.json` (Avatar IV default; Avatar 6 Turbo opt-in
  via `avatar_engine` in presenter jobs). HeyGen MCP tools are approved
  for read-only discovery only — never for paid generation.
- **Presenter lock is fail-closed.** `tools/verify_presenter.py` exits
  non-zero until `config/ui-presenter-lock.json` has real look/voice ids.
  Never render an unlisted look; never reuse MALB Jonas/CHM Jerome assets.
  `--require-engine <engine>` also verifies a look's `supported_api_engines`
  before Avatar 6 renders.

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

## Owner review (always, after any production)

After producing any export, serve the production dir on a local port so the
owner can review in a browser — do this every time, unprompted:

```
cd production/<slug> && python -m http.server 8790 --bind 127.0.0.1
# -> http://127.0.0.1:8790/exports/   (preview/ QC frames also reachable)
```
