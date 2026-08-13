---
title: "DeepSeek-Harness 安装与快速上手"
tags: [deepseek-harness, ai, agent, 教程, 安装]
created: 2026-08-13
updated: 2026-08-13
status: new
source_project: deepseek-harness
---

# DeepSeek-Harness 安装与快速上手：5 分钟跑通第一个会话

> [!summary] 本章导读
> 对熟悉 [[Claude Code MOC|Claude Code]] 的用户，dsh 的安装并不复杂——不需要构建任何东西，`npx` 一行即可启动。本章带你走完安装三路径、Web UI 首次配置、跑通第一个会话，并覆盖 headless 一次性任务与常见坑。

## 2.1 系统要求与安装三路径

dsh 官方未发布预构建二进制，安装方式为 npm（npx）或源码构建；Python 走 SDK。前置要求：

- **npm 方式**：仅需 Node.js，版本 `^22.19 || >=24`；
- **源码构建**：Node `^22.19 || >=24` + pnpm；
- **Python SDK**：Python 3.10+；平台限 Linux x64/arm64 或 macOS 14+ arm64；运行时无需系统 Node.js。

三路径对应命令[^1]：

```bash
# 路径一：npm（推荐），一行启动 Web UI
npx @deepseek-ai/dsh web

# 路径二：源码构建四步
git clone https://github.com/deepseek-ai/deepseek-harness.git
cd deepseek-harness
pnpm install
pnpm run build
pnpm dsh web

# 路径三：Python SDK
pip install deepseek-harness-sdk
```

> [!tip] 大白话
> npx 像「借一辆现成的车」，源码构建像「买零件自己组装」，SDK 像「租一辆会开就行」。新手用 npm 最省事。

## 2.2 Web UI 首次配置

运行 `npx @deepseek-ai/dsh web` 后，浏览器打开 **http://127.0.0.1:3080**（默认地址）。首次配置只有两步[^1]：

1. **Settings → Models 填 DeepSeek API Key**：保存即生效，无需重启。密钥是 **write-only** 的——页面只回显脱敏描述，明文存于 `$DSH_HOME/.credentials.yaml`。
2. **Choose workspace 选择项目目录**：dsh 以调用目录作为默认文件系统根。**不选工作区无法开始会话**。

> [!tip] 大白话
> 把 API Key 想成保险箱里的钥匙——填进去后，页面只告诉你「钥匙在保险箱里」，不再让你看到钥匙本身。明文只存在本机 `$DSH_HOME/.credentials.yaml`。

## 2.3 跑通第一个会话

选完工作区后，新建会话发送首个任务，官方示例：

```text
Summarize this repository and identify its main packages.
```

涉及需审批的操作会按当前权限策略弹出确认——新会话默认 `workspace-write` 权限预设（[[DeepSeek-Harness 配置体系|第三章]]详解）。到这里，第一个会话就算跑通了[^1]。

## 2.4 headless 一次性任务（CI 验证）

不想开浏览器时，用 headless 模式跑一次性任务[^1]：

```bash
dsh --profile headless "run the tests"
```

- 行为：提交任务 → 等待 agent 静默执行 → 打印最后一条非空助手消息 → 退出；
- 退出码：`0` 表示 completed，`1` 表示失败；
- 不开监听端口、无交互跟进面，适合 CI；
- 每次调用创建新 agent，**无 resume 机制**；每次任务创建全新持久化会话。

## 2.5 常见安装/上手坑

> [!warning] 高频坑
> 1. **端口被占**：Web 端口被占 → `dsh web --port <空闲端口>`；
> 2. **npm peer 冲突**：装插件时 ERESOLVE 冲突 → 加 `--legacy-peer-deps`；
> 3. **Windows 多插件重复注册 `ctx.bash`**：报 "service bash has been registered" 启动失败；
> 4. 官方不开 Issues，问题走 GitHub Discussions；
> 5. developer preview 期，升级注意破坏性变更；
> 6. 谨防与官方同名的第三方包。

---

## 本章小结

> [!summary]
> - 安装三路径：npm（推荐，`npx @deepseek-ai/dsh web`）、源码构建（clone → `pnpm install` → `pnpm run build` → `pnpm dsh web`）、Python SDK（`pip install deepseek-harness-sdk`）；
> - Web UI 首次配置两步：Settings→Models 填 Key（write-only，存 `$DSH_HOME/.credentials.yaml`）+ Choose workspace（不选无法开始会话）；
> - headless 一次性任务：退出码 0/1、无 resume，适合 CI；
> - 常见坑：端口占用、ERESOLVE、Windows `ctx.bash` 重复注册。

下一章进入全书核心：[[DeepSeek-Harness 配置体系]]。

---

[^1]: 素材来源：DeepSeek Harness 官方仓库与文档（2026-08-13 收集）。
