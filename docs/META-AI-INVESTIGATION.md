# Meta AI / Vibes — API & Automation Investigation

Date: 2026 (investigation only — no generation, no credentials, no automation built)

## Verdict

**There is no official API for the Meta AI / Vibes image-to-video experience,
and no permitted way to automate it.** The viable architecture is a
human-in-the-loop handoff: generate in the Meta AI app manually, drop the
MP4 into the repo, and let `tools/brand_clip.py` brand it (implemented).

## What exists (official)

| Surface | Status |
|---|---|
| **Meta AI app / Vibes** | Consumer product. Image→"Animate"→vibe. No public API. Output retrieved manually (download/share in app). |
| **Meta Model API** (`dev.meta.ai`) | Official paid developer API at `api.meta.ai/v1` — **text/image models only**: Muse Wonder/Spark/Ember (text out), Muse Image (image gen/edit), Muse Voice Transcribe, SAM. **No video-generation model is offered.** |
| **Movie Gen** | Research paper only; never released as a product or API. |
| **Muse Video** | Announced as *early preview* — not on Model API, no GA date. |
| `developer.vibes.com` | Unrelated company (Vibes Media LLC — SMS marketing). Not Meta. |

## Why automation is off the table

1. **Meta's own rules prohibit it.** `meta.ai/robots.txt`: "Collection of
   data on Meta AI through automated means is prohibited unless you have
   express written permission." Meta ToS §3: "You may not access or collect
   data from our Products using automated means (without our prior
   permission)" and bars circumventing access controls.
2. **The only working "API" is unofficial.** `VibesAI-api` (GitHub) works
   via `meta_session` cookie extraction from browser DevTools + reversed
   endpoints — exactly the session-token extraction / ToS bypass this
   project prohibits. It also risks account action and can break silently.
3. **Devin Local has no sanctioned computer-use path** for driving a
   logged-in consumer session — and even with one, point 1 makes it
   non-viable.

## If Meta ever opens it

Muse Video on Model API would plug in cleanly: it would be another
`tools/render_*.py` sibling beside `render_presenter.py` (HeyGen). Watch
`dev.meta.ai/docs/models` — worth re-checking quarterly.

## Implemented: local intake workflow

`tools/brand_clip.py` — zero-cost, reuses `build_video.py` + canonical
brand assets (promoted to `brand/assets/`):

```bash
python tools/brand_clip.py <input.mp4> [--name slug] [--music bed.wav]
# -> production/_intake/<name>/<name>_branded.mp4
```

- Preserves the input untouched; generates manifest + empty captions
- Source scaled/cropped to 1080×1920 @25fps, appended 1.8s V4 endcard
- Source audio kept; UI sting mixed at the endcard cut; output limited
  (`alimiter=0.94`, verified -3.0dB peak on test)
- Reports runtime, mean/max volume; writes a QC frame of the endcard
- Verified end-to-end on `vp1_ricky.mp4` (3.16s → 5.56s branded)

## Update — Meta Model API integration (dev.meta.ai)

Official Responses API at `https://api.meta.ai/v1` (Bearer `MODEL_API_KEY`,
OpenAI-compatible). Implemented in `tools/meta_provider.py`, wired into
`brand_clip.py --meta-qc` and the ep3 runbook.

| Capability | Model | Status | Cost |
|---|---|---|---|
| Model discovery | — | `meta_provider.py models` | free |
| Video understanding QC | `muse-ember-1.0` (default) / `muse-spark-1.3` | `qc` subcommand → structured JSON report vs episode brief | per-token: Ember $0.10/$0.50 Mtok, Spark $1.25/$4.25 Mtok — est cents per clip |
| Image generation | `muse-image-1.0` | `image` subcommand → PNG + metadata sidecar | **$0.01/image** |
| Segmentation | `sam-3.1` | `sam` subcommand (optional only) | per image/frame |
| **Video generation** | — | **does not exist on this API** | — |

Safety: all subcommands refuse without `--paid`; key read from env only,
never logged; `store:false` keeps nothing server-side. Contributor-mode
models ($0.10/$0.20 Mtok) deliberately NOT used — they train on your
content. Model QC output is advisory — human review stays the gate.

## Resulting production flow

1. **Manual (Meta side):** prompt ChatGPT image → Meta AI app → Animate →
   download MP4. (Could not be automated legitimately.)
2. **Automated (our side):** `brand_clip.py` → branded review copy.
3. **Manual:** review, approve, publish.

Estimated human time per clip: ~2–4 min of app interaction + one command.
