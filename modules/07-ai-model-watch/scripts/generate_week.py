#!/usr/bin/env python3
"""模組 07 週報工具。

產出由 Claude Routine 每週一觸發的雲端 session 執行（見 prompts/routine.md）：
該 session 自己做四軌檢索、自己寫出當期 JSON，再用本腳本驗證與寫檔。
本腳本因此不再呼叫 Anthropic API，也不需要 ANTHROPIC_API_KEY。

    python3 scripts/generate_week.py --print-brief          # 印出本期作業指示（含期別與上期快照）
    python3 scripts/generate_week.py --ingest week.json     # 驗證後寫入當期檔案、索引與快照
    python3 scripts/generate_week.py --ingest week.json --dry-run   # 只驗證，不寫檔
    python3 scripts/generate_week.py --validate-only        # 驗現有檔案、保留期與索引一致性
    python3 scripts/generate_week.py --rebuild-index        # 從期別檔案重建 archive-index.json

設計原則：
  * 產出檔案永不覆寫既有期別 —— 保留期內的資料是唯讀的。
  * snapshot.yaml 只在當期 JSON 寫入成功後才更新，避免拿本期跟本期比。
  * 每期 snapshot 另存一份 data/snapshots/YYYY-Www.yaml，讓一年後可回溯
    「當時的基準長什麼樣」，而不只有最新一份。
  * 期別、觀測期間、上期快照一律由本腳本計算與注入，不由執行者自行判斷 ——
    換成 Routine 執行之後，這是「不得寫死日期」這條規則唯一的機械保障。
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TAIPEI = timezone(timedelta(hours=8))

RETENTION_MIN_MONTHS = 12

EVIDENCE = {"verified", "vendor", "thirdparty", "unverified"}
PRIORITY = {"P0", "P1", "P2", "P3"}
TRACK_STATUS = {"changed", "unchanged", "baseline", "failed"}
TRACKS = ("A", "B", "C", "D")


# --------------------------------------------------------------------------- #
# 期別與路徑

def iso_week(now: datetime) -> tuple[str, str, str]:
    """回傳 (week_id, period_start, period_end)，以 Asia/Taipei 為準。"""
    year, week, _ = now.isocalendar()
    monday = now - timedelta(days=now.isoweekday() - 1)
    start = monday - timedelta(days=7)
    return f"{year}-W{week:02d}", start.strftime("%Y-%m-%d"), now.strftime("%Y-%m-%d")


def week_path(week_id: str) -> Path:
    return ROOT / "data" / "weeks" / week_id.split("-")[0] / f"{week_id}.json"


# --------------------------------------------------------------------------- #
# 驗證 —— schema 不合就讓 CI 紅燈，不要讓壞資料進入保留期

def validate(doc: dict) -> list[str]:
    errs: list[str] = []
    add = errs.append

    for field in ("module", "week", "period", "mode", "exec_summary", "tracks", "entries"):
        if field not in doc:
            add(f"缺少必填欄位: {field}")
    if errs:
        return errs

    if doc["mode"] not in ("baseline", "delta"):
        add(f"mode 值不合法: {doc['mode']}")
    if not isinstance(doc["exec_summary"], str):
        add(f"exec_summary 型別錯誤: {type(doc['exec_summary']).__name__}，應為字串")
    elif len(doc["exec_summary"]) > 700:
        add(f"exec_summary 過長 ({len(doc['exec_summary'])} 字)，規格為 400 字以內")

    for k in TRACKS:
        t = doc["tracks"].get(k)
        if not t:
            add(f"tracks 缺少 {k} 軌")
            continue
        if t.get("status") not in TRACK_STATUS:
            add(f"{k} 軌 status 不合法: {t.get('status')}")

    for i, e in enumerate(doc["entries"]):
        tag = f"entries[{i}] ({e.get('id', '無 id')})"
        if e.get("track") not in TRACKS:
            add(f"{tag} track 不合法: {e.get('track')}")
        if e.get("evidence") not in EVIDENCE:
            add(f"{tag} evidence 不合法或缺漏: {e.get('evidence')}")
        if e.get("priority") not in PRIORITY:
            add(f"{tag} priority 不合法: {e.get('priority')}")
        # id 必填：write_all() 之後的 rebuild_archive_index() 以 e["id"] 硬索引，
        # 這裡放行等於讓 KeyError 在期別檔已落地之後才爆，而該檔已受唯讀保護。
        for f in ("id", "title", "prev_state", "curr_state", "detail"):
            if not e.get(f):
                add(f"{tag} 缺少 {f}")
        srcs = e.get("sources") or []
        if not srcs:
            add(f"{tag} 沒有任何來源")
        for j, s in enumerate(srcs):
            if s.get("tier") not in (1, 2, 3):
                add(f"{tag} 來源 tier 不合法: {s.get('tier')}")
            # 來源必須可回溯。否則「2 筆來源含 Tier 1」可以用兩個空殼滿足，
            # verified 的門檻在形式上就被繞過了。
            for f in ("org", "title", "url", "date"):
                if not str(s.get(f, "")).strip():
                    add(f"{tag} 來源[{j}] 缺少 {f}")
        # 分級紀律：單一來源不得標為已證實；已證實必須有 Tier 1
        if e.get("evidence") == "verified":
            if len(srcs) < 2:
                add(f"{tag} 標為 verified 但來源少於 2 筆")
            if not any(s.get("tier") == 1 for s in srcs):
                add(f"{tag} 標為 verified 但無 Tier 1 來源")

    # id 唯一性：重複會讓 archive-index 出現同 key 兩筆，時間軸長出兩個同名節點。
    ids = [e.get("id") for e in doc["entries"] if e.get("id")]
    dups = sorted({i for i in ids if ids.count(i) > 1})
    if dups:
        add(f"entries id 重複: {', '.join(dups)}")

    cv = doc.get("counter_views") or []
    if len(cv) < 2:
        add(f"counter_views 少於 2 則（目前 {len(cv)} 則）—— 反面觀點為必填")
    for i, c in enumerate(cv):
        tag = f"counter_views[{i}]"
        if not str(c.get("point", "")).strip():
            add(f"{tag} 缺少 point")
        src = c.get("source") or {}
        if not src:
            add(f"{tag} 沒有來源 —— 反面觀點須附來源")
            continue
        # url 不強制：內部方法論引用（如「模組 07 規格」）本來就沒有外部連結。
        for f in ("org", "title", "date"):
            if not str(src.get(f, "")).strip():
                add(f"{tag} 來源缺少 {f}")
        if src.get("tier") not in (1, 2, 3):
            add(f"{tag} 來源 tier 不合法: {src.get('tier')}")

    return errs


# --------------------------------------------------------------------------- #
# 作業指示 —— 由 Routine 的雲端 session 讀取後自行執行

def build_brief(week_id: str, start: str, end: str, snapshot: str) -> str:
    """組出本期作業指示：方法論 + 執行參數 + 上期快照 + 輸出 schema。

    期別與觀測期間由 iso_week() 算出、上期快照由檔案讀出，都不交給執行者判斷。
    prompts/module-07.md 步驟 0 要求「不得寫死日期」，這裡是它的機械保障。
    """
    spec = (ROOT / "prompts" / "module-07.md").read_text(encoding="utf-8")
    schema = (ROOT / "docs" / "SCHEMA.md").read_text(encoding="utf-8")
    return (
        f"{spec}\n\n---\n\n# 本次執行參數\n\n"
        f"- 期別 week: `{week_id}`\n"
        f"- 觀測期間: `{start}` ～ `{end}`（Asia/Taipei）\n"
        f"- 輸出檔案路徑: `{week_path(week_id).relative_to(ROOT)}`\n"
        f"- 寫入方式: 先把 JSON 存成暫存檔，再執行\n"
        f"  `python3 scripts/generate_week.py --ingest <暫存檔>`。\n"
        f"  不要自己搬檔案或改 data/index.json、data/snapshot.yaml。\n\n"
        f"# 上期快照（Delta 基準）\n\n"
        f"```yaml\n{snapshot or '（空 —— 視為首期，mode 設為 baseline）'}\n```\n\n"
        f"---\n\n# 輸出 schema\n\n{schema}\n"
    )


def current_brief() -> tuple[str, str]:
    """回傳 (week_id, 作業指示全文)。"""
    week_id, start, end = iso_week(datetime.now(TAIPEI))
    snap_file = ROOT / "data" / "snapshot.yaml"
    snapshot = snap_file.read_text(encoding="utf-8") if snap_file.exists() else ""
    return week_id, build_brief(week_id, start, end, snapshot)


# --------------------------------------------------------------------------- #
# 寫檔

def to_yaml(week_id: str, period_end: str, mode: str, targets: list[dict]) -> str:
    lines = [
        "### 模組 07 — 追蹤標的狀態快照",
        "### 此檔為下期 Delta 比對基準。由 scripts/generate_week.py 自動產出，請勿手改。",
        f'module: "07"',
        f'week: "{week_id}"',
        f'period_end: "{period_end}"',
        f"mode: {mode}",
        "",
        "targets:",
    ]
    for t in targets:
        lines.append(f'  - id: {t.get("id", "unknown")}')
        lines.append(f'    label: {t.get("label", "")}')
        lines.append(f'    state: "{str(t.get("state", "")).replace(chr(34), chr(39))}"')
        lines.append(f'    evidence: {t.get("evidence", "")}')
        lines.append(f'    source_date: "{t.get("source_date", "")}"')
    return "\n".join(lines) + "\n"


def write_all(doc: dict) -> None:
    week_id = doc["week"]
    wp = week_path(week_id)
    if wp.exists():
        sys.exit(f"{wp} 已存在。保留期內的期別檔案為唯讀，不予覆寫。")
    wp.parent.mkdir(parents=True, exist_ok=True)
    wp.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    idx_path = ROOT / "data" / "index.json"
    idx = json.loads(idx_path.read_text(encoding="utf-8"))
    idx["weeks"] = [w for w in idx["weeks"] if w["week"] != week_id]
    idx["weeks"].insert(0, {
        "week": week_id,
        "period_end": doc["period"]["end"],
        "mode": doc["mode"],
        "file": str(wp.relative_to(ROOT / "data")).replace("\\", "/"),
    })
    idx["weeks"].sort(key=lambda w: w["week"], reverse=True)
    idx_path.write_text(json.dumps(idx, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    # snapshot 最後才寫，且同時留一份當期存檔
    targets = doc.get("snapshot_targets") or []
    if targets:
        y = to_yaml(week_id, doc["period"]["end"], doc["mode"], targets)
        (ROOT / "data" / "snapshot.yaml").write_text(y, encoding="utf-8")
        (ROOT / "data" / "snapshots").mkdir(parents=True, exist_ok=True)
        (ROOT / "data" / "snapshots" / f"{week_id}.yaml").write_text(y, encoding="utf-8")
    else:
        print("警告：本期未回傳 snapshot_targets，保留上期快照不動。", file=sys.stderr)

    rebuild_archive_index()

    print(f"已寫入 {wp.relative_to(ROOT)}（{len(doc['entries'])} 則）")


def rebuild_archive_index() -> None:
    """重建 data/archive-index.json —— 跨期查詢用的扁平索引。

    保留一年以上的期別後，逐期點閱已不可行。這個索引把所有期別的 entries
    攤平成一份檔案，讓 archive.html 只抓一次就能做關鍵字搜尋、篩選，
    以及「同一追蹤標的一年來的狀態變化」時間軸。
    索引是衍生資料，隨時可從期別檔案重建；期別檔案才是真實來源。
    """
    idx = json.loads((ROOT / "data" / "index.json").read_text(encoding="utf-8"))
    labels: dict[str, str] = {}
    snap = ROOT / "data" / "snapshot.yaml"
    if snap.exists():
        cur = None
        for line in snap.read_text(encoding="utf-8").splitlines():
            t = line.strip()
            if t.startswith("- id:"):
                cur = t.split(":", 1)[1].strip().strip('"')
            elif t.startswith("label:") and cur:
                labels[cur] = t.split(":", 1)[1].strip().strip('"')
                cur = None

    rows, weeks = [], []
    for w in sorted(idx["weeks"], key=lambda x: x["week"], reverse=True):
        doc = json.loads((ROOT / "data" / w["file"]).read_text(encoding="utf-8"))
        weeks.append({"week": doc["week"], "period_end": doc["period"]["end"],
                      "mode": doc["mode"], "file": w["file"],
                      "count": len(doc.get("entries", []))})
        for e in doc.get("entries", []):
            src = (e.get("sources") or [{}])[0]
            tgt = e.get("target", "")
            rows.append({
                "week": doc["week"], "period_end": doc["period"]["end"],
                "id": e["id"], "track": e["track"],
                "target": tgt, "target_label": labels.get(tgt, tgt or "未標記標的"),
                "title": e["title"], "prev_state": e["prev_state"],
                "curr_state": e["curr_state"], "evidence": e["evidence"],
                "priority": e["priority"], "impact": e.get("impact", []),
                "detail": e.get("detail", ""),
                "source_org": src.get("org", ""), "source_date": src.get("date", ""),
            })

    out = {
        "module": "07",
        "retention": {"min_months": RETENTION_MIN_MONTHS, "purge_allowed": False,
                      "note": "索引為衍生資料。期別檔案為真實來源，保留期內唯讀。"},
        "updated": max((w["period_end"] for w in weeks), default=""),
        "weeks": weeks, "entries": rows,
    }
    (ROOT / "data" / "archive-index.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    untagged = sum(1 for r in rows if not r["target"])
    print(f"已重建 archive-index.json：{len(weeks)} 期、{len(rows)} 則"
          + (f"（其中 {untagged} 則未標記 target，時間軸將歸入「未標記標的」）" if untagged else ""))


def index_is_stale() -> bool:
    """檢查 archive-index.json 是否落後於期別檔案。CI 用，不改檔。"""
    path = ROOT / "data" / "archive-index.json"
    before = path.read_text(encoding="utf-8") if path.exists() else ""
    rebuild_archive_index()
    after = path.read_text(encoding="utf-8")
    if before != after:
        if before:
            path.write_text(before, encoding="utf-8")   # 還原，CI 不該動工作區
        else:
            path.unlink(missing_ok=True)
        return True
    return False


def audit_retention() -> None:
    """檢查保留期。只警告，永不刪檔。"""
    idx = json.loads((ROOT / "data" / "index.json").read_text(encoding="utf-8"))
    missing = [w["week"] for w in idx["weeks"] if not (ROOT / "data" / w["file"]).exists()]
    if missing:
        sys.exit(f"保留期違規：index.json 列出但檔案不存在 → {', '.join(missing)}")
    print(f"保留期檢查通過：{len(idx['weeks'])} 期在檔，政策為至少 {RETENTION_MIN_MONTHS} 個月不刪除。")


# --------------------------------------------------------------------------- #

def main() -> None:
    ap = argparse.ArgumentParser(description="模組 07 週報工具")
    ap.add_argument("--print-brief", action="store_true",
                    help="印出本期作業指示（期別、觀測期間、上期快照、schema）")
    ap.add_argument("--ingest", metavar="FILE",
                    help="讀入產出的當期 JSON，驗證後寫入期別檔、索引與快照")
    ap.add_argument("--dry-run", action="store_true", help="搭配 --ingest：只驗證，不寫檔")
    ap.add_argument("--validate-only", action="store_true", help="只驗證現有檔案與保留期")
    ap.add_argument("--rebuild-index", action="store_true", help="只從期別檔案重建 archive-index.json")
    args = ap.parse_args()

    if args.print_brief:
        week_id, brief = current_brief()
        print(brief)
        return

    if args.rebuild_index:
        rebuild_archive_index()
        return

    if args.validate_only:
        idx = json.loads((ROOT / "data" / "index.json").read_text(encoding="utf-8"))
        bad = 0
        for w in idx["weeks"]:
            path = ROOT / "data" / w["file"]
            if not path.exists():
                print(f"[FAIL] {w['week']}")
                print(f"        檔案不存在: {w['file']}")
                bad += 1
                continue
            doc = json.loads(path.read_text(encoding="utf-8"))
            errs = validate(doc)
            if errs:
                bad += 1
                print(f"[FAIL] {w['week']}")
                for e in errs:
                    print(f"        {e}")
            else:
                print(f"[ OK ] {w['week']}")
        audit_retention()
        if index_is_stale():
            print("[FAIL] archive-index.json 與期別檔案不一致。"
                  "執行 python3 scripts/generate_week.py --rebuild-index 後重新提交。")
            bad += 1
        else:
            print("[ OK ] archive-index.json 與期別檔案一致")
        sys.exit(1 if bad else 0)

    if args.ingest:
        src = Path(args.ingest)
        if not src.exists():
            sys.exit(f"找不到輸入檔案: {src}")
        try:
            doc = json.loads(src.read_text(encoding="utf-8"))
        except json.JSONDecodeError as ex:
            sys.exit(f"{src} 不是合法的 JSON：{ex}")
        if not isinstance(doc, dict):
            sys.exit(f"{src} 的最外層必須是 JSON 物件，實際為 {type(doc).__name__}")

        # 期別與觀測期間以本腳本的計算為準，不採信輸入檔案裡的值。
        week_id, start, end = iso_week(datetime.now(TAIPEI))
        if doc.get("week") and doc["week"] != week_id:
            print(f"警告：輸入檔案的 week 為 {doc['week']}，與本次計算的 {week_id} 不符，"
                  f"以 {week_id} 為準。", file=sys.stderr)
        doc["week"] = week_id
        doc["period"] = {"start": start, "end": end}
        doc.setdefault("module", "07")

        errs = validate(doc)
        if errs:
            print("驗證失敗，不寫入任何檔案：", file=sys.stderr)
            for e in errs:
                print(f"  - {e}", file=sys.stderr)
            (ROOT / "rejected.json").write_text(
                json.dumps(doc, ensure_ascii=False, indent=2), encoding="utf-8")
            sys.exit("被拒的輸出已存為 rejected.json 供檢視。修正後重新 --ingest。")

        if args.dry_run:
            print(f"驗證通過（{week_id}，{len(doc['entries'])} 則）。--dry-run，未寫入任何檔案。")
            return

        write_all(doc)
        audit_retention()
        return

    ap.print_help()
    sys.exit("\n請指定一個動作。每週產出的流程見 prompts/routine.md。")


if __name__ == "__main__":
    main()
