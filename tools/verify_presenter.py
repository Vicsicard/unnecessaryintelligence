#!/usr/bin/env python3
# UI presenter preflight — fail-closed gate before ANY paid HeyGen render.
# Derived from MALB `curriculum/production/tools/verify_presenter.py`
# (see docs/PROVENANCE.md). Adapted to config/ui-presenter-lock.json.
#
# Checks (in order, each is a hard stop):
#   1. lock file is configured (look + voice ids present — TBD = block)
#   2. requested look_id is in the lock's approved_look_ids
#   3. requested look is not in retired_look_ids
#   4. live verification the look exists + is renderable (requires
#      HEYGEN_API_KEY; without it the script performs offline checks
#      only and exits 2 = "live verification required before render")
#
# Usage:
#   verify_presenter.py --look-id <id>
#   verify_presenter.py --list-approved
import json, os, sys, urllib.request, urllib.error, argparse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOCK = os.path.join(ROOT, "config", "ui-presenter-lock.json")
API = "https://api.heygen.com"


def die(msg, code=1):
    print(f"PREFLIGHT FAIL: {msg}")
    sys.exit(code)


def load_lock():
    with open(LOCK, encoding="utf-8") as f:
        return json.load(f)


def api(path, key):
    req = urllib.request.Request(API + path, headers={"X-Api-Key": key})
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        return {"error": e.code}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--look-id")
    p.add_argument("--voice-id", help="narration voice_id under test — must equal the locked UI voice id")
    p.add_argument("--list-approved", action="store_true")
    args = p.parse_args()

    lock = load_lock()
    pres = lock.get("presenter") or {}
    approved = pres.get("approved_look_ids") or {}
    names = pres.get("approved_look_names") or {}

    if args.list_approved:
        if not approved:
            print("UI presenter lock is NOT CONFIGURED — no approved looks yet.")
            print(f"  set group/look ids in {os.path.relpath(LOCK)}")
            sys.exit(3)
        print(f"locked group: {pres.get('group_id')} ({pres.get('group_name')})")
        for k, v in approved.items():
            print(f"  {k}: {v}  ({names.get(k, '?')})")
        return

    if not approved:
        die("UI presenter lock is NOT CONFIGURED — no approved looks. "
            "Choose the Steve avatar first (create_photo_avatar / "
            "create_prompt_avatar / stock look), record it in "
            "config/ui-presenter-lock.json.")

    voice = (lock.get("voice") or {}).get("voice_id")
    if args.voice_id:
        if not voice:
            die("voice lock NOT CONFIGURED — record the UI voice id first")
        if args.voice_id != voice:
            die(f"voice_id {args.voice_id} is not the locked UI voice {voice}")

    if not args.look_id:
        die("--look-id required")

    retired = pres.get("retired_look_ids") or {}
    if args.look_id in retired.values():
        die(f"look {args.look_id} is a RETIRED id — never submit")
    if args.look_id not in approved.values():
        die(f"look {args.look_id} is not in approved_look_ids")

    key = os.environ.get("HEYGEN_API_KEY")
    if not key:
        print(f"OFFLINE PASS: {args.look_id} — approved look, group {pres.get('group_id')}")
        print("LIVE VERIFICATION REQUIRED before render: run get_avatar_look via MCP or set HEYGEN_API_KEY")
        sys.exit(2)

    look = api(f"/v3/avatars/looks/{args.look_id}", key)
    if look.get("error"):
        die(f"look {args.look_id} not renderable: {look}")
    data = look.get("data", look)
    if pres.get("group_id") and data.get("group_id") != pres["group_id"]:
        die(f"look belongs to group {data.get('group_id')} — expected locked group {pres['group_id']}")
    if data.get("status") != "completed":
        die(f"look status {data.get('status')} — not renderable")
    print(f"PREFLIGHT PASS: {data.get('name')} ({args.look_id}) — group verified, status completed")


if __name__ == "__main__":
    main()
