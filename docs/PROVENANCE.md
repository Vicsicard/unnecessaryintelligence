# Provenance & Licensing

Every reused component's origin, what changed, and license state.

## Ported code

| UI file | Source | Change |
|---|---|---|
| `tools/build_video.py` | MALB `curriculum/production/tools/build_video.py` (V2.3-certified) | verbatim + vertical-inset width fix |
| `tools/gen_tts.py` | malb-builder-4 `start-video-a-v1/gen_tts.py` | script/voice externalized, `--dry-run` |
| `tools/render_presenter.py` | malb-builder-4 `start-video-a-v1/render_jonas.py` | look id from lock, jobs JSON, `--dry-run` |
| `tools/verify_presenter.py` | MALB `curriculum/production/tools/verify_presenter.py` | UI lock path, unconfigured = fail |
| `tools/build_captions.py` | MALB `blueprint-promo/_build_narr.py` pattern | script/pacing-driven, adds VTT+chars support |
| `tools/mix_music_bed.py` | CHM `episodes/episode-002/project/mix_music.py` pattern | generic `sidechaincompress`, no block timings |
| `tools/render_html.py` | MALB `gen_state_html.py` + Edge-screenshot practice | generic batch renderer |
| `tools/r2-serve/` | CHM `tools/r2-serve` worker | **defect fix**: UPLOAD_KEY was committed plaintext there — here it's a Wrangler secret |

## What was deliberately NOT copied

- **MALB presenter assets** (Jonas looks/voice) and **CHM assets** (Jerome,
  Chatterbox config) — brand-locked to their productions. UI needs its own
  Steve.
- **MALB asset library** — licensed/approved for MALB only.
- **CHM wrangler secrets** — the CHM `r2-serve` has a plaintext upload key
  in source; flagged as a known defect, not reproduced here.
- **Modal/Chatterbox TTS** — proven for CHM long-form but heavier than the
  Dev API path that produced Video A at $0.45; kept as future option.

## Fonts (vendored)

| file | license |
|---|---|
| `brand/fonts/Inter.ttf`, `Inter-SemiBold.ttf` | SIL OFL 1.1 — free to embed/redistribute |
| `brand/fonts/Playfair-Bold.ttf` | SIL OFL 1.1 |

## Music/SFX policy

- Not vendored. Per-production: supply a cleared track.
- CC-BY sources (e.g. incompetech, used by CHM EP002 for "Peace of Mind")
  require attribution in the video description — log it in the production's
  ASSET-REQUIREMENTS.md.
- HeyGen `search_audio_sounds` MCP catalog is available for bed candidates.

## Known inherited constraints

- Avatar V 1080p cost was higher than MCP implied for MALB blueprint
  (~16 premium credits/render). Prefer the Developer API path (Video A:
  ~$0.22/avatar render) or Avatar IV unless quality demands V.
- `presenter` fullscreen scrim burns a dark band — caption MarginV sits
  above it; don't place claim text in the bottom 14%.
- Historical CHM `tpad=stop=` bug is absent here (`stop_duration`/clone
  patterns used) — keep packet-count checks if you add freeze tails.
