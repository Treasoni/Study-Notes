# Update Plan — cc19「LLM Prompt Caching 提示缓存」

> 目标：同步 2026-08 现状，draft 补全为完整笔记（含小结/FAQ），核心概念加 `[!tip] 大白话`
> 参考：shared_research/source_bank.md（SB-01、SB-20）；项目 `.claude/rules/common/prompt-cache.md`

## 依据来源

| 条目 | 来源 | 日期 | 摘要 |
|------|------|------|------|
| SB-01 | code.claude.com/docs/en/changelog | v2.1.197（2026-06 下旬） | Claude Sonnet 5 成为默认模型，原生 1M token 上下文，促销价 $2/$10 每 Mtok 至 2026-08-31 |
| SB-20 | code.claude.com/docs/en/changelog | v2.1.197 / v2.1.223 | `CLAUDE_CODE_DISABLE_1M_CONTEXT` 对所有原生 1M 模型强制 200K 自动压缩；缓存命中策略需更新（长上下文分段缓存） |

## 更新步骤

1. **frontmatter**：`updated` → `2026-08-10`；`status` → `updated`（draft 补全为正式态）。
2. **保留一~七章原有结构**，仅局部 patch；修正「三层缓存结构」标题为「五层」（S5）。
3. **三章新增小节**「1M 上下文与更大的缓存窗口」：Sonnet 5 / Opus 5 原生 1M、缓存窗口对比表、`CLAUDE_CODE_DISABLE_1M_CONTEXT=1` 说明 + `[!warning]`（S3/S4）。
4. **三章「项目中的缓存优化实践」**：在稳定前缀顺序后追加「5 分钟 TTL 断点对应」说明（S6）。
5. **四章**：❌ 破坏缓存表新增「环境变量切换 / 自动压缩触发」行；诊断表新增「自动压缩触发」行（S7/S8）。
6. **五章**：新增「5. 长上下文分段缓存（1M 时代）」策略；原「5. 监控缓存效果」顺延为「6.」（S9）。
7. **七章**：新增误区「1M 上下文就不需要缓存了」（S10）。
8. **补全结尾**：「小结」+「常见问题（FAQ）」+ 参考资料补充 changelog（S11）。
9. **核心概念**补 `[!tip] 大白话`：命中/未命中、缓存断点、1M 窗口、自动压缩（S12）。
10. **追加** `## 更新记录`（2026-08-10，逐条列变更）（S13）。

## 约束执行

- 不修改原 vault 文件；产物写入 output_dir（`updates/cc19/`）。
- 列表内不嵌套表格（新表格全部置于标题层级）。
- YAML 特殊字符值加引号。
- moc_path：none（P5 统一处理 MOC）。
