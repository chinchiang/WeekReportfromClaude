---
description: "Four-track retrieval plan, priority URLs, fallbacks, and per-track self-check. Read before spawning A/B/C/D subagents."
connections: [evidence, snapshot-schema]
---

# 四軌檢索

每軌 ≥3 次獨立查詢。順序：Tier 1 → 後備 → 檢核種子標的。

觀測窗內無原始發布日的內容**不得**當本期發現。

## A 軌 — 模型發布與能力變更

**優先（Tier 1）**

| 標的 | URL／位置 |
|---|---|
| Anthropic | https://www.anthropic.com/news |
| OpenAI | https://openai.com/news |
| Google DeepMind | https://deepmind.google/discover/blog |
| Meta AI | https://ai.meta.com/blog |
| Mistral | https://mistral.ai/news |
| xAI | https://x.ai/news |
| 各家 docs | models / pricing / deprecations / changelog |
| AWS Bedrock | https://aws.amazon.com/about-aws/whats-new |
| Azure | Azure AI Foundry / Model catalog |
| Google Cloud | Vertex AI Model Garden |

**後備**：Hugging Face、Artificial Analysis、LMSYS Arena（標 Tier 2／3）。

**至少覆蓋**：Claude、GPT、Gemini、Grok、Llama、Mistral 的版本字串、context、pricing、deprecation。

## B 軌 — AI 資安能力與計畫

**優先**

| 標的 | URL／位置 |
|---|---|
| Project Glasswing | https://www.anthropic.com/project/glasswing |
| Frontier Red Team | https://red.anthropic.com |
| OpenAI 資安發布 | openai.com/news 與 security 相關頁 |
| Google Project Zero / Big Sleep | projectzero.google、Google Cloud security blog |
| 夥伴技術部落格 | Cloudflare、CrowdStrike、Palo Alto Networks |
| 主管機關 | CISA 與各國對 AI 資安能力之公告 |

**後備**：獨立安全研究報告（Tier 2／3）。

**至少覆蓋**：Glasswing 狀態與夥伴數、Mythos／相關 gated model 可用性、Big Sleep 公開進展。

## C 軌 — 企業導入與供應條件

**優先**：各家 enterprise／security 頁、DPA、資料留存條款、region 可用性、出口管制與地緣導致的存取變更（官方公告）。

**後備**：SEC filing、官方 status page。

**至少覆蓋**：區域可用性、資料留存／訓練用途條款、出口管制存取限制。

## D 軌 — 監理與標準連動

**僅取與模型能力、可用性或資安能力直接相關者。**

**優先**：官方監理機關、標準組織。  
**後備**：具編輯審查的法規分析（Tier 2）。

邊界：EU AI Act 模型風險分類更新、出口管制對特定模型的存取限制 → 納入。完整法遵週報（CRA／NIS2 全貌）→ **排除**（那是另一個週報模組）。

## Subagent 回傳格式

每則發現：

```yaml
id: <target-id or new-id>
track: A|B|C|D
item: <短名>
prev: <上期狀態或「無／基線」>
curr: <本期狀態>
published: YYYY-MM-DD
sources:
  - {tier: 1, org: "", title: "", url: "", date: YYYY-MM-DD}
evidence_suggested: 已證實|廠商主張|第三方評論|尚未證實
notes: <衝突或查無>
```

無變更：`status: 本期無變更`，附「已查 URL 清單」。
