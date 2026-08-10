---
title: DeepSeek-Reasonix 插件与扩展开发
topic: DeepSeek-Reasonix 配置教程
type: guide
difficulty: 高级
tags: [DeepSeek-Reasonix, 插件, 扩展, Extension-Protocol, Sidecar, Hooks, skills]
created: 2026-08-10
updated: 2026-08-10
status: new
source_project: deepseek-reasonix-tutorial
sources:
  - R1: "DeepSeek-Reasonix 官方仓库 (esengine, 2026) https://github.com/esengine/DeepSeek-Reasonix"
  - R2: "扩展体系总览 EXTENSIONS.zh-CN.md (esengine, 2026) https://github.com/esengine/DeepSeek-Reasonix/blob/main-v2/docs/EXTENSIONS.zh-CN.md"
  - R3: "Sidecar 协议 EXTENSION_PROTOCOL.zh-CN.md (esengine, 2026) https://github.com/esengine/DeepSeek-Reasonix/blob/main-v2/docs/EXTENSION_PROTOCOL.zh-CN.md"
  - R4: "插件包分发 PLUGIN_PACKAGES.zh-CN.md（打包、发布、分发、版本约定）(esengine, 2026) https://github.com/esengine/DeepSeek-Reasonix/blob/main-v2/docs/PLUGIN_PACKAGES.zh-CN.md"
  - R5: "Go SDK 说明 sdk/go/README.md (esengine, 2026) https://github.com/esengine/DeepSeek-Reasonix/blob/main-v2/sdk/go/README.md"
concepts:
  - extension-protocol
  - sidecar
  - plugins
  - skills
  - hooks
  - plugin-package
related_notes:
  - "[[reasonix.toml 配置详解]]"
  - "[[DeepSeek-Reasonix MCP 使用指南]]"
  - "[[DeepSeek-Reasonix ACP 协议指南]]"
  - "[[DeepSeek-Reasonix 自动化与 CI]]"
---

# DeepSeek-Reasonix 插件与扩展开发

> [!info] 文档定位
> 本文是 DeepSeek-Reasonix 的扩展开发章（04-高级功能篇第 12 章）：讲清 Extension Protocol v1 Sidecar 模式的整体架构、`[[plugins]]` 与 `[skills]` 的配置声明、版本化插件包的分发方式，以及开发一个扩展前需要掌握的机制骨架。面向已熟悉 Claude Code 插件/MCP 生态、想给 Reasonix 扩展能力的用户。本章刻意停留在「机制概览 + 官方文档指引」层面——插件协议的精确 API 与消息帧格式以官方 `docs/EXTENSIONS.zh-CN.md`、`docs/EXTENSION_PROTOCOL.zh-CN.md`、`docs/PLUGIN_PACKAGES.zh-CN.md` 与 `sdk/go/README.md` 为准，不臆造。关联：[[reasonix.toml 配置详解]]、[[DeepSeek-Reasonix MCP 使用指南]]、[[DeepSeek-Reasonix ACP 协议指南]]。

本文回答一个核心问题：**Reasonix 的「插件」到底是怎么一回事？** 如果你在 Claude Code 里用过多进程扩展、MCP server 或 settings.json hooks，这里的概念边界值得重新对齐一次——因为 Reasonix 的扩展体系把「能力提供」与「运行时介入」拆成了两个角色（MCP server 与 Sidecar），而插件本身只是你在配置里声明的一行 `name + command`。

## 一、扩展体系总览：Extension Protocol v1 Sidecar

Reasonix 的扩展体系基于 **Extension Protocol v1**，核心形态是 **Sidecar 模式**。一个扩展可以承担两类职责：

| 角色 | 提供什么 | 类比 |
|------|----------|------|
| **MCP server** | 工具（tools）、提示词（prompts）、资源（resources） | 带进来的工具箱 |
| **Sidecar** | 拦截运行时事件、提供 Provider、提供结构化 UI | 驻场观察员/协调员 |

也就是说，扩展的能力面是「标准 MCP server」——给 agent 新增可调用的工具、可复用的提示词、可读取的资源，这部分协议你在[[DeepSeek-Reasonix MCP 使用指南]]里已经熟悉。Sidecar 则更进一步：它不是一个被 agent 按需调用的工具，而是一个**常驻的旁路进程**，负责在运行时「插一脚」——拦截事件、注册 Provider（插件式 provider 体系见[[reasonix.toml 配置详解]]）、渲染结构化 UI。这两者通过**版本化插件包**统一分发。

