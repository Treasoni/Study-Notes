---
title: "DeepSeek-Harness 配置专册 · 配置体系——补丁树、Profile 与 bundle"
tags: [deepseek-harness, ai, agent, 配置, 教程]
created: 2026-08-13
updated: 2026-08-15
status: updated
source_project: deepseek-harness
---

# DeepSeek-Harness 配置专册 · 配置体系——补丁树、Profile 与 bundle

> [!summary] 本章导读
> 这是 [[DeepSeek-Harness 插件开发核心|插件开发核心]] 的配套专册。dsh **没有「一份完整配置文件」**——配置是**多层 YAML 补丁**按顺序叠加的结果。本册讲清四件事：① 补丁树怎么叠加（1）；② 两级配置 Profile 与 Agent Preset（2）；③ 插件怎么声明并接收配置（3）；④ 打包发布时 bundle 与 profile 各管什么（4）。

## 1. 配置心智模型：多层 YAML 补丁树

插件不是放进某个目录就生效，而是通过 **YAML 补丁树**装配。dsh 的配置在**空根**上按顺序叠加补丁[^1]：

1. **bundle 补丁**：profile manifest 中 `dsh.profile.bundles` 列表命名的每个 bundle 补丁；
2. **profile 自身 `cordis.patch.yml`**；
3. **home 级 `$DSH_HOME/cordis.patch.yml`**（机器级偏好，所有 profile 共享）；
4. **`--patch <path>` 覆盖层**（按 argv 顺序）。

```mermaid
flowchart TD
    ROOT["空白配置（空根）"] --> L1["第①层 bundle 补丁<br/>profile.bundles 命名的每个包"]
    L1 --> L2["第②层 profile 自身 cordis.patch.yml"]
    L2 --> L3["第③层 home 级 $DSH_HOME/cordis.patch.yml<br/>机器级偏好"]
    L3 --> L4["第④层 --patch 覆盖层<br/>按 argv 顺序"]
    L4 --> FINAL["最终配置<br/>--dump-config 摊开看"]

    classDef root fill:#f5f5f5,stroke:#9e9e9e
    classDef patch fill:#e3f2fd,stroke:#1976d2
    classDef final fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px

    class ROOT root
    class L1,L2,L3,L4 patch
    class FINAL final
```

补丁语义：**"Later layers win per row"**——后层按行覆盖，**替换目标行的完整 config 值，不做深合并**，可插入新行。

> [!tip] 大白话
> 把补丁树想成一层层铺在桌上的透明纸。后铺的纸会盖住先铺的同一位置，但不会去改下面那层的其他内容——「整行替换，不做深合并」。

### 四层补丁：在哪、谁写的、管多宽

| 层                               | 文件在哪                                       | 谁写的  | 管多宽                           |
| ------------------------------- | ------------------------------------------ | ---- | ----------------------------- |
| ① bundle 补丁                     | 每个插件包内部自带一份（包声明 `dsh.bundle.patch` 指向它）    | 插件作者 | 这个包贡献的配置；profile 点名几个包就按顺序叠几份 |
| ② profile 自身 `cordis.patch.yml` | `$DSH_HOME/profiles/<名字>/cordis.patch.yml` | 你/本地 | 只对这个 profile 生效               |
| ③ home 级 `cordis.patch.yml`     | `$DSH_HOME/cordis.patch.yml`               | 你/机器 | 这台机器所有 profile 共享             |
| ④ `--patch <path>`              | 命令行临时指定的任意文件                               | 命令行  | 只影响这一次运行，优先级最高                |

