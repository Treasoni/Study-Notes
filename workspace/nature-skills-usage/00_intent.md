# 如何用好 nature-skills（Codex 上手实战指南） - 意图文件

## 基本信息

- **主题**: 如何用好 nature-skills（Codex 上手实战指南）
- **项目标识**: nature-skills-usage
- **运行标识**: nature-skills-usage
- **创建时间**: 2026-09-08
- **当前阶段**: 阶段 0（意图澄清）
- **输出目标**: obsidian-vault（发布位置暂不指定，阶段 6 前确认 note_folder/moc_path）
- **Vault 路径**: D:\Study-Notes（当前 vault；阶段 6 发布时按 vault 内相对目录写入）
- **笔记目录**: 暂不指定（阶段 6 发布前确认）
- **MOC 路径**: 暂不指定（阶段 6/7 前确认）
- **来源 URL**: https://github.com/Yuan1z0825/nature-skills

## 学习目标

### 笔记类型
实战笔记（上手实战指南）

### 学习深度
上手：装得上、认得全、会选技能、典型科研场景能跑通、会排错

### 用户基础
熟悉 agent skill 机制（SKILL.md / 技能包 / npx skills 概念已有认知）

### 主用环境
Codex（`npx skills add` 官方主推路径）；与 Claude Code 安装方式差异作对照说明

## 研究计划

### 探索方向
1. **是什么与设计哲学**: 项目定位、SKILL.md 组织方式、`nature-shared` 共享支持包、引用体系与“可验证工作流”理念
2. **Codex 安装与维护**: `npx skills add/list/update`，全局 vs 项目级、单技能 vs 全量、`--copy` 语义、`--list` 与 frontmatter 技能名映射
3. **技能清单速查**: 19 个技能逐个用途、触发场景、依赖（含 `nature-reader`、`nature-paper2ppt`、`nature-polishing`、`nature-writing`、`nature-response`、`researchwrite` 等）
4. **典型科研场景实操**: 读论文/中英对照、组会汇报 PPT、写作润色与 Nature 风格改写、摘要引言草拟、预投稿互盲审稿模拟、逐点回复审稿意见、引用数与引用者画像、科研绘图
5. **使用技巧与避坑**: 怎么选对技能、提示词最佳实践、运行时依赖（Python/R/浏览器/MCP）、更新与卸载、与 Claude Code 本地 clone 方式的取舍

### 重点收集
- **核心概念**: SKILL.md、可安装技能单元、nature-shared、npx skills、引用体系、可验证工作流、frontmatter 技能名
- **实战代码**: Codex 安装/列出/更新/卸载命令；各技能开箱即用的提示词示例
- **常见坑**: 运行时依赖未配置、目录名 ≠ frontmatter 技能名、单独装依赖技能漏掉 `nature-shared`、Claude Code 不可用 `scripts/update-codex-skills.sh`
- **工具链**: Codex、Node.js ≥18、npx skills CLI、nature-skills 仓库结构与配套脚本

### 信源偏好
- 官方文档: 是（GitHub README / 在线网站 / skills/*/SKILL.md）
- 技术博客: 是（作者视频教程、社区文章）
- 社区讨论: 是（知识星球 / Agent 科研交流群公开内容、GitHub issues）
- 学术论文: 否

## 备注

- 输出位置候选 `AI学习/` 或 `GitHub项目/`，在阶段 0 用户确认点敲定 note_folder 与 moc_path。
- 本笔记聚焦 **Codex 环境**，Claude Code 用法仅作对照，避免两套安装说明互相稀释。
- 阶段 2 结束时需向用户确认：进入「大纲模式」逐章写，还是「随性模式」直接出笔记。
