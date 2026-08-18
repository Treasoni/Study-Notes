---
title: "DeepSeek-Harness 插件开发 · 第 5 章：速查与排错"
tags: [deepseek-harness, ai, agent, 插件, 教程, 速查]
created: 2026-08-13
updated: 2026-08-15
status: updated
source_project: deepseek-harness
---

# DeepSeek-Harness 插件开发 · 第 5 章：速查与排错

> [!summary] 本章导读
> 最后一章是写插件时的常驻速查：按环节排的高频坑、命令速查（含 `dsh plugin` 全家族）、工具契约速查、配置引用与 launcher 规则。遇到问题先翻这里，再决定回看哪一章。

## 5.1 插件开发高频坑（按环节）

| 环节 | 坑 | 处理 |
|---|---|---|
| 注册 | 插件路径写了相对路径 | **必须绝对路径**——patch 层不改变 loader 解析模块路径时的 profile 目录[^1] |
| 注册 | 模块找不到 / 加载静默失败 | 路径拼错走 logger 可能丢失，先查拼写；`--dump-config` 看合成配置[^2] |
| 依赖 | 插件一直不加载 | `inject` 声明了未就绪服务 → 保持 PENDING；检查服务是否存在 |
| 依赖 | Windows 多插件重复注册 `ctx.bash` | 报 "service bash has been registered" 启动失败，避免重复注册 |
| 配置 | 坏配置加载失败 | `Config` schema 校验失败 → fiber FAILED，报错精确（ValidationError）[^3] |
| 构建 | git 安装插件找不到 `lib/` | git 拉的是源码不跑 build；作者要 `prepare` 脚本，用户 `allowBuilds` 放行[^4] |
| 安装 | npm peer 冲突（ERESOLVE） | 加 `--legacy-peer-deps` |
| 运行 | Web 端口被占 | `dsh web --port <空闲端口>` |
| 升级 | developer preview 破坏性变更 | 升级前留意 README 变更，接口可能不兼容 |
| 生态 | 同名第三方包 | 认准 `@deepseek-ai/dsh` 与 `deepseek-harness-sdk` |

## 5.2 命令速查表

### 启动 / 调试

| 命令 | 用途 |
|---|---|
| `dsh web` | 启动 Web UI（`--profile web` 硬编码别名） |
| `dsh web --port <端口>` | 端口被占时换端口 |
| `dsh --profile headless "任务"` | 一次性任务，退出码 0/1，适合 CI |
| `dsh --profile <name> --dump-config` | 打印合成配置（bundle + profile + home 补丁） |
| `dsh --profile <name> --patch <extra.yml> --dump-config` | 叠加 `--patch` 覆盖层后打印 |
| `dsh --profile <name> --dump-default-config` | 只看 bundle 层合成结果 |

### `dsh plugin` 全家族

| 命令 | 用途 |
|---|---|
| `dsh plugin --profile <name> add <package>` | 安装插件/包（转发 pnpm；首个 bundle 自动初始化 profile） |
| `dsh plugin --profile <name> remove <package>` | 移除依赖 + 配置层 |
| `dsh plugin --profile <name> add ./hello-plugin` | 安装本地目录包 |
| `dsh plugin --profile <name> add github:you/hello-plugin#<sha>` | 从 git 安装（钉 commit） |
| `dsh plugin --profile <name> add ./hello-plugin-0.1.0.tgz` | 安装 tarball |

## 5.3 工具契约速查

### defineTool 字段

| 字段 | 含义 | 要点 |
|---|---|---|
| `name` | 工具名 | 模型经此调用 |
| `description` | 模型看到的描述 | 决定「何时被调用」，要写清边界 |
| `parameters` | 参数 schema | `execute` 前自动校验，推断 TS 类型 |
| `output.schema` | canonical 返回值声明 | `execute` 只返回这一个值 |
| `output.render` | 转成模型可见内容 | 展示层，别在返回值里塞 prose |
| `async execute(args)` | 执行体 | 基础设施失败 throw（= isError）；业务成功态放 canonical 值 |

### hook 扩展点（工具策略与观察）

| 扩展点 | 用途 |
|---|---|
| `tools/pre-execute` | allow / deny / ask 决策（权限门） |
| `ctx.tools.guard()` | 单调最终拒绝，后面的监听者无法撤销 |
| `tools/execute` | 包 dispatch 加超时、重试、指标 |
| `tools/post-execute` | 替换展示内容或返回值、附加上下文 |
| `tools/result` | 只读观察不可变的最终结果 |

### 长任务与取消

- **后台长任务**：`run_in_background` 经 `ctx.jobs.start` 做，不阻塞工具循环；
- **取消**：`execute` 接收 `exec`，遵守 `exec.signal` 取消进行中的工作；
- **异步通知**：`exec.agent.inject()` 在工具运行中异步注入消息。

