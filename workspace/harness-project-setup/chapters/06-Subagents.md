# 第六章 Subagents——ctx.subagents 与 SubagentProvider

> [!summary] 本章导读
> 这是你问的「subagents 怎么配」在 dsh 里的答案。先说清最核心的差异：**Claude Code 从 `.claude/agents/*.md` 自动发现 subagent，dsh 用 `ctx.subagents.registerProvider` 显式注册**。本章给工程视角的最小挂载路径 + 关键契约速查，深挖请指路你 vault 的《DeepSeek-Harness Subagent 教程》分册（7 章，已覆盖心智/契约/选型/生命周期）。

## 6.0 先定位：工程脚手架里 subagent 只需要「选 + 挂」

写 dsh 工程时，绝大多数情况**不需要自己写 provider**——官方/社区已有现成的，你要做的是[^d4]：

1. **选 provider**：`spawn` / `fork` / `acp` / `dsh-sdk`；
2. **挂载**：在 cordis.yml 里 `dsh plugin add` + insert（或直接配 preset）；
3. **暴露给模型**：用 `dsh-tool-subagent` 把 provider 变成模型可调的工具。

只有你要「换执行后端 / 写自定义能力缝」时才去实现 `SubagentProvider`——那是 Subagent 分册第 4 章的事。

## 6.1 核心契约速查：`ctx.subagents` + `SubagentProvider`

**注册表**：`ctx.subagents` 是能力缝的「总机」[^d4]：

| 方法 | 一句话职责 |
|---|---|
| `registerProvider(provider)` | 按 `provider.name` 注册，重名失败；effect-scoped（移除阻止新 start、不撤销已返回 run） |
| `getProvider(name)` / `list()` | 只读查询 |
| `start` / `startContinuable` | 一次性前台委托 / 建立可恢复 child |
| `followup` / `interrupt` / `reportFrom` | 向可恢复 child 续发 / 停止 / 反向上报 |
| `listChildren` / `listDescendants` | 只读枚举委派树 |

**`SubagentProvider` 契约五块**（类型以官方为准，这里做字段地图）[^d4]：

```ts
const myProvider: SubagentProvider = {
  name: 'my-provider',          // ① 唯一注册名
  capabilities: {},             // ② 四 flag 启动期声明
  inheritsParentContext: false, // ③ 是否注入父对话种子（描述性标注）
  async start(request) { /* 发布后返回 handle */ },  // ④
  // prepareContinuable?(request)  // ⑤ 存在即能力
}
```

**`capabilities` 四 flag**：`outputSchema` / `depthLimit` / `toolFilter` / `persona`——启动期静态声明，请求对应能力但 provider 没声明 → **`UNSUPPORTED_CAPABILITY` 响亮拒绝**，绝不静默[^d4]。

> [!warning] 三个必记坑
> 1. **UNSUPPORTED_CAPABILITY** = 选错 provider（该换 spawn/fork 而不是 acp），不是重试能解决；
> 2. **outputSchema 请求了不保证拿到 `structured`**——消费方要回退 `output` 文本；
> 3. **`inheritsParentContext` 名不副实**——只担保「对话种子」这一件事，工具/服务/权限一概不继承。

## 6.2 选 provider：一张速查表

来自 Subagent 分册第 7 章决策速查[^d4]：

| 需求 | 选 | 一句依据 |
|---|---|---|
| 要结构化输出 / toolFilter / persona / 深度强制 | spawn / fork | in-process 四项启动期能力全支持 |
| 要子代理继承父对话上下文 | fork | `inheritsParentContext: true`，带对话种子 |
| 不想子代理看到父对话 | spawn / acp / dsh-sdk | 三者均 `inheritsParentContext: false` |
| 要驱动任意 ACP 协议 agent | acp | 独立子进程、ACP 客户端驱动 |
| 要完整独立 harness（自管模型/组合/递归预算） | dsh-sdk | 子进程是完整 peer harness；可设 `maxDepth: 'provider-managed'` |

**in-process vs out-of-process**：in-process（spawn/fork）同进程新建 child、能力全支持、无进程隔离；out-of-process（acp/dsh-sdk）独立子进程、环境变量擦除 + 独立 session root，要隔离或驱动外部协议时用[^d4]。

## 6.3 暴露给模型：`dsh-tool-subagent`

`dsh-tool-subagent` 把 provider 暴露成模型可调能力。关键配置[^d4]：

- **一个 provider 绑一个 `toolName`**，全局唯一，重复冲突；
- **maxDepth 默认 3、0 禁止委派**；dsh-sdk 上设 `'provider-managed'` 才由子 harness 自管递归预算；
- 后台 one-shot 结果经 task 工具回传（监听 task 回传而非前台 await）。

> [!note] 这在 Claude Code 里相当于
> `dsh-tool-subagent` ≈ Claude Code 的 `task` 工具；但 dsh 把「子代理 = 一条能力缝」显式化——provider 可换、能力可声明、生命周期可编程。

## 6.4 挂载示例（cordis.yml）

```yaml
- insert:
    - id: tool-subagent
      name: '@deepseek-ai/dsh-tool-subagent'
      config:
        provider: spawn          # 选 provider
        toolName: subagent       # 模型看到的工具名
        maxDepth: 3
```

> [!tip] 指路
> 想自己写 provider（三段式方法论 + 最小骨架 + 生命周期 + 工具化），读 [[DeepSeek-Harness Subagent 教程/README|Subagent 分册]]——本笔记是工程挂载视角，分册是开发深挖视角。

## 本章小结

> [!summary]
> - Claude Code `.claude/agents/*.md` 自动发现 vs dsh `ctx.subagents.registerProvider` 显式注册（effect-scoped）；
> - 工程里 subagent 只需「选 provider + 挂载 + 用 dsh-tool-subagent 暴露」，不用自己写 provider；
> - 契约五块：name / capabilities 四 flag / inheritsParentContext / start / prepareContinuable；能力不匹配 → UNSUPPORTED_CAPABILITY 响亮失败；
> - 选型速查：要能力强制 → in-process；要继承父对话 → fork；要隔离/外部协议 → acp；要完整 peer harness → dsh-sdk。

下一章：**配置体系与常见坑清单**。

---

## 素材来源

[^d4]: D4 · 你的 vault 笔记《DeepSeek-Harness Subagent 教程》（README + 第 2 章核心契约 + 第 7 章速查），2026-08-16。
