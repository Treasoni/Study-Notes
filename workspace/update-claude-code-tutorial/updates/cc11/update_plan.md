# cc11 更新计划

> note_id: cc11
> 目标: 同步 2026-07/08 插件系统安全与来源变化（SB-19），局部 patch，不改原 vault 文件。
> 策略: 保留原结构、写作风格；逐段 patch；核心概念加 `[!tip] 大白话`。

## 补丁列表

| 顺序 | 位置 | 操作 | 内容要点 |
|------|------|------|---------|
| P1 | frontmatter | 修改 | `updated: 2026-07-12` → `2026-08-10`；status 保持 `updated` |
| P2 | §1 核心概念 | 插入 | `[!tip] 大白话`：插件=技能包类比 |
| P3 | §3 用户可配置选项 | 插入 | `[!warning]`：shell 形式 `headersHelper:${user_config.*}` 被拒绝，避免把 `${user_config.*}` 拼进 shell 命令 |
| P4 | §3 插件默认设置 | 修改+插入 | 「项目或用户配置」改为「用户级配置」+ `[!warning]`：`pluginConfigs` 不再从项目级 settings 读取 |
| P5 | §4 安装方法 | 插入 | archive 来源：`claude plugin install <https zip>` + 可选 `--sha256 <digest>` |
| P6 | §4 安装方法（tip） | 插入 | `[!tip] 大白话`：四种安装姿势 + SHA-256 验指纹 |
| P7 | §6 企业管理设置 | 修改 | 表格加 `blockedMarketplaces` 行；示例补 blocked；说明 owner 通配符 |
| P8 | §6 新增「安装同意」小节 | 插入 | 外部插件只由项目设置启用时，每个加载路径要求明确安装同意（防自批准） |
| P9 | §6 插件安全限制 | 插入 | `[!warning]` shell 注入修复（headersHelper） |
| P10 | §7 FAQ 插件安全吗？ | 修改 | 补充 SHA-256 校验、安装同意提醒 |
| P11 | 文末 | 插入 | `## 更新记录`（2026-08-10 变更摘要） |

## 约束检查

- [x] 列表内不嵌套表格（安装同意小节用列表不用表）。
- [x] YAML 特殊字符值加引号（本笔记 frontmatter 无特殊字符，保持原样）。
- [x] 不改原 vault 文件，产物写入 output_dir。
- [x] 保留原章节编号与写作风格。

## 完成后校验

- 逐条核对 P1-P11 已应用到 updated_note.md。
- 确认「更新记录」已追加。
