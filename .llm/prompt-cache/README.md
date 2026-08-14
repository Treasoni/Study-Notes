# Prompt Cache Telemetry

本项目 LLM 调用的本地可观测性设施。schema 与回归样本入库；事件日志仅本地保留。

## 目录结构

| 文件 | 用途 | 入库 |
| --- | --- | --- |
| `llm-usage-event.schema.json` | 调用事件字段合同（provider-neutral） | ✅ |
| `regression-cases.json` | 5 个高频请求类型的稳定回归样本（含质量检查） | ✅ |
| `fixtures/*.md` | 回归样本的脱敏输入 profile | ✅ |
| `collect-usage.py` | 从 Claude Code transcripts 采集 usage 事件 | ✅ |
| `usage-events.jsonl` | 本地事件日志（gitignored） | ❌ |
| `.collect-state.json` | 幂等采集状态（gitignored） | ❌ |

## 采集

**自动**：`.claude/settings.json` 注册了 `SessionEnd` hook。Claude Code 会通过 stdin 提供当前 `transcript_path`，采集器只处理该会话，避免扫描其他项目或依赖本机目录名：

```json
"SessionEnd": [{ "matcher": "", "hooks": [{ "type": "command",
  "command": "python .llm/prompt-cache/collect-usage.py" }] }]
```

> 采集器不会把转录路径、原始提示词或输出写入事件日志；事件仅保存文件名、消息 ID 和 provider usage 字段。

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
| `input_reference` | 会话文件名（安全，不含内容） |

## 基线

- **历史基线（2026-08-03，已丢失）**：26 会话 / 844 条消息，新鲜输入 1.88M tokens，缓存读取 71.6M（有效占比 ~97.4%）。该批次事件于 08-06 因采集路径失效被清空，`usage-events.jsonl` 与 `.collect-state.json` 重置。
- **当前基线（2026-08-10，管道修复后重新采集）**：99 会话 / 2,436 条事件（按消息 id 去重，JSONL 为 append-only）：
  - 新鲜输入 11.4M tokens，缓存读取 223M tokens（有效输入缓存占比 ~95.1%）
  - 平均新鲜输入/请求 4,682 tokens；缓存读取/请求 ~91.7k tokens
  - **冷启动主导成本**：每会话前 5 个请求占全部新鲜输入的 ~67%（7.6M）；首个请求 ≈ system prompt 大小（平均 ~36k）。稳态请求新鲜输入中位数仅 ~500 tokens。
- 回归样本逐例基线待下次自然运行对应工作流时回填（`baseline.*` 字段）。
- 模板/模型/工具定义变更后：运行同一批回归样本，只有质量检查通过时缓存指标变化才算有效优化。
- Codex 桌面未提供可由项目自动读取的 provider usage 边界，因此不写入或混入 Claude 的缓存指标；它只复用同一份提示缓存规则。
