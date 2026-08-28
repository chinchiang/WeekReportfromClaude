# AGENTS.md — WeekReportfromClaude

這個 repo 掛了兩個彼此獨立的模組，共用一個 GitHub Pages 站台：

| 模組 | 路徑 | 資料 | 產出節奏 |
|---|---|---|---|
| 資安合規週報 | repo 根目錄 `index.html` | `reports/*.json` | 每週日 20:00 (Asia/Taipei) |
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
- 禁止改寫 `modules/07-ai-model-watch/` 下的任何檔案。

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
- 只 commit `modules/07-ai-model-watch/data/` 下的檔案。在模組目錄裡下 `git add data/` ——
  git 的 pathspec 相對於當前目錄，寫成完整路徑會失敗。
- Commit message：`chore(m07): weekly AI model watch YYYY-Www`。

完整 schema 與驗證器會擋下來的情況見
[`docs/SCHEMA.md`](modules/07-ai-model-watch/docs/SCHEMA.md)。

## CI

`.github/workflows/m07-validate.yml` 只對 `modules/07-ai-model-watch/**` 的變動做稽核
（schema、保留期、索引一致性），不產出、不呼叫任何 API。
