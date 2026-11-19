# Outstanding Blockers — HumanGPT

## RESOLVED (HumanGPT v1 produced)

| # | blocker | resolution |
|---|---|---|
| 1 | Steve look | **Brody Office 8** `e0337c592ccd408c937337a6a33f9fee` — locked |
| 2 | Narrator voice | **Garret** `f49763c1a284420b8f25f16472d8738e` — locked |
| 3 | `HEYGEN_API_KEY` | supplied by owner for this run (rotate afterward — passed through chat) |
| 4 | Script approval | owner approved, produced as scripted |
| 5 | Music bed | HeyGen catalog `01483ce1` mixed via `mix_music_bed.py` |
| 6 | 9:16 cost unknown | resolved — landscape photo avatar renders true 9:16; 2 renders = **$0.33** |

## REMAINING

| # | blocker | unblock |
|---|---|---|
| 7 | No UI Metricool brand/channels, no R2 bucket/worker | Create Metricool brand + connect Shorts/TikTok/Reels; `wrangler r2 bucket create ui-social-distribution` + deploy `tools/r2-serve` when publishing is approved |
| 8 | Owner review of the actual export | Watch `production/humangpt/exports/humangpt_v1_music.mp4`; certify or request v1.1 changes |

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
