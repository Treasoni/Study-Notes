---
workflow_id: learning-note-flow
workflow_name: 学习笔记工作流
workflow_version: 1
state_file_type: workflow-run
run_id: "nastool-fnos-deploy"
task: "在飞牛 fnOS 上搭建 nastool 家庭影院（以最新可用方案为主线）"
created_from: ".claude/workflows/learning-note-flow/state-template.md"
topic: "在飞牛 fnOS 上搭建 nastool 家庭影院（以最新可用方案为主线）"
project_slug: "nastool-fnos-deploy"
created_at: "2026-10-06"
last_updated: "2026-10-07"
current_phase: done
current_status: complete
mode: outline
blocked_reason: ""
quality_gate: passed
quality_gate_owner: ""
quality_gate_due: ""
---

# 学习笔记工作流 - 执行检查清单

> 工作流：learning-note-flow
> 主题：在飞牛 fnOS 上搭建 nastool 家庭影院（以最新可用方案为主线）
> 运行标识：nastool-fnos-deploy
> 项目标识：nastool-fnos-deploy
> 创建时间：2026-10-06
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
- [ ] 并行写作 ≥2 章时：已冻结跨章口径表并写进每个 dispatch
- [ ] 全部章节交付后：已做跨章一致性比对三类全覆盖（可照抄的配置块 / 同一来源的散文式转述与定性 / 定义与判据句对冻结语义框架自洽）

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

> [P6] ✅ 已完成 {complete}

---

## 阶段 7：MOC 同步
- [ ] 已定位或创建 MOC 文件
- [ ] 新笔记双链已加入 MOC
- [ ] 已去重并更新摘要/标签
- [ ] MOC 只保留索引，不复制正文

> [P7] ✅ 已完成 {complete}

---

## 用户确认记录

| 阶段 | 确认内容 | 时间 |
|------|----------|------|
| P5 | 组装完成 output/final_note.md + chapters/_merged.md（**当时值** 20666 汉字；本次更新后最新值见「最终产出」）；C 比对 20 组 0 差异 | 2026-10-07 07:53 |
| 收尾后更新 | 第 6 章新增 6.5「第二备选路：玩 BT」（note-updater 路径，用户选 A 案）；四份副本同步，副本漂移 0/10、C 比对 21 组 0 差异、结构自检 0 可疑、死链 0；重跑取数：vault 11 文件 23754 汉字，final_note.md 22328 汉字 | 2026-10-07 |
| P4 | 10 章写作完成（约 20600 汉字）；校验 V/S/结构全绿 | 2026-10-07 01:32 |
| P3 | 大纲确认：10 章；C 路留第 6 章；保留 3.5 端口免责节 | 2026-10-07 00:04 |
| P2 | P2 素材与来源表确认；进入大纲模式 | 2026-10-07 00:04 |
| P1 | 用户选定方向：A+C 双路合写（主路 MoviePilot V3，标注需 PT 认证；备选路不依赖 PT） | 2026-10-06 23:38 |
| P0 | 用户确认意图文件与研究计划（选题=最新可用方案；目录=流媒体与影音/nastool 家庭影院 fnOS 部署） | 2026-10-06 23:25 |
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
| 2026-10-06 | P1 | 原计划派 3 个并行探测子代理（选型 / 部署 / 生态），用户中断该派发 | 改为按用户指示**只跑方向 1（现状与选型）**，由主流程自己用 WebSearch/WebFetch/crawl 核实；方向 2/3 延迟到 P2 |
| 2026-10-06 | P1 | 预判「原版 nastool = jxxghp/nas-tools」有误 | 更正：原版仓库是 **NAStool/nas-tools**（2023-05-16 归档、只读）；`jxxghp/nas-tools` 为 404 |
| 2026-10-06 | P1 | 发现 MoviePilot **需要 PT 站点认证**（官方 Wiki 确认），且 **V3 初始化方式已变** | 已写入 `01_explore_result.md` 并升级为 P1 用户关卡的先决问题；未确认前不进入 P2 |

---

## 方向调整记录

| 时间 | 原方向 | 新方向 | 是否需要补充收集 |
|------|--------|--------|-----------------|
| 2026-10-06 | 原版 nastool（视频口径） | MoviePilot V3（同作者最新主线） | 是——P2 需补齐 V3 一手来源 |
| 2026-10-06 | 单路 A（MoviePilot 完整链路） | A+C 双路（主路 V3 + 不依赖 PT 的网盘流媒体备选路） | 是——P2 需补 C 路来源 |

---

## 最终产出

> **取数纪律**：下表的体积 / 字数 / 章数 / 锚点数 / Callout 数必须**当场重新运行取数或重新计数**，并把命令留在「取数命令」一行；不要从上下文里的历史输出誊抄，也不要手算合计。产物在记录之后又被改动时，grep 同一数字的**所有**出现处一并更新（同一组数字常同时出现在阶段段落与本节）。

- **笔记类型**：实战笔记（入门优先 · 照做即用），分册形式发布
- **总字数**：23754 汉字（发布件 11 个文件合计；单一合并件 `output/final_note.md` 为 22328 汉字）
- **章节数**：10 章 + 1 篇总览（共 11 个发布文件）
- **输出格式**：Obsidian Markdown 分册（总览 + 10 章），含 frontmatter / Callout / 双链 / 章末引文对照表
- **取数命令**：
  ```bash
  python3 - <<'PY'
  import re, glob, os
  d = "流媒体与影音/nastool 家庭影院 fnOS 部署"
  cjk = re.compile(r'[一-鿿]'); tot = 0
  for f in sorted(glob.glob(os.path.join(d, "*.md"))):
      n = len(cjk.findall(open(f, encoding="utf-8").read())); tot += n
      print("%-46s %8d" % (os.path.basename(f), n))
  print("合计 %d 个文件 %d 汉字" % (len(glob.glob(os.path.join(d, "*.md"))), tot))
  PY
  ```
  本次运行结果：11 个文件 / 23754 汉字（明细：01=2161、02=1560、03=2559、04=2501、05=2172、06=3056、07=2468、08=3029、09=2236、10=1284、总览=728）
- **文件路径**：
  - 工作区：`workspace/nastool-fnos-deploy/output/final_note.md`（合并件）、`workspace/nastool-fnos-deploy/chapters/`（10 章源文件）
  - 发布件：`流媒体与影音/nastool 家庭影院 fnOS 部署/`（总览 + 10 章）
- **Obsidian Vault**：`/Users/zhqznc/Documents/项目`（本仓库即 vault 根）
- **MOC 路径**：`流媒体与影音 MOC.md`（已更新 `updated: 2026-10-07` 并追加 1 条索引项）
