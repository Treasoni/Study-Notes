# uv 的常用命令 - 意图文件

## 基本信息

- **主题**: uv 的常用命令
- **项目标识**: uv-common-commands
- **创建时间**: 2026-09-05
- **当前阶段**: 阶段 0
- **输出目标**: obsidian
- **Vault 路径**: D:\Study-Notes
- **笔记目录**: python/
- **MOC 路径**: python/Python MOC.md

## 学习目标

### 笔记类型
常用命令速查手册（按场景分组的命令清单 + 最小示例，定位日常快速检索）

### 学习深度
上手（覆盖日常 80% 场景：init/add/remove/run/sync/venv/python/tool/tree 等）

### 用户基础
有了解（已发布过「uv 配置虚拟环境」笔记，知道 uv 与 pip/venv 的关系）

## 研究计划

### 探索方向
1. uv 官方 CLI 命令全景：按子命令族梳理（project / python / tool / cache / publish）
2. 常用场景命令组合：新建项目、增删依赖、跑脚本、切换 Python 版本、进入 .venv
3. 与 pip/venv/conda/poetry 的对照与迁移命令
4. 进阶与周边：uvx、uv tool、cache 清理、镜像源配置、CI 中的常用命令

### 重点收集
- **核心概念**: uv 命令模型（uv run 为统一入口）、pyproject.toml + uv.lock、.venv、uv tool/uvx 与全局工具安装
- **实战代码**: 每条常用命令的最小示例，以及高频命令组合
- **常见坑**: 虚拟环境是否需手动 activate、Python 版本选择、镜像源、与系统 Python / pip 混用
- **工具链**: uvx、ruff、pre-commit、GitHub Actions 中安装与使用 uv

### 信源偏好
- 官方文档: 是
- 技术博客: 是
- 社区讨论: 是
- 学术论文: 否

## 备注

- 与既有笔记「python/如何用uv配置Python虚拟环境.md」（run_id: uv-python-virtualenv）区分定位：本篇是**速查手册**，按命令/场景组织；既有笔记是**虚拟环境配置实战**。避免整段重复，交叉引用即可。
- 已确认发布策略：写入 vault `python/` 目录，并更新 `python/Python MOC.md`（追加一条索引，不复制正文）。
