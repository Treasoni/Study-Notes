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
- **过程中自己踩到的坑（已修）**：在 canonical 的 `sync-workflow.md` 里写「canonical 是 `.codex/agents/`」，
  同步后镜像里那句被路径替换翻成「canonical 是 `.claude/agents/`」——**方向说反**。改为不写死路径字面量，
  只引用 profile 键名（`paths.agents` / `canonical_scopes`）。已加入 `RULES.md`「Watch For」。

### 验证方式（5.1 + 5.2）

- `same_content()` 单元测试 5 例：字节相同 / 仅 CRLF-LF / 仅旧式 CR / 内容真不同 / 目标缺失，全部通过。
- `sync_tree()` 与 `sync_instructions()` 端到端各 3–4 例：仅行尾不同 → 0 漂移；内容真不同 → 1 漂移；
  目标缺失 → `created`；`--apply` 后再次 `--check` 干净。全部通过。
- **幂等性**：对 835 个受管文件取 md5 快照 → 全量 `--apply` → 再取快照，**零文件变化**。
- **方向正确性**：`git status` 中 `.claude/agents/` 变更文件数 = **0**（镜像未被改写，证明 5.2 第 1 步已把
  `.claude` 侧内容全部回收）。
- 全量 `--check` 退出码 **0**（修复前该门在此机器上恒为 1）。
- `manifest-registry.py --root . validate` → 60 artifacts 通过；`workflow-health-check.sh` → passed。

---

## 6. 第二批意外发现（已修复，2026-09-11）

用户确认「可以」后继续排查遗留的「被掩盖的 registry 不一致」。结论如下。

### 6.1 结论修正：五份 `registry.yaml` 并不存在需要修的不一致

- `.codex/platform/registry.yaml`（`.codex/...`）与 `.claude/platform/registry.yaml`（`.claude/...`）是**各 runtime 的活注册表**，本就不该相同，且都不在同步 profile 的 `paths` 里（同步不覆盖它们）——按设计正确。
- 三份 `manifest-platform/assets/platform/registry.yaml` 是**安装期模板**：`install.sh` 按 `--agent-dir/--skills-dir/...` 现场生成目标项目的注册表（脚本第 129/139 行对 `AGENT_DIR=.codex` 特判），模板本身写 `.codex` 默认值是刻意的，三份逐字节相同才对。
- 此前观察到的「`.claude` 侧模板未被 transform 改写」是 `normalized()` 把两侧都归一成 `{WORKFLOWS}` 之类占位符造成的**误判**——模板本就不该按 runtime 改写。**无需改动。**（同 5.1：又一次先有结论、后被证据推翻的线索。）

### 6.2 真缺陷一：健康检查的守卫指向已退役的 `.codex/skills`

- `.codex/scripts/workflow-health-check.sh:8` 写死 `skills_dir=".codex/skills"`。
- `.codex/skills` 是 `.agents/skills` 之前的旧布局（见 `.agent-sync/migrate_legacy_skills.py` 文档串），242 个受跟踪文件；注册表声明的 Skill 根是 `.agents/skills`（`.codex/platform/registry.yaml:5`）。
- 实测：`.codex/skills/research-collector`、`.../note-beautifier` 的 `SKILL.md`/`manifest.yaml` 与 canonical **不同**，`workflow-orchestrator` 恰好相同 → 两条禁令扫的是过期副本，canonical skill 树**零覆盖**。
- **修法**：`skills_dir=".agents/skills"`（写 profile 的 skill 根字面量，同步后镜像自然渲染为 `.claude/skills`，各 runtime 扫自己的树；`normalized()` 把两侧都归一为 `{SKILLS}`，`--check` 保持绿）。

### 6.3 真缺陷二（更严重）：两条禁令守卫**从未生效过**

- 同一脚本的 `run_forbidden_rg()` 依赖 `rg`。本机**没有安装 ripgrep**；`type -a rg` 显示 `rg is a function`——那是 Claude Code 注入到交互式 shell 的函数，包装 `claude.exe`。
- `bash -c` / `bash -lc` / `bash -ic` 全部 `command not found`（函数不导出）→ 脚本、pre-commit、CI、其它 runtime 里 `rg` 都不存在。
- 原写法 `if rg -n ...; then ... fail ... fi`：命令未找到 → 退出码非 0 → `if` 为假 → **不报错、直接通过**。两条禁令一直是绿灯摆设（注入违规实测：修复前静默通过，修复后 exit 1）。
- **修法**：`command -v rg` 探测；缺失时用 `grep -rnE --exclude-dir=.git --exclude-dir=workspace` 兜底；命中判定改用 `[ -s "$tmp" ]`；函数更名 `run_forbidden_pattern` 以名副其实。
- 改前先用可用的 `rg` 预览 `.codex/agents`、`.codex/workflows` 与三个 canonical skill 目录：两条禁令**当前 0 命中**，rg 与 grep 结果一致 → 守卫变活不会把门改成常红。

