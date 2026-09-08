# AGENTS.md — WeekReportfromClaude

這個 repo 掛了兩個彼此獨立的模組，共用一個 GitHub Pages 站台：

| 模組 | 路徑 | 資料 | 產出節奏 |
|---|---|---|---|
| 資安合規週報 | repo 根目錄 `index.html` | `reports/*.json` | 每週一 23:30 (Asia/Taipei) |
| └ 同業觀測（`peer-odm` 區塊） | 同上（共用 `index.html`） | 同一份 `reports/<期別>.json` 內的 `peer-odm` section | 每週一 23:30 之後（緊接合規週報） |
| 模組 07 — 全球 AI 模型與產業動態觀測 | `modules/07-ai-model-watch/` | `modules/07-ai-model-watch/data/` | 每週一 08:00 (Asia/Taipei) |

**兩個模組不共用 schema、不共用渲染器，也不得互相寫入。** 執行任一模組的週報流程時，
另一個模組的檔案一個字都不要動。

## 通用規則
- 技術情報報告使用正體中文（臺灣慣用語）；專業術語保留英文原文，首次出現加註中文。
- 禁止推測、幻覺或填補無來源資訊。查無資料寫「查無公開資料」。
- 兩個以上 Tier 1 來源衝突時並列並標「【衝突未解】」，不得自行取捨。

## 資安合規週報（根目錄）
- 追蹤主題、重要性評級規則、來源引用政策、Watchlist 與每週更新流程見 [`README.md`](README.md)。
- 產出為 `reports/YYYY-Www.json`，並在 `reports/index.json` **最前面**插入新一期索引。
- 雙語欄位一律用 `{ "zh": "...", "en": "..." }`。
- 期別採 **ISO 週次**，涵蓋期間為該週的週一至週日；每週一 23:30 產出「剛結束的那一週」。
  例：2026-W36 涵蓋 2026-08-31 ~ 2026-09-06。**不得以執行日當週的週次命名剛結束的那一週。**
- 禁止改寫 `modules/07-ai-model-watch/` 下的任何檔案。
- 輔助腳本（都在 repo 根目錄執行）：
  - `python3 scripts/period.py --json`：決定期別；非零退出＝停下來回報（昨天非週日／該期已存在／index 連號不上）。
  - `python3 scripts/validate_report.py 2026-W36`：schema 與品質守則檢查，有 ERROR 不得 commit。
  - `areas/watchlist.json`：六個 Watchlist 標的的現況與歷史，每期回寫；驗證器據此檢查【重點追蹤】項目是否齊全。
  - `python3 scripts/csp_hash.py --write`：**改動 `index.html` 的 inline script 後必跑**，重算 CSP 的 script-src hash；
    忘了跑整站 JS 會被 CSP 擋掉。`--check` 供 CI 用。
- CI：`.github/workflows/reports-validate.yml` 在 `reports/**`、`areas/**`、`scripts/**`、`index.html` 變動時
  跑全部期別的驗證器、最新一期的 Watchlist 檢查、CSP hash 檢查與同業觀測渲染 smoke test。

### `peer-odm` 區塊（同業觀測）
- 由**獨立的 Routine**產出，寫入的是**同一份** `reports/<期別>.json` 的第 10 個 section
  （`topic: "peer-odm"`，排在 `incidents` 之後），不另開檔案、不動 `reports/index.json`。
- **必須在合規週報寫完該期檔案之後才執行**：兩者寫同一個檔，同時跑會互相覆蓋。
  執行前先 `git pull --rebase origin main`；若該期檔案尚不存在或九大主題 section 尚未齊備，
  **不得自行建檔**，應回報並中止，等合規週報完成後再跑。
- 該 section 的 items 沿用本站既有 schema（雙語 `title`／`content`／`action`、`date`、
  `importance`、`sources`）。同業觀測自有的四級證據等級以 `〔已證實〕`／`〔廠商主張〕`／
  `〔第三方評論〕`／`〔尚未證實〕` 前綴寫在 `title` 內，不新增 schema 欄位。
- `importance` 仍依 README 的評級規則判定，不與證據等級混用。
- 去重帳本放在 repo 內的 [`areas/peer-odm-watch.md`](areas/peer-odm-watch.md)（不用 memory 工具）：
  執行前先讀，產出後回寫「已報過的項目」「追蹤中的懸案」「已檢索但無所獲的方向」，
  與該期 JSON 一起 commit。
- 單獨渲染某一期的同業觀測：`python3 scripts/render_peer_watch.py 2026-W36`
  → `build/peer-watch-2026-W36.html`（`build/` 不進版控；加 `--fragment` 可得 Artifact 用的片段）。
  內容直接取自該期 JSON，不改寫；頁尾另列該期各章節標題帶【重點追蹤】的 Watchlist 項目。

## 模組 07 — 全球 AI 模型與產業動態觀測

**方法論的單一真實來源是 [`modules/07-ai-model-watch/prompts/module-07.md`](modules/07-ai-model-watch/prompts/module-07.md)，
不是本檔。** 本節只寫「這個模組在這個 repo 裡怎麼運作」，規則不抄第二份 ——
抄兩份的那天，就是它們開始不一致的那天。

- 產出由 **Claude Routine** 每週一觸發雲端 session 執行，設定與 Instructions 見
  [`prompts/routine.md`](modules/07-ai-model-watch/prompts/routine.md)。repo 內沒有任何 API 金鑰。
- **所有指令都在 `modules/07-ai-model-watch/` 子目錄執行**：

  ```bash
  cd modules/07-ai-model-watch
  python3 scripts/generate_week.py --print-brief          # 期別、觀測期間、上期快照、schema
  python3 scripts/generate_week.py --ingest /tmp/m07-week.json
  ```

  期別、觀測期間與上期快照一律由 `--print-brief` 計算後注入，**不得寫死日期、不得自行推算**。
- 產出是 **JSON，不是 HTML**。`index.html` 與 `archive.html` 是渲染器，每期都不需要改。
- `--ingest` 驗證通過才寫檔，並自動更新 `data/index.json`、`data/snapshot.yaml`、
  `data/snapshots/<期別>.yaml` 與 `data/archive-index.json`。**這四個檔一律不得手改。**
- `data/weeks/` 下已存在的期別檔案是唯讀的，保留期至少 12 個月。
- `entries[].evidence` 四選一：`verified`｜`vendor`｜`thirdparty`｜`unverified`，無預設值。
  標 `verified` 需 ≥2 筆來源且含 ≥1 筆 Tier 1 —— 驗證器會擋。
- `entries[].impact` 只填工作項層級（PSIRT、SBOM、SDL、架構韌性、採用政策、SOC 工具鏈），
  **不得填入 BG 層級曝險描述**，除非 repo 轉為 private（見 `docs/DEPLOY.md` 階段 0）。
- `entries[].target` 必須對應 `snapshot_targets[].id`，這是跨期時間軸的接點。
- `counter_views` 至少 2 則，必填。
- Commit message：`chore(m07): weekly AI model watch YYYY-Www`，只 add `modules/07-ai-model-watch/data/`。

完整 schema 與驗證器會擋下來的情況見
[`docs/SCHEMA.md`](modules/07-ai-model-watch/docs/SCHEMA.md)。

## CI

`.github/workflows/m07-validate.yml` 只對 `modules/07-ai-model-watch/**` 的變動做稽核
（schema、保留期、索引一致性），不產出、不呼叫任何 API。
