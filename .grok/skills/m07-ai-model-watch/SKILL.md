---
name: m07-ai-model-watch
description: "Run Module 07 weekly global AI model and industry watch: Taipei time window, snapshot YAML delta, four-track parallel retrieval, evidence tiers, eight-section Traditional Chinese intel report, then overwrite latest-snapshot.yaml and commit. Use when the user says 執行模組 07, 跑 m07 週報, AI model watch, 模組07, weekly AI model watch, or asks Grok Build to produce the Inventec AI-model weekly intel. NOT for EU AI Act JSON weekly reports, daily SOC patrols, or generic AI news roundups."
type: orchestrator
lifecycle: active
---

# 模組 07 — 全球 AI 模型與產業動態觀測

每週一 08:00（Asia/Taipei）執行。產出內部技術情報，非公關稿。全程**正體中文（臺灣慣用語）**；專業術語保留英文，首次加註中文。

**Repo**：`chinchiang/WeekReportfromClaude`（預設 `main`）  
**MODULE07_PATH**：`modules/07-ai-model-watch`（若 repo 已有不同路徑，以現況為準，禁止臆造）

讀取前先載入：
- `references/tracks.md` — 四軌來源與後備
- `references/evidence.md` — Tier／證據等級／衝突
- `references/report-structure.md` — 八節欄位
- `references/snapshot-schema.md` — YAML 契約
- `references/inventec-matrix.md` — 業務群組影響
- `assets/report-template.html` — 頁面樣式（對齊既有週報 CSS tokens）
- `references/agents-md.md` — 寫入目標 repo 的 AGENTS.md

## 硬性規則（最高優先）

1. 證據等級四選一、不得省略：【已證實】【廠商主張】【第三方評論】【尚未證實】
2. 廠商自評 benchmark 一律【廠商主張】，除非第三方復現
3. 查無資料寫「查無公開資料」——**嚴禁推測補齊**
4. ≥2 個 Tier 1 互相矛盾 → 並列並標【衝突未解】
5. 某軌無實質變更 → 寫「本期無變更」，禁止擴寫
6. 每則發現 ≥2 個獨立來源，其中 ≥1 個 Tier 1
7. 判定「本期」用來源**原始發布日**，非抓取日
8. 報告完成後才覆寫 `latest-snapshot.yaml`

## 工作流程

```
0 計算時間窗 → 1 讀 snapshot → 2 四軌平行檢索 → 3 查證分級
→ 4 寫八節 HTML → 5 更新 index + snapshot → commit
```

失敗不得中止整份報告。任一軌全失敗：該軌註明「本期檢索失敗：\<原因\>」，列入行動看板 P1，仍產出頁面與 snapshot。

### 步驟 0 — 時間窗

```bash
python3 .grok/skills/m07-ai-model-watch/scripts/period.py
```

觀測期間 = **前一個週一 00:00** 至 **執行日 07:59**（Asia/Taipei）。  
報告檔名用觀測週 ISO：`YYYY-Www.html`。開頭必須寫出本期起訖日。

### 步驟 1 — Snapshot（Delta 基準）

優先讀：

`https://raw.githubusercontent.com/chinchiang/WeekReportfromClaude/main/{MODULE07_PATH}/latest-snapshot.yaml`

也可用 GitHub `get_file_contents`。

| 結果 | 動作 |
|---|---|
| 成功 | 作為 Delta 基準，禁止改寫其上期值 |
| 失敗／不存在 | **基線建立版**。管理階層摘要第一句：「本期為基線建立版，無 Delta 比對」。種子標的見 `references/snapshot-schema.md` |

報告必須列出「本期新增追蹤標的」與「本期移除／暫停追蹤標的」。

### 步驟 2 — 四軌平行檢索（Subagents）

對 A/B/C/D **各啟動一個 subagent**（`isolation: none`）。每軌：

1. 至少 **3 次獨立查詢**（不同關鍵字或不同站點）
2. 先 Tier 1，無更新再後備來源
3. 自我檢核種子標的是否全查；漏了補查一次再交回

Subagent 回傳結構化發現清單（項目、上期→本期、來源 URL、發布日、建議證據等級）。主 agent 不得把 subagent 未附來源的內容寫進報告。

來源清單見 `references/tracks.md`。

### 步驟 3 — 查證

依 `references/evidence.md` 定 Tier 與證據等級。主 agent 合併四軌、去重、處理衝突。

### 步驟 4 — 八節報告

產出 `{MODULE07_PATH}/YYYY-Www.html`，沿用 `assets/report-template.html`（既有週報 `:root` tokens、`.site-header` / `.panel` / `.item` / `.imp-high|medium|low`）。

章節固定、不得增刪（細節見 `references/report-structure.md`）：

1. 管理階層摘要（≤400 字）
2. 本期 Delta 對照表
3. 模型能力雷達
4. 資安能力專章（防守方／攻擊方雙向）
5. Inventec 影響矩陣
6. 行動看板 P0–P3
7. 風險與反面觀點（必寫）
8. 來源附錄（依 Tier 分組）

語氣：內部技術情報。禁止行銷語彙。

**P0–P3**

| 級 | 準則 |
|---|---|
| P0 | 直接衝擊 PSIRT／SBOM／SDL；出口管制或重大存取限制；能力跳躍導致攻擊面明顯擴大 |
| P1 | 本月須評估的企業導入條件、定價、可用性 |
| P2 | 本季追蹤的中長期影響 |
| P3 | 僅觀察 |

### 步驟 5 — 寫入 repo

順序固定：

1. 寫 `{MODULE07_PATH}/YYYY-Www.html`
2. 更新 `{MODULE07_PATH}/index.html` 期數清單（**最新在最上方**）
3. `python3 .grok/skills/m07-ai-model-watch/scripts/validate_snapshot.py <yaml>` 通過後，才覆寫 `{MODULE07_PATH}/latest-snapshot.yaml`
4. 若 repo 根目錄尚無 Module 07 規則，寫入 `references/agents-md.md` 內容為 `AGENTS.md`（或合併既有檔，不得覆蓋無關規則）
5. Commit：`chore(m07): weekly AI model watch YYYY-Www`

GitHub：用 `push_files` 一次推送上述檔案到 `main`。本地 clone 則 `git add` → `commit` → `push`。

Snapshot 寫入失敗：報告末尾註記並建議人工介入。

## 品質檢查（交卷前）

- [ ] 時間窗起訖日正確
- [ ] 基線版已標示（若適用）
- [ ] 每則發現 ≥2 來源且含 1 個 Tier 1（或已標檢索失敗）
- [ ] 證據等級無空白
- [ ] 衝突已並列
- [ ] 八節齊全；無變更軌未灌水
- [ ] snapshot 通過 validate 腳本後才覆寫
- [ ] commit message 格式正確

## 常見問題

| 問題 | 處理 |
|---|---|
| `{MODULE07_PATH}` 不存在 | 建立目錄；index.html 用 template 的清單骨架；snapshot 走基線 |
| 官方頁 403／登入牆 | 改後備來源，Tier 降級並註明 |
| 與現有 `reports/*.json` SPA 週報衝突 | **不要**改 `reports/` JSON；Module 07 獨立目錄 |
| 部分軌失敗 | 繼續其他軌，失敗軌寫原因 + P1 |
