#!/usr/bin/env python3
"""Decide which week the compliance weekly should cover, and refuse to guess.

The report covers the week that just ended (last Monday to yesterday, a Sunday).
This script exists because the wrong week has been produced before.

    python3 scripts/period.py            # human-readable brief, exit 0 when OK
    python3 scripts/period.py --json     # machine-readable brief
    python3 scripts/period.py --today 2026-09-14
    python3 scripts/period.py --allow-existing   # OK to update an existing file for that week

Exit codes:
    0  produce/update reports/<id>.json as printed
    2  yesterday is not a Sunday (run fired on the wrong day) -> stop and report
    3  that week's file already exists and is a complete report -> stop and report
    4  reports/index.json does not chain to this week -> stop and report
"""
import argparse
import datetime as dt
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOPICS = ["eu-ai-act", "eu-cra", "nis2", "cmmc", "iso27000", "iso42001", "tisax", "iec62443", "incidents"]


def week_id(d: dt.date) -> str:
    y, w, _ = d.isocalendar()
    return f"{y}-W{w:02d}"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--today", help="override today's date (YYYY-MM-DD), for testing")
    ap.add_argument("--allow-existing", action="store_true", help="do not fail when the week's file already exists")
    ap.add_argument("--json", action="store_true", help="print a JSON brief")
    args = ap.parse_args()

    today = dt.date.fromisoformat(args.today) if args.today else dt.date.today()
    yesterday = today - dt.timedelta(days=1)
    problems = []
    code = 0

    if yesterday.weekday() != 6:
        problems.append(f"昨天 {yesterday} 是{'一二三四五六日'[yesterday.weekday()]}，不是週日：本次執行不在週一，停下來回報，不得產出當週期別。")
        code = 2

    wid = week_id(yesterday)
    monday = yesterday - dt.timedelta(days=6)
    prev_id = week_id(yesterday - dt.timedelta(days=7))
    path = ROOT / "reports" / f"{wid}.json"

    idx_path = ROOT / "reports" / "index.json"
    idx = json.loads(idx_path.read_text(encoding="utf-8")) if idx_path.exists() else []
    top = idx[0]["id"] if idx else None
    exists = path.exists()
    complete = False
    if exists:
        try:
            rep = json.loads(path.read_text(encoding="utf-8"))
            topics = [s.get("topic") for s in rep.get("sections", [])]
            complete = topics[:9] == TOPICS
        except Exception:
            complete = False

    if exists and complete and not args.allow_existing:
        problems.append(f"reports/{wid}.json 已存在且九大主題齊備：這一期已產出。要更新請加 --allow-existing，否則停下來回報。")
        code = code or 3
    if top not in (prev_id, wid):
        problems.append(f"reports/index.json 最新一期是 {top}，與本期 {wid} 連號不上（預期上一期為 {prev_id}）：停下來回報，不要自行推測。")
        code = code or 4

    brief = {
        "ok": code == 0,
        "today": today.isoformat(),
        "id": wid,
        "period": f"{monday.isoformat()} ~ {yesterday.isoformat()}",
        "periodShort": f"{monday.month:02d}/{monday.day:02d} ~ {yesterday.month:02d}/{yesterday.day:02d}",
        "publishedAt": today.isoformat(),
        "file": f"reports/{wid}.json",
        "fileExists": exists,
        "fileComplete": complete,
        "indexTop": top,
        "expectedPrevious": prev_id,
        "problems": problems,
    }
    if args.json:
        print(json.dumps(brief, ensure_ascii=False, indent=2))
    else:
        print(f"期別        {wid}")
        print(f"涵蓋期間    {brief['period']}   (index period: {brief['periodShort']})")
        print(f"publishedAt {brief['publishedAt']}")
        print(f"檔案        {brief['file']}  exists={exists} complete={complete}")
        print(f"index 最新  {top}  (預期上一期 {prev_id})")
        for p in problems:
            print("STOP:", p)
        print("OK" if code == 0 else f"EXIT {code}")
    sys.exit(code)


if __name__ == "__main__":
    main()
