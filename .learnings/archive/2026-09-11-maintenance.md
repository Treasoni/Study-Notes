# 归档 — 2026-09-11 maintain-learnings 维护

由 `/maintain-learnings` 触发。本文件记录本轮**已在源头修复并验证**的活跃条目，
以及对应的机制改动。条目从 `LEARNINGS.md` / `ERRORS.md` 移出，`RULES.md` 中的简短铁律保留。

审计入口：

```bash
python3 .claude/skills/maintain-learnings/scripts/audit_learnings.py \
  --root . --skills-dir .claude/skills --rules-file CLAUDE.md --hooks-path .claude/hooks
```

审计把 `workflow-todo-state` 标为唯一有源头的活跃簇，指向 `.claude/skills/workflow-todo-state/SKILL.md`。
溯源后确认 SKILL.md 本身是正确的，**真正的缺陷在它下游的 workflow state template**。

---

## 1. [LRN-20260911-008] `todo-state.sh` 命令集与最终阶段 quality_gate

**原记录摘要**：脚本只实现 `start|complete|skip|block`，没有 `confirm`；`complete` 前必须先
`start`；最后一个阶段要求 frontmatter `quality_gate: passed`，否则报
`final phase requires quality_gate`。本次收尾连撞这两道门，靠手工补 frontmatter 才通过。

**根因（溯源结果）**：不是 SKILL.md 写错——`.agents/skills/workflow-todo-state/SKILL.md`
第 34–37 行只列 `start|complete|skip|block`，第 77 行也已列出 `quality_gate*` 三个字段，全部正确。
缺陷在**三个 workflow 的 `state-template.md` 未跟随脚本重写而更新**：

| 文件 | 旧（失效） | 新 |
| --- | --- | --- |
| `.codex/workflows/batch-note-update-flow/state-template.md` | 5 个脚本已不读的字段 | + `quality_gate` / `_owner` / `_due` |
| `.codex/workflows/learning-note-flow/state-template.md` | 同上 | 同上 |
| `.codex/workflows/legacy-note-import-flow/state-template.md` | 同上 | 同上 |

移除的失效字段（当前脚本 `frontmatter_value` 从不读取）：
`confirmed_phases`、`skippable_phases`、`mode_dependent_skips`、`allowed_modes`、`mode_change_phase`。
新增的必需字段：`quality_gate: pending`、`quality_gate_owner: ""`、`quality_gate_due: ""`
——与 canonical 参考模板 `.agents/skills/workflow-todo-state/references/basic-state-template.md` 对齐。

**影响面**：任何按旧模板新建的 workflow run，都会在最后一个阶段撞同一道门。

**修复路径**：
1. 补齐三个 `state-template.md` 的 frontmatter（脚本化改写，逐文件打印改动计数）。
2. 在 `.codex/scripts/workflow-health-check.sh` 增加**自动守卫**：遍历
   `.codex/workflows/*/state-template.md`，缺 `^quality_gate:` 或仍含上述失效键即 `fail`。
3. 删除 2026-08-15 迁移遗留的 8 个 `.bak.20260815004244` 快照（含
   `.codex/scripts/todo-state.sh.bak.20260815004244`——它仍在文档里描述已不存在的
   `confirm` 动作，是本次排查中的误导源）。
4. 同步到 `.claude/` 镜像。

**验证方式**：
- 守卫双向量测试：三个已修模板 `quality_gate=1 dead_keys=0`（不误报）；伪造含
  `confirmed_phases` 且缺 `quality_gate` 的 frontmatter，两条守卫均按预期触发。
- `bash .claude/scripts/workflow-health-check.sh` → `Workflow health check passed.`
- `python3 .codex/platform/manifest-registry.py --root . validate` → 60 artifacts 通过。
- `python3 .agent-sync/sync_agents.py --root . --check --scope workflows|scripts` → 无漂移。

**处理结果**：已修复并验证，条目移出活跃文件。`RULES.md`「Watch For」保留简短铁律。

---

## 2. [ERR-20260911-007] 父 agent 在 prompt 里改写来源论断导致伪引证

**原记录摘要**：第二章 2.9.1 出现「官方口径是：`Run`/`RunOnce` 这两个键本身不执行任何操作
[S19]」，而官方原文是「使程序在用户登录时运行」。伪论断落到 callout 与本章小结两处。
根因是**父 agent 在派发 prompt 里把来源论断转述成陈述句并保留来源 ID**，子 agent 无法区分
原文与概括，照抄后形成伪引证。

**修复路径**：在 `.agents/skills/research-collector/SKILL.md` 的 `## Source policy` 增加硬约束
（canonical 源）：

