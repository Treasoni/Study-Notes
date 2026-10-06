# Prompt Cache Telemetry

本项目 LLM 调用的本地可观测性设施。schema 与回归样本入库；事件日志仅本地保留。

## 目录结构

| 文件 | 用途 | 入库 |
| --- | --- | --- |
| `llm-usage-event.schema.json` | 调用事件字段合同（provider-neutral） | ✅ |
| `regression-cases.json` | 5 个高频请求类型的稳定回归样本（含质量检查） | ✅ |
| `fixtures/*.md` | 回归样本的脱敏输入 profile | ✅ |
| `collect-usage.py` | 从 Claude Code transcripts 采集 usage 事件 | ✅ |
| `cache-guard.py` | 冻结基线 / 对照验收协议守卫（旋钮漂移 + 指标回归） | ✅ |
| `baseline-*.json` | 冻结的验收基线（机器可读，由 `cache-guard.py --freeze` 生成） | ✅ |
| `usage-events.jsonl` | 本地事件日志（gitignored） | ❌ |
| `.collect-state.json` | 幂等采集状态（gitignored） | ❌ |

## 采集

**自动**：`.claude/settings.json` 注册了 `SessionEnd` hook。Claude Code 会通过 stdin 提供当前 `transcript_path`，采集器只处理该会话，避免扫描其他项目或依赖本机目录名：

```json
"SessionEnd": [{ "matcher": "", "hooks": [{ "type": "command",
  "command": "python .llm/prompt-cache/collect-usage.py" }] }]
```

> 采集器不会把转录路径、原始提示词或输出写入事件日志；事件仅保存文件名、消息 ID 和 provider usage 字段。

采集范围**包含该会话派生的子代理转录**（`<session>/subagents/agent-*.jsonl`，2026-09-14 起）。子代理事件以 `request_type=subagent` 落盘，`metadata` 带 `layer` / `parent_session` / `attribution_agent`。此前子代理消耗不在本日志内——修复前它占全量新鲜输入的 59%，属测量盲区。

**手动**：

```bash
python .llm/prompt-cache/collect-usage.py --project /path/to/claude-project
python .llm/prompt-cache/collect-usage.py --project /path/to/claude-project --dry-run
```

幂等：按（会话文件, 消息 id）去重，重复运行不会产生重复事件。hook 失败只记日志、不阻断会话。

## 字段映射（与 schema 的显式兼容等价）

| schema 字段 | 来源 |
| --- | --- |
| `request_type` | 会话首条用户消息关键词分类（learning_note / note_update / note_import / note_beautify / moc_sync / prompt_cache / system_workflow / claude_code_general） |
| `template_id` | `claude-code.session`（每次请求即会话级提示） |
| `cache_read_tokens` | `usage.cache_read_input_tokens` |
| `cache_write_tokens` | `usage.cache_creation_input_tokens`（本环境恒为 0） |
| `latency_ms` | **恒为 `null`** — Claude Code transcripts 不记录逐请求延迟，schema 显式允许该值 |
| `input_reference` | 会话或子代理文件名（安全，不含内容） |
| `request_type="subagent"` | 子代理转录（`<session>/subagents/agent-*.jsonl`）；`metadata` 另带 `layer`、`parent_session`、`attribution_agent` |

## 基线

- **历史基线（2026-08-03 / 2026-08-10，均已失效）**：两个批次分别因采集路径失效被清空或从未落盘；本 README 曾声称的「2026-08-10：99 会话 / 2,436 事件」在磁盘上不存在。教训：基线必须能由 `usage-events.jsonl` 复算，不能只写在文档里。
- **当前基线（2026-09-14，窗口 2026-08-15 → 2026-09-14，含子代理）**：8,972 条事件（按消息 id 去重，JSONL 为 append-only）：

| 层 | 规模 | 新鲜输入 | 缓存读取 |
| --- | --- | --- | --- |
| 主会话 | 75 会话 / 4,604 事件 | 10,916,719 | 406,293,248 |
| 子代理 | 446 代理 / 4,368 事件 | 15,554,020 | 200,093,440 |
| 合计 | | **26,470,739** | **606,386,688** |

  - 命中率（有效输入缓存占比）：全量 95.8%，主会话 97.4%——已无上行空间，只能当护栏。
  - **冷启动/固定前缀主导**：主会话首个请求新鲜输入中位数 ~34.9k（p90 ~38.3k）；子代理首请求 ~5.0k。
  - **子代理层是最大一块全价输入**（59%）：其中 chapter-writer 一类占子代理新鲜输入的 45%（7.07M）。
  - 本基线是 2026-09-14 token/缓存优化（`docs/superpowers/reports/2026-09-14-token-cost-optimization.md`）的验收对照：主指标 = 全价输入 −30%（冲刺 −50%），命中率不得回退。
- 回归样本逐例基线待下次自然运行对应工作流时回填（`baseline.*` 字段）。
- 模板/模型/工具定义变更后：运行同一批回归样本，只有质量检查通过时缓存指标变化才算有效优化。
- Codex 桌面未提供可由项目自动读取的 provider usage 边界，因此不写入或混入 Claude 的缓存指标；它只复用同一份提示缓存规则。

## 守卫

`cache-guard.py` 把上面的基线变成可执行的验收协议，生成侧（`--freeze`）与校验侧（默认对照）共用同一份统计代码，避免两边口径漂移：

```bash
python3 .llm/prompt-cache/cache-guard.py            # 对照最新基线
python3 .llm/prompt-cache/cache-guard.py --json      # 机器可读
python3 .llm/prompt-cache/cache-guard.py --quiet     # 只在需要行动时输出（健康检查用）
python3 .llm/prompt-cache/cache-guard.py --freeze    # 冻结新基线（已存在则需 --force）
```

判定（需要该层 ≥10 个变更后上下文，即「7 天或 10 个上下文」协议）：

| 层 | 主指标 | PASS | 冲刺 | WARN | REGRESS |
| --- | --- | --- | --- | --- | --- |
| 主会话 | 每上下文全价输入中位数 | ≤0.70× 基线 | ≤0.50× | >0.90× | >1.00× |
| 子代理 | 同上 | ≤0.50× 基线 | — | >0.90× | >1.00× |

同时校验三个推理旋钮（`effortLevel` / `thinkingBudget` / `savedProviderEffort.claude`）是否仍等于冻结值：静默回写会让测量失效，因此按失败处理。本机无账本或无设置文件视为「无数据」，不算失败。

退出码：`0` 通过或数据不足，`1` 需要行动（回归或旋钮漂移），`2` 错误。已接入 `workflow-health-check.sh`（`.codex/scripts/` 与 `.claude/scripts/` 各一份）——旋钮与指标两层都做过注入测试，空绿不成立。
