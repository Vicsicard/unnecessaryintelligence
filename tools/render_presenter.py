#!/usr/bin/env python3
"""UI presenter clips via the funded HeyGen Developer API.

Derived from malb-builder-4 `start-video-a-v1/render_jonas.py` (see
docs/PROVENANCE.md). Genericized: the avatar look comes from
`config/ui-presenter-lock.json` (or `--look-id`), and jobs come from a
`presenter_jobs.json` in the production dir instead of a hardcoded JOBS list.

Flow: POST /v3/assets uploads each narration WAV (free), then POST /v3/videos
(type=avatar, audio_asset_id, resolution + aspect_ratio), poll, download to
presenter/. Idempotent: existing clips/assets are never re-billed.
HEYGEN_API_KEY from env; never printed. Wallet balance printed before/after
each render.

Avatar engine selection (optional, per jobs file):
    "avatar_engine": "heygen-avatar-6-turbo"  — opt-in; omitted = Avatar IV
    "motion_expressiveness": "default"|"less" — engine motion control
    "motion_prompt": "<text>"                 — plain-language direction
Engines/rates live in config/ui-heygen-policy.json (ENGINES). Unknown engine
strings are REJECTED — never silently fall back to another engine or billing
source (see docs/UI-HEYGEN-API-ONLY.md). A numeric API wallet balance must be
visible via /v3/users/me before any paid submit; if it isn't readable the
billing source cannot be verified and the script stops.

Usage (from a production dir):
    python ../../tools/render_presenter.py --jobs presenter_jobs.json --out presenter
    python ../../tools/render_presenter.py --jobs presenter_jobs.json --dry-run

presenter_jobs.json:
    {"look_id": "<optional override>",
     "aspect_ratio": "9:16", "resolution": "1080p",
     "avatar_engine": "heygen-avatar-6-turbo",   # optional — default Avatar IV
     "motion_expressiveness": "default",          # optional
     "motion_prompt": "confident keynote delivery", # optional
     "jobs": [["vp1", "audio/n01.wav"], ["vp4", "audio/n04.wav"]]}
"""
import json, os, sys, time, wave
import urllib.request, urllib.error

API = "https://api.heygen.com"
POLICY = os.path.join(os.path.dirname(__file__), "..", "config",
                      "ui-heygen-policy.json")


def die(msg, code=1):
    print("STOP:", msg); sys.exit(code)


