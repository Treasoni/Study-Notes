## 4. 配——Config schema 加可调参数 + patch 传值

第 3 节写完了工具，本节给 `git_log` 加一个「可调旋钮」——提交数上限 `maxCommits`。

### 为什么做成配置项

「不硬编码可调值」：不同项目想看 5 条还是 50 条提交，不该改代码。判断标准一句话：**两个部署可能设不同值 → 做成配置字段**[^S2]。这样换项目只改配置、不改源码。

### Config schema 两步

在 `src/index.ts` 里分两步声明「这个插件要什么参数、默认多少」：

```ts
export interface Config {
  /** git log 默认显示的提交数上限 */
  maxCommits: number
}

export const Config: Schema<Config> = Schema.object({
  maxCommits: Schema.number().default(5),
})
```

- ① `interface Config` 声明字段与类型（`maxCommits: number`）；
- ② 导出**同名 `Config`** 的 Schemastery schema。两个要点：**必须**用 `Schema.object` 导出（普通 JS 对象缺 Standard Schema 接口，框架读不了你的参数契约[^S2]）；默认值用 `.default()` 写在 schema 上，用户没传时兜底为 5[^S2]。

### 两份 patch 传值

改好 schema，让两个部署环境把值传进来。`dev-cordis.yml` 与 `cordis.patch.yml` 各加一个 `config:` 块，并统一把 `id` 改成 `git-log`：

```yaml
# 开发层 patch：插件路径必须是【绝对路径】（dsh 要求，相对路径会失效）
- insert:
    - id: git-log
      name: '/absolute/path/to/example-plugin/src/index.ts'
      config:
        maxCommits: 5
```

```yaml
# 打包层 patch：插件行按包名引用（Node resolution 从 profile node_modules 找已安装代码）
- insert:
    - id: git-log
      name: dsh-git-log-plugin
      config:
        maxCommits: 5
```

两份 patch 长得像、角色不同[^S7]：**dev 层 `name` 用绝对路径指向源码**，改完立刻生效；**bundle 层用包名 `dsh-git-log-plugin` 指向已安装产物**，发布后别人装的是这份[^S7]。`id: git-log` 两边一致，它只是给插件实例起的诊断名（模型可见的工具名是第三节 `defineTool` 里的 `git_log`，两者可以不同）。

> [!tip] 大白话
> Config schema = **岗位说明书 / 入职登记表**：提前声明「这个插件要什么参数、默认多少」。`config:` 传值 = **入职时在表上填你想要的默认值**：同一张登记表，不同项目填 5 还是 50，随你。

> [!note] 这在 Claude Code 里相当于
> Schemastery schema ≈ Claude Code tool 的 `input_schema`——声明参数的类型、必填、默认；`.default(5)` ≈ `input_schema` 里的 `default`；配置校验失败 ≈ 工具参数校验失败时直接报错给你看。

### 易错点三连

- **Schemastery 没有 `.optional()`**：字段默认就是可选的，要必填得显式 `.required(true)`[^S11]。
- **补丁树整行替换、不做深合并**：想覆盖某一行，必须把这一行需要的 key 全写上，别指望框架帮你补齐[^S9]。
- **坏配置加载即响亮失败**：报 ValidationError / fiber FAILED，不会静默兜底[^S4]——写错立刻发现，是好事。

配置就绪。下一节用命令链验证「改得对不对」。

## 注释

[^S2]: [官方 docs/user/develop/basic/config.md「插件配置」](https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/user/develop/basic/config.md)（raw 镜像抓取）· official · 2026-08-15 · Config+Schemastery 模式、默认值、cordis.yml config、坏配置响亮失败、HMR

[^S4]: [官方 docs/cordis-tutorial/05-config.md](https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/cordis-tutorial/05-config.md) · official · 2026-08-15 · 坏配置→fiber FAILED / ValidationError

[^S7]: 本地 vault `AI学习/DeepSeek-Harness 教程/example-plugin/*` · vault-note · 2026-08-15 · 实战基底：README / package.json / tsconfig / src/index.ts / src/tools/repo-status.ts / cordis.patch.yml / dev-cordis.yml

[^S9]: 本地 vault `DeepSeek-Harness 配置体系.md` · vault-note · 2026-08-15 · 补丁树 / Profile vs Agent Preset / Config schema / bundle vs profile

[^S11]: 本地 vault `DeepSeek-Harness 常见坑与速查.md`（第 5 章）· vault-note · 2026-08-15 · 分环节坑清单、dsh plugin 命令族、工具契约