## 5.4 配置引用速查

### 多层补丁树（后层整行替换，不做深合并）

1. bundle 补丁（profile `dsh.profile.bundles` 列表顺序）
2. profile 自身 `cordis.patch.yml`
3. home 级 `$DSH_HOME/cordis.patch.yml`（机器级，共享）
4. `--patch <path>` 覆盖层（argv 顺序）

要点：覆盖某行要**重写它需要的每个 key**，不只写改动的那个；用户可在自己 profile 层覆盖 bundle 行而不改你的包[^4]。

### 运行时值：`!!js` 标签

`config` 与 `disabled` 字段可用 `!!js` 算运行时值：

```yaml
- insert:
    - id: my-app
      name: '@example/my-app'
      config:
        port: !!js ctx.myAppStartup.port ?? 8080
```

### launcher 规则

> [!warning]
> 标志必须在 app 参数之前；launcher 解析器消费一个 `--`（app 参数要字面 `--` 需写 `-- --`）；launcher 标志在第一个无法识别的 token 处结束。

### 热重载与关闭

profile 启动时监听 profile 与 home 两个 `cordis.patch.yml` 的编辑并事务性重放；进程关闭给插件树最多 5 秒清理，首个 SIGINT/SIGTERM 触发优雅排空（SIGTERM 退出码 0，SIGINT 报 130），第二个信号强制立即退出。

## 5.5 模型协议参考（接 DeepSeek V4 时）

写会做模型调用的插件、或直接配 DeepSeek V4 后端时留意（第三方整理）[^5]：

- **thinking 默认开启**，会烧 token；
- 多轮对话必须回传 `reasoning_content`，否则 HTTP 400；
- 必须设 `max_tokens`（否则 reasoning 流可达 26KB/84s 撑爆客户端）；
- thinking 模式下 `tool_choice` 只能 `auto`。

> [!tip] 大白话
> V4 的 thinking 像「默认开了录音」——每次都先烧一段思考 token；多轮对话不把上次的思考笔记还回去，服务端就直接拒绝（HTTP 400）。

## 5.6 生态资源与下一步

- **官方反馈**：GitHub Discussions（官方唯一反馈渠道，不开 Issues）；
- **社区**：Discord 与微信群；
- **插件生态**：约 300 个，通过 `dsh plugin --profile <name> add <package>` 安装；
- **官方包名清单**：npm `@deepseek-ai/dsh`、Python `deepseek-harness-sdk`、MCP 客户端 `@deepseek-ai/dsh-mcp-client`；
- **下一步**：回顾 [[DeepSeek-Harness 是什么|第 1 章]]心智模型 → [[DeepSeek-Harness 安装与快速上手|第 2 章]]环境 → [[DeepSeek-Harness 插件开发教程/01-插件开发核心-从apply到system-prompt|第 03 章]]核心（配置细节见 [[DeepSeek-Harness 插件开发教程/02-配置体系-补丁树Profile与bundle|配置专册]]）→ [[DeepSeek-Harness 与ClaudeCode对照迁移|第 4 章]]实战，把例子换成你自己的工具（API 封装 / 笔记检索 / 构建脚本），流程不变。

---

## 本章小结

> [!summary]
> - 高频坑集中在插件路径（必须绝对）、`inject` 依赖未就绪、git 安装不跑 build、Windows `ctx.bash` 重复注册；
> - 命令速查：`--dump-config` / `--dump-default-config` 排查合成配置，`dsh plugin` 全家族管理安装；
> - 工具契约：canonical 返回值 + render、基础设施失败 throw、`ctx.jobs.start` 做长任务；
> - 配置：多层补丁树整行替换、`!!js` 运行时值、launcher 标志前置、HMR 热重载；
> - 反馈走 GitHub Discussions；dsh 属 developer preview，插件 API 可能变动。

至此五章全部完成。

---

## 更新记录

- 2026-08-15：从「常见坑 + 命令速查 + V4 协议」重构为「插件开发速查与排错」。新增 5.1 插件开发环节化坑清单、5.2 `dsh plugin` 全家族、5.3 工具契约速查（defineTool / hook 扩展点 / 长任务）；原 V4 协议降为 5.5 模型协议参考。

---

[^1]: 素材来源：官方「你的第一个插件」（2026-08-15 抓取）。
[^2]: 素材来源：官方 Cordis 教程 01「第一个插件」（2026-08-15 抓取）。
[^3]: 素材来源：官方 Cordis 教程 05「配置」（2026-08-15 抓取）。
[^4]: 素材来源：官方「打包并安装插件」（2026-08-15 抓取）。
[^5]: 素材来源：DeepSeek Harness 官方仓库与文档（2026-08-13 收集）。
