# 模組 07 — 全球 AI 模型與產業動態觀測

Inventec 全球資安管理處內部技術情報站。每週一 08:00 (Asia/Taipei) 由 [Claude Routine](prompts/routine.md) 產出一期。

本模組掛在 [`chinchiang/WeekReportfromClaude`](../../) 的 `modules/07-ai-model-watch/` 子目錄下，
與根目錄的「資安合規週報」共用同一個 GitHub Pages 站台，網址為
`https://<owner>.github.io/WeekReportfromClaude/modules/07-ai-model-watch/`。
兩個模組的資料完全獨立：合規週報讀 `reports/*.json`，本模組讀 `modules/07-ai-model-watch/data/`，
彼此不共用 schema、不共用渲染器，也不得互相寫入。

與模組 02（EU AI Act）、模組 03（NIS2）、模組 04（ISO 27001 / IEC 62443）、模組 05（RED DA）、模組 06（CSL/DSL/PIPL）並行；本模組只處理**模型能力與產業供應面**，純法規進度交由其他模組，避免重複。

---

## 為什麼獨立成站

模組 07 的更新節奏與資料形狀跟法規週報不同：法規週報是「里程碑與截止日」，模型觀測是「狀態值的連續變動」。所以這個站不採每期一張 HTML 的做法，而是**資料驅動**：

- 每週的產出只寫 JSON，不產生 HTML
- `index.html` 永遠不需要改，網站樣式與資料徹底分離
- Delta 比對直接對結構化欄位做，不必從上期 HTML 反推

---

## 目錄結構

所有路徑相對於 `modules/07-ai-model-watch/`；腳本以 `__file__` 定位模組根目錄，
不受 repo 根目錄影響，因此在子目錄下運作方式與獨立 repo 時完全相同。

```
modules/07-ai-model-watch/
├── index.html                  # 本期報告渲染器，不需 build，不需依賴
├── archive.html                # 跨期查詢（逐則列表／標的時間軸）
├── data/
│   ├── index.json              # 期數清單，最新一期在陣列第一個
│   ├── archive-index.json      # 跨期查詢用的扁平索引（衍生資料）
│   ├── snapshot.yaml           # 追蹤標的狀態快照 = 下期 Delta 基準
│   ├── snapshots/              # 每期快照存檔，可回溯當時的基準
│   └── weeks/2026/2026-W34.json  # 每期一檔，保留期內唯讀
├── prompts/
│   ├── module-07.md            # 受版本控管的方法論
│   └── routine.md              # Claude Routine 的設定與 Instructions
├── scripts/generate_week.py    # 驗證與寫檔，不呼叫任何 API
└── docs/{SCHEMA,DEPLOY}.md
```

稽核工作流程放在 repo 根目錄的 `.github/workflows/m07-validate.yml`
（GitHub 只讀根目錄的 `.github/workflows/`），以 `paths:` 限定只在
`modules/07-ai-model-watch/**` 有變動時觸發，並以 `working-directory` 切進本目錄執行。

## 部署

Pages 由父 repo 統一提供（`main` 分支 `/ (root)`），本模組不需要獨立設定 ——
推上 `main` 後 `https://<owner>.github.io/WeekReportfromClaude/modules/07-ai-model-watch/`
就會更新。剩下的只有 [`prompts/routine.md`](prompts/routine.md) 的 Claude Routine 設定。

完整逐步流程見 [`docs/DEPLOY.md`](docs/DEPLOY.md)。

`index.html` 的 `const SEED = null;` 代表以 `data/` 為單一真實來源。因為是子目錄部署，
用 `file://` 直接開檔看不到資料 —— 本機預覽請在 repo 根目錄執行 `python3 -m http.server 8080`，
再開 `http://localhost:8080/modules/07-ai-model-watch/`。

---

## 資料結構

### `data/index.json`

`weeks` 陣列**最新一期必須在第一個**，頁面預設載入 `weeks[0]`。

### `data/weeks/YYYY-Www.json`

| 欄位 | 說明 |
|---|---|
| `mode` | `baseline`（首期，無 Delta）或 `delta` |
| `exec_summary` | 管理階層摘要，≤400 字，非技術讀者可讀 |
| `tracks.{A,B,C,D}.status` | `changed` / `unchanged` / `baseline` / `failed` |
| `entries[].evidence` | `verified` / `vendor` / `thirdparty` / `unverified` — 四選一，無預設值 |
| `entries[].priority` | `P0` / `P1` / `P2` / `P3` |
| `entries[].prev_state` → `curr_state` | 狀態轉換，頁面主視覺就是這條線 |
| `entries[].sources[].tier` | `1` / `2` / `3` |
| `counter_views` | 反面觀點，**必填**。空陣列時頁面會顯示「視為報告未完成」 |

