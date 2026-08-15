## 第 7 章：第 6 步——打包发布安装

前几章我们一直在 dsh 源码仓库里用 `--patch` 跑插件，插件活得好好的，但这是"临时工"状态：换台机器、或想分享给别人，都无从谈起。这一章把 `dsh-git-log-plugin` 收尾成能分发的产物：先讲清 **bundle**（作者造包）与 **profile**（用户搭家）的分工，再走一遍四层补丁树如何决定"最终配置长什么样"，最后用 `pnpm pack` 打 tarball、用 `dsh plugin` 装进 profile 并跑通，并单独交代 git 源安装的三道坎。

### 7.1 bundle vs profile：作者造包，用户搭家

先说两个最容易混的概念，它们**互斥**，各管一件事：

- **bundle**：一个 npm 包，作者在里面声明 `dsh.bundle.patch`（即上一章定型的 `cordis.patch.yml`），等于"这个包贡献一层配置"。作者造 bundle，负责把配置随包分发出去。
- **profile**：Harness home 下的一个命名目录，里面声明 `dsh.profile.bundles` 的**有序列表**，决定"这台机器要激活哪些 bundle、按什么顺序"。用户 boot profile，负责组装自己的环境。

我们第 6 章做的事就是"作者面"：把 `dsh-git-log-plugin` 的 `cordis.patch.yml` 挂在 `dsh.bundle.patch` 字段上，包一装、profile 一激活，这一层配置就进来了。[^S3] 官方架构文档把 profile 描述为"命名配置集合"，bundle 是它的一个来源，两者正交。[^S9]

这里有个决定成败的硬规则，务必记牢：**bundle patch 里的 `name` 必须等于 package.json 的 `name`**。对我们是 `dsh-git-log-plugin` 对 `dsh-git-log-plugin`。原因是 dsh 安装时把 bundle 装进 profile 的 `node_modules`，加载 patch 时 Node 靠这个 `name` 去 `node_modules` 里解析已装代码——对不上，层就静默不激活。[^S11]

> [!tip] 大白话
> bundle 像「已装修的户型包」——开发商（作者）把墙、水电、软装（配置）都做进包里；profile 像「你选好哪些户型包进自己家」——你按顺序选 3 个包，决定家里装成什么样。作者造包、用户搭家，各管各的。

> [!note] 这在 Claude Code 里相当于
> bundle ≈ npm 插件包（自带一份"安装后如何配置"的声明）；profile ≈ 你在插件市场里装进自己环境的插件集合。作者发布插件，用户选择装哪些。

### 7.2 四层补丁树：后层整行替换

上一章你已经在 `--dump-config` 里见过"分层打印"。补丁树完整地有**四层**，按序叠加：

| 层序 | 层 | 内容 |
| --- | --- | --- |
| ① | bundles 各层 | 按 profile 声明的列表顺序，逐 bundle 应用各自的 `cordis.patch.yml` |
| ② | profile 的 `cordis.patch.yml` | profile 目录里自己的 patch，覆盖 bundle 层 |
| ③ | home 级 | Harness home 层面的通用配置 |
| ④ | `--patch` 叠加 | 命令行临时追加的 patch，优先级最高 |

关键语义：**每层都作用于一张空条目表，后层按 id 定位目标行、整行替换，不做字段级深合并**。[^S9] 意思是——配置不是"一层叠一层地做字段合并"，而是按 patch 条目的 `id` 找到那一行，整个替换掉。如果 bundle 层给 `git-log` 写了 `config: { maxCommits: 5 }`，profile 层想改成 10，它必须写**同一 id 的完整行**（含要保留的所有字段），而不是只写 `maxCommits: 10` 指望"合并"。

> [!tip] 大白话
> 四层补丁树像「千层饼」：每层饼都是独立的，后压上去的层不是跟下面融合，而是把同一块位置整个盖住。你以为"只改了一个参数"，实际是把那一整行配置都换掉了。