> [!tip] 大白话
> 把扩展想成「外聘团队进驻项目」：MCP server 部分是**带进来的工具箱**（给 agent 加新工具、新提示词、新资源），Sidecar 部分是**驻场的观察员**（盯着运行过程、代管 Provider、定制界面）。
> 所以一个完整的扩展 = 工具箱 + 观察员；如果你只需要「多加几个工具」，光有工具箱（纯 MCP server）就够了。

## 二、插件类型与声明：`[[plugins]]` 与 `[skills]`

插件管理走 **`reasonix.toml` 配置声明**，没有独立的插件子命令（这点与 `reasonix mcp` 的 server 管理子命令不同，见[[DeepSeek-Reasonix MCP 使用指南]]）。

### 2.1 `[[plugins]]`：外部 stdio 插件

```toml
# [[plugins]]                         # MCP/外部 stdio 插件
# name = "example"                    # 插件标识
# command = "reasonix-plugin-example" # 启动该 stdio 插件的命令
```

字段只有两个：`name` 是插件标识；`command` 是**启动外部 stdio 进程的可执行命令**（可以是本地二进制，也可以用 `npx` 等启动器拉起）。Reasonix 按需启动这个子进程，通过 stdio 与它通信。`${VAR}` 占位符由项目根目录 `.env` 展开，但项目 `.env` **不导入 provider key**——这点与 MCP 章节一致。

### 2.2 `[skills]`：路径、排除与禁用

skills 是另一类声明式扩展，以**目录**为单位组织：

```toml
# [skills]
# paths = ["~/my-skills", "../shared/skills"]  # 加载哪些目录
# excluded_paths = ["~/.agents/skills"]        # 排除哪些目录
# disable_implicit_invocation = true           # 关闭隐式调用
# disabled_skills = ["review"]                 # 禁用哪些 skill
```

- `paths`：加载 skills 的目录列表。
- `excluded_paths`：在加载范围内排除的目录。
- `disable_implicit_invocation`：关闭隐式调用（skill 不再被自动触发，改为显式调用）。
- `disabled_skills`：按名字禁用指定 skill。

会话内用 `/skills`（main-v2 命令族收录）查看与管理；改完配置用 `/reload` 重载。

> [!tip] 大白话
> 把 skills 想成**装在文件夹里的岗位手册**：你在 `paths` 里指一下「手册都放在这几个抽屉」，`excluded_paths` 说「这几个抽屉别看」，`disabled_skills` 说「这本手册不许用」。
> 所以加载 skill 不用写代码，写路径声明就行——这跟插件（要拉起一个进程）是两种完全不同形态的扩展。

## 三、插件包分发与安装

扩展通过**版本化插件包**分发：插件被打包、打上版本号，消费方安装后在 `[[plugins]]` 里声明启动命令即可。官方文档 `docs/PLUGIN_PACKAGES.zh-CN.md` 是打包、发布与消费的权威说明。

关于社区插件源与目录约定，本文**不复述具体细节**——素材只确认了「版本化插件包分发」这一机制，具体的包注册表、安装命令与目录约定应以官方 `PLUGIN_PACKAGES.zh-CN.md` 为准，避免以讹传讹。开发者在接入任何第三方插件前，也应当先确认该包的目标版本与你的 Reasonix 版本兼容。

> [!tip] 大白话
> 把插件包想成**预装好的家用电器**：厂商打包、贴好版本号，你按说明书「插上电」（在 `[[plugins]]` 里声明 `command`）就能用。
> 至于「去哪里买、有哪些型号」，那就是 `PLUGIN_PACKAGES` 文档管的事——本章不替你编一个不存在的「应用商店」地址。

## 四、开发入门：一个扩展长什么样

### 4.1 机制骨架：Sidecar 生命周期与 stdio 通信

