# 資安合規週報 Security & Compliance Weekly

每週自動彙整資訊安全 / 網路安全重大事件、新聞與法遵動態的動態網站。

## 追蹤主題

1. **EU AI Act** — 歐盟人工智慧法案
2. **EU CRA** — 歐盟網路韌性法案（Cyber Resilience Act）
3. **EU NIS2** — 歐盟網路與資訊安全指令 2.0
4. **CMMC** — 美國國防部網路安全成熟度模型認證
5. **ISO 27000 系列** — 資訊安全管理標準
6. **ISO 42001** — 人工智慧管理系統標準
7. **TISAX** — 汽車產業資訊安全評鑑（VDA ISA）
8. 其他重大資安事件與新聞

## 網站架構

```
index.html            # 單頁式週報網站（無外部相依，純 HTML/CSS/JS）
reports/index.json    # 週報索引（新的排最前面）
reports/<id>.json     # 每週一份週報資料，id 格式：YYYY-Www（如 2026-W31）
```

網站於載入時讀取 `reports/index.json` 取得週報清單，再依選擇載入對應的
`reports/<id>.json` 渲染內容，支援深/淺色主題與週報存檔切換。

## 部署（GitHub Pages）

1. 進入 repo 的 **Settings → Pages**
2. Source 選擇 **Deploy from a branch**，Branch 選擇 `main`（root）
3. 儲存後即可透過 `https://<username>.github.io/WeekReportfromClaude/` 瀏覽

本機預覽：`python3 -m http.server` 後開啟 `http://localhost:8000`
（直接以 file:// 開啟會因瀏覽器安全限制無法讀取 JSON）。

## 每週更新流程（自動排程用）

每週一 08:00 由排程任務執行以下步驟：

1. 以網路搜尋彙整**過去一週**上述各主題的重大事件、新聞、法令動態
2. 依現有 schema 新增 `reports/YYYY-Www.json`（參考既有檔案結構）：
   - **雙語內容**：`title`、`summary`、`highlights[]`、`sections[].name`、item 的
     `title`/`content`/`action` 及含中文的 `date`，一律使用 `{ "zh": "...", "en": "..." }`
     物件（純日期或英文專名可用字串，網站兩種語言都會直接顯示）
   - `highlights`：本週 3–5 條焦點摘要
   - `sections[].topic` 使用固定 key：`eu-ai-act`、`eu-cra`、`nis2`、`cmmc`、`iso27000`、`iso42001`、`tisax`、`incidents`
   - 每則 item 含 `title`、`date`、`importance`（high/medium/low）、`content`、`action`（建議行動）、`sources`（來源連結）
   - 某主題當週無重大更新時，`items` 留空陣列即可
3. 在 `reports/index.json` **最前面**插入新週報的索引項目
4. Commit 並 push
