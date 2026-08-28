# 模組 07 上線與維運 Runbook

從掛載完成到「每週一自己跑」，約 25 分鐘。照順序做，每階段結束都有一個可驗證的成功條件 —— 條件不成立就不要進下一階段。

產出由 **Claude Routine** 觸發，不是 GitHub Actions。repo 內沒有任何 API 金鑰，用量算在訂閱方案裡。

---

## 階段 0 — 兩個要先確認的事（3 分鐘）

模組 07 已併入 `chinchiang/WeekReportfromClaude` 的 `modules/07-ai-model-watch/` 子目錄，
repo 與 GitHub Pages 都由父 repo 提供，**不需要再建 repo、不需要再開 Pages**。
以下用 `<OWNER>` 代稱 repo 擁有者。

| 決定 | 選項 | 影響 |
|---|---|---|
| **repo 可見性** | private / public | 目前 `entries[].impact` 只寫到工作項層級（PSIRT、SBOM、SDL），刻意不含 BG 曝險，public 可行。若日後要放完整「Inventec 影響矩陣」，**必須** private —— 注意這會一併把根目錄的資安合規週報變成 private。 |
| **產出模型** | 建議 Opus 級 | 在 Routine 的 model selector 選，不寫在 repo 裡。四軌檢索加交叉查證的判斷密度不低。 |

**private + GitHub Pages 需要付費方案**（Pro / Team / Enterprise）。

**成功條件**：兩個值都寫下來了。

---

## 階段 1 — 本機檢查（5 分鐘）

```bash
cd modules/07-ai-model-watch

# 1-1 驗證器要全綠
python3 scripts/generate_week.py --validate-only
```

預期輸出：`[ OK ] 2026-W34` + 保留期檢查通過 + 索引一致。任一項 FAIL 就停下來看訊息，不要往下做。

```bash
# 1-2 從 repo 根目錄起站（子目錄部署，路徑要對得起來）
cd ../..
python3 -m http.server 8080
```

開 `http://localhost:8080/modules/07-ai-model-watch/` 與
`http://localhost:8080/modules/07-ai-model-watch/archive.html`。
順手確認 `http://localhost:8080/` 的資安合規週報左側欄有「其他模組」面板，點得進本模組。

`index.html` 的 `const SEED` 已經是 `null`，資料一律來自 `data/`；
用 `file://` 雙擊開檔會看到「資料檔讀取失敗」，那是正常的，不是壞掉。

**成功條件**：
- 首頁顯示 W34 基線報告，四軌看板有數字，頁尾**沒有**橘色的「種子資料」警告
- `archive.html` 能搜尋、能切「標的時間軸」、點「看該期報告」能跳回首頁對應期別
- 主站左側欄的「其他模組」連得進本模組

---

## 階段 2 — 推上 GitHub（3 分鐘）

```bash
git add -A
git commit -m "feat(m07): mount AI model watch into WeekReportfromClaude"
git push -u origin main
```

**成功條件**：GitHub 上看得到 `.github/workflows/m07-validate.yml`、
`modules/07-ai-model-watch/data/weeks/2026/2026-W34.json`、
`modules/07-ai-model-watch/archive.html`，且 Actions 分頁的「模組 07 資料稽核」對這次 push 顯示綠燈。

---

## 階段 3 — 確認 Pages（2 分鐘）

父 repo 的 Pages 若已是 `main` / `/ (root)`，本模組不需任何額外設定。

**成功條件**：`https://<OWNER>.github.io/WeekReportfromClaude/modules/07-ai-model-watch/`
與 `.../archive.html` 都開得起來，且顯示的是真實資料而非錯誤畫面。
若看到「資料檔讀取失敗」，代表 `modules/07-ai-model-watch/data/` 沒被推上去或路徑錯了。

---

## 階段 4 — 建立 Claude Routine（10 分鐘）

