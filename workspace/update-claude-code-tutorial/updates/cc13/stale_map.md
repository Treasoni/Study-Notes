# cc13 — Claude Code Slash Commands 完整参考 — Stale Map

> 更新基线：2026-08-10（覆盖 v2.1.193 ~ v2.1.226）
> 核对来源：SB-08、SB-09、SB-10、SB-11、SB-12（shared_source_bank）

## 保留（KEEP）
- 核心概念：命令类型总览（内置 / Bundled Skills / 自定义 / Legacy / Plugin / MCP）—— 未过时
- 通俗理解的结构与比喻 —— 保留（其中 `/review` 示例需局部替换）
- Bundled Skills 5 个捆绑技能 —— 仍有效
- 自定义命令（Skills）：文件位置、创建步骤、SKILL.md 示例、Frontmatter 字段、参数处理、动态上下文注入、文件引用 —— 未过时
- Plugin 命令、MCP Prompts 作为命令、MCP 权限语法 —— 未过时
- 命令架构与生命周期图、序列图 —— 未过时
- 实用自定义命令示例（/commit、/push-all、/pr、/optimize）—— 未过时
- 安装自定义命令、最佳实践、故障排除 —— 未过时
- 与其他概念的关系、相关文档、参考资料 —— 未过时

## 更新（UPDATE）
1. frontmatter `updated: 2026-07-12` → `2026-08-10`（status 保持 `updated`）
2. 命令类型表：自定义 Skills 示例 `/review`, `/commit` → `/commit`, `/optimize`（`/review` 已变更为内置 `/code-review` 别名）【SB-09】
3. 通俗理解示例：`/review src/auth.ts`（标注为自定义 Skill）→ `/code-review`（内置，后台子代理运行）【SB-09】
4. 会话管理命令表：`/branch` 别名说明更新；新增 `/fork` 独立行；`/resume` 补充 agent 视图后台恢复；`/rewind` 补充可恢复到 `/clear` 之前【SB-08】
5. 信息与调试命令表：`/checkup` 为主、`/doctor` 为别名的方向反转 → `/doctor`（全量体检）、`/checkup` 为别名【SB-10】；`/status` 补充会话类型【SB-10】
6. 版本更新历史表：新增 v2.1.212 / v2.1.205-210 / v2.1.199 条目；`/review` 行更新为 `/code-review` 别名【SB-08 / SB-09 / SB-10 / SB-11】
7. Frontmatter 字段参考：`disable-model-invocation` 补充「禁止模型自动调用、此时 Claude 会请你手动运行」说明【SB-18 语境】

## 新增（ADD）
1. `/fork` —— 复制当前对话到新后台会话【SB-08】
2. `/subtask` —— in-session 子代理（取代旧逻辑）【SB-08】
3. 新「代码审查命令」分类：`/code-review`（后台子代理运行，复用上次 effort 等级）+ `/review`（别名，不再自动运行）【SB-09】
4. `/doctor` 全量体检命令行（原 `/checkup` 行改写为主命令）【SB-10】
5. 内置命令参考末尾 tip：Slash/Skill 叠加调用（最多 5 个前置 skill）+ emoji 短码自动补全（`:thumbsup:`）【SB-11 / SB-12】
6. 核心概念 `[!tip] 大白话`（什么是 Slash Commands、`/fork`、`/subtask`）
7. `## 更新记录` 章节

## 删除（DELETE）
- 无整段删除；仅局部替换过时示例（`/review` 自定义示例）与过时描述（`/checkup`→`/doctor`、`/status`、`/branch` 别名）
