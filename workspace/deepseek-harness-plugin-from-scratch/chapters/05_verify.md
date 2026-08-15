## 第 5 章：第 4 步——验证命令链

写到这里，`git_log` 工具和 `maxCommits` 配置都「写出来了」，但**写出来不等于跑通了**。这一章用 dsh 自带的四条验证命令，把三件事分别验清楚：插件有没有被加载、配置最终落在哪一层、端到端能不能用。这是全篇最值得真机完整跑一遍的部分——后面第 6 步打包、安装出了问题，都要回到这几条命令来定位。

### 5.1 `pnpm dsh web --patch ./dev-cordis.patch.yml` 复跑：确认 `[git-log-plugin] plugin loaded!`

从第 2 章到第 4 章，`src/index.ts` 里已经注册了 `git_log` 工具、加了 `maxCommits` 配置，`dev-cordis.patch.yml` 里也补上了对应的 `config` 块。加载命令和之前完全一样，仍然在 **dsh 源码仓库根目录**执行（开发期不用 npx；命令根目录、绝对路径这些坑清单见 [[DeepSeek-Harness 常见坑与速查]]）[^S11]：

```bash
pnpm dsh web --patch ./dev-cordis.patch.yml
```

启动后终端应再次看到插件自身的加载日志：

```text
[git-log-plugin] plugin loaded!
```

注意：这条日志是 `src/index.ts` 里 `console.log` 打出来的，不是 dsh 框架/CLI 的功能（第 2 章校准过）。`dsh web` 是 `--profile web` 的硬编码别名，方便本地起一个带 Web UI 的开发实例[^S8]。看到日志只说明「模块被加载了」，工具和配置到底对不对，要靠下面三条命令。

### 5.2 `dsh --profile demo --dump-config`：分层打印（bundle 各层 → profile patch → home 级 → `--patch` 叠加）

dsh 的配置不是单个文件，而是**四层补丁树**叠出来的：bundle 各层（按列表序）→ profile patch → home 级 → `--patch` 叠加，后层对前层做整行替换、不做字段级深合并[^S8]。想知道某条配置最终从哪一层来、合并成什么样，用 `--dump-config` 看全量：

```bash
# --dump-config 打印全量分层；加 --patch 把开发期补丁作为最顶层叠进来
# （不加的话，还在开发中的 git-log 层看不到）
dsh --profile demo --dump-config --patch ./dev-cordis.patch.yml
```

输出按层打印，每层都带来源文件注释，大致长这样（示意，实际输出以你的环境为准）：

```yaml
# from bundle 层（列表序，最低）
# from <harness-home>/profiles/demo/cordis.patch.yml   ← profile patch 层
# from <harness-home>/cordis.yml                        ← home 级
# from ./dev-cordis.patch.yml                          ← --patch 叠加（最顶层）
- insert:
    id: git-log
    name: <绝对路径>/src/index.ts
    config:
      maxCommits: 5
```

逐层核对下来，你能看到 `git-log` 这条来自 `--patch` 层、`maxCommits` 最终等于 5。四层补丁树的完整心智模型见 [[DeepSeek-Harness 配置体系]]。

> [!tip] 大白话
> 把 `--dump-config` 想成「验房验收单」——每层配置像每道工序（水电、木工、油漆），验收单按施工顺序一层层打勾，最后这张单子就是房子的最终状态。所以它能直接告诉你：`git-log` 是哪个文件贡献的、`maxCommits` 最终等于几。

### 5.3 `dsh --profile demo --dump-default-config`：只看 bundle 层（不含 profile/home/patch）

这条和 5.2 一字之差，含义**相反**。`--dump-default-config` 只看 bundle 层，不含 profile patch、home 级，也不含 `--patch` 叠加[^S8]：

```bash
dsh --profile demo --dump-default-config
```

它回答的是「各 bundle 作者默认贡献了什么配置」，与用户侧任何定制无关。开发期你的 `dev-cordis.patch.yml` 还没打进 bundle，所以这条命令里看不到 `git-log` 是**正常的**；等第 6 章工程化、把补丁打进包之后，再跑它就能核对「我这个包到底声明了哪一层配置」。

> [!warning] 别搞反
> `--dump-config` = 全层（含 profile / home / `--patch`）；`--dump-default-config` = 只看 bundle 层。两个命令只差一个词，用途完全不同。

