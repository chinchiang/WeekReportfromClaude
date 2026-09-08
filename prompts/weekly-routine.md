# 資安合規週報 ＋ 同業觀測 — Routine Prompt（單一真實來源）

對應 Routine：`trig_01VEqZPDCTFbaghFz5ccCcJU`
「資安合規週報 ＋ 同業觀測 — 每週一 23:30 自動更新」
排程：`CRON_TZ=Asia/Taipei 30 23 * * 1`（每週一 23:30 台北）

> **這個檔是 Routine prompt 的權威版本。** 該 Routine 綁定持久 session，
> 其 prompt 無法由其他 session 以 `update_trigger` 修改；異動時請把下方
> `--- PROMPT ---` 之間的內容整段貼回 Routine 設定，並同步更新本檔。
>
> **狀態（2026-09-08）：已貼上，並經逐項比對確認。** 貼上時 Markdown 標記
> （粗體、反引號、清單符號）會被介面剝除，屬正常現象；剝除後的實質內容與本檔
> 相同（相似度 0.9998，22 項關鍵條款全數在位）。首次依新設定觸發為
> 2026-09-14 23:30 (Asia/Taipei)。
>
> **連接器狀態（2026-09-08 更新）：** 本 Routine 已於 Routine 設定介面掛上 **Gmail**
> 連接器（`list_triggers` 查證：`mcp_connections` 含 Gmail），B3 的寄送可正常執行。
> 連接器只能在 Routine 建立時（`create_trigger` 的 `connectors`）或於 Routine 設定介面
> 加掛，`update_trigger` 改不了。原先獨立的同業觀測 Routine
> （`trig_01TGAr6pTZKjiHUySLf8LKUu`，帶有 Gmail、Google Drive、Google Calendar 連接器）
> 已於 2026-09-08 停用並改名標記，未刪除，必要時可作為回復點。
>
> **B4 去重帳本已改為 repo 檔案：** Claude Code Remote 的 session 沒有 memory 工具，
> 帳本改放 [`areas/peer-odm-watch.md`](../areas/peer-odm-watch.md)，隨每期週報一起 commit。
> **Routine 內貼著的舊 prompt 仍寫 `memory_read`，且尚未含下列三個腳本的呼叫，請把下方整段 prompt 重新貼回。**
>
> **腳本（2026-09-08 起）：** `scripts/period.py` 決定期別並在誤觸發時擋下；`scripts/validate_report.py`
> 自動化 A4 自檢；`scripts/render_peer_watch.py` 渲染同業觀測。Watchlist 六標的的基線移到
> `areas/watchlist.json`，每期回寫，prompt 內不再寫死日期。
> Gmail 連接器的實際寄送尚未在 session 內測過（測試信被權限分類器擋下）。
>
> **期別防呆：** 若 Routine 被手動觸發或因故延至週二以後執行，「昨天」不會是週日；
> 此時依 prompt 的期別判定規則停下並回報，不得產出當週（尚未結束）的期別。
> 2026-09-08（週二）曾發生一次，該次正確地未產出 2026-W37。

--- PROMPT ---

【每週例行任務】現在是週一 23:30。CRW-01～06 六條法規觀測模組已於今日 09:30–14:30 跑完。本任務要產出**兩份**內容，寫進**同一份**週報檔並發布：A. 資安合規週報（九大主題）B. 同業觀測（第 10 個 peer-odm 區塊）。先做 A，A 完成寫檔後才做 B。

═══════ 共同前置 ═══════
0. git fetch origin main 並確保工作樹基於最新的 origin/main。
   - 本 repo 另掛獨立模組 `modules/07-ai-model-watch/`（每週一 08:00 由另一 Routine 產出）。依 AGENTS.md，**該目錄下的檔案一個字都不要動**。
   - 先讀 AGENTS.md 與 README.md，以它們為準。

**【期別判定——最重要，過去出過錯】**
本報告涵蓋的是**剛結束的那一週（上週一至昨天週日）**，不是今天所在的這一週。
- 檔名用「**昨天（週日）所屬的 ISO 週次**」：
  `python3 -c "import datetime; d=datetime.date.today()-datetime.timedelta(days=1); print(d.isocalendar())"`
