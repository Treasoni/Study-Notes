# Token / 缓存优化报告（2026-09-14）

**Date:** 2026-09-14
**Scope:** Claudian（Obsidian 插件）+ Claude Code CLI；子代理层计入；Codex 仅作为下游复用同一份提示缓存规则
**Plan:** `/grill-me` → `/grilling` 设计树（Q1–Q23 全部确认后执行）；执行入口 `prompt-cache-optimizer`
**Status:** 落地完成；验收窗口进行中（协议见 §6）

关联文档：`docs/superpowers/reports/2026-06-02-token-cost-optimization-verify.md`（六月方案，其中合并脚本职能由本次 `merge_files.py` 复活）、`.llm/prompt-cache/README.md`（遥测设施与守卫手册）。

## 1. 结论摘要

1. **修复了测量盲区**：子代理转录此前完全不在账本内——它占全价输入的 **58.8%**（15.55M / 26.47M）。修复前任何「优化」都无法证明对最大的那块有效。
2. **冻结了可复算的基线**：`.llm/prompt-cache/baseline-2026-09-14.json`（8,972 事件），并由 `cache-guard.py` 把验收协议变成可执行判定（生成侧/校验侧共用同一份统计代码）。
3. **落地 5 组变更**：仪表修复（A1）、子代理层削减（A2）、主会话侧治理（A3）、规则/工件修订（A4）、守卫与基线（A5）。
4. **预期效果为估算而非实测**：按杠杆估算主会话全价输入 −32% ~ −57%（与批准计划一致）；是否达标由 §6 协议在 **7 天或 10 个上下文** 后判定。
5. 命中率（95.8% 全量 / 97.4% 主会话）**已无上行空间**，只作护栏：它下降即视为异常。

## 2. 基线与测量口径（2026-09-14 冻结）

窗口 2026-08-15 → 2026-09-14；按消息 id 去重；冻结时切点 `2026-09-14T09:54:04.771Z`。

| 层 | 规模 | 全价输入 | 缓存读取 | 命中率 | 每上下文全价输入中位数 |
| --- | --- | --- | --- | --- | --- |
| 主会话 | 75 会话 / 4,604 事件 | 10,916,719 | 406,293,248 | 97.4% | 99,786（p25 52,703 / p75 212,502） |
| 子代理 | 446 代理 / 4,368 事件 | 15,554,020 | 200,093,440 | 92.8% | 29,429（p25 18,675 / p75 41,500） |
| 合计 | 8,972 事件 | **26,470,739** | **606,386,688** | 95.8% | — |

- **主指标 = 全价输入（`input_tokens`）**，按上下文（会话 / 子代理转录）取中位数；**命中率只作护栏**。
- 扇出：**5.95 个子代理上下文 / 主会话**——批量化的主要战场。
- 子代理内部分布：chapter-writer 类占子代理全价输入的 45%（7,070,249），general-purpose 4,764,450，note-assembler 2,014,625。
- 可复算性：基线由 `python3 .llm/prompt-cache/cache-guard.py --freeze` 从账本生成（教训：文档里写死的基线会腐烂，见 README「基线」节）。
- `cache_read_price_ratio = 0.1` 仅用于**计费估算**字段，不是实测价格；判定不看它。

## 3. 落地变更

### A1 · 仪表修复（子代理进账本）

- `.llm/prompt-cache/collect-usage.py`：追加扫描 `<project>/<session>/subagents/agent-*.jsonl`，以 `request_type="subagent"` 落盘，`metadata` 带 `layer` / `parent_session` / `attribution_agent`；保留原幂等键与去重语义。SessionEnd hook 路径经由 `transcript_path.parent` 自动覆盖该会话的子代理，无需改 hook。
- schema 未改：`request_type` 与 `metadata` 本就是自由字段。
- 回填：dry-run 4429 → 实际 +4431 事件，重跑 +0（幂等）。
- `.llm/prompt-cache/README.md`：补采集范围、字段映射、基线表与守卫手册；标注两条历史基线均已失效。

