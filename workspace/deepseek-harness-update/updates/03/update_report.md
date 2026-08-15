# Update Report · id 03 · DeepSeek-Harness 安装与快速上手.md

## 摘要

- **动作**：update（整篇重写，patch-in-place）
- **新标题**：DeepSeek-Harness 插件开发：环境准备——源码运行路径
- **新职责**：Ch2 环境准备：写插件必须先走源码路径，5 分钟跑通开发环境
- **frontmatter**：title/tags 更新；`updated: 2026-08-15`；`status: updated`

## 变更点

1. **源码构建升级为主路径**（2.2）：官方插件教程以 run-from-source 为前提，`--patch` 加载本地插件必须在仓库上下文跑。
2. **npm 快跑降级为次选**（2.4），新增 `[!warning] 写插件别用 npx` 边界。
3. 保留 Web UI 首配（API Key write-only、选工作区）与 headless（退出码 0/1）作为验证通路。
4. 常见坑重排为环境相关：端口占用、ERESOLVE、Windows `ctx.bash` 重复注册、官方包名防伪。

## 来源

- S1（第一个插件，含 run-from-source 前提）；官方仓库 README（2026-08-15 抓取）。

## 未处理风险

- Python SDK 仅 Linux x64/arm64 或 macOS 14+ arm64 才可用；主路径建议走 Node 源码。
- 与父级 MOC 描述行待 P5 同步。
