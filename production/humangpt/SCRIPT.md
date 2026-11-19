# HumanGPT — 20s satirical commercial — script v1

**Concept:** a completely dead-serious corporate tech ad. Glossy voiceover,
confident feature claims, minimal light plates. The reveal is the last line
+ endcard: the "AI" is Steve, an ordinary employee.

**Tagline:** *"The future of artificial intelligence is Steve."*

## Beats (≈46 spoken words → ~18s narration + holds ≈ 20–21s)

| beat | sec | visual | line |
|---|---|---|---|
| s00 | 0.0–2.2 | title plate "HumanGPT" (light, corporate) | — (music sting) |
| n01 | ~2.5–7.5 | Steve, direct to camera (presenter) | "Meet HumanGPT — the most advanced productivity intelligence ever deployed." |
| n02 | ~7.8–11.8 | claim plate 1→2, word-timed | "It writes your emails. It sits in your meetings." |
| n03 | ~12.1–17.1 | claim plate 3, word-timed | "It remembers every password — and only asks for vacation twice a year." |
| n04 | ~17.4–20.6 | Steve again, tiny shrug/wave (presenter) | "HumanGPT. The future of artificial intelligence is Steve." |
| s05 | ~20.6–23.0 | endcard: wordmark + tagline + brand | — (music tail) |

## Punchline rule
The ad must read 100% sincere until ~17s. No wink, no comedy voice — the
corporate-ad sincerity *is* the joke. Voice direction: glossy tech-ad
deadpan (think keynote voiceover), not a "wacky ad voice."

## Timing
`pacing.json` holds provisional beats; after `gen_tts.py` runs, replace
with measured wav durations + ~0.4s breaths. Total target 20–23s — inside
the 15–30s spec.

## Steve look direction
Ordinary corporate employee: business-casual, friendly, unremarkable —
NOT a futuristic "AI spokesperson." Stock HeyGen business-casual look or a
prompt-generated "office worker, 30s, button-down, neutral office bg."
The ordinariness lands the joke.
