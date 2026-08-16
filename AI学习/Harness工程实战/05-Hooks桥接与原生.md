---
title: "第五章 Hooks——桥接复用 vs 原生插件"
tags: [deepseek-harness, ai, agent, hooks, 实战]
created: 2026-08-16
updated: 2026-08-16
status: new
source_project: deepseek-harness
---

# 第五章 Hooks——桥接复用 vs 原生插件

> [!summary] 本章导读
> dsh 的 hooks 有**两套完全不同的玩法**：桥接插件（复用你现成的 Claude Code hooks.json，迁移成本最低）和原生 cordis 插件（更强大，但要写代码）。读完你会知道：什么时候用桥接、什么时候写原生、桥接支持哪些 hook 点、两个必踩的坑、以及「这段配置写进哪个文件」。

## 5.0 心智前提：hook ⊂ 插件

先纠正一个概念：**hook 不是 dsh 的一等公民，插件才是**。dsh 里一切能力都是 cordis 插件（容器），hook 只是其中「监听扩展点、返回决策」的那一类职责[^c5-d1]。

| 判断标准 | 例子 |
|---|---|
| 监听 `ctx.on(...)` 生命周期/执行类扩展点并返回决策 → **是 hook** | `tools/pre-execute` 权限门、`agent/pre-step` 策略 |
| 干别的（连 MCP server、桥接 Claude Code hooks、提供工具）→ **是插件但不是 hook** | `dsh-hooks-claude-code` 桥接插件、`dsh-mcp-client` |

## 5.1 桥接复用你现成的 Claude Code hooks（迁移成本最低）

装 `@deepseek-ai/dsh-hooks-claude-code` 桥接插件，它把你 `hooks.json`（或 settings 的 `hooks` 键）里的 shell 命令 hooks 翻译成 dsh 的类型化扩展点[^c5-b3][^c5-d1]：

```yaml
- id: hooks-cc
  name: '@deepseek-ai/dsh-hooks-claude-code'
  config:
    configPath: ./hooks.json        # 你现成的 Claude Code hooks 配置
    # projectDir 省略时，默认把 CLAUDE_PROJECT_DIR 导出为 session 工作目录
```

**支持的 hook 点**：`SessionStart` / `UserPromptSubmit` / `PreToolUse` / `PostToolUse` / `Stop` / `SubagentStart` / `SubagentStop`[^c5-d1]。`CLAUDE_PROJECT_DIR` 会自动注入给 hook 进程，常见项目相对路径的 hook 不用改就能跑[^c5-b3]。

**配置项**（config-catalog）[^c5-b3]：

| 键 | 含义 |
|---|---|
| `configPath` | 指向 `hooks.json` 或 settings 文件（其 `hooks` 键为配置） |
| `pluginRoot` | 替换命令串里的 `${CLAUDE_PLUGIN_ROOT}` |
| `projectDir` | 替换 `${CLAUDE_PROJECT_DIR}` **并**导出为 hook 进程的 env；默认按 session workspace |
| `defaultTimeoutMs` | 默认每 hook 超时（CC 默认 600000） |
| `stderrSummaryMaxChars` | `hook/result` 事件持久化 stderr 摘要的字符上限 |

> [!note] 这段写进哪个文件？
> 这个 `- id: hooks-cc` 块是 **cordis.yml 补丁文件里的插件行**，不是丢进 `.dsh/` 目录的独立文件。落点按生效范围选[^c5-d1]：

| 生效范围 | 写进哪个文件 | 怎么生效 |
|---|---|---|
| 项目里先试跑 | 项目根新建 `./cordis.yml` | `pnpm dsh web --patch ./cordis.yml` |
| 某个 profile 长期 | `~/.dsh/profiles/<name>/cordis.patch.yml` | 随该 profile 自动叠加（补丁树第②层） |
| 机器全局 | `~/.dsh/cordis.patch.yml` | 所有 profile 共享（补丁树第③层） |

两个前提：① 插件包要能解析——`name` 引用 npm 包，未安装先 `dsh plugin --profile <name> add @deepseek-ai/dsh-hooks-claude-code`；② `configPath: ./hooks.json` 是进程级、按启动 cwd 解析（见坑 2）。

## 5.2 原生插件（更强大，但要点编程）

「原生 hook」就是普通的 cordis 插件，监听类型化扩展点并返回决策[^c5-d1]：

| 扩展点 | 用途 |
|---|---|
| `tools/pre-execute` | 权限门：allow / deny / ask |
| `tools/post-execute` | 改写展示内容或返回值 |
| `agent/pre-step` | 每步前的策略 |
| `agent/turn-stopping` | 结束前干预 |
| `subagent/start` / `subagent/end` | 子代理生命周期 |

```ts
ctx.on('tools/pre-execute', async (exec, next): Promise<PreToolDecision> => {
  if (!(await isAllowed(exec))) {
    return { kind: 'deny', reason: 'Denied by policy.' }
  }
  return next()
})
```

> [!tip] 选择建议
> 想「原样跑起现有 hooks」→ 桥接；想「写新的、复杂的策略」→ 原生插件。桥接是「兼容适配器，不是威力工具」——原生插件有类型化返回、完整 `ctx`、无序列化边界[^c5-d1]。

## 5.3 三个坑（照搬前必看）

1. **hooks 桥接只跑 shell-form 的 `type: 'command'`**；`http` / `mcp_tool` / `prompt` / `agent` 类型的 hook 会被解析但跳过；`updatedInput`（工具入参改写）不生效，只记录告警[^c5-d1]。
2. **`configPath` 是进程级**：启动时读一次，相对路径按进程启动 cwd 解析；**不会**像 Claude Code 那样按 session 自动发现项目里的 `hooks.json`（官方标记 `TODO(per-session-hook-config)`）[^c5-b3][^c5-d1]。要么写绝对路径，要么在 `hooks.json` 所在目录启动。
3. **别把 hooks 配置塞进 `.dsh/`**——`.dsh` 只管技能 + 用户级 home；hooks 走 `cordis.yml` 补丁层。

## 本章小结

> [!summary]
> - hook ⊂ 插件：hook 是监听扩展点返回决策的那类插件职责；
> - 桥接 `dsh-hooks-claude-code`：`configPath` 指向 hooks.json，支持 SessionStart/UserPromptSubmit/PreToolUse/PostToolUse/Stop/SubagentStart/SubagentStop；只跑 shell command；
> - 原生插件：`ctx.on('tools/pre-execute', ...)` 返回 deny/next，更强大；
> - 落点：试跑 `--patch ./cordis.yml` / profile `cordis.patch.yml` / home `cordis.patch.yml` 三层；
> - 两个坑：桥接只跑 shell command、`configPath` 进程级。

下一章：**Subagents——ctx.subagents 与 SubagentProvider**。

---

## 素材来源

[^c5-b3]: B3 · dsh 官方 `docs/config-catalog.md`（hooks 桥接 / mcp-client），2026-08-16 抓取。
[^c5-d1]: D1 · 你的 vault 笔记《03-配置实战-接入skills-hooks-mcp-rules》，2026-08-16。

---

> [!info] 导航
> [[04-Skills放置与结构|← 上一章：Skills]] · [[README|返回首页]] · [[06-Subagents|下一章：Subagents →]]
