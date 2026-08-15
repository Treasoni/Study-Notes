## 2. 环境确认 + 拷贝脚手架（5 分钟热身）

第一节那 8 步能不能走完，取决于两块地基：环境是否可用、脚手架是否到手。本节只热身、不写代码——先把地基打好：确认环境 + 领到模板房。

### 环境确认三连

开工前花 1 分钟做个体检，缺哪步回第 2 章补课：

- [ ] dsh 源码仓库已 clone 到本地
- [ ] `pnpm install && pnpm run build` 已跑通
- [ ] 在仓库根目录 `pnpm dsh web --patch <某插件 dev patch>` 能起 Web UI

第 ③ 步的通过标准：终端打印 `plugin loaded!`，浏览器能开 http://127.0.0.1:3080 [^S1]。达标说明「脚手架 + 你的机器」没毛病，才值得动手改造。

### 拷贝脚手架

把 vault 里的模板房复制一份到自己工作区：

```bash
cp -r "<vault>/AI学习/DeepSeek-Harness 教程/example-plugin" ./example-plugin
```

拷贝 = 领一套带精装修的样板房：随便拆改，原件永不碰 [^S7]。拷完这些文件各司其职：

- `package.json` — 包名、构建脚本、`dsh.bundle.patch` 指向
- `tsconfig.json` — 编译配置（src → dist）
- `src/index.ts` — 注册中心：装配 Config + 注册工具
- `src/tools/repo-status.ts` — 工具本体：`repo_status` 的 defineTool
- `dev-cordis.yml` — 开发期 patch，`name` 指向本地绝对路径
- `cordis.patch.yml` — 打包期 patch，`name` 用 npm 包名

### 第一次跑通原版

把 `dev-cordis.yml` 的 `name` 改成指向 `./example-plugin/src/index.ts` 的**绝对路径**，然后加载：

```bash
pnpm dsh web --patch ./example-plugin/dev-cordis.yml
```

```text
# 预期输出
[repo-status-plugin] plugin loaded!
```

这一步证明「脚手架 + 你的环境」是通的，第三节的改造才有基线可对比。

> [!tip] 大白话
> 环境确认 = 开工前检查水电煤气都通，别等砌到一半才发现没水；拷贝 = 领到模板房钥匙，原件锁在开发商那里，房间随便你装修。

> [!note] 这在 Claude Code 里相当于
> `--patch` 指向 dev-cordis.yml，≈ Claude Code 里用 `--append-system-prompt` 或加载本地插件源码目录——都是「开发期用本地代码、不发布」的姿势。

> [!warning] 两个坑，踩了会白忙
> `--patch` 循环必须在 dsh 源码仓库根目录跑，别用 `npx @deepseek-ai/dsh`；patch 的 `name` 必须是绝对路径，相对路径会静默失效、且没有任何报错 [^S11]。

地基稳了、模板房到手了——下一节，动手把 `repo_status` 改造成你自己的 `git_log`。

## 注释

[^S1]: [官方 docs/user/develop/basic/index.md「第一个插件」](https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/user/develop/basic/index.md)（raw 镜像抓取）· official · 2026-08-15 · 首插件五步、绝对路径要求、`plugin loaded!` 预期输出、inject+tools.register

[^S7]: 本地 vault `AI学习/DeepSeek-Harness 教程/example-plugin/*` · vault-note · 2026-08-15 · 实战基底：README / package.json / tsconfig / src/index.ts / src/tools/repo-status.ts / cordis.patch.yml / dev-cordis.yml

[^S11]: 本地 vault `DeepSeek-Harness 常见坑与速查.md`（第 5 章）· vault-note · 2026-08-15 · 分环节坑清单、dsh plugin 命令族、工具契约
