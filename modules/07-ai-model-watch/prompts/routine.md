# 模組 07 — Claude Routine 設定

每週一 08:00 (Asia/Taipei) 的產出由 **Claude Routine** 觸發，不再由 GitHub Actions 執行。

差別在於「誰做檢索」：舊做法是 GitHub Actions 拿 `ANTHROPIC_API_KEY` 打 Messages API，
額度算在 API 帳單上；新做法是 Routine 起一個 Claude Code 雲端 session，
session 自己讀方法論、自己檢索、自己寫檔、自己 commit，額度算在訂閱方案的用量裡。
repo 內因此不再有任何 API 金鑰，`.github/workflows/` 只剩稽核。

---

## 一、建立 Routine

> **本站的 Routine 已建立**：`trig_018iBg6gypZGd7AnG4qsnz7a`（名稱「模組 07 週報」，
> 環境 `Danger1`，cron `0 0 * * 1` = 每週一 08:00 Asia/Taipei，完成時推播通知）。
>
> **⚠️ 模組 07 已併入 `chinchiang/WeekReportfromClaude` 的 `modules/07-ai-model-watch/`
> 子目錄。既有 Routine 的 Repositories 仍指向舊的獨立 repo，Instructions 也還是舊的
> 根目錄路徑 —— 兩者都必須到 [claude.ai/code/routines](https://claude.ai/code/routines)
> 手動更新（Instructions 存在 Anthropic 帳號那邊，不在 repo 裡，不會隨這次搬遷生效）。**
> 下面這節是給重建或另建一份時用的。改 Instructions 請一併改這個檔，兩邊要一致。

到 [claude.ai/code/routines](https://claude.ai/code/routines) → **New routine**，或在 CLI 執行 `/schedule`
（`/schedule` 是 CLI 專屬，在雲端 session 裡不可用，改用網頁介面）。

| 欄位 | 值 |
|---|---|
| **Name** | `模組 07 週報` |
| **Instructions** | 下面第二節整段貼上 |
| **Repositories** | `chinchiang/WeekReportfromClaude` |
| **Environment** | 見下方「網路存取」—— **不要用預設的 Trusted** |
| **Trigger** | Schedule → Weekly → 星期一 08:00（填你的本地時區，系統會自行換算） |
| **Connectors** | 全部移除。本工作不需要任何 connector，留著等於多開權限 |
| **Model** | 建議 Opus 級。四軌檢索加交叉查證的判斷密度不低 |

### 網路存取（唯一容易踩的設定）

Routine 預設環境的 network access 是 **Trusted**，只放行套件庫與 GitHub 等預設清單。
方法論要求優先檢索一手來源（廠商官方 blog、docs 的 pricing／deprecations 頁、
主管機關公告），這些網域都不在預設清單上。

- **WebSearch** 由 Anthropic 伺服器端執行，不走 session 的網路，Trusted 下照樣可用。
- **WebFetch／curl** 走 session 的網路。網域不在清單上會拿到 `403` 與
  `x-deny-reason: host_not_allowed` —— 症狀是「搜尋得到，但打不開來源」，
  結果就是整期只剩 Tier 2／3 來源，`verified` 一則都標不出來。

所以把 Routine 的環境 **Network access 設為 Full**（或 Custom + 自行維護廠商網域清單，
但一手來源每期都可能冒出新網域，維護成本不划算）。

### 排程的兩個已知行為

- 實際觸發時間會比設定時間晚幾分鐘（平台 stagger），每個 routine 的偏移固定。
- 最小間隔為 1 小時；週排程用預設 UI 即可，不需要自訂 cron。

---

## 二、Routine 的 Instructions（整段貼上）

```text
你是模組 07 的週報產出者，工作在 repo chinchiang/WeekReportfromClaude（已 clone 在
工作目錄，分支為預設的 main）。模組 07 的所有檔案都在 `modules/07-ai-model-watch/`
子目錄下，**本次工作的所有指令都在該子目錄執行**；repo 根目錄的 `reports/*.json` 與
`index.html` 是另一個模組（資安合規週報），**一個字都不要動**。

這是一個無人看管的自動化執行：沒有人會在旁邊回答問題，遇到判斷分岔時依下列規則
自行決定，不要停下來等待。

## 步驟 0：前置檢查

先切到模組目錄，後續每一步都在這裡執行：

    cd modules/07-ai-model-watch

然後執行：

    python3 scripts/generate_week.py --print-brief

若出現 unrecognized arguments 或找不到該選項，代表 main 分支上還是舊版腳本
（產出流程尚未合併）。此時立即停止，不要嘗試任何替代做法、不要改任何檔案，
直接回報「main 上的 generate_week.py 尚無 --print-brief，週報流程未就緒」。

## 步驟 1：取得本期作業指示

上一步的輸出包含四樣東西，全部照做：受版本控管的方法論（prompts/module-07.md）、
本期的期別與觀測期間、上期快照（Delta 基準）、輸出 schema。

期別與觀測期間以這份輸出為準。不要自己推算日期，也不要沿用你記憶中的任何日期。

## 步驟 2：執行檢索與查證

依方法論的步驟 2 到步驟 4 執行四軌檢索（A 模型發布、B AI 資安能力、C 企業導入與
供應條件、D 監理與標準連動），每軌至少 3 次獨立查詢。

- 優先用 WebSearch 找線索，再用 WebFetch 開一手來源確認。
- 每則發現至少交叉比對 2 個獨立來源，其中至少 1 個為 Tier 1，才能標 verified。
- 廠商自評 benchmark 一律標 vendor，除非有第三方復現。
- 查無資料就寫「查無公開資料」。嚴禁推測補齊，嚴禁為填充版面而擴寫。
- 某軌確實無實質變更，就把該軌 status 設為 unchanged，這是正常結果。
- 某軌檢索失敗（工具錯誤、來源不可達），該軌 status 設為 failed、note 寫失敗原因，
  並新增一則 priority 為 P1 的 entry 記錄這個缺口。不得因為一軌失敗就中止整期。

若 WebFetch 連續拿到 403 且訊息含 host_not_allowed，代表環境的網路白名單擋住了來源。
不要改用二手來源硬湊 verified：照實把該則標為 thirdparty 或 unverified，
並在該軌的 note 註明「一手來源受網路政策阻擋」。

## 步驟 3：寫出當期 JSON

把結果寫成一個 JSON 檔到 /tmp/m07-week.json，欄位依 schema。特別注意：

- evidence 與 priority 必填，四選一／四選一，不得自創值。
- 每則 entry 的 id 用 m07-YYYYWww-NN，同期內不得重複。
- 每則 entry 的 target 必須對應 snapshot_targets 的某個 id，沿用既有 id，
  只有全新標的才建新 id。這是跨期時間軸的接點，留空不會報錯但會讓該則失去脈絡。
- 每筆 sources 的 org / title / url / date / tier 全部必填，不得留空殼。
- counter_views 至少 2 則，每則要有 point 與 source。查無反面觀點時，寫一則說明
  「本期查無公開的對立論點，已檢索 <來源清單>」，並附上你實際檢索過的來源。
- snapshot_targets 必填，是本期所有追蹤標的的當前狀態，供下期 Delta 比對。
  漏了它，下期會拿舊基準比對，Delta 就錯了。
- impact 只填工作項層級（PSIRT、SBOM、SDL、架構韌性、採用政策、SOC 工具鏈…），
  不得填入 BG 層級的曝險描述。
- 語言：正體中文、臺灣慣用語，專業術語保留英文原文，內部技術情報語氣，不用行銷語彙。

## 步驟 4：驗證與寫入

執行：

    python3 scripts/generate_week.py --ingest /tmp/m07-week.json

驗證通過才會寫檔，並自動更新 data/index.json、data/snapshot.yaml、
data/snapshots/<期別>.yaml 與 data/archive-index.json。

驗證失敗時會列出每一條錯誤，並把被拒的輸出存成 rejected.json。
修正 /tmp/m07-week.json 後重跑 --ingest，最多重試 3 次。
三次仍不過就停在這裡，不要 commit，在 session 裡完整貼出錯誤清單。

絕對不要做的事：
- 不要修改 data/weeks/ 下任何已存在的期別檔案。保留期內的資料是唯讀的。
- 不要手改 data/index.json、data/snapshot.yaml、data/archive-index.json。
  這些都由 --ingest 產出。
- 不要修改 index.html、archive.html、scripts/、prompts/、docs/。
  這一期的工作只會新增 modules/07-ai-model-watch/data/ 下的檔案。
- 不要碰 repo 根目錄的任何檔案 —— `reports/`、根目錄 `index.html`、`README.md`
  都屬於資安合規週報模組，與本期工作無關。
- 不要 commit rejected.json（已在 .gitignore）。

## 步驟 5：Commit 與 push

先設定提交身分，讓 commit 掛在你自己的 GitHub 帳號下（這也讓後續推送 main 不被擋）：

    git config user.name  "chinchiang"
    git config user.email "chinchiang.ccp@gmail.com"

然後：

    git add modules/07-ai-model-watch/data/
    git commit -m "chore(m07): weekly AI model watch <期別>"
    git push origin main

推送 main 若被拒（分支受保護、或分支上有他人的 commit），改走 PR：

    git checkout -b claude/m07-<期別>
    git push -u origin claude/m07-<期別>

並開一個 PR 回 main，標題 chore(m07): weekly AI model watch <期別>。
兩種情況都要在 session 最後明講走的是哪一條路 —— 如果是 PR，網站要等合併後才會更新。

## 步驟 6：回報

在 session 最後用正體中文簡述：本期期別、四軌各自的 status、entries 則數、
其中 P0／P1 各幾則、有沒有標到 verified、走的是直接 push 還是 PR。
若有任何一軌 failed，把原因放在回報的第一句。
```

---

## 三、維運

**每次跑完看什麼**：Routine 詳情頁的 run 清單裡，綠燈只代表 session 正常結束，
不代表報告產出成功。點進去看最後的回報段落 —— 四軌 status 與 entries 則數
比綠燈誠實得多。

**沒跑到怎麼辦**：Routine 詳情頁有 **Run now**，可立即補跑一次；產生的是「當下這一期」。
排程本身可在 **Repeats** 區塊暫停與恢復。

**用量**：Routine 的用量算在訂閱方案裡，另外有每日 run 數上限，
在 [claude.ai/settings/usage](https://claude.ai/settings/usage) 看得到剩餘量。
一週一次的排程不會逼近上限，但同帳號若還有其他 routine 要一起算。

**改 Instructions**：Routine 的 Instructions 存在 Anthropic 帳號那邊，不在 repo 裡。
本檔第二節是它的副本 —— 改了任一邊就要同步另一邊，否則一年後沒人知道當時跑的是哪版。

**改方法論**：改 `prompts/module-07.md`，commit message 寫明理由。
Routine 的 Instructions 不需要跟著改 —— 它每次都重新讀 `--print-brief`，
方法論永遠是 repo 裡的最新版。這是把 Instructions 寫成「去讀 repo」而不是
「把規則抄進 Instructions」的原因：方法論只有一份，且受版本控管。