这也解释了最常见的排查盲区：改完配置发现不生效——不是没加载，而是**前层被后层整行顶掉**，或者你改的是 bundle 层、被 profile/home 层覆盖了。遇到"我以为改了但被覆盖"，先去 `dsh --profile demo --dump-config` 看 `git-log` 那一行最终落在哪层。另外注意：如果 profile 里声明了一个**没有 `dsh.bundle.patch` 声明**的普通包，dsh 只把它装成普通依赖、给一次告警，**不会**把它当成配置层激活。[^S3]

### 7.3 打包：pnpm pack 打 tarball

发布有两条路：推到 npm registry（长期分享），或 `pnpm pack` 打个 tarball（临时分发 / 自用）。后者不用注册表，最适合验证流程。在第 6 章工程目录根目录执行：

```bash
pnpm pack
```

输出类似（产物受第 6 章 `files` 白名单限制，只有 `dist/` 和 `cordis.patch.yml`）：

```bash
Tarball Contents:

120B package.json
3.2kB dist/index.js
1.1kB dist/index.d.ts
1.5kB cordis.patch.yml

Tarball Details
name: dsh-git-log-plugin
version: 0.1.0
packageSize: 5.8 kB
unpackedSize: 16.4 kB
totalFiles: 4

npm notice
npm notice 📦  dsh-git-log-plugin@0.1.0
npm notice Tarball Contents
npm notice 120B  package.json
npm notice 3.2kB dist/index.js
npm notice 1.1kB dist/index.d.ts
npm notice 1.5kB cordis.patch.yml
npm notice Total Files: 4
npm notice == Tarball Contents ==
```

这一步顺便自检了第 6 章的 `files` 白名单：如果 `dist/index.js` 没打进去，说明构建没跑或白名单写错——tarball 里没有产物，装进 profile 就是个空壳。包名 `dsh-git-log-plugin` 与 bundle patch 的 `name` 一致，才谈得上激活。

### 7.4 安装：dsh plugin --profile demo add

拿到 tarball（路径记作 `/path/to/dsh-git-log-plugin-0.1.0.tgz`），用 `dsh plugin` 命令族装进一个名为 `demo` 的 profile：

```bash
dsh plugin --profile demo add /path/to/dsh-git-log-plugin-0.1.0.tgz
```

`dsh plugin` 内部**转发 pnpm 的完整动词**（add / remove 等），所以语法基本可以按 pnpm 的习惯写：装 tarball 写文件路径，装 registry 包写包名，装 git 源写 `git+https://...#sha`（见 7.6）。tarball 和本地目录两种安装方式**不需要** `allowBuilds` 放行——因为产物已经在那里，没有"装完再跑构建脚本"这一步。[^S14][^S8] 从源码仓库根目录跑 `dsh plugin` 依旧成立。

> [!tip] 大白话
> `dsh plugin add` 像「物业帮你把包装进门」——你不需要自己研究入户线路、强弱电怎么走，物业（dsh plugin 命令）按规矩把包放进正确的位置（profile 的 node_modules 和 bundles 列表）并登记在册。

### 7.5 跑通已装插件：dsh --profile demo

装完后直接带 profile 启动，看插件自身的加载日志：

```bash
dsh --profile demo
```

正常会看到类似输出（诊断名是第 1 章定的 `git-log-plugin`）：

```bash
[info] profile "demo" loaded, bundles: dsh-git-log-plugin
[git-log-plugin] plugin loaded!
[info] Harness is running. Press Ctrl+C to exit.
```

此刻插件已不再是"开发期 `--patch` 注入"，而是真正作为 bundle 从 profile 激活。这里有一条贯穿全章的纪律：**profile 永不手写**——它的 `dsh.profile.bundles` 列表、`node_modules`、`pnpm-workspace.yaml` 全由 `dsh plugin` 命令自动维护对账。你想加包、换版本、删包，都走 `dsh plugin --profile demo <add|remove|...>`，而不是去改 profile 目录里的文件；手写很容易写坏对账关系，装进去却不激活。[^S3][^S12]