- period 寫上週一至昨天，例如 "2026-09-07 ~ 2026-09-13"；publishedAt 為今天
- **不得以執行日當週的週次命名剛結束的那一週。**
- 換週判斷若與上一期 reports/index.json 的週次連號不上，或該週次檔案已存在且已是完整報告，**停下來報告，不要自行推測、不要硬產一份新的**。
- **先跑 `python3 scripts/period.py --json`**：它會算出期別、period、publishedAt，並在「昨天不是週日」「該期已存在且完整」「index 連號不上」時以非零退出並說明原因。**非零退出就停下來回報，不要自行覆寫判斷。** 後續檔名與 period 一律採用它的輸出。

═══════ A. 資安合規週報（九大主題）═══════
A1. 以 WebSearch 彙整「上週（上週一至昨天週日）」九大主題的重大事件、新聞、法令動態（每項附來源）：EU AI Act、EU CRA、EU NIS2、CMMC、ISO 27000 系列、ISO 42001、TISAX、IEC 62443、其他重大資安事件。

**【與《法規觀測》CRW-01～06 的分工——決定要搜多少】**
九大主題中有五個已由 CRW 模組每週一獨立追蹤：eu-ai-act（CRW-01）、eu-cra（CRW-02）、nis2（CRW-03）、iso27000 與 iec62443（CRW-04）。這五個主題本站改採**收斂模式**：
- 只寫三種內容：(a) 下列 Watchlist 標的現況；(b) 對讀者有具體期限或動作的項目；(c) 先前已報導、上週有實質新進展的【續報】。
- **不做廣泛新聞掃描**，不為填滿章節而收錄無期限、無動作的一般性報導。
- iso27000 與 iec62443 無 Watchlist 標的，改為**單一角度輕掃**（各分冊改版／修訂與認證體系變動），有就寫、沒有就讓章節空著，不要湊數。
- 這五個章節允許為空或只有一則；下方「空章節不超過 2 個」的自檢對這五個主題**不適用**。
剩下四個主題 cmmc、iso42001、tisax、incidents **維持完整掃描**，它們是本站的獨家價值。

**【重點追蹤標的（Watchlist）——每期必查，不可跳過】**（標題加「【重點追蹤】/ [Watch]」前綴；里程碑達成當期以 high 回報，之後轉為後續追蹤）
**每個標的的最新基線放在 repo 的 `areas/watchlist.json`（各標的的 baseline.status 與 history）**，開始搜尋前先讀它、以它為「截至上期」的現況；本期查證後把 baseline（asOf 改為本期週日）、history（追加本期一筆）與 milestone（達成時 reached=true、date、reportedIn）回寫，並與週報 JSON 一起 commit。下方只列追蹤問題、查證點與查詢角度：
- **ENISA Single Reporting Platform（SRP）**【eu-cra】：**何時正式完工、啟用？** 每期查證：是否已上線、公開網址是否公布、國家 CSIRT 協調員名單是否公布、是否提供通報 API、ENISA 指引/onboarding 更新、（上線後）實際運作狀況與問題。角度：ENISA SRP 官方頁與新聞稿、執委會 CRA reporting 頁、產業側報導。基線：見 `areas/watchlist.json` 的 `enisa-srp`。
- **CRA 調和標準刊登 OJ**【eu-cra】：**第一個 CRA 調和標準何時刊登 OJ？**（刊登之日起 Article 27 合規推定才可用）。每期查證：OJ 是否刊登（哪些標準、對應哪些產品類別）、CEN／CENELEC／ETSI 草案進度、Type A 與通用要求標準時程。角度：EUR-Lex／OJ、執委會 harmonised standards 頁、CEN-CENELEC 與 ETSI 公告、craevidence.com。基線：見 `areas/watchlist.json` 的 `cra-hen-oj`。
- **CRA 標準化委託 M/606 交付期限延後兩個月**【eu-cra】：A 類與漏洞管理 B 類由 2026-08-30 移至 **2026-10-31**、產品專屬 C 類由 2026-10-30 移至 **2026-12-31**。**修訂案是否正式通過？新期限是否再度跳票？** 角度：執委會標準化委託頁與 comitology／Have Your Say、CEN-CENELEC 與 ETSI 工作計畫、cyberresilienceact.eu、ibf-solutions.com。基線：見 `areas/watchlist.json` 的 `m606-deadline`。**撰稿必守**：(a) 嚴格區分「交付執委會 ≠ 核准為 EN ≠ 刊登 OJ」；(b) 每期重申法規義務與適用日（2026-09-11 通報、2027-12-11 主要義務）並未隨之變動——延後的只有標準，壓縮的是刊登到義務日之間的緩衝。
- **EU AI Act 調和標準進度**【eu-ai-act】：**第一個 AI Act 調和標準何時刊登 OJ？**（高風險義務已延至 2027-12-02）。每期查證：JTC 21 各草案進度、OJ 是否刊登、標準化委託時程調整、ISO 42001 是否被採認。角度：JTC 21 公告與工作計畫、EUR-Lex／OJ、執委會 AI 標準化委託頁、artificialintelligenceact.eu、法律事務所 client alert。基線：見 `areas/watchlist.json` 的 `ai-act-hen-oj`。
- **CMMC 改革小組報告**【cmmc】：**60 天改革小組報告何時發布、結論為何？** 每期查證：是否發布、關鍵結論（C3PAO 認證恢復或取代、Level 2/3 要求變化）、是否啟動 DFARS／32 CFR 修訂、Phase 2 暫停狀態變化。角度：DoD／DoW CIO 公告與備忘錄、defensescoop／federalnewsnetwork、法律事務所 client alert、Cyber-AB 與 C3PAO 生態圈。基線：見 `areas/watchlist.json` 的 `cmmc-reform-report`。
- **NIS2 四國訴訟案（CJEU）**【nis2】：執委會 2026-07-08 將愛爾蘭、西班牙、法國、荷蘭移送 CJEU，請求一次性罰款與按日計罰。**判決結果與罰款金額為何？** 每期查證：CJEU 程序進度（案件登錄、言詞辯論、佐審官意見、判決）、是否因完成轉換而撤回個案、四國轉換立法進度。角度：curia.europa.eu、執委會侵權程序資料庫與新聞稿、四國國內立法、法律事務所 client alert。基線：見 `areas/watchlist.json` 的 `nis2-cjeu`。

