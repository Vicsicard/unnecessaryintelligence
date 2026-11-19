#!/usr/bin/env python3
"""Headless-Edge HTML -> PNG plate renderer for UI graphics.

Derived from the MALB/CHM HTML-plate pattern (`gen_state_html.py` +
Edge `--screenshot`; see docs/PROVENANCE.md). Genericized: any HTML file,
any output size, manifest-driven state batches via a jobs JSON.

Usage:
    python render_html.py plate.html out.png [--w 1080 --h 1920]
    python render_html.py --jobs render_jobs.json

render_jobs.json: [{"in": "brand/templates/claim.html", "out": "g/claim_0.png",
                     "w": 1080, "h": 1920, "params": {"text": "..."}}]
"params" are URL query args appended to the file URL — templates read them
via location.search, so one HTML file renders every state.
"""
import json, os, subprocess, sys, urllib.parse

EDGE_CANDIDATES = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
]
FALLBACKS = ["msedge", "chrome", "chromium", "google-chrome"]


def find_browser():
    env = os.environ.get("UI_BROWSER_EXE")
    if env and os.path.exists(env):
        return env
    for p in EDGE_CANDIDATES:
        if os.path.exists(p):
            return p
    for exe in FALLBACKS:
        w = subprocess.run(["where", exe] if os.name == "nt" else ["which", exe],
                           capture_output=True, text=True)
        if w.returncode == 0:
            return w.stdout.splitlines()[0].strip()
    return None


def render(browser, src, out, w, h, params=None, transparent=False):
    src = os.path.abspath(src)
    url = "file:///" + src.replace("\\", "/")
    if params:
        url += "?" + urllib.parse.urlencode(params)
    os.makedirs(os.path.dirname(os.path.abspath(out)) or ".", exist_ok=True)
    cmd = [browser, "--headless=new", "--disable-gpu", "--hide-scrollbars",
           f"--screenshot={os.path.abspath(out)}", f"--window-size={w},{h}",
           "--virtual-time-budget=2000"]
    if transparent:
        cmd.append("--default-background-color=00000000")
    cmd.append(url)
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    if not os.path.exists(out):
        raise SystemExit(f"FATAL: screenshot failed {src}\n{r.stderr[-400:]}")
    return out


def main():
    args = sys.argv[1:]
    browser = find_browser()
    if not browser:
        raise SystemExit("FATAL: no headless browser found (set UI_BROWSER_EXE)")
    if "--jobs" in args:
        spec = json.load(open(args[args.index("--jobs") + 1], encoding="utf-8"))
        for j in spec:
            print(render(browser, j["in"], j["out"],
                         j.get("w", 1080), j.get("h", 1920), j.get("params"),
                         j.get("transparent", False)))
        return
    if len(args) < 2:
        print(__doc__); sys.exit(1)
    src, out = args[0], args[1]
    w = int(args[args.index("--w") + 1]) if "--w" in args else 1080
    h = int(args[args.index("--h") + 1]) if "--h" in args else 1920
    print(render(browser, src, out, w, h))


if __name__ == "__main__":
    main()
