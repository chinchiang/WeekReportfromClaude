---
description: "Fixed eight-section Traditional Chinese report contract, table columns, P0-P3 rules, and HTML class mapping. Read before writing the weekly HTML."
connections: [evidence, inventec-matrix]
---

# 報告結構（固定八節）

語言：正體中文、臺灣慣用語。術語英文原文，首次加註。禁止行銷語彙。

對應 template：`assets/report-template.html`。重要性 class：P0→`.imp-high`，P1→`.imp-medium`，P2／P3→`.imp-low`。

## 1. 管理階層摘要（≤400 字）

- 首句：本期起訖日 + 是否基線建立版
- 濃縮 3–5 項變化與建議行動
- 字數以中文字元計，超標刪修飾不刪事實

## 2. 本期 Delta 對照表

| 軌別 | 項目 | 上期狀態 → 本期狀態 | 證據等級 | 優先級 |

基線版：上期狀態填「—（基線）」。無變更軌：一列「本期無變更」。

## 3. 模型能力雷達

| 模型名稱 | 版本／能力變更 | 定價變更 | 可用性／region 變更 | 證據等級 | 備註 |

查無公開資料的欄位寫「查無公開資料」，禁止填「維持不變」除非 snapshot 有上期值可對。

## 4. 資安能力專章（B 軌）

必含：
- 本期計畫／模型／夥伴變化
- **防守方影響**
- **攻擊方影響**
- 獨立驗證缺口

## 5. Inventec 影響矩陣

欄位與群組定義見 [[inventec-matrix]]。無影響的群組仍列一列「本期無直接影響」，禁止省略群組。

## 6. 行動看板

分 P0 立即／P1 本月／P2 本季／P3 觀察。空級寫「無」。

| 級 | 準則 |
|---|---|
| P0 | 直接衝擊 PSIRT／SBOM／SDL；出口管制或重大存取限制；能力跳躍導致攻擊面明顯擴大 |
| P1 | 本月須評估的導入條件、定價、可用性；任一軌檢索失敗 |
| P2 | 本季中長期影響 |
| P3 | 僅觀察 |

## 7. 風險與反面觀點（必寫、不可空）

至少涵蓋：PR 動機、商業誘因、benchmark 可比性、獨立驗證缺口、潛在過度宣稱。對主流敘事提出可檢驗的質疑，不是情緒反對。

## 8. 來源附錄

依 Tier 1 → 2 → 3 分組。每則：機構、標題、URL、原始發布日。

可選：重大跨軌事件於摘要後以短段落標示，**不新增第九節標題**。