### A2 · 子代理层削减（最大一块）

- **新增 `.codex/scripts/merge_files.py`**：通用确定性合并（`--input-dir` / `--pattern` / `--output`，默认 `<dir>/_merged.md`；跳空文件与 `status: failed`；HTML 注释分隔 `<!-- SOURCE: name | N bytes --> … <!-- END: name -->`；退出码 0/1/2；纯标准库）。
- **新增 `.codex/scripts/note-digest.py`**：大文件有界摘要（frontmatter 摘要 + 标题树 + 每节首段摘录 + 体积统计），替代 >15 KB 的整文件读取。
- `.codex/agents/chapter-writer.md`：每批 **≤3 章**、同批续写不重读材料、章间确认保留；一次写不完时的降级路径写死；**顺带修掉一处既有矛盾**（「After saving」曾要求子代理自行编辑 workflow state file，与「状态由 orchestrator 集中推进」冲突）。
- `.codex/agents/note-assembler.md`：优先读父流程产出的 `chapters/_merged.md`（有则不再逐章读取），无则回退逐章。
- `.codex/workflows/learning-note-flow/workflow.md`：P1 要求 2–3 个批量子代理并行探测（同类并发 ≤4）；P4 增派发约束；P5 增预合并步骤与 `_merged.md` 目录项。
- `.agents/skills/research-collector/SKILL.md`：扇出上限（每阶段 ≤3 子代理、同类并发 ≤4、优先续写而非新增兄弟代理），禁止「一源一代理」。
- 新增 `.codex/rules/common/context-discipline.md`（规则层）：读文件（>15 KB 先 digest、多文件先 merge、下游只回结论）、派发子代理（按批不按单元）、维护（走 `.agent-sync`）。

### A3 · 主会话侧

- **推理旋钮降档（已生效于配置文件）**：`.claudian/claudian-settings.json` 的 `effortLevel` `max → medium`、`thinkingBudget` `xhigh → medium`、`savedProviderEffort.claude` `max → medium`。
  - **机制判定（读插件 bundle 得出）**：Claude provider 的 `isAdaptiveReasoningModel` 恒为真，因此**生效旋钮是 `effortLevel`**（CLI 参数 `--effort <值>`）；`thinkingBudget` 在该 provider 下不生效（sanitize 逻辑还会删除其 saved 副本，与文件里 `savedProviderThinkingBudget = {}` 一致）。按批准计划两个旋钮同降，避免将来切换 provider 时继承旧值。
  - 合法取值 `low|medium|high|xhigh|max`；默认 `high`。
  - **生效条件**：Claudian 在内存中持有设置，需**重载插件 / 重启 Obsidian** 后新建会话才用新值；守卫会盯着是否被静默回写。
- **新增 `note-digest.py`**（见 A2）承担「不整读大文件」的机械部分。

### A4 · 规则 / 工件修订

- 全部改 canonical（`.codex/*`、`.agents/*`、`AGENTS.md`），经 `.agent-sync` 同步到 `.claude/*`、`CLAUDE.md`；生成目录未手工编辑。
- manifest 版本：`chapter-writer` 1.1.0→1.2.0、`note-assembler` 1.0.0→1.1.0、`learning-note-flow` 1.1.0→1.2.0、`research-collector` 2.2.0→2.3.0（描述同步更新）。
- `.codex/rules/research-tools.md`：补 `crawl.sh` 批量抓取行与「单页 WebFetch / 批量 crawl.sh」的选择顺序。
- `docs/superpowers/reports/2026-06-02-token-cost-optimization-verify.md`：加状态补记（该实现的 v1 拆除、估算从未实测、合并职能本次复活）。

### A5 · 守卫与基线

