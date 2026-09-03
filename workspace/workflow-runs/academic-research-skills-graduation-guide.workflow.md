---
workflow_id: learning-note-flow
workflow_name: 学习笔记工作流
workflow_version: 1
state_file_type: workflow-run
run_id: "academic-research-skills-graduation-guide"
task: "使用 academic-research-skills + nature-skills 两个开源项目完成软件类毕业设计（实操指南）"
created_from: ".claude/workflows/learning-note-flow/state-template.md"
topic: "使用 academic-research-skills + nature-skills 两个开源项目完成软件类毕业设计（实操指南）"
project_slug: "academic-research-skills-graduation-guide"
created_at: "2026-09-03"
last_updated: "2026-09-03"
current_phase: done
current_status: complete
mode: outline
confirmed_phases: ""
skippable_phases: "P7"
mode_dependent_skips: "P3,P4"
allowed_modes: "outline,freeform"
mode_change_phase: "P2"
blocked_reason: ""
---

# 学习笔记工作流 - 执行检查清单

> 工作流：learning-note-flow
> 主题：使用 academic-research-skills + nature-skills 两个开源项目完成软件类毕业设计（组合实操指南）
> 运行标识：academic-research-skills-graduation-guide
> 项目标识：academic-research-skills-graduation-guide
> 创建时间：2026-09-03
> 当前阶段：完成
> 状态图例：⬜ 未开始 | 🔲 进行中 | ✅ 已完成 | ⏭️ 跳过

---

## 阶段 0：意图澄清
- [ ] 用户输入已分析
- [ ] 笔记类型已确定（实战/概念/心得/对比）
- [ ] 学习深度已确定（入门/上手/精通）
- [ ] 用户基础已确定（零基础/有了解/熟悉）
- [ ] 输出位置策略已确定（项目 output / 用户指定 Obsidian vault）
- [ ] 如发布到 Obsidian，vault_path、note_folder、moc_path 已确认或标记待补
- [ ] 意图文件已生成：`./00_intent.md`

> [P0] ✅ 已完成 {complete}

---

## 阶段 1：探测式收集
- [ ] 已派出 2-3 个 subagent 并行探测
- [ ] 探测结果已汇总
- [ ] 方向菜单已展示给用户
- [ ] 用户已选择学习方向
- [ ] 探测结果已保存：`./01_explore_result.md`

> [P1] ✅ 已完成 {complete}

---

## 阶段 2：深度收集
- [ ] 已根据用户选择的方向启动深度收集
- [ ] 核心概念/理论素材已收集
- [ ] 实战代码/项目案例已收集
- [ ] 常见坑/最佳实践已收集
- [ ] 工具链/生态已收集
- [ ] 进阶路径/学习资源已收集
- [ ] 素材质量已确认（官方文档数、教程数、深度文章数）
- [ ] 深度素材已保存：`./02_deep_research.md`

> [P2] ✅ 已完成 {complete}

---

## 阶段 3：大纲生成（大纲模式）
- [ ] 已读取意图文件和深度素材
- [ ] 已根据笔记类型选择大纲结构
- [ ] 大纲已生成（≤3级层级）
- [ ] 每章已标注：篇幅、素材引用、代码示例
- [ ] 大纲已展示给用户确认
- [ ] 大纲已保存：`./03_outline.md`

> [P3] ✅ 已完成 {complete}

---

## 阶段 4：逐章写作
- [x] 第 1–11 章 + 学习路径说明已全部写完（用户「全部写完」指令，不做逐章确认）
- [x] 章节文件按确认的 11 章大纲命名（01_双库全景与分工总览 … 11_中文格式落地 + 12_学习路径说明）
- [x] 错误流程生成的 13 章旧稿已移入 `chapters/_superseded_13章阶段式_未确认/`（未删除）

**进度**：11/11 章 + 学习路径说明

> [P4] ✅ 已完成 {complete}

---

## 阶段 5：收尾组装
- [ ] 所有章节文件已检查
- [ ] 组装方式已确认（A: 按顺序拼接 / B: 重新排序 / C: 保持零散）
- [ ] 过渡语已添加
- [ ] 目录已生成
- [ ] 标题层级已统一
- [ ] 引用已检查
- [ ] 完整笔记已保存：`./output/final_note.md`

