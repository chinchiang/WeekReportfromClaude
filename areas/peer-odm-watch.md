# 同業觀測（peer-odm）— 觀測規格與去重帳本

> 這個檔取代原先設計中的 memory `/areas/peer-odm-watch.md`。Claude Code Remote 的
> session 沒有 memory 工具，因此帳本改放 repo，隨每期週報一起 commit。
> **每次執行 B（同業觀測）前先讀本檔；產出後回寫「已報過的項目」與「追蹤中的懸案」。**
> 唯一寫入者是合規週報 Routine（`trig_01VEqZPDCTFbaghFz5ccCcJU`）；
> 觀測規格的權威版本仍在 `prompts/weekly-routine.md` 的 B 段，本檔只摘要。

## 觀測規格（摘要）

- 收件人：英業達（Inventec, TWSE 2356）全球資安管理處處長 Jungle。
- 窗口：上週一至昨天週日；窗口外但重大且未報過者可回溯 4～6 週，須標「窗口外」與實際日期。
- 對象：ODM/EMS 同業、品牌客戶（供應商資安要求變化）、台灣鄰接製造與零組件。
- 六大面向：AI 安全／資料與 IP 保護／SOC 現代化／OT 安全／供應鏈安全／產品安全期待。
- 證據等級寫在 title 前綴：〔已證實〕〔廠商主張〕〔第三方評論〕〔尚未證實〕；
  勒索集團掛名而受害方未證實者一律〔尚未證實〕。
- 分工：EU AI Act、EU CRA、NIS2、RED DA、ISO 27001／IEC 62443、中國 CSL/DSL/PIPL 由
  法規觀測 CRW-01～06 追蹤；本區塊只帶「同業如何反應」或「新增操作面事實」。

## 去重規則

1. 同一則新聞不連續兩週重報，除非有實質新進展。
2. 有新進展時，content 開頭寫明「上週報過 X，本週新增的是 Y」。
3. 每期產出後：把本期 items 追加到「已報過的項目」，把仍在演變的事件寫進「追蹤中的懸案」；
   懸案結案時移到已報項目並註明結案期別。

## 已報過的項目

| 期別 | 日期 | 證據等級 | 標題（zh） | 面向 | 主要來源 |
|---|---|---|---|---|---|
| 2026-W36 | 2026-09-04 | 已證實 | SEMI E187 驗證標章 9/4 亮相：台灣主導的半導體設備資安標準走到「發證」這一步 | OT 安全／產品安全期待 | https://www.ithome.com.tw/news/178733 |
| 2026-W36 | 2026-08-28（窗口前 3 天）；下游處置落在 09 月第一週 | 已證實 | Zeabur 環境變數外洩：一把內部服務憑證換走整片 AI 金鑰，下游廠商被迫停用 AI 服務 | 供應鏈安全／AI 安全 | https://www.codecat.tw/blog/zeabur-security-incident-response |
| 2026-W36 | 2026-08-05 出現，首月活動至 2026-09-05（窗口外） | 尚未證實 | 新勒索服務 Panzer 首月宣稱 16–19 名受害者，含製造業；受害方均未證實 | 資料／IP 保護 | https://andreafortuna.org/2026/09/07/panzer-ransomware-italian-victims/ |
| 2026-W37 | 2026-09-01 掛名；2026-09-10～11 台灣媒體與台達回應 | 尚未證實 | Everest 掛名台達子公司晶睿通訊（VIVOTEK），宣稱 236 GB／約 9.5 萬檔；台達 9/11 否認系統受影響 | 資料／IP 保護 | https://www.ithome.com.tw/news/178859 |
| 2026-W37 | 事件 2026-08-28；官方證實 2026-09-05～06（窗口外） | 已證實 | 中科院採購資訊網：委外開發商內藏隱蔽排程管理介面遭境外 IP 破解；初判誤歸因於「AI Agent 越權」後更正 | 供應鏈安全 | https://udn.com/news/story/10930/9736514 |
| 2026-W37 | 2026-09-08 | 已證實 | ICS Patch Tuesday：Schneider Modicon M580 認證漏洞 CVE-2026-3869（CVSS 9.2）、Siemens 九則（四則 Critical）、Rockwell 九則 | OT 安全 | https://www.icscybersecurityconference.com/ics-patch-tuesday-september-2026-vulnerabilities-fixed-by-schneider-electric-siemens-aveva/ |

