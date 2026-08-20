# 資安合規週報 Security & Compliance Weekly

每週自動彙整資訊安全 / 網路安全重大事件、新聞與法遵動態的動態網站。

## 追蹤主題

1. **EU AI Act** — 歐盟人工智慧法案
2. **EU CRA** — 歐盟網路韌性法案（Cyber Resilience Act）
3. **EU NIS2** — 歐盟網路與資訊安全指令 2.0
4. **CMMC** — 美國國防部網路安全成熟度模型認證
5. **ISO 27000 系列** — 指 ISO/IEC 27000 系列中**與資訊安全相關的標準**：
   27001（ISMS 要求）、27002（控制措施）、27005（風險管理）、27017/27018（雲端安全與隱私）、
   27031（營運持續）、27035（事件管理）、27036（供應鏈）、27701（隱私資訊管理）等
6. **ISO 42001** — 人工智慧管理系統標準
7. **TISAX** — 汽車產業資訊安全評鑑（VDA ISA）
8. **IEC 62443** — 工業自動化與控制系統（IACS／OT）資安標準系列：
   4-1（安全開發流程）、4-2（元件要求）、3-2（風險評鑑）、3-3（系統要求）、2-1（IACS 資安管理）
9. 其他重大資安事件與新聞

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

## 各主題搜尋範圍

法遵類主題若只搜「本週新聞」常會落空——法規動態多發生在成員國、主管機關或標準組織層級，
而非國際媒體頭條。每個主題至少從下列角度各搜一次：

| 主題 | 除主線新聞外，必查的角度 |
|---|---|
| **EU NIS2** | 各成員國轉換進度與**登記期限**、**實際裁罰案例**（enforcement tracker）、國家主管機關指引（德國 BSI、荷蘭、比利時、義大利等）、NIS Cooperation Group 與 ENISA 技術文件、供應鏈安全條款 |
| **ISO 27000 系列** | **不限 27001，須逐一涵蓋系列中與資訊安全相關且不分產業適用的標準**：27000（總覽/術語）、27001（ISMS 要求）、27002（控制措施）、27003（實施指引）、27004（量測）、27005（風險管理）、27017/27018（雲端安全與隱私）、27031（營運持續）、27035（事件管理）、27036（供應鏈）、27040（儲存安全）、27701（隱私資訊管理）等的改版與修訂（amendment）；另含 27006（驗證機構要求，影響證書效力與稽核規則）、認可體系變動與稽核實務趨勢。<br>**排除**：產業別專屬分冊（27019 能源公用事業、27011 電信、27799 醫療照護等）預設不納入——本站讀者輪廓為製造與產品供應鏈，這些標準的適用對象是各該產業的營運者；僅在與追蹤主題產生實質交集時（例如某分冊改版連動 27002 控制措施）才報導。<br>**延伸範圍**：與上述標準直接相關的其他資訊安全標準（如 NIST CSF 與 SP 800-171 之於 CMMC/TISAX 對應、ISO 22301 之於營運持續、ISO/IEC 15408 Common Criteria 之於產品驗證；IEC 62443 已獨立為主題），在與本站追蹤主題有實質關聯時一併納入 |
| EU AI Act | 執委會/AI Office 執法動態、調和標準進度、Digital Omnibus 修正、成員國主管機關建置 |
| EU CRA | 調和標準發布、ENISA 通報平台、產品類別（Class I/II）技術規格 |
| CMMC | DoD/DoW 備忘錄、DFARS 修訂、C3PAO 生態、SPRS 規則 |
| ISO 42001 | 認證案例、與 AI Act 對應、稽核機構動態 |
| TISAX | ENX 公告、VDA ISA 版本適用日、AL2/AL3 評鑑實務 |
| **IEC 62443** | 各分冊改版與修訂（4-1／4-2／3-2／3-3／2-1、EN 版本與 A11 修訂）、**與 CRA 的調和進度**（CEN-CENELEC 調和標準、EN IEC TS 62443-6-2 評鑑方法）、ISASecure（CSA／SDLA／SSA）認證動態、ISA/IEC 委員會公告、OT/ICS 資安事件與工控產品漏洞（ICS-CERT／CISA ICS advisories） |

## 重點追蹤標的（Watchlist）

除九大主題的例行掃描外，下列標的每期**必查現況**，直到其里程碑達成為止；
相關項目標題加「【重點追蹤】/ [Watch]」前綴，讓讀者能逐期追蹤進度：