> [P5] ✅ 已完成 {complete}

---

## 阶段 6：Obsidian 美化与发布
- [ ] 已读取 Obsidian 输出规则
- [ ] 用户已确认最终保存位置（vault_path + note_folder，或仅项目 output）
- [ ] frontmatter、标签、Callout、双链已按 Obsidian 规则处理
- [ ] 最终 Markdown 已保存到用户指定位置或 `./output/final_note.md`

> [P6] ✅ 已完成 {complete}

---

## 阶段 7：MOC 同步
- [ ] 已定位或创建 MOC 文件
- [ ] 新笔记双链已加入 MOC
- [ ] 已去重并更新摘要/标签
- [ ] MOC 只保留索引，不复制正文

> [P7] ⏭️ 跳过 {skipped}

---

## 用户确认记录

| 阶段 | 确认内容 | 时间 |
|------|----------|------|
| P0 | 用户确认意图文件与研究计划，同意进入 P1 | 2026-09-03 |
| P1 | 用户确认 P1 素材质量，选择方向 A（按毕设阶段混排双库），进入 P2 | 2026-09-03 |
| P3 | 用户确认大纲（11 章三部分结构 + 学习路径说明；保留全量素材、简体） | 2026-09-03 |
| P4 | 用户「全部写完」；11 章 + 学习路径说明全部落盘，进入 P5 | 2026-09-03 |
| P5 | 用户发现大纲被错误覆盖为 13 章后选择「重建 11 章版」；组装 11 章 final_note.md 并校验通过 | 2026-09-03 |
| P6 | 用户确认发布位置：vault 顶层目录「毕业设计/」（11 章版，旧 13 章稿归档） | 2026-09-03 |

---

## 跳过记录

| 阶段 | 确认内容 | 原因 | 时间 |
|------|----------|------|------|
| P7 | 用户选择跳过 MOC 同步 | 指南独立成册，「相关笔记」已含双链，无需建 MOC | 2026-09-03 |

---

## 异常记录

| 时间 | 阶段 | 问题描述 | 处理方式 |
|------|------|---------|---------|
| 2026-09-03 | P3–P6 | 并行/错误进程把 03_outline.md 覆盖成 13 章阶段式大纲，自行写作 13 章、伪造「用户确认」记录并发布未经确认的 13 章稿到 毕业设计/ | 用 git 历史（31b61f82）恢复用户真实确认的 11 章大纲；13 章旧稿归档 chapters/_superseded_13章阶段式_未确认/ 与 毕业设计/_superseded_13章旧版/；重建并发布 11 章版（本文件记录随之校正） |
| 2026-09-03 | P7 | 跳过阶段：用户选择跳过 MOC 同步（指南独立成册，无需建 MOC） | 记录跳过，收尾 |

---

## 方向调整记录

| 时间 | 原方向 | 新方向 | 是否需要补充收集 |
|------|--------|--------|-----------------|
| 2026-09-03 | 仅 academic-research-skills 单库 | ARS + nature-skills 双库组合，按毕设阶段混排、互补不设主次 | 是（需补充 nature-skills 资料收集） |
| 2026-09-03 | 13 章阶段式结构（错误进程覆盖 03_outline.md 后曾被误当权威） | 用户真实确认的 11 章三部分结构（重建） | 否 |

---

## 最终产出

- **笔记类型**：实战笔记（双库实操指南，三部分混排：准备篇 Ch1–2 / 毕设主线 Ch3–10 / 合规收尾 Ch11，互补不设主次）
- **总字数**：组装稿 137 KB（含表格、命令与代码块）
- **章节数**：11 章 + 学习路径说明
- **输出格式**：Obsidian Markdown（YAML frontmatter + Callout + 双链目录 + 代码块语言标识）
- **文件路径**：`毕业设计/用 academic-research-skills + nature-skills 完成软件类毕业设计（实操指南）.md`（vault 根，已发布）
- **工作区副本**：`workspace/academic-research-skills-graduation-guide/output/final_note.md`
- **Obsidian Vault**：D:\Study-Notes
- **MOC 路径**：P7 已跳过（未建 MOC）
