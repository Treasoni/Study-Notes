---
workflow_id: learning-note-flow
workflow_name: 学习笔记工作流
workflow_version: 1
state_file_type: workflow-run
run_id: "haos-deploy-tutorial"
task: "部署 HAOS 详细教程：国内源 + 稳定运行"
created_from: ".claude/workflows/learning-note-flow/state-template.md"
topic: "部署 HAOS 详细教程：国内源 + 稳定运行"
project_slug: "haos-deploy-tutorial"
created_at: "2026-08-06"
last_updated: "2026-08-06"
current_phase: done
current_status: complete
mode: outline
confirmed_phases: "P0,P1,P2,P3,P4,P5,P6,P7"
skippable_phases: "P7"
mode_dependent_skips: "P3,P4"
allowed_modes: "outline,freeform"
mode_change_phase: "P2"
blocked_reason: ""
---

# 学习笔记工作流 - 执行检查清单

> 工作流：learning-note-flow
> 主题：部署 HAOS 详细教程：国内源 + 稳定运行
> 运行标识：haos-deploy-tutorial
> 项目标识：haos-deploy-tutorial
> 创建时间：2026-08-06
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

> [P0] ✅ 已完成

---

## 阶段 1：探测式收集
- [ ] 已派出 2-3 个 subagent 并行探测
- [ ] 探测结果已汇总
- [ ] 方向菜单已展示给用户
- [ ] 用户已选择学习方向
- [ ] 探测结果已保存：`./01_explore_result.md`

> [P1] ✅ 已完成

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

> [P2] ✅ 已完成

---

## 阶段 3：大纲生成（大纲模式）
- [ ] 已读取意图文件和深度素材
- [ ] 已根据笔记类型选择大纲结构
- [ ] 大纲已生成（≤3级层级）
- [ ] 每章已标注：篇幅、素材引用、代码示例
- [ ] 大纲已展示给用户确认
- [ ] 大纲已保存：`./03_outline.md`

> [P3] ✅ 已完成

---

## 阶段 4：逐章写作
- [x] 第 1 章已写完并确认
- [x] 第 2 章已写完并确认
- [x] 第 3 章已写完并确认（`chapters/03_官方原版HAOS安装实战.md`）
- [x] 第 4 章已写完并确认（手动配置国内源，官方原版加速核心）
- [x] 第 5 章已写完并确认（HAOS-CN 极速版）
- [x] 第 6 章已写完并确认（双路线对比与选型建议）
- [x] 第 7 章已写完并确认（`chapters/07_稳定运行保障.md`）
- [x] 第 8 章已写完并确认（`chapters/08_故障排查手册与长期运维.md`）

**进度**：8/8

> [P4] ✅ 已完成

---

## 阶段 5：收尾组装
- [ ] 所有章节文件已检查
- [ ] 组装方式已确认（A: 按顺序拼接 / B: 重新排序 / C: 保持零散）
- [ ] 过渡语已添加
- [ ] 目录已生成
- [ ] 标题层级已统一
- [ ] 引用已检查
- [ ] 完整笔记已保存：`./output/final_note.md`

> [P5] ✅ 已完成

---

## 阶段 6：Obsidian 美化与发布
- [ ] 已读取 Obsidian 输出规则
- [ ] 用户已确认最终保存位置（vault_path + note_folder，或仅项目 output）
- [ ] frontmatter、标签、Callout、双链已按 Obsidian 规则处理
- [ ] 最终 Markdown 已保存到用户指定位置或 `./output/final_note.md`

> [P6] ✅ 已完成

---

## 阶段 7：MOC 同步
- [ ] 已定位或创建 MOC 文件
- [ ] 新笔记双链已加入 MOC
- [ ] 已去重并更新摘要/标签
- [ ] MOC 只保留索引，不复制正文

> [P7] ✅ 已完成

---

## 用户确认记录

| 阶段 | 确认内容 | 时间 |
|------|----------|------|
| P7 | 用户确认同步 MOC（Home Assistant MOC 部署指南分组新增索引行） | 2026-08-06 22:15 |
| P6 | 用户确认拆分美化发布结果（索引页+8章节到 homeassistant/haos-deploy/） | 2026-08-06 22:15 |
| P5 | 用户确认组装结果（8章约1.9万字）与发布方式：拆分（索引页+8章节文件） | 2026-08-06 22:08 |
| P4 | 用户授权连续写作，8 章全部完成（第 3 章由本章 agent 完成并确认） | 2026-08-06 22:01 |
| P3 | 用户确认大纲（8章双路线对比，连续写作授权） | 2026-08-06 21:58 |
| P2 | 用户确认深度收集素材质量（官方+社区交叉验证，含时效性标注） | 2026-08-06 21:54 |
| P1 | 用户选择方向 C：双路线对比（官方原版+手动国内源 vs HAOS-CN 极速版） | 2026-08-06 21:49 |
| P0 | 用户确认意图文件和研究计划 | 2026-08-06 21:45 |

---

## 跳过记录

| 阶段 | 确认内容 | 原因 | 时间 |
|------|----------|------|------|
| | | | |

---

## 异常记录

| 时间 | 阶段 | 问题描述 | 处理方式 |
|------|------|---------|---------|
| | | | |

---

## 方向调整记录

| 时间 | 原方向 | 新方向 | 是否需要补充收集 |
|------|--------|--------|-----------------|
| | | | |

---

## 最终产出

- **笔记类型**：实战教程 practice（双路线对比：官方原版+手动国内源 vs HAOS-CN 极速版）
- **总字数**：约 1.9 万字
- **章节数**：8
- **输出格式**：Obsidian Markdown（拆分：索引页 + 8 章节文件 + 章节导航）
- **文件路径**：`homeassistant/haos-deploy/`（`部署 HAOS 详细教程.md` 索引页 + `01_绪论` ~ `08_故障排查手册与长期运维` 8 个章节文件）
- **Obsidian Vault**：`C:\note\Study-Notes`
- **MOC 路径**：`homeassistant/Home Assistant MOC.md`（部署指南分组已追加索引）