> **Never paraphrase a source claim into a dispatch prompt.** …pass source IDs, paths, and
> anchors — not a rewritten sentence carrying a source ID. …If a claim must appear in the
> prompt, quote it verbatim inside quotation marks, or label it explicitly as an unverified
> summary. When reviewing a chapter, re-open the source for every "官方口径是" /
> "the official wording is" claim instead of only checking that a source ID is attached.

选择该位置的理由：`research-collector` 拥有 source policy 且是**唯一同时定义了「来源如何
交给下游」的 canonical 同步技能**（做出该决定时 subagent 定义还不在同步范围内，`.codex/agents/`
与 `.claude/agents/` 各存一份；**该缺口已在本轮一并修复，见文末「本轮意外发现」**）。
manifest 版本 `2.1.0 → 2.2.0`。

**验证方式**：
- `.agents/skills/` 与 `.claude/skills/` 的 SKILL.md/manifest 均已同步（`--scope skills --check` 无漂移）。
- skill frontmatter 元数据断言通过。
- manifest registry 校验通过。

**处理结果**：已修复并验证，条目移出活跃文件。`RULES.md`「Do」保留简短铁律。

---

## 3. [LRN-20260911-010] 加双链前核实目标存在、锚点可解析

**原记录摘要**：发布后加双链时，(1) 提议阶段举了 `[[NTFS]]`、`[[注册表]]` 这类 vault 中
并不存在的目标，照做即死链；(2) `[[Note#2.7.3 主路径：导出 \`.reg\` → …]]` 的锚点标题含
反引号与箭头，解析不稳。

**修复路径**：在 `.agents/skills/note-beautifier/SKILL.md` 的 `### 2. 双链使用规范` 增加
「落地前必做的两项校验」：目标必须逐条校验存在（`os.path.exists(target + '.md')`）；
锚点标题避开含反引号/箭头/竖线的标题，改链不含特殊字符的上级标题。
manifest 版本 `1.0.0 → 1.1.0`。

**验证方式**：`--scope skills --check` 无漂移；manifest registry 校验通过。

**处理结果**：已修复并验证，条目移出活跃文件。`RULES.md`「Watch For」保留简短铁律。

---

## 4. [LRN-20260905-007] 概念解释要「落到可见处」

**原记录摘要**：解释抽象概念须给「看得见、可代入」的落点；其 Suggested Action 要求把该
标准从 RULES.md 提升进 chapter-writer 的写作要求。

**溯源结果**：**该动作已经完成，无需再改**。`.codex/agents/chapter-writer.md`：

- 第 127–137 行：完整的「按顺序组织」写作要求 + 自检标准（遮住大白话后正文能否独立读懂）；
- 第 199 行：Quality Checklist 项「抽象概念解释有『可见落点』…」；
- 第 120–125 行：`[!tip] 大白话` Callout 要求与常用类比素材清单。

**处理结果**：Suggested Action 已在源头落地，条目移出活跃文件。

---

## 仍未归档（继续观察）

- `[LRN-20260911-009]` 超大笔记组装/校验走父进程 python；反向扫描定位插入点须同时跳过
  空行与 `---`。**尚未做源头修复**——该行为发生在父进程编排层，`note-assembler` 无 Bash，
  暂无自然归属的 skill 落点，暂由 `RULES.md` 承载。**未修复，故不归档。**

## 5. 本轮意外发现（已修复，2026-09-11）

两条都在用户确认「都修」后于同日修完，验证方式见本节末。

### 5.1 `[DRIFT] updated: CLAUDE.md` 是同步工具的 Windows 换行符误报

**结论：不是内容漂移。**

- 现象：`python3 .agent-sync/sync_agents.py --root . --check`（全量或 `--scope rules`）报
  `[DRIFT] updated: CLAUDE.md` 并**退出码 1**；其余四个 scope 均 `[OK]`。
- 取证（2026-09-11 复核）：
  - 用真实 `transform()` 把 `AGENTS.md` 转换后，与 `CLAUDE.md` **逐字节相等**（9843 B, md5 `907f89ad`）——
    即**内容零差异**，此前的路径映射猜测（`.agents/skills/`、`.codex/hooks.json` 未映射）**不成立**。
  - 真实原因：`sync_instructions()`（`sync_agents.py` 211–222 行）用**原始字节**比较
    `rendered_bytes(...)` 与 `target_path.read_bytes()`。而 `rendered_bytes`（186–189 行）走
    `read_text(encoding="utf-8")`，Python 的 **universal newline 会把 `\r\n` 折成 `\n`**，
    于是 expected 是 **LF-only（9709 B）**，磁盘上的 `CLAUDE.md` 是 **CRLF（9843 B）** → 恒不相等。
  - `sync_tree()`（192–208 行）有 `normalized()` 兜底把 `\r\n` 归一化，`sync_instructions()` **没有这个兜底**，
    所以只有 instructions 层（`CLAUDE.md`）误报。
