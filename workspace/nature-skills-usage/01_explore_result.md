# 如何用好 nature-skills — P1 探测结果

> 运行: nature-skills-usage · 阶段: P1 探测式收集 · 检索日期: 2026-09-08
> 方法: 3 个独立镜头并行探测（概览 / 安装维护 / 实战用法），返回候选源记录，已按 canonical URL 去重。

## 一、候选信源（去重后）

| # | 标题 | URL | 层级 | 分 | 相关性 |
|---|------|-----|------|----|--------|
| S1 | nature-skills 官方 README（中文，含 §4 快速开始、§5 安装、§6 技能索引） | https://github.com/Yuan1z0825/nature-skills | official | 5 | 项目定位/设计原则/19 技能/安装命令/可复制提示词的一手源头 |
| S2 | npx skills CLI 官方文档（vercel-labs/skills，codex 路径 `.agents/skills/`、全局 `~/.codex/skills/`） | https://github.com/vercel-labs/skills | official | 5 | add/list/update/remove 及 `--global/--agent/--copy/--yes` 语义唯一权威 |
| S3 | nature-skills 官方在线网站 | https://yuan1z0825.github.io/nature-skills/ | official | 4 | 官方门户：读-写-审-图-检索 19 技能全流程导航 |
| S4 | nature-skills README_EN §5 Installation（英文镜像） | https://github.com/Yuan1z0825/nature-skills/blob/main/README_EN.md | official | 4 | 安装命令与 frontmatter 命名差异交叉核对 |
| S5 | 今日开源[第45期] nature-research-skills 解读（zhang-yd） | https://www.cnblogs.com/zhang-yd/p/22151100 | implementation-report | 4 | 逐文件解读：router 心智模型、nature-shared 共享包、端到端流水线示例 |
| S6 | Nature Skills：把论文精读到专利生成的科研全流程装进 AI Agent（iTech） | https://www.cnblogs.com/itech/p/22851434 | implementation-report | 3 | 以科研日常场景串讲 19 技能、6 条流程线实战走查 |
| S7 | nature-skills 实测报告（头条） | https://www.toutiao.com/article/7640074589502046746/ | community | 3 | 诚实避坑：润色有 AI 味、绘图一般、多数技能 Draft/Beta |
| S8 | LINUX DO「AI 科研党推荐好使的 skill」讨论串 | https://linux.do/t/topic/2327036/19 | community | 3 | 真实用户推荐与吐槽：绘图分化、润色冗长、防 AI 率 |
| S9 | skillsmp nature-shared 技能详情页 | https://skillsmp.com/zh/creators/yuan1z0825/nature-skills/skills-nature-shared | community | 2 | 佐证 nature-shared 为共享依赖（低权威，仅旁证） |

**关键更正**：README 里的 `npx skills` CLI 规范源是 **vercel-labs/skills**（`nicholasoxford/npx-skills` 为 404 假线索）。其 Supported Agents 表确认 Codex 项目路径 `.agents/skills/`、全局路径 `~/.codex/skills/`。

## 二、方向菜单

面向「Codex 上手实战指南」笔记，P2 深度收集建议聚焦以下方向（可多选）：

1. **A. 技能全景速查** — 19 个技能逐个用途/触发词/Stable-Beta-Draft 状态/运行依赖，做成速查表（偏参考资料）
2. **B. Codex 安装与日常维护** — `npx skills` 命令矩阵、全量 vs 单技能、frontmatter 名映射、更新/卸载、依赖配置与排错
3. **C. 典型科研场景实操** — 官方 8 类可复制提示词 + 端到端流程（读论文→组会 PPT→润色→审稿→回复→引用画像→绘图）
4. **D. 避坑与最佳实践** — AI 味润色、绘图质量分化、Draft 技能需人工核验、防 AI 率、目录整包复制、运行时依赖

## 三、覆盖缺口

- 官方仓库网页对 WebFetch 受限，P2 需用 `curl` 抓 raw README / SKILL.md / manifest / scripts。
- 各技能目录内部细节（触发词、manifest.yaml、references/、static/、脚本依赖）需 P2 直接抓 `skills/*/` 文件，README 一级索引不够。
- 作者抖音视频教程与知识星球「Nature Skills 以及背后的哲学」无稳定可抓 URL，仅作背景线索，不列为信源。
- 官方未提供与 Matt Pocock Skills / superpowers 的直接对比；生态对比只出现在 iTech 博文。
- 仓库 meta（约 40.1k stars / 创建于 2026-04-24 / 被 DeepMind Science Skills 借鉴）由 subagent 经 GitHub API 于 2026-09-08 获取，属辅助信息。

## 四、P2 预估范围

- 必抓官方：README 全文（curl raw）、README_EN、在线网站导览页、`npx skills`（vercel-labs/skills）README。
- 技能级：按用户所选方向抓 3–8 个核心技能的 `SKILL.md` + `manifest.yaml`（优先 reader/paper2ppt/polishing/writing/response/researchwrite）。
- 第三方走查：zhang-yd + iTech（选 1–2）；社区实测（头条/LINUX DO）仅取避坑观点并标注 operational experience。
- 产出：`02_deep_research.md`（scope、source table、claim/source map、contradictions、practical guidance、open questions、downstream handoff）。

## 五、下一步

等用户在方向菜单中选择 A/B/C/D（可多选），随后进入 P2 深度收集。
