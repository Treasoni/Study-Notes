# cdx02 结构映射表（stale map）

> 笔记 ID：cdx02
> 原路径：`AI学习/Codex/02 config.toml 核心配置.md`
> 新路径：`AI学习/Codex/02-基础功能/config.toml 核心配置.md`
> 重构日期：2026-08-10

## 结构映射（旧 → 新）

| 旧结构（原书章式） | 新结构（Claude Code 教程模板） |
|------|------|
| frontmatter：`title="Codex 完整配置体系"`，`tags=[codex, claude-code, configuration]`，`updated=2026-07-31`，`status=completed` | frontmatter：`title="config.toml 核心配置"`，`tags=[codex, ai, 工具使用, 基础功能, 配置]`，`updated=2026-08-10`，`status=updated`（`created`、`source_project` 不变） |
| H1「第二章：核心配置 —— config.toml 全面解读」+ 章节导语段落 | H1「config.toml 核心配置」+ `> [!info] 文档定位` 一句话定位（导语内容并入） |
| `### 1. 五层优先级回顾与合并机制` | `## 配置合并与优先级` |
| `#### 1.1 优先级总览` | `### 优先级总览` |
| `#### 1.2 合并规则` | `### 合并规则` |
| `#### 1.3 三组互斥配置区块` | `### 三组互斥配置区块` |
| `### 2. 安全限定：哪些键只能在用户级设置？` | `## 安全限定：用户级专属键` |
| `### 3. sandbox_mode 沙箱模式` | `## 沙箱模式 sandbox_mode` |
| `### 4. approval_policy 审批策略` | `## 审批策略 approval_policy` |
| `### 5. Permissions 新一代权限系统` | `## Permissions 新一代权限系统` |
| `### 6. Profiles 多环境配置档` | `## Profiles 多环境配置档` |
| `### 7. Model 配置与多提供商` | `## 模型配置与多提供商` |
| `### 8. Features 功能开关` | `## Features 功能开关` |
| `### 9. Shell 环境策略与项目信任` | `## Shell 环境策略与项目信任` |
| `### 10. 完整配置示例` | `## 完整配置示例` |
| `> **本章小结**`（普通引用） | `> [!summary] 本章小结`（Callout） |
| 无 | `## 常见问题`（3 条 Q&A，新增） |
| 无 | `## 最佳实践`（Do's / Don'ts，新增） |
| 无 | `## 小结`（新增） |
| `> [!note] 导航` + `[[01 配置哲学概览|← 上一章]]` / `[[03 AGENTS.md 分层体系|下一章 →]]`（旧书章导航） | `## 相关文档` wikilink 表格（替换） |
| 无 | `## 参考资料`（官方链接，新增） |
| 无 | `## 更新记录`（新增） |

## 内容变更

### 保留（未删改）
- 全部 9 个 toml/bash 代码块（优先级合并示例、用户级专属键、sandbox 子区块、approval 粒度、permissions 配置、profiles、模型配置、features、完整配置示例）
- 全部表格：五层优先级、沙箱模式、审批策略、内置配置档速查、Codex vs Claude Code、Shell 环境策略
- 全部 callout/警示：Claude Code 对照、陷阱警示、实战建议、危险组合、profiles 最佳实践、本章小结
- 全部技术结论与数值（gpt-5.4 / gpt-5.4-mini、`network_access = true`、`inherit = "core"` 等）

### 新增
- `> [!info] 文档定位` 一句话定位
- `## 常见问题`（3 条：项目级 sandbox_mode 不生效 / sandbox 与 approval 区别 / workspace-write 装不上依赖）
- `## 最佳实践`（Do's 6 条、Don'ts 4 条）
- `## 小结` 总结段落
- `## 相关文档` 表格（4 个 wikilink，含返回目录）
- `## 参考资料`（2 个官方链接）
- `## 更新记录`

### 移除 / 重命名
- 移除旧书章式 `> [!note] 导航` 区块与 `[[xx|← 上一章]]` / `[[xx|下一章 →]]` 导航（改为相关文档表格）
- 移除章节导语第一句「第一章我们建立了 Codex 配置体系的整体地图…」（并入文档定位）
- 移除 frontmatter 旧 tag `claude-code`、`configuration`（改为 `ai`、`基础功能`、`配置`）
- 所有编号标题 `### N.` / `#### N.M` 重命名为无编号的 `##` / `###` 描述性标题
- 文件名从 `02 config.toml 核心配置.md` 移入 `02-基础功能/` 子目录并去序号改名 `config.toml 核心配置.md`
