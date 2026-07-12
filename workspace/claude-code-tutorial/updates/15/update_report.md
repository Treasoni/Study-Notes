# 更新报告：Claude Code 定时任务自动化指南.md

| 项目 | 内容 |
|------|------|
| **文件** | Claude Code 定时任务自动化指南.md |
| **动作** | patch-in-place |
| **更新范围** | frontmatter、安装 URL、Hook 事件信息 |
| **完成时间** | 2026-07-12 |

## 修改记录

| # | 修改项 | 旧值 → 新值 |
|---|--------|-------------|
| 1 | Frontmatter | 补充 `title`、`status`、`source_project` |
| 2 | 安装 URL | `code.claude.com/install.sh` → `claude.ai/install.sh` |
| 3 | Hook 事件数 | 14 → 24+ |
| 4 | Hook 处理器类型 | 3 种 → 5 种（新增 Prompt、Agent、MCP Tool） |
| 5 | 补丁范围 | ~3% 内容更新（patch 层面，非重写） |

## 风险等级
- **低** — 内容相对更新且全面，仅做最小局部更新。
