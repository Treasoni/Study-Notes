# 更新报告：Claude Code CLI 完整参考.md

| 项目 | 内容 |
|------|------|
| **文件** | Claude Code CLI 完整参考.md |
| **动作** | patch-in-place |
| **更新范围** | frontmatter、版本号、模型表、模式标志、CI/CD 示例 |
| **完成时间** | 2026-07-12 |

## 修改记录
| # | 修改项 | 旧值 → 新值 |
|---|--------|-------------|
| 1 | Frontmatter | 补充 `title`、`updated`、`status`、`source_project` |
| 2 | 版本号 | v2.1.119 → v2.1.207 |
| 3 | 模型表 | 新增 Opus 4.8（新默认）、Sonnet 5（新默认）；调整排序 |
| 4 | 努力级别 | 新增 Opus 4.8 支持，增加 xhigh 级别 |
| 5 | 模式控制 | 新增 `--safe-mode` 标志 |
| 6 | CI/CD 示例 | npm 安装 → curl 原生安装器 |
| 7 | 环境变量 | 努力级别增加 xhigh/max |

## 风险等级
- **低** — 仅局部替换，未改动整体结构
