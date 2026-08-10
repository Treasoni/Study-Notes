# cdx05 结构对照表：05 Agents 与 MCP → Agents 与 MCP

> 源文件：`AI学习/Codex/05 Agents 与 MCP.md`
> 目标文件：`AI学习/Codex/03-进阶应用/Agents 与 MCP.md`

## 旧结构 → 新结构

| 旧结构（书章节风格） | 新结构（Claude Code 教程风格） | 处理方式 |
|------|------|------|
| `# 第五章：Agents 子代理与 MCP 服务配置` | `# Agents 与 MCP` | 重命名标题 |
| （无） | `> [!info] 文档定位` | 新增（紧随 H1 之后） |
| 前两段引言（Skills vs Agents 的引出、两种扩展机制介绍） | 文档定位下方正文引言 | 保留原文，去掉章回叙述，仅保留技术含义 |
| `### Part 1：Agents 子代理系统` | `## Agents 子代理系统` | 重编号为 `##` |
| `#### 1.1 配置路径与定义格式` | `### 配置路径与定义格式` | 重编号为 `###` |
| `#### 1.2 三种内置代理` | `### 三种内置代理` | 重编号为 `###` |
| `#### 1.3 全局代理设置` | `### 全局代理设置` | 重编号为 `###` |
| `#### 1.4 Codex Agents vs Claude Code Agents 对比` | `### Codex Agents vs Claude Code Agents 对比` | 重编号为 `###` |
| `> **一句话总结**：…`（内嵌引用块） | `> [!note] 一句话总结` | 格式化为 Callout，内容保留 |
| `### Part 2：MCP 服务配置` | `## MCP 服务配置` | 重编号为 `##` |
| `#### 2.1 配置位置` | `### 配置位置` | 重编号为 `###` |
| `#### 2.2 STDIO（本地进程）` | `### STDIO（本地进程）` | 重编号为 `###` |
| `#### 2.3 Streamable HTTP（远程 API）` | `### Streamable HTTP（远程 API）` | 重编号为 `###` |
| `#### 2.4 审批模式` | `### 审批模式` | 重编号为 `###` |
| `#### 2.5 工具白名单与黑名单` | `### 工具白名单与黑名单` | 重编号为 `###` |
| `#### 2.6 CLI 管理：codex mcp add` | `### CLI 管理：codex mcp add` | 重编号为 `###` |
| `#### 2.7 Codex MCP vs Claude Code MCP 对比` | `### Codex MCP vs Claude Code MCP 对比` | 重编号为 `###` |
| `> **本章小结**：…`（内嵌引用块） | `## 小结` | 从内嵌块提升为独立章节，正文保留 |
| （无） | `## 常见问题`（3 个 Q&A） | 新增（内容均源自原文：Agent vs Skill、审批模式选择、STDIO vs Streamable HTTP） |
| （无） | `## 最佳实践`（Do's / Don'ts） | 新增（从原文「审批模式」「工具白名单/黑名单」「STDIO/HTTP 传输」「全局代理设置」提炼） |
| （无） | `## 相关文档`（表格） | 新增（替换旧导航块） |
| （无） | `## 参考资料` | 新增（官方 Codex 链接） |
| （无） | `## 更新记录` | 新增 |

## 新增 / 删除 / 重命名清单

### 新增（结构性、非技术内容）
- `> [!info] 文档定位` Callout
- `## 常见问题`（3 个 Q&A）
- `## 最佳实践`（Do's / Don'ts）
- `## 相关文档` 表格
- `## 参考资料`
- `## 更新记录`

### 删除
- `> [!note] 导航` 块（`[[04 Skills 技能系统|← 上一章]] | [[06 Hooks 与插件|下一章 →]]`）
- 旧章号前缀（`第五章：`、`### Part N`、`#### N.M`）

### 重命名 / 移动
- 标题：`第五章：Agents 子代理与 MCP 服务配置` → `Agents 与 MCP`
- 位置：`AI学习/Codex/05 Agents 与 MCP.md` → `AI学习/Codex/03-进阶应用/Agents 与 MCP.md`
- 内嵌引用块 → Callout（内容未变）：`> **一句话总结**` → `> [!note] 一句话总结`
- `> **本章小结**` 内嵌块 → `## 小结`

## 保留的实质性内容（未删改）
- 全部代码块：代理配置路径、`code-explorer.toml` 完整示例、`[agents]` 全局设置、MCP `[mcp_servers.*]` 配置位置、STDIO 本地进程示例、Streamable HTTP 远程 API 示例、工具白名单/黑名单示例、`codex mcp add` 命令
- 全部表格：代理字段表、三种内置代理表、Codex vs Claude Code Agents 对比表、审批模式表、Codex vs Claude Code MCP 对比表
- 全部 Callout / 引用块正文
- frontmatter 中 `source_project: codex-config`、`created: 2026-07-31` 不变；`updated` 更新为 2026-08-10，`status` 更新为 updated