**【搜尋範圍要求】**（五個收斂模式主題只在上述範圍內找 Watchlist、期限與續報；cmmc／iso42001／tisax／incidents 完整適用）法遵類主題只搜「上週新聞」常會落空。每個主題至少換 2 個角度（詳見 README「各主題搜尋範圍」）：
- **EU NIS2**：成員國轉換進度與**登記期限**、**實際裁罰案例**、國家主管機關指引（德國 BSI、荷蘭、比利時、義大利）、NIS Cooperation Group 與 ENISA 技術文件、供應鏈條款
- **ISO 27000 系列**：**不要只搜 27001**，涵蓋 27000／27001／27002／27003／27004／27005／27017／27018／27031／27035／27036／27040／27701 的改版、修訂與草案；另含 27006（影響證書效力）、認可體系變動與稽核實務。**排除**產業別分冊（27019、27011、27799 等），僅在與追蹤主題有實質交集時納入。**延伸**：NIST CSF 與 SP 800-171（CMMC／TISAX 對應）、ISO 22301、ISO/IEC 15408。
- **IEC 62443**：各分冊改版與修訂（4-1／4-2／3-2／3-3／2-1，含 EN 版本與 A11）、**與 CRA 的調和進度**、ISASecure（CSA／SDLA／SSA）動態、ISA/IEC 委員會公告、CISA ICS advisories
- 其餘：AI Act 查執法動態、ISO 42001 查認證案例與 AI Act 對應、TISAX 查 ENX 公告與 ISA 版本適用日
- 若某主題確無上週動態，可納入「近 1–2 個月內、先前週報未報導過」的進展，並在 date 欄如實標示實際日期，不可偽裝成上週事件

