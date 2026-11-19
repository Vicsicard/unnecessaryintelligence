# UI Production SOP — fictional commercials

Owner gates marked **[GATE]**. No paid step runs before its gate.

## 1. Script
- Write `production/<slug>/script.json` — beats (`n01`, `n02`…), order,
  transcript lines, optional `voice_id`.
- ~2.7 words/sec target: a 20s ad ≈ 45–55 spoken words.
- **[GATE] Owner approves script.**

## 2. Identity (first production only)
- Pick Steve presenter look + UI narrator voice; record real ids in
  `config/ui-presenter-lock.json`.
- Verify: `python tools/verify_presenter.py --look-id <id>` (live check
  needs `HEYGEN_API_KEY`).
- **[GATE] Owner approves look + voice.**

## 3. Narration (paid)
```
cd production/<slug>
python ../../tools/gen_tts.py --script script.json --out audio --dry-run
python ../../tools/gen_tts.py --script script.json --out audio
```
- Writes `audio/n*.wav` + `n*_words.json`. Idempotent — existing files are
  never re-billed.
- **[GATE] First paid call — owner authorizes.**

## 4. Pacing
- Measure each wav (`ffprobe`); write `pacing.json` — beat start offsets +
  total. Leave breaths (~0.3–0.5s) between beats.
```
python ../../tools/build_captions.py --prod .
```
- Produces `narration.wav`, `timestamps.json`, `captions/` (ASS/SRT/VTT).

## 5. Plates + graphics (free)
```
python ../../tools/render_html.py --jobs render_jobs.json
```
- jobs map `brand/templates/*.html` + params → `graphics/*.png`.
- Word-timed states: use `timestamps.json` word times for `graphic` shot
  `states` in the manifest.

## 6. Presenter clips (paid)
- Build `presenter_jobs.json`; dry-run first.
```
python ../../tools/verify_presenter.py --look-id <id>
python ../../tools/render_presenter.py --jobs presenter_jobs.json --dry-run
python ../../tools/render_presenter.py --jobs presenter_jobs.json
```
- **[GATE] Owner authorizes render spend.**

## 7. Assemble + export (free)
```
python ../../tools/build_video.py manifest_v1.json
```
- Validation → segments → concat → **duration preflight** (video vs
  narration; never silently truncates) → mux + burned ASS.
- Optional music: `mix_music_bed.py narration.wav track.mp3` then remux.
- **[GATE] Human review** — watch the export end-to-end; check caption
  safe area, joke timing, brand lockup. Then certify.

## 8. Static meme (free)
- `render_html.py brand/templates/meme.html production/<slug>/exports/meme.png --w 1080 --h 1080`
  with `top`/`bot`/`img` params.

## 9. Publish (future gate)
- Deploy `tools/r2-serve`, upload export, schedule via Metricool — after
  the UI brand + channels exist and owner approves.
