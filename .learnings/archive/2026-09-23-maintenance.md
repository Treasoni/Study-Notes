# 2026-09-23 经验库维护（`/maintain-learnings`）

本次维护目标：把「教训已进 RULES、记录仍留在活跃文件」的 7 条记录逐条追回源头，
落到可执行机制后归档。所有修复先改 canonical（`.codex/`、`.agents/skills/`），
再同步镜像。

## 维护前审计

```
.learnings/LEARNINGS.md: 97 行   .learnings/ERRORS.md: 72 行   .learnings/RULES.md: 61 行
热点：markdown(活跃 5/合计 16)、general(2/12)、research(1/7)、interaction(0/19)
```

命中判定标准第 3 条（已写入 RULES 但仍在 ERRORS/LEARNINGS 中复发）：6 条命中，
另有 1 条（`LRN-20260912-011`）有明确 Suggested Action 但无 RULES 铁律。

---

## 归档 1：`LRN-20260912-011` workflow — vault 与 workspace 副本漂移未登记

- **原记录摘要**：`learning-note-flow` 运行 `openlist-webdav-rclone-docker` 已 `done`；此后
  走 `note-updater` 单篇更新 vault 笔记（`OpenList网盘挂载-02` +3 行、`-03` 约 83 行），
  工作区 `chapters/`、`output/` 未改动 → 两边同名副本必然长期漂移。根因：`current_phase: done`
  表示生产流程结束，不表示笔记冻结，后续单篇更新没有回写 workspace 的机制。
  Suggested Action：在 `note-updater` / `note-beautifier` 收尾检查里加漂移提示。
- **修复路径**：`.agents/skills/note-updater/SKILL.md` 新增 Workflow 步骤 6「vault / workspace
  漂移登记」——改动落在 vault 内时检查工作区同名副本，`current_phase: done` 的 run 必须登记
  「vault 已于 <日期> 更新，workspace 副本停留在 <日期>」并让用户二选一（重跑 note-assembler
  同步 / 明确弃用副本）。canonical 同步到 `.claude/skills/note-updater/SKILL.md`。
  `.learnings/RULES.md` 的 Watch For 增加同名铁律。
- **验证方式**：`.claude/skills/note-updater/SKILL.md` 与 canonical 逐字节一致（`sync_agents.py
  --check` 退出 0）；skill 元数据断言（frontmatter `name`/`description`）通过。
- **处理结果**：已修复；记录从 `LEARNINGS.md` 归档。

---

## 归档 2：`LRN-20260923-014` workflow — 并行写作多章时跨章共享口径未冻结

- **原记录摘要**：同一篇笔记第 1 章写 `method: "raw"`（据权威传输文档），第 5、6 章写
  `network: "tcp"`（照抄官方示例），两处配置互相矛盾。两章并行写作、各自都没错，错在没有共享
  口径；交付后靠跨章 grep 抓到，改了 6 处。Suggested Action：把「跨章口径表 + 交付后跨章 grep」
  写进 `learning-note-flow` 并行派发章节的检查点。
- **修复路径**：`.codex/workflows/learning-note-flow/workflow.md` 阶段 4 检查项新增两条，并新增
  「#### 并行写作的跨章口径（阶段 4）」小节：派发前冻结跨章口径表写进每个 dispatch、交付后对
  「可照抄的配置块」做跨章比对（附 grep 命令）、无来源可引的等价断言必须标为**推断**。
  RULES 第 43 行原有铁律保留。
- **验证方式**：canonical 与 `.claude/workflows/learning-note-flow/workflow.md` 全量
  `sync_agents.py --check` 退出 0；`workflow-health-check.sh` 双侧 passed。
- **处理结果**：已修复；记录从 `LEARNINGS.md` 归档。

---

## 归档 3：`LRN-20260923-015` + `ERR-20260923 todo-state` — 文档调用了未实现的动作

> 两条记录是**同一事故**（LEARNINGS 记教训、ERRORS 记错误），一并归档。

