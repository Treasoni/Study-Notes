## 6. 打包——bundle 打包 + profile 安装 + git 安装的坑

第 5 节证明了开发期插件能跑；本节把插件变成「能分发给别人的料理包」，装进 profile，让 `git_log` 在普通启动下也能被模型调用。

### 打包：产出 `dist/`

```bash
cd example-plugin && pnpm install && pnpm run build
```

**预期输出**：`tsc` 编译完成，`example-plugin/dist/` 下出现 `index.js`、`index.d.ts`。

动手前先看 `package.json` 三个关键点（S7 实测）[^S7]：

1. **入口 + 发布白名单**：`main: "dist/index.js"` + `files: ["dist", "cordis.patch.yml"]`——`npm publish` 只带这两样，源文件和 dev 配置不上架；
2. **build + prepare**：`scripts.build = "tsc -p tsconfig.json"`（rootDir=src → outDir=dist）、`scripts.prepare = "npm run build"`——`prepare` 是「装依赖时自动 build」的钩子，是后面 git 安装能用的前提；
3. **bundle 声明**：`dsh.bundle.patch = "./cordis.patch.yml"`——告诉 dsh「这个包贡献一层配置」。

先钉死两个词：**bundle** = 带 `dsh.bundle.patch` 声明的 npm 包（料理包）[^S5]；**profile** = 目录里声明 `dsh.profile.bundles` 的有序列表（上菜顺序单）[^S9]。`dsh plugin` 命令自动维护 profile，不用手写。

### 本地安装三步

```bash
# ① 把 ./example-plugin 装进 demo profile（dsh 命令在 dsh 源码仓库根目录或已安装 CLI 下运行）
dsh plugin --profile demo add ./example-plugin

# ② 打开 profile 的 package.json —— dsh.profile.bundles 应出现该包

# ③ 看合成配置：应出现 bundle 贡献的层
dsh --profile demo --dump-config
```

**预期输出**（③）：`--dump-config` 里出现

```text
# == dsh-git-log-plugin
```

这一行来自 bundle 的 `cordis.patch.yml`——注意 patch 的 `name` 必须等于 package.json 的 `name`（`dsh-git-log-plugin`），Node 才能从 profile 的 node_modules 里找到已安装代码[^S7]。

### git 安装的坑（警示为主）

官方没有独立的「安装命令」专页，命令族以 `dsh plugin` CLI 实测为准[^S11]：

```bash
dsh plugin --profile <name> add github:you/repo#<sha>
```

git 安装拉的是**源码**不是构建产物，所以三个坑：

1. 包必须带 **`prepare`** 脚本——装依赖时自动 build，否则装进去是缺 `dist/` 的半成品；
2. **pnpm≥10 默认拒绝跑 git 依赖的 `prepare`**——需要 **`allowBuilds`** 放行；
3. 用 **`#<sha>`** 钉死 commit，保证可复现。

> [!tip] 大白话
> - **bundle** = 料理包：预制好的菜，拿出来热一下就能上桌；**profile** = 上菜顺序单：先上哪个 bundle 的配置层。
> - **allowBuilds** = 给 git 依赖发一张「在我机器上跑 build 脚本」的门禁卡：pnpm 不放心陌生人喂的脚本，你签字它才跑。

> [!note] 这在 Claude Code 里相当于
> bundle 打包发布 ≈ Claude Code 插件市场：把自定义 slash command 或 MCP server 打包分发；`dsh plugin add` ≈ 安装第三方插件并启用。

安装后模型在 Web UI 里照样能调 `git_log`——现在你的插件已经能给别人用了。

## 注释

[^S5]: 官方 [docs/architecture.md](https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/architecture.md)（raw 镜像抓取）— official，2026-08-15。用途：bundle/profile 分层概念
[^S7]: 本地 vault `AI学习/DeepSeek-Harness 教程/example-plugin/*` — vault-note，2026-08-15。用途：实战基底（README / package.json / tsconfig / src/index.ts / src/tools/repo-status.ts / cordis.patch.yml / dev-cordis.yml）
[^S9]: 本地 vault `DeepSeek-Harness 配置体系.md` — vault-note，2026-08-15。用途：补丁树 / Profile vs Agent Preset / Config schema / bundle vs profile
[^S11]: 本地 vault `DeepSeek-Harness 常见坑与速查.md`（第 5 章）— vault-note，2026-08-15。用途：分环节坑清单、dsh plugin 命令族、工具契约
