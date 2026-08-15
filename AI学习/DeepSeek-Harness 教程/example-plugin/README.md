# example-plugin · dsh 自定义工具插件脚手架

> 配套 [[../DeepSeek-Harness 与ClaudeCode对照迁移|第 4 章 实战]]的完整示例插件。效果：给 agent 加一个 `repo_status` 工具，返回当前仓库 git 状态摘要。
> 你的目标插件只需替换 `src/tools/repo-status.ts` 里的 `execute` 实现，其余结构（入口 / 配置 / 打包）不用动。

## 目录结构

```
example-plugin/
├── package.json          # dsh.bundle 发布清单（打包时用）
├── tsconfig.json
├── cordis.patch.yml      # 打包层 patch：按包名引用插件
├── dev-cordis.yml        # 开发层 patch：按绝对路径引用（开发时用）
└── src/
    ├── index.ts          # 插件入口：name + inject + apply(ctx, config)
    └── tools/
        └── repo-status.ts # defineTool：真正的工具实现
```

## 开发运行（源码路径）

前提：已完成第 2 章的源码构建（clone → `pnpm install` → `pnpm run build`），在 `deepseek-harness` 仓库根目录。

```bash
# 1. 把本目录拷到 dsh 仓库根（或任意位置，但 dev-cordis.yml 里的路径必须是绝对路径）
cp -r "<vault>/AI学习/DeepSeek-Harness 教程/example-plugin" ./example-plugin

# 2. 把 dev-cordis.yml 里的 name 改成你机器上的实际绝对路径

# 3. 启动，加载插件
pnpm dsh web --patch ./example-plugin/dev-cordis.yml
# 终端应打印 [repo-status-plugin] plugin loaded!

# 4. 打开 http://127.0.0.1:3080，新建会话让模型调用 repo_status
```

排查：`pnpm dsh --profile web --patch ./example-plugin/dev-cordis.yml --dump-config` 看合成配置里有没有 `repo-status` 行。

> [!warning] 开发期不要用 `npx @deepseek-ai/dsh`
> `--patch` 加载本地插件的开发循环必须在源码仓库上下文里跑（见第 2 章 2.1）。

## 打包发布（bundle）

给别人的时候打包成 npm bundle：

```bash
pnpm install            # 装 devDeps（typescript / @types/node / @deepseek-ai/*）
pnpm run build          # tsc 产出 dist/
dsh plugin --profile demo add ./example-plugin
dsh --profile demo --dump-config   # 应看到 "# == dsh-repo-status-plugin" 层
dsh --profile demo
```

- git 安装（`dsh plugin --profile demo add github:you/dsh-repo-status-plugin`）拉的是源码，靠 `prepare` 脚本构建；用户需在 profile 的 `pnpm-workspace.yaml` 里 `allowBuilds` 放行（详见 [[../DeepSeek-Harness 配置体系|配置体系]] / 第 4 章 4.6）。
- `@deepseek-ai/*` 三个包声明为 peerDependencies：宿主 dsh 安装已内置；若你的发布环境解析不到，把它们挪到 `dependencies` 即可。

## 换成你自己的工具

1. 在 `src/tools/` 新建 `my-tool.ts`，用 `defineTool` 描述 `name / description / parameters / output.{schema,render} / execute`；
2. `src/index.ts` 里 `ctx.tools.register(myTool(config))` 注册；
3. 想加权限门/审计，用 `tools/pre-execute` 等 hook 扩展点（第 3 章 3.5）；
4. 可调参数都做成 `Config` schema 字段（[[../DeepSeek-Harness 配置体系|配置体系]]），`dev-cordis.yml` 的 `config:` 传值。

## 关联笔记

- [[../DeepSeek-Harness 插件开发核心|第 3 章 插件开发核心]]
- [[../DeepSeek-Harness 配置体系|配置体系专册]]
- [[../DeepSeek-Harness 与ClaudeCode对照迁移|第 4 章 实战]]
- [[../DeepSeek-Harness 常见坑与速查|第 5 章 速查与排错]]