def http(method, path, key, payload=None, files=None, timeout=60):
    headers = {"X-Api-Key": key}
    data = None
    if payload is not None:
        data = json.dumps(payload).encode()
        headers["Content-Type"] = "application/json"
    if files is not None:
        # minimal multipart for the single-file upload case
        import mimetypes, uuid
        boundary = uuid.uuid4().hex
        parts = []
        for name, (fname, blob, ctype) in files.items():
            parts.append(
                f'--{boundary}\r\nContent-Disposition: form-data; name="{name}";'
                f' filename="{fname}"\r\nContent-Type: {ctype}\r\n\r\n'.encode())
            parts.append(blob); parts.append(b"\r\n")
        parts.append(f"--{boundary}--\r\n".encode())
        data = b"".join(parts)
        headers["Content-Type"] = f"multipart/form-data; boundary={boundary}"
    r = urllib.request.Request(API + path, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(r, timeout=timeout) as x:
            body = x.read()
            return x.status, json.loads(body) if body else {}
    except urllib.error.HTTPError as e:
        return e.code, {"_http_error": e.code, "_body": e.read().decode("utf-8", "replace")[:500]}
    except Exception as e:
        return None, {"_exception": repr(e)}


def wallet(key):
    st, me = http("GET", "/v3/users/me", key, timeout=20)
    if st != 200:
        return None
    return (me.get("data", {}).get("wallet") or {}).get("remaining_balance")


def policy():
    """UI-HEYGEN-API-ONLY enforcement: allowed engines + rate card (USD/sec
    of output). Absent policy = fail closed, no paid submits."""
    try:
        with open(POLICY, encoding="utf-8") as f:
            return json.load(f)
    except OSError:
        die(f"missing {POLICY} — billing policy is mandatory before paid renders")


def wav_seconds(path):
    try:
        with wave.open(path, "rb") as w:
            return w.getnframes() / w.getframerate()
    except Exception:
        return None


def check_engine(spec, key):
    """Validate the requested engine against policy + this look's eligibility.
    Returns (engine_type or None-for-default-IV, payload_fragment, est_rate)."""
    eng = spec.get("avatar_engine")
    if not eng:
        return None, {}, None
    p = policy()
    allowed = (p.get("engines") or {})
    if eng not in allowed:
        die(f"engine '{eng}' not in ui-heygen-policy.json engines {list(allowed)} "
            "— refusing to submit (no silent engine substitution)")
    rate = allowed[eng].get("usd_per_second")
    frag = {"engine": {"type": eng}}
    if spec.get("motion_expressiveness"):
        if spec["motion_expressiveness"] not in ("default", "less"):
            die(f"motion_expressiveness '{spec['motion_expressiveness']}' invalid")
        frag["engine"]["motion_expressiveness"] = spec["motion_expressiveness"]
    if spec.get("motion_prompt"):
        frag["motion_prompt"] = spec["motion_prompt"]
    return eng, frag, rate


def locked_look():
    lock_p = os.path.join(os.path.dirname(__file__), "..", "config",
                          "ui-presenter-lock.json")
    try:
        with open(lock_p, encoding="utf-8") as f:
            pres = json.load(f).get("presenter") or {}
            ids = list((pres.get("approved_look_ids") or {}).values())
            return ids[0] if ids else None
    except OSError:
        return None


def upload(key, path):
    with open(path, "rb") as f:
        blob = f.read()
    st, d = http("POST", "/v3/assets", key,
                 files={"file": (os.path.basename(path), blob, "audio/wav")},
                 timeout=120)
    if st not in (200, 201):
        die(f"asset upload {path} -> {st}: {d}")
    d = d.get("data", d)
    return d.get("asset_id") or d.get("id")


def download(url, out):
    with urllib.request.urlopen(url, timeout=300) as x, open(out, "wb") as f:
        while True:
            chunk = x.read(1 << 20)
            if not chunk:
                break
            f.write(chunk)


def main():
    args = sys.argv[1:]
    if "--jobs" not in args:
        die("--jobs <presenter_jobs.json> required")
    jobs_p = args[args.index("--jobs") + 1]
    out_dir = args[args.index("--out") + 1] if "--out" in args else "presenter"
    dry = "--dry-run" in args

    spec = json.load(open(jobs_p, encoding="utf-8"))
    look = spec.get("look_id") or locked_look()
    aspect = spec.get("aspect_ratio", "9:16")
    res = spec.get("resolution", "1080p")
    jobs = spec["jobs"]
    if not look and not dry:
        die("no look_id — set it in presenter_jobs.json or config/ui-presenter-lock.json")

    if dry:
        print(f"DRY RUN — {len(jobs)} presenter renders, look {look or 'NOT CONFIGURED (blocker #1)'}, {aspect} {res}")
        if spec.get("avatar_engine"):
            print(f"  engine: {spec['avatar_engine']} (default is Avatar IV when omitted)")
        for tag, wav in jobs:
            print(f"  {tag}: {wav} ({'exists' if os.path.exists(wav) else 'MISSING'})")
        print("no API calls made")
        return

    key = os.environ.get("HEYGEN_API_KEY") or die("HEYGEN_API_KEY absent", 2)

    # UI-HEYGEN-API-ONLY gate: paid submits require a readable numeric API
    # wallet balance — no verifiable billing source, no paid generation.
    bal = wallet(key)
    if not isinstance(bal, (int, float)):
        die("API wallet balance unreadable — cannot verify Developer API "
            "billing source (subscription/Studio credits are NOT permitted). "
            "Stop per docs/UI-HEYGEN-API-ONLY.md.")
    eng, eng_frag, rate = check_engine(spec, key)
    if eng and rate:
        secs = [wav_seconds(w) or 0 for _, w in jobs if not os.path.exists(
            os.path.join(out_dir, f"{_}.mp4"))]
        print(f"ENGINE {eng} @ ${rate}/s — est. cost ${sum(secs)*rate:.3f} "
              f"for {sum(secs):.1f}s of new audio | wallet ${bal}")

    os.makedirs(out_dir, exist_ok=True)
    registry_p = os.path.join(out_dir, "_jobs.json")
    reg = json.load(open(registry_p)) if os.path.exists(registry_p) else {}

    for tag, wav in jobs:
        out = os.path.join(out_dir, f"{tag}.mp4")
        if os.path.exists(out):
            print(f"{tag}: clip exists — SKIP (no re-billing)"); continue
        if not os.path.exists(wav):
            die(f"{tag}: missing audio {wav} — run gen_tts.py first")
        job = reg.get(tag, {})
        if not job.get("asset_id"):
            job["asset_id"] = upload(key, wav)
            print(f"{tag}: uploaded {wav} -> asset {job['asset_id']}")
        if not job.get("video_id"):
            print(f"{tag}: wallet before render: {wallet(key)}")
            st, d = http("POST", "/v3/videos", key,
                         payload={"type": "avatar", "avatar_id": look,
                                  "audio_asset_id": job["asset_id"],
                                  "aspect_ratio": aspect, "resolution": res,
                                  "title": f"UI presenter {tag}",
                                  **eng_frag})
            if st not in (200, 201):
                die(f"render {tag} -> {st}: {d}")
            d = d.get("data", d)
            job["video_id"] = d.get("video_id")
            if not job["video_id"]:
                die(f"render {tag}: no video_id in {json.dumps(d)[:300]}")
            reg[tag] = job
            json.dump(reg, open(registry_p, "w"), indent=1)
            print(f"{tag}: render {job['video_id']} submitted | wallet after: {wallet(key)}")
        reg[tag] = job
        json.dump(reg, open(registry_p, "w"), indent=1)

    for tag, _ in jobs:
        out = os.path.join(out_dir, f"{tag}.mp4")
        if os.path.exists(out):
            continue
        vid = reg[tag]["video_id"]
        url = None
        for _ in range(120):
            st, d = http("GET", f"/v3/videos/{vid}", key, timeout=30)
            d = d.get("data", d)
            status = d.get("status")
            if status == "completed":
                url = d.get("video_url") or d.get("url"); break
            if status in ("failed", "error"):
                die(f"render {tag} {vid} failed: {json.dumps(d)[:400]} — no retry without authorization")
            time.sleep(10)
        if not url:
            die(f"render {tag} {vid} timed out")
        download(url, out)
        print(f"{tag}: downloaded -> {out} | wallet now: {wallet(key)}")


if __name__ == "__main__":
    main()
