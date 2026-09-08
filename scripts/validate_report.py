#!/usr/bin/env python3
"""Validate one weekly report against the site's schema and the README quality rules.

    python3 scripts/validate_report.py 2026-W36
    python3 scripts/validate_report.py reports/2026-W36.json --no-watchlist

Errors (exit 1) are schema/policy violations that must be fixed before commit.
Warnings (exit 0) are judgment calls the author should look at once.
"""
import argparse
import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent
TOPICS = ["eu-ai-act", "eu-cra", "nis2", "cmmc", "iso27000", "iso42001", "tisax", "iec62443", "incidents"]
FULL_SCAN = {"cmmc", "iso42001", "tisax", "incidents"}   # "空章節不超過 2 個" applies to these only
IMPORTANCE = {"high", "medium", "low"}
GRADES_ZH = ("〔已證實〕", "〔廠商主張〕", "〔第三方評論〕", "〔尚未證實〕")
GRADES_EN = ("[Confirmed]", "[Vendor claim]", "[Third-party]", "[Unconfirmed]")
HOMEPAGE_HINTS = {"", "/", "/news", "/news/", "/blog", "/blog/", "/en", "/en/", "/zh", "/zh/", "/press", "/press/", "/newsroom", "/newsroom/"}


class Check:
    def __init__(self):
        self.errors, self.warnings = [], []

    def err(self, where, msg):
        self.errors.append(f"{where}: {msg}")

    def warn(self, where, msg):
        self.warnings.append(f"{where}: {msg}")


def is_bilingual(v):
    return isinstance(v, dict) and isinstance(v.get("zh"), str) and isinstance(v.get("en"), str) and v["zh"].strip() and v["en"].strip()


def has_cjk(s):
    return re.search(r"[一-鿿]", s or "") is not None


def check_bilingual(c, where, v, allow_str=False):
    if is_bilingual(v):
        return
    if allow_str and isinstance(v, str) and v.strip() and not has_cjk(v):
        return
    c.err(where, "必須是 {zh, en} 且兩邊皆非空" + ("（純日期／英文可用字串）" if allow_str else ""))


def check_source(c, where, s):
    if not isinstance(s, dict) or not s.get("url"):
        c.err(where, "來源缺 url")
        return
    u = urlparse(s["url"])
    if u.scheme not in ("http", "https") or not u.netloc:
        c.err(where, f"url 不合法：{s['url']}")
        return
    if u.path in HOMEPAGE_HINTS and not u.query and not u.fragment:
        c.err(where, f"來源只指向首頁／列表頁，須連到具體文章：{s['url']}")
    if not s.get("title"):
        c.warn(where, f"來源缺 title：{s['url']}")


def check_item(c, where, it, topic):
    for k in ("title", "content", "action"):
        if k not in it:
            c.err(where, f"缺 {k}")
        else:
            check_bilingual(c, f"{where}.{k}", it[k])
    if "date" not in it:
        c.err(where, "缺 date")
    else:
        check_bilingual(c, f"{where}.date", it["date"], allow_str=True)
    if it.get("importance") not in IMPORTANCE:
        c.err(where, f"importance 必須是 high/medium/low，得到 {it.get('importance')!r}")
    srcs = it.get("sources") or []
    if not srcs:
        c.err(where, "至少要有一個來源")
    for j, s in enumerate(srcs, 1):
        check_source(c, f"{where}.sources[{j}]", s)
    if topic == "peer-odm" and is_bilingual(it.get("title")):
        tz, te = it["title"]["zh"], it["title"]["en"]
        if not tz.startswith(GRADES_ZH):
            c.err(where, "peer-odm 的 title.zh 必須以〔已證實〕/〔廠商主張〕/〔第三方評論〕/〔尚未證實〕開頭")
        if not te.startswith(GRADES_EN):
            c.err(where, "peer-odm 的 title.en 必須以 [Confirmed]/[Vendor claim]/[Third-party]/[Unconfirmed] 開頭")
        if is_bilingual(it.get("content")) and not re.match(r"\*\*面向[:：]", it["content"]["zh"]):
            c.warn(where, "peer-odm 的 content.zh 應以「**面向：…**」開頭標明六大面向")


def check_watchlist(c, report):
    wl_path = ROOT / "areas" / "watchlist.json"
    if not wl_path.exists():
        c.warn("watchlist", "找不到 areas/watchlist.json，略過 Watchlist 檢查")
        return
    wl = json.loads(wl_path.read_text(encoding="utf-8"))
    by_topic = {s.get("topic"): s.get("items", []) for s in report.get("sections", [])}
    for t in wl.get("targets", []):
        items = by_topic.get(t["topic"], [])
        hit = None
        for it in items:
            tz = it.get("title", {}).get("zh", "") if isinstance(it.get("title"), dict) else ""
            if tz.startswith("【重點追蹤】") and any(k in tz for k in t.get("keywords", [])):
                hit = it
                break
        if hit is None:
            c.err("watchlist", f"標的「{t['title']['zh']}」在 {t['topic']} 章節沒有【重點追蹤】項目（六個標的每期必查）")
            continue
        te = hit["title"].get("en", "")
        if not te.startswith("[Watch]"):
            c.err("watchlist", f"「{t['title']['zh']}」的 title.en 應以 [Watch] 開頭")
        if t.get("milestone", {}).get("reached") and t["milestone"].get("reportedIn") == report.get("id") and hit.get("importance") != "high":
            c.err("watchlist", f"「{t['title']['zh']}」本期達成里程碑，importance 應為 high")


