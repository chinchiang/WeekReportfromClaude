#!/usr/bin/env python3
"""Render the peer-odm (同業觀測) section of one weekly report as a standalone HTML page.

Usage:
    python3 scripts/render_peer_watch.py 2026-W36                 # -> build/peer-watch-2026-W36.html
    python3 scripts/render_peer_watch.py reports/2026-W36.json -o /tmp/x.html
    python3 scripts/render_peer_watch.py 2026-W36 --fragment     # body-only fragment (for Artifact publishing)

The page is generated verbatim from reports/<week>.json; nothing is rewritten.
It also lists the week's Watchlist items (titles prefixed 【重點追蹤】) from the other
sections as a compact "checkpoints" block, so the reader sees what to verify next week.
"""
import argparse
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

GRADE = {
    "已證實": ("confirmed", "已證實", "Confirmed"),
    "廠商主張": ("vendor", "廠商主張", "Vendor claim"),
    "第三方評論": ("third", "第三方評論", "Third-party"),
    "尚未證實": ("unconfirmed", "尚未證實", "Unconfirmed"),
}
IMP = {"high": ("高", "High"), "medium": ("中", "Medium"), "low": ("低", "Low")}


def md(s: str) -> str:
    """Minimal markdown: paragraphs, **bold**, `code`."""
    s = html.escape(s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"`(.+?)`", r"<code>\1</code>", s)
    return "".join(f"<p>{p.strip()}</p>" for p in s.split("\n\n") if p.strip())


def bi(v, key):
    """Bilingual field accessor: dict {zh,en} or plain string."""
    return v[key] if isinstance(v, dict) else str(v)


def span(zh, en, escape=True):
    if escape:
        zh, en = html.escape(zh), html.escape(en)
    return f'<span lang="zh">{zh}</span><span lang="en">{en}</span>'


LENS_RE = re.compile(r"^\*\*(?:Lens|面向)[:：]\s*(.+?)\*\*\s*")


def lens_of(txt):
    m = LENS_RE.match(txt)
    return m.group(1).rstrip("。.") if m else ""


def strip_lens(txt):
    return LENS_RE.sub("", txt)


def render_item(i, it):
    tzh, ten = bi(it["title"], "zh"), bi(it["title"], "en")
    gm = re.match(r"〔(.+?)〕", tzh)
    gk, gzh, gen = GRADE.get(gm.group(1) if gm else "", ("none", "未標", "Ungraded"))
    tzh = re.sub(r"^〔.+?〕", "", tzh).strip()
    ten = re.sub(r"^\[[^\]]+\]\s*", "", ten).strip()
    outside = "【窗口外】" in tzh or "[Outside window]" in ten
    tzh = tzh.replace("【窗口外】", "").strip()
    ten = re.sub(r"^\[Outside window\]\s*", "", ten)
    izh, ien = IMP.get(it.get("importance", ""), ("—", "—"))
    czh, cen = bi(it["content"], "zh"), bi(it["content"], "en")
    azh, aen = bi(it["action"], "zh"), bi(it["action"], "en")
    src = "".join(
        f'<li><a href="{html.escape(s["url"])}" target="_blank" rel="noopener">{html.escape(s.get("title", s["url"]))}</a></li>'
        for s in it.get("sources", [])
    )
    flag = f'<span class="flag">{span("窗口外", "Outside window")}</span>' if outside else ""
    return f"""
<article class="item" id="item-{i}">
  <aside class="rail">
    <span class="grade grade-{gk}">{span(f"〔{gzh}〕", f"[{gen}]")}</span>
    <dl>
      <dt>{span("重要性", "Importance")}</dt>
      <dd class="imp imp-{html.escape(it.get("importance", ""))}">{span(izh, ien)}</dd>
      <dt>{span("面向", "Lens")}</dt>
      <dd>{span(lens_of(czh), lens_of(cen))}</dd>
      <dt>{span("日期", "Date")}</dt>
      <dd class="date">{span(bi(it["date"], "zh"), bi(it["date"], "en"))}</dd>
    </dl>
    {flag}
  </aside>
  <div class="body">
    <h2>{span(tzh, ten)}</h2>
    <div class="prose"><div lang="zh">{md(strip_lens(czh))}</div><div lang="en">{md(strip_lens(cen))}</div></div>
    <div class="action">
      <h3>{span("建議動作", "Recommended action")}</h3>
      <div lang="zh">{md(azh)}</div><div lang="en">{md(aen)}</div>
    </div>
    <div class="sources">
      <h3>{span("來源", "Sources")}</h3>
      <ol>{src}</ol>
    </div>
  </div>
</article>"""


