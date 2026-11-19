"""meta_provider.py — Meta Model API provider for UI production (dev.meta.ai).

Official endpoints only. Base https://api.meta.ai/v1, Bearer MODEL_API_KEY,
OpenAI-compatible Responses API. Stateless by default (store:false) — no
server-side conversation persistence.

Capabilities (all individually gated):
  models      — GET /v1/models (read-only account/model verification, free)
  qc          — video understanding via Muse Spark/Ember (PAID per token)
  image       — Muse Image generation (PAID $0.01/image)
  sam         — SAM 3.1 segmentation (PAID per image/frame)

PAID calls require --paid on the command line. There is no video-GENERATION
model on this API — see docs/META-AI-INVESTIGATION.md. Understanding !=
generation; never represent QC output as proof of correctness.

Credentials: MODEL_API_KEY env var (or .env via --env file). Never logged.
"""
import os, sys, json, base64, argparse, mimetypes, urllib.request, urllib.error, uuid

BASE = "https://api.meta.ai/v1"
DEFAULT_VQC_MODEL = "muse-ember-1.0"     # cheapest reasoning model; spark-1.3 for harder QC
IMG_MODEL = "muse-image-1.0"
SAM_MODEL = "sam-3.1"


def _key():
    return os.environ.get("MODEL_API_KEY") or os.environ.get("META_MODEL_API_KEY")


def _req(method, path, payload=None, files=None, fields=None, timeout=300):
    url = BASE + path
    headers = {"Authorization": f"Bearer {_key()}"}
    if files:
        boundary = "----ui" + uuid.uuid4().hex
        body = b""
        for k, v in (fields or {}).items():
            body += f"--{boundary}\r\nContent-Disposition: form-data; name=\"{k}\"\r\n\r\n{v}\r\n".encode()
        for name, (fname, data, ctype) in files.items():
            body += (f"--{boundary}\r\nContent-Disposition: form-data; name=\"{name}\"; "
                     f"filename=\"{fname}\"\r\nContent-Type: {ctype}\r\n\r\n").encode() + data + b"\r\n"
        body += f"--{boundary}--\r\n".encode()
        headers["Content-Type"] = f"multipart/form-data; boundary={boundary}"
    else:
        body = json.dumps(payload).encode() if payload is not None else None
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, json.loads(r.read() or b"{}")
    except urllib.error.HTTPError as e:
        detail = e.read().decode(errors="replace")[:500]
        raise RuntimeError(f"Meta API {e.code} {method} {path}: {detail}") from None


def need_key():
    if not _key():
        print("FATAL: MODEL_API_KEY not set — add it to .env or the environment. "
              "Meta features are OFF (local pipeline unaffected).")
        sys.exit(3)


def need_paid(args, est):
    if not args.paid:
        print(f"REFUSED (unpaid-gate): {est}. Re-run with --paid to authorize this spend.")
        sys.exit(4)


def out_text(resp):
    for item in resp.get("output", []):
        if item.get("type") == "message":
            for c in item.get("content", []):
                if c.get("type") == "output_text":
                    return c.get("text", "")
    return ""


def cmd_models(_a):
    need_key()
    _s, r = _req("GET", "/models")
    for m in r.get("data", []):
        print(" ", m.get("id"))
    print(f"{len(r.get('data', []))} model(s) visible to this key")


def _upload_file(path):
    data = open(path, "rb").read()
    ctype = mimetypes.guess_type(path)[0] or "application/octet-stream"
    _s, r = _req("POST", "/files", files={"file": (os.path.basename(path), data, ctype)},
                 fields={"purpose": "user_data"})
    return r.get("id")


