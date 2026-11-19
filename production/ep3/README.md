# UI Episode 3 — Production Runbook

Pipeline: `brief → ChatGPT image → Meta AI (manual) → MP4 intake → branding → review`
The Meta animation step is **manual** — no permitted API exists
(`docs/META-AI-INVESTIGATION.md`). Everything downstream is one command.

## Drop zone

| File | Put it here |
|---|---|
| Approved creative brief | `production/ep3/BRIEF.md` (or `--brief` path) |
| ChatGPT starting image | `production/ep3/source/` (reference only) |
| Meta-animated MP4 | `production/ep3/source/` |

`source/` is gitignored — external media stays local.

## Produce the branded cut (one command)

```bash
python tools/brand_clip.py "production/ep3/source/<meta_render>.mp4" \
    --name ep3_v1 --out "production/ep3/exports/ep3_v1_branded.mp4"
```

Adds: 1080×1920 normalize → V4 endcard (1.8s) → UI sting → limiter.
Prints runtime + audio levels + preflight warnings; writes an endcard QC frame
next to the output.

## Optional paid features (off by default)

```bash
# Model API video QC against the brief (~$0.01–0.10 est, Muse Ember)
set MODEL_API_KEY=...   # or export; never committed
python tools/brand_clip.py "production/ep3/source/<meta_render>.mp4" \
    --name ep3_v1 --meta-qc --brief production/ep3/BRIEF.md \
    --out "production/ep3/exports/ep3_v1_branded.mp4"

# or standalone:      python tools/meta_provider.py qc <mp4> --brief BRIEF.md --paid
# verify key/models:  python tools/meta_provider.py models        (free)
# Muse Image:         python tools/meta_provider.py image "<prompt>" --out dir --paid
# SAM 3.1 (optional): python tools/meta_provider.py sam <mp4> "<noun>" --paid
```

All Meta calls are OFF without `MODEL_API_KEY` and refuse without `--paid`.
Provider: `tools/meta_provider.py` — stateless Responses API, official
endpoints only, no video generation (none exists).

## Review

`http://127.0.0.1:8790/` serves the repo — play the export, compare against
BRIEF.md. Meta QC output is advisory, not approval.
