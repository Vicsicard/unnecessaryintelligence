# HeyGen Avatar 6 — API Investigation & Controlled-Test Plan

Status: **investigation complete · test blocked pending `HEYGEN_API_KEY`**
(The env var is not present in this session — see Blockers.)

## 1. Compatibility report (verified from official docs)

Source: `developers.heygen.com/docs/models/avatar-6` + API reference (Nov 2026).

| # | Question | Answer |
|---|---|---|
| 1 | Does our Developer API support Avatar 6? | Yes — via the same `POST /v3/videos` we already use (`X-Api-Key`, `api.heygen.com`). Account-level eligibility unconfirmed until a live look check runs (needs API key). |
| 2 | Avatar 6 Turbo via same API key? | Yes — same endpoint, `engine.type: "heygen-avatar-6-turbo"`. |
| 3 | `/v3/videos` integration support? | Yes — single-avatar requests only (`type: "avatar"`). Not supported: raw-image requests, studio scenes, batch creation, scene editing. |
| 4 | Engine-selection schema | `"engine": {"type": "heygen-avatar-6[-turbo]", "motion_expressiveness": "default"|"less"}`. Omitting `engine` keeps Avatar IV. |
| 5 | `motion_prompt` schema | Top-level string field on `POST /v3/videos`; plain-language direction for gestures/expression/posture. Overrides `motion_expressiveness` where they overlap. |
| 6 | Motion-prompt length limit | ≤ 1,200 characters (Model API table; same field on Application API). Our test prompt is ~380 chars. |
| 7 | Resolutions | `1080p` (default) or `2k`. `720p`/`4k` NOT supported for Avatar 6. `aspect_ratio`: `16:9` (default), `9:16`, `1:1`, `4:5`, `5:4`, `auto`. |
| 8 | 2K via Developer API? | Supported by spec; billed higher (see pricing). Unverified on our wallet until a render runs. |
| 9 | Photo-plus-audio? | Yes — both routes support photo avatars; the Model API also animates a raw reference photo (`POST /v3/models/avatars`). Our founder is a **photo avatar look** → Application API path. |
| 10 | Existing voices/audio compatible? | Yes — same speech sources (`script`+`voice_id`, `audio_url`, `audio_asset_id`). Our uploaded WAV assets and Brock voice are unchanged. |
| 11 | Existing avatar identities reusable? | Conditional — look must list the engine in `supported_api_engines` on `GET /v3/avatars/looks/{id}`. **Founder look eligibility is unverified** (MCP response omits the field; needs API key). |
| 12 | Lip-sync/input changes? | Same speech-input contract. Avatar 6 adds motion control fields; legacy top-level `expressiveness` is rejected for Avatar 6 (use `engine.motion_expressiveness`). |
| 13 | Extra permissions/activation? | None documented for photo-avatar looks. Digital twins require consent flow; video references are Enterprise-gated (`realistic_human_reference_not_allowed`). |

## 2. Verified pricing (Developer API, pay-as-you-go USD wallet)

Sources: HeyGen self-serve price card (via help article + platform docs,
Nov 19 2026) and prior wallet deltas in this project.

| Engine | 1080p | 2K | Verified? |
|---|---|---|---|
| Avatar IV, photo avatar | ~$0.05/s (our observed delta ≈ $0.037–0.04/s) | n/a | ✔ observed on wallet (3.33→2.97 for ~9.8 s) |
| Avatar 6 Turbo | $0.05/s advertised | $0.0875/s | ✗ advertised — verify from wallet delta |
| Avatar 6 (Pro) | $0.10/s advertised | $0.145/s | ✗ advertised |

- Billing unit: **USD per second of output**, metered to the prepaid API
  wallet (`GET /v3/users/me → data.wallet.remaining_balance`).
- Credits expire 12 months after purchase; no subscription required;
  no free API credits since Feb 2026.
- Failed-generation billing: docs list `failure_code`s but no explicit
  billing statement for failures — treat as unknown; no auto-retries regardless.
- `motion_prompt`, `motion_expressiveness`, `aspect_ratio`: no documented
  surcharge (priced per output second only).
- Our test estimate: 3.29 s × $0.05 = **~$0.165**.

## 3. Existing pipeline audit

- `tools/render_presenter.py` — Developer API client: uploads audio to
  `/v3/assets`, submits `type=avatar` to `/v3/videos`, polls, downloads.
  Default engine (omitted) = Avatar IV. Now supports optional
  `avatar_engine` + `motion_prompt` + `motion_expressiveness` in the jobs
  spec, an allowlisted engine gate (`config/ui-heygen-policy.json`),
  wallet-verification gate, and per-run cost estimate.
- `tools/verify_presenter.py` — new `--require-engine` flag checks the
  look's `supported_api_engines`; fails closed if the field is absent.
- `tools/gen_tts.py` — TTS unchanged (engine-independent).
- Config: `config/ui-heygen-policy.json` (rule + rate card + limits),
  `config/ui-presenter-lock.json` (founder look + Brock voice — unchanged).
- Permanent rule: `docs/UI-HEYGEN-API-ONLY.md`.

## 4. Controlled test (staged, not yet submitted)

- Jobs file: `production/prosperityai/v1/avatar6_test_jobs.json`
- Look: Sebastian Office 11 `f00a2f4b726e4808866d4740ede6e1e0` (locked founder)
- Audio: existing `audio/n01.wav` — "Today, we're announcing the end of poverty." (3.29 s)
- Engine: `heygen-avatar-6-turbo`, 1080p, 9:16
- Motion prompt: keynote-confident direction (in jobs file, ~380 chars)
- Output: `presenter_avatar6/vp1_a6t.mp4` (v1 `presenter/` untouched)
- Estimated: ~$0.165 at advertised rate; actual = wallet delta.

### Pre-submit checklist (all must pass)

1. `HEYGEN_API_KEY` present — **BLOCKED: not in environment**
2. API wallet readable + numeric — pending (needs key)
3. `verify_presenter.py --look-id f00a2f4b… --character founder --require-engine heygen-avatar-6-turbo` → PREFLIGHT PASS — pending (needs key)
4. One render only; no retries without authorization.

## 5. Creative evaluation (expected, pending visual test)

- **Founder (keynote):** Avatar 6's motion_prompt + `motion_expressiveness`
  directly addresses the flat delivery of Avatar IV — controlled gestures,
  open hands, stage presence. If lip-sync and identity hold, this is the
  stronger founder engine for future ProsperityAI spots.
- **Steve (HumanGPT):** likely *less* useful — Steve's gag is restrained
  awkwardness; Avatar 4's flatter motion may already be optimal, and
  `motion_expressiveness: "less"` can approximate it on 6 if needed.
- **Cost parity at 1080p:** Turbo's advertised $0.05/s ≈ Avatar IV photo
  rate → adoption carries no obvious per-second premium (verify actual).

## 6. Blockers / unresolved

1. **`HEYGEN_API_KEY` absent from the environment.** Required for wallet
   verification, the `--require-engine` look check, and the paid test.
   Action needed: set it (env var or local `.env`) — it is never printed.
2. Founder look `supported_api_engines` unverified (MCP doesn't expose it).
3. Actual API rate for Avatar 6 Turbo unconfirmed until a billed render.
4. 2K availability on this account unconfirmed.
5. Failed-generation billing behavior undocumented.