設計上的一個硬性約束：`evidence` 沒有預設值，缺漏會被渲染成「尚未證實」的空心虛線樣式。**看起來未經查證的東西，就長得像未經查證。**

### `data/snapshot.yaml`

下期 Delta 的唯一基準。**必須在當期報告寫入成功後才覆寫**，否則會拿本期資料跟本期比。
`--ingest` 已經保證了這個順序：期別檔寫入成功才會動 snapshot。

---

## 每期怎麼產出

產出由 **Claude Routine** 每週一觸發一個 Claude Code 雲端 session 執行，
設定與 Instructions 全文見 [`prompts/routine.md`](prompts/routine.md)。流程是：

```
Routine（每週一 08:00）
  └─ 雲端 session
       ├─ python3 scripts/generate_week.py --print-brief
       │     方法論 + 本期期別／觀測期間 + 上期快照 + schema
       ├─ 四軌檢索與查證（WebSearch／WebFetch）
       ├─ 寫出 /tmp/m07-week.json
       ├─ python3 scripts/generate_week.py --ingest /tmp/m07-week.json
       │     驗證 → 寫期別檔 → 更新 index.json → 覆寫 snapshot → 重建 archive-index
       └─ commit & push（push main 被拒時改開 PR）
```

repo 內**沒有任何 API 金鑰**。`scripts/generate_week.py` 不呼叫 Anthropic API，
用量算在訂閱方案而非 API 帳單。`.github/workflows/validate.yml` 只做稽核
（schema、保留期、索引一致性），每次 push 與 PR 都跑。

期別、觀測期間與上期快照一律由 `--print-brief` 計算後注入，不由執行者自行判斷 ——
方法論步驟 0 的「不得寫死日期」靠這個機械保障，而不是靠指示寫得夠大聲。

## 保留與查詢

**保留政策**：期別檔案一經產出即唯讀。`scripts/generate_week.py` 在 `write_all()` 開頭就會檢查目標檔案是否已存在，存在即中止，不覆寫。政策為至少 12 個月不刪除（`data/index.json` 的 `retention` 欄位，`purge_allowed: false`），實務上永久保留 —— git 歷史本身就是不可否認的稽核軌跡。

`--validate-only` 會做保留期稽核：`index.json` 列出但檔案不存在，直接讓 CI 紅燈。這是防止有人「整理」掉舊期別的唯一機械式保護。

**查詢**：`index.html` 是本期報告，`archive.html` 是跨期查詢。一年 52 期之後逐期點閱不可行，所以 `archive.html` 讀的是 `data/archive-index.json` —— 一份把所有期別 entries 攤平的索引，只抓一次就能做關鍵字搜尋與篩選。

兩種檢視：

- **逐則列表** —— 依期別排序，可用關鍵字、年份、軌別、證據等級、優先級交叉篩選，每則可跳回原期報告。
- **標的時間軸** —— 依 `target` 分組，把同一個追蹤標的（例如 `glasswing-findings`）一年來的狀態變化串成一條線。這是保留一年真正的用途：不是為了留檔，是為了看得出趨勢。

索引是衍生資料，期別檔案才是真實來源。任何時候都可以重建：

```bash
cd modules/07-ai-model-watch
python3 scripts/generate_week.py --rebuild-index
```

## 每期的 target 標記

`entries[].target` 必須對應 `snapshot_targets[].id`。留空不會讓驗證失敗，但該則會被歸入「未標記標的」，一年後查不到它的演變 —— 這是唯一一個「不會報錯但會讓一年後的你吃虧」的欄位，值得每期抽查。

## 一個尚待決定的事項

`entries[].impact` 欄位目前填的是工作項層級（PSIRT、SBOM、SDL、架構韌性），不含 BG 層級的曝險描述。

如果這個 repo 是 public，就維持現狀 —— **不要**把「Inventec 影響矩陣」的 BG 層級內容寫進來。若要保留完整影響矩陣，repo 必須設為 private，並改用 GitHub Pages 的私有站或內部 intranet 託管。