- 插件是**外部 stdio 进程**：配置里的 `command` 被 Reasonix 当作子进程拉起。
- 纯 MCP 形态下，通信就是 MCP 协议 over stdio（见[[DeepSeek-Reasonix MCP 使用指南]]）。
- Sidecar 形态下，进程要额外响应运行时事件、注册 Provider 与结构化 UI——这部分协议的消息帧格式在本文素材中没有可复述的细节，**请直接以官方 `docs/EXTENSION_PROTOCOL.zh-CN.md` 为唯一依据**，不要凭本章推断 API。

开发语言上，官方提供 **Go SDK**（`sdk/go/README.md`），写 Go 的扩展可以先从 SDK 入手；协议本身面向 stdio 进程，理论上其他语言只要实现协议也能接入。

### 4.2 最小插件示例思路

不臆造 API，只给「先走通哪几步」的思路：

1. **先定形态**：只需要给 agent 加工具 → 纯 MCP server 即可；需要拦截事件 / 提供 Provider / 结构化 UI → 上 Sidecar。
2. **写能力**：纯 MCP 形态就按 MCP stdio server 的标准写一个可执行程序（第 8 章已给过 `[[plugins]]` 接入示例）；Sidecar 形态先读官方 EXTENSION_PROTOCOL 文档与 Go SDK 示例。
3. **声明并验证**：在 `reasonix.toml` 里加 `[[plugins]]`：

```toml
[[plugins]]
name = "my-ext"
command = "my-ext"   # 从 PATH 可找到的可执行文件
```

4. **启动验证**：`reasonix code .` 进入 TUI，用 `/mcp`（或命令行 `reasonix mcp list` / `mcp inspect`）确认 server 被加载；写日志观察进程是否被拉起、stdio 是否通。

### 4.3 开发前先读的官方文档

| 文档 | 回答什么 |
|------|----------|
| `docs/EXTENSIONS.zh-CN.md` | 扩展体系总览，先读这个建立全局 |
| `docs/EXTENSION_PROTOCOL.zh-CN.md` | Sidecar 协议细节、消息格式、生命周期 |
| `docs/PLUGIN_PACKAGES.zh-CN.md` | 打包、发布、分发、版本约定 |
| `sdk/go/README.md` | Go SDK 用法与示例 |

## 五、Hooks：settings.json 里的轻量扩展

Hooks 与插件是两种**不同层级的扩展机制**，注意别混为一谈：

- **Hooks 不在 `reasonix.toml`**，而在 settings.json：全局 `<Reasonix home>/settings.json` + 项目 `<project>/.reasonix/settings.json` 两处（这与 Claude Code 的 settings.json hooks 位置对齐）。
- Hooks 是**事件回调**：在生命周期事件上挂一段动作，轻量、配置即用。会话内可用 `/hooks`（main-v2 收录）查看；CI 只读接口也有 `hook list/status`（见[[DeepSeek-Reasonix 自动化与 CI]]）。
- 插件是**能力提供进程**：声明在 `reasonix.toml`，拉起外部 stdio 进程，提供工具/提示词/资源/事件拦截/Provider/UI。

一句话区分：**想「在某个事件发生时就地干点事」用 hooks；想「给 agent 加一种全新的能力面」用插件。**

> [!tip] 大白话
> 把 hooks 想成**前台留言条**——贴一张「开会时喊我」的纸条（轻量，写在 settings.json），前台照做；把插件想成**常驻外包团队**——签合同、进项目、带一整套家伙事（重量级，在 reasonix.toml 里声明一个进程）。
> 所以「快速在事件上插一脚」用留言条，「要给 agent 加新能力」才需要外包团队。

## 六、常见坑

1. **插件经 `reasonix.toml` 声明，不是独立命令**。找不到 `reasonix plugin install` 之类的子命令是正常的——插件管理没有独立子命令，全靠配置声明。改配置后用 `/reload` 重载。
2. **Sidecar 与纯 MCP 的选型**。只想加工具 → 纯 MCP server 足够，别一上来就上 Sidecar；需要拦截运行时事件、提供 Provider、结构化 UI 才选 Sidecar。Sidecar 意味着一个常驻旁路进程，复杂度与资源占用都更高。
3. **项目 `.env` 只作 `${VAR}` 展开来源，不导入 provider key**。插件要用环境变量就把变量写进项目 `.env` 用 `${VAR}` 引用；provider 凭据只在全局 `<Reasonix home>/.env`。
4. **配置优先级**。插件声明写在项目 `./reasonix.toml`，被全局 `~/.reasonix/config.toml` 与命令行 flag 覆盖；「声明了不生效」按 flag > 项目配置 > 全局配置 > 内置默认的顺序排查。
5. **版本差异**。v1 与 main-v2 的文档命令列表不同，插件/扩展协议细节也可能随版本演进；实时权威是应用内 `/help` 与官方对应版本的 EXTENSION 文档。
6. **别凭本文猜协议 API**。本文只复述机制骨架，Sidecar 的消息帧与 SDK 用法以官方文档为准——写扩展前务必读 `EXTENSION_PROTOCOL.zh-CN.md` 与 `sdk/go/README.md`，否则很容易写出「协议对不上」的插件。

