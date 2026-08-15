## 第 6 章：第 5 步——工程化补齐

前四步我们从空目录一路写到了 `src/index.ts`（注册中心）、`src/tools/git-log.ts`（工具）和 `dev-cordis.patch.yml`（开发期补丁），插件已经能在 `dsh web --patch` 下加载。但严格说，它还是一堆能跑的 TypeScript 文件——没有 `package.json` 的目录不具备「被安装、被打包、被发布」的资格。第 5 步就是补上工程化四件套：`package.json`、`tsconfig.json`、`files` 白名单和双 patch，让项目从「手工作坊」升级成「流水线」。

> [!tip] 大白话
> 工程化像给手工作坊上流水线：`package.json` 是营业执照（注册身份、声明经营范围），`tsconfig` 是生产标准（统一怎么编译），`npm run build` 是出厂质检（产出 `dist/` 合格品）。没有这些，产品再能用也进不了市场。

### 6.1 package.json 最小字段

在插件目录根新建 `package.json`。独立插件的最小字段（[^S10]）如下：

```json
{
  "name": "dsh-git-log-plugin",
  "version": "0.1.0",
  "main": "dist/index.js",
  "types": "dist/index.d.ts",
  "dsh.bundle.patch": "./cordis.patch.yml",
  "files": ["dist", "cordis.patch.yml"],
  "scripts": {
    "build": "tsc",
    "prepare": "npm run build"
  },
  "peerDependencies": {
    "cordis": "*",
    "dsh-tools": "*",
    "schemastery": "*"
  },
  "devDependencies": {
    "cordis": "*",
    "dsh-tools": "*",
    "schemastery": "*",
    "typescript": "^5.0.0"
  }
}
```

逐字段看，最关键的是前五个：

| 字段 | 值 | 作用 |
| --- | --- | --- |
| `name` | `dsh-git-log-plugin` | 包名，全篇四名分离里的「包」；**bundle patch 的 `name` 必须等于它** |
| `version` | `0.1.0` | 语义化版本，打包 / 发布必需 |
| `main` | `dist/index.js` | Node 解析这个包的入口——必须是**编译产物**，不是 `src/index.ts` |
| `types` | `dist/index.d.ts` | 类型入口，配合 `declaration` 由 tsc 自动产出 |
| `dsh.bundle.patch` | `./cordis.patch.yml` | **声明自己是 dsh 插件**的字段，指向随包发布的 bundle 补丁 |
| `scripts.build` | `tsc` | 编译命令 |
| `scripts.prepare` | `npm run build` | 安装 / 发布前自动先构建——这是第 7 章 git 源安装「自包含构建」的前提 |

`dsh.bundle.patch` 是这个包能被 dsh 识别为 bundle 的关键：dsh 安装一个 bundle 时读这个字段找到补丁文件，把它作为一层配置合并进去。没有它，包只是普通 npm 依赖。

注意这里出现的是四名分离里的第二个名字：`export const name = 'git-log-plugin'`（诊断 / 日志）≠ `dsh-git-log-plugin`（包，本节）≠ `git-log`（patch id / 实例）≠ `git_log`（defineTool 的模型可见工具名）。四个名字各管一段，后面两节会逐个用到。

> [!note] 这在 Claude Code 里相当于
> 任何 npm 插件 / CLI 工程都有的 `main` / `types` / `files` 字段，Claude Code 插件同样要声明入口；`dsh.bundle.patch` ≈ 在包里写一句「我是 dsh 插件，这是我的激活清单」，相当于 Claude Code 插件里的激活 / manifest 声明。

### 6.2 依赖双份：cordis / dsh-tools / schemastery

插件源码里用到三个核心包：`cordis`（插件框架运行时）、`dsh-tools`（工具 DSL / 注册辅助）、`schemastery`（Config schema）。它们**同时出现在 peerDependencies 和 devDependencies**（[^S10]）：

- **peerDependencies**：声明「运行时靠宿主提供什么」。dsh 宿主环境已自带这三者，插件不该再打包一份重复副本，否则会出现「框架是 A 版、插件用 B 版」的版本割裂。
- **devDependencies**：声明「构建时需要装什么」。`src/` 直接 import 它们，`tsc` 编译时必须能解析到类型和符号，所以开发目录里也要有一份实例。

