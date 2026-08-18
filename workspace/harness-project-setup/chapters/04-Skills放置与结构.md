# 第四章 Skills——往哪放、怎么写、扫描优先级

> [!summary] 本章导读
> 这是你问的「skills 放在那里」的完整答案。dsh 的 skills 格式与 Claude Code 兼容（`<name>/SKILL.md` 或 `<name>.md`），但**扫描根有六个、优先级 first-wins**。读完你会知道：项目级放哪、用户级放哪、custom/bundled 什么时候出现、SKILL.md 到底哪些字段是强制的、以及怎么把现成 Claude Code skills 一键搬过来。

## 4.1 六个扫描根：rank 表（first-wins）

dsh 的本地技能发现按 rank 顺序，**同名取先命中的**（first-wins）[^b2][^d1]：

| Rank | 源 | 根目录 |
|---|---|---|
| 100 | project-dsh | `<项目根>/.dsh/skills` |
| 200 | project-agents | `<项目根>/.agents/skills` |
| 300 | custom | `Config.customSkillDirs` |
| 400 | user-dsh | `~/.dsh/skills` |
| 500 | user-agents | `~/.agents/skills` |
| 600 | bundled | 包内自带（`Config.bundledSkillDir`） |

项目根 = 最近含 `.git` 的祖先；无 `.git` 用 cwd；`ctx.fs` 可用时 git-root walk 走 fs 服务（远程/沙箱工作区不落回宿主边界）[^b2]。

> [!tip] 大白话
> 六个抽屉从近到远：项目的 `.dsh` 最优先，其次 `.agents`，然后你自定义的、你机器级的、最后是包自带的。同一个 skill 名在多个抽屉出现，**近的赢**。

**同名解析细节**（来自官方 skills.md）：同层内按 rank → provider order → local order 决出；跨层 registry 是 host+per-scope 分层，**nearest layer 直接赢同名**，rank 只决定同层内；runtime 条目 outrank user 条目[^b2]。

## 4.2 格式：与 Claude Code 兼容，但 frontmatter 只强两键

**放置形式**：目录 bundle `<name>/SKILL.md` **或** 单文件 `<name>.md`；名字必须 kebab-case（`^[a-z0-9]+(?:-[a-z0-9]+)*$`）；**不支持**嵌套递归 `**/SKILL.md` 发现[^b2]。

**frontmatter 契约**：本地 provider 只读**两个精确 kebab-case 键**——`disable-model-invocation` 和 `user-invocable`，缺省字段视为 `true`。两者归一化为 `SkillInvocationPolicy`：`modelInvocable` / `userInvocable`；两键皆 `false` 则该 skill 只能被受信 `ctx.skills.get()` 调用[^b2]。

> [!note] 和 Claude Code 的差异
> Claude Code 的 SKILL.md frontmatter 里 `name`/`description` 决定自动加载；dsh 的本地 provider **不读 `name`/`description` 为强制字段**——它靠目录名（或文件名）当 skill 名。`SkillSummary`/`SkillDefinition` 里的 `name`/`description`/`whenToUse` 是 registry 级字段，不是 provider 强制 frontmatter。

最小 skill：

```text
.dsh/skills/my-skill/SKILL.md
```

```yaml
---
name: my-skill
description: Do something useful when the user asks for it.
---
正文指令……
```

> [!warning] 渐进式披露
> 目录只放 `name` + `description` 摘要（模型看到简介决定要不要读），正文不进每轮请求。所以**简介写没写清楚很关键**——模型只靠简介判断「要不要拉开抽屉」。

## 4.3 加载机制：热加载 + 按需读正文

- **目录被 watcher 监听，新建即热加载**，不用重启[^d1]；
- 模型侧通过一个 **`skill({name})` 工具**按需加载正文——`skill({name})` 先校验 kebab-case 名、找 summary、`isModelInvocable` 检查，再按调用 agent 的 cwd 重读完整定义并重查策略[^b2]；
- **全文不缓存**：registry 的每次 `get()` 重读当前正文（本地 provider rereads body）；所以改正文立即影响后续工具调用，不产生 catalog 消息、不改写旧工具结果[^b2]；
- 热更新：模型侧 `write`/`edit` 观测同步失效 provider；host watcher 覆盖 IDE/Git/shell/外部进程变更；watcher 失败会保留 last-good 视图[^b2]。

## 4.4 把现成 Claude Code skills 搬过来

迁移成本 = **复制文件夹**（格式兼容）[^d1]：

```bash
# 项目级
mkdir -p .dsh/skills
cp -r ~/.claude/skills/* .dsh/skills/

# 或用户级（所有项目共享）
cp -r ~/.claude/skills/* ~/.dsh/skills/
```

> [!note] 这在 Claude Code 里相当于
> `.claude/skills/<name>/SKILL.md` → `.dsh/skills/<name>/SKILL.md`。格式一样、frontmatter 兼容、热加载一样，只是目录根从 `.claude` 变成 `.dsh`。

## 4.5 常见坑

1. **目录名 / 文件名即 skill 名**，必须是 kebab-case；写 `My Skill/` 不会被发现。
2. **嵌套 `subdir/skill/SKILL.md` 不被发现**——只支持一层 bundle 或扁平单文件。
3. **忘了 `disable-model-invocation` 语义**——两键默认 `true`；想彻底私有化（只允许代码调用）两键都设 `false`。
4. **以为 `.dsh/` 还能放 hooks/mcp**——`.dsh/skills` 只管技能；hooks/mcp 走 `cordis.yml`（第 5、7 章）。

## 本章小结

> [!summary]
> - 六个扫描根 rank：`.dsh/skills`(100) → `.agents/skills`(200) → custom(300) → user-dsh(400) → user-agents(500) → bundled(600)，**first-wins**；
> - 格式：目录 bundle `<name>/SKILL.md` 或单文件 `<name>.md`，kebab-case，不支持嵌套递归；frontmatter 只强两键 `disable-model-invocation` / `user-invocable`；
> - 热加载 + `skill({name})` 工具按需读正文 + 全文不缓存；
> - 迁移 = 复制文件夹（格式与 Claude Code 兼容）。

下一章：**Hooks——桥接复用 vs 原生插件**。

---

## 素材来源

[^b2]: B2 · dsh 官方 `docs/subsystems/skills.md`，2026-08-16 抓取。
[^d1]: D1 · 你的 vault 笔记《03-配置实战-接入skills-hooks-mcp-rules》，2026-08-16。
