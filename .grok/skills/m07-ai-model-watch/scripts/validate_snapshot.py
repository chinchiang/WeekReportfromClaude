#!/usr/bin/env python3
"""Validate Module 07 latest-snapshot.yaml against the skill contract.

Usage:
    python3 validate_snapshot.py path/to/latest-snapshot.yaml
Exit 0 on pass, 1 on failure.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

EVIDENCE = {"證實", "廠商主張", "第三方評論", "未證實"}
ID_RE = re.compile(r"^[a-z0-9][a-z0-9-]{0,62}[a-z0-9]$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
PREFIXES = ("model-", "security-", "enterprise-", "reg-")


def parse_simple_yaml(text: str) -> dict:
    """Minimal parser for the snapshot schema only."""
    lines = [ln.rstrip() for ln in text.splitlines() if ln.strip() and not ln.strip().startswith("#")]
    data: dict = {"targets": []}
    current = None
    for ln in lines:
        if ln.startswith("module:"):
            data["module"] = ln.split(":", 1)[1].strip()
        elif ln.startswith("period_end:"):
            data["period_end"] = ln.split(":", 1)[1].strip()
        elif ln.startswith("targets:"):
            continue
        elif ln.startswith("  - id:") or ln.startswith("- id:"):
            current = {"id": ln.split(":", 1)[1].strip()}
            data["targets"].append(current)
        elif current is not None and ":" in ln:
            key, val = ln.strip().split(":", 1)
            current[key.strip()] = val.strip()
    return data


def validate(path: Path) -> list[str]:
    errors = []
    text = path.read_text(encoding="utf-8")
    data = parse_simple_yaml(text)
    if str(data.get("module", "")).strip().strip("\"'") != "07":
        errors.append("module must be 07")
    pe = str(data.get("period_end", ""))
    if not DATE_RE.match(pe):
        errors.append(f"period_end not YYYY-MM-DD: {pe!r}")
    targets = data.get("targets") or []
    if not targets:
        errors.append("targets is empty")
    ids = []
    for i, t in enumerate(targets):
        tid = t.get("id", "")
        ids.append(tid)
        if not ID_RE.match(tid):
            errors.append(f"targets[{i}].id invalid: {tid!r}")
        elif not any(tid.startswith(p) for p in PREFIXES):
            errors.append(f"targets[{i}].id missing prefix model-|security-|enterprise-|reg-: {tid}")
        if not t.get("state"):
            errors.append(f"targets[{i}] ({tid}) missing state")
        ev = t.get("evidence", "")
        if ev not in EVIDENCE:
            errors.append(f"targets[{i}] ({tid}) evidence not in {sorted(EVIDENCE)}: {ev!r}")
        sd = t.get("source_date", "")
        if not DATE_RE.match(sd):
            errors.append(f"targets[{i}] ({tid}) source_date not YYYY-MM-DD: {sd!r}")
    if len(ids) != len(set(ids)):
        errors.append("duplicate target ids")
    return errors


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: validate_snapshot.py <latest-snapshot.yaml>", file=sys.stderr)
        return 2
    path = Path(sys.argv[1])
    if not path.is_file():
        print(f"not a file: {path}", file=sys.stderr)
        return 2
    errors = validate(path)
    if errors:
        print("FAIL")
        for e in errors:
            print(f" - {e}")
        return 1
    print("PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