> [!tip] 大白话
> 双份依赖像「简历里写会用 Excel（peer，声明能力）+ 自己电脑上真装了 Excel（dev，干活要用）」。宿主提供的是工作电脑里的 Excel，你编译时用的是自己装的那份——两边都要有。

版本号不要照抄：`*` 是占位，要和你的 dsh 源码仓库 `pnpm-lock.yaml` 实际解析到的版本对齐（源码仓库内 `dsh-tools` 通常以 `workspace:*` 形式存在）。另外 `scripts.build` 用的是 `tsc`，所以 `typescript` 进 `devDependencies`（生产环境不需要编译器，不进 peer）；如果工具用到 Node 内置模块（如 `child_process` 跑 `git log`），再补 `@types/node`。

### 6.3 tsconfig：一份能产出 dist/ 的编译配置

新建 `tsconfig.json`。独立插件的最小配置（[^S10]）：

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ESNext",
    "moduleResolution": "Bundler",
    "declaration": true,
    "outDir": "dist",
    "rootDir": "src",
    "strict": true
  },
  "include": ["src"]
}
```

各字段为什么这么设：

- `target: ES2022`：输出语法级。插件跑在 Node 端，ES2022 覆盖现代 Node 语法，不必降级。
- `module: ESNext` + `moduleResolution: Bundler`：源码用 ESM 的 `import` / `export` 写，输出保持 ESM 模块形态，并让 tsc 按 Bundler 模式解析依赖。
- `declaration: true`：编译时同时产出 `.d.ts`——对应 `package.json` 的 `types`。
- `outDir: dist` + `rootDir: src`：`src/` 结构原样映射到 `dist/`，把 `main` 和 `types` 两个入口串起来。
- `strict: true`：全量严格检查。插件是写给框架的代码，类型安全直接关系到 execute 契约的正确性（第 3 章讲过的 canonical 值校验，靠类型先兜底）。

> [!note] 这在 Claude Code 里相当于
> `tsconfig` 就是项目的「生产标准」，Claude Code 插件的工程化同样需要 `tsconfig` + `tsc` 构建链；`declaration` 产出的 `.d.ts` 相当于给插件 API 留了类型文档。

### 6.4 files 白名单：只发布该带的

`files: ["dist", "cordis.patch.yml"]` 声明「打进 tarball 的只有这两样」（[^S10]）：

- `dist/`：编译产物，`main` / `types` 都指向这里，消费者只需要产物，不需要 `src/`。
- `cordis.patch.yml`：bundle patch，`dsh.bundle.patch` 指向的文件必须在包里。
- **不在**白名单里的 `dev-cordis.patch.yml`、`src/`、`tsconfig.json` 都不会进包：dev patch 里是机器相关的绝对路径，打进包既无意义，装到别的机器还容易误触发。

> [!tip] 大白话
> files 白名单像登机行李清单：只带 `dist/`（成品）和 `cordis.patch.yml`（激活卡）上飞机，`src/`（图纸）和 `dev-cordis.patch.yml`（本地临时工牌）留在家里。清单外一律不托运，装包体积小、也少泄密。

### 6.5 双 patch 定型：dev 用绝对路径，bundle 用包名

第 2 章只用了 `dev-cordis.patch.yml`，现在补第二份 `cordis.patch.yml`。两者结构完全一致，**唯一实质区别是插件条目的 `name`**：

`dev-cordis.patch.yml`（开发期，`pnpm dsh web --patch` 手动叠加用）：

```yaml
- insert:
    - id: git-log
      name: '/absolute/path/to/git-log-plugin/src/index.ts'   # 绝对路径（同第 2 章）
      config:
        maxCommits: 5
```

`cordis.patch.yml`（bundle 补丁，随包发布，`dsh.bundle.patch` 指向它）：

```yaml
- insert:
    - id: git-log
      name: dsh-git-log-plugin
      config:
        maxCommits: 5