> [!note] 这在 Claude Code 里相当于
> `--dump-config` / `--dump-default-config` 类似 `claude config list` 这类「看合并后配置」的调试手段——排查「我改的配置到底生效没有」时，先看合并结果，而不是凭感觉猜。

### 5.4 `dsh --profile headless "<task>"`：一次性任务端到端，stdout 打印文本，退出码 **0 = completed / 1 = otherwise**；无任务文本 = usage 错误

前三条验「加载」和「配置」，这条验「端到端能不能用」。headless 模式直接执行一个一次性任务，结果文本打印到 stdout：

```bash
dsh --profile headless "用 git_log 工具查看当前仓库最近的 5 次提交"
echo $?
# 0  ← 上一条命令的退出码
```

成败只看退出码[^S8]：

| 退出码 | 含义 |
| --- | --- |
| 0 | completed（任务完成） |
| 1 | otherwise（失败 / 异常 / usage 错误） |

headless 也是 dsh 自动初始化 profile 的入口之一（缺 profile 时按模板建），所以就算 `demo` profile 还没手动建过，这一条也能直接跑通[^S8]。**关键坑：无任务文本是 usage 错误**，不是「正常返回」：

```bash
dsh --profile headless
# usage 错误：缺少任务文本，退出码为 1（otherwise）
```

> [!tip] 大白话
> headless 的退出码 0/1 像验收时盖的章——0 是「验收合格」，1 是「不合格」。脚本里可以直接 `if dsh --profile headless "任务"; then ...` 当布尔判断用，放进 CI 或批处理都很顺手。

> [!note] 这在 Claude Code 里相当于
> headless 的 0/1 退出码约定，和所有 CLI 命令一致——脚本判断成功失败看退出码，而不是去解析 stdout 文本。

### 5.5 读 dump 输出的要点：文件名注释、`!!js` 不求值、stderr 报未命中

真跑起来之后，读 dump 输出记住三个要点[^S8]：

1. **文件名注释**：每层输出前都有 `# from ...` 注释标明来源文件，「这条配置谁定义的」靠它定位。
2. **`!!js` 不求值**：dump 是诊断视图，遇到 `!!js` 这类 YAML 标签会**原样打印、不求值**；它只在 dsh 真正加载配置、执行对应代码时才有意义，别把 dump 里的原样标签当成运行时值。
3. **未命中走 stderr**：查找某条配置/条目未命中时，dsh 把提示打到 **stderr** 而不是 stdout。排查时别只盯 stdout——把 `2>&1` 或终端报错区一起看了才完整。

把四条命令串起来，就是这张验证速查表：

| 要验证什么 | 用哪条命令 |
| --- | --- |
| 插件被加载 | `pnpm dsh web --patch ./dev-cordis.patch.yml` |
| 配置合并成什么样 | `dsh --profile demo --dump-config --patch ./dev-cordis.patch.yml` |
| bundle 默认贡献了什么 | `dsh --profile demo --dump-default-config` |
| 端到端能不能用 | `dsh --profile headless "<task>"` |

### 本章小结

- 四条验证命令分工明确：`dsh web --patch` 验「加载」，`--dump-config` 验「配置落在哪一层」，`--dump-default-config` 验「bundle 默认贡献」，headless 验「端到端」。
- `--dump-config` 是全层（bundle → profile → home → `--patch`），`--dump-default-config` 只看 bundle 层——别搞反。
- headless 退出码 0 = completed、1 = otherwise；无任务文本是 usage 错误，不是正常返回。
- dump 输出带文件名注释、`!!js` 不求值、未命中配置走 stderr。
- 命令统一在 dsh 源码仓库根目录执行，开发期不用 npx。

验证通过，插件在开发态就「能用」了。但它现在还依赖源码仓库和绝对路径，不是一个正经可分发的东西——下一章我们把插件工程化补齐（package.json + tsconfig + build 产出 `dist/`），为第 6 步打包安装铺路。

[^S8]: O8，官方 `apps/cli/reference/README.md`——dsh CLI 全家族与验证命令精确语法。
[^S11]: V2，《DeepSeek-Harness 插件实战》——一致性基线；开发期验证命令统一在 dsh 源码仓库根目录执行。