### 7.6 git 源安装三坑（未实测）

`dsh plugin --profile demo add git+https://github.com/you/dsh-git-log-plugin.git#v0.1.0` 这类 git 源安装很方便，但有三道坎。**以下内容以官方 publish 文档为准，本篇教学未真机复现，动手时以实际报错为准**[^S3]：

**坑①：git 源拉的是源码，不是产物。** git 依赖只 clone 仓库源码，不会带上 `dist/`。所以作者必须在 package.json 里提供 `scripts.prepare`（第 6 章已配：`"prepare": "npm run build"`），让安装方 clone 后自动自包含构建。没有 prepare，装进来只有源码、没有可加载的 `dist/index.js`。

**坑②：pnpm ≥ 10 默认拒跑 git 依赖的 prepare 构建脚本。** 这是 pnpm 的安全策略：外来 git 依赖要跑任意构建脚本，必须先显式放行。当你 `dsh plugin add` 一个 git 源包时，pnpm 会在终端打印一串需要放行的包 key（如 `dsh-git-log-plugin`）并拒绝继续；你要把打印的包 key 抄进 profile 的 `pnpm-workspace.yaml` 的 `allowBuilds` 列表，再重跑安装命令：

```yaml
# profile 的 pnpm-workspace.yaml（由 dsh plugin 维护，此处仅示意放行字段）
allowBuilds:
  dsh-git-log-plugin: true
```

放行后重跑 `dsh plugin --profile demo add git+...#sha`，prepare 才会被允许执行。tarball / 本地目录安装没有这一步，因为产物不需要现场构建。

**坑③：用 `#sha` 钉 commit。** git 依赖默认跟着分支走，哪天仓库变了你本地就悄悄升级，配置可能突然对不上。规范做法是钉死一个 commit 或 tag：`git+...#<40 位 commit sha>` 或 `...#v0.1.0`，保证每次安装的是同一份代码。[^S3]

> [!note] 这在 Claude Code 里相当于
> `allowBuilds` ≈ 包管理器对「安装后要跑构建脚本」的插件逐包给信任；不信任就不让脚本跑。Claude Code 生态里安装需要原生编译或构建钩子的包时，同样会遇到类似的放行确认。

## 本章小结

- **bundle（作者造包，贡献一层配置）与 profile（用户搭家，声明有序 bundles）互斥**；bundle patch 的 `name` 必须等于 package.json 的 `name`，Node 才能从 profile 的 `node_modules` 解析到已装代码。[^S3][^S11]
- **四层补丁树**：bundles 各层 → profile patch → home 级 → `--patch`；后层按 id **整行替换**、不做字段级深合并，排查"配置没生效"先 `--dump-config` 看目标行落在哪层。[^S9]
- **打包用 `pnpm pack`**（受 `files` 白名单约束）或 `npm publish`；**安装用 `dsh plugin --profile demo add <tarball>`**，tarball / 本地目录无需 `allowBuilds`。[^S3]
- **profile 由 `dsh plugin` 自动对账，永不手写**；缺 dsh 声明的包只装为普通依赖 + 一次告警，不激活层。[^S12]
- **git 源安装三坑（未实测）**：prepare 自包含构建、pnpm≥10 的 `allowBuilds` 放行、`#sha` 钉 commit。[^S3]

下一章把全篇压缩成一张「从零到装好」的路线图，串起 `dsh web --patch` → `--dump-config` → headless → `pnpm pack` → `dsh plugin add` 这条完整命令链。

---

[^S3]: 官方 `docs/user/develop/basic/publish.md`（bundle/profile / 发布 / 安装 / git 坑）。
[^S9]: 官方 `docs/architecture.md`（bundle/profile 分层 / 四层补丁树）。
[^S11]: 《DeepSeek-Harness 插件实战》§6（bundle patch name = 包名）。
[^S12]: 《DeepSeek-Harness 配置体系》（bundle/profile 心智模型）。
[^S14]: 《DeepSeek-Harness 常见坑与速查》（`dsh plugin` 命令族）。