到 [claude.ai/code/routines](https://claude.ai/code/routines) → **New routine**（或 CLI 執行 `/schedule`），
欄位與 Instructions 全文見 [`../prompts/routine.md`](../prompts/routine.md)（Instructions 內含 `cd modules/07-ai-model-watch`，別漏掉）。摘要：

| 欄位 | 值 |
|---|---|
| Name | `模組 07 週報` |
| Instructions | `prompts/routine.md` 第二節整段貼上 |
| Repositories | `<OWNER>/WeekReportfromClaude` |
| Environment | **Network access 改為 Full** —— 見下 |
| Trigger | Schedule → Weekly → 星期一 08:00（填本地時區） |
| Connectors | 全部移除 |

**唯一容易踩的設定是網路存取。** 預設環境是 **Trusted**，只放行套件庫與 GitHub
等預設清單。WebSearch 走 Anthropic 伺服器端不受影響，但 **WebFetch 走 session 的網路**
—— 廠商官方 blog、docs 的 pricing／deprecations 頁、主管機關公告都不在預設清單上，
會拿到 `403` 與 `x-deny-reason: host_not_allowed`。

症狀很好認：**搜尋得到，但打不開來源**，結果整期只剩 Tier 2／3，`verified` 一則都標不出來。
在 Routine 編輯頁點環境名稱 → 設定圖示 → **Network access** 改 **Full** → Save changes。

**成功條件**：Routine 出現在清單裡，詳情頁的 **Repeats** 顯示每週一，環境顯示的不是 Trusted。

---

## 階段 5 — 第一次正式產出（10 分鐘）

Routine 詳情頁 → **Run now**。這會開一個 session，你可以即時看它做什麼。

**成功條件**（五項全中才算成功）：

1. `modules/07-ai-model-watch/data/weeks/2026/2026-W35.json` 出現在 repo
2. `data/index.json` 的 `weeks[0]` 是 W35
3. `data/snapshot.yaml` 已更新，且 `data/snapshots/2026-W35.yaml` 多了一份存檔（皆在模組目錄下）
4. `data/archive-index.json` 的 `entries` 變多，`archive.html` 的「在檔期別」顯示 2
5. session 最後的回報段落列出四軌 status 與則數，且**沒有**「一手來源受網路政策阻擋」

**若失敗**：

- **驗證錯誤** —— session 裡會完整列出每一條。多半是模型漏填 `evidence`／`target`／
  `counter_views`，或來源少了 `url`／`date`。去 `prompts/module-07.md` 把該條規則寫得更硬，
  下一期就會照著做。這個階段失敗**不會**污染任何資料，`--ingest` 驗證不過就一個字都不寫。
- **四軌大量 `unverified`、note 提到 `host_not_allowed`** —— 回階段 4 改網路存取，
  然後**不要**重跑同一期：期別檔已經寫進去了就是唯讀的。等下一期即可，
  或先手動刪掉該期檔案與 `index.json` 裡的那一列再重跑（這是唯一一次可以這樣做的時機，
  因為保留期的意義是「已發布的報告不可竄改」，而這一期還沒發布給任何人看過）。
- **push 被拒改開了 PR** —— session 會明講。合併 PR 後 Pages 才會更新。
  若你希望每期都走 PR 而不是直接進 main，把 Instructions 步驟 5 的
  `git push origin main` 那段刪掉，只留 PR 那條路。

---

## 階段 6 — 確認排程接手（2 分鐘）

Routine 詳情頁的 **Repeats** 區塊要是啟用狀態，`Next run` 顯示下週一。
實際觸發會比設定時間晚幾分鐘（平台 stagger），每個 routine 的偏移固定，屬正常。

**成功條件**：`Next run` 有值，且指向下週一。

---

## 階段 7 — 維運

### 每月一次目視檢查（2 分鐘）

開 `archive.html`，看標頭的「最新」日期。**若落後超過兩週，排程出問題了**，沒有人會通知你。

Routine 詳情頁的 run 清單裡，**綠燈只代表 session 正常結束，不代表報告產出成功** —— 驗證不過而沒 commit 的那種失敗，run 一樣是綠的。所以目視檢查要看 `archive.html` 的最新日期，不是看 run 的顏色。

另外，Routine 用量算在訂閱方案裡，且有每日 run 數上限（見 [claude.ai/settings/usage](https://claude.ai/settings/usage)）。一週一次不會逼近上限，但同帳號的其他 routine 要一起算。

### 漏掉一期怎麼補

不要改既有檔案。Routine 詳情頁按 **Run now** 跑一次即可 —— 產生的是「當下這一期」。若真的要補歷史期別，本機執行後手動放檔案，並確認 `data/index.json` 的 `weeks` 有加進去、順序仍為新到舊，最後跑：

```bash
cd modules/07-ai-model-watch
python3 scripts/generate_week.py --rebuild-index
python3 scripts/generate_week.py --validate-only
```

### 改方法論

改 `prompts/module-07.md`，**commit message 必須寫明理由**。這個檔受版本控管的意義就在這裡：一年後回頭看某一期，`git log` 能告訴你當時是用哪版規則產出的。改了規則之後不要回頭重跑舊期別 —— 那會破壞保留期的唯讀性，也讓時間軸失真。

**Routine 的 Instructions 不需要跟著改。** 它每次都重新跑 `--print-brief` 去讀 repo 裡的方法論，所以永遠是最新版。Instructions 只寫「怎麼執行」，方法論只寫「查什麼、怎麼查證」，兩者不重疊 —— 規則抄兩份的那天，就是它們開始不一致的那天。

### 絕對不要做的事

- 改或刪 `data/weeks/` 下已存在的檔案。`write_all()` 會擋，但本機手改擋不住。
- 把 API 金鑰放回 repo 或環境變數。產出已經不走 API 了，`scripts/generate_week.py` 連 `urllib` 都不 import。
- 手改 `data/archive-index.json`。那是衍生資料，一律用 `--rebuild-index` 重建。
- 從模組 07 的流程去改 repo 根目錄的 `reports/`、`index.html`。那是資安合規週報，兩個模組共用 repo 但不共用資料。
- 在 `snapshot.yaml` 手動「修正」上期狀態去湊本期 Delta。要修正就在本期開一則新 entry 說明修正，讓歷史保留錯誤與更正的痕跡。

### 品質抽查（建議每季一次）

打開 `archive.html` → 篩選【已證實】→ 隨機挑 3 則，確認來源真的是 2 筆以上且有 Tier 1。驗證器只檢查數量與 tier 標記，**不檢查你標的 tier 是否誠實** —— 那是唯一需要人來把關的地方。

另外篩選一次「未標記標的」（時間軸檢視的最後一組）：`target` 留空不會讓驗證失敗，但那些紀錄在一年後查不到脈絡。
