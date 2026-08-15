## 第 8 章：小结与下一步

前面 7 章从空目录一步步把插件「写 → 配 → 验证 → 打包 → 装」走通，这一章没有新代码、没有新命令，只做一次完整复盘：收拢全文件增量、命令链和下一步方向——卡在哪一步，就翻回哪一章。

### 8.1 全文件清单回顾：从 2 文件到完整工程的每一次增量

整条路线只有 6 次增量，手写文件从 2 个长到 6 个，构建后再产出 `dist/`，终点共 8 个文件：

| 阶段 | 章节 | 新增/修改 | 文件 |
| --- | --- | --- | --- |
| ① 最小跑通 | 第 2 章 | 新增 2 个 | `src/index.ts` + `dev-cordis.patch.yml` |
| ② 加工具 | 第 3 章 | 新增 1 个 | `src/tools/git-log.ts`；`src/index.ts` 升级为注册中心 |
| ③ 加配置 | 第 4 章 | 不新增 | `src/index.ts` 加 `Config` schema；两份 patch 加 `config` 块 |
| ④ 验证 | 第 5 章 | 不新增 | 四条验证命令 |
| ⑤ 工程化 | 第 6 章 | 新增 3 个 | `package.json` + `tsconfig.json` + `cordis.patch.yml`；build 产出 `dist/` |
| ⑥ 打包安装 | 第 7 章 | 不新增 | `pnpm pack` → `dsh plugin add` |

起点是最小 2 文件骨架 [^S1]。第 ⑤ 步定型双 patch：`dev-cordis.patch.yml`（开发期绝对路径）与 `cordis.patch.yml`（bundle，`name = dsh-git-log-plugin`）。文件归属沿用 [[DeepSeek-Harness 插件开发核心]]：工具进 `src/tools/`，`src/index.ts` 做注册中心。

### 8.2 一条命令链串起来：`dsh web --patch` → `--dump-config` → headless → `pnpm pack` → `dsh plugin add`

从开发到交付，五条命令按顺序就是整条流水线：

| 顺序 | 命令 | 作用 | 章节 |
| --- | --- | --- | --- |
| 1 | `pnpm dsh web --patch ./dev-cordis.patch.yml` | 开发期加载，看 `[git-log-plugin] plugin loaded!` | 第 2 章 |
| 2 | `dsh --profile demo --dump-config` | 分层打印合并后配置 | 第 5 章 |
| 3 | `dsh --profile headless "<task>"` | 一次性任务端到端（退出码 0/1） | 第 5 章 |
| 4 | `pnpm pack` | 打成 tarball | 第 7 章 |
| 5 | `dsh plugin --profile demo add <tarball>` | 装进 profile 并对账 | 第 7 章 |

前三条在 dsh 源码仓库根目录执行，后两条在插件工程里执行；打包安装机制来自官方 bundle/profile 文档 [^S3]。

### 8.3 下一步：更多工具 / 配置实战 / 发布到 npm registry / 官方模板 `dsh-plugin-*`

按「补全当前插件 → 走向真实发布」排四个方向：

1. **更多工具**：按第 3 章 defineTool 五件套继续加，一个插件可注册多个工具。
2. **配置实战**：按第 4 章扩展 Schema 类型，把参数做成可配，对照 [[DeepSeek-Harness 配置实战]]。
3. **发布到 npm registry**：第 7 章只演示 `pnpm pack`，改走 `npm publish`，任何 profile 即可 `dsh plugin add dsh-git-log-plugin` 安装。
4. **官方模板 `dsh-plugin-*`**：现在回头看脚手架能读懂每个文件为何存在——从零练理解，模板提速度，与 [[DeepSeek-Harness 插件实战]] 对照读。

> [!tip] 大白话
> 把全篇压成一张「从零到装好」的路线图：先 2 个文件把插件点亮（第 2 章），再长出手脚（工具）、装上旋钮（配置）、验过合格（第 5 章）、搭好流水线（第 6 章）、装箱送货（第 7 章）。卡在哪一步，就翻回哪一章——8.1 的表格就是索引。

> [!note] 这在 Claude Code 里相当于
> 一篇插件的「从模板 starter 到 npm 发布」完整 SOP 回顾：入口初始化（apply）→ 注册工具 → 配置校验（schema）→ 本地验证 → 工程化打包 → 发布安装，每一步都有 Claude Code 插件开发现实可对照。

唯一要回翻的坑：忘了「四名分离」或「bundle patch name = 包名」就翻第 6、7 章——前者管名字，后者管装进去能不能激活。

## 本章小结

- 从零到装好共 6 次增量，手写文件 2 → 6 个，加 `dist/` 产物共 8 个文件。
- 一条命令链覆盖开发到交付：`web --patch` → `--dump-config` → headless → `pnpm pack` → `dsh plugin add`。
- 四名分离（`git-log-plugin` / `dsh-git-log-plugin` / `git-log` / `git_log`）与「bundle patch name = 包名」是唯一要回翻的坑。
- 下一步四条路：更多工具、配置实战、npm 发布、官方模板 `dsh-plugin-*`。
- 至此你能脱离脚手架，从空目录独立造出带 `git_log` 工具与 `maxCommits` 配置的 dsh 插件。

[^S1]: O1 — `docs/user/develop/basic/index.zh.md`（Your first plugin）｜官方文档｜层级 5：最小 2 文件骨架与加载命令。
[^S3]: O3 — `docs/user/develop/basic/publish.md`（bundle/profile/发布/安装/git 坑）｜官方文档｜层级 5。
