# HumanGPT — asset requirements & cost estimate

Everything needed before `build_video.py` runs. Paid items are marked.

## Required before build

| asset | path | source | status |
|---|---|---|---|
| UI voice id | `config/ui-presenter-lock.json` | pick stock / `design_voice` | ⬜ pick |
| Steve look id | `config/ui-presenter-lock.json` | stock look / `create_prompt_avatar` | ⬜ pick |
| narration ×4 | `audio/n01..n04.wav` + `*_words.json` | `gen_tts.py` (paid ~$0.01) | ⬜ authorized? |
| presenter ×2 | `presenter/vp1.mp4`, `vp4.mp4` | `render_presenter.py` (paid ~$0.43) | ⬜ authorized? |
| title plate | `graphics/title.png` | `render_html.py brand/templates/title.html` | ⬜ free |
| claim plates ×4 | `graphics/claim_0..3.png` | `render_html.py claim.html?claim=…` | ⬜ free |
| endcard | `graphics/endcard.png` | `render_html.py endcard.html` | ⬜ free |
| music bed | `audio/bed.*` (optional) | cleared track — see licensing | ⬜ optional |
| measured pacing | `pacing.json` | ffprobe each wav → update | ⬜ after TTS |

## presenter_jobs.json (create after look chosen)
```json
{
  "look_id": "<STEVE_LOOK_ID>",
  "aspect_ratio": "9:16",
  "resolution": "1080p",
  "jobs": [["vp1", "audio/n01.wav"], ["vp4", "audio/n04.wav"]]
}
```

## Claim plate params (one template, four renders)
- `claim_0`: kicker="Key capabilities" claim="It writes your emails." foot="Results may vary. Steve does his best."
- `claim_1`: same + claim2="It sits in your meetings." (dim→lit per word timing)
- `claim_2`: claim="It remembers every password."
- `claim_3`: + claim2="…and only asks for vacation twice a year."

Word-timed state switches: pull exact times from `timestamps.json` after
`build_captions.py` runs (e.g. claim_1 lights when "meetings" is spoken).

## Music / SFX
- Bed: light corporate underscore at −26dB under narration via
  `mix_music_bed.py`. Source a cleared track (CC-BY with attribution — log
  it — or HeyGen `search_audio_sounds` catalog).
- SFX: optional endcard "sting"/whoosh — not required for v1.

## Estimated cost (labeled assumptions)
- TTS ×4 ≈ **$0.01** (Video A measured ~$0.003/call)
- Avatar renders ×2 @1080p/9:16 ≈ **$0.43** (Video A measured ~$0.21 each)
- Music/SFX $0 · plates/captions/render $0
- **Total ≈ $0.45–0.60 via Developer API**
- Or MCP premium credits: ~4–32 credits depending on engine.
