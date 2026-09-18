---
workflow_id: learning-note-flow
workflow_name: 学习笔记工作流
workflow_version: 1
state_file_type: workflow-run
run_id: "smb-cifs-mount-linux"
task: "把 SMB/CIFS 共享文件夹挂载到 Linux 服务器"
created_from: ".claude/workflows/learning-note-flow/state-template.md"
topic: "把 SMB/CIFS 共享文件夹挂载到 Linux 服务器"
project_slug: "smb-cifs-mount-linux"
created_at: "2026-09-18"
last_updated: "2026-09-18"
current_phase: P6
current_status: in_progress
mode: outline
blocked_reason: ""
quality_gate: pending
quality_gate_owner: ""
quality_gate_due: ""
---

# 学习笔记工作流 - 执行检查清单

> 工作流：learning-note-flow
> 主题：把 SMB/CIFS 共享文件夹挂载到 Linux 服务器
> 运行标识：smb-cifs-mount-linux
> 项目标识：smb-cifs-mount-linux
> 创建时间：2026-09-18
> 当前阶段：阶段 6
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

**进度**：0/待大纲确定

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

> [P6] 🔲 进行中 {in_progress}

---

## 阶段 7：MOC 同步
- [ ] 已定位或创建 MOC 文件
- [ ] 新笔记双链已加入 MOC
- [ ] 已去重并更新摘要/标签
- [ ] MOC 只保留索引，不复制正文

> [P7] ⬜ 未开始

---

## 用户确认记录

| 阶段 | 确认内容 | 时间 |
|------|----------|------|
| P5 | 确认组装结果：`output/final_note.md` 12,362 中文字 / 一级标题 1 个 / 标注零损失（社区 9・推断 12・缺口 6，脚本复核）；**确认发布格式 = 拆分系列**，vault_path=`D:\Study-Notes`、note_folder=`linux/SMB挂载/`、moc_path=`linux/linux MOC.md`（另在 `docker/Docker MOC.md` 加容器册索引） | 2026-09-18 |
| P4 | 确认五章全部写完。第 1 章超大纲篇幅预算（1,629 中文字 vs 800–1,200）经确认**保留现状、不删小节**；组装方式（独立章节 + 前后导航双链 + MOC 索引页）留待 P5 确认 | 2026-09-18 |
| P3 | 确认大纲：5 章骨架、篇幅与深度合适；**保留第 5 章**（容器，作可选小节）；同意回补 `smbclient`/`findmnt` 来源缺口；**授权「全部写完」——第 1–5 章连续写作、不再逐章暂停**（仍按每批 ≤3 章分批派发） | 2026-09-18 |
| P2 | 确认素材够用（16 条：official 11 / secondary 1 / community 3 / 历史一手 1）；确认执行模式 = **大纲模式**（非随性）；接受 5 项未解问题按「不得写成官方结论」处理 | 2026-09-18 |
| P1 | 确认素材质量与方向：选 **A 均衡实战**（协议选型→手动挂载→凭据+fstab→排错→容器为可选小节），5 章；接受 FNOS 段落按 community 层级标注、112/115/2 按 errno 推断、容器只作一小节 | 2026-09-18 |
| P0 | 确认意图：SMB/CIFS 主线（sma=SMB 笔误）、挂载端 Debian/Ubuntu、共享端通用+FNOS/NAS 与 Windows 双例、上手实战深度、五个探索方向全要、输出先落 workspace/output/ | 2026-09-18 |
| | | |

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

- **笔记类型**：
- **总字数**：
- **章节数**：
- **输出格式**：
- **文件路径**：
- **Obsidian Vault**：
- **MOC 路径**：