def render_checkpoints(report):
    rows = []
    for sec in report.get("sections", []):
        if sec.get("topic") == "peer-odm":
            continue
        for it in sec.get("items", []):
            tzh = bi(it["title"], "zh")
            if not tzh.startswith("【重點追蹤】"):
                continue
            ten = re.sub(r"^\[Watch\]\s*", "", bi(it["title"], "en"))
            tzh = tzh.replace("【重點追蹤】", "", 1).strip()
            izh, ien = IMP.get(it.get("importance", ""), ("—", "—"))
            rows.append(f"""
      <div class="cp">
        <div class="d"><span class="topic">{html.escape(sec.get("topic", ""))}</span><small class="imp imp-{html.escape(it.get("importance", ""))}">{span(izh, ien)}</small></div>
        <h3>{span(tzh, ten)}</h3>
        <p class="base">{span(bi(it["date"], "zh"), bi(it["date"], "en"))}</p>
      </div>""")
    if not rows:
        return ""
    return f"""
  <section class="checkpoints">
    <h2>{span("本期 Watchlist 現況（下期續查）", "Watchlist status this issue (re-check next week)")}</h2>
    <p class="sub">{span("取自本期其他章節中標題帶【重點追蹤】的項目，供同業觀測讀者對照法規面的節點。", "Items from the other sections whose titles carry the [Watch] prefix, so peer-watch readers can see the regulatory checkpoints alongside.")}</p>
    <div class="cp-grid">{''.join(rows)}
    </div>
  </section>"""


