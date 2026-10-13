---
workflow_id: learning-note-flow
workflow_name: 学习笔记工作流
workflow_version: 1
state_file_type: workflow-run
run_id: "searxng-hermes"
task: "SearXNG 自托管与 Hermes 接入"
created_from: ".claude/workflows/learning-note-flow/state-template.md"
topic: "SearXNG 自托管与 Hermes 接入"
project_slug: "searxng-hermes"
created_at: "2026-10-07"
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
> 主题：SearXNG 自托管与 Hermes 接入
> 运行标识：searxng-hermes
> 项目标识：searxng-hermes
> 创建时间：2026-10-07
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
- [x] 已根据用户选择的方向启动深度收集
- [x] 核心概念/理论素材已收集
- [x] 实战代码/项目案例已收集
- [x] 常见坑/最佳实践已收集
- [x] 工具链/生态已收集
- [x] 进阶路径/学习资源已收集
- [x] 素材质量已确认（官方文档数、教程数、深度文章数）
- [x] 深度素材已保存：`./02_deep_research.md`

> [P2] ✅ 已完成 {complete}

**P2 自检行**：引文 47 处逐字核对（其中英文整句 17 处经校验器 V 全绿：命中 17 / 仅中间产物 0 / 未命中 0）/ 数值 8 处重新计数。
命令：`python3.12 .claude/scripts/note-citation-check.py workspace/searxng-hermes --mode verbatim --file 02_deep_research.md`
来源：19 件引用件（official 11 / primary 8），全部 `fetched`，无 `snippet-only`。矛盾 C1/C2/C3 已定案。

---

## 阶段 3：大纲生成（大纲模式）
- [x] 已读取意图文件和深度素材
- [x] 已根据笔记类型选择大纲结构
- [x] 大纲已生成（≤3级层级）
- [x] 每章已标注：篇幅、素材引用、代码示例
- [x] 大纲已展示给用户确认
- [x] 大纲已保存：`./03_outline.md`

> [P3] ✅ 已完成 {complete}

**P3 记录**：6 章（约 6700–9900 字，1 短/1 长/4 中）；含跨章口径冻结表 F1–F10。
用户确认：保持 6 章（「开启 JSON API」独立为第 3 章）。
大纲生成期间发现并回写修正 `02_deep_research.md` 6 处 HTML 源行号漂移（去标签行号 → 原文件行号），修正后校验器复跑全绿。

---

## 阶段 4：逐章写作
- [x] 第 1 章已写完并确认
- [x] 第 2 章已写完并确认（父流程独立验收：引文校验 V 全绿、结构自检 0 处、脚注全唯一）
- [x] 第 3 章已写完并确认（同上；父流程修正 1 处引文归属错误，见异常记录）
- [x] 第 4 章已写完并确认（同上）
- [x] 第 5 章已写完并确认（父流程独立验收：引文校验 V 全绿、结构自检 0 处、脚注全唯一、锚点逐条回源）
- [x] 第 6 章已写完并确认（同上）
- [x] 并行写作 ≥2 章时：已冻结跨章口径表并写进每个 dispatch（F1–F10，逐章 dispatch 附全表）
- [x] 全部章节交付后：已做跨章一致性比对三类全覆盖（可照抄的配置块 / 同一来源的散文式转述与定性 / 定义与判据句对冻结语义框架自洽）

