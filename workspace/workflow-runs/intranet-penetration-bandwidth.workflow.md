---
workflow_id: learning-note-flow
workflow_name: 学习笔记工作流
workflow_version: 1
state_file_type: workflow-run
run_id: "intranet-penetration-bandwidth"
task: "内网穿透带宽性能分析"
created_from: ".claude/workflows/learning-note-flow/state-template.md"
topic: "内网穿透带宽性能分析"
project_slug: "intranet-penetration-bandwidth"
created_at: "2026-08-27"
last_updated: "2026-08-27"
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
> 主题：内网穿透带宽性能分析
> 运行标识：intranet-penetration-bandwidth
> 项目标识：intranet-penetration-bandwidth
> 创建时间：2026-08-27
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
- [ ] 第 1 章已写完并确认
- [ ] 第 2 章已写完并确认
- [ ] 第 3 章已写完并确认
- [ ] ...（根据实际章节数添加）

**进度**：5/5

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
| P0 | 用户确认意图文件和研究计划 | 2026-08-27 |
| P1 | 用户确认素材质量并选择方向：全部深挖 | 2026-08-27 |
| P2 | 用户确认深度素材质量 | 2026-08-27 |
| P3 | 用户确认大纲（5 章） | 2026-08-27 |
| P4 | 用户指示直接写完，跳过逐章确认（5 章全部完成） | 2026-08-27 |

---

## 跳过记录

| 阶段 | 确认内容 | 原因 | 时间 |
|------|----------|------|------|
| | | | |

---

## 异常记录

| 时间 | 阶段 | 问题描述 | 处理方式 |
|------|------|---------|---------|
| 2026-08-27 23:09 | P7 | 跳过阶段：moc_path 待指定，暂无 MOC 可同步；用户在 Obsidian 指定 vault 后可再执行 moc-organizer | 继续推进到下一未完成阶段 |
| | | | |

---

## 方向调整记录

| 时间 | 原方向 | 新方向 | 是否需要补充收集 |
|------|--------|--------|-----------------|
| | | | |

---

## 最终产出

- **笔记类型**：概念笔记（附带实战内容）
- **总字数**：约 9,900 字（正文中文，含 Markdown 约 48k 字符）
- **章节数**：5
- **输出格式**：Obsidian Markdown（YAML frontmatter + Callout + 双链 + 脚注）
- **文件路径**：workspace/intranet-penetration-bandwidth/output/final_note.md
- **Obsidian Vault**：D:\Study-Notes
- **已发布**：D:\Study-Notes\虚拟机\内网穿透带宽性能分析.md
- **MOC 路径**：待指定（用户可在 Obsidian 中指定后执行 moc-organizer）
