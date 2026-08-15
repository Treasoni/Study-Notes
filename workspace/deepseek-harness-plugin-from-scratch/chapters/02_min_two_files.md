## 第 2 章：第 1 步——空目录 + 最小 2 文件跑通

这一章是全篇的第一个关键里程碑。目标只有一个：用一个空目录、两个文件，让 dsh 在启动时真的把「你写的插件」加载起来，并在日志里看到 `[git-log-plugin] plugin loaded!`。这一步不碰任何脚手架、不建 `package.json`、不编译——纯粹验证「空目录 + 2 文件 → 加载」这条链路是通的。走通它，后面所有章节（加工具、加配置、打包安装）才有地基。

### 2.1 建目录：`mkdir git-log-plugin && cd git-log-plugin`

先明确一个前置：所有开发期的验证命令（`pnpm dsh ...`）都要在 **dsh 源码仓库根目录能访问到的位置**执行，因为我们用的是源码仓库自带的 dsh CLI，而不是全局装的 npx 版本。所以插件目录也建在源码仓库根目录下面：

```bash
# 在 dsh 源码仓库根目录执行
mkdir git-log-plugin
cd git-log-plugin
```

> [!tip] 大白话
> 把源码仓库想成「整栋楼」，`git-log-plugin/` 是你刚租下来的一间毛坯房。你得在这栋楼里干活没错，但「住哪间、门牌号多少」是后面 patch 里要写清楚的事——现在先把房间建出来。

目录名直接用 `git-log-plugin`，对应一致性基线里的「诊断名」：后面 `export const name` 也用同一个名字，第一步就对齐，免得后面再改。注意这一步我们**不需要** `package.json`——那是第 6 章工程化才出现的东西，现在两文件起步最干净。

### 2.2 写 `src/index.ts` 最小版

插件本体是一个普通的 TypeScript 模块。先建 `src/` 目录，再写入口文件：

```bash
mkdir -p src
```

```ts
// src/index.ts
import type { Context } from '@deepseek-ai/cordis'

export const name = 'git-log-plugin'

export function apply(ctx: Context) {
  console.log(`[${name}] plugin loaded!`)
}
```

逐行拆开看：

1. `import type { Context } from '@deepseek-ai/cordis'` — 纯类型导入：`import type` 保证编译后这行直接被擦掉。`Context` 只是给 `apply` 参数做类型标注，运行时的上下文对象由 cordis 自己注入，你不 import 也会拿到它。
2. `export const name = 'git-log-plugin'` — 插件在日志/诊断里的名字，也就是四名分离的**第一个名字（诊断名）**[^S11]。它 ≠ 包名 `dsh-git-log-plugin` ≠ patch id `git-log` ≠ 工具名 `git_log`。这一章只用得上它，但先把「四个名字是四件事」记牢，第 3、6 章会逐个落地。这条基线来自系列里的 [[DeepSeek-Harness 插件实战]]，两篇可以对照读。
3. `export function apply(ctx: Context)` — 插件入口。cordis 加载到插件后调用它。`ctx` 是上下文句柄，这一章还只拿它做占位，第 3 章开始用它取工具注册表 `ctx.tools`。
4. `console.log(\`[${name}] plugin loaded!\`)` — 插件自己的加载日志。模板串展开后就是 `[git-log-plugin] plugin loaded!`，这里的 `name` 正是第 2 步的常量——日志前缀和诊断名天然一致。

> [!note] 这在 Claude Code 里相当于
> `export function apply(ctx)` ≈ 插件入口的初始化钩子——就像 Claude Code 插件加载时执行的那个初始化回调；`console.log` 打出的加载日志 ≈ 插件模块被 require/import 时打印的启动日志。它们共同证明一件事：**你的代码真的被宿主加载并执行了**。

### 2.3 写最小 patch yml：`- insert:` 注册

模块写好了，但 dsh 还不知道它的存在——`src/index.ts` 只是躺在文件系统里的一份文件。patch 文件就是「登记表」：用 `- insert:` 把插件注册进运行时的那张配置表。在 `git-log-plugin/` 根目录写 `dev-cordis.patch.yml`：

