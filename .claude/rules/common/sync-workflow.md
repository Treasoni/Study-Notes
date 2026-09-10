# Agent 配置同步工作流

本项目以 `.agent-sync/` 作为跨 runtime 配置同步的唯一入口。canonical 源与生成目标由 `.agent-sync/agents/*.yaml` 的 profile 定义；不再维护独立的单向同步脚本。

## When To Sync

修改以下内容后必须运行同步：

- `.agent-sync/agents/*.yaml`（profile 映射本身）
- 任一区域 canonical source：skills / rules / hooks / scripts / workflows / agents / instructions（目录与文件见 `.agent-sync/agents/codex.yaml` 的 `paths`）
- canonical 目录下的新增、删除、重命名或实质修改
- instructions canonical（`paths.instructions`）中改变了工作流、skill 路由或规则路径

## Command

先以只读模式检查差异：

```bash
python3 .agent-sync/sync_agents.py --root . --check --scope <area>
```

`<area>` 取值：`skills` / `rules` / `hooks` / `scripts` / `workflows` / `agents` / `mcp`。

确认差异符合预期后应用：

```bash
python3 .agent-sync/sync_agents.py --root . --apply --scope <area>
```

同步后必须验证镜像没有漂移（全量 check）：

```bash
python3 .agent-sync/sync_agents.py --root . --check
```

## What It Does

1. 读取 canonical profile（`.agent-sync/agents/codex.yaml`，`canonical: true`）与 target profile（`.agent-sync/agents/claude.yaml`）的 `paths` 映射。
2. 把 canonical 源复制到 target 的 `paths` 目录，并对文本做路径替换（source `paths` → target `paths`）与 runtime 名替换（source `name` → target `name`）。
3. 保留 target 专属文件（如 target 专属 hooks 文档、`skill-creator`），不被 canonical 镜像覆盖。
4. `rules` 区域同步时还会同步 instructions 文件（`paths.instructions`），生成 target 的入口文档。
5. `agents` 区域同步 subagent 定义；canonical 是 `.claude/agents/`。两个 profile 都必须在 `paths` 中声明 `agents`，且 canonical 侧在 `canonical_scopes` 中包含 `agents`——否则 `load_profiles` 直接报错。

比较按**行尾不敏感**进行：`--check` 只把真实内容差异算作漂移，仅 CRLF/LF 不同视为已同步，`--apply` 也不会为行尾重写文件。（`rendered_bytes` 经 `read_text` 会把 CRLF 折成 LF，若按原始字节比较，CRLF 工作区会永久误报。）

`--check` 只报告差异，不修改任何文件；有差异时退出码为 1，用于 pre-commit / CI。

## Boundary

- 各区域 canonical / target 的目录映射以 `.agent-sync/agents/*.yaml` 的 `paths` 为准，本文件不重复列出具体路径，避免与 profile 漂移。
- `.agent-sync/bootstrap.py` 负责生成当前机器的 hook 注册文件（见 profile `paths.hook_config`），并注册到 target 的 settings。
- 生成目标目录是同步产物，不手工编辑；如需修改，先改 canonical 再同步。
