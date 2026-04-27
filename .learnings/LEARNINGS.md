# Learnings

Corrections, insights, and knowledge gaps captured during development.

**Categories**: correction | insight | knowledge_gap | best_practice

---

## [LRN-20260427-001] best_practice

**Logged**: 2026-04-27T10:00:00Z
**Priority**: high
**Status**: promoted
**Promoted**: CLAUDE.md (Global Rules 第6条)
**Area**: config

### Summary
网络搜索失败时，应使用 opencli 替代 WebSearch/WebFetch

### Details
在 /learn 任务中，researcher subagent 使用 WebSearch 和 WebFetch 获取资料失败时返回 "API 错误"。用户指出此时应该使用 opencli 工具进行浏览器操作来获取网页内容。

具体场景：
- WebSearch 返回 "服务不可用 (API 错误)" 时
- WebFetch 无法获取需要动态加载的内容时
- 需要登录或交互式操作的页面时

应该使用的工具：
- `mcp__browsermcp__browser_navigate` - 导航到目标 URL
- `mcp__browsermcp__browser_snapshot` - 获取页面快照
- `mcp__browsermcp__browser_click` - 点击展开内容
- `mcp__browsermcp__browser_wait` - 等待动态内容加载

### Suggested Action
更新 CLAUDE.md 中 /learn 流程的 research 阶段说明，添加当 WebSearch/WebFetch 失败时的 fallback 策略：调用 opencli-browser 进行 ad-hoc 浏览器操作

### Metadata
- Source: user_feedback
- Tags: network-fallback, opencli, browser-tool
- See Also: LRN-20250115-001 (if related to existing entry)
- Pattern-Key: network-fallback.opencli

---
