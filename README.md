# Unnecessary Intelligence (UI)

Satirical entertainment brand by DIG Development — professionally produced
fictional commercials and memes. First production: **HumanGPT — "The future
of artificial intelligence is Steve."** (a ~20s corporate tech ad that is
dead-serious until the reveal: the extraordinary AI is an ordinary employee).

Site (planned): UnnecessaryIntelligence.com — not built yet.

## What this repo is

A **production tooling repo**, not a new video engine. It reuses the proven
manifest-driven pipeline built for MyAssistedLivingBusiness (MALB) — ported
to `tools/` — plus the CHM caption/music/R2 patterns. See
`docs/PROVENANCE.md` for every reused file's origin and license status.

## Pipeline shape

```
script.json (beats) ──gen_tts──> audio/n*.wav + *_words.json
HTML templates ──────render_html──> graphics/*.png plates
audio + presenter_jobs ─render_presenter──> presenter/vp*.mp4  (paid gate)
pacing.json ──build_captions──> narration.wav + timestamps.json + ASS/SRT/VTT
manifest ──build_video──> exports/*.mp4 (concat → preflight mux → burned captions)
meme.html ──render_html──> static meme PNG
```

- Canvas: **1080×1920, 25fps** (manifest-set; the renderer is size-agnostic).
- Presenter/narration: HeyGen Developer API (funded wallet) or HeyGen MCP.
- Local render: ffmpeg + Edge headless — zero paid calls needed to validate.

## Layout

| path | contents |
|---|---|
| `tools/` | ported render pipeline + UI adaptations (see ARCHITECTURE) |
| `brand/` | palette.json, OFL fonts, HTML plate templates (title/claim/endcard/meme) |
| `config/` | `ui-brand.json`, `ui-presenter-lock.json` (fail-closed until filled) |
| `production/humangpt/` | first commercial: script, manifest, asset checklist |
| `tools/r2-serve/` | media-serving worker template for future social delivery |
| `tools/tests/` | free end-to-end validation assets + manifest |
| `validation/` | local validation results |
| `docs/` | ARCHITECTURE, PROVENANCE, PRODUCTION-SOP, COSTS |

## Quickstart

```
cp .env.template .env   # fill HEYGEN_API_KEY when authorized for paid steps
python tools/tests/make_test_assets.py
python tools/build_video.py tools/tests/test_manifest.json
```

## Status

Foundation initialized — pipeline tools validated locally (see
`validation/VALIDATION-RESULTS.md`). HumanGPT is spec'd and ready to produce
once the Steve presenter look + UI voice are chosen and paid calls are
authorized. Remaining blockers: `docs/BLOCKERS.md`.
