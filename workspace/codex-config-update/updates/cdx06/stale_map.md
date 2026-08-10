# cdx06 结构映射：Hooks 与插件

## 结构映射表（旧结构 → 新结构）

| 旧结构（来源） | 新结构（目标） | 变更类型 |
|------|------|------|
| `title: "Codex 完整配置体系"` | `title: Hooks 与插件` | renamed |
| `tags: [codex, claude-code, configuration]` | `tags: [codex, ai, 工具使用, 进阶应用, hooks]` | renamed |
| `updated: 2026-07-31` / `status: completed` | `updated: 2026-08-10` / `status: updated` | renamed |
| `# 第六章：Hooks 生命周期钩子与插件体系` | `# Hooks 与插件` | renamed |
| （无） | `> [!info] 文档定位`（紧随 H1） | added |
| `### Part 1：Hooks 生命周期钩子系统` | `## Hooks 生命周期钩子系统` | renamed（层级 3→2） |
| `#### 1.1 配置文件与合并规则` | `### 配置文件与合并规则` | renamed（编号去除） |
| `#### 1.2 11 种事件类型详解` | `### 11 种事件类型详解` | renamed（编号去除） |
| `#### 1.3 PreToolUse 重写输入示例` | `### PreToolUse 重写输入示例` | renamed（编号去除） |
| `#### 1.4 退出码约定` | `### 退出码约定` | renamed（编号去除） |
| `#### 1.5 启用与安全管理` | `### 启用与安全管理` | renamed（编号去除） |
| `#### 1.6 Codex Hooks vs Claude Code Hooks 对比` | `### Codex Hooks vs Claude Code Hooks 对比` | renamed（编号去除） |
| `### Part 2：插件体系` | `## 插件体系` | renamed（层级 3→2） |
| （Part 2 无子节标题） | `### 插件目录结构` / `### 插件清单 plugin.json` / `### 插件 vs MCP 扩展对比` | added |
| `> [!note] 导航`（`[[05 ...|← 上一章]] \| [[07 ...|下一章 →]]`） | `## 相关文档` 表格 | removed → replaced |
| （无） | `## 常见问题` | added |
| （无） | `## 最佳实践`（Do's / Don'ts） | added |
| `> **本章小结**` | `## 小结` 中的 `> [!note] 本章小结` | renamed（独立段落 → 小节内 Callout） |
| （无） | `## 相关文档` | added |
| （无） | `## 参考资料` | added |
| （无） | `## 更新记录` | added |

## 内容保留说明

- **代码块全部保留**：`hooks.json` JSON、内联 `config.toml`、PreToolUse 重写 Python 示例、`/hooks` 管理命令 bash、插件目录结构 `text`、`plugin.json`。
- **表格全部保留**：11 种事件类型、退出码约定、Codex vs Claude Code 对比、插件 vs MCP 扩展对比。
- **Callout 全部保留**：插件 `> **决策指南**`、`> **本章小结**`。
- **删除项**：旧的书本式导航块（`> [!note] 导航` / `上一章` / `下一章`），仅移除章节交叉引用文字，未删除技术内容。

## 命名对照（wikilink 目标）

| 参数文档 | 指向文件 |
|------|------|
| `[[Agents 与 MCP]]` | `05 Agents 与 MCP.md`（原 05 章） |
| `[[Codex CLI 与调试]]` | `07 CLI 与调试.md`（原 07 章） |
| `[[对照表与迁移实战]]` | `08 对照表与迁移实战.md`（原 08 章） |
| `[[Codex MOC]]` | `Codex 配置体系 MOC.md` |