CSS = """
:root {
  --bg:#F4F6F7; --paper:#FFFFFF; --ink:#18242B; --ink-2:#4A5A63; --ink-3:#7A8990;
  --rule:#D6DEE2; --rule-2:#E7ECEF; --accent:#0F6C74; --accent-ink:#0B565C; --accent-soft:#E1F0F1;
  --warn:#9A5B0B; --warn-soft:#F6EBDA; --code:#EEF2F4;
  --serif:"Noto Serif TC","Songti TC","PMingLiU",Georgia,serif;
  --sans:"Noto Sans TC","PingFang TC","Microsoft JhengHei",-apple-system,"Segoe UI",sans-serif;
  --mono:"IBM Plex Mono","SFMono-Regular",Menlo,Consolas,monospace;
}
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) {
  --bg:#0F1619; --paper:#161F24; --ink:#E4EBEE; --ink-2:#AEBCC3; --ink-3:#7C8B92;
  --rule:#2B373D; --rule-2:#202A2F; --accent:#63C4CA; --accent-ink:#8ED8DC; --accent-soft:#12292C;
  --warn:#E0A657; --warn-soft:#2E2414; --code:#1E282D;
} }
:root[data-theme="dark"] {
  --bg:#0F1619; --paper:#161F24; --ink:#E4EBEE; --ink-2:#AEBCC3; --ink-3:#7C8B92;
  --rule:#2B373D; --rule-2:#202A2F; --accent:#63C4CA; --accent-ink:#8ED8DC; --accent-soft:#12292C;
  --warn:#E0A657; --warn-soft:#2E2414; --code:#1E282D;
}
* { box-sizing:border-box; }
body { background:var(--bg); color:var(--ink); font-family:var(--sans); font-size:15px; line-height:1.7; margin:0; }
:root:not([data-lang="en"]) [lang="en"] { display:none; }
:root[data-lang="en"] [lang="zh"] { display:none; }
.wrap { max-width:960px; margin:0 auto; padding:32px 20px 64px; }
.mast { display:flex; flex-wrap:wrap; align-items:flex-end; justify-content:space-between; gap:12px 24px; border-bottom:2px solid var(--ink); padding-bottom:14px; }
.mast .eyebrow { font-family:var(--mono); font-size:12px; letter-spacing:.08em; text-transform:uppercase; color:var(--ink-3); margin:0 0 6px; }
.mast h1 { font-family:var(--serif); font-size:30px; line-height:1.2; margin:0; text-wrap:balance; }
.mast h1 small { display:block; font-family:var(--sans); font-weight:500; font-size:14px; color:var(--ink-2); margin-top:6px; }
.mast .meta { font-family:var(--mono); font-size:12px; color:var(--ink-2); text-align:right; line-height:1.9; }
.mast .meta b { color:var(--ink); font-weight:500; }
.toggle { display:inline-flex; border:1px solid var(--rule); border-radius:999px; overflow:hidden; margin-top:4px; }
.toggle button { font:inherit; font-family:var(--mono); font-size:12px; padding:3px 12px; border:0; background:transparent; color:var(--ink-2); cursor:pointer; }
.toggle button[aria-pressed="true"] { background:var(--ink); color:var(--bg); }
.toggle button:focus-visible { outline:2px solid var(--accent); outline-offset:-2px; }
.legend { display:flex; flex-wrap:wrap; gap:8px 18px; padding:14px 0; border-bottom:1px solid var(--rule); font-size:12.5px; color:var(--ink-2); }
.legend .k { font-family:var(--mono); color:var(--ink-3); margin-right:4px; }
.grade { display:inline-block; font-family:var(--mono); font-size:12px; font-weight:500; padding:2px 8px; border-radius:3px; border:1px solid currentColor; line-height:1.5; white-space:nowrap; }
.grade-confirmed { color:var(--accent-ink); background:var(--accent-soft); border-color:transparent; }
.grade-vendor { color:var(--ink-2); }
.grade-third { color:var(--ink-2); border-style:dashed; }
.grade-unconfirmed { color:var(--warn); background:var(--warn-soft); border-color:transparent; }
.grade-none { color:var(--ink-3); border-style:dotted; }
.summary { margin:26px 0 8px; max-width:68ch; color:var(--ink-2); font-size:14.5px; }
.summary p { margin:0 0 8px; }
.empty { margin:26px 0; padding:18px; border:1px dashed var(--rule); color:var(--ink-2); }
.item { display:grid; grid-template-columns:184px 1fr; gap:0 32px; padding:30px 0; border-bottom:1px solid var(--rule); }
.item:last-of-type { border-bottom:2px solid var(--ink); }
.rail { font-size:12.5px; color:var(--ink-2); }
.rail dl { margin:14px 0 0; display:grid; grid-template-columns:auto 1fr; gap:4px 10px; }
.rail dt { font-family:var(--mono); font-size:11px; letter-spacing:.06em; text-transform:uppercase; color:var(--ink-3); padding-top:2px; }
.rail dd { margin:0; }
.rail .date { font-family:var(--mono); font-size:12px; }
.imp { font-weight:700; }
.imp-high { color:var(--warn); }
.imp-medium { color:var(--ink); }
.imp-low { color:var(--ink-3); }
.flag { display:inline-block; margin-top:12px; font-family:var(--mono); font-size:11px; letter-spacing:.06em; color:var(--warn); border-bottom:1px dashed var(--warn); }
.body h2 { font-family:var(--serif); font-size:21px; line-height:1.4; margin:0 0 14px; text-wrap:balance; }
.prose { max-width:68ch; }
.prose p, .action p { margin:0 0 12px; }
.prose strong, .action strong { font-weight:700; color:var(--ink); }
code { font-family:var(--mono); font-size:.88em; background:var(--code); padding:1px 5px; border-radius:3px; }
.action { max-width:68ch; margin-top:18px; padding:14px 18px; background:var(--paper); border-left:3px solid var(--accent); }
.action h3, .sources h3 { font-family:var(--mono); font-size:11px; letter-spacing:.08em; text-transform:uppercase; color:var(--accent-ink); margin:0 0 8px; }
.action p:last-child { margin-bottom:0; }
.sources { margin-top:18px; }
.sources h3 { color:var(--ink-3); }
.sources ol { margin:0; padding-left:20px; font-size:13px; line-height:1.6; }
.sources li { margin:0 0 4px; overflow-wrap:anywhere; }
.sources a { color:var(--accent-ink); text-decoration-color:var(--rule); text-underline-offset:3px; }
.sources a:hover { text-decoration-color:currentColor; }
.checkpoints { margin-top:34px; }
.checkpoints h2 { font-family:var(--serif); font-size:19px; margin:0 0 6px; }
.checkpoints .sub { margin:0 0 16px; font-size:13.5px; color:var(--ink-2); }
.cp-grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(300px,1fr)); gap:16px; }
.cp { background:var(--paper); border:1px solid var(--rule); padding:16px 18px; display:flex; flex-direction:column; gap:6px; }
.cp .d { display:flex; justify-content:space-between; align-items:baseline; font-family:var(--mono); font-size:12px; color:var(--accent-ink); }
.cp .d small { font-size:11px; }
.cp h3 { font-size:15px; margin:0; line-height:1.4; }
.cp p { margin:0; font-size:13px; color:var(--ink-2); }
.cp .base { font-family:var(--mono); font-size:11.5px; color:var(--ink-3); }
.foot { margin-top:36px; font-family:var(--mono); font-size:11.5px; color:var(--ink-3); }
@media (max-width:720px) {
  .item { grid-template-columns:1fr; gap:14px; }
  .mast .meta { text-align:left; }
  .mast h1 { font-size:25px; }
}
@media (prefers-reduced-motion:no-preference) { .toggle button { transition:background .15s, color .15s; } }
"""