```

两个关键点：

1. **`config` 块与第 4 章完全同步**：两份 patch 的 `config` 都要有 `maxCommits`，开发期行为与发布后行为一致——你验证的是什么，用户装到的就是什么。schema 默认值仍是第 4 章定死的 `maxCommits: Schema.number().default(5)`，patch 里的 `maxCommits: 5` 是显式覆盖值，两份 patch 保持一致。
2. **bundle patch 的 `name` 必须等于 `package.json` 的 `name`（`dsh-git-log-plugin`）**（[^S3]）。这是本节最容易被忽视的坑：dsh 装好 bundle 后，Node 要从 profile 的 `node_modules` 里按这个 `name` 解析已装代码；写错（沿用绝对路径、或写成 `git-log-plugin`）就会**装进去但不激活**——没有报错，只是静默不生效（[^S11]，四名分离基线见 [[DeepSeek-Harness 插件实战]]，这类坑也收录在 [[DeepSeek-Harness 常见坑与速查]]）。

`id: git-log` 仍是补丁实例 id（四名分离里的第三个名字），在补丁树「整行替换」机制里用于定位目标行——第 7 章展开。

> [!note] 这在 Claude Code 里相当于
> `dsh.bundle.patch` + `cordis.patch.yml` 的 `name` ≈ 包里声明「我是 dsh 插件」并给出激活清单；`name` 必须等于包名，相当于激活记录里的标识符必须能对应到 `node_modules` 里真实存在的那个包。

### 6.6 校准注记：独立插件 ≠ monorepo 内建包

dsh 仓库的 `docs/cookbook/adding-a-package.md` 讲的是**在 deepseek-harness 仓库内部新增内建包**的规范：用 `lib/`、`types/` 目录结构、`extends` 根 tsconfig、`references` 项目引用、`constraints` 依赖约束——这套规范**不适用于**独立插件，也不会用 `dsh.bundle.patch`（[^S2]）。

本篇只教独立插件规范（V1 example-plugin 那套：`src/` + `tsc` + `dist/` + `dsh.bundle.patch`）。**不要**把 `references` / `constraints` / extends 根 tsconfig 搬进独立插件——那会让一个本该独立发布的小包背上 monorepo 的耦合。

### 构建一次，看 dist/ 产物

补齐上述文件后，在插件目录执行：

```bash
pnpm install && pnpm run build
```

`pnpm run build` 执行 `tsc`，按 `tsconfig.json` 编译 `src/`，得到：

```
dist/
├── index.js
├── index.d.ts
└── tools/
    ├── git-log.js
    └── git-log.d.ts
```

看到这个结构，说明 `main: dist/index.js` 和 `types: dist/index.d.ts` 指向的文件真实存在了，插件已具备被 `pnpm pack` 打包、被 `dsh plugin add` 安装的资格。下一步（第 7 章）进入打包安装。

## 本章小结

- `package.json` 是工程化地基：`main` / `types` 指向 `dist/` 产物，`dsh.bundle.patch` 声明「我是 dsh 插件」，`prepare` 保证安装前自动构建。
- `cordis` / `dsh-tools` / `schemastery` 必须 **peer + dev 双份**：peer 声明运行时靠宿主提供，dev 保证构建时能解析到。
- `tsconfig` 用 `ES2022 + ESNext + Bundler + declaration + outDir + rootDir + strict`，一次编译产出 `.js` + `.d.ts`，串起 `main` 和 `types`。
- `files` 白名单只放 `dist/` 和 `cordis.patch.yml`；`dev-cordis.patch.yml` 带绝对路径，不进包。
- **双 patch 定型**：dev patch 的 `name` 用绝对路径，bundle patch 的 `name` 必须等于 `package.json` 的 `name`（`dsh-git-log-plugin`），且两边 `config` 块完全同步——否则装进去不激活。

## 脚注

[^S10]: V1 `example-plugin/` 的真实独立插件工程字段（`package.json` / `tsconfig` / dev 与 bundle patch），vault 素材，层级 4。
[^S2]: O2 `docs/cookbook/adding-a-package.md`：monorepo 内建包规范（lib/types、extends 根 tsconfig、references、constraints），本篇仅作校准排除，不适用于独立插件。
[^S3]: O3 `docs/user/develop/basic/publish.md`：bundle/profile、发布、安装与 bundle patch `name` 规则。
[^S11]: V2《DeepSeek-Harness 插件实战》：本篇一致性基线（四名分离、bundle patch name = 包名、maxCommits=5）的来源。
