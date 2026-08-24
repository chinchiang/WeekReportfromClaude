---
description: "Tier definitions, four evidence labels, conflict handling, and anti-speculation rules. Read during verification (step 3)."
connections: [tracks, report-structure]
---

# 查證與分級

## Tier

| Tier | 定義 | 例子 |
|---|---|---|
| 1 | 廠商官方一手 | model card、system card、API docs、pricing、status page、官方 blog、SEC filing、主管機關公告 |
| 2 | 具編輯審查的專業媒體與獨立技術評測 | 專業媒體、獨立評測、經同儕或編輯審查之研究 |
| 3 | 其餘 | 部落格、社群、分析師評論、廠商行銷內容 |

每則發現：**≥2 個獨立來源，其中 ≥1 個 Tier 1**。無法滿足則降為【尚未證實】或刪除（寧可漏報，不可灌水）。

## 證據等級（報告用字固定）

| 標籤 | 何時用 |
|---|---|
| 【已證實】 | ≥1 Tier 1 + 獨立交叉，且無衝突 |
| 【廠商主張】 | 僅來自該廠商一手，或自評 benchmark 未經第三方復現 |
| 【第三方評論】 | 僅有 Tier 2／3，無官方一手 |
| 【尚未證實】 | 單一來源、傳聞、無法交叉 |
| 【衝突未解】 | ≥2 個 Tier 1 對同一事實矛盾——並列雙方，**不得擇一** |

Snapshot YAML 的 `evidence` 欄只能是：`證實`｜`廠商主張`｜`第三方評論`｜`未證實`（無書名號、無「衝突」值；衝突項在報告內處理，snapshot 取「未證實」並在報告註記）。

## 禁止

- 推測補齊「合理應有」的定價、日期、夥伴數
- 把 retriever／搜尋摘要日期當成 published date
- 把行銷 landing page 當 Tier 1（官方 docs／news／legal 才是）
- 把「即將」「據說」寫成已發布