def cmd_qc(a):
    need_key(); need_paid(a, f"video-QC call on {a.model} (billed per token)")
    brief = open(a.brief, encoding="utf-8").read() if a.brief else "(no brief supplied)"
    fid = _upload_file(a.video)
    print(f"uploaded {os.path.basename(a.video)} -> {fid}")
    prompt = (
        "You are a QC reviewer for a satirical product commercial. Compare this video "
        "against its approved episode brief and report findings as STRICT JSON only:\n"
        "{\"summary\": str, \"dialogue_present\": bool|null, "
        "\"pricing\": {\"expected\": str|null, \"observed\": str|null, \"correct\": bool|null}, "
        "\"punchline_present\": bool|null, \"continuity_flags\": [str], "
        "\"timing_notes\": [str], \"confidence\": \"low|medium|high\"}\n"
        "Use null when unsure — never guess. You cannot verify lip sync, exact audio wording, "
        "or brand assets; note those as unverifiable rather than passing them.\n\nBRIEF:\n" + brief)
    _s, r = _req("POST", "/responses", {
        "model": a.model, "store": False,
        "input": [{"type": "message", "role": "user", "content": [
            {"type": "input_text", "text": prompt},
            {"type": "input_video", "file_id": fid}]}]})
    report = {"tool": "meta_video_qc", "model": a.model,
              "usage": r.get("usage"), "file_id": fid,
              "assessment_raw": out_text(r),
              "disclaimer": "Model assessment — NOT definitive proof of audio/visual correctness. "
                            "Human review remains the approval gate."}
    raw = report["assessment_raw"]
    try:
        report["assessment"] = json.loads(raw[raw.index("{"):raw.rindex("}") + 1])
    except Exception:
        report["assessment"] = None
    outp = a.out or (os.path.splitext(a.video)[0] + ".qc_report.json")
    json.dump(report, open(outp, "w"), indent=2)
    print(f"QC report -> {outp}  usage={r.get('usage')}")
    if report["assessment"]:
        print(json.dumps(report["assessment"], indent=2)[:800])


def cmd_image(a):
    need_key(); need_paid(a, f"Muse Image generation x{a.n} (~$0.01/image)")
    payload = {"model": IMG_MODEL, "prompt": a.prompt, "n": a.n,
               "size": a.size, "output_format": "png"}
    _s, r = _req("POST", "/images/generations", payload)
    meta = {"model": IMG_MODEL, "prompt": a.prompt, "usage": r.get("usage"),
            "billed_per_image_usd": 0.01, "files": []}
    for i, d in enumerate(r.get("data", [])):
        fp = os.path.join(a.out, f"muse_{i}.png")
        open(fp, "wb").write(base64.b64decode(d["b64_json"]))
        meta["files"].append(fp); print("saved", fp)
    json.dump(meta, open(os.path.join(a.out, "muse_gen.json"), "w"), indent=2)


def cmd_sam(a):
    need_key(); need_paid(a, f"SAM 3.1 segmentation on {a.media} (billed per image/frame)")
    fid = _upload_file(a.media)
    kind = "input_video" if a.media.lower().endswith((".mp4", ".mov")) else "input_image"
    _s, r = _req("POST", "/responses", {
        "model": SAM_MODEL, "store": False,
        "input": [{"type": "message", "role": "user", "content": [
            {"type": "input_text", "text": a.noun},
            {"type": kind, "file_id": fid}]}]})
    outp = a.out or (os.path.splitext(a.media)[0] + ".sam.txt")
    open(outp, "w").write(out_text(r))
    print(f"SAM masks/boxes -> {outp}  usage={r.get('usage')}")


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name, fn in (("models", cmd_models),):
        p = sub.add_parser(name); p.set_defaults(fn=fn); p.add_argument("--paid", action="store_true")
    p = sub.add_parser("qc"); p.set_defaults(fn=cmd_qc)
    p.add_argument("video"); p.add_argument("--brief"); p.add_argument("--out")
    p.add_argument("--model", default=DEFAULT_VQC_MODEL)
    p.add_argument("--paid", action="store_true")
    p = sub.add_parser("image"); p.set_defaults(fn=cmd_image)
    p.add_argument("prompt"); p.add_argument("--out", default="."); p.add_argument("--n", type=int, default=1)
    p.add_argument("--size", default="1024x1792")
    p.add_argument("--paid", action="store_true")
    p = sub.add_parser("sam"); p.set_defaults(fn=cmd_sam)
    p.add_argument("media"); p.add_argument("noun"); p.add_argument("--out")
    p.add_argument("--paid", action="store_true")
    a = ap.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
