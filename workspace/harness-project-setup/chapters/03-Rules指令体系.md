# 第三章 Rules/指令体系——AGENTS.md、CLAUDE.md 与 workspaceContext

> [!summary] 本章导读
> 这是你迁移成本最低的一块：**你的 `CLAUDE.md` 在 dsh 里原样生效，零迁移**。但「零迁移」背后有一套精确的加载规则——默认读哪些文件、按什么顺序、项目根怎么找、字节预算怎么控。搞懂它，你才知道什么时候该写 `AGENTS.md`、什么时候写 `AGENTS.local.md`、什么时候动 `workspaceContext`。

## 3.1 默认读哪些文件：`AGENTS.md` + `CLAUDE.md` 都读

dsh 官方源码里 `instructionFileCandidates` 的默认值就是 **`['AGENTS.md', 'CLAUDE.md']`**[^b3][^d1]——它从 session 工作目录向上找最近的含 `.git` 的祖先作为项目根，逐个目录加载这些文件。

> [!example] 实操结论
> 什么都不用做。你现在的 `CLAUDE.md` 在 dsh 里照常被读。想加「只在这个项目生效」的补充，再写一个 `AGENTS.md`；想加「机器级偏好」，写 `~/.dsh/AGENTS.md`。

## 3.2 项目根怎么找 + 加载顺序

| 机制 | 规则 | 来源 |
|---|---|---|
| 项目根 | 从 session 工作目录向上找**最近含 `.git` 的祖先**；无 `.git` 用当前 cwd；`ctx.fs` 可用时走 fs 服务探测 | B3 |
| 加载范围 | 逐目录向上加载候选文件 | B3 |
| 本地覆盖 | 同目录 **`AGENTS.local.md` / `CLAUDE.local.md`** 在基础文件之后加载（覆盖同名目录的重复内容）；`localInstructionFileCandidates` 空则禁用 overlay | B3, D1 |
| 用户级 | 固定读 **`~/.dsh/AGENTS.md`**（`$DSH_HOME` 下），所有项目共享 | B3, D1 |

## 3.3 `workspaceContext`：字节预算与开关

`@deepseek-ai/dsh-agent-instructions` 插件（"User-facing workspace instruction loader configuration"）拥有 AGENTS.md/CLAUDE.md 加载能力。在 spine bundle 里字段是 `workspaceContext`[^b3]：

| 配置键 | 含义 |
|---|---|
| `dshHome` | harness home，含固定的用户全局 `AGENTS.md`；默认 `$DSH_HOME` 或 `~/.dsh` |
| `projectRootMarkers` | 标识项目根的目录项（向上 walk 用） |
| `maxBytes` | **一个渲染 baseline/动态批次的 UTF-8 字节上限**；非正数或非有限禁用加载 |
| `maxSourceBytes` | 单条指令文件读取的 UTF-8 上限；更大的文件被忽略 |
| `instructionFileCandidates` | 同目录项目候选；每个存在的文件都加载（同目录重复内容折叠到最早候选） |
| `localInstructionFileCandidates` | 本地覆盖候选，基础文件之后加载；空则禁用 |

**设 `false` 可整体关闭**：官方注释明确 "Workspace context instead requires an explicit byte budget or `false` because it changes model-visible input"——关闭后得到 hermetic prompts[^b3]。

> [!note] 这在 Claude Code 里相当于
> Claude Code 的 `claudeMdExcludes` / 记忆上限。dsh 用一个显式字节预算（`maxBytes`）而不是「行数」来约束指令文件对模型可见输入的影响。

## 3.4 官方仓库自身的惯例：CLAUDE.md symlink AGENTS.md

dsh 官方仓库 root/packages/examples 三处都用 `CLAUDE.md` symlink 到 `AGENTS.md`，**edit 真文件**（即 `AGENTS.md` 是 canonical source）[^b1]。

> [!tip] 迁移建议
> 如果你从 Claude Code 迁过来、想保持单一事实源：把规则写进 `AGENTS.md`（canonical），`CLAUDE.md` 用 symlink 或 `@AGENTS.md` import 指向它。dsh 两个都读，哪个是真文件都行，但别双份维护。

## 3.5 常见坑

1. **写了 `AGENTS.md` 又写 `CLAUDE.md` 两份重复规则**——两个都会加载，内容不一致时以覆盖顺序为准；不如一个真文件 + 一个 symlink/import。
2. **指令文件太大**——超过 `maxSourceBytes` 的单个文件被**忽略**（不是截断）；合理设置 `maxBytes` 控制模型可见输入，避免「陈规坟场」。
3. **以为 hooks/mcp 也放 `.dsh/`**——`.dsh` 只管技能 + 用户级 home；hooks/mcp 走 `cordis.yml`（第 5、7 章）。

## 本章小结

> [!summary]
> - `instructionFileCandidates` 默认 `['AGENTS.md', 'CLAUDE.md']`——**CLAUDE.md 零迁移**；
> - 项目根 = 最近含 `.git` 的祖先；逐目录向上加载；本地覆盖 `AGENTS.local.md`/`CLAUDE.local.md`；用户级 `~/.dsh/AGENTS.md`；
> - `workspaceContext` 控制自动加载与字节预算（`maxBytes`/`maxSourceBytes`/`projectRootMarkers`），设 `false` 整体关闭 → hermetic prompts；
> - 官方惯例：`CLAUDE.md` symlink `AGENTS.md`，edit 真文件；别双份维护。

下一章：**Skills——往哪放、怎么写、扫描优先级**。

---

## 素材来源

[^b1]: B1 · dsh 官方仓库 `AGENTS.md`，2026-08-16 抓取。
[^b3]: B3 · dsh 官方 `docs/config-catalog.md`（workspaceContext / agent-instructions），2026-08-16 抓取。
[^d1]: D1 · 你的 vault 笔记《03-配置实战-接入skills-hooks-mcp-rules》，2026-08-16。
