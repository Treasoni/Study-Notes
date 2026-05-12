2026 年，AI 產業出現一個新共識：決定 AI 產品好壞的，不再是模型本身，而是模型外面那層叫做「harness」的東西。當 Claude Code、Cursor、OpenClaw 使用的底層模型越來越接近時，真正拉開產品差距的，是 harness 的設計。Martin Fowler 的技術部落格、Anthropic 產品負責人 [trq212](https://x.com/trq212/status/2042318547519762678) 、以及 Andrej Karpathy 的 [近期發言](https://abmedia.io/karpathy-ai-capability-perception-gap-free-vs-frontier-agents) ，都指向同一個方向：AI 的下一個戰場是 Harness Engineering。

## 什麼是 Agent Harness

一個 AI agent 可以拆成兩部分：模型（Model）和 Harness。模型是大腦，負責理解語言和推理。Harness 是模型以外的一切 — 工具呼叫、記憶管理、上下文組裝、狀態持久化、錯誤處理、安全護欄、任務排程、生命週期管理。

用一個直觀的比喻：LLM 是一匹馬，harness 是馬具 — 韁繩、馬鞍、與馬車的連接結構。沒有馬具，馬再強壯也拉不動車。AI agent 也一樣，模型再聰明，沒有好的 harness 就無法可靠地完成實際任務。

Akshay Pachaar 在一則廣為流傳的 [推文](https://x.com/akshay_pachaar/status/2041433526189633928) 中提出了另一個比喻：「裸 LLM 就像沒有作業系統的 CPU — 它能計算，但靠自己做不了任何有用的事。」Harness 就是那個作業系統。

## 為什麼 2026 年 Harness Engineering 突然變重要

原因有三：

第一，模型能力趨於同質化。GPT-5.4、Claude Opus 4.6、Gemini 3.1 Pro 在多數基準測試上的差距已經縮小到個位數百分點。當模型不再是瓶頸，產品差異化自然轉移到 harness 層。

第二，agent 從實驗進入生產。2025 年的 agent 大多是 demo，2026 年的 agent 要跑在企業環境裡 — 需要處理中斷恢復、長時間運行、多步驟任務、權限控制。這些全是 harness 的工作。

第三，LLM 天生無狀態。每次新的 session 都從零開始，模型不記得上一次對話。Harness 負責把記憶、上下文、工作進度持久化，讓 agent 能像一個真正的「同事」一樣持續工作。

## Harness 的核心組件

一個完整的 agent harness 通常包含以下幾層：

| 組件 | 功能 | 類比 |
| --- | --- | --- |
| Orchestration Loop | 控制 agent 的「思考 → 行動 → 觀察」循環 | 作業系統的主循環 |
| Tool Management | 管理 agent 可以使用的工具（檔案讀寫、API 呼叫、瀏覽器操作等） | 驅動程式 |
| Context Engineering | 決定每次呼叫模型時送入哪些資訊、裁切哪些資訊 | 記憶體管理 |
| State Persistence | 保存工作進度、對話歷史、中間結果 | 硬碟 |
| Error Recovery | 偵測失敗並自動重試或回退 | 例外處理 |
| Safety Guardrails | 限制 agent 的行為範圍，防止危險操作 | 防火牆 |
| Verification Loops | 讓 agent 自我檢查輸出品質 | 單元測試 |

## 三層工程學：Prompt、Context、Harness

圍繞 LLM 的工程實踐可以分為三個同心圓層次：

最內層是 Prompt Engineering — 設計送給模型的指令，決定模型「怎麼想」。這是 2023 年的主流技能。

中間層是 Context Engineering — 管理模型「看到什麼」。決定哪些資訊在什麼時機送入 context window，哪些該裁切。隨著 context window 擴大到百萬 token，這層的重要性在 2025 年開始浮現。

最外層是 Harness Engineering — 涵蓋前兩者，再加上整個應用基礎設施：工具編排、狀態持久化、錯誤恢復、驗證循環、安全機制、生命週期管理。這是 2026 年的核心戰場。

## 實例：為什麼同一個模型在不同產品裡表現天差地遠

Claude Opus 4.6 在 [Claude Code](https://abmedia.io/claude-ai-complete-guide-2026) 裡可以花一小時重構整個程式碼庫。但把同一個模型透過 API 接上一個簡陋的 harness，它可能連跨檔案的 bug 修復都做不好。差別不在模型，在 harness。

Claude Code 的 harness 做了什麼？

- 自動搜尋整個程式碼庫找到相關檔案，而非要求用戶一一指定
- 在修改前先讀取檔案內容，修改後執行測試驗證
- 遇到測試失敗會自動分析錯誤並重試
- 透過 [MCP](https://abmedia.io/mcp-model-context-protocol-complete-guide-2026) 連接外部工具（GitHub、資料庫等）
- 記憶系統跨 session 保存使用者偏好與專案脈絡
- [Advisor 策略](https://abmedia.io/anthropic-advisor-strategy-opus-sonnet-haiku-cost-saving) 讓不同能力的模型分工合作

這些全是 harness 的功勞。

## Feedforward 與 Feedback：Harness 的兩大控制模式

根據 [Martin Fowler 技術部落格](https://martinfowler.com/articles/exploring-gen-ai/harness-engineering.html) 的分析，harness 的控制機制分為兩類：

Feedforward（前饋控制）— 在 agent 行動前就設好規則，預防不想要的輸出。例如：system prompt 中的行為準則、工具白名單、檔案存取權限。

Feedback（回饋控制）— 在 agent 行動後檢查結果，允許自我修正。例如：執行測試確認程式碼正確、比對輸出與預期格式、偵測幻覺並重新生成。

好的 harness 同時使用兩種控制，既限制行為範圍又保留靈活性。

## Harness Engineering 的產品化：Anthropic 怎麼做

Anthropic 在 2026 年 4 月密集推出的產品更新，幾乎都是 harness engineering 的產品化：

- [Managed Agents](https://abmedia.io/anthropic-claude-managed-agents-public-beta) — 把 harness 的基礎設施（沙箱、排程、狀態管理）做成託管服務，開發者只需定義 agent 行為
- [Advisor 策略](https://abmedia.io/anthropic-advisor-strategy-opus-sonnet-haiku-cost-saving) — harness 層級的模型混用架構，自動判斷何時該諮詢更強的模型
- [Cowork 企業版](https://abmedia.io/claude-cowork-ga-enterprise-rbac-spend-limits) — 為非技術用戶提供完整的 harness（權限控制、支出管理、使用分析），讓他們不需要理解底層技術

Anthropic 產品負責人 trq212 的表述最為精準：「Prompting 是跟 agent 對話的技能，但它是被 harness 所中介的。我的核心目標是增大人類與 agent 之間的頻寬。」

## 對開發者的意義：新職業與新技能

Harness Engineering 正在成為一個獨立的工程領域。它需要的技能組合跟傳統後端工程或 ML 工程都不同：

- 理解 LLM 的能力邊界與失敗模式
- 設計可靠的工具呼叫與錯誤處理流程
- 管理 context window — 什麼時候塞入什麼資訊
- 建構可觀測性 — 追蹤 agent 的決策路徑與工具使用
- 安全設計 — 限制 agent 的行為範圍而不扼殺其能力

對於正在學習 [Vibe Coding](https://abmedia.io/vibe-coding-complete-guide-2026) 或使用 AI 工具開發的人來說，理解 harness 的概念將幫助你更有效地與 AI agent 協作 — 因為你會知道問題出在模型還是 harness，以及如何透過調整 harness 設定（而非反覆改 prompt）來改善結果。

## 結語：下一個十年的基礎設施之爭

AI 模型的競爭不會停止，但邊際收益正在遞減。Harness 層的競爭才剛開始 — 誰能建構最可靠、最靈活、最安全的 harness，誰就能把同樣的模型能力轉化為更好的產品體驗。

這也解釋了為什麼 Anthropic、OpenAI、Google 都在從「模型公司」轉型為「平台公司」— 他們賣的不再只是模型 API，而是完整的 harness 基礎設施。對開發者而言，理解 harness engineering 不是可選項，而是在 AI 時代建構產品的核心素養。

風險提示

加密貨幣投資具有高度風險，其價格可能波動劇烈，您可能損失全部本金。請謹慎評估風險。

[![鏈新聞](https://abmedia.io/wp-content/uploads/2026/04/732x200.jpg "鏈新聞")](https://www.bitget.com/zh-TC/markets/tradFi?channelCode=regd&vipCode=w4wm)