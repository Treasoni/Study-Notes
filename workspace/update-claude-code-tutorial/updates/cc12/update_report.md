# 更新报告 — cc12 「Claude Code 高级功能」

> 更新日期：2026-08-10
> 目标版本：v2.1.193 ~ v2.1.226（截至 2026-08-10）

## 更新摘要

本篇为「高级功能」总览笔记，采用局部 patch 方式更新到 2026-08 现状，未重写未过时段落。

**主要变更：**

1. **模型**（SB-01、SB-02）
   - Extended Thinking「模型支持」表新增 `Opus 5`（默认 Opus，1M 上下文），`Sonnet 5` 标注「默认模型」。
   - 新增 `[!note] 默认模型（2026-08）` callout：Sonnet 5 默认（1M 上下文，促销至 2026-08-31）、Opus 5 默认 Opus、Bedrock/Vertex/AWS 默认 Opus 4.8。
   - 环境变量 `ANTHROPIC_MODEL=claude-sonnet-5`、`ANTHROPIC_DEFAULT_OPUS_MODEL=claude-opus-5`（原为 `claude-opus-4-8`）。

2. **Auto Mode**（SB-03、SB-14）
   - 「正式发布」callout 补充：第三方平台（Bedrock/Vertex/Foundry）无需 opt-in（不再需要 `CLAUDE_CODE_ENABLE_AUTO_MODE`，可用 `disableAutoMode` 关闭）。
   - 「默认阻止的操作」表新增两行：篡改会话 transcript；命令替换 `$(…)`/反引号/`<(…)` 中的灾难性删除（即使 `--dangerously-skip-permissions` 也会提示）。
   - 新增 `[!warning]` callout：AskUserQuestion 对话框默认不再自动继续（可在 `/config` 设置 idle timeout）。

3. **新增章节**
   - 「Session Management（会话管理）」：`/fork` 复制对话到新后台会话（SB-08）。
   - 「Subagents（子代理）」：默认后台运行、并发上限默认 20、嵌套深度默认 3（`CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH=1` 禁用）、`/subtask` 取代旧 in-session 子代理、`/tasks` 保留已完成后台代理、`--forward-subagent-text` 透传、worktree 隔离子代理不能对主 checkout 执行破坏性 git 命令（SB-06、SB-07、SB-05）。
   - 「Accessibility（无障碍）」：`claude --ax-screen-reader` / `CLAUDE_AX_SCREEN_READER=1` / `axScreenReader`（SB-15）。
   - 均为原写作风格：一句话定义 callout + 代码示例 + `[!tip] 大白话`。

4. **沙盒**（SB-13）：配置示例新增 `sandbox.filesystem.disabled`（跳过文件系统隔离但保留网络出口控制）与 `credentialMasking.mode: "mask"`（凭据 mask 模式）。

5. **桌面端**（SB-14）：Desktop App 核心功能表新增「内置浏览器 — 沙盒化内置浏览器，外部站点有安全分类器」。

6. **权限模式**（SB-04，补充核对）：权限模式 `default` → `manual`（权限模式表、使用场景表、最佳实践、完整配置示例；`defaultMode` 配置键名不变）。

7. **Mermaid 图**：`E` 分组新增 `E6[Accessibility]`。

8. **元数据**：frontmatter `updated: 2026-08-10`；文末追加「## 更新记录」。

## 引用来源

| 来源 ID | 内容 | 来源 |
|---------|------|------|
| SB-01 | Claude Sonnet 5 默认（1M 上下文，促销至 2026-08-31） | code.claude.com changelog v2.1.197 |
| SB-02 | Claude Opus 5 默认 Opus（`claude-opus-5`，1M 上下文） | code.claude.com changelog v2.1.219 |
| SB-03 | Bedrock/Vertex/AWS 默认 Opus 4.8；Auto mode 第三方平台免 opt-in | classmethod / changelog v2.1.207 |
| SB-05 | `--ax-screen-reader`、`--forward-subagent-text`、`CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS`、`CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH=1` | changelog v2.1.208–v2.1.223 |
| SB-06 | Subagents 默认后台、并发 20、嵌套 3、`/subtask` | changelog v2.1.198/217/219 |
| SB-07 | worktree 隔离子代理不能对主 checkout 执行破坏性 git 命令 | changelog v2.1.216/222/225 |
| SB-08 | `/fork` 复制对话到新后台会话 | changelog v2.1.212 |
| SB-13 | 沙盒 `mode: "mask"`、credential-masking 增强 | changelog v2.1.216/221/224 |
| SB-14 | Auto mode transcript 保护、灾难性删除提示、AskUserQuestion、桌面内置浏览器 | whats-new 2026-w28 |
| SB-15 | 屏幕阅读器模式 | changelog v2.1.208 |
| SB-04* | 权限模式 default→manual | changelog v2.1.200 |

\* SB-04 不在任务给定适用清单（SB-01/02/03/05/06/07/14/15）内，属「核对其它过时点一并修正」时补充引用。

## 未处理风险

1. **`--enable-auto-mode` 保留**：Auto Mode 启用方式 1 仍保留 `claude --enable-auto-mode`。来源库未显示该标志被移除，但既然 Auto mode 已 GA 且第三方免 opt-in，该标志是否仍为必要解锁方式存在不确定性，建议发布前对照 code.claude.com 现行文档确认。
2. **`credentialMasking.mode: "mask"` 配置路径**：SB-13 确认存在 `mode: "mask"`，但未给出完整配置键路径；`sandbox.credentialMasking` 为推断路径，若与现行 schema 不符需按 docs 微调。
3. **SB-04 越界引用**：`default`→`manual` 依据 SB-04（不在本笔记适用清单）。若编排方希望 cc12 保留 `default` 旧名描述，可撤销该处修改。
4. **Opus 4.6/4.7 行保留**：模型支持表中 `Opus 4.6/4.7` 行按原文保留，未在来源库中单独核验其 effort 级别细节。
5. **Mermaid 图未加 `D5`/`/fork` 节点**：`/fork` 归入已有 `D1[Session Management]`，未单独加节点，避免图过密。

## 审阅建议

- **需要 needs-review：是**。理由：
  - `credentialMasking` 配置路径为推断值，需对照 docs 确认。
  - `default`→`manual` 属任务清单外补充，需编排方/用户确认接受。
  - 新增 3 个章节（Subagents / Accessibility / Session Management）属结构性新增，建议用户审阅后写回。
