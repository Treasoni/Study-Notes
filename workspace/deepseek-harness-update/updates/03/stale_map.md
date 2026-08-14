# Stale Map · id 03 · DeepSeek-Harness 安装与快速上手.md

> 更新目标：从「安装 + 快速上手」改为「写插件必须的环境准备」（Ch2）
> 日期：2026-08-15

## 处理方式：整篇重写（patch-in-place）

| 原段落 | 判定 | 处置 |
|---|---|---|
| npm 快跑路径为主 | 降级 | 2.4 降为「只使用不开发」次选，明确「写插件别用 npx」 |
| （新增）为什么写插件必须源码路径 | 新增 | 2.1：官方插件教程以 run-from-source 为前提；开发循环 = 仓库内 pnpm dsh web --patch |
| 源码构建步骤 | 保留并强化 | 2.2：clone → pnpm install → pnpm run build → pnpm dsh web |
| Web UI 首次配置 | 保留 | 2.3 验证手段：填 Key + 选工作区 |
| headless 一次性任务 | 保留 | 2.3：退出码 0/1，适合 CI |
| 常见坑 | 保留并重排 | 2.5：端口占用 / ERESOLVE / Windows ctx.bash / 包名防伪 |

## 链接影响

- 文件名不变，wikilink 不断。
- 结尾下一章指针改为 Ch3 插件开发核心。