**进度**：6/6（第 1–6 章全部写完并通过父流程独立验收；用户以「全部写完」豁免逐章确认，改为整批在 P4→P5 门前一次性复核）
**验收证据（父流程，非子代理自述）**：`python3.12 .claude/scripts/note-citation-check.py workspace/searxng-hermes --mode text` → V 英文整句 36 处命中 36 / 仅中间产物 0 / 未命中 0；S1=0、S2=0、S4=0。`python3 .claude/scripts/check-md-structure.py workspace/searxng-hermes/chapters/*.md` → 6 文件 0 处可疑。6 章脚注 ID 全唯一、无未定义引用。锚点逐条 `grep -n` 回源核对通过。
**父流程对章节的改动（3 处，均属冻结口径落地）**：① 第 3 章引文对照第 1 条出处 `L2-4 → L2-6`（见异常记录）；② 6 章引文对照引导句补「本章所引来源快照的取回日期均为 2026-10-07」（冻结口径 F10）。
**字数实况（取数命令：`python3 -c "import re,glob; [print(p, len(re.findall(r'[一-鿿]', open(p,encoding='utf-8').read()))) for p in sorted(glob.glob('workspace/searxng-hermes/chapters/*.md'))]"`，口径＝全文汉字含表格/脚注）**：ch1 1700 / ch2 1615 / ch3 1199 / ch4 816 / ch5 1198 / ch6 1283，**合计 7811 汉字 / 47.8 KB**。大纲区间为 ch1 800–1200、ch2 1800–2600、ch3 1000–1500、ch4 1000–1400、ch5 1200–1800、ch6 900–1400 —— 实况与区间系统性偏离（ch1 超上限，ch2–4 低于下限）。判定：**不按字数返工**，理由：各章「结构（≤3 级）」小节全部到位、无缺节；动手章含大量代码块与英文标识，纯汉字统计天然偏低；「不为凑字数引入无来源内容」。**47.8 KB > 30 KB 阈值 → 支持拆分为分册**（与 vault 既有分册惯例一致）。
**已知未落地项**：`l2-8_env.example` 因扩展名 `.example` 不被校验器 `CITE_FULL` 接受，未进任何引文对照表（其内容改由脚注 `[^c6-f]` 承载）。
**后置内容修正（2026-10-07，P6 之后）**：修正「`docker cp` 是否必经」的误导表述（第 2 章 3 处、第 3 章 3 处 + 新增脚注 `[^c3-j/k/l]`；详见异常记录）。此后本文件所有字数/体积数字均已**当场重取**（ch2 1568→1615、ch3 889→1199）。

> [P4] ✅ 已完成 {complete}

---

## 阶段 5：收尾组装
- [x] 所有章节文件已检查
- [x] 组装方式已确认（**B 拆分为分册**；用户在 P4→P5 门确认，按 vault 既有惯例 `README.md` + 编号章节）
- [x] 过渡语已添加（第 2–6 章各前置一句过渡）
- [x] 目录已生成（章级 TOC + 「这本册子讲什么」章概览表）
- [x] 标题层级已统一（`#` 文档标题 > `## 第 N 章` > `### N.M`；重新解析标题树确认逐层递减）
- [x] 引用已检查（三族校验器全跑，见 P5 记录）
- [x] 完整笔记已保存：`./output/final_note.md`

> [P5] ✅ 已完成 {complete}

**P5 记录**：
- 预合并：`python3.12 .claude/scripts/merge_files.py --input-dir workspace/searxng-hermes/chapters` → `chapters/_merged.md`（49512 B，6 文件）。
- 组装件：`output/final_note.md`（8379 汉字 / 52105 B）。H1 + 一句话看懂 + 章概览表 + 目录 + 6 章正文。
- 引文对照逐章数据行在 **合并件 / 组装件** 完全一致：第1章 8 / 第2章 5 / 第3章 5 / 第4章 5 / 第5章 6 / 第6章 4。
- 三族校验器 `python3.12 .claude/scripts/note-citation-check.py workspace/searxng-hermes`：`V` 英文整句 108 处，命中 108 / 仅中间产物 0 / 未命中 0；`S1`=0、`S2`=0、`S4`=0；**`C` 多副本一致 8 份副本、实际比对 12 组、0 处差异**（N>0）。

---

## 阶段 6：Obsidian 美化与发布
- [x] 已读取 Obsidian 输出规则
- [x] 用户已确认最终保存位置（vault_path + note_folder，或仅项目 output）
- [x] frontmatter、标签、Callout、双链已按 Obsidian 规则处理
- [x] 最终 Markdown 已保存到用户指定位置或 `./output/final_note.md`

> [P6] ✅ 已完成 {complete}

