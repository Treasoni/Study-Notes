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

**自动**：`.claude/settings.json` 注册了 `SessionEnd` hook，每次 Claude Code 会话结束时自动增量采集：

```json
"SessionEnd": [{ "matcher": "", "hooks": [{ "type": "command",
  "command": "python .llm/prompt-cache/collect-usage.py" }] }]
```

**手动**：

```bash
python .llm/prompt-cache/collect-usage.py            # 增量追加新事件
python .llm/prompt-cache/collect-usage.py --dry-run  # 只报告将新增数量
```

幂等：按（会话文件, 消息 id）去重，重复运行不会产生重复事件。hook 失败只记日志、不阻断会话。

## 字段映射（与 schema 的显式兼容等价）

| schema 字段 | 来源 |
| --- | --- |
| `request_type` | 会话首条用户消息关键词分类（learning_note / note_update / note_import / note_beautify / moc_sync / prompt_cache / system_workflow / claude_code_general） |
| `template_id` | `claude-code.session`（每次请求即会话级提示） |
| `cache_read_tokens` | `usage.cache_read_input_tokens` |
| `cache_write_tokens` | `usage.cache_creation_input_tokens`（本环境恒为 0） |
| `latency_ms` | **恒为 `null`** — Claude Code transcripts 不记录逐请求延迟 |
| `input_reference` | 会话文件名（安全，不含内容） |

## 基线

- 首次采集基线（2026-08-03，26 会话 / 844 条唯一消息；按消息 id 去重，JSONL 为 append-only 存在重复记录）：
  - 新鲜输入 1.88M tokens，缓存读取 71.6M tokens（有效输入缓存占比 ~97.4%）
  - 平均新鲜输入/消息 2,222 tokens；缓存读取/消息 ~85k tokens
- 回归样本逐例基线待下次自然运行对应工作流时回填（`baseline.*` 字段）。
- 模板/模型/工具定义变更后：运行同一批回归样本，只有质量检查通过时缓存指标变化才算有效优化。
