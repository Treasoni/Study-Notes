# DeepSeek-Harness 插件实战教学 - 探测结果（P1）

> 主题：DeepSeek-Harness 插件实战教学（写 + 配置 + 打包 全链路）
> 日期：2026-08-15
> 探测透镜：① 官方文档实操路径 ② example-plugin 脚手架拆解 ③ 实战坑点与验证命令

## 方向菜单（请选择主线路）

| 方向 | 做法 | 优点 | 依据 |
|---|---|---|---|
| **A. 改造 example-plugin 出新工具（推荐）** | 复制本地 `example-plugin` → 把 `repo_status` 改成你自己的工具 → 加 Config 配置项 → `--patch` 加载验证 → 打包 bundle → 装进 profile | 最快建立"我能写插件"的信心；环境已跑通、脚手架已验证，全链路最顺 | 透镜② adaptation_map |
| **B. 从零手写最小插件** | 不复制，从空目录亲手创建 package.json / tsconfig / src/index.ts / src/tools/my-tool.ts / 两个 patch，理解每个文件为什么存在 | 理解最深，不留黑盒；官方「第一个插件」+ cordis 教程 01 直接支撑 | 透镜① index.md / cordis-01 |
| **C. 发布交付优先** | 主线路是打包 bundle + profile 安装 + git 安装（prepare / allowBuilds / #sha 钉死），目标"能分发给别人用" | 覆盖复用/交付场景，补官方文档缺失的安装命令实操 | 透镜③ 配置体系§4 |

> 说明：三方向不互斥。推荐 A 为主线、C 为收尾（写+配+打包全链路正好落在 A→C）。

## 候选来源（去重后）

| # | 来源 | 层级 | 分 | 用途 |
|---|---|---|---|---|
| 1 | [deepseek-harness docs/user/develop/basic/index.md「第一个插件」](https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/user/develop/basic/index.md) | official | 5 | 「写+注册」最小闭环权威起点 |
| 2 | [docs/user/develop/basic/config.md「插件配置」](https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/user/develop/basic/config.md) | official | 4 | Config + Schemastery + HMR |
| 3 | [docs/cordis-tutorial/01-first-plugin.md](https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/cordis-tutorial/01-first-plugin.md) | official | 4 | function/object/class 三形态最小插件 |
| 4 | [docs/cordis-tutorial/05-config.md](https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/cordis-tutorial/05-config.md) | official | 5 | 坏配置→fiber FAILED、精确 ValidationError 出处 |
| 5 | [docs/architecture.md（插件/Bundle/Profile）](https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/architecture.md) | official | 3 | bundle/profile 分层概念、dsh 字段 |
| 6 | [docs/cookbook/adding-a-package.md](https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/cookbook/adding-a-package.md) | official | 4 | 新增 bundle 与 `--dump-config` 摊开 |
| 7 | [@deepseek-ai/dsh-base（npm 基底 bundle）](https://www.npmjs.com/package/@deepseek-ai/dsh-base) | official | 3 | dsh.bundle 声明补丁层官方范例 |
| 8 | [pingfanfan/hello-dsh（零基础中文插件教程）](https://github.com/pingfanfan/hello-dsh) | community | 4 | 22 实例、checkpoint、--patch 静默失败实测坑 |
| 9 | 本地 vault：`DeepSeek-Harness 常见坑与速查.md` | vault-note | 5 | 分环节坑清单 + dsh plugin 命令族 |
| 10 | 本地 vault：`DeepSeek-Harness 配置体系.md` | vault-note | 5 | 补丁树 / Config schema / bundle vs profile |
| 11 | 本地 vault：`DeepSeek-Harness 配置实战.md` | vault-note | 4 | 插件 vs hook / 配置落点选择 |
| 12 | 本地 vault：`example-plugin/`（repo_status 脚手架） | vault-note | 5 | 实战基底（skeleton / 命令链 / 改造映射） |
| — | jishuzhan 社区文章 / Discussion #380 | report/community | 4/3 | 补充实测坑（schemastery 无 .optional()、dispose 时序） |
| — | dsh-plugin-doctor（npm） | community | 2 | 存在但 403 未核实，**不纳入** |

## 关键提取（供 P2 直接使用）

### example-plugin 最小骨架（透镜②）
- `package.json`（包名 / main / files / `dsh.bundle.patch`）+ `tsconfig.json`（rootDir=src→outDir=dist）
- `src/index.ts`：`inject=['tools']` + Config schema + `apply(ctx){ ctx.tools.register(...) }`
- `src/tools/my-tool.ts`：`defineTool`（name/description/parameters/execute）
- `dev-cordis.yml`（开发 patch，`name`=绝对路径）与 `cordis.patch.yml`（打包 patch，`name`=npm 包名）

### 命令链（透镜②）
1. 拷脚手架 → 2. 改 dev-cordis.yml 绝对路径 → 3. `pnpm dsh web --patch ./dev-cordis.yml`（看到 plugin loaded）→ 4. `--dump-config` 验证配置层 → 5. Web UI 会话调用工具 → 6. `pnpm install && pnpm run build` → 7. `dsh plugin --profile demo add ./example-plugin` → 8. `--dump-config` 出现 bundle 层

### 高频坑（透镜③，教程必须覆盖）
1. **四处名字混淆**：`export name`（诊断）/ package.json `name`（bundle patch 引用）/ patch `id`（实例）/ defineTool `name`（模型可见工具名）——改错必踩空
2. **patch `name` 双形态**：bundle=包名、dev=绝对路径；开发期写成包名/相对路径会加载失败
3. **git 安装只拉源码不跑 build**：作者必须给 `prepare` 脚本；pnpm≥10 默认拒绝跑 git 依赖的 prepare，须 `allowBuilds` 放行 + `#<sha>` 钉 commit
4. **Schemastery 没有 `.optional()`**：必填用 `.required(true)`，默认值写 schema；不能用普通对象
5. **坏配置要响亮失败**：校验失败→fiber FAILED、精确 ValidationError；不静默兜底
6. **补丁树整行替换、不做深合并**：覆盖某行要重写所有需要的 key
7. **`inject` 声明未就绪服务 → 插件保持 PENDING 不加载**；勿重复注册 `ctx.bash`

### 验证命令（透镜③）
- `dsh --profile <name> --dump-config`：摊开合成配置树，证明插件行已入列
- `--patch <extra> --dump-config`：验证覆盖层整行替换语义
- `--dump-default-config`：只看 bundle 层，区分是 bundle 错还是上层覆盖
- `dsh plugin --profile <name> add <pkg>` 后查 profile package.json 的 `dsh.profile.bundles`
- `dsh --profile headless "任务"`：端到端验证插件运行时真正生效

## 覆盖缺口

- 官方「安装命令」独立文档缺失（architecture.md 只讲概念）——P2 以 `dsh plugin add` 实测 + 本地笔记为主补足
- github.com 无法 WebFetch：官方文档以 raw.githubusercontent 镜像 / 搜索摘要 + 本地笔记（已标注 2026-08-15 官方抓取）交叉引用
- dsh-plugin-doctor 未核实，不纳入

## P2 范围预估

- 核心来源 5-8 个：官方 index/config/cordis-01/cordis-05/architecture + 3 篇 vault 笔记 + example-plugin 源码
- 产出：逐步命令链 + 最小骨架 + 改造映射 + 坑清单 + 验证对照表（结合意图文件"每步有命令+预期输出+出错排查"）
