## 7. 小结与下一步——换成你自己的工具

8 步走完，`example-plugin` 已被你改造成 `git_log`，写、配、验证、打包、安装整条 A→C 链路都亲手跑过[^S7]。收尾三件事：把全链路压成一张 checklist、记住三处最容易翻车的点、然后把它换成你自己的工具。

### A→C 全链路回顾

| 环节 | 做了什么 | 关键命令 / 文件 |
|---|---|---|
| ① 写 | 建 `src/tools/git-log.ts` 写 `defineTool`，改 `src/index.ts` 注册 | `defineTool`（name/description/parameters/output/execute）+ `ctx.tools.register` |
| ② 配 | Config schema 加可调参数，patch 里 `config:` 传值，不硬编码[^S2] | `dev-cordis.yml` / `cordis.patch.yml` |
| ③ 验证 | 加载成功 → 配置层注入 → 模型调用 → 端到端 | `pnpm dsh web --patch` → `--dump-config` → Web UI → `dsh --profile headless "..."` |
| ④ 打包 | 装依赖 + 编译出 dist/ | `cd example-plugin && pnpm install && pnpm run build` |
| ⑤ 安装 | 装进 profile，看到自己的配置层 | `dsh plugin --profile demo add ./example-plugin` → `--dump-config` 见 `# == dsh-...` |

### 自查清单（改别人工具 / 重写前对着过一遍）

- **第 2 节｜绝对路径**：dev patch 的 `name` 必须是指向 `src/index.ts` 的**绝对路径**，相对路径静默失效。
- **第 3 节｜四处名字**：`export const name`（诊断）/ package.json `name`（包名）/ patch `id`（实例）/ defineTool `name`（模型可见），别混[^S7]。
- **第 6 节｜打包三件套**：`prepare` 脚本 + pnpm≥10 的 `allowBuilds` 放行 + git 安装用 `#<sha>` 钉 commit；bundle patch `name` == package.json `name`[^S11]。

### 下一步：换成你自己的工具

| 工具想法 | defineTool 要改哪 | execute 换成什么 | 要不要加配置项 |
|---|---|---|---|
| API 封装（天气 / 股票 / 汇率） | name + description + parameters | `fetch('https://api...')` + 解析结果 | 建议：endpoint、key 做成 config |
| 笔记检索（在 vault 里搜） | name + description + parameters | `rg` 扫 vault 目录 + 组装结果 | 建议：vault 路径做成 config |
| 目录统计（各目录文件数） | name + description + parameters | `find <dir> -type f` + 汇总 | 可选：目录路径做成 config |
| 构建脚本（跑测试 / 编译） | name + description + parameters | `pnpm run build` / `tsc` | 视情况：目标路径做成 config |

任何「agent 能帮你做、但需要执行外部命令/查数据」的事，都能包成 dsh 工具[^S7]——改 `defineTool` 的 name/description/parameters 告诉模型它是什么、要什么参数，再换 `execute` 里的命令/调用。

> [!tip] 大白话
> 改造脚手架 = 拿到模板房钥匙后，自己决定每间房用来做什么。`git_log` 是改好的第一间；下一个工具只是给 `execute` 摆上不同的家具，钥匙（A→C 链路）已经在你手里。

> [!note] 这在 Claude Code 里相当于
> 「换成你自己的工具」≈ 在 Claude Code 里持续往工具包里加自定义 tool / MCP——一样是「一次声明（name + description + parameters）、到处调用」，攒多了就是你的工具箱。

## 本章小结

本分册没让你从零盖房：改造 `example-plugin` 脚手架走通了写 → 配 → 验证 → 打包 → 安装。核心就四招——四处名字别混、可调值进 Config schema 不硬编码、`--dump-config` 切层排查、打包靠 `prepare` + `allowBuilds` + `#<sha>`。第 4 章教你插件怎么从零长出来，本分册教你拿到现成的怎么快速改成自己的，两章合起来，从看懂到亲手交付就齐了。挑一个上表里的想法（或你自己的），照第三节到第六节再来一遍，就正式出师。本分册产出已同步系列 README 与 MOC。

## 注释

[^S2]: 官方 [docs/user/develop/basic/config.md「插件配置」](https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/user/develop/basic/config.md)（official，2026-08-15）——Config+Schemastery 模式、默认值、cordis.yml config、坏配置响亮失败、HMR。

[^S7]: 本地 vault `AI学习/DeepSeek-Harness 教程/example-plugin/*`（vault-note，2026-08-15）——实战基底：README / package.json / tsconfig / src/index.ts / src/tools/repo-status.ts / dev-cordis.yml / cordis.patch.yml。

[^S11]: 本地 vault `DeepSeek-Harness 常见坑与速查.md`（第 5 章，vault-note，2026-08-15）——分环节坑清单、dsh plugin 命令族、工具契约。