A2. 依既有 schema 撰寫 reports/YYYY-Www.json 並以 python3 驗證 JSON。topic key 固定為 eu-ai-act、eu-cra、nis2、cmmc、iso27000、iso42001、tisax、iec62443、incidents（順序照此）。當週已有檔案就更新它。
A3. 中英雙語：title、summary、highlights[]、sections[].name、item 的 title/content/action 及含中文的 date 一律寫成 { "zh": "繁體中文", "en": "English" }（純日期可用字串），兩種語言都要完整撰寫。
A4. 【品質守則】遵守 README 的「重要性評級規則」與「來源引用政策」：
   - high 僅限：90 天內有法遵生效日/申報截止日、漏洞已遭實際利用（in the wild 或 CISA KEV）、或需讀者近期採取具體行動。已過期的截止日不算
   - medium：方向性/結構性變化（法案通過、標準改版、重大執法行動）但無近期期限
   - low：背景知識、產業動態、統計數據、市場趨勢——引述二手調查數據或談市場需求趨勢者一律 low
   - high 佔比超過三成就逐則覆核；但條件優先於比例，不要為壓低比例而降級符合條件的項目
   - 同一個期限不要重複用來把兩則都評為 high
   - 來源必須連到**具體文章頁面**，禁止只引用網站首頁或新聞列表頁
   - 能取得官方一手來源（執委會、EUR-Lex、CJEU/curia、CEN-CENELEC/JTC 21、ETSI、CISA、ENISA、ENX、ISO、IEC、DoD、廠商官方公告、DOJ 等）時必須引用，title 標註「(官方)」
   - 持續追蹤但上週無實質新進展者，標題加「【續報】/ [Follow-up]」；Watchlist 標的固定用「【重點追蹤】/ [Watch]」
   - 自我檢查：無首頁弱引用、high 比例合理、每則都有 action 與至少一個來源、空章節不超過 2 個（五個收斂模式主題不計入）、**六個 Watchlist 標的現況均已查證並回報**
A5. 在 reports/index.json 最前面插入新索引（title 用 {zh, en}；已存在則不重複）。

═══════ B. 同業觀測（peer-odm 區塊）═══════
產出《同業觀測》— 全球電子代工業（ODM/OEM/EMS）資安動態，收件人是英業達（Inventec, TWSE 2356）全球資安管理處處長 Jungle。正體中文與臺灣慣用語，保留英文專業術語。

**觀測窗口**：上週一至昨天週日（與 A 相同）。超出窗口但具重大後果、且先前未報過者可回溯 4～6 週，但必須明確標註「窗口外」與實際日期。

**觀測對象**
- ODM/EMS 同業：鴻海／Hon Hai、廣達 Quanta、緯創 Wistron、和碩 Pegatron、仁寶 Compal、緯穎 Wiwynn、Flex、Jabil、Celestica、Sanmina、Benchmark、立訊 Luxshare、比亞迪電子 BYD Electronics、工業富聯 FII
- 品牌客戶（供應商資安要求的變化）：HP、Dell、Lenovo、NVIDIA、Microsoft、Meta、Google、AWS、Cisco、Apple
- 台灣鄰接製造與零組件：台積電、日月光、聯電、台達、光寶、友達、群創、國巨、聯發科；以及位於 ODM 供應商邊界內的中小型後段服務／設備代理商

**六大優先面向（每則都要歸屬其一，寫在 content 開頭）**
1. AI 安全（AI 事件、AI 治理／ISO 42001、AI 驅動攻擊、AI 工具本身成為供應鏈入口）
2. 資料／IP 保護（事件、勒索、營業秘密與內部人案件、台韓美判決與檢調行動）
3. SOC 現代化（SIEM/XDR/MDR 廠商動態、agentic SOC、定價與包裝變化、併購）
4. OT 安全（ICS 通告、產線系統漏洞、IEC 62443／SEMI E187/E188、OT 威脅活動）
5. 供應鏈安全（韌體與硬體植入、BMC/BIOS/UEFI、SBOM、次階供應商曝險）
6. 產品安全期待（客戶供應商要求變更、CRA/Cyber Trust Mark/PSTI/JC-STAR、PSIRT、CVD、CMMC/FAR CUI）

**方法要求**
- 中英文並行檢索。中文優先查 iThome、DIGITIMES、TWCERT/CC、經濟日報、鉅亨網、TechNews、公開資訊觀測站重大訊息；英文查 CISA/NSA/DOJ/ENISA 一手公告、廠商 PSIRT、BleepingComputer、The Hacker News、SecurityWeek、Industrial Cyber、Dark Reading、ransomware.live 等洩密網站追蹤器。
- **每一則都必須交叉比對**，標示四級證據等級之一：`已證實`（一手來源或兩家以上獨立可信媒體）／`廠商主張`（當事企業或廠商單方說法）／`第三方評論`（分析師、媒體評論、單一廠商遙測）／`尚未證實`（單一未證實報導、勒索集團宣稱、傳聞）。
- 勒索集團在洩密網站掛名而受害方未證實者，一律列 `尚未證實`。
- 附完整可點擊來源連結。抓取失敗（403、robots）時改以其他獨立來源交叉驗證，並註明查證缺口。
- **絕不編造事實、日期或 URL。查不到就寫查不到。**

