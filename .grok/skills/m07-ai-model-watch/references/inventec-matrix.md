---
description: "Inventec business-group impact matrix: PSG/EBG/NBG/ICZ and mapped work items (PSIRT, SBOM, SDL, supply chain, on-prem LLM). Read when filling section 5."
connections: [report-structure]
---

# Inventec 影響矩陣

公開可對應範圍（ODM／OEM 製造與資料中心）：不得虛構內部專案名稱。只能標「可能影響的既有工作項類型」。

## 群組

| 代碼 | 公開定位（寫進報告時可用此描述） | 與 AI 模型動態的典型接點 |
|---|---|---|
| EBG | Enterprise Business Group — 伺服器／資料中心／AI server | 雲端 API 可用性、Bedrock／Vertex 上架、AI server 客戶對模型世代的規格需求、出口管制 |
| PSG | 產品／系統相關製造群組（筆電以外之產品線，內部細分以公開資料為準） | 終端裝置端側模型、供應鏈元件 SBOM、客戶 SDL 要求 |
| NBG | Notebook Business Group — 筆電 | 裝置端 NPU／地端 LLM、消費／商用筆電 AI 功能供應條件 |
| ICZ | 其他營運／製造據點或內部代碼所指單位；**查無公開細分時標「公開資料不足以對應具體產品線」** | 供應鏈、在地資料主權、跨境模型存取 |

查無公開職責細分時：影響說明寫「查無公開資料可對應到該群組具體產品線」，**禁止編造組織圖**。

## 既有工作項（欄位必須出現，無影響填「無」）

| 工作項 | 何時標受影響 |
|---|---|
| PSIRT | 新模型顯著提升漏洞發現／利用能力，或 Glasswing／Big Sleep 類防禦能力改變通報節奏 |
| SBOM | 模型即服務或內嵌權重成為供應聲明對象；客戶要求模型版本列入物料 |
| SDL | 開發流程需納入新模型威脅（提示注入、供應鏈模型替換、評測造假） |
| 供應鏈安全 | 出口管制、區域下架、第三方模型 API 依賴、權重來源 |
| 地端 LLM 架構 | 旗艦模型授權／權重／硬體需求改變地端部署可行性 |

## 列表示例

| 業務群組 | 受影響既有工作項 | 影響說明 | 建議優先級 |
|---|---|---|---|
| EBG | 供應鏈安全、地端 LLM 架構 | （事實 + 證據等級） | P1 |
