"""The FOCUS.md "done when" check, against the running server.

Start the server first:
  .venv/bin/uvicorn app.server:app --host 127.0.0.1 --port 8000
Then:
  .venv/bin/python scripts/done_check.py

Passes only if a 2-minute memo comes back with status 200, non-empty text,
a .txt file name, in under 60 seconds.
"""

import sys
import time
from pathlib import Path

import httpx

BASE = "http://127.0.0.1:8000"
MEMO = Path(__file__).resolve().parent.parent / "tests" / "fixtures" / "long_memo.m4a"
LIMIT_SECONDS = 60


def main() -> int:
    if not MEMO.exists():
        print(f"Missing {MEMO}. Run: bash tests/make_fixtures.sh")
        return 2
    try:
        httpx.get(BASE + "/", timeout=5).raise_for_status()
    except httpx.HTTPError:
        print(f"The server is not running at {BASE}. Start it first (see the top of this file).")
        return 2

    start = time.perf_counter()
    with MEMO.open("rb") as f:
        r = httpx.post(BASE + "/transcribe", files={"file": (MEMO.name, f)}, timeout=180)
    took = time.perf_counter() - start

    body = r.json()
    text = body.get("text", "")
    checks = {
        "status is 200": r.status_code == 200,
        "transcript is not empty": bool(text.strip()),
        "download name is long_memo.txt": body.get("filename") == "long_memo.txt",
        f"took under {LIMIT_SECONDS} s ({took:.1f} s)": took < LIMIT_SECONDS,
    }
    for name, ok in checks.items():
        print(("PASS  " if ok else "FAIL  ") + name)
    print(f"Words: {len(text.split())}")
    ok = all(checks.values())
    print("DONE-WHEN CHECK: " + ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
