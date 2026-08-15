---
topic: DeepSeek-Harness 从零写插件（空目录手写全文件）
run_id: deepseek-harness-plugin-from-scratch
created: 2026-08-15
status: confirmed
direction: A（渐进式从零：先最小 2 文件跑通 → 再补工程化 → 打包安装）
---

# 02 深度素材（P2）

## 范围

方向 A：从空目录手写一个 dsh 插件，先按官方「最小 2 文件」跑通加载，再补齐 package.json/tsconfig 工程化，最后验证 → 打包 → 安装。示范工具 **git_log**（与《插件实战》同名，可对照）。

## 来源表

| 编号 | 来源 | 类型 | 层级 | 用途 |
|------|------|------|------|------|
| O1 | `docs/user/develop/basic/index.zh.md`（Your first plugin） | official | 5 | 最小 2 文件骨架 + 加载命令 |
| O2 | `docs/cookbook/adding-a-package.md` | official | 5 | ⚠️ monorepo 内建包规范（校准用，不直接教） |
| O3 | `docs/user/develop/basic/publish.md` | official | 5 | bundle/profile / 发布 / 安装 / git 坑 |
| O4 | `docs/user/develop/basic/tool.md` | official | 5 | defineTool 五件套 |
| O5 | `docs/cookbook/adding-a-tool.md` | official | 5 | execute() 契约（canonical / throw=isError） |
| O6 | `docs/user/develop/basic/config.md` | official | 5 | Config schema（.required() 校准） |
| O7 | `docs/cordis-tutorial/05-config.md` | official | 4 | ValidationError / fiber FAILED |
| O8 | `apps/cli/reference/README.md` | official | 5 | dsh CLI 全家族 / 验证命令精确语法 |
| O9 | `docs/architecture.md` | official | 4 | bundle/profile 分层 / 四层补丁树 |
| V1 | `example-plugin/`（package.json / tsconfig / dev / bundle patch） | vault | 4 | 独立插件真实字段（dist/ + dsh.bundle.patch） |
| V2 | 《DeepSeek-Harness 插件实战》 | vault | 4 | 一致性基线（git_log / 四处名字 / maxCommits=5） |
| V3 | 《DeepSeek-Harness 配置体系》 | vault | 3 | bundle/profile 中文心智模型 / Profile vs Preset |
| V4 | 《DeepSeek-Harness 插件开发核心》 | vault | 4 | 文件归属 / apply 三形态 / defineTool 契约 |
| V5 | 《DeepSeek-Harness 常见坑与速查》 | vault | 3 | dsh plugin 命令族 / 绝对路径坑 |

## Claim / Source 映射

### 阶段①：最小 2 文件跑通（O1 + V5 + V2§5.1）

| Claim | 来源 |
|-------|------|
| 最小骨架仅 2 文件：插件模块（`src/my-plugin.ts`）+ `cordis.yml` | O1 |
| 模块导出 `export const name` + `export function apply(ctx)`；`import type { Context } from '@deepseek-ai/cordis'` | O1 |
| apply 里 `console.log('[hello-plugin] plugin loaded!')` 是插件自身日志，非 CLI 功能 | O1 / O8 校准 |
| patch 用 `- insert:` 注册；`name` 必须是**绝对路径**，相对路径静默失效 | O1 / V5§5.1 |
| 加载命令：`pnpm dsh web --patch <yml>`，开 http://127.0.0.1:3080 | O1 |
| 官方 index.md **不覆盖** package.json / tsconfig / 打包 → 工程化缺口是本分册增量 | O1 |

### 阶段②：工具 DSL + Config（O4 / O5 / O6 / O7 + V4 + V2）