## 追蹤中的懸案

| 首報期別 | 事件 | 下一個觀察點 | 狀態 |
|---|---|---|---|
| 2026-W37 | 晶睿通訊（VIVOTEK）遭 Everest 掛名 | Everest 是否實際公開資料；晶睿／台達是否有後續公告；SOCRadar 所指員工與客戶憑證外洩是否出現下游濫用 | 追蹤中（尚未證實） |
| 2026-W37 | 中科院採購資訊網委外開發商隱蔽介面事件 | 調查局調查結果；中科院 SOP 內容；是否有其他公部門或民間系統使用同一開發商而存在相同介面 | 追蹤中 |
| 2026-W37 | Schneider Modicon M580 CVE-2026-3869（CVSS 9.2） | 是否出現在野利用或 PoC 公開；Schneider 是否釋出安全型號的修補與重新驗證指引 | 追蹤中 |
| 2026-W36 | SEMI E187 驗證標章 | TCA 是否於 2026-10 取得 TAF 認可成為驗證機構；年底前首波標章產品；台達電、志聖實機驗證結果 | 追蹤中 |
| 2026-W36 | Zeabur 環境變數外洩 | 官方事後檢討報告（root cause、受影響租戶數）；下游廠商求償與服務恢復；是否有二次濫用 | 追蹤中 |
| 2026-W36 | Panzer 勒索服務 | 任一製造業受害方公開證實；是否出現台灣或 ODM 供應鏈受害者 | 追蹤中（尚未證實） |

## 已檢索但無所獲的方向（供下期避免重複無效檢索）

- 2026-W37：ODM／EMS 十四家同業（鴻海、廣達、緯創、和碩、仁寶、緯穎、Flex、Jabil、Celestica、
  Sanmina、Benchmark、立訊、比亞迪電子、工業富聯）窗口內**均無**公開資安事件、重大訊息或洩密網站掛名；
  品牌客戶（HP／Dell／Lenovo／NVIDIA／Microsoft／Meta／Google／AWS／Cisco／Apple）無供應商資安要求公告變更；
  台灣鄰接製造與零組件（台積電、日月光、聯電、光寶、友達、群創、國巨、聯發科）窗口內無公開資安事件；
  台、韓、美三地無新的半導體／電子製造業營業秘密起訴或判決；SIEM／XDR／MDR 無新併購或定價包裝變化；
  韌體與硬體植入、BMC／BIOS／UEFI 無新事件；SEMI E187 驗證標章（W36 首報）窗口內無新公告。
- 2026-W37【不予採用】：「ReactorLock」新勒索軟體變種鎖定製造業 ICS 的說法（報導日 2026-09-09）僅見於
  單一每日新聞彙整，無一手來源、無研究報告、無受害者可佐證，本期不採用；下期若出現第二個獨立來源再評估。
- 2026-W37【避免誤讀】：Direwolf 於 9/7～9/8 掛名的 Lightcast（人資軟體）與 EMS1R（企業健康服務）
  **均非電子代工業者**，名稱中的 "EMS" 與本報告的 EMS 產業無關，勿誤列為同業受害。

- 2026-W36：鴻海／廣達／緯創／和碩／仁寶／緯穎、Flex／Jabil／Celestica／Sanmina／Benchmark、
  立訊／比亞迪電子／工業富聯 於窗口內均無公開資安事件或重大訊息；品牌客戶供應商資安要求無公告變更。