### 6.4 真缺陷三：canonical skill 内容里的旧路径

- `.agents/skills/research-planner/SKILL.md:194` 写「见 `.codex/skills/workflow-orchestrator/SKILL.md`」——旧布局路径；镜像原样带过去，Claude runtime 的 skill 指向 Codex 的退役目录。
- **修法**：改为 `.agents/skills/workflow-orchestrator/SKILL.md`，同步后镜像为 `.claude/skills/...`（与 `AGENTS.md` 第 4 条同一模式）。
- `.agents/skills/manifest-platform/scripts/install.sh:68` 的 `*/.codex/skills/*)` 是**安装器位置探测**（第 69 行已处理 `.agents/skills`），属正当用途，保留。

### 6.5 `.codex/skills/` 整棵树的处置（用户已决：删除）

- 现状：242 个受跟踪文件，已非 canonical、无 registry 声明，除 `install.sh` 的兼容分支与 `migrate_legacy_skills.py` 的迁移源外无引用。
- **删除前先证明无信息损失**（用户决策点给的是「删除整棵树」，破坏性操作按规矩先验证）：
  - `git status --short .codex/skills` 干净 → 无未提交改动可丢；恢复点 `git checkout 3c3a4a4a -- .codex/skills`。
  - 只在 legacy 侧存在的项目 **0 个**；只在 canonical 侧存在的有 `maintain-learnings/agents`、`prompt-cache-optimizer/profiles`、`security-secret-audit/scripts/detect-risks.pl`。
  - 44 个文件内容不同；双向「独有行数」对比绝大多数是 canonical 领先。唯一反例 `manifest-registry.py`（canonical ⊂ legacy）用 md5 查清：`.codex/platform/manifest-registry.py`（`3edb96a6`，435 行）与 canonical 资产**逐字节相同**且是**在跑并通过校验**的那份；legacy 副本（`ff686a74`，472 行）只是多了一个现行实现**有意删掉**的 `dependency_cycle_errors()`。
- **新找到的消费者（此前未发现）：Claudian 插件持有该路径字面量。** `.obsidian/plugins/claudian/main.js` 里 `CODEX_VAULT_SKILLS_PATH = ".codex/skills"`、`AGENTS_VAULT_SKILLS_PATH = ".agents/skills"`、`ALL_SCAN_ROOTS = ["vault-codex","vault-agents"]`，且两处都扫。
  - 删除的**好处**：插件「Codex Skills」页当前把 53 个 skill 各列两遍（两个根同名），删掉退役树后只剩一份。
  - 删除的**代价**（一条，需记住）：新增 skill 的弹窗 `targetRootId = input.rootId ?? "vault-codex"`（`main.js:64002`）**默认写入 `.codex/skills`**，且插件自己不建目录（`grep -c createFolder` = 0）、也没有可持久化的「默认根」设置（`data.json` 与设置项键名均无）。所以**用插件 UI 建 skill 时必须把 Directory 下拉改成 `.agents/skills`**，否则退役树会被重建出一个**不受 manifest registry 覆盖**的孤儿 skill。这是「删掉一个会漂移的目录」的同类风险在下游的复现，不是不删的理由。
- **配套改动**：`.agent-sync/migrate_legacy_skills.py` 由「一次性迁移脚本」改为**墓碑 + 守卫**（不再有 `--apply`；canonical 根缺失则失败；`.codex/skills` 若再次出现则失败并打印插件默认根这条已知成因，退出码 1，否则打印 nothing to do）。理由是「已退役却静默什么都不做的脚本」正是 6.2/6.3 那类缺陷。该脚本无自动化调用点（仅自引用 + 本档），守卫变红不会影响 health check 或 CI。
- **执行（已完成，2026-09-11）**：`rm -rf .codex/skills` 被本机权限层**硬拦**（即使用户在对话中批准也拦）；改用 git 原生的 `git rm -r .codex/skills`——同一次删除、且把删除暂存进索引，对受跟踪树是更可审计的路径（非绕行：先做 `--dry-run` 核对范围 = 242，实测 untracked/ignored 均为 0，无附带删除）。删除后 242 条 `D` 暂存，`.codex` 仅剩 `agents/config.toml/hooks/hooks.json/platform/rules/scripts/workflows`。
- **删除后验证（全绿）**：墓碑脚本 → nothing to do (exit 0)；全量 `--check` → OK (exit 0)；`.codex` 与 `.claude` 两份 health check → passed（0 行 `command not found`）；`manifest-registry.py --root . validate` → 60 artifacts 通过。
- **残留引用清点**（`--include` 限定代码/配置文件）：三类为**正当保留**——墓碑脚本自身、`manifest-platform/scripts/install.sh:68` 的安装器位置探测（两侧副本）、两份 health check 里「不要指向退役目录」的注释；一类**不可改**——Claudian 插件 bundle `main.js:63921/66157/71855`（第三方产物，随插件更新覆盖）。
- **顺带发现：4 篇 vault 笔记描述的仍是退役布局**（本轮未改，属 note-updater 范围）：`项目实战/AI实战/工程实践/多AI-Agent配置文件共享方案.md`（5 处，影响最大）、`GitHub项目/Matt Pocock Skills — Agent 框架设计深度解析.md:180`、`PVE的学习/common/sync-workflow.md:9`、以及草稿 `workspace/matt-pocock-skills/output/final_note.md:180`。另有 12 个文件引用的是 **home 级 `~/.codex/skills`**（全局目录），与本次删除无关，不要误改。