| 標的 | 追蹤問題 | 現況（隨每期更新） |
|---|---|---|
| **ENISA Single Reporting Platform（SRP）** | "The Cyber Resilience Act (CRA) introduces the Single Reporting Platform (SRP) for cybersecurity incident reporting in the EU Digital Single Market." —— **何時正式完工、啟用？** 官方規劃與 9/11 通報義務同步上線，須每期確認：平台是否已上線、公開網址是否公布、ENISA 指引／onboarding 文件更新、上線後的實際運作狀況與問題 | 截至 2026-08-16 仍未上線，網址未公布；ENISA 於 8/3–8/14 更新三份指引 |
| **CRA 調和標準刊登歐盟公報（OJ）** | **第一個 CRA 調和標準（harmonised standard）何時刊登 OJ？** 刊登之日起 Article 27 合規推定（presumption of conformity）才開始可用。須每期確認：OJ 是否已刊登任何 CRA 調和標準（刊登哪些、對應哪些產品類別）、CEN／CENELEC／ETSI 各標準草案進度（公眾意見徵詢、核准、交付執委會）、漏洞處理 Type A 標準與通用要求標準的時程變化 | 截至 2026-08-09 OJ 尚無任何 CRA 調和標準；Type A 原訂 2026-08 交付未實現，通用要求標準預估 2027-10；數項 CEN 標準已進入核准階段 |
| **CMMC 改革小組報告（9 月中出爐）** | DoD 的 60 天 CMMC 改革小組報告**何時發布、結論為何？** 報告將決定 Phase 2 第三方認證的存廢與替代方案（自我聲明擴大、商用方案採認、時程重排），直接影響國防供應鏈的合規路線。須每期確認：報告是否發布、發布後的關鍵結論（C3PAO 認證恢復或取代、Level 2/3 要求變化）、DoD 是否啟動 DFARS／32 CFR 修訂、Phase 2 暫停狀態是否變化 | RFI 已於 2026-08-14 截止；報告預計 2026-09 中旬提出；Phase 2 維持暫停，Level 1 自評與 DFARS 義務不變 |
| **NIS2 四國訴訟案（CJEU）結果** | 執委會於 2026-07-08 以未完成 NIS2 轉換為由，將**愛爾蘭、西班牙、法國、荷蘭**移送歐洲法院（CJEU），請求課以一次性罰款與按日計罰——**判決結果與罰款金額為何？** 須每期確認：CJEU 程序進度（案號、言詞辯論、佐審官意見、判決）、執委會是否因成員國完成轉換而撤回個別案件（荷蘭已於 2026-08-15 生效轉換法，其被訴基礎可能消失）、其餘三國的轉換立法進度 | 2026-07-08 移送；荷蘭 8/15 已完成轉換（觀察是否撤案）；愛爾蘭、西班牙、法國尚未完成；CJEU 尚未有程序進展公開 |

- 報導位置：SRP 與調和標準在 `eu-cra` 章節、CMMC 改革報告在 `cmmc` 章節、NIS2 訴訟案在 `nis2` 章節；**里程碑達成當期（SRP 正式啟用／首個調和標準刊登 OJ／CMMC 改革報告發布／CJEU 判決或撤案）以 high 回報**，之後轉為後續追蹤
- SRP 查詢角度：ENISA SRP 官方頁（enisa.europa.eu/topics/product-security/single-reporting-platform-srp）、ENISA 新聞稿、執委會 CRA reporting 頁、產業側報導（上線體驗、故障、onboarding 問題）
- 調和標準查詢角度：歐盟公報（eur-lex）、執委會 harmonised standards 頁、CEN-CENELEC 與 ETSI 公告、追蹤網站（如 craevidence.com 的 status tracker）
- CMMC 改革報告查詢角度：DoD／DoW CIO 辦公室公告與備忘錄、defensescoop／federalnewsnetwork 等國防媒體、法律事務所 client alert、Cyber-AB 與 C3PAO 生態圈反應
- NIS2 訴訟案查詢角度：CJEU 案件查詢（curia.europa.eu）、執委會侵權程序資料庫（infringement decisions）與新聞稿、四國國內立法進度、法律事務所 client alert

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
   - `sections[].topic` 使用固定 key：`eu-ai-act`、`eu-cra`、`nis2`、`cmmc`、`iso27000`、`iso42001`、`tisax`、`iec62443`、`incidents`
   - 每則 item 含 `title`、`date`、`importance`（high/medium/low）、`content`、`action`（建議行動）、`sources`（來源連結）
   - `importance` 依上方「重要性評級規則」判定；`sources` 依「來源引用政策」（官方優先、必須連到具體文章）
   - 某主題當週無重大更新時，`items` 留空陣列即可
3. 在 `reports/index.json` **最前面**插入新一期的索引項目（title 如「2026 第 33 週」）
4. Commit 並 push
