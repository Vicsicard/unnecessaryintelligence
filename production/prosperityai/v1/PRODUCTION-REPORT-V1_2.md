# ProsperityAI v1.2 — Production Report (Ricky founder)

**Master:** `exports/prosperityai_v1_2_music.mp4` · 31.6 s · 1080×1920, 9:16,
h264, aac 160k, 25 fps
**Review URL:** `http://127.0.0.1:8790/prosperityai/v1/exports/prosperityai_v1_2_music.mp4`
**Base:** v1.1 graphics/audio/structure; founder re-cast. v1 + v1.1 untouched.

## What changed from v1.1

| | v1.1 (Sebastian) | v1.2 (Ricky) |
|---|---|---|
| Founder | Sebastian Office 11 — seated office shot composited inside a rendered mega-screen | Ricky `94e7ae7f` — **standing on a real keynote stage**, LED grid wall + spotlights + clicker + earpiece, full-frame |
| Framing | Letterboxed landscape crop `1080:608:0:656` inside screen | **Native portrait 1080×1920 — no crop, no letterbox** |
| Stage plates | keynote_stage plate held the founder shots | Retired for founder shots; **kept only for the finale wide auditorium shot** |
| Opening | Founder on mega-screen + marquee | Founder full-frame, "POVERTY ENDS TODAY" drops onto a lower-third navy band @0.95s |
| s03 | Founder on mega-screen | Founder full-frame + "FINANCIAL INCLUSION INITIATIVE" orange kicker (PIL) |
| Finale | Ovation plate + confetti 5.8s | **Two-beat:** founder delivers line 2.8s → cut to wide ovation shot 3.0s — founder's held frame plays inside the mega-screen while audience rises + confetti falls. Matches the original spec's "wide auditorium shot". |
| Applause timing | @26.0 | retimed @27.0 (ovation cut +0.2) |

## Avatar investigation → adoption

- Candidate `380e45e5` (landscape) led to the Ricky group (20 looks); owner selected `94e7ae7f` portrait stage look.
- Verified via Developer API: `photo_avatar`, completed, **all 5 engines** supported on every look incl. `heygen-avatar-6` + `heygen-avatar-6-turbo`; works with existing `audio_asset_id` workflow.
- Controlled test (`presenter_ricky/vp1_ricky.mp4`, auditorium look `e7dd61a7`, n01, $0.15) confirmed native-portrait output, zero letterboxing, honored motion prompts.
- Presenter-lock: new `founder_ricky` character; `founder` (Sebastian) archived, not deleted.

## Cost — v1.2 incremental

| Item | Actual |
|---|---|
| Controlled Ricky test (vp1_ricky, 3.16s) | $0.15 |
| 3 founder renders on 94e7ae7f (n01 3.16s + n04 2.39s + n05 4.06s) | **$0.60** (wallet 2.52→1.92, ~$0.062/s blended) |
| **Total session spend** | **$0.75** |
| Everything else | $0 — local PNG/ffmpeg/PIL |

Note: observed per-second metering ran higher on this batch (~$0.062/s) than the earlier 3.3s test (~$0.046/s) — pricing varies slightly per render; treat ~$0.05-0.065/s as the planning range for A6T.

## QC

`preview/qc12_*.png` — open (2.0), reveal (9.8), dashboard (15.8), kicker (18.2),
pricing (21.5), closing line (25.5), ovation+confetti+screen (27.8), endcard (30.5).
Fixed during QC: `tagline.png` invisible Edge flake → PIL (alpha 20→full);
empty mega-screen on ovation → held founder frame; confetti retimed 0.0/0.4/0.8.

## Honest notes

- Founder identity intentionally **changed** (owner-directed re-cast). Lip-sync + voice (Brock wavs) unchanged.
- Audience still silhouette graphics in the wide shot — no video crowd exists; acceptable per spec (visible audience + rising).
- Sebastian v1/v1.1 masters preserved; nothing overwritten.