def check_index(c, report):
    idx_path = ROOT / "reports" / "index.json"
    if not idx_path.exists():
        c.err("index", "reports/index.json 不存在")
        return
    idx = json.loads(idx_path.read_text(encoding="utf-8"))
    ids = [e.get("id") for e in idx]
    rid = report.get("id")
    if ids.count(rid) > 1:
        c.err("index", f"{rid} 在 index.json 出現 {ids.count(rid)} 次")
    if rid not in ids:
        c.err("index", f"{rid} 尚未加入 reports/index.json")
    elif ids[0] != rid:
        c.warn("index", f"{rid} 不在 index.json 最前面（最前面是 {ids[0]}）")
    for e in idx:
        if e.get("id") == rid:
            if not is_bilingual(e.get("title")):
                c.err("index", "index 的 title 必須是 {zh, en}")
            if e.get("publishedAt") != report.get("publishedAt"):
                c.warn("index", f"index publishedAt {e.get('publishedAt')} 與報告 {report.get('publishedAt')} 不一致")


def validate(path: Path, want_watchlist=True):
    c = Check()
    try:
        report = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        c.err("json", f"JSON 不合法：{e}")
        return c, None

    rid = report.get("id", "")
    if not re.fullmatch(r"\d{4}-W\d{2}", rid):
        c.err("id", f"id 格式應為 YYYY-Www，得到 {rid!r}")
    if path.stem != rid:
        c.err("id", f"檔名 {path.name} 與 id {rid} 不一致")
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2} ~ \d{4}-\d{2}-\d{2}", report.get("period", "")):
        c.err("period", f"period 應為 'YYYY-MM-DD ~ YYYY-MM-DD'，得到 {report.get('period')!r}")
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", report.get("publishedAt", "")):
        c.err("publishedAt", f"應為 YYYY-MM-DD，得到 {report.get('publishedAt')!r}")
    for k in ("title", "summary"):
        check_bilingual(c, k, report.get(k))
    hl = report.get("highlights") or []
    if not 3 <= len(hl) <= 8:
        c.warn("highlights", f"建議 3–5 條，目前 {len(hl)} 條")
    for i, h in enumerate(hl, 1):
        check_bilingual(c, f"highlights[{i}]", h)

    sections = report.get("sections") or []
    topics = [s.get("topic") for s in sections]
    if topics[:9] != TOPICS:
        c.err("sections", f"前九個 topic 必須依序為 {TOPICS}，得到 {topics[:9]}")
    extra = topics[9:]
    if extra and extra != ["peer-odm"]:
        c.err("sections", f"第 10 個 section 只能是 peer-odm，得到 {extra}")

    total = high = 0
    empty_full = []
    for s in sections:
        t = s.get("topic")
        check_bilingual(c, f"sections[{t}].name", s.get("name"))
        items = s.get("items")
        if not isinstance(items, list):
            c.err(f"sections[{t}]", "items 必須是陣列")
            continue
        if not items and t in FULL_SCAN:
            empty_full.append(t)
        for i, it in enumerate(items, 1):
            check_item(c, f"{t}[{i}]", it, t)
            if t != "peer-odm":
                total += 1
                high += it.get("importance") == "high"
    if len(empty_full) > 2:
        c.err("sections", f"完整掃描主題中空章節超過 2 個：{empty_full}")
    if total and high / total > 0.30:
        c.warn("importance", f"high 佔比 {high}/{total} = {high/total:.0%}，超過三成，請逐則覆核（條件優先於比例）")

    if want_watchlist:
        check_watchlist(c, report)
    check_index(c, report)
    return c, report


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("week", help="week id such as 2026-W36, or a path to a report JSON")
    ap.add_argument("--no-watchlist", action="store_true", help="skip the six-target Watchlist presence check")
    args = ap.parse_args()
    p = Path(args.week)
    if not p.exists():
        p = ROOT / "reports" / f"{args.week}.json"
    if not p.exists():
        sys.exit(f"report not found: {args.week}")
    c, report = validate(p, want_watchlist=not args.no_watchlist)
    for w in c.warnings:
        print("WARN ", w)
    for e in c.errors:
        print("ERROR", e)
    n = sum(len(s.get("items", [])) for s in (report or {}).get("sections", []))
    print(f"{p.name}: {len(c.errors)} errors, {len(c.warnings)} warnings, {n} items")
    sys.exit(1 if c.errors else 0)


if __name__ == "__main__":
    main()
