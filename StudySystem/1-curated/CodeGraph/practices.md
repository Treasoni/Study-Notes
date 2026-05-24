# CodeGraph 实战示例

## 安装与初始化

### 安装方式一：curl 一键安装（推荐）

```bash
# macOS / Linux
curl -fsSL https://raw.githubusercontent.com/colbymchenry/codegraph/main/install.sh | sh

# Windows (PowerShell)
irm https://raw.githubusercontent.com/colbymchenry/codegraph/main/install.ps1 | iex
```

> CodeGraph 自带运行时，无需 Node.js 环境

### 安装方式二：npm 安装

```bash
npx @colbymchenry/codegraph        # 零安装运行
npm i -g @colbymchenry/codegraph   # 全局安装
```

### 初始化项目

```bash
cd your-project
codegraph init -i
```

## 交互式安装器

运行 `npx @colbymchenry/codegraph` 会：
1. 自动检测已安装的 Agent（Claude Code、Cursor、Codex CLI、opencode、Hermes Agent）
2. 询问安装位置（全局/项目本地）
3. 写入 MCP 服务器配置和指令文件
4. 为 Claude Code 设置自动允许权限
5. 初始化当前项目（本地安装时）

### 非交互式安装（CI/脚本）

```bash
# 自动检测 agent，全局安装
codegraph install --yes

# 指定 agent 列表
codegraph install --target=cursor,claude --yes

# 检测 agent，项目本地安装
codegraph install --target=auto --location=local

# 打印配置但不写入文件
codegraph install --print-config codex
```

## CLI 命令参考

| 命令 | 说明 |
|------|------|
| `codegraph` | 运行交互式安装器 |
| `codegraph install` | 运行安装器（显式） |
| `codegraph uninstall` | 移除所有 agent 的配置 |
| `codegraph init [path]` | 初始化项目（加 `--index` 同时索引） |
| `codegraph uninit [path]` | 移除项目本地索引 |
| `codegraph index [path]` | 完整索引（加 `--force` 重新索引） |
| `codegraph sync [path]` | 增量更新 |
| `codegraph status [path]` | 查看索引状态 |
| `codegraph query <search>` | 搜索符号 |
| `codegraph files [path]` | 显示文件结构 |

### 符号查询命令

| 命令 | 说明 |
|------|------|
| `codegraph callers <symbol>` | 查找调用者 |
| `codegraph callees <symbol>` | 查找被调用者 |
| `codegraph impact <symbol>` | 分析影响范围 |
| `codegraph context <task>` | 为 AI 任务构建上下文 |

### 代码影响分析

```bash
# 查找受变更影响的测试文件
codegraph affected src/utils.ts src/api.ts

# 从 git diff 获取变更文件
git diff --name-only | codegraph affected --stdin

# 自定义测试文件模式
codegraph affected src/auth.ts --filter "e2e/*"

# CI/hook 集成示例
#!/usr/bin/env bash
AFFECTED=$(git diff --name-only HEAD | codegraph affected --stdin --quiet)
if [ -n "$AFFECTED" ]; then
  npx vitest run $AFFECTED
fi
```

## MCP 工具集

当作为 MCP 服务器运行时，CodeGraph 暴露以下工具：

| 工具 | 用途 |
|------|------|
| `codegraph_search` | 按名称搜索符号 |
| `codegraph_context` | 为任务构建代码上下文 |
| `codegraph_callers` | 查找函数调用者 |
| `codegraph_callees` | 查找函数被调用者 |
| `codegraph_impact` | 分析符号变更影响 |
| `codegraph_node` | 获取符号详情（可含源码） |
| `codegraph_explore` | 返回相关符号源码和关系图 |
| `codegraph_files` | 获取索引文件结构 |
| `codegraph_status` | 检查索引健康状态 |

## 手动配置 MCP

### 安装全局 npm 包

```bash
npm install -g @colbymchenry/codegraph
```

### 添加到 `~/.claude.json`

```json
{
  "mcpServers": {
    "codegraph": {
      "type": "stdio",
      "command": "codegraph",
      "args": ["serve", "--mcp"]
    }
  }
}
```

### 添加权限到 `~/.claude/settings.json`

```json
{
  "permissions": {
    "allow": [
      "mcp__codegraph__codegraph_search",
      "mcp__codegraph__codegraph_context",
      "mcp__codegraph__codegraph_callers",
      "mcp__codegraph__codegraph_callees",
      "mcp__codegraph__codegraph_impact",
      "mcp__codegraph__codegraph_node",
      "mcp__codegraph__codegraph_status",
      "mcp__codegraph__codegraph_files"
    ]
  }
}
```

## 卸载

```bash
# 移除所有 agent 的配置
codegraph uninstall

# 移除项目本地索引
codegraph uninit

# 指定移除特定 agent
codegraph uninstall --target=cursor,claude --yes

# 非交互式卸载
codegraph uninstall --yes
```

## 数据来源

- [GitHub 官方仓库 - Get Started](https://github.com/colbymchenry/codegraph#get-started)
- [GitHub 官方仓库 - CLI Reference](https://github.com/colbymchenry/codegraph#cli-reference)
- [GitHub 官方仓库 - MCP Tools](https://github.com/colbymchenry/codegraph#mcp-tools)
