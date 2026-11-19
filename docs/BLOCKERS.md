# Outstanding Blockers — HumanGPT

Ordered; each names its unblock action.

| # | blocker | impact | unblock |
|---|---|---|---|
| 1 | **Steve presenter look not chosen** — `config/ui-presenter-lock.json` has null look ids | Can't render presenter shots (s01, s04) or verify_presenter passes | Pick: HeyGen stock/public look (fastest, licensed), `create_prompt_avatar`, or consented actor photo avatar → record `group_id`/`approved_look_ids` |
| 2 | **UI narrator voice not chosen** — `voice_id` null | Can't run `gen_tts.py` (fails closed) | Pick HeyGen stock voice or `design_voice` "corporate tech-ad deadpan" → record `voice_id` |
| 3 | **`HEYGEN_API_KEY` not in current env** | All paid calls blocked | Resupply the funded Dev API key (existed Nov 16–17 for MALB Video A) or use HeyGen MCP tools |
| 4 | **Script not owner-approved** | Gate 1 stops all downstream | Owner reads `production/humangpt/SCRIPT.md`, approves or edits `script.json` |
| 5 | **Music bed not selected** | Mix step can't run; video is still complete without it | Pick cleared track (CC-BY w/ attribution, or HeyGen `search_audio_sounds`); log license in ASSET-REQUIREMENTS |
| 6 | **Avatar engine/cost unconfirmed for 9:16** | Cost estimate has a range, not a point | One dry-run/`v3/videos` quote or check `supported_api_engines` on the chosen look before rendering |
| 7 | **No UI Metricool brand/channels, no R2 bucket/worker** | Can't publish (not needed to *produce*) | Create Metricool brand + connect Shorts/TikTok/Reels; `wrangler r2 bucket create ui-social-distribution` + deploy `tools/r2-serve` when publishing is approved |

## Estimated HumanGPT cost (assumption-labeled)

Based on MALB Start Video A measured rates (Developer API, Nov 16–17):

| item | qty | est. cost |
|---|---|---|
| TTS beats (with timestamps) | 4 | ~$0.01 |
| Avatar renders (1080p 9:16, ~4–6s each) | 2 | ~$0.43 |
| Music/SFX | — | $0 (CC-BY/catalog) |
| Local render + captions + plates | — | $0 |
| **Total** | | **~$0.45–0.60** |

Or via HeyGen MCP premium credits: 2 renders ≈ 4–32 credits depending on
engine (Avatar IV cheap / Avatar V ~16 each per blueprint data) — 600
credits available on the subscription. Dev API path is cheaper and has
exact wallet accounting.