> [!example] 数字走一遍
> 假设 profile `web` 点名装 `base`、`web-app` 两个包，各层都写了插件 `hello`：
>
> | 层 | 给 hello 设置的 |
> |---|---|
> | ① base 包补丁 | `greeting: 'Hello'`、`maxRetries: 3` |
> | ① web-app 包补丁 | `greeting: 'Hi'`、`maxRetries: 5` |
> | ② profile 自己的 patch | `greeting: 'Hi'`、`maxRetries: 4` |
> | ③ home 级 patch | `greeting: 'Hi'`、`maxRetries: 6` |
> | ④ `--patch` | `greeting: 'Yo'`、`maxRetries: 6` |
>
> 同一字段越晚越赢：`greeting` 被第 ④ 层压成 `'Yo'`，`maxRetries` 被第 ③/④ 层压成 `6`。只被某一层写过的插件保持那一层的值；后层也可以插入全新插件行。

> [!warning] 按行替换，不做深合并
> 补丁不是 Git 式的字段深合并：后层写**同一行**（同一插件 id）时，是拿这行的内容**整体替换**目标行，而不是逐字段拼接。拿不准某层盖出了什么，用 `--dump-config` 摊开看合成结果。

### 检查合成配置（排查利器）

```bash
pnpm dsh --profile web --dump-default-config          # 只看 bundle 层
pnpm dsh --profile web --patch ./extra.yml --dump-config  # 含 profile/home 补丁与 --patch 覆盖层
```

## 2. 两级配置：Profile 与 Agent Preset

两个正交的维度（不是同一个东西的两个名字）：

- **Profile（进程级）**：决定装哪些 bundle。`web`（base + web-app）与 `headless`（base + headless）首次使用自动从模板初始化；其他缺失 profile 需 `dsh plugin --profile <name> add <package>`[^1]。
- **Agent Preset（会话级）**：决定工具/提示词/skill/子代理。内置 4 个预设：`minimal` / `standard` / `code` / `cordis`。作用域解析：`agent → preset → global`[^1]。

| | Profile | Agent Preset |
|---|---|---|
| 级别 | 进程级 | 会话级 |
| 决定 | 装**哪些 bundle**、什么顺序 | 会话里用**哪些工具/提示词/skill/子代理** |
| 类比 Claude Code | 启用哪些插件 + 核心配置 | 某个子代理 / agent 类型的配置 |

其中 `minimal` 固定系统提示 "You are a helpful software engineer assistant."，只组合 `bash` + `str_replace_editor` 两个工具。

> [!tip] 大白话
> Profile 和 Agent Preset 不是「同一个东西的两个名字」，而是**两条独立的轴**。**Profile 像「你电脑上装了哪些 App」**——决定这次启动能干什么；**Agent Preset 像「你叫的是哪个角色的员工」**——决定他手上有哪些工具、按什么人设干活。装了什么 ≠ 用了什么，两条都要设。

## 3. 插件如何接收配置：Config schema

插件可接受 `cordis.yml` 传入的配置。导出同名 `Config` 接口 + **Schemastery** schema（不能用普通对象），默认值写在 schema 上[^1][^2]：

```ts
import Schema from '@deepseek-ai/schemastery'

export interface Config {
  greeting: string
  maxRetries: number
}
export const Config: Schema<Config> = Schema.object({
  greeting: Schema.string().default('Hello'),
  maxRetries: Schema.number().default(3),
})

export function apply(ctx: Context, config: Config) {
  console.log(config.greeting)   // 用户值或 schema 默认值
}
```

在 `cordis.yml` 里配：

```yaml
- insert:
    - id: hello
      name: './src/my-plugin.ts'
      config:
        greeting: 'Hi there'
        maxRetries: 5
```

- **原则**：两个部署可能想设不同的值，就做成配置字段（测试：`cordis.yml` 能否不改代码改值）[^1]；
- **失效即响亮失败**：无效配置让 fiber 进 FAILED，报错精确；
- **HMR**：配置编辑热替换插件，旧实例注册自动清理，不残留。

> [!tip] 大白话
> 插件像一个**新入职的员工**，`Config` schema 就是他的**岗位说明书**：上面写清楚有哪些字段、每格填什么类型、不填时用什么默认值。用说明书而不是随便一张纸，是因为说明书能做「入职审核」——填错了当场打回（响亮失败），不会糊弄过去。改完配置不用重启进程，原地换血（HMR 热替换）。

