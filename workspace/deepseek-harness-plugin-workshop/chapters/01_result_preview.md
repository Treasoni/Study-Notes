## 1. 先看结果——你要做出什么

读完理论分册、环境也跑通了，可让你亲手写一个插件还是不知道从哪下手？本分册就是补这个缺口：不从头搭骨架，而是把现成的 `example-plugin`（repo_status）**改造成你自己的工具**，照着走就能跑通 **写 → 配 → 验证 → 打包 → 安装** 全链路[^S7]。整条链路最后交付两样东西：**① 一个新工具 `git_log`**——用 `defineTool` 声明，会出现在 Web UI 里、模型随时能调用[^S8]；**② 一个可安装的 bundle**——打包好的插件包，装进 profile 就能复用[^S5][^S9]。

> [!tip] 大白话
> 改造脚手架 = 领一套带精装修的模板房：不用从地基砌砖，先住进去，再按自己的喜好改客厅。所以别怕「不会写插件」——你不是从零盖房，只是改精装房。

> [!note] 这在 Claude Code 里相当于
> 本节要交付的 `git_log`，约等于你在 Claude Code 里声明一个自定义 tool（name + description + parameters），让 agent 能调用；「模型在 Web UI 里调用它」约等于「Claude Code 里 agent 调用你的自定义工具」。

### 你要走完的 8 步（先混个眼熟，细节后面每节拆开）

```bash
# ① 前提：源码环境已就绪（clone → pnpm install → pnpm run build），在 dsh 仓库根目录
#    —— 这一步得到：一个能跑 dsh 的本地源码仓库

# ② 拷贝脚手架：把 example-plugin 复制成「你自己的插件目录」
cp -r "<vault>/AI学习/DeepSeek-Harness 教程/example-plugin" ./example-plugin
#    —— 这一步得到：一份可以随便改、不碰原件的插件骨架

# ③ 改 dev-cordis.yml 的 name 为指向 src/index.ts 的绝对路径
#    —— 这一步得到：开发期 patch 指向你的入口（相对路径会静默失效，后面细讲）

# ④ 启动加载：确认插件被框架接住
pnpm dsh web --patch ./example-plugin/dev-cordis.yml
#    —— 预期输出：[repo-status-plugin] plugin loaded!

# ⑤ 验证配置层：确认 patch 真的合进了合成配置
pnpm dsh --profile web --patch ./example-plugin/dev-cordis.yml --dump-config
#    —— 预期输出：合成配置里出现 repo-status 行

# ⑥ 浏览器开 http://127.0.0.1:3080 新建会话，让模型调用 repo_status
#    —— 这一步得到：一个「模型能调用的工具」真的出现在 Web UI 里

# ⑦ 打包：装依赖 + 编译，产出可安装产物
cd example-plugin && pnpm install && pnpm run build
#    —— 这一步得到：dist/（bundle 的料理包本体）

# ⑧ 装进 profile：本地目录安装并验证
dsh plugin --profile demo add ./example-plugin
dsh --profile demo --dump-config
#    —— 预期输出：出现 "# == dsh-repo-status-plugin" 层
```

改造完成后，模型在 Web UI 里调用 `git_log` 的样子大致如下——`execute` 跑 `git log --oneline -n <max>`，`render` 把结果转成模型能读的文本：

```text
# 模型调用 git_log（参数 max=5）后，模型看到的输出：
最近 5 条提交：
db5f25c vault backup: 2026-08-15 18:17:40
99aa24a vault backup: 2026-08-15 18:16:37
d02e904 vault backup: 2026-08-15 18:15:13
c0da45b vault backup: 2026-08-15 18:11:16
4ced37b vault backup: 2026-08-15 18:08:53
```

接下来的每一节，就是把这 8 步**逐个拆开**，每步给你「可复现命令 + 预期输出 + 出错排查」——终点长什么样你已经看到了，现在从第 2 步（拷贝脚手架）开始动手。

## 注释

[^S5]: 官方 [docs/architecture.md](https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/architecture.md)（official，2026-08-15）——bundle / profile 分层概念。
[^S7]: 本地 vault `AI学习/DeepSeek-Harness 教程/example-plugin/*`（vault-note，2026-08-15）——实战基底：README / package.json / tsconfig / src/index.ts / src/tools/repo-status.ts / dev-cordis.yml / cordis.patch.yml。
[^S8]: 本地 vault `DeepSeek-Harness 插件开发核心.md`（第 3 章，vault-note，2026-08-15）——apply / 生命周期 / 依赖 / defineTool / 工具契约。
[^S9]: 本地 vault `DeepSeek-Harness 配置体系.md`（vault-note，2026-08-15）——补丁树 / Profile vs Agent Preset / Config schema / bundle vs profile。