**P6 记录（发布到 vault，分册形态 B）**：
- 目标：`AI学习/Hermes Agent/SearXNG 自托管指南/`（P0 用户确认）+ `README.md` + `01-…`～`06-…`（P4→P5 用户确认组装方式 B）。
- 发布器：`workspace/searxng-hermes/_publish/publish_vault.py`（**纯机械变换层**，不改内容/引文/措辞）：章文件加 frontmatter + 导航行；正文 ATX 标题层级整体下移一级（`## 第 N 章`→`# 第 N 章`、`### N.M`→`## N.M`，与 vault 既有分册一致，正是校验器 `chapter_block` 明示抹平的「④ 标题层级下沉」）；代码围栏内 `#` 注释不参与变换；README 由 `output/final_note.md` 前言切片 + 目录/阅读顺序/分册关系/快速上手/更新记录构成。
- 发布器内置四道自检（不过则不写文件）：A 变换可逆（逆向还原后与源章正文逐字相等）；B 源文件正文标题只到 `###`；C 引文对照数据行数源/成品两侧一致（8/5/5/5/6/4）；D 每条导航与目录指向的目标文件真实存在。
- 成品：7 个文件 / 55,567 B（约 54.3 KB，1024 进制）— README 4567 B；ch1 9222 / ch2 11735 / ch3 8377 / ch4 6383 / ch5 7748 / ch6 7535 B。
- 引文门（`note-beautifier` Step 4，逐个成品跑）：`python3.12 .claude/scripts/note-citation-check.py workspace/searxng-hermes --vault-note "AI学习/Hermes Agent/SearXNG 自托管指南/<文件>.md"` × 6 → 全部 `判定：✅ 无硬失败`；V 英文整句 112–119 处，命中 100% / 仅中间产物 0 / 未命中 0；S1=0、S2=0、S4=0；`C 多副本一致 9 份副本、实际比对 13 组、0 处差异`（新成品文件各被认到 1 章并纳入比对）。README 另跑 `--mode text`（V 108 命中 108 / S1=S2=S4=0；S3 193 处 / 去重 21 个全部为保留类：文档标签名、产品名、`API key`、`extract provider` 等技术词，无未译成句）。
- 结构门：`python3 .claude/scripts/check-md-structure.py "AI学习/Hermes Agent/SearXNG 自托管指南"` → 扫描 7 个文件、0 处可疑。
- 人工读成品：README 与第 3 章全文逐行读过，其余各章首尾与标题层级脚本复核；围栏外标题仅 `#`/`##` 两级（残留 `###` 0 处），无残留 `SOURCE:`/`END:` 标记。

---

## 阶段 7：MOC 同步
- [x] 已定位或创建 MOC 文件
- [x] 新笔记双链已加入 MOC
- [x] 已去重并更新摘要/标签
- [x] MOC 只保留索引，不复制正文

> [P7] ✅ 已完成 {complete}

**P7 记录**：
- MOC：`AI学习/Hermes Agent/Hermes Agent MOC.md`（`00_intent.md` 指定路径，非新建）。
- 四处改动：① frontmatter `updated` 2026-09-18 → 2026-10-07；② `> [!info] 目录导航` 由「五册并存」改「六册并存」并追加一行 `[[SearXNG 自托管指南/README|SearXNG 自托管分册]]` 摘要；③ 学习路径代码块追加一行 `↘ SearXNG 自托管分册：…`；④ `## 核心笔记` 表追加一行分册索引。
- 未复制正文：新增内容均为「一行说明」级摘要（callout bullet / 表格说明列 / 路径图一行）。
- 验证：`python3 .claude/scripts/check-md-structure.py "AI学习/Hermes Agent/Hermes Agent MOC.md"` → 0 处可疑；脚本逐条解析 MOC 内全部 wikilink → 死链 0 个；callout 内分册 bullet 6 条、核心笔记表分册行 6 行，均与新分册一致。

---

## 用户确认记录

