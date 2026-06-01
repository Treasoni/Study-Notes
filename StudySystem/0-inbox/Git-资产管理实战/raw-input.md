# Git 与资产管理实战笔记

> 原始用户输入，来自用户直接分享的内容

---

## 📂 一、资产划分清单（传什么？不传什么？）

在工作流推送到 GitHub 时，核心原则是：共享逻辑与结构规约，隐藏凭证与本地状态。

### 1. 绝对不要推送（写入 .gitignore）
- **敏感凭证**：`.env`（包含 OpenAI/Anthropic API Key、Comet 凭证、OpenSec 密钥）。
- **工具缓存**：`.claude/` 文件夹（包含本地会话历史与缓存）。
- **自带插件/Skills**：`.claude/skills/` 中由 Superpowers 或 OpenSec 官方自带的、通过插件市场安装的标准 Skills（避免仓库臃肿及版本冲突）。
- **语言依赖/日志**：`__pycache__/`、`node_modules/`、`*.log`。

### 2. 必须推送（项目的核心资产）
- **核心代码**：你的主工作流逻辑脚本、`docker-compose.yml` 等。
- **配置模板**：`.env.example`（擦除真实密钥后的空载荷模板）。
- **AI 规约资产**：
  - `docs/` 目录：Superpowers 产出的设计、规划文档（spec.md、plan.md）。
  - `openspec/` 目录：OpenSec 的业务变更提案与任务单（proposals/、tasks.md）。
  - 注：这些文件是 AI 的"灵魂"，必须上传，以便多设备同步时 Claude 能立刻找回上下文。

---

## 💻 二、核心配置文件模板

### 1. `.gitignore` 推荐配置

```plaintext
# 敏感凭证与本地环境
.env
*.pem
*.key

# Claude Code 运行缓存与本地插件实体
.claude/

# 编程语言标准忽略
__pycache__/
*.pyc
.pytest_cache/
node_modules/

# 操作系统与日志
.DS_Store
*.log
```

### 2. `.env.example` 模板配置

```ini
# Comet & OpenSec 凭证配置
COMET_API_KEY=your_comet_api_key_here
OPENSEC_TOKEN=your_opensec_token_here

# LLM API 配置
CLAUDE_API_KEY=your_claude_api_key_here

# 第三方 Skills 路径（若有本地自定义模板）
SKILLS_DIR=./skills
```

---

## 🔄 三、多设备跨平台分布式开发 SOP

### 1. 在 A 设备（当前设备）暂存进度

不要因为代码没写完就不提交，利用 dev 分支高频上传作为云端备份。

```powershell
# 切换并确保在 dev 分支
git checkout -b dev 2>/dev/null || git checkout dev

# 暂存所有改动（包括代码、docs、openspec 等规约文件）
git add .

# 提交并打上 wip (Work In Progress) 标记
git commit -m "wip: 暂存当前开发进度，准备更换设备"

# 推送到 GitHub 远程仓库
git push origin dev
```

### 2. 在 B 设备（新设备/虚拟机）恢复现场

**Step 1: 刷新并同步远程分支**

新设备第一次直接 checkout dev 会报错 `pathspec 'dev' did not match...`，必须先抓取远程状态：

```powershell
# 1. 刷新远程分支列表
git fetch origin

# 2. 切换并追踪远程的 dev 分支
git checkout dev
# 若仍报错，使用强关联命令：git checkout -b dev origin/dev
```

**Step 2: 恢复本地特定环境**

```powershell
# 1. 复制模板生成本地 .env
cp .env.example .env

# 2. 【手动打开 .env】填入 B 设备对应的 API Key 与本地路径

# 3. 对齐依赖（根据项目语言执行 pip install 或 npm install）
```

**Step 3: 给新设备上的 Claude"搜魂"**

由于 `.claude/` 缓存未同步，在新设备上首次启动 Claude Code 时，直接对它输入以下 Prompt 重构上下文：

> 💡 **上下文唤醒词：**
> "我更换了开发设备。请阅读项目根目录下 docs/ 和 openspec/ 文件夹中的最新设计、规划与任务文件（如 spec.md, plan.md, tasks.md），帮我接续上一步的开发进度。"

---

## 🏁 四、开发完毕：代码合并与清理 SOP

### 方式一：本地命令行合并（效率最高）

```powershell
# 1. 确保 dev 分支代码全部提交并推送
git checkout dev
git add .
git commit -m "chore: 完成所有功能开发与测试"
git push origin dev

# 2. 切换到主分支并同步
git checkout main
git pull origin main

# 3. 将 dev 分支合并入 main
git merge dev

# 4. 推送最新的稳定版主分支到 GitHub
git push origin main
```

### 方式二：GitHub Pull Request 合并（最规范）

1. 将最新的 `dev` 分支 `git push origin dev` 到 GitHub。
2. 登录 GitHub 网页端，点击 "Compare & pull request"。
3. 检查方向：`base: main` ← `compare: dev`。
4. 确认无冲突后，点击 "Merge pull request" → "Confirm merge"。
5. 回到本地同步主分支：`git checkout main` → `git pull origin main`。

### 🧹 善后：清理过期分支

合并完成后，可以删除功成身退的 dev 分支以保持干净：

```powershell
git branch -d dev               # 删除本地 dev 分支
git push origin --delete dev    # 删除 GitHub 远程 dev 分支
```