- **原记录摘要**：`learning-note-flow` 的 `workflow.md` 有 4 处调用 `todo-state.sh … mode P2 freeform`
  / `confirm P2 …`，而脚本动作白名单只有 `start|complete|skip|block`：「随性模式」分支在阶段 2
  收尾第一步就 `exit 2`（`unknown action: mode`）。更值得记的是化石——RULES 里早写着「没有
  `confirm`」，发现缺口的人没有修实现，而是把它固化成绕行规则。
- **修复路径（已在上一轮完成）**：canonical `.codex/scripts/todo-state.sh` 新增 `mode`（只改
  frontmatter `mode` 键）与 `confirm`（只追加 `## 用户确认记录`）；分发包、`SKILL.md`、
  `references/integration.md` 同步，manifest `0.1.0 → 0.2.0`；RULES 的绕行规则改写为现行语义。
- **修复路径（本次补齐）**：原 Suggested Action「每个动作都在脚本白名单内」此前没有落地机制，
  本次加进 canonical `.codex/scripts/workflow-health-check.sh`：解析每个
  `workflows/*/workflow.md` 里对 `todo-state.sh` 的调用，**按实际探针**（而不是手抄一份动作清单）
  逐个执行，命中 `unknown action` 即失败。三层自保：
  1. 控制组探针——已知动作 `mode` 在全新 state 副本上必须被接受，证明脚本真的走到了动作分发；
  2. 空绿保护——`probed_invocations == 0` 时直接失败（扫描没读到数据不算通过）；
  3. 成功时打印 `todo-state action guard: N invocation(s) probed`。
  调用点：`AGENTS.md` 与 `.codex/rules/common/sync-workflow.md` 把它写成 canonical 变更后的
  伞形收口命令（此前 `workflow-health-check.sh` **没有任何调用点**，属 RULES 第 59 行「守卫三问」
  的第一条不成立）。
- **验证方式**：
  - 正常态：canonical / 镜像双侧 `workflow-health-check.sh` passed，打印 `15 invocation(s) probed`；
  - 注入 1（定义里加 `frobnicate P1`）→ 报
    `Workflow definition calls a todo-state.sh action the script does not implement: frobnicate`，退 1；
  - 注入 2（把控制组动作改成 `modez`）→ 报 `Control probe failed: … rejected a known-good action`，退 1；
  - 注入 3（让扫描匹配不到调用）→ 报 `… the action guard verified nothing`。
  - `manifest-registry.py --root . validate` → 60 artifacts 通过。
- **处理结果**：已修复并具备三层自保；两条记录分别从 `LEARNINGS.md`、`ERRORS.md` 归档。

---

## 归档 4：`LRN-20260923-017` + `ERR-20260923 引文墙` — 逐字引文串成 828 字符段落

> 两条记录是**同一事故**（LEARNINGS 记教训、ERRORS 记错误），一并归档。

- **原记录摘要**：交付到 vault 的笔记 1.2 节，把 netfilter man page 的 8 处英文长引文用分号串成
  单个 828 字符段落，逐字准确、脚注齐全，但用户读不懂（「你这样写，让人很难去理解和看懂啊」）；
  同类形状还有 3.3、4.4。根因：写作规范只有「引文要逐字、要挂来源」，没有一条说引文该怎么摆放。
- **修复路径（已在上一轮完成，本次复核确认）**：`.codex/agents/chapter-writer.md` 写作规范已写入
  摆放判定（段落要摆 ≥3 处引文 / 含任一整句英文 / 长度 >300 字符 → 改「官方原文 / 说人话」两列
  对照表 + 结论单独成句），并写明反例边界「只有 1 处短引文时行内引用即可，不要套表」；验收清单
  增加可读性一项（遮住英文列仍能读懂）。第 144/147/154 行与 Quality Checklist 第 221 行可查。
- **验证方式**：`grep` 确认上述条款在 canonical `.codex/agents/chapter-writer.md` 中存在且已同步
  到镜像；`sync_agents.py --check` 退出 0。