> [!tip] 大白话
> 把两个文件的分工想成「员工本人」和「前台登记表」：`src/index.ts` 是员工本人（会干活），patch yml 是登记表（写上「这号人今天来上班」）。只有登记过（`- insert:`），员工才会被叫去 apply；没登记，本事再大也白搭。

```yaml
# dev-cordis.patch.yml
- insert:
    index: 0
    items:
      - type: 'cordis'
        id: 'git-log'
        name: '<你的 deepseek-harness 仓库绝对路径>/git-log-plugin/src/index.ts'
```

逐行看：

- `- insert:` — patch 的最小编排动作：「往配置表里插一行」。patch 文件就是一个动作列表，`- insert:` 是其中一种；这一章只用得到它。具体字段以官方最小骨架为准，见脚注 [^S1]。
- `index: 0` — 插到表头。只插一个插件时插哪都行，0 最直观。
- `type: 'cordis'` — 标记这一行是一个 cordis 插件条目，告诉加载器「这是一个插件，不是别的配置」。
- `id: 'git-log'` — 这一条目的实例 id，也就是四名分离的**第三个名字（patch id）**。它标识「这个实例」，和 `export const name` 的 `git-log-plugin` 是两回事：一个是「这个插件叫什么」，一个是「这张登记表里这一行叫什么」。
- `name:` — **关键**：必须填 `src/index.ts` 的**绝对路径**。把 `<你的 deepseek-harness 仓库绝对路径>` 换成你机器上的真实路径（macOS 形如 `/Users/你/deepseek-harness/git-log-plugin/src/index.ts`，Linux 形如 `/home/你/deepseek-harness/...`）。

为什么必须绝对路径：patch 的 `name` 会被加载器**直接当文件系统路径**去定位模块，它不会相对工作目录做任何换算[^S14]。写相对路径等于指了一个「在加载器眼里不存在」的地址。

> [!warning] 易错点：name 必须是绝对路径，相对路径静默失效
> 把 `name` 写成 `./git-log-plugin/src/index.ts` 或 `src/index.ts`，**不会报错，也不会警告**——只是模块永远加载不上，日志里永远没有 `[git-log-plugin] plugin loaded!`。这种「没报错的静默」是新手最容易被消耗时间的地方：你以为配置生效了，其实那行根本没被加载。第一步就写绝对路径，能省掉后面所有迷惑。

> [!tip] 大白话
> patch 里的绝对路径 `name` 像门禁卡必须写门牌号：你得写「楼栋 + 房间号」这种绝对地址。写相对路径等于拿一张写着「自己屋里」的门禁卡去刷——这栋楼里根本没有一间叫「自己屋里」的房间，刷了没反应，还不报错。所以：要么写 `src/index.ts` 的完整绝对路径，要么等第 6 章换成按包名安装的写法（bundle patch），那条路不用绝对路径。

### 2.4 加载命令：`pnpm dsh web --patch ./dev-cordis.patch.yml`

现在还在 `git-log-plugin/` 目录里，直接运行：

```bash
# 仍在 git-log-plugin/ 目录里执行（它在 dsh 源码仓库内部）
pnpm dsh web --patch ./dev-cordis.patch.yml
```

期望输出（时间戳/日志级别格式随版本略有差异，关键是那行 `[git-log-plugin] plugin loaded!`）：

```text
[12:00:01] INFO  loading plugin git-log (cordis)
[12:00:01] INFO  [git-log-plugin] plugin loaded!
[12:00:01] INFO  Web UI listening on http://127.0.0.1:3080
```

命令会一直前台运行（Web 服务）。看到三行日志后，浏览器打开 http://127.0.0.1:3080，在 Web UI 的日志/控制台面板里也能看到同样的 `[git-log-plugin] plugin loaded!`。验证完 `Ctrl+C` 退出即可。

三个必须讲清的要点：

