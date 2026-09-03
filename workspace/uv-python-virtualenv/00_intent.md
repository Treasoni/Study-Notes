# 如何用uv配置python虚拟环境 - 意图文件

## 基本信息

- **主题**: 如何用uv配置python虚拟环境
- **项目标识**: uv-python-virtualenv
- **创建时间**: 2026-09-03
- **当前阶段**: 阶段 0
- **输出目标**: obsidian（当前 Vault）
- **Vault 路径**: D:\Study-Notes
- **笔记目录**: `python/`（待确认）
- **MOC 路径**: `python/Python MOC.md`（待确认，若无 Python MOC 则新建）

## 学习目标

### 笔记类型
概念 + 实战结合

### 学习深度
上手实操：能完整走通「安装 uv → 创建/激活虚拟环境 → 安装管理依赖 → 日常使用」，并理解核心概念

### 用户基础
有了解（用过 pip/venv 或 conda，想换用 uv）

## 研究计划

### 探索方向
1. uv 是什么：定位、与 venv/pip/poetry/conda 的关系，为什么值得用
2. 核心实操：安装 uv、指定 Python 版本、创建虚拟环境、激活/停用（含 Windows/macOS/Linux）
3. 日常管理与进阶：依赖安装（pyproject.toml vs requirements.txt）、`uv add`/`uv sync`/`uv run`、环境迁移、IDE 接入、常见坑

### 重点收集
- **核心概念**: virtual environment 原理；uv 的 Python 版本管理；pyproject.toml 与 uv.lock；`uv venv` vs `uv init` vs `python -m venv`
- **实战代码**: 安装命令（curl/pipx/brew）；`uv venv`、`uv init`、`uv add <pkg>`、`uv sync`、`uv run`、`uv python install/pin`、激活命令（Windows CMD/PowerShell、bash/zsh/fish）；`uv python list`
- **常见坑**: Windows 激活与执行策略、PATH/命令找不到、uv 自动发现虚拟环境逻辑、镜像源/代理、缓存目录（UV_CACHE_DIR）、与 conda 并存时的选择
- **工具链**: uv（Astral）、VS Code/PyCharm 解释器选择、ruff、pre-commit、GitHub Actions `astral-sh/setup-uv`

### 信源偏好
- 官方文档: 是（astral.sh/uv 文档优先）
- 技术博客: 是
- 社区讨论: 否
- 学术论文: 否

## 备注

- 用户已确认直接发布到当前 Vault；具体 note_folder（建议 `python/`）与 MOC（建议新建 `python/Python MOC.md`）需在阶段 0 确认点与用户最终确认。
- 平台差异（Windows 为主，兼顾 macOS/Linux）应在实战步骤中标注。
- 输出为 Obsidian Markdown，遵循 `.claude/rules/obsidian/note-system.md`。
