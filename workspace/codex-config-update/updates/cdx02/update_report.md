# cdx02 更新报告

> 笔记 ID：cdx02
> 原路径：`AI学习/Codex/02 config.toml 核心配置.md`
> 新路径：`AI学习/Codex/02-基础功能/config.toml 核心配置.md`
> 重构日期：2026-08-10

## 1. 做了什么

按 Claude Code 教程模板将《config.toml 核心配置》从"书章式"重排为"教程式"。新区块顺序：frontmatter → H1 → `> [!info] 文档定位` → 主体分节（`##` / `###` + `---` 分隔）→ 常见问题 → 最佳实践 → 小结 → 相关文档 → 参考资料 → 更新记录。文件名同步从 `02 config.toml 核心配置.md` 改为 `02-基础功能/config.toml 核心配置.md`。

## 2. 内容保留

- 10 个主体区块的全部技术内容原样保留：五层优先级与合并机制、用户级安全限定、sandbox_mode、approval_policy、Permissions、Profiles、模型多提供商、Features、Shell 环境策略、完整配置示例。
- 全部代码块、表格、callout、警示均未删减、未改写，也未新增任何源内容之外的技术事实。

## 3. 结构变更

- 编号标题 `### N.` / `#### N.M` 全部重命名为无编号的 `##` / `###` 描述性标题。
- 旧书章导航 `> [!note] 导航` + `[[xx|← 上一章]]` 移除，替换为「相关文档」wikilink 表格。
- 章节导语并入「文档定位」callout。
- 新增区块：常见问题（3 条 Q&A）、最佳实践（Do's 6 / Don'ts 4）、小结、相关文档、参考资料、更新记录。
- `> **本章小结**` 普通引用改为 `> [!summary]` Callout。
- 大主题之间统一用 `---` 分隔。

## 4. frontmatter

- title：`Codex 完整配置体系` → `config.toml 核心配置`
- tags：`[codex, claude-code, configuration]` → `[codex, ai, 工具使用, 基础功能, 配置]`
- updated：`2026-07-31` → `2026-08-10`
- status：`completed` → `updated`
- created：`2026-07-31`（保持不变）
- source_project：`codex-config`（保持不变）

## 5. 输出文件

- 更新后的笔记已写入 vault 新路径 `AI学习/Codex/02-基础功能/config.toml 核心配置.md`（patch-in-place）
- 副本：`workspace/codex-config-update/updates/cdx02/updated_note.md`
- 映射表：`workspace/codex-config-update/updates/cdx02/stale_map.md`

## 6. 待办（后续阶段）

- 旧文件 `AI学习/Codex/02 config.toml 核心配置.md` 按批次计划在 P5 用户确认后删除。
- `AI学习/00-索引/AI学习 MOC.md` 中相关旧 wikilink 需在 P5 更新。
