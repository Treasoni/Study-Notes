# 更新报告：Claude Code 高级功能.md

| 项目 | 内容 |
|------|------|
| **文件** | Claude Code 高级功能.md |
| **动作** | patch-in-place |
| **更新范围** | frontmatter、模型表、Mermaid 图、Auto Mode 状态、环境变量、新增章节 |
| **完成时间** | 2026-07-12 |

## 修改记录

| # | 修改项 | 旧值 → 新值 |
|---|--------|-------------|
| 1 | Frontmatter | 补充 `title`、`updated`、`status`、`source_project` |
| 2 | Auto Mode | "研究预览" → "正式发布 GA"（Q2 2026） |
| 3 | Extended Thinking 模型表 | 补充 Opus 4.8、Sonnet 5，移除 Opus 4.6/Sonnet 4.6 作为主要推荐 |
| 4 | Mermaid 概览图 | 补充 Ultraplan、Dynamic Workflows、Computer Use、Artifacts 节点 |
| 5 | 概述文字 | 补充 Dynamic Workflows、Ultraplan、Computer Use 到列举 |
| 6 | Effort 级别注释 | "仅 Opus 4.6" → "Opus 系列" |
| 7 | 权限模式表 Auto 行 | "研究预览" → "正式发布 GA" |
| 8 | CI/CD 安装命令 | `npm install -g @anthropic-ai/claude-code` → `curl -fsSL https://claude.ai/install.sh \| bash` |
| 9 | 环境变量模型名 | `claude-opus-4-6` → `claude-opus-4-8` |
| 10 | 新增 Ultraplan 章节 | 云端规划功能（Q2 2026） |
| 11 | 新增 Dynamic Workflows 章节 | 6 种编排模式 + 真实案例（GA 2026-05-28） |
| 12 | 新增 Computer Use 章节 | CLI 计算机操作（研究预览） |
| 13 | 新增 Artifacts 章节 | 对话中可视化内容渲染（Q2 2026） |
| 14 | 补丁范围 | ~15% 内容新增/更新（patch 层面，非重写） |

## 风险等级
- **低** — 补充新章节和更新过时信息，未改变原有核心内容和结构。