- 影响：
  - 本机 `core.autocrlf=true`，仓库索引存 LF、工作区检出 CRLF；因此**全量 `--check` 在此机器上永远无法通过**，
    CLAUDE.md 里「最后运行全量 `--check`」这一步和任何以它为准的 pre-commit / CI 门都处于常红状态。
  - 若执行 `--apply`，会把 `CLAUDE.md` 重写为 **LF**（内容不变、行尾全变）。因 autocrlf 归一化，
    `git status` **看不到这个改动**——即「修好了」也修不掉真问题，只是把误报掩盖成脏的工作区行尾。
    本轮同步已在 `.claude/skills/**`、`.claude/workflows/**` 产生同样效果（镜像为 LF、canonical 为 CRLF）。
- **修法（已执行）**：没有补 `normalized()` 兜底——实测该兜底对 `CLAUDE.md` 无效（见下条），补了也修不好。
  改为在 `sync_agents.py` 中新增 `same_content()`，对两侧文本做**行尾归一化后再比较**，并让
  `sync_tree()` 与 `sync_instructions()` **共用**它。效果：仅行尾不同 → 既不算漂移、也不触发写盘（原先 `--apply`
  会把这类文件全部重写一遍只为换行尾）。
- **刻意没做**：没有改写入端的行尾策略（`--apply` 仍写 LF）。本机 `core.autocrlf=true`，索引存 LF，
  写 LF 在仓库层面是中性且正确的；改写入端属于另一件事，且需为二进制文件加保护，不在本次范围。
- 另需注意：`normalized()` 只替换 `"{name} hook"` / `"{id}-hook"`，**不替换裸 runtime 名**（`Codex` ↔ `Claude Code`），
  所以它对含运行时名的文件（如 `CLAUDE.md`）判定为不相等。行尾问题修掉后该兜底不再是 `CLAUDE.md` 的必经路径，
  其保守行为（不摘裸名 → 仍报差异）保留不动。

### 5.2 subagent 定义不在同步范围（`.codex/agents/` vs `.claude/agents/`）

- 现象：三份 subagent 定义两侧 md5 全部不同，而 `agents` **既不在 `PATH_KEYS` 也不在 `canonical_scopes`**，
  同步工具对它零覆盖——这正是本轮刚修完的「改了 canonical、下游副本没跟上」同一类 bug。
- **取证时发现的真正风险**：差异**不是双向的**，`.claude/agents/` 侧**严格领先**，多出 5 处经验
  （并行 writer 竞态、脚注命名空间 `[^cN-]`、Write 100KB 上限、教程章节按「文件/产物」组织、多章脚注去重）。
  若直接按 `.codex/agents` 为 canonical 跑 `--apply`，这 5 处会被**删除**。
- **修法（已执行）**：
  1. 先把 `.claude/agents/*.md` 反向归一化写回 `.codex/agents/*.md`，使 canonical 成为最完整版本；
     并用「往返一致」证明（`transform(new canonical)` 与现状 `.claude` 文件逐字节相等，EOL 归一后）。
  2. 再把 `agents` 纳入同步：`PATH_KEYS` / `SCOPES` 增加 `agents`；`codex.yaml` 增加 `paths.agents`
     并把 `agents` 写入 `canonical_scopes`；`claude.yaml` 增加 `paths.agents`。`load_profiles` 会强制两个
     profile 都声明 `paths.agents`，缺一即报错。
  3. 同步更新 `AGENTS.md` 第 6 条与 `.codex/rules/common/sync-workflow.md` 的区域枚举。
- **附带修掉的真 bug**：`CLAUDE.md` 第 5 条原先写「读取 `.codex/agents/{agent-name}.md`」——在 Claude runtime 里
  是错的；纳入 `agents` 后由 `transform()` 自动渲染为 `.claude/agents/`。

### 验证方式（5.1 + 5.2）

- `same_content()` 单元测试 5 例：字节相同 / 仅 CRLF-LF / 仅旧式 CR / 内容真不同 / 目标缺失，全部通过。
- `sync_tree()` 与 `sync_instructions()` 端到端各 3–4 例：仅行尾不同 → 0 漂移；内容真不同 → 1 漂移；
  目标缺失 → `created`；`--apply` 后再次 `--check` 干净。全部通过。
- **幂等性**：对 835 个受管文件取 md5 快照 → 全量 `--apply` → 再取快照，**零文件变化**。
- **方向正确性**：`git status` 中 `.claude/agents/` 变更文件数 = **0**（镜像未被改写，证明 5.2 第 1 步已把
  `.claude` 侧内容全部回收）。
- 全量 `--check` 退出码 **0**（修复前该门在此机器上恒为 1）。
- `manifest-registry.py --root . validate` → 60 artifacts 通过；`workflow-health-check.sh` → passed。