- **处理结果**：源头机制已在位，本次仅复核后归档；两条记录分别从 `LEARNINGS.md`、`ERRORS.md` 归档。

---

## 归档 5：`ERR-20260923 note-assembler` — 章标题降级未级联到子标题

- **原记录摘要**：组装出的 `final_note.md` 里 `## 第一章：…`、`## 1.1 …`、`## 小结` 全在 `##`
  同一层级，渲染后大纲扁平。根因：降级按「章标题」这一个已知模式做替换，没有把它当成「整体
  下沉一级、所有后代标题跟着下沉」的层级变换。当时 note-assembler 自己报告了问题。
- **修复路径**：`.codex/agents/note-assembler.md`：
  - Step 4 第 1 条改写为**子树变换**语义——降级必须级联到章内 `## N.M`、`## 小结`、`####` 子节；
    并写明「只替换你认识的那个模式不算校验」，要求重新解析标题树断言 章 < 节 < 子节 严格递增，
    并打印 `heading levels adjusted: N`（N 小于「所有被降级章的全部后代」即说明级联提前停止）。
  - Quality Checklist 对应项改为「已重新解析标题树确认 章 < 节 < 子节 严格递减；章标题与节标题
    同级是缺陷，不是风格选择」。
  - `.codex/workflows/learning-note-flow/workflow.md` 阶段 5 检查项同步收紧（`## N.M`、`## 小结`
    随章标题一起下沉，已重新解析标题树确认逐层递减）。
  - manifest 版本：note-assembler `1.0.0 → 1.1.0`、learning-note-flow `1.1.0 → 1.2.0`。
- **验证方式**：`manifest-registry.py --root . validate` → 60 artifacts 通过；双侧
  `workflow-health-check.sh` passed；`sync_agents.py --check` 退出 0。
- **处理结果**：已修复；记录从 `ERRORS.md` 归档。

---

## 本次维护的边界与遗留

- 未触碰 `.learnings/` 之外的非机制内容；未做跨 profile 同步以外的配置改动。
- 发现但**未修**（超出本次范围，登记备查）：`.claude/scripts/workflow-health-check.sh` 的
  `this_dir` 仍是 `.codex`，因此 Claude 侧跑的是 canonical 的 agents/workflows/scripts 守卫，
  `.claude/agents`、`.claude/workflows` 自身不被本侧检查（`sync_agents.py --check` 仍能兜住漂移，
  属「注释与行为不一致」的潜在陷阱）。该发现此前已在 `2026-09-11-maintenance.md` 记录，本次复核
  仍然成立。
- 环境提示（非缺陷）：本运行时 Bash 工具的 PATH 里 `python3` 解析为 `/usr/bin/python3`（3.9.6），
  低于 `sync-workflow-routing.sh`/`sync-agents` 系列要求的 3.10+；用户登录 shell 解析为
  `/Users/zhqznc/miniconda3/bin/python3`（3.13.11），校验正常。判定脚本「能不能跑」时不要只信
  工具 shell 的 `python3`，必要时显式 `PYTHON=<3.10+> `。
- 发现但**未修**（与本次改动无关，纯属既有状态）：
  `python3 .agent-sync/bootstrap.py --root . --check` 报三处漂移——
  `created: .agent-sync/local/host.json`（该目录缺失且被 `.gitignore` 忽略）、
  `updated: .claude/settings.json`、`updated: .codex/hooks.json`。证据表明与本次维护无关：
  `git status --short .codex/hooks .codex/hooks.json .agent-sync/` 为空，本次未触碰任何 hook 渲染输入。
  已提交的 `.codex/hooks.json` 里 hook 命令是 `"python" …`，而本机 bootstrap 默认渲染 `python3`
  （非 Windows 分支），故判定为「本机从未跑过 `--apply`」而非新引入的缺陷。
  **不要顺手 `--apply`**：它会重写受跟踪的 hook 注册文件，属机器相关渲染，需用户确认后进行。