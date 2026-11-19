# UI-HEYGEN-API-ONLY — permanent production rule

All Unnecessary Intelligence HeyGen media generation must occur through the
authorized **HeyGen Developer API** integration:

- Endpoint base: `https://api.heygen.com` (v3)
- Auth: `X-Api-Key: $HEYGEN_API_KEY` (environment only — never logged,
  printed, or committed)
- Billing: the Developer API **pay-as-you-go USD wallet**, observable as
  `data.wallet.remaining_balance` on `GET /v3/users/me`

## Prohibited

1. HeyGen web-app subscription credits
2. HeyGen Studio credits
3. HeyGen account video-generation credits outside Developer API billing
4. HeyGen Playground generation for production content
5. Browser automation against the HeyGen website
6. Switching to subscription-based generation
7. Purchasing credits or changing plans from tooling
8. Non-API fallback when an API request fails

## Technical enforcement

- `tools/render_presenter.py` reads the numeric API wallet balance before
  every paid submit and **stops** if it cannot be read (unverifiable
  billing source). There is no automatic billing fallback.
- Engine selection is allowlisted in `config/ui-heygen-policy.json`
  (`engines`). Unknown engine strings are rejected; Avatar IV remains the
  default when `avatar_engine` is omitted.
- Estimated cost (policy rate × measured audio seconds) is printed before
  each paid submit; the wallet delta is printed after — actual cost is the
  delta, not the rate card.
- `tools/verify_presenter.py --require-engine <engine>` fails closed when
  a look's `supported_api_engines` cannot be confirmed via the API.
- Failed paid renders are never retried automatically.
- The HeyGen MCP tools in this environment authenticate over OAuth to the
  same account but meter through the subscription/plan balance — they are
  approved for **read-only discovery** (looks, voices, assets) and are
  **not** an approved billing path for generation. Paid generation goes
  through `tools/render_presenter.py` / `tools/gen_tts.py` only.

## Known limitation

The API exposes the wallet balance but not a per-request billing-source
attestation. "Developer API billing" is therefore verified as: the request
authenticates with `HEYGEN_API_KEY`, hits `api.heygen.com`, and the
pre-paid USD wallet delta matches the metered charge. Any endpoint whose
cost does not move this wallet is out of policy — stop and report.