JS = """
(function(){
  var root=document.documentElement, btns=document.querySelectorAll('.toggle button');
  function set(l){ if(l==='en') root.setAttribute('data-lang','en'); else root.removeAttribute('data-lang');
    btns.forEach(function(b){ b.setAttribute('aria-pressed', String(b.dataset.set===l)); });
    try{ localStorage.setItem('peerwatch-lang', l); }catch(e){} }
  btns.forEach(function(b){ b.addEventListener('click', function(){ set(b.dataset.set); }); });
  var saved=null; try{ saved=localStorage.getItem('peerwatch-lang'); }catch(e){}
  set(saved==='en'?'en':'zh');
})();
"""


def peer_summary(report):
    """Pull the 【同業觀測】 paragraph out of the report summary if present."""
    out = {}
    for lang, marker in (("zh", "【同業觀測】"), ("en", "[Peer Watch]")):
        s = bi(report.get("summary", ""), lang)
        idx = s.find(marker)
        if idx >= 0:
            para = s[idx + len(marker):].split("\n\n")[0].strip().lstrip("*").strip()
            out[lang] = para
    return out


def render(report):
    week = report["id"]
    sec = next((s for s in report.get("sections", []) if s.get("topic") == "peer-odm"), None)
    items = sec["items"] if sec else []
    body_items = "".join(render_item(i, it) for i, it in enumerate(items, 1))
    if not items:
        body_items = f'<div class="empty">{span("本期同業觀測未收錄任何項目（已檢索、無所獲；見 areas/peer-odm-watch.md）。", "No peer-watch items this issue (searched, nothing found; see areas/peer-odm-watch.md).")}</div>'
    summ = peer_summary(report)
    summary_html = ""
    if summ:
        summary_html = '<div class="summary">' + "".join(
            f'<p lang="{l}">{md(t)[3:-4]}</p>' for l, t in summ.items()) + "</div>"
    published = html.escape(str(report.get("publishedAt", "")))
    period = html.escape(str(report.get("period", "")))
    inner = f"""<div class="wrap">
  <header class="mast">
    <div>
      <p class="eyebrow">Inventec · GSMD · Peer Watch</p>
      <h1>{span("同業觀測", "Peer Watch")}
        <small>{span(f"全球電子代工業資安動態 · 資安合規週報 {week} 第 10 區塊", f"Security developments across the global ODM/OEM/EMS sector · Section 10 of the {week} compliance weekly")}</small></h1>
    </div>
    <div class="meta">
      <div>{span("觀測窗口", "Window")} <b>{period}</b></div>
      <div>{span("發布", "Published")} <b>{published}</b></div>
      <div class="toggle" role="group" aria-label="Language">
        <button type="button" data-set="zh" aria-pressed="true">中文</button><button type="button" data-set="en" aria-pressed="false">EN</button>
      </div>
    </div>
  </header>
  <div class="legend">
    <span class="k">{span("證據等級", "Evidence grade")}</span>
    <span><span class="grade grade-confirmed">{span("〔已證實〕", "[Confirmed]")}</span> {span("一手來源或兩家以上獨立可信媒體", "primary source, or two or more independent outlets")}</span>
    <span><span class="grade grade-vendor">{span("〔廠商主張〕", "[Vendor claim]")}</span> {span("當事企業單方說法", "the affected party's own account")}</span>
    <span><span class="grade grade-third">{span("〔第三方評論〕", "[Third-party]")}</span> {span("分析師或單一廠商遙測", "analyst view or single-vendor telemetry")}</span>
    <span><span class="grade grade-unconfirmed">{span("〔尚未證實〕", "[Unconfirmed]")}</span> {span("勒索集團宣稱、單一未證實報導", "leak-site claims, a single unverified report")}</span>
  </div>
  {summary_html}
  {body_items}
  {render_checkpoints(report)}
  <p class="foot">{span(f"資料來源：reports/{week}.json 的 peer-odm section，未經改寫。去重帳本：areas/peer-odm-watch.md。", f"Rendered verbatim from the peer-odm section of reports/{week}.json. Dedup ledger: areas/peer-odm-watch.md.")}</p>
</div>
<script>{JS}</script>"""
    fonts = '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Serif+TC:wght@600;700&family=Noto+Sans+TC:wght@400;500;700&family=IBM+Plex+Mono:wght@400;500&display=swap">'
    fragment = f"<title>同業觀測 {week}</title>\n{fonts}\n<style>{CSS}</style>\n{inner}\n"
    full = f"""<!doctype html>
<html lang="zh-Hant">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="light dark">
<title>同業觀測 {week}</title>
{fonts}
<style>{CSS}</style>
</head>
<body>
{inner}
</body>
</html>
"""
    return full, fragment


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("week", help="week id such as 2026-W36, or a path to a report JSON")
    ap.add_argument("-o", "--out", help="output path (default build/peer-watch-<week>.html)")
    ap.add_argument("--fragment", action="store_true", help="emit a body-only fragment with <title>/<style> at top (Artifact format)")
    args = ap.parse_args()

    src = Path(args.week)
    if not src.exists():
        src = ROOT / "reports" / f"{args.week}.json"
    if not src.exists():
        sys.exit(f"report not found: {args.week}")
    report = json.loads(src.read_text(encoding="utf-8"))
    full, fragment = render(report)
    out = Path(args.out) if args.out else ROOT / "build" / f"peer-watch-{report['id']}.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(fragment if args.fragment else full, encoding="utf-8")
    n = len(next((s["items"] for s in report.get("sections", []) if s.get("topic") == "peer-odm"), []))
    print(f"{out}  ({n} peer-odm items)")


if __name__ == "__main__":
    main()
