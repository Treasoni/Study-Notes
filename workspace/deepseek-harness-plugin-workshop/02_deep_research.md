# DeepSeek-Harness 插件实战教学 - 深度素材（P2）

> 主题：DeepSeek-Harness 插件实战教学（A→C 完整链路：改造 example-plugin → 打包发布）
> 日期：2026-08-15
> 用途：供 P3 大纲生成与 P4 逐章写作引用。**本文件是素材库，不是成品笔记。**

## 1. Scope

面向"已读理论、环境已跑通、但从未独立写出插件"的用户，提供一份**照做即可跑通**的实战分册：
- 主线：把 `example-plugin`（repo_status）改造成用户自己的工具插件，走通 **写 → 配 → 验证 → 打包 → 安装** 全链路。
- 每步给出：可复现命令 + 预期输出 + 出错排查。
- 产出位置：Obsidian `AI学习/DeepSeek-Harness 教程/` 新增一篇分册，同步 README 与 MOC。

## 2. 来源表

| ID | 来源 | 层级 | 日期 | 用途 |
|---|---|---|---|---|
| S1 | [官方 docs/user/develop/basic/index.md「第一个插件」](https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/user/develop/basic/index.md)（raw 镜像抓取） | official | 2026-08-15 | 首插件五步、绝对路径要求、`plugin loaded!` 预期输出、inject+tools.register |
| S2 | [官方 docs/user/develop/basic/config.md「插件配置」](https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/user/develop/basic/config.md)（raw 镜像抓取） | official | 2026-08-15 | Config+Schemastery 模式、默认值、cordis.yml config、坏配置响亮失败、HMR |
| S3 | [官方 docs/cordis-tutorial/01-first-plugin.md](https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/cordis-tutorial/01-first-plugin.md)（raw 镜像抓取） | official | 2026-08-15 | cordis.yml 装配、name=模块说明符、三种插件形态、模块找不到静默丢失 |
| S4 | [官方 docs/cordis-tutorial/05-config.md](https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/cordis-tutorial/05-config.md) | official | 2026-08-15 | 坏配置→fiber FAILED / ValidationError |
| S5 | [官方 docs/architecture.md](https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/architecture.md) | official | 2026-08-15 | bundle/profile 分层概念 |
| S6 | [官方 docs/cookbook/adding-a-package.md](https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/cookbook/adding-a-package.md) | official | 2026-08-15 | 新增 bundle、--dump-config |
| S7 | 本地 vault `AI学习/DeepSeek-Harness 教程/example-plugin/*` | vault-note | 2026-08-15 | 实战基底：README / package.json / tsconfig / src/index.ts / src/tools/repo-status.ts / cordis.patch.yml / dev-cordis.yml |
| S8 | 本地 vault `DeepSeek-Harness 插件开发核心.md`（第 3 章） | vault-note | 2026-08-15 | apply/生命周期/依赖/defineTool/hook/提示词 |
| S9 | 本地 vault `DeepSeek-Harness 配置体系.md` | vault-note | 2026-08-15 | 补丁树 / Profile vs Agent Preset / Config schema / bundle vs profile |
| S10 | 本地 vault `DeepSeek-Harness 配置实战.md` | vault-note | 2026-08-15 | 配置落点选择、插件 vs hook |
| S11 | 本地 vault `DeepSeek-Harness 常见坑与速查.md`（第 5 章） | vault-note | 2026-08-15 | 分环节坑清单、dsh plugin 命令族、工具契约 |
| S12 | [pingfanfan/hello-dsh](https://github.com/pingfanfan/hello-dsh) | community | 2026-08-15 | 零基础中文实例、checkpoint、--patch 静默失败实测坑（对照参考） |

## 3. 声明↔来源映射（写作引用锚点）

### 3.1 「写」——最小插件骨架（S1, S7, S8）
- 插件 = 导出 `apply(ctx)` 的 TS 模块；`name` 仅诊断元数据（S1/S8）
- 注册工具：`export const inject = ['tools']` + `apply(ctx){ ctx.tools.register(...) }`（S1）
- `defineTool` 字段：name / description / parameters / output.{schema,render} / execute（S8 §3.4, S11 §5.3）
- **代码放哪**：`src/index.ts` = 注册中心；`src/tools/*.ts` = 工具本体（S8, S7）
- 工具契约：canonical 单一返回值 + render；基础设施失败 throw（S8/S11）

### 3.2 example-plugin 文件角色（S7）
| 文件 | 角色 |
|---|---|
| `package.json` | 包名 / main=dist/index.js / files=[dist,cordis.patch.yml] / peerDeps(3 个 @deepseek-ai/*) / scripts.build=tsc / **scripts.prepare=npm run build** / `dsh.bundle.patch=./cordis.patch.yml` |
| `tsconfig.json` | rootDir=src → outDir=dist |
| `src/index.ts` | Config interface + Schemastery schema + `export const name` + `inject=['tools']` + `apply(ctx){ ctx.tools.register(repoStatusTool(config)) }` |
| `src/tools/repo-status.ts` | `defineTool` 本体：`repoStatusTool(options)` 工厂，execute 跑 `git status --short --branch` |
| `dev-cordis.yml` | 开发 patch：`name`=**绝对路径**到 `src/index.ts`；config 传值 |
| `cordis.patch.yml` | 打包 patch：`name`=npm 包名（`dsh-repo-status-plugin`）；config 传值 |

### 3.3 「配」——Config schema（S2, S9）
- 必须导出同名 `Config` 接口 + **Schemastery schema**（普通对象不行，缺 Standard Schema 接口）（S2）
- 默认值写 schema 上：`Schema.number().default(10)`（S2）
- cordis.yml 用 `config:` 传值，覆盖默认值（S2, S7 dev/cordis patch）
- 设计原则："不硬编码可调值；两个部署可能设不同值就做成配置字段"（S2）
- 坏配置：加载即失败、报 actionable error / ValidationError、fiber 进 FAILED（S2/S4/S9）
- HMR：改配置热替换，旧实例注册自动清理（S2/S9）

### 3.4 「验证」——命令链（S1, S9, S11）
1. `pnpm dsh web --patch ./example-plugin/dev-cordis.yml` → 终端打印 `[repo-status-plugin] plugin loaded!`（S1/S7）
2. `pnpm dsh --profile web --patch ./example-plugin/dev-cordis.yml --dump-config` → 合成配置出现 `repo-status` 行（S7/S9）
3. 开 `http://127.0.0.1:3080` 新建会话让模型调用 `repo_status`（S1/S7）
4. `dsh --profile demo --dump-default-config`：只看 bundle 层，区分"bundle 错 vs 上层覆盖"（S11）
5. `dsh --profile headless "任务"`：端到端验证真实生效（S11）

### 3.5 「打包」——bundle 与安装（S5, S9, S11, S7）
- bundle = 带 `dsh.bundle.patch` 的 npm 包，贡献配置层（S5/S9）
- profile = 目录声明 `dsh.profile.bundles` 有序列表；`dsh plugin` 自动维护（S9）
- 本地安装：`pnpm install && pnpm run build` → `dsh plugin --profile demo add ./example-plugin` → `--dump-config` 出现 `# == dsh-...` 层（S7 README）
- git 安装：`dsh plugin --profile <name> add github:you/repo#<sha>`（S11）；**拉源码不跑 build**，作者要 `prepare` 脚本（S7/S9），pnpm≥10 需 `allowBuilds` 放行（S9/S11）
- `dsh plugin` 命令族：add/remove、本地目录/tarball/git（S11 §5.2）
- 排查命令：`dsh plugin --profile <name> add <pkg>` 后查 profile package.json 的 `dsh.profile.bundles`（S11/S9）

### 3.6 高频坑清单（写作必含，S11 + S7 + S2）
1. **插件路径必须绝对**（S1/S11）——patch 层不改变 loader 解析 profile 目录；相对路径静默失败
2. **四处名字混淆**（S7 拆解）：`export const name`（诊断）/ package.json `name`（bundle patch 引用）/ patch `id`（实例 id）/ defineTool `name`（模型可见工具名）
3. **patch name 双形态**（S7）：dev=绝对路径、bundle=包名；写错加载失败
4. **模块找不到静默丢失**（S3/S11）：拼写错了走 logger 可能丢，先查拼写 + `--dump-config`
5. **`inject` 服务未就绪 → PENDING 不加载**（S8/S11）
6. **Schemastery 无 `.optional()`**（S11/S2）：字段默认可选，必填 `.required(true)`
7. **补丁树整行替换、不做深合并**（S9/S11）：覆盖要重写所有需要的 key
8. **git 安装 build 坑**（S9/S11）：prepare + allowBuilds + `#<sha>` 钉 commit
9. **开发期不用 `npx @deepseek-ai/dsh`**（S7 README）：`--patch` 开发循环必须在源码仓库上下文跑

## 4. 矛盾与缺口

- **官方"安装命令"文档分散**：architecture.md 只讲概念，安装命令靠 `dsh plugin` CLI 实测（S11 命令族 + S7 README）。写作以"本地目录 add"为主、git 安装为警示，避免依赖不存在的官方安装专页。
- **cordis 教程 01 的 `cordis.yml` 最小形态**（`- name: './hello.ts'`，无 `- insert:` 包装）与 example-plugin 的 `- insert:` 形态不同：前者是 Cordis 原生装配，后者是 dsh 补丁树 insert 语义。分册统一用 `- insert:` 补丁形态（与 dsh 实际用法一致），可一句话注明差异避免读者困惑。
- **github.com 不可直接抓取**：官方文档以 raw.githubusercontent 镜像 + 本地笔记（已标注 2026-08-15 官方抓取）交叉验证，无内容冲突。

## 5. 实战指导（供 P4 章节直接使用）

### 5.1 完整命令链（照做版）
```bash
# ① 前提：源码环境已就绪（第 2 章：clone → pnpm install → pnpm run build），在 dsh 仓库根目录

# ② 拷贝脚手架
cp -r "<vault>/AI学习/DeepSeek-Harness 教程/example-plugin" ./example-plugin

# ③ 改 dev-cordis.yml 的 name 为绝对路径（指向 src/index.ts）

# ④ 启动加载（预期打印 plugin loaded!）
pnpm dsh web --patch ./example-plugin/dev-cordis.yml

# ⑤ 验证配置层（应出现 repo-status 行）
pnpm dsh --profile web --patch ./example-plugin/dev-cordis.yml --dump-config

# ⑥ 浏览器开 http://127.0.0.1:3080 新建会话，让模型调用 repo_status

# ⑦ 打包
cd example-plugin && pnpm install && pnpm run build   # 产出 dist/

# ⑧ 装进 profile
dsh plugin --profile demo add ./example-plugin
dsh --profile demo --dump-config   # 应看到 "# == dsh-repo-status-plugin" 层
dsh --profile demo
```

### 5.2 改造为新工具的最小动作（S7 adaptation_map）
1. `src/tools/` 新建 `my-tool.ts`，写 `defineTool`（name/description/parameters/output/execute）
2. `src/index.ts`：改 import + `ctx.tools.register(myTool(config))` + Config schema 加字段
3. `dev-cordis.yml`：name=自己 src/index.ts 的绝对路径
4. `cordis.patch.yml`：name=新 package.json 包名、id=新实例名、config 传值
5. 匹配关系：bundle patch `name` == package.json `name`；dev patch `name` == 绝对路径；`export const name` 仅诊断；defineTool `name` 是模型可见工具名（与 patch `id` 可不同）

### 5.3 用「大白话」预置的类比（符合用户偏好，S8 已有先例）
- `apply(ctx)` = 入职第一天领工牌（S8 已有）
- effect = 门禁卡离职自动失效（S8 已有）
- defineTool = 教模型一个新招式 / 技能登记表（S8 已有）
- 四处 name = 身份证 vs 工牌 vs 花名（新）
- Config schema = 岗位说明书 / 入职登记表（新）
- bundle = 料理包；profile = 上菜顺序单（S9/本次新增）
- allowBuilds = 发一张"在我机器上跑代码"的门禁卡（新）
- `--dump-config` = 切开千层饼看每层（S9 已有）

## 6. 待解决开放问题

1. 用户要改造的**具体新工具**是什么？（repo_status 换成什么？）——P3 大纲后与用户确认，或分册用一个通用示例（如 `dir_stats` / `note_search`）作为示范，教读者替换成自己的。
2. 分册与第 4 章（对照迁移）的关系：第 4 章是"从零对照 Claude Code 写"，本分册是"基于脚手架改造 + 打包"。需在分册导读里说明互补关系，避免重复。
3. 是否需要真正在用户机器上实操验证命令链？——本工作流产出笔记；如用户想现场跑通，可在 P4 后补一次"一起跑一遍"会话。

## 7. Downstream Handoff（给 P3/P4）

- **P3 大纲**：建议章节结构（约 5-6 节）：
  1. 实战目标与成果预览（含大白话总览）
  2. 环境确认 + 拷贝脚手架（5 分钟）
  3. 写：把 repo_status 改造成你的工具（defineTool + index.ts 注册）
  4. 配：Config schema 加可调参数 + patch 传值
  5. 验证：--patch 加载 / --dump-config / Web UI 调用 / 出错排查表
  6. 打包：bundle + profile 安装 + git 安装坑（prepare/allowBuilds/#sha）
  7. 小结 + 下一步（换你自己的工具：API 封装/笔记检索/构建脚本）
- 每节配 `[!tip] 大白话` + `[!note] 这在 Claude Code 里相当于`；代码块带语言标识；命令给"预期输出"。
- 素材引用用 S 编号脚注。
