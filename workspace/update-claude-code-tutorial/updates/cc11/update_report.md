# cc11 更新报告

> note_id: cc11
> 笔记: Claude Code 插件系统使用指南
> 更新时间: 2026-08-10
> 资料来源: SB-19（共享 source bank）+ update_goal 专项补充
> 产物: updated_note.md / stale_map.md / update_plan.md

## 变更摘要

1. frontmatter：`updated` → `2026-08-10`（status 保持 `updated`）。
2. 新增安全警告：插件 shell 形式 `headersHelper:${user_config.*}` 被拒绝（shell 注入修复）。
3. 修正 `pluginConfigs` 行为：不再从项目级 `.claude/settings.json` 读取，覆盖仅限用户级。
4. 安装来源新增 `archive`：`claude plugin install <https-zip>` + 可选 `--sha256` 固定。
5. 新增「安装同意」：外部插件只由项目设置启用时，每个加载路径要求明确安装同意（防自批准）。
6. 企业管理设置补充 `blockedMarketplaces`（owner 通配符）。
7. 核心概念补充 `[!tip] 大白话`（§1 核心概念、§4 安装、§6 安全）。
8. 文末追加 `## 更新记录`。

## 过时点统计

共 8 处过时/缺口（见 stale_map.md S1-S8）：
- **breaking 安全变更 2 项**：`headersHelper` 注入修复、`pluginConfigs` 项目级配置失效。
- **功能新增 3 项**：`archive` 安装来源、安装同意机制、`blockedMarketplaces`。
- **常规更新 3 项**：frontmatter 日期、FAQ 安全建议、大白话 tip。

## 风险项

- **版本号映射不确定**：SB-19 仅给出 v2.1.207 / v2.1.224 两个版本号，未逐条对应。本报告将 `headersHelper` 拒绝与 `archive` 来源标为 v2.1.224+、`pluginConfigs` 与安装同意标为 v2.1.207+，建议对照 code.claude.com changelog 复核。
- **`headersHelper` 替代写法**：SB-19 未给出对象形式的具体 schema，正文仅给方向性建议（环境变量/对象传参），未写死配置示例。
- **「插件默认设置」覆盖行为**：`pluginConfigs` 不再从项目级 settings 读取的具体影响范围（是否波及其它 settings 键）未在 source bank 细化。
- **未改动 vault 原文件**：所有产物在 output_dir；发布需走 note-beautifier / 统一发布流程。

## 是否需要 needs-review

**是（建议人工复核）**。涉及 breaking 安全变更与版本号归属，建议：
1. 对照现行 changelog 确认 4 项变更的准确版本号。
2. 确认 `headersHelper` 推荐替代写法的官方 schema。
3. 确认 `pluginConfigs` 不再从项目级读取后，「插件默认设置」段落表述与实际行为一致。

## 已遵守约束

- 未修改原 vault 文件（只读，产物全部写入 output_dir）。
- 列表内不嵌套表格（安装同意小节用列表不用表）。
- YAML 特殊字符值加引号（本笔记 frontmatter 无特殊字符，保持原样）。
- 保留原结构与写作风格，局部 patch。
- frontmatter `updated`=2026-08-10；文末追加 `## 更新记录`。
