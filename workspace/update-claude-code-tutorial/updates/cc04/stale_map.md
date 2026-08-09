# cc04 — Claude Code 会话管理 — Stale Map

> 更新基线：2026-08-10（覆盖 v2.1.193 ~ v2.1.226）
> 核对来源：SB-06、SB-08、SB-21、SB-22（shared_source_bank），SB-02（Opus 模型示例）

## 保留（KEEP）
- 记忆系统架构、记忆类型对比、会话 vs 记忆 —— 未过时
- `.claude/rules/` 路径范围规则（2026 Q2）—— 仍有效
- CLAUDE.md / user_memory.md / settings 记忆文件结构 —— 未过时
- Skills 存储位置、Frontmatter 配置、字符串替换变量 —— 未过时
- Token 管理策略、记忆文件管理、实用场景 —— 未过时
- CLI `--continue` / `--resume` / `agents` / `--search` / `--directory` —— 仍有效

## 更新（UPDATE）
1. frontmatter `updated: 2026-07-12` → `2026-08-10`（status 保持 `updated`）
2. `/status` 描述 → 显示会话类型（interactive / attached / unattended）【SB-21】
3. CLI 模型示例 `claude --model claude-opus-4-8` → `claude-opus-5`【SB-02】
4. 配置优先级说明 → 补充 CLI args 层级（点6：配置优先级核对）
5. 会话清理策略 → 在其后新增「会话恢复与复制」小节，补充 `/fork` / `/rewind`

## 新增（ADD）
1. `/fork` —— 复制当前对话到新后台会话【SB-08】
2. agent 视图 `/resume` —— 历史会话选择器，以后台会话恢复【SB-08】
3. `/rewind` —— 恢复到 `/clear` 之前的对话；不再通过符号链接/硬链接恢复或删除文件（防逃逸）【SB-08 / SB-22】
4. `/subtask` —— 取代旧 in-session 子代理【SB-06 / SB-08】
5. `/tasks` —— 查看/管理后台代理（含已完成）【SB-06】
6. Subagents 默认后台运行说明 + 并发上限 20【SB-06】
7. AskUserQuestion 对话框默认不再自动继续；可在 `/config` 设 idle timeout【SB-21】
8. transcript 写入失败警告；登录过期警告【SB-21】
9. `## 更新记录` 章节

## 删除（DELETE）
- 无整段删除；仅局部替换过时示例（Opus 模型名）与过时描述（/status）
