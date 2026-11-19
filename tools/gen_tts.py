#!/usr/bin/env python3
"""UI narration beats via the funded HeyGen Developer API.

Derived from malb-builder-4 `start-video-a-v1/gen_tts.py` (see
docs/PROVENANCE.md). Genericized: script beats + voice come from the
production's `script.json` and `config/ui-presenter-lock.json` — nothing is
hardcoded to a brand, voice, or text.

POST /v3/models/audio/tts with `with_timestamps=true` returns word/char
timing used for caption cues and graphic-state triggers. One call per beat;
idempotent (existing wav + timing file are never re-billed).

Usage (from a production dir, e.g. production/humangpt):
    python ../../tools/gen_tts.py --script script.json --out audio
    python ../../tools/gen_tts.py --script script.json --out audio --only n01,n03
    python ../../tools/gen_tts.py --script script.json --dry-run   # plan only, zero API

HEYGEN_API_KEY comes from env; it is never printed. Wallet balance is printed
before/after each call. No call is ever made without the key present.
"""
import json, os, sys, urllib.request, urllib.error

API = "https://api.heygen.com"


def die(msg, code=1):
    print("STOP:", msg); sys.exit(code)


def req(path, key, payload=None, timeout=180):
    r = urllib.request.Request(
        API + path,
        data=json.dumps(payload).encode() if payload is not None else None,
        headers={"X-Api-Key": key, "Content-Type": "application/json"},
        method="POST" if payload is not None else "GET")
    try:
        with urllib.request.urlopen(r, timeout=timeout) as x:
            return x.status, json.loads(x.read())
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", "replace")[:500]
        return e.code, {"_http_error": e.code, "_body": body}
    except Exception as e:
        return None, {"_exception": repr(e)}


def balance(key):
    st, me = req("/v3/users/me", key)
    if st != 200:
        return None
    return (me.get("data", {}).get("wallet") or {}).get("remaining_balance")


def locked_voice():
    lock_p = os.path.join(os.path.dirname(__file__), "..", "config",
                          "ui-presenter-lock.json")
    try:
        with open(lock_p, encoding="utf-8") as f:
            return (json.load(f).get("voice") or {}).get("voice_id")
    except OSError:
        return None


def run_beat(b, text, voice, out_dir, key):
    wav_p   = os.path.join(out_dir, f"{b}.wav")
    chars_p = os.path.join(out_dir, f"{b}_chars.json")
    raw_p   = os.path.join(out_dir, f"{b}_raw.json")
    if os.path.exists(wav_p) and os.path.exists(chars_p):
        print(f"{b}: exists, skipping"); return
    b0 = balance(key)
    st, j = req("/v3/models/audio/tts", key, {
        "voice_id": voice, "text": text,
        "language": "en", "with_timestamps": True})
    if st != 200:
        die(f"{b} TTS failed: {st} {j}")
    d = j.get("data", {})
    audio_url = d.get("audio_url") or d.get("url")
    if not audio_url:
        die(f"{b}: no audio_url in response keys {list(d.keys())}")
    json.dump(d, open(raw_p, "w"))
    chars = (d.get("timestamp_info") or {}).get("original_characters") \
        or d.get("original_characters") or d.get("characters") \
        or d.get("timestamp_info")
    if not chars:
        die(f"{b}: no char timestamps in response — inspect {raw_p}")
    with urllib.request.urlopen(audio_url, timeout=180) as x:
        open(wav_p, "wb").write(x.read())
    json.dump(chars, open(chars_p, "w"))
    b1 = balance(key)
    print(f"{b}: {len(text)} chars -> {wav_p} | wallet {b0} -> {b1}")


def main():
    args = sys.argv[1:]
    if "--script" not in args:
        die("--script <path> required")
    script_p = args[args.index("--script") + 1]
    out_dir  = args[args.index("--out") + 1] if "--out" in args else "audio"
    dry      = "--dry-run" in args
    only     = set(args[args.index("--only") + 1].split(",")) if "--only" in args else None

    spec = json.load(open(script_p, encoding="utf-8"))
    beats = spec["beats"]
    order = spec.get("beat_order") or sorted(beats)
    voice = spec.get("voice_id") or locked_voice()
    if not voice and not dry:
        die("no voice_id — set it in script.json or config/ui-presenter-lock.json")

    todo = [b for b in order if b in beats and (not only or b in only)]
    if not todo:
        die(f"no beats to render; order={order} only={only}")

    if dry:
        print(f"DRY RUN — {len(todo)} beats via voice {voice or 'NOT CONFIGURED (blocker #2)'}")
        for b in todo:
            print(f"  {b}: {len(beats[b])} chars — {beats[b][:60]}")
        print("no API calls made")
        return

    key = os.environ.get("HEYGEN_API_KEY") or die(
        "HEYGEN_API_KEY not set — stop, no paid calls without wallet key", 2)
    os.makedirs(out_dir, exist_ok=True)
    for b in todo:
        run_beat(b, beats[b], voice, out_dir, key)
    print("done — wallet", balance(key))


if __name__ == "__main__":
    main()
