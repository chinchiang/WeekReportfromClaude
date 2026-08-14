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
index.html            # 單頁式網站（無外部相依，純 HTML/CSS/JS）
reports/index.json    # 週報索引（新的排最前面）
reports/<id>.json     # 每週一份報告資料，id 格式：YYYY-Www（如 2026-W33）
```

網站於載入時讀取 `reports/index.json` 取得週報清單，再依選擇載入對應的
`reports/<id>.json` 渲染內容，支援深/淺色主題、中英雙語與週報存檔切換。

## 部署（GitHub Pages）

1. 進入 repo 的 **Settings → Pages**
2. Source 選擇 **Deploy from a branch**，Branch 選擇 `main`（root）
3. 儲存後即可透過 `https://<username>.github.io/WeekReportfromClaude/` 瀏覽

本機預覽：`python3 -m http.server` 後開啟 `http://localhost:8000`
（直接以 file:// 開啟會因瀏覽器安全限制無法讀取 JSON）。

## 重要性評級規則（importance）

每則消息依下列標準評級，避免「高度關注」被濫用而稀釋警示價值：

| 等級 | key | 標準（符合任一即可） |
|---|---|---|
| 高度關注 | `high` | ① 90 天內有法遵生效日／申報截止日；② 漏洞已遭實際利用（in the wild / 列入 KEV）；③ 需要讀者在近期內採取具體行動 |
| 持續留意 | `medium` | 方向性／結構性變化（法案通過、標準改版、重大執法行動），但無近期行動期限 |
| 一般資訊 | `low` | 背景知識、產業動態、統計數據等參考性內容 |

**續報標示**：持續追蹤且本週無實質新進展的項目，標題加「【續報】/ [Follow-up]」前綴，讓讀者區分新聞與追蹤提醒。

**比例觀察**：`high` 佔比若超過三成，應回頭逐則覆核是否真的符合上表條件——但條件優先於比例，法遵密集期（多個生效日疊加遭利用漏洞）出現較高比例屬正常，不應為了壓低比例而降級符合條件的項目。

## 來源引用政策

1. **官方優先**：能取得一手來源（歐盟執委會、EUR-Lex、CISA、ENISA、ENX、ISO、廠商官方公告、司法部新聞稿等）時必須引用，並在 title 標註「(官方)」
2. **具體文章**：一律連到具體文章頁面，禁止只引用網站首頁或新聞列表頁
3. **免責**：內容由 AI 彙整公開資訊產生，重要決策應回到官方原文確認（頁尾已載明）

## 每週更新流程（自動排程用）

**發布頻率：每週一次，週日晚間 20:00（台北時間）。**
週日是該 ISO 週的最後一天，因此每期涵蓋的正是剛結束的完整一週（週一～週日）。

每次執行以下步驟：

1. 以網路搜尋彙整**本週（週一至週日）**上述各主題的重大事件、新聞、法令動態
2. 依現有 schema 新增 `reports/YYYY-Www.json`（Www 為今天所屬的 ISO 週次；
   `period` 寫本週一至週日，`publishedAt` 為當天）：
   - **雙語內容**：`title`、`summary`、`highlights[]`、`sections[].name`、item 的
     `title`/`content`/`action` 及含中文的 `date`，一律使用 `{ "zh": "...", "en": "..." }`
     物件（純日期或英文專名可用字串，網站兩種語言都會直接顯示）
   - `highlights`：本週 3–5 條焦點摘要
   - `sections[].topic` 使用固定 key：`eu-ai-act`、`eu-cra`、`nis2`、`cmmc`、`iso27000`、`iso42001`、`tisax`、`incidents`
   - 每則 item 含 `title`、`date`、`importance`（high/medium/low）、`content`、`action`（建議行動）、`sources`（來源連結）
   - `importance` 依上方「重要性評級規則」判定；`sources` 依「來源引用政策」（官方優先、必須連到具體文章）
   - 某主題當週無重大更新時，`items` 留空陣列即可
3. 在 `reports/index.json` **最前面**插入新一期的索引項目（title 如「2026 第 33 週」）
4. Commit 並 push
