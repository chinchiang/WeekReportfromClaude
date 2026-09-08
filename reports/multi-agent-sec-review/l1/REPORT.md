# L1 Mechanical Security Scan — WeekReportfromClaude

- **Repo:** https://github.com/chinchiang/WeekReportfromClaude (public)
- **Default / scanned:** `claude/security-weekly-report-site-joles7` @ `a1051392e0b595eeb697c212eb55851eeeacbdb8`
- **`origin/main`:** same SHA (no tree diff)
- **Live site:** https://chinchiang.github.io/WeekReportfromClaude
- **Pages:** legacy branch deploy, `main` `/`, `https_enforced=true`, last build `a105139`
- **Scan UTC:** 2026-09-08T08:20:00Z
- **Mode:** L1 mechanical only. No product fixes. No exploit PoC.

Machine-readable findings: [`FINDINGS.json`](FINDINGS.json). Tool artifacts: [`tools/`](tools/).

## Repo map

```
index.html                          # 資安合規週報 SPA (inline CSS/JS, no npm)
assets/sindy.png
reports/index.json + reports/2026-W3{1-6}.json
prompts/weekly-routine.md
AGENTS.md README.md
.github/workflows/m07-validate.yml  # only in-repo workflow
modules/07-ai-model-watch/
  index.html archive.html           # renderers (inline CSS/JS)
  scripts/generate_week.py          # stdlib validator/ingestor
  data/                             # weekly JSON + snapshots (no HTML)
  docs/ prompts/
```

- No `package.json`, lockfiles, `requirements.txt`, or other package manifests.
- No application server. Static GitHub Pages.
- Two HTML apps, same origin path prefix `/WeekReportfromClaude/`.

## Tools

| Tool | Result |
|---|---|
| gitleaks 8.24.2 tree (`--no-git`) | 1 hit, CVE id FP (L1-F06) |
| gitleaks 8.24.2 history (49 commits) | same 1 hit |
| osv-scanner 2.0.2 `-r` | no package sources |
| npm / pip-audit | N/A (no manifests) |
| rg storage / PAT / gist / Bearer | this-repo HTML/JS clean except `lang` localStorage |
| curl live Pages + sibling | 200s; no CSP; sibling live on same origin |
| `gh` repo / pages / workflows | default ≠ Pages source name; SHAs currently equal |
| workflow YAML review | 1 in-repo + GitHub-managed `pages-build-deployment` |
| DOM sink counts | innerHTML assign 15; eval 0; document.write 0 |

## Special focus (commander)

Same-origin class as WeeklySocialMediaIdea **F-web-gist-pat-localstorage**:

| Pattern | This repo HTML/JS | Sibling live `WeeklySocialMediaIdea` |
|---|---|---|
| `localStorage` set/get | `lang` only (`index.html`) | 15 hits; keys `wsmi-used-v2`, `wsmi-gh-token`, `wsmi-gist-id` |
| `sessionStorage` | 0 | 0 |
| `github_pat_` / `ghp_` / `ghpat_` literals | 0 | 0 (prompted at runtime, not hardcoded) |
| `api.github.com` | 0 | yes (`fetch('https://api.github.com'+path)`) |
| `Authorization` / `Bearer` | 0 | `Authorization: Bearer ` + `localStorage.getItem('wsmi-gh-token')` |
| gist / auto-sync | 0 | create/search/PATCH gists; UI「同步設定（設定/更換/移除 Token）」 |

Sibling origin check: `https://chinchiang.github.io/WeeklySocialMediaIdea/` → HTTP/2 200. Shared origin: `https://chinchiang.github.io`.

## Findings

See `FINDINGS.json` for the required field set. Summary:

| id | score | title |
|---|---|---|
| L1-F01 | 4 | Same github.io origin as sibling PAT-in-localStorage |
| L1-F02 | 1 | This repo localStorage is `lang` only (PAT search clean) |
| L1-F03 | 3 | Live Pages: no CSP / XFO / XCTO / RP / PP; ACAO `*` |
| L1-F04 | 3 | 15× innerHTML; href not protocol-allowlisted |
| L1-F05 | 2 | GHA: `checkout@v4` / `setup-python@v5` unpinned; persist-credentials default; no secrets |
| L1-F06 | 0 | gitleaks FP `CVE-2026-18577` |
| L1-F07 | 0 | No OSV/npm ecosystem |
| L1-F08 | 1 | Pages source `main` vs default branch name (SHAs equal now) |

## Stats

- findings_total: 8
- by_score: 0→2, 1→2, 2→1, 3→2, 4→1, 5→0
- gitleaks true secrets: 0
- pat_literals_this_repo: 0
- innerHTML_assign_total: 15
- eval_total: 0
- document_write_total: 0
- sibling_same_origin_live: true

## L2 gaps

1. XSS reachability via `javascript:` / `data:` in committed JSON `sources[].url` (no PoC in L1).
2. Reachability of unescaped `r.id` / `loadFail(id)` given index-constrained ids.
3. Whether operator browsers actually hold `wsmi-gh-token` while visiting this site.
4. GitHub-managed `pages-build-deployment` token permissions (not in repo).
5. Org/repo Actions secrets not referenced in YAML.
6. Google Fonts CSS on m07 as third-party on an origin that also hosts sibling PAT storage.
7. Other `chinchiang.github.io` projects that may also write credentials to localStorage.
8. HSTS at apex vs per-path (absent on captured project-page 200s).