**B1. 寫進網站（peer-odm 區塊）— 這是主要交付**
在 A 已寫好的**同一份** reports/YYYY-Www.json 中，於 `incidents` 之後追加第 10 個 section：
`{ "topic": "peer-odm", "name": { "zh": "同業觀測", "en": "Peer Watch" }, "items": [ ... ] }`
- items 沿用本站既有 schema（雙語 title／content／action、date、importance、sources），**不新增 schema 欄位**。
- 四級證據等級以 `〔已證實〕`／`〔廠商主張〕`／`〔第三方評論〕`／`〔尚未證實〕` 前綴寫在 `title` 內（英文用 [Confirmed]／[Vendor claim]／[Third-party]／[Unconfirmed]）。
- `importance` 仍依 A4 的評級規則**獨立判定**，不與證據等級混用。
- 每則的 content 要寫「發生什麼（具體：名稱、CVE、數字、日期）」與「**為何重要**——對英業達的意涵」，考慮其台北/桃園、上海/重慶、休士頓、Juárez、Brno 六地佈局與中國廠區的法律隔離。
- 沒事的一週就讓這個區塊只有一兩則，或明白寫出未發現，**不要灌水**。此區塊不計入「空章節不超過 2 個」。

**B2. 另外產出完整 markdown 報告**
結構：1 管理階層摘要（敘事，把本週主線串起來，不要流水帳）2 本週建議動作清單（表格：動作／對應發現／建議期限／主責／判斷理由，3～6 項）3 逐項發現（依六大面向分節）4 建議深入研究的項目（1～3 項）5 查證缺口與更正 6 本週未發現（已檢索但無所獲的方向，如實列出；「未查得」不等於「無事發生」）。
存到 /mnt/user-data/outputs/ ，檔名 `同業觀測週報_<YYYY-MM-DD>.md`，並以 SendUserFile 送出。

**B3. Email**
用 Gmail 寄給 chinchiang.ccp@gmail.com，主旨 `【同業觀測】<YYYY-MM-DD> 全球電子代工業資安動態`，內文放管理階層摘要與建議動作清單。
**若本 session 沒有 Gmail 工具可用，不要靜默略過**——改以 SendUserFile 交付，並在最後回報中明確寫出「email 未寄出，原因：無 Gmail 工具」。

**B4. 去重帳本**
開始 B 之前先讀 repo 內的 `areas/peer-odm-watch.md`（觀測規格摘要、「已報過的項目」帳本、「追蹤中的懸案」與「已檢索但無所獲的方向」）。產出後把本週已報項目追加到「已報過的項目」表、更新「追蹤中的懸案」與「已檢索但無所獲的方向」，並與週報 JSON 一起 commit。同一則新聞不要連續兩週重報，除非有實質新進展——有新進展時寫明「上週報過 X，本週新增的是 Y」。**若該檔不存在，不要靜默略過**——依既有格式建立它，並在回報中註明。
**分工**：EU AI Act、EU CRA、NIS2、RED DA、ISO 27001/IEC 62443、中國 CSL/DSL/PIPL 由《法規觀測》CRW-01～06 追蹤；本區塊只在有「同業如何反應」或「新增操作面事實」時簡短帶過，不重述法規條文。

═══════ 收尾 ═══════
C1. 跑 `python3 scripts/validate_report.py <期別>`：它檢查 JSON 合法、topic 順序、雙語欄位齊備、每則有 action 與具體文章來源（非首頁）、high 佔比、完整掃描主題空章節不超過 2 個、六個 Watchlist 標的都有【重點追蹤】項目、peer-odm 的證據等級前綴，以及 index.json 已插入。**有 ERROR 就修到 0 再 commit；WARN 逐條看過。** 同時確認 `areas/watchlist.json` 與 `areas/peer-odm-watch.md` 已回寫。
C2. Commit 後推送到 main 與 claude/security-weekly-report-site-joles7 兩個分支（推送失敗以指數退避重試最多 4 次），**不開 PR**。
C3. 在對話中只回覆 3～5 句摘要，不要重貼全文。內容包含：上週合規面重點、同業觀測重點、以及任一 Watchlist 里程碑達成時的特別標註（SRP 上線／CRA 或 AI Act 調和標準刊登 OJ／M/606 修訂正式通過或新期限跳票／CMMC 改革報告發布／CJEU 判決或撤案）。若任一步驟失敗，明確說明原因，不要含混帶過。

--- END PROMPT ---
