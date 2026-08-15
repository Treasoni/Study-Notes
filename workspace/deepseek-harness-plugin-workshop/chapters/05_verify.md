## 5. 验证——加载、看配置层、让模型真正调用

前三节把脚手架的 `repo_status` 改造成了 `git_log`，第四节又把 `maxCommits` 接进了配置层——但「改了」不等于「能跑」。本节用「验证四连」逐层确认：插件被框架接住、配置层真的注入、模型能真正调用、headless 端到端生效；每连都给命令 + 预期输出 + 它证明了什么，最后附一张排查表。以下命令都在 dsh 源码仓库根目录执行（开发期不用 `npx @deepseek-ai/dsh`）。[^S1]

### 5.1 验证第一连：插件被框架接住

```bash
# dev-cordis.yml 的 name 已指向改造后的 src/index.ts（绝对路径）
pnpm dsh web --patch ./example-plugin/dev-cordis.yml
```

预期输出：

```
[git-log-plugin] plugin loaded!
```

**这一验证证明什么**：入口注册成功——`apply(ctx)` 被执行，加载消息与诊断名 `git-log-plugin` 一致；若看到 `repo-status-plugin`，说明加载的还是未改造的旧配置。[^S1][^S7]

### 5.2 验证第二连：配置层真的注入

```bash
pnpm dsh --profile web --patch ./example-plugin/dev-cordis.yml --dump-config
```

预期输出（节选）：

```yaml
# 合成配置中出现 git-log 层
git-log:
  maxCommits: 5
```

**这一验证证明什么**：patch 生效、Config 读到——`config:` 传的值进入了合成配置，`maxCommits` 落到实例上，没有被静默丢弃。[^S7][^S9]

> [!tip] 大白话
> 把 `--dump-config` 想成**切开千层饼看每一层**：默认配置、profile、patch 各自摊开一层摆在眼前，哪一层放了什么一眼看清。所以「patch 到底生效没有」不用猜，切一刀就知道。

> [!note] 这在 Claude Code 里相当于
> `--dump-config` ≈ Claude Code 里展开 `--settings` 看生效配置 + 检查插件是否注册。都是先看清楚运行时真正拿到的配置，再动手调试。

### 5.3 验证第三连：模型能真正调用

浏览器开 `http://127.0.0.1:3080` → 新建会话 → 让模型调用 `git_log`（可提示它「看看最近的提交」）→ 模型返回最近 N 条提交。

预期输出（模型回复，示意）：

```
最近的提交：
- a1b2c3d feat: 新增 git_log 工具
- d4e5f6a fix: 修正 repo_status 的参数名
- ...
```

**这一验证证明什么**：工具对模型可见、可执行、结果回传——defineTool 的 name/description 被模型读到，execute 被真正执行，返回被带回对话。[^S1]

### 5.4 验证第四连：端到端真实生效

```bash
dsh --profile headless "最近 5 条提交是什么？"
```

预期输出：

```
（模型调用 git_log 后作答，示意）
最近的 5 条提交是：a1b2c3d feat: 新增 git_log 工具 / d4e5f6a fix: 修正 repo_status 参数名 / ...
```

**这一验证证明什么**：不是只有 Web UI 才加载——headless 模式下插件同样被装配，工具在无界面会话里也能被调用并拿到结果。[^S11]

> [!tip] 大白话
> `--profile headless` 想成**不点页面、直接问一句看它答不答得上来**：Web UI 像有人陪着练，headless 是把陪练撤了直接开考——能答上来，才说明工具是「真会」而不是界面在兜底。

> [!note] 这在 Claude Code 里相当于
> headless 端到端 ≈ 在命令行直接让 agent 用工具完成任务（相当于 `claude -p "..."` 无交互模式）——验证「工具真的被模型执行并回传结果」，而不是只在界面上看得到。

### 5.5 错误排查表

验证失败先对号入座，不要盲目重来：

| 现象 | 可能原因 | 排查命令 / 动作 |
|---|---|---|
| `plugin loaded!` 一直不出现 | 拼写错 / patch `name` 不是绝对路径 | 先查 `src/index.ts` 路径与 `export const name` 拼写，再 `--dump-config` 看有没有 `git-log` 行 |
| 模型列表里没有 `git_log` | `inject` 的 tools 服务未就绪（PENDING 不加载） | 检查 `export const inject = ['tools']` 依赖声明 |
| `--patch` 配错但无报错 | dev patch `name` 是相对路径 / 写错（静默失败） | 确认 `dev-cordis.yml` 的 `name` 为绝对路径，对照第 2 节示例 [^S12] |
| 配置改了没生效 | 补丁树整行替换、不做深合并；HMR 热替换旧实例注册自动清理 | 重看第 4 节易错点：覆盖要重写所有需要的 key，改完确认 HMR 已重载 |
| 其他 | bundle 层错 vs 上层覆盖错 | `dsh --profile <name> --dump-default-config` 分层定位 |

---

## 注释

[^S1]: [官方 docs/user/develop/basic/index.md「第一个插件」](https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/user/develop/basic/index.md)（raw 镜像抓取） | official | 2026-08-15 | 首插件五步、绝对路径要求、`plugin loaded!` 预期输出、inject+tools.register

[^S7]: 本地 vault `AI学习/DeepSeek-Harness 教程/example-plugin/*` | vault-note | 2026-08-15 | 实战基底：README / package.json / tsconfig / src/index.ts / src/tools/repo-status.ts / cordis.patch.yml / dev-cordis.yml

[^S9]: 本地 vault `DeepSeek-Harness 配置体系.md` | vault-note | 2026-08-15 | 补丁树 / Profile vs Agent Preset / Config schema / bundle vs profile

[^S11]: 本地 vault `DeepSeek-Harness 常见坑与速查.md`（第 5 章） | vault-note | 2026-08-15 | 分环节坑清单、dsh plugin 命令族、工具契约

[^S12]: [pingfanfan/hello-dsh](https://github.com/pingfanfan/hello-dsh) | community | 2026-08-15 | 零基础中文实例、checkpoint、--patch 静默失败实测坑（对照参考）