| Claim | 来源 |
|-------|------|
| defineTool 收单个配置对象：name / description / parameters / output / execute | O4 |
| parameters 类 JSON-schema：`{ type, required, description }`，属性级 required 布尔 | O4 |
| output = `{ schema, render }`；render 把 canonical 值转文本块 `[{ type: 'text', text: value }]` | O4 |
| execute(args) 返回 output.schema 声明的 **唯一 canonical JSON 值**，不返回内容块 | O4 / O5 |
| args 由 schema 推断类型、框架自动校验、视为只读；exec 含 identity+token+signal | O5 |
| **抛错或返回非法值 = isError**；注册表捕获 throw，失败不泄漏给模型 | O5 |
| **基础设施失败 throw；业务成功态放 canonical 值** | O5 |
| 注册即 effect：卸载 fiber 自动注销工具 | O5 |
| schema 自动流入系统提示词组装，无需手拼 | O5 |
| apply 注册：`ctx.tools.register(defineTool({...}))`；`inject = ['tools']` 等工具注册表就绪 | O4 / V4 |
| Config 两段式：`export interface Config` + `export const Config: Schema<Config> = Schema.object({...})` | O6 |
| **必填用 `.required()`（官方从不用 `.required(true)` 或 `.optional()`）**；可选靠 TS `?` | O6 ★校准 |
| 默认值写 schema 上 `.default(value)` | O6 |
| 禁止导出普通对象作 Config（缺 Standard Schema 接口） | O6 |
| schema 在插件加载时运行；坏配置 → ValidationError / fiber FAILED / 永不半启动 | O6 / O7 |
| apply 总收到完整校验后的 config | O7 |
| 文件归属：src/index.ts 注册中心；工具本体放 src/tools/*.ts | V4 |

### 阶段③：工程化（V1 + O2 校准）

| Claim | 来源 |
|-------|------|
| **独立插件规范 ≠ O2 的 monorepo 内建包规范**（后者用 lib/types、extends 根 tsconfig、references、constraints，**不含 dsh.bundle.patch**，不要教给独立插件读者） | O2 ★校准 |
| 独立插件 package.json 最小字段：name / version / main=dist/index.js / types=dist/index.d.ts / `dsh.bundle.patch="./cordis.patch.yml"` / scripts.build=tsc / scripts.prepare=npm run build | V1 |
| cordis/dsh-tools/schemastery 进 peerDependencies + devDependencies 双份 | V1 / O2 |
| tsconfig：target=ES2022 / module=ESNext / moduleResolution=Bundler / declaration=true / outDir=dist / rootDir=src / strict=true | V1 |
| files 白名单（`["dist","cordis.patch.yml"]`）| V1 |

### 阶段④：验证命令链（O8 + V2§5）

| Claim | 来源 |
|-------|------|
| 命令在 dsh 源码仓库根目录执行（开发期不用 npx） | V2§5 |
| `dsh web` = `--profile web` 硬编码别名 | O8 |
| `dsh web --patch <dev.yml>` → 见插件自身 `plugin loaded!` 日志 | O1 / V2 |
| `dsh --profile <name> --dump-config`：打印 bundle + profile patch + home patch + --patch 全层 | O8 |
| `dsh --profile <name> --dump-default-config`：只打印 bundle 层 | O8 |
| dump 打文件名注释、`!!js` 不求值、stderr 报未命中 | O8 |
| `dsh --profile headless "<task>"`：一次性任务，stdout 打印文本，退出码 **0=completed / 1=otherwise**，无任务文本=usage 错误 | O8 |
| 缺 profile 时自动初始化（web/headless 用模板，其他用 @deepseek-ai/dsh-base 首 bundle） | O8 / O3 |

### 阶段⑤：打包安装（O3 / O9 + V3 + V5 + V2§6）

| Claim | 来源 |
|-------|------|
| **bundle = npm 包贡献一层配置**（声明 dsh.bundle.patch）；**profile = Harness home 下命名目录，声明 dsh.profile.bundles 有序列表** | O3 / O9 |
| 作者造 bundle、用户 boot profile，二者互斥；profile 永不手写，`dsh plugin` 自动维护对账 | O3 / V3 |
| **四层补丁树**：bundles 各层（列表序）→ profile 的 cordis.patch.yml → home 级 → `--patch` 叠加；每层应用于空条目表 | O3 / O9 |
| **后层整行替换，不做字段级深合并**；按 id 定位目标行 | O9 / V5§5.4 |
| bundle patch 的 `name` **必须等于 package.json 的 name**（Node 从 profile node_modules 解析已装代码） | V2§6 / O3 |
| 发布：npm registry 或 `pnpm pack` tarball | O3 |
| 安装：`dsh plugin --profile <name> add <pkg>`（本地目录 / git#sha / tarball / registry）；转发 pnpm 全动词 | O3 / O8 |
| **git 安装三坑**：①拉源码不拉产物 → 作者须 `prepare` 自包含构建；②pnpm≥10 拒跑 git 依赖 prepare → 把打印的包 key 抄进 profile 的 pnpm-workspace.yaml allowBuilds 再重跑；③`#sha` 钉 commit | O3 / V2§6 |
| tarball / 本地目录安装无需 allowBuilds | O8 |
| 缺 dsh 声明的包仅装为普通依赖 + 一次告警，不激活层 | O3 |
| Profile（进程级装哪些 bundle）与 Agent Preset（会话级工具/提示词）**正交两轴** | V3 |

## 矛盾与校准（写分册时必须处理）

1. **`.required()` 口径**：本地《插件实战》§4 写「无 .optional()，必填用 `.required(true)`」；官方 O6 明确「从不用 `.required(true)` 或 `.optional()`，必填用 `.required()`」。→ 新分册以官方为准写 `.required()`；保留「无 .optional()、字段默认可选（用 TS `?`）」；加一句校准注记说明旧笔记差异。
2. **O2 与独立插件是两套规范**：O2（lib/types、references、constraints）只适用于 deepseek-harness 仓库内部建包；独立插件按 V1（dist/、dsh.bundle.patch、tsc -p）。→ 分册只教独立插件规范。
3. **`docs/user/develop/advanced/bundle.md` / `profile.md` 不存在**（404 已核实）→ 引用 publish.md + architecture.md。
4. **「plugin loaded!」是插件自身 console.log**（诊断名 = export const name），不是 dsh 框架/CLI 特性 → 按「插件自身日志」表述。
5. **四名分离**：export const name（诊断/日志）≠ package.json name（包）≠ patch id（实例）≠ defineTool name（模型可见工具名）。示范固定：`git-log-plugin` / `dsh-git-log-plugin` / `git-log` / `git_log`。

## 实战指引（方向 A 渐进式主线）

1. 空目录 `mkdir git-log-plugin && cd` → 写 `src/index.ts`（先只 name+apply+console.log）+ 手写最小 patch yml → `pnpm dsh web --patch ./dev-cordis.yml` → 看到 `[git-log-plugin] plugin loaded!`
2. 加工具：`src/tools/git-log.ts` 工厂 + defineTool；index.ts 加 inject=['tools']、Config、register
3. 加 Config：interface Config + Schema.object({ maxCommits: Schema.number().default(5) })；两份 patch 加 config 块
4. 验证：--dump-config 分层看 git-log 层；headless 端到端
5. 工程化：package.json（name/version/main/types/dsh.bundle.patch/scripts）+ tsconfig（ES2022/ESNext/Bundler/declaration/dist/strict）+ `pnpm install && pnpm run build`
6. 打包安装：`pnpm pack` 或 npm publish → `dsh plugin --profile demo add ./tarball` → `dsh --profile demo` 跑通；git 源三坑单独一节

## 未决问题

- 分册是否保留「最小 2 文件」时 cordis.yml 直接放根目录 vs 放 dev-cordis.yml（先最小，后改名为 dev 双 patch）→ 大纲定
- headless 验证是否需要 Web UI 截图 → 默认文本对照
- git 安装坑是否真机复现 → 教学以官方文档为准，标注「未实测」

## 下游交接（给 outline-generator / chapter-writer）

- 一致性基线：name=`git-log-plugin` / package `dsh-git-log-plugin` / id `git-log` / tool `git_log` / config `maxCommits: 5`
- 每个核心概念带 `[!tip] 大白话` + `[!note] 这在 Claude Code 里相当于`（系列约定）
- 脚注引用源编号 O1-O9 / V1-V5
- 校准注记：`.required()` vs `.required(true)` 差异
