---
description: "Knowledge graph index for m07-ai-model-watch. Start here when choosing which reference to load."
connections: [tracks, evidence, report-structure, snapshot-schema, inventec-matrix, agents-md]
---

# Module 07 Knowledge Graph

## Core

- [[tracks]] — A/B/C/D 軌優先來源、後備來源、最低查詢次數
- [[evidence]] — Tier 1/2/3、證據四級、衝突並列規則
- [[report-structure]] — 固定八節、欄位、摘要字數、P0–P3
- [[snapshot-schema]] — latest-snapshot.yaml 契約與種子標的
- [[inventec-matrix]] — PSG／EBG／NBG／ICZ 與既有工作項
- [[agents-md]] — 寫入目標 repo 的 AGENTS.md 全文

## 載入時機

| 步驟 | 讀 |
|---|---|
| 步驟 2 派 subagent 前 | [[tracks]] |
| 步驟 3 分級 | [[evidence]] |
| 步驟 4 寫 HTML | [[report-structure]] + `assets/report-template.html` |
| 步驟 1／5 snapshot | [[snapshot-schema]] |
| 影響矩陣 | [[inventec-matrix]] |
| 首次落地或缺 AGENTS.md | [[agents-md]] |