| 阶段 | 确认内容 | 时间 |
|------|----------|------|
| P4→P5 | 用户在 P4→P5 门确认组装方式 **B（拆分为分册）**；并确认字数不返工、`.example` 未入表保持现状 | 2026-10-07 19:05 |
| P3 | 用户确认大纲：保持 6 章（「开启 JSON API」独立为第 3 章） | 2026-10-07 18:28 |
| P1 | 用户选择方向 A：全量主线（是什么→怎么搭→怎么接 Hermes→验证排错，约 5–6 章） | 2026-10-07 18:14 |
| P0 | 用户确认 Phase 0 方案：概念+实战混合、上手深度、输出到 AI学习/Hermes Agent/SearXNG 自托管指南、与 Hermes 同机本地 Docker | 2026-10-07 17:59 |
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
| 2026-10-07 | P4 | 第 3 章引文对照第 1 条：原句 `If you want to consume the results as JSON, CSV, or RSS...` 实际在 `l2-6_search_api.html:444-445`，被标成 `L2-4 · l2-4_settings_search.html:444-445`（该两行是 YAML `default_lang`/`ban_time_on_fail`）。校验器 V 只验「引文能否回源命中」，不验「出处文件 ID 是否即引文所在文件」，故此缺陷不被自动校验覆盖。 | 父流程 grep 回源核对时发现，已改 `出处` 为 `L2-6 · sources/l2-6_search_api.html:444-445` 并复跑校验（V 全绿）；把「出处列必须逐行 grep 回源确认所在文件」写进第 5、6 章 dispatch 作为纪律。 |
| 2026-10-07 | P6 之后 | 第 3 章把 `docker cp` 写成开 JSON 的必经「第一步」，与同册自己给出的 compose **自相矛盾**：两条路径都把宿主目录绑定挂载到容器 `/etc/searxng`，容器首启生成的 `settings.yml` 本就落在宿主，取回/写回是多余的（第 2 章还有两处说法与之呼应）。用户读第 3 章时指出。 | 已在 canonical 章文件改正（第 2 章 3 处、第 3 章 3.1 与整节 3.3 + 新增脚注 `[^c3-j/k/l]`），并机械回填 `_merged.md` / `output/final_note.md` / 7 个 vault 成品 / README 快速上手 / MOC 摘要；复跑引文校验（V 全绿、`C` 9 副本 13 组 0 差异）与结构自检（0 处）。本文件字数/体积已按取数纪律当场重取。 |

---

## 方向调整记录

| 时间 | 原方向 | 新方向 | 是否需要补充收集 |
|------|--------|--------|-----------------|
| | | | |

---

## 最终产出

> **取数纪律**：下表的体积 / 字数 / 章数 / 锚点数 / Callout 数必须**当场重新运行取数或重新计数**，并把命令留在「取数命令」一行；不要从上下文里的历史输出誊抄，也不要手算合计。产物在记录之后又被改动时，grep 同一数字的**所有**出现处一并更新（同一组数字常同时出现在阶段段落与本节）。

- **笔记类型**：概念 + 实战混合（`note-style.md`「入门优先」档：结论先行 + 比喻 + 术语解释 + 代码后置）
- **总字数**：成品正文汉字 **7811**（与源章合计一致，发布变换不改一个正文字符）；含 frontmatter/导航壳的逐文件计数合计 **8866 汉字 / 54.3 KB**
- **章节数**：6 章 + README 入口页（分册形态 = `README.md` + `01-…`～`06-…`）
- **输出格式**：Obsidian Markdown 分册（每章独立笔记，章间前后导航双链，引文对照表逐章保留）
- **取数命令**：`python3 -c "import re,glob; [print(p, len(re.findall(r'[一-鿿]', open(p,encoding='utf-8').read()))) for p in sorted(glob.glob('AI学习/Hermes Agent/SearXNG 自托管指南/*.md'))]"`（口径＝全文汉字含表格/脚注，当场重跑）
- **文件路径**：`workspace/searxng-hermes/output/final_note.md`（单文件组装件，8379 汉字 / 52105 B）＋分册成品 `AI学习/Hermes Agent/SearXNG 自托管指南/`
- **Obsidian Vault**：项目根即 Obsidian vault 根；发布目录 `AI学习/Hermes Agent/SearXNG 自托管指南/`（vault 相对路径，不写机器绝对路径）
- **MOC 路径**：`AI学习/Hermes Agent/Hermes Agent MOC.md`