1. **为什么在插件目录里能跑 `pnpm dsh web`**：`git-log-plugin/` 建在源码仓库内部，`pnpm` 会向上找到 workspace 根部的 dsh CLI。开发期**不用 npx**——npx 会去全局或远程找 dsh，跟你正在源码里改的东西完全脱节。反过来，如果插件目录建在源码仓库**外面**，`pnpm dsh` 就找不到命令了[^S11]。
2. **`dsh web` 是 `dsh --profile web` 的硬编码别名**：`web` 不是某个参数值，是 CLI 层写死的快捷方式，含义是「用 web 这个 profile 跑起来并开 Web 服务」。想换 profile 就写 `dsh --profile <名字> --patch ...`，第 5 章会用到。
3. **为什么 patch 文件叫 `dev-cordis.patch.yml`**：大纲落定的命名——第一步就用 `dev-` 前缀，给第 5 步的打包 patch（bundle patch，`cordis.patch.yml`）留好命名空间，避免以后改名。现在这份就是「开发期手工挂载」的 dev patch，用 `--patch` 指定路径加载。

### 2.5 校准认知：「plugin loaded!」是插件自己的日志

重要校准：`[git-log-plugin] plugin loaded!` 这行**完全是插件自己写的**——就是 `src/index.ts` 里那句 `console.log`。dsh 只负责「找到模块 → 调用 apply」，它不会替你打任何带你自己名字前缀的日志，框架/CLI 里也不存在「加载插件就打印 hello」这种特性[^S1]。

这个认知直接决定排错方向：

- **看到这行** → 模块被加载了，`apply` 被调了，链路通。
- **没看到这行** → 先别怀疑 dsh，大概率是模块根本没被加载：检查 patch 的 `name` 绝对路径是否写对、`--patch ./dev-cordis.patch.yml` 相对路径是否在正确的目录下执行。对照 [[DeepSeek-Harness 常见坑与速查]] 里的排错顺序，第一步先查「登记表」，而不是查「dsh」。

> [!note] 这在 Claude Code 里相当于
> 插件被 require 时打的那条启动日志本来就是你写的，宿主不会替你发明日志——同理，`plugin loaded!` 这个文本是你 `console.log` 出来的，别把它当成 dsh 自带能力去依赖。哪天你想改这行字，改的是自己插件里的 `console.log`，而不是 dsh 的任何配置。

### 本章小结

- 最小 2 文件 = 插件模块 `src/index.ts` + 注册 patch `dev-cordis.patch.yml`，不依赖脚手架、不需要 `package.json`。
- `export const name`（`git-log-plugin`）是四名分离的**诊断名**；patch 的 `id`（`git-log`）是实例 id，两个名字不是一回事。
- patch 的 `name` 必须写 `src/index.ts` 的**绝对路径**，相对路径静默失效（无报错无警告）——第一步就写对，能避开最经典的排查陷阱。
- 加载命令在 dsh 源码仓库内执行 `pnpm dsh web --patch ./dev-cordis.patch.yml`：开发期不用 npx；`dsh web` 是 `--profile web` 的硬编码别名。
- `[git-log-plugin] plugin loaded!` 是插件自身的 `console.log`，不是 dsh 的特性；看不到它时先查 patch 路径，而不是怀疑 dsh。

下一步：插件能被加载了，但它还没有任何「能力」。第 3 章给它加第一个工具 `git_log`——把 `apply(ctx)` 升级成真正的注册中心，用 `ctx.tools.register` 把工具挂给模型。这两个文件会升级成三个文件，四名分离也从「知道」变成「落地」。

---

[^S1]: 官方「Your first plugin」：`deepseek-harness/docs/user/develop/basic/index.zh.md`。最小 2 文件骨架（`import type { Context } from '@deepseek-ai/cordis'` + `export const name` + `export function apply(ctx)`）、`- insert:` 注册、`pnpm dsh web --patch` 加载命令；官方 index 不覆盖 package.json/tsconfig/打包（工程化缺口是本分册增量）。
[^S14]: 本系列《DeepSeek-Harness 常见坑与速查》（V5）：patch `name` 必须绝对路径、相对路径静默失效，及 dsh 命令族排错顺序。
[^S11]: 本系列《DeepSeek-Harness 插件实战》（V2）：一致性基线（`git_log` / 四名分离 / `maxCommits=5`）与「验证命令在 dsh 源码仓库根目录执行、开发期不用 npx」口径。