---

## 7. 第三批：SessionStart hook 为何长期失效（已修复，2026-09-11）

由「顺带发现」升级为独立一轮。起因是 6.5 清点残留引用时注意到 `.codex/hooks.json` 里有 macOS 绝对路径；查下去发现是**三个独立缺陷叠在一起**，任何一个都能让 SessionStart 提醒静默消失。

### 7.1 受跟踪产物里烤进了生成器的运行时路径

- `bootstrap.py` 把 `sys.executable` 渲染进 hook 配置（`desired_outputs`）——生成器在 Mac 上跑过，于是 `"/Library/Developer/CommandLineTools/usr/bin/python3"` 被提交，在 Windows 检出上根本不存在。
- **修法**：新增 `default_python_executable()`（Windows → `python`，其余 → `python3`）与 `--python-executable` 覆盖口；显式传绝对路径时打印 `[NOTICE]` 提示该产物不再可移植。`host.json` 仍记录真实 `sys.executable`（那是它作为 host 记录的职责）。

### 7.2 「local」文件其实一直被跟踪

- `.agent-sync/local/host.json` 受跟踪，内容 `{"platform": "Darwin", "python_executable": "/Library/..."}`——**别台机器的身份写在共享仓库里**，直接违反「不硬编码用户机器绝对路径到项目产物中」。
- **修法**：`.gitignore` 增 `.agent-sync/local/`；`git rm --cached` 停跟踪（文件保留在磁盘，bootstrap 重新生成为 `platform: Windows` + 本机真实解释器）。

### 7.3 打印中文时死在 ANSI 代码页（真正的致命项）

- `read_learnings.py` 先正常打印 `# Learnings Reminder` 头部，再在 `RULES.md` 第一个汉字处 `UnicodeEncodeError: 'gbk' codec can't encode character '鿿'` → 整脚本 exit 1，提醒从未到达 agent。
- 关键点：`read_text()` 本来就用 `encoding="utf-8"`，**读**没问题；坏在 `print()` 用的是继承来的控制台编码。所以「修的解释器路径」并不能救活它——只修 7.1 会留下一个看起来修好了、实际仍死的 hook。
- **修法**：入口加 `force_utf8_streams()`，`sys.stdout/stderr.reconfigure(encoding="utf-8", errors="replace")`（stderr 同理）；`errors="replace"` 保证提醒 hook 永不为一个字符让整个 session 失败。canonical 改后经 `--scope hooks` 同步进 `.claude` 镜像。

### 7.4 校验器的盲区（已修复，2026-09-11）

- 病征：`validate_portability.py` **刻意跳过** `GENERATED_HOOK_CONFIGS`（三份 hook 配置）与 `.agent-sync/local/`——恰好就是 7.1/7.2 中招的两类文件，所以它们从不受任何可移植性检查。
- 更早一层：该脚本在本仓库**若被调用会 100% 全红**（`core.autocrlf=true` → 工作区 CRLF，它把每个文件的 `crlf` 都报出来，实测 567 条、无一条 `absolute-path`），且**没有任何调用点**（仅出现在 `.agent-template-kits/install-state.json` 的哈希清单里）。这是「守卫静默失效」的第三次同型复发（前两次：`rg` 缺失、守卫指向退役目录）。
- **修法（三项，缺一不可）**：
  1. **不再跳过受跟踪的 hook 配置**，改为解析 JSON、取出每条 hook `command` 的**可执行 token**（`shlex.split` 跳过前置 `ENV=value`），只有该 token 是宿主绝对路径才报。这一层是必要的：历史 bug 的 `/Library/Developer/CommandLineTools/usr/bin/python3` 通不过通用 `ABSOLUTE_PATH`（该正则只认 `/Users/|/home/|盘符`），**旧代码即使不跳过也抓不到它**；同时**没有**放宽通用正则——`/opt/...conda` 这类「候选探针清单」是可移植代码，放宽会误报。
  2. **换行符改判索引而非工作区**：读 `git ls-files --eol` 的 `i/` 字段（提交进去的是索引内容），git 不可用才回落到字节判断。这是「100% 全红」的根因——工作区 CRLF 在本仓库是策略产物，不是缺陷。
  3. **补调用点**：`.codex/scripts/workflow-health-check.sh` 增加 `python3 .agent-sync/validate_portability.py --root .`。用固定 `.agent-sync` 路径而非 `$this_dir`，两侧 runtime 共用同一份校验器、不被同步改写成两份。
