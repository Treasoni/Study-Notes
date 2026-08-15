---
title: "DeepSeek-Harness 插件开发：环境准备"
tags: [deepseek-harness, ai, agent, 插件, 教程, 安装]
created: 2026-08-13
updated: 2026-08-15
status: updated
source_project: deepseek-harness
---

# DeepSeek-Harness 插件开发：环境准备——源码运行路径

> [!summary] 本章导读
> 写插件和「只使用 dsh」要求不一样：官方插件文档的第一步就是「从源码运行」（run from source）。这一章带你把源码仓库克隆、构建、跑通，并验证 Web UI 与 headless 两条通路——它们是后续写插件时的调试环境。

## 2.1 为什么写插件必须走源码路径

官方插件教程（第一个插件 / 开发一个 Tool）都以「仓库 checkout 已完成 run-from-source」为前提[^1]。原因是开发期的插件用**相对仓库的绝对路径**挂进插件树（`cordis.yml` patch），并且你要在仓库里跑 `pnpm dsh web --patch ...` 来加载它。只 `npx @deepseek-ai/dsh web` 的安装方式没有仓库上下文，无法承载开发循环。

> [!tip] 大白话
> npx 是「借一辆现成的车开」，源码构建是「买零件自己组装」。写插件等于要改零件，所以必须自己有一辆能拆的车。

## 2.2 源码构建四步

前置要求：Node `^22.19 || >=24` + pnpm[^1]。

```bash
# 1. 克隆官方仓库
git clone https://github.com/deepseek-ai/deepseek-harness.git
cd deepseek-harness

# 2. 安装依赖
pnpm install

# 3. 构建
pnpm run build

# 4. 启动 Web UI（默认 http://127.0.0.1:3080）
pnpm dsh web
```

> [!note] 版本与兼容
> dsh 处于 developer preview，README 明确 "THERE WILL BE COMPATIBILITY-BREAKING CHANGES."。升级前留意 README 变更；接口可能随时不兼容。

## 2.3 快速验证：Web UI 首配 + headless

### Web UI 首次配置

启动后浏览器打开 **http://127.0.0.1:3080**（默认地址）。首次配置只有两步[^1]：

1. **Settings → Models 填 DeepSeek API Key**：保存即生效，无需重启。密钥是 **write-only** 的——页面只回显脱敏描述，明文存于 `$DSH_HOME/.credentials.yaml`。
2. **Choose workspace 选择项目目录**：dsh 以调用目录作为默认文件系统根。**不选工作区无法开始会话**。

> [!tip] 大白话
> 把 API Key 想成保险箱里的钥匙——填进去后，页面只告诉你「钥匙在保险箱里」，不再让你看到钥匙本身。明文只存在本机 `$DSH_HOME/.credentials.yaml`。

跑通第一个会话：新建会话发送 `Summarize this repository and identify its main packages.`，涉及需审批的操作会按当前权限策略弹确认——新会话默认 `workspace-write` 权限预设。

### headless 一次性任务

不想开浏览器时，用 headless 模式跑一次性任务[^1]：

```bash
pnpm dsh --profile headless "run the tests"
```

- 行为：提交任务 → 等待 agent 静默执行 → 打印最后一条非空助手消息 → 退出；
- 退出码：`0` 表示 completed，`1` 表示失败；
- 不开监听端口、无交互跟进面，适合 CI；
- 每次调用创建新 agent，**无 resume 机制**；每次任务创建全新持久化会话。

## 2.4 npm 快跑路径（只使用不开发）

只想用 dsh、不写插件时，npm 一行即可，无需源码：

```bash
# 路径一：npm（推荐），一行启动 Web UI
npx @deepseek-ai/dsh web

# 路径二：Python SDK（Python 3.10+，仅 Linux x64/arm64 或 macOS 14+ arm64）
pip install deepseek-harness-sdk
```

> [!warning] 写插件别用 npx
> 开发插件必须回到源码路径（2.2）。npm 安装没有仓库上下文，`--patch` 加载本地插件的开发循环跑不起来。

## 2.5 常见环境坑

> [!warning] 高频坑
> 1. **端口被占**：Web 端口被占 → `pnpm dsh web --port <空闲端口>`；
> 2. **npm peer 冲突**：装插件时 ERESOLVE 冲突 → 加 `--legacy-peer-deps`；
> 3. **Windows 多插件重复注册 `ctx.bash`**：报 "service bash has been registered" 启动失败；
> 4. 官方不开 Issues，问题走 GitHub Discussions；
> 5. developer preview 期，升级注意破坏性变更；
> 6. 谨防与官方同名的第三方包（认准 `@deepseek-ai/dsh`）；
> 7. **`pnpm not found`**：新环境常没装 pnpm。先 `node --version` 确认满足 `^22.19 || >=24`，再 `npm install -g pnpm`（最简单）或 `brew install pnpm` 安装，装完 `pnpm --version` 验证；npm 也不可用时走官方脚本 `curl -fsSL https://get.pnpm.io/install.sh | sh -`。

---

## 本章小结

> [!summary]
> - **写插件必须源码运行路径**：clone → `pnpm install` → `pnpm run build` → `pnpm dsh web`；
> - 验证两条通路：Web UI（首配 = 填 Key + 选工作区）与 headless（退出码 0/1，适合 CI）；
> - 只使用不开发时用 `npx @deepseek-ai/dsh web`；写插件时回到源码路径；
> - 常见坑：端口占用、ERESOLVE、Windows `ctx.bash` 重复注册。

下一章进入全书核心：[[DeepSeek-Harness 插件开发核心]]——插件到底是什么、怎么写、怎么依赖、怎么发布（注册与装配细节见配套 [[DeepSeek-Harness 配置体系|配置体系]]）。

---

## 更新记录

- 2026-08-15：全套重构为「写自己的 dsh 插件」主线；源码运行路径升级为主路径，npm 快跑降为次选；明确「写插件别用 npx」的边界。
- 2026-08-15：2.5 高频坑新增 `pnpm not found` 排查与安装方法。

---

[^1]: 素材来源：DeepSeek Harness 官方仓库与文档（2026-08-15 收集）。