## 4. 打包与发布：bundle 与 profile

开发期用 `--patch` 加载本地插件；要给别人用时打包成 **bundle**（npm 包）[^3]。

两个概念（都由 `package.json` 描述，但 manifest 不同）：

- **bundle**：携带配置层的 npm 包，声明 `dsh.bundle.patch`——回答「这个包贡献什么」；
- **profile**：`$DSH_HOME/profiles/<name>` 目录，声明 `dsh.profile.bundles` 有序列表——回答「装哪些 bundle、什么顺序」。你从不手写 profile，`dsh plugin` 自动维护。

最小 bundle：

```json
{
  "name": "dsh-hello-plugin",
  "version": "0.1.0",
  "type": "module",
  "main": "index.js",
  "files": ["index.js", "cordis.patch.yml"],
  "dsh": { "bundle": { "patch": "./cordis.patch.yml" } }
}
```

```yaml
# cordis.patch.yml（插件行按包名引用，不用相对路径）
- insert:
    - id: hello
      name: dsh-hello-plugin
```

安装进 profile：

```bash
dsh plugin --profile demo add ./hello-plugin     # 转发 pnpm，自动追加 bundle
dsh --profile demo --dump-config                  # 验证层
dsh --profile demo
```

> [!warning] git 安装的 build 坑
> `dsh plugin add github:you/hello-plugin` 拉的是**源码不是构建产物**。作者必须提供 `prepare` 脚本（pnpm 在 git 安装后运行），用户还需在 profile 的 `pnpm-workspace.yaml` 里 `allowBuilds` 放行——这等于「授权在安装时执行该包的代码」，只放行你信任的包，并 `#<sha>` 钉住 commit[^3]。

> [!tip] 大白话
> **bundle 是「料理包」**——每个 npm 包自己声明「我贡献哪一层配置」；**profile 是「上菜顺序单」**——决定按什么顺序装哪些料理包，这单子不用你手写，`dsh plugin` 命令自动维护。git 安装那个坑再补一句：`allowBuilds` 放行 = 你亲手递给这个包一张「在我机器上跑代码」的门禁卡，只发给信任的包，还要用 `#<sha>` 把版本钉死。

---

## 本章小结

> [!summary]
> - dsh 没有「一份完整配置」，配置是**多层 YAML 补丁树**（bundle → profile → home → `--patch`）在空根上叠加的结果，后层整行替换、不做深合并；`--dump-config` 可摊开看最终配置；
> - **Profile（进程级）管装哪些 bundle；Agent Preset（会话级）管会话用什么能力**（minimal / standard / code / cordis）；
> - 插件接受配置：`Config` 接口 + Schemastery schema，默认值写 schema 上，坏配置响亮失败，HMR 热替换；
> - 发布：**bundle 贡献配置层**（`dsh.bundle.patch`）vs **profile 决定装哪些 bundle 及顺序**（`dsh.profile.bundles`）；`dsh plugin add` 安装，git 安装注意 prepare + allowBuilds。

相关：[[DeepSeek-Harness 插件开发核心|第 3 章 插件开发核心]] → [[DeepSeek-Harness 与ClaudeCode对照迁移|实战：自定义工具插件]]。

---

## 更新记录

- 2026-08-15：从原《配置体系》（插件开发核心）中拆出配置专册，独立成篇；原 3.2（补丁树）/ 3.3（两级配置）/ 3.6（Config schema）/ 3.9（bundle 发布）整合为本册 1–4 节。

---

[^1]: 素材来源：DeepSeek Harness 官方文档「第一个插件 / 插件配置」（2026-08-15 收集）。
[^2]: 素材来源：官方 Cordis 教程 01–03/05（2026-08-15 收集）。
[^3]: 素材来源：官方「打包并安装插件」（2026-08-15 收集）。