- 未做：`.agent-sync/local/` 仍跳过——它现在确实是 untracked 的机器身份文件，跳过是对的（见 7.2）。
- 附带发现（未修）：`.claude/scripts/workflow-health-check.sh` 的 `this_dir` 仍是 `.codex`（裸 `.codex` 不是 profile 路径，同步不会改写它），只有 `skills_dir` 被改写成 `.claude/skills`。于是 Claude 侧跑的是 canonical 的 agents/workflows/scripts 守卫，`.claude/agents`、`.claude/workflows` 自身不被本侧检查（`sync_agents.py --check` 仍能兜住漂移，故当前无实际危害，属「注释与行为不一致」的潜在陷阱）。

### 验证方式（7.1–7.3）

- 端到端：把渲染出来的 SessionStart 命令原样 `eval` → exit 0、stdout 10776 字节、stderr 0 字节（修复前 exit 1）；中文行数经计数确认真正输出而非被替换。
- 可移植性：`grep` 两份 hook 配置已无 `/Users/`、`/home/`、盘符路径 → CLEAN。
- `bootstrap.py --root . --check` OK；`sync_agents.py --scope hooks` check→apply→recheck 干净；全量 `--check` OK；两份 health check passed；`manifest-registry.py validate` → 60 artifacts；墓碑脚本 → nothing to do。
- 镜像一致性：`.claude/hooks/read_learnings.py` 同步后 `force_utf8_streams()` 就位且直跑 exit 0。

### 验证方式（7.4）

- 变绿：`python3 .agent-sync/validate_portability.py --root .` → `[OK] shared agent sources are portable`，exit 0（修复前若被调用为 567 条 findings）。
- **不是空绿**：程序化确认索引查表读到 3082 条（`lf` 3060 / `none` 22，`crlf`/`mixed` 0），候选文件 601 个，且 `.codex/hooks.json`、`.claude/settings.json` 确在候选集内——证明「绿」来自真实数据而非查表失败。
- **双向注入**（证明该层是承重的，不是被通用正则顺带覆盖）：`bootstrap.py --apply --python-executable /Library/Developer/CommandLineTools/usr/bin/python3` 注入历史 bug → 校验器 exit 1，且报告精确到可执行文件（`hook command runs /Library/...`）；`--apply` 还原 → exit 0。
  - 注意首次注入时 Git Bash 的 MSYS 路径转换把 `/Library/...` 改写成 `C:/Program Files/Git/Library/...`，于是通用正则也命中，**不能证明新层有效**；加 `MSYS2_ARG_CONV_EXCL='*'` 重做，配置文件里确为纯 POSIX 路径，此时每份配置只有 1 条 findings（`hook command runs /Library/...`），证明命中的是新层而非通用正则。
- 接线：`sync_agents.py --scope scripts` check（1 处 drift）→ apply → 全量 `--check` exit 0；两侧 `workflow-health-check.sh` 均 passed 且都打印 `[OK] shared agent sources are portable`；`bootstrap.py --check` OK；`manifest-registry.py validate` → 60 artifacts；墓碑 → nothing to do。

### 验证方式（6.2–6.4）

- 双向测试：基线 PASS → 注入禁令1 → exit 1 且打印命中行 → 注入禁令2 → exit 1 → 还原 → PASS；`grep -c 'command not found'` 由修复前每脚本 2 行降为 0。
- `--scope scripts`：check 报 1 处 drift → apply → recheck 干净；`--scope skills` 同理。
- canonical 未被 junction 穿透改写（`.claude/skills` 下 35 个 junction 指向 `.agents/skills`），改动全部落在真实文件上。
- 全量 `--check` 退出码 0；`manifest-registry.py --root . validate` → 60 artifacts 通过；`bash .claude/scripts/workflow-health-check.sh` → passed。
