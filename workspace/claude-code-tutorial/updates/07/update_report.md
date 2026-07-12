# 更新报告：Claude Code Hooks 使用指南.md

| 项目 | 内容 |
|------|------|
| **文件** | Claude Code Hooks 使用指南.md |
| **动作** | patch-in-place |
| **更新范围** | frontmatter、Hook 类型数、MCP Tool Hook 补充、事件计数 |
| **完成时间** | 2026-07-12 |

## 修改记录

| # | 修改项 | 旧值 → 新值 |
|---|--------|-------------|
| 1 | Frontmatter | 补充 `title`、`updated`、`status`、`source_project` |
| 2 | Hook 类型数 | 4 类 → 5 类（新增 `mcp_tool`） |
| 3 | MCP Tool Hook | 新增完整章节描述 MCP Tool Hook 类型 |
| 4 | 事件计数 | "25个" → "24+个（v2.1.83+新增文件系统事件）" |
| 5 | 补丁范围 | ~5% 内容更新（patch 层面，非重写） |

## 风险等级
- **低** — 仅在过时区域做局部替换和补充，未改变原有结构和主要内容。
