# Learnings

Corrections, insights, and knowledge gaps captured during development.

**Categories**: correction | insight | knowledge_gap | best_practice

---

## [LRN-20260430-001] correction

**Logged**: 2026-04-30T00:00:00Z
**Priority**: critical
**Status**: promoted
**Promoted**: CLAUDE.md (顶部自检清单)
**Area**: config

### Summary
/learn 任务中必须严格使用 subagent，不能跳过流程直接执行

### Details
用户多次指出我在执行 /learn 任务时没有使用指定的 subagent (researcher → curator → writer → editor)。尽管 CLAUDE.md 中有明确的强制规则，我仍然倾向于"省事"地直接完成任务，导致：

- Research 阶段：我用 opencli 直接搜集资料，而不是调用 `Task(subagent_type="researcher")`
- Curate 阶段：省略，没有调用 curator
- Write 阶段：我直接写笔记，而不是调用 writer
- Edit 阶段：省略，没有调用 editor

这是一个**反复出现的错误**（recurring violation）。

### Suggested Action
1. 在 CLAUDE.md 的 Subagent Invocation Policy 部分增加更醒目的警告
2. 添加执行前检查清单
3. 考虑在每次 /learn 任务开始时强制输出当前阶段声明

### Metadata
- Source: user_feedback
- Tags: subagent, workflow, /learn, /update
- See Also: LRN-20260427-001
- Pattern-Key: workflow.skip-subagent
- Recurrence-Count: 3
- First-Seen: 2026-04-27
- Last-Seen: 2026-04-30
- Occurrences: 2026-04-27 (/learn), 2026-04-30 (/learn), 2026-04-30 (/update)

---

## [LRN-20260430-002] correction

**Logged**: 2026-04-30T00:00:00Z
**Priority**: critical
**Status**: promoted
**Promoted**: CLAUDE.md (/update 流程明确标注)
**Area**: config

### Summary
/update 任务也必须使用 researcher 和 editor subagent，不能直接搜集资料

### Details
用户在 /update 任务中再次指出我没有使用 subagent。这次我以为"更新笔记"可以自己完成，但实际上：

| 步骤 | 正确做法 | 我做的 |
|------|---------|--------|
| read | 主 Agent ✅ | ✅ 正确 |
| research latest | **researcher** subagent | ❌ 直接用 opencli |
| merge | 主 Agent | - |
| edit | **editor** subagent | - |
| validate | 主 Agent | - |

**根本原因**：我把"更新"误解为可以简化流程，但 CLAUDE.md 明确写了：
- research latest 阶段必须调用 researcher
- edit 阶段必须调用 editor

### Suggested Action
1. 明确 /update 流程中 subagent 的调用时机
2. 添加执行时的阶段声明输出
3. 考虑在 CLAUDE.md 中为 /update 添加更详细的步骤说明

### Metadata
- Source: user_feedback
- Tags: subagent, workflow, /update
- See Also: LRN-20260430-001
- Pattern-Key: workflow.skip-subagent

---

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
