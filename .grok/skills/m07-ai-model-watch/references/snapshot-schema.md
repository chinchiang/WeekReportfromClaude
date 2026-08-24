---
description: "latest-snapshot.yaml contract, seed tracking targets, id naming, and validation. Read in step 1 and before overwriting the snapshot in step 5."
connections: [tracks, evidence]
---

# Snapshot 契約

路徑：`{MODULE07_PATH}/latest-snapshot.yaml`  
預設 MODULE07_PATH = `modules/07-ai-model-watch`

**報告完成並通過** `scripts/validate_snapshot.py` **之後才覆寫。**

## 格式

```yaml
module: 07
period_end: YYYY-MM-DD
targets:
  - id: model-claude-flagship
    state: <當前狀態值，單行字串>
    evidence: 證實|廠商主張|第三方評論|未證實
    source_date: YYYY-MM-DD
```

- `id`：小寫字母、數字、連字號；建議前綴 `model-` / `security-` / `enterprise-` / `reg-`
- `state`：可 diff 的具體值（版本字串、價格、夥伴數、region 清單），禁止空泛「有更新」
- `evidence`：四選一，對應報告標籤（無書名號）
- `source_date`：該狀態所依據文件的原始發布日
- 上期有、本期查無公開資料：保留 id，`state` 寫 `查無公開資料（上期：…）`，`evidence: 未證實`

## 種子標的（首期或 snapshot 缺失時建立，之後以檔案為準）

| id | 追蹤內容 |
|---|---|
| model-claude-flagship | Claude 旗艦版本／能力／定價 |
| model-gpt-flagship | GPT 旗艦版本／能力／定價 |
| model-gemini-flagship | Gemini 旗艦版本／能力／定價 |
| model-grok-flagship | Grok 旗艦版本／能力／定價 |
| model-llama-flagship | Llama 旗艦版本 |
| model-mistral-flagship | Mistral 旗艦版本 |
| model-bedrock-catalog | Bedrock 重大上架／下架／定價 |
| model-vertex-garden | Vertex Model Garden 重大變更 |
| model-azure-foundry | Azure AI Foundry 重大變更 |
| security-glasswing | Project Glasswing 階段與夥伴數 |
| security-red-anthropic | red.anthropic.com 公開進展 |
| security-big-sleep | Google Big Sleep／Project Zero AI 漏洞研究公開進展 |
| enterprise-dpa-retention | 主要供應商 DPA／資料留存／訓練用途條款 |
| enterprise-region-access | 區域可用性與出口管制存取限制 |
| reg-model-capability | 與模型能力直接相關的監理／標準 |

本期新增／移除必須在報告列出。新增 id 遵循前綴。不得刪除上期 id，除非報告宣告「暫停追蹤」並將 state 標為 `暫停追蹤`。