- **新增 `.llm/prompt-cache/cache-guard.py`**：`--freeze` 冻结基线；默认对照最新基线判定；`--json` / `--quiet`。
- **新增 `.llm/prompt-cache/baseline-2026-09-14.json`**（由 freeze 生成，本报告 §2 数字即出自它）。
- 接入 `.codex/scripts/workflow-health-check.sh`（同步到 `.claude/scripts/`）：`--quiet` 调用，回归或旋钮漂移才失败。

### 验证记录（全部通过）

| 检查 | 结果 |
| --- | --- |
| `sync_agents.py --check`（全量） | `[OK] synchronized`，RC=0 |
| `manifest-registry.py validate` | 60 个工件通过 |
| `sync-workflow-routing.sh --check`（canonical 与镜像两侧） | up to date |
| `workflow-health-check.sh`（两侧，含新守卫） | passed，RC=0 |
| 脚本自测（merge/digest，含空目录、缺目录、失败状态、幂等重跑） | 退出码 0/1/2 全部符合契约；重跑不自我合并 |
| 镜像脚本冒烟 + 路径替换检查 | 可通过；镜像只指向 `.claude`，无 `.codex` 残留 |
| 守卫注入测试（两层） | 旋钮漂移→RC=1；改进→STRETCH/PASS 且 RC=0；回归→REGRESS 且 RC=1；`--quiet` 非行动时静默；缺账本/缺设置文件→PENDING+RC=0 |

## 4. 决策回顾（Q17–Q23）

- **Q17**：规则禁止 >~15 KB 整文件读取 + 写 `note-digest.py` → 已落地。
- **Q19**：两个 thinking 旋钮同降 medium，按既有验收协议判定，质量回退则回滚 → 已降档（机制见 A3）。
- **Q20**：只复活合并脚本（+ 两条零成本文档项：六月报告补记、research-tools 补 crawl.sh）→ 已落地。
- **Q21(c)**：chapter-writer 每批 ≤3 章、同代理续写、章间确认保留 + 机械项（合并文件、同类并发 ≤4）→ 已落地。
- **Q22(a)**：collector 每阶段 2–3 个批量子代理 → 已落地。
- **Q23(a)**：assembler 读父流程产出的合并文件 → 已落地。

本次工作**不经过**三个命名工作流（`learning-note-flow` / `legacy-note-import-flow` / `batch-note-update-flow`），未创建 workflow state file；这是执行前与用户确认过的边界。

## 5. 偏离、事故与观察

1. **`thinkingBudget` 实际不生效（机制发现）**：原计划「两个旋钮同降」，实施时发现 Claude provider 下只有 `effortLevel` 生效。按计划仍降 `thinkingBudget`，并在此明确记录其非生效状态，避免后续误读测量结果。
2. **顺带修复**：`chapter-writer.md` 中「子代理自行写 state file」的既有矛盾（与项目规则冲突），属 drive-by 修复，已在上文标注。
3. **安全事故（自我报告）**：实施中一次「设置结构 dump」脚本把 `providerConfigs.claude.environmentVariables` 的明文凭据打进了本会话记录——脱敏正则匹配的是**键名**（`token|key|secret|auth`），而泄漏点在键名无害、值内嵌 `KEY=value` 的字段上。**建议立即轮换该 API key**；后续脚本已把 `environment` 加入脱敏名单，且只读白名单字段。
4. **会话外写者**：Obsidian Git 自动备份（`vault backup: <时间>`）在实施途中多次提交，canonical 改动因此分散在自动提交里（最新一次含 `.claude/*` 镜像与 `cache-guard.py`）；`baseline-2026-09-14.json` 尚未入库，等下次自动备份。未发现内容被回退（逐项 grep 复核通过）。
5. **未修既有噪声**：`sync-workflow-routing.sh` 的 awk 每次输出 18 行 `regexp escape sequence \"` 警告（本次为既有问题，改动它可能影响引号剥离逻辑，需单独验证）。建议单独排期修复，否则健康检查输出会持续被噪声稀释。
6. **hook 未变更** → 未运行 `bootstrap.py --apply`（无 hook 注册变化）。

## 6. 验收协议（如何判定成功）

