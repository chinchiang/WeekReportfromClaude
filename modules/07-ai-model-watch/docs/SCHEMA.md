# 模組 07 輸出 Schema

```jsonc
{
  "module": "07",
  "week": "2026-W35",                       // ISO 週別，由呼叫端提供
  "period": { "start": "2026-08-24", "end": "2026-08-31" },
  "mode": "delta",                          // "baseline" | "delta"

  "exec_summary": "…",                      // ≤400 字，非技術讀者可讀

  "tracks": {
    "A": { "name": "模型發布與能力變更", "status": "changed",   "note": "…" },
    "B": { "name": "AI 資安能力與相關計畫", "status": "unchanged", "note": "本期無變更。" },
    "C": { "name": "企業導入與供應條件變更", "status": "changed",   "note": "…" },
    "D": { "name": "監理與標準連動",     "status": "failed",    "note": "檢索失敗：…" }
  },
  // status: "changed" | "unchanged" | "baseline" | "failed"

  "entries": [
    {
      "id": "m07-2026W35-01",
      "track": "B",                          // "A" | "B" | "C" | "D"
      "target": "glasswing-findings",        // 對應 snapshot_targets[].id，跨期時間軸靠這個串起來
      "title": "…",
      "prev_state": "…",                     // 基線期填「—（基線）」
      "curr_state": "…",
      "evidence": "verified",                // verified | vendor | thirdparty | unverified
      "priority": "P0",                      // P0 | P1 | P2 | P3
      "detail": "…",
      "impact": ["PSIRT", "SBOM"],           // 工作項層級，不含 BG 層級曝險
      "sources": [
        { "org": "Anthropic", "title": "…", "url": "https://…",
          "date": "2026-08-27", "tier": 1 }  // tier: 1 | 2 | 3，date 為原始發布日
      ]
    }
  ],

  "counter_views": [                         // 至少 2 則，必填
    { "point": "…",
      "source": { "org": "…", "title": "…", "url": "https://…", "date": "…", "tier": 2 } }
  ],

  "snapshot_targets": [                      // 覆寫 data/snapshot.yaml，供下期 Delta
    { "id": "anthropic-frontier-tier",
      "label": "Anthropic 前沿模型世代",
      "state": "…",
      "evidence": "已證實",
      "source_date": "2026-08-27" }
  ]
}
```

## 驗證器會擋下來的情況

`scripts/generate_week.py` 的 `validate()` 在寫檔前執行，任一項不通過就不寫入任何檔案
（被拒的輸出存為 `rejected.json`）：

- `evidence`、`priority`、`track`、`tracks.*.status` 使用了不在列舉內的值，或缺漏
- `entries[]` 缺少 `id` / `title` / `prev_state` / `curr_state` / `detail`
- `entries[].id` 在同一期內重複
- 任一 entry 沒有來源，或來源 `tier` 不是 1／2／3
- **任一來源缺少 `org` / `title` / `url` / `date`**（來源必須可回溯，不接受空殼）
- **標為 `verified` 但來源少於 2 筆，或沒有任何 Tier 1 來源**
- `counter_views` 少於 2 則，或任一則缺 `point`、缺 `source`、
  來源缺 `org` / `title` / `date`、來源 `tier` 不是 1／2／3
- `exec_summary` 不是字串，或超過 700 字（規格為 400 字，留緩衝）
- 四軌任一軌缺漏

這些不是格式潔癖。分級紀律如果不在寫入前強制，一年後的檔案就沒有稽核價值 ——
「已證實」這個標籤必須真的代表兩個來源、其中一個是一手文件。來源欄位一併強制，
是因為「2 筆來源含 Tier 1」若允許空殼填充，等於留了一條繞過分級的形式路徑。

兩個刻意的例外：

- `counter_views[].source.url` 不強制。內部方法論引用（例如來源 `org` 為
  「模組 07 規格」的那類）本來就沒有外部連結，強制 URL 會逼出假連結。
  entry 的來源則四項全要 —— 那是對外主張，必須可查。
- 日期只驗非空，不驗格式。查證中的來源允許寫「發布日待覆核」這類標記，
  比逼模型填一個假的 ISO 日期誠實。

## `target` 欄位為什麼重要

`entries[].target` 必須對應 `snapshot_targets[].id`。跨期查詢頁（`archive.html`）
就是靠這個欄位把同一個追蹤標的在一年內的狀態變化串成時間軸。
留空不會讓驗證失敗，但該則會被歸入「未標記標的」，一年後查不到它的演變。
新出現的標的請同時加進 `snapshot_targets`，並沿用既有 id 命名（kebab-case）。
