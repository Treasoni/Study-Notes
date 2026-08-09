# 更新计划 — cc12 「Claude Code 高级功能」

> note_id: cc12
> 策略：局部 patch，保留原结构与写作风格；不重写未过时段落。

## 过时点与更新计划

### 1. 模型（依据 SB-01、SB-02）
- **现状问题**：模型支持表缺 Opus 5，Sonnet 5 未标注为默认；Configuration 环境变量仍写 `claude-opus-4-8`。
- **计划**：
  - Extended Thinking「模型支持」表新增 `Opus 5`（默认 Opus，1M 上下文）行、`Sonnet 5` 标注「默认模型」，其余行保留。
  - 表前新增 `[!note] 默认模型（2026-08）` callout：Sonnet 5 默认（1M 上下文，促销至 2026-08-31）、Opus 5（`claude-opus-5`）默认 Opus、Bedrock/Vertex/AWS 默认 Opus 4.8。
  - 环境变量改为 `ANTHROPIC_MODEL=claude-sonnet-5`、`ANTHROPIC_DEFAULT_OPUS_MODEL=claude-opus-5`。

### 2. Auto Mode（依据 SB-03、SB-14）
- **现状问题**：正式发布 callout 未提第三方平台免 opt-in；默认阻止表缺 transcript 与灾难性删除保护；缺 AskUserQuestion 行为。
- **计划**：
  - 更新正式发布 callout：Bedrock/Vertex/Foundry 无需 opt-in（不再需要 `CLAUDE_CODE_ENABLE_AUTO_MODE`，可用 `disableAutoMode` 关闭）。
  - 默认阻止操作表新增两行：篡改会话 transcript；命令替换 `$(…)`/反引号/`<(…)` 中的灾难性删除（即使 `--dangerously-skip-permissions` 也会提示）。
  - 新增 `[!warning]` callout：AskUserQuestion 对话框默认不再自动继续（可在 `/config` 设置 idle timeout）。

### 3. Subagents（依据 SB-06、SB-07、SB-05）— 新增节
- 原文无独立 Subagents 节（仅 Mermaid 图与 Dynamic Workflows 对比表提及）。
- **计划**：在 Dynamic Workflows 后新增「## Subagents（子代理）」：默认后台运行；并发上限默认 20（`CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS`）；嵌套深度默认 3（`CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH=1` 禁用）；`/subtask` 取代旧 in-session 子代理；`/tasks` 保留已完成后台代理；`--forward-subagent-text` 透传；worktree 隔离子代理不能对主 checkout 执行破坏性 git 命令（含 `git -C`/`--git-dir` 重定向）。附 `[!tip] 大白话`。

### 4. 沙盒（依据 SB-13）
- **现状问题**：Sandboxing 配置示例缺 `sandbox.filesystem.disabled` 与凭据 mask。
- **计划**：配置示例新增 `filesystem.disabled`（跳过文件系统隔离但保留网络出口控制）与 `credentialMasking.mode: "mask"`，并加一句说明。

### 5. 无障碍（依据 SB-15）— 新增节
- 原文无无障碍内容。
- **计划**：在 Voice Dictation 后新增「## 无障碍（Screen Reader）」：`claude --ax-screen-reader` / `CLAUDE_AX_SCREEN_READER=1` / `axScreenReader`；界面转线性纯文本供 VoiceOver/NVDA；支持删除操作播报。附 `[!tip] 大白话`。

### 6. 桌面端（依据 SB-14）
- **现状问题**：Desktop App 核心功能表缺内置浏览器。
- **计划**：新增一行「内置浏览器 — 沙盒化内置浏览器，外部站点有安全分类器」。

### 7. /fork（依据 SB-08）— 新增节
- 原文无 `/fork`。
- **计划**：在 Scheduled Tasks 后新增「## Session Management（会话管理）」小节：`/fork` 复制对话到新后台会话。

### 8. 其它过时点核对（依据 SB-04）
- Permission Modes 表中 `default` 权限模式已改名 `manual`（SB-04，v2.1.200）。
- **计划**：权限模式表、使用场景表、最佳实践、完整配置示例中的 `default` 模式值改为 `manual`（`defaultMode` 配置键名本身不变）。

### 9. Mermaid 图
- **计划**：`E` 分组下新增 `E6[Accessibility]`；`D1[Session Management]`、`F2[Subagents]` 已存在，与新增节对应。

### 10. 元数据与更新记录
- frontmatter `updated: 2026-08-10`；文末追加「## 更新记录」表。

## 不处理项（明确排除）
- `--enable-auto-mode` 启动方式保留（来源库未显示其移除）。
- 未按 SB-12 给 Managed Settings 加 `disableAutoMode`（SB-12 不在本笔记适用清单；避免越界）。