**采样**：自然运行 7 天，或积累 **≥10 个变更后上下文**（每层分别计算）；质量验收优先于指标验收。

```bash
python3 .llm/prompt-cache/cache-guard.py          # 对照冻结基线
python3 .llm/prompt-cache/cache-guard.py --json    # 机器可读
```

| 层 | 主指标 | PASS | 冲刺 | WARN | REGRESS |
| --- | --- | --- | --- | --- | --- |
| 主会话 | 每上下文全价输入中位数 | ≤0.70× 基线 | ≤0.50× | >0.90× | >1.00× |
| 子代理 | 同上 | ≤0.50× 基线 | — | >0.90× | >1.00× |

附加约束：

1. **旋钮不得漂移**（`effortLevel` / `thinkingBudget` / `savedProviderEffort.claude` 必须等于冻结值），否则测量作废——守卫按失败处理。
2. **命中率不得回退**（当前 95.8% / 97.4%）；它只作护栏，不再作为优化目标。
3. **质量不回退**：首个任务完成后按既有验收协议检查（章节回源核对、用户确认、组装/美化自检）；只有质量不降级时，指标改善才算有效。
4. 触发回滚的条件：旋钮漂移无法解释、主会话中位数 >1.00× 基线、或质量验收失败 → 回滚顺序为「先恢复按钮档位，再回退规则批次」。

## 7. 预期效果（估算，非实测）

按杠杆分层的估算区间（来源：子代理转录聚类分析 + 计划期评审；**这些是估算，不是测量值**）：

| 杠杆 | 依据 | 估算（全价输入） |
| --- | --- | --- |
| chapter-writer 去重复读 | 子代理新鲜输入的 45% 集中在写作类，重复材料读取是主因 | −3M ~ −5M |
| collector 扇出批量化 | 446 个子代理上下文 / 75 主会话（5.95×），批量化后同类大幅下降 | −1.5M ~ −2.5M |
| assembler 预合并 | 组装期逐章重读 → 单文件读取 | −1.5M ~ −2M |
| 固定前缀/整读治理（规则 + digest） | 冷启动中位数 ~34.9k/会话 | 待观察 |
| 合计 | 相对 26.47M 基线 | **约 −32% ~ −57%**（对应目标 −30% / 冲刺 −50%） |

Thinking 降档作用于**输出侧**，不计入主指标（全价输入），但影响实际计费，单独观察。

## 8. 待办

**B 层（内容裁剪，需逐条批准后执行，本次未动）**

- `.learnings` 注入裁剪：每会话注入 ~16,974 B；候选动作 = 去重维护类元段落、合并近似 RULES 条目。
- `CLAUDE.md` / `AGENTS.md` 精简项（固定前缀体积）。
- `read_learnings.py` 输出整形：属 hook 变更，实施后需 `bootstrap.py --apply` + `--check`。

**C 层（仅建议，未实施）**

- 长会话按主题切分（会话越长，固定前缀与历史复读的相对成本越高）。
- 回归样本逐例基线回填（README 已记）。

**建议单独排期**

- `sync-workflow-routing.sh` awk 警告噪声修复（见 §5.5）。
- 轮换凭据（见 §5.3）。

## 9. 复现 / 操作手册

```bash
# 冻结新基线（已存在需 --force；会把变更后数据一并烤进基线，慎用）
python3 .llm/prompt-cache/cache-guard.py --freeze

# 采集（通常由 SessionEnd hook 自动执行）
python .llm/prompt-cache/collect-usage.py --project <claude-project-dir>
python .llm/prompt-cache/collect-usage.py --project <claude-project-dir> --dry-run

# 合并章节 / 生成摘要
python .codex/scripts/merge_files.py --input-dir workspace/<topic>/chapters
python .codex/scripts/note-digest.py <大文件.md>
```

旋钮修改后必须**重载 Claudian 插件 / 重启 Obsidian**；守卫在健康检查中会自动核对是否被静默回写。
