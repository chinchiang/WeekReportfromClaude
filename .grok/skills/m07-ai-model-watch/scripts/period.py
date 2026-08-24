#!/usr/bin/env python3
"""Compute Module 07 observation window in Asia/Taipei.

Observation period = previous Monday 00:00 through execution day 07:59.
ISO week id uses the Monday that starts the observation window.

Usage:
    python3 period.py              # now
    python3 period.py --date 2026-08-24
"""
from __future__ import annotations

import argparse
import json
from datetime import date, datetime, time, timedelta
from zoneinfo import ZoneInfo

TZ = ZoneInfo("Asia/Taipei")
MODULE07_PATH = "modules/07-ai-model-watch"
REPO = "chinchiang/WeekReportfromClaude"


def previous_monday(d: date) -> date:
    """Monday strictly before d if d is Monday, else the Monday of d's week."""
    if d.weekday() == 0:
        return d - timedelta(days=7)
    return d - timedelta(days=d.weekday())


def compute(exec_date: date) -> dict:
    start = previous_monday(exec_date)
    iso = start.isocalendar()
    week_id = f"{iso.year}-W{iso.week:02d}"
    return {
        "timezone": "Asia/Taipei",
        "execution_date": exec_date.isoformat(),
        "period_start": start.isoformat(),
        "period_start_local": f"{start.isoformat()}T00:00:00+08:00",
        "period_end_local": f"{exec_date.isoformat()}T07:59:00+08:00",
        "period_end": exec_date.isoformat(),
        "week_id": week_id,
        "report_filename": f"{week_id}.html",
        "report_path": f"{MODULE07_PATH}/{week_id}.html",
        "index_path": f"{MODULE07_PATH}/index.html",
        "snapshot_path": f"{MODULE07_PATH}/latest-snapshot.yaml",
        "snapshot_url": (
            f"https://raw.githubusercontent.com/{REPO}/main/"
            f"{MODULE07_PATH}/latest-snapshot.yaml"
        ),
        "commit_message": f"chore(m07): weekly AI model watch {week_id}",
        "module07_path": MODULE07_PATH,
        "repo": REPO,
    }


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--date", help="Execution date YYYY-MM-DD (default: today Taipei)")
    args = p.parse_args()
    if args.date:
        exec_date = date.fromisoformat(args.date)
    else:
        exec_date = datetime.now(TZ).date()
    print(json.dumps(compute(exec_date), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