---

一句话收束：Reasonix 的扩展体系把「能力」与「介入」拆成两个角色——MCP server 提供工具/提示词/资源，Sidecar 提供事件、Provider 与 UI；插件在 `reasonix.toml` 里只是一行 `name + command`，分发靠版本化插件包，而轻量的事件响应交给 settings.json 里的 hooks。

## 常见问题

**Q: Reasonix 的「插件」和「MCP server」是什么关系？**
A: 插件是用户在 `reasonix.toml` 里声明的扩展单元（`name + command` 拉起的外部 stdio 进程）。它可以只包含一个 MCP server（提供工具/提示词/资源），也可以是「MCP server + Sidecar」的组合（再叠加运行时事件、Provider 与结构化 UI）。

**Q: Sidecar 到底是什么，什么时候需要它？**
A: Sidecar 是旁路的常驻进程，负责拦截运行时事件、提供 Provider 与结构化 UI。只在你要介入运行过程或定制 UI 时才需要；单纯加工具用纯 MCP server 就够了。

**Q: 插件怎么安装/管理？有没有 `reasonix plugin install` 之类的命令？**
A: 没有。插件管理走 `reasonix.toml` 配置声明，无独立插件子命令。安装 = 把插件包装好（确保 `command` 可执行）+ 在 `[[plugins]]` 里声明。

**Q: Hooks 和插件可以互相替代吗？**
A: 不能。Hooks 是 settings.json 里的轻量事件回调（全局 + 项目两处）；插件是 reasonix.toml 声明的能力进程。事件响应用 hooks，能力扩展用插件。

**Q: 想开发一个插件，第一步该读什么？**
A: 先读 `docs/EXTENSIONS.zh-CN.md` 建立全局，再按形态读 `EXTENSION_PROTOCOL.zh-CN.md`（Sidecar）或直接参考 MCP stdio server 标准（纯 MCP）；Go 开发者可从 `sdk/go/README.md` 入手。

## 相关文档

- [[DeepSeek-Reasonix MCP 使用指南]] — `[[plugins]]` 接入示例、`reasonix mcp` 管理与超时配置
- [[DeepSeek-Reasonix ACP 协议指南]] — 编辑器/IDE 接入的协议面（与扩展协议相互独立）
- [[reasonix.toml 配置详解]] — `[[plugins]]` / `[skills]` 字段书写位置与配置优先级
- [[DeepSeek-Reasonix 自动化与 CI]] — `hook list/status` 只读接口与 `reasonix run` 集成

## 参考资料

- [esengine/DeepSeek-Reasonix 官方仓库](https://github.com/esengine/DeepSeek-Reasonix)
- `main-v2/reasonix.example.toml`：`[skills]` 与 `[[plugins]]` 声明示例（素材 3.4）
- `main-v2/docs/GUIDE.zh-CN.md` 与 `docs/CONFIG_PATHS.zh-CN.md`：Hooks 位置（`<Reasonix home>/settings.json` + `<project>/.reasonix/settings.json`，素材 3.6/6.2）
- `docs/EXTENSIONS.zh-CN.md`、`docs/EXTENSION_PROTOCOL.zh-CN.md`、`docs/PLUGIN_PACKAGES.zh-CN.md`、`sdk/go/README.md`：扩展/插件协议与 SDK（素材 5.3、第八节）
- 素材第 7 节（常见坑：配置优先级、项目 `.env` 不导入 provider key、版本差异）

## 更新记录

| 日期 | 变更 |
|------|------|
| 2026-08-10 | 创建初稿（高级功能篇第 12 章，插件与扩展开发） |
