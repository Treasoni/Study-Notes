# cdx07 更新报告：Codex CLI 与调试

> 运行：codex-config-update / 批次 3 / cdx07
> 日期：2026-08-10
> 模式：patch-in-place（就地重构）

## 1. 变更概览

- **旧路径**：`AI学习/Codex/07 CLI 与调试.md`
- **新路径**：`AI学习/Codex/02-基础功能/Codex CLI 与调试.md`
- **标题**：`Codex 完整配置体系` → `Codex CLI 与调试`
- **标签**：`[codex, claude-code, configuration]` → `[codex, ai, 工具使用, 基础功能, cli]`
- **状态**：`completed` → `updated`；`updated` 字段更新为 `2026-08-10`

## 2. 结构调整

1. **Frontmatter**：标题、标签、状态、更新时间套用 Claude Code 教程模板。
2. **标题层级**：章式标题（`第七章`）移除；原 `### N.` 全部转成 `##` / `###` 两级标题并去序号。
3. **文档定位**：H1 后新增 `> [!info] 文档定位` callout，开头说明段落语义并入。
4. **分节规范**：大主题用 `---` 分隔，仅保留 `##` / `###` 两级。
5. **新增教程区块**：常见问题（3 条 Q&A）、最佳实践（Do's 4 条 / Don'ts 4 条）、小结、相关文档表格、参考资料、更新记录。
6. **移除旧导航**：`> [!note] 导航` 书籍式上一章/下一章导航块替换为「相关文档」wikilink 表格。

## 3. 内容保留

- 全部技术内容未删减、未改写、未新增虚构事实。
- 核心 CLI 命令两段代码块（REPL/exec、status/-c/--profile/mcp add）、交互式命令、环境变量、调试与验证方法、快速诊断清单等代码块完整保留。
- `--cd` 重要性说明、`.env` 加载规则、经验法则等段落与 bullet 列表完整保留。
- 常见故障案例表（4 行 4 列：模型提供商配置、技能自动加载、SessionStart hook、CODEX_HOME）完整保留。
- 本章小结 callout 精炼为「小结」章节，语义未改变。

## 4. 新增内容来源

| 新增区块 | 来源 |
|----------|------|
| 常见问题 | 从正文"配置审计技巧"（诊断清单 + 故障案例表）提炼：配置不生效、如何确认加载内容、CODEX_HOME 作用 |
| 最佳实践 Do's | 从正文经验法则、`--cd` 重要性、调试优先用 `codex status`、故障排查顺序提炼 |
| 最佳实践 Don'ts | 从正文静默忽略键、CODEX_HOME 误指向、hook untrusted、配置层级确认提炼 |
| 小结 | 精炼正文"本章小结" |
| 相关文档 | 按批次参数指定的 4 个 wikilink |
| 参考资料 | 仅官方 Codex 文档 + GitHub 仓库两个链接 |

## 5. 相关文档链接

- `[[config.toml 核心配置]]`
- `[[Hooks 与插件]]`
- `[[快速参考卡片]]`
- `[[Codex MOC]]`

## 6. 参考资料

- [OpenAI Codex 文档](https://developers.openai.com/codex/)
- [OpenAI Codex GitHub](https://github.com/openai/codex)

## 7. 输出文件

| 文件 | 说明 |
|------|------|
| `workspace/codex-config-update/updates/cdx07/stale_map.md` | 旧结构 → 新结构映射表 |
| `workspace/codex-config-update/updates/cdx07/updated_note.md` | 完整新笔记正文 |
| `AI学习/Codex/02-基础功能/Codex CLI 与调试.md` | 已写入 vault 目标路径 |
