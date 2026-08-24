# AGENTS.md — WeekReportfromClaude / Module 07

## 通用規則
- 技術情報報告使用正體中文（臺灣慣用語）；專業術語保留英文原文，首次出現加註中文。
- 禁止推測、幻覺或填補無來源資訊。查無資料寫「查無公開資料」。
- 證據等級只能使用：【已證實】【廠商主張】【第三方評論】【尚未證實】。
- 兩個以上 Tier 1 來源衝突時並列並標「【衝突未解】」，不得自行取捨。

## Module 07 特定規則
- 時間窗動態計算：前一週一 00:00 至執行日 07:59 Asia/Taipei；以原始發布日為準。
- 先讀 `{MODULE07_PATH}/latest-snapshot.yaml` 作 Delta；失敗標「基線建立版」。
- MODULE07_PATH 預設 `modules/07-ai-model-watch`。禁止改寫 `reports/*.json` 合規 SPA 週報。
- 四軌（A 模型、B 資安、C 企業導入、D 監理）使用平行 subagents，每軌至少 3 次獨立查詢。
- 報告固定八節，不得增刪。
- Inventec 影響矩陣必須涵蓋 PSG／EBG／NBG／ICZ 與 PSIRT、SBOM、SDL、供應鏈安全、地端 LLM 架構。
- 行動看板 P0–P3 判斷準則見 m07-ai-model-watch skill。
- snapshot.yaml 必須在報告完成後才覆寫；`evidence` 僅允許：證實｜廠商主張｜第三方評論｜未證實。
- Commit message：`chore(m07): weekly AI model watch YYYY-Www`

## Git
- 報告：`{MODULE07_PATH}/YYYY-Www.html`
- 更新 `{MODULE07_PATH}/index.html`（最新在最上方）
- 完成後 commit／push（權限允許時）

## 品質檢查
- [ ] 時間窗起訖日已寫入
- [ ] 基線版已標示（若適用）
- [ ] 每則發現 ≥2 來源且含 1 個 Tier 1
- [ ] 證據等級全部填寫
- [ ] 衝突已並列
- [ ] 八節完整
- [ ] snapshot 已驗證後覆寫
- [ ] commit message 符合格式
