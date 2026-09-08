#!/usr/bin/env python3
"""Keep index.html's CSP script-src hash in sync with its single inline <script>.

    python3 scripts/csp_hash.py --check    # exit 1 if the meta CSP hash does not match (CI)
    python3 scripts/csp_hash.py --write    # recompute and rewrite the hash in place

The page has exactly one inline <script>; the CSP allows it by SHA-256 so that any
inline handler injected through innerHTML (onerror=, javascript: ...) is blocked.
Edit the script, then run --write; forgetting to do so breaks the page, which is
why CI runs --check.
"""
import argparse
import base64
import hashlib
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGE = ROOT / "index.html"
# 只認行首的 <script> 標籤，避免被註解或文字裡的字樣誤匹配
SCRIPT_RE = re.compile(r"^<script>(.*?)^</script>", re.S | re.M)
META_RE = re.compile(r"(script-src 'sha256-)([A-Za-z0-9+/=]+|PLACEHOLDER)(')")


def compute(html: str) -> str:
    scripts = SCRIPT_RE.findall(html)
    if len(scripts) != 1:
        sys.exit(f"index.html must contain exactly one inline <script>, found {len(scripts)}")
    return base64.b64encode(hashlib.sha256(scripts[0].encode("utf-8")).digest()).decode()


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--check", action="store_true")
    g.add_argument("--write", action="store_true")
    args = ap.parse_args()

    html = PAGE.read_text(encoding="utf-8")
    want = compute(html)
    m = META_RE.search(html)
    if not m:
        sys.exit("index.html has no CSP meta with script-src 'sha256-...'")
    have = m.group(2)
    if args.check:
        if have == want:
            print(f"CSP hash OK: sha256-{want}")
            return
        sys.exit(f"CSP hash mismatch: meta has {have}, script is {want}. Run: python3 scripts/csp_hash.py --write")
    new = html[: m.start(2)] + want + html[m.end(2):]
    if new != html:
        PAGE.write_text(new, encoding="utf-8")
        print(f"CSP hash written: sha256-{want}")
    else:
        print(f"CSP hash unchanged: sha256-{want}")


if __name__ == "__main__":
    main()
