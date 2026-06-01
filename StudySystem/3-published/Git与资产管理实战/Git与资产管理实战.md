---
title: Git与资产管理实战
type: experience
difficulty: intermediate
tags:
  - Git
  - 资产管理
  - ClaudeCode
  - OpenSpec
  - 开发工作流
  - 多设备协作
  - SOP
created: 2026-06-02
updated: 2026-06-02
concepts:
  - Git资产分类
  - 多设备同步
  - AI规约文档
  - WIP提交
aliases:
  - Git资产管理
  - 多设备Git同步
---

# Git 与资产管理实战

## 背景

> 什么项目、什么场景、遇到了什么问题

在使用 [[ClaudeCode防遗忘策略-笔记|Claude Code]] + [[Superpowers]]/OpenSpec 进行 AI 辅助开发时，项目资产种类繁杂——既有核心代码，又有 AI 对话的规约文档（docs/、openspec/）、工具缓存（.claude/）、敏感凭证（.env）等。如果一股脑全部提交到 Git，仓库会变得臃肿且不安全；但如果不提交 AI 规约资产，跨设备切换时 Claude 就失去了上下文，需要从头开始构建理解。

这套实践就是在这样的场景下沉淀出来的：一套 Git 资产管理的清晰规范，解决 ==**"传什么、不传什么"**== 和 ==**"多设备怎么同步"**== 的问题。 #Git #资产管理 #AI辅助开发

[来源: 个人经验]

---

## 过程

> 怎么做的、尝试了什么、结果如何

整个实践经历了四个阶段的逐步梳理，从资产分类到多设备 SOP，再到最终的合并清理。 [来源: 个人经验]

---

### 一、资产划分清单：传什么？不传什么？

核心原则是：==**共享逻辑与结构规约，隐藏凭证与本地状态。**==

**绝对不要推送的内容（写入 .gitignore）：**

- **敏感凭证**：`.env` 文件（包含 OpenAI/Anthropic API Key、Comet 凭证、OpenSpec 密钥等）
- **工具缓存**：`.claude/` 文件夹（包含本地会话历史与缓存，每台设备独立）
- **自带插件/Skills**：`.claude/skills/` 中由 [[Superpowers]] 或 OpenSpec 官方自带的、通过插件市场安装的标准 Skills——这些不应入库，避免仓库臃肿及版本冲突
- **语言依赖/日志**：`__pycache__/`、`node_modules/`、`*.log`

**必须推送的核心资产：**

- **核心代码**：主工作流逻辑脚本、`docker-compose.yml` 等运行主体
- **配置模板**：`.env.example`（擦除真实密钥后的空载荷模板）
- **AI 规约资产**：
  - `docs/` 目录：Superpowers 产出的设计、规划文档（spec.md、plan.md）
  - `openspec/` 目录：OpenSpec 的业务变更提案与任务单（proposals/、tasks.md）
  - 这些文件是 AI 的 ==**"灵魂"**==，必须上传，以便多设备同步时 Claude 能立刻找回上下文

---

### 二、多设备跨平台分布式开发 SOP

这是实践中迭代最多的部分。核心场景：在 A 设备上开发到一半，需要切换到 B 设备继续。

#### Step A —— 在 A 设备暂存进度

不要因为代码没写完就不提交。利用 dev 分支高频上传，把它当作云端备份。 #Git #WIP提交

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

#### Step B —— 在 B 设备恢复现场

新设备第一次直接 `checkout dev` 会报错 `pathspec 'dev' did not match...`，必须先抓取远程状态： #Git #多设备同步

```powershell
# 1. 刷新远程分支列表
git fetch origin

# 2. 切换并追踪远程的 dev 分支
git checkout dev
# 若仍报错，使用强关联命令：git checkout -b dev origin/dev
```

然后恢复本地特定环境：

```powershell
# 1. 复制模板生成本地 .env
cp .env.example .env

# 2. 【手动打开 .env】填入 B 设备对应的 API Key 与本地路径

# 3. 对齐依赖（根据项目语言执行 pip install 或 npm install）
```

> [!tip] 上下文唤醒 Prompt
> 最后，也是最关键的一步——**给新设备上的 Claude "搜魂"**。由于 `.claude/` 缓存未同步，在新设备上首次启动 Claude Code 时，直接输入以下 Prompt 重构上下文：
>
> **上下文唤醒词：**
> *"我更换了开发设备。请阅读项目根目录下 docs/ 和 openspec/ 文件夹中的最新设计、规划与任务文件（如 spec.md, plan.md, tasks.md），帮我接续上一步的开发进度。"*

---

### 三、开发完毕：代码合并与清理 SOP

实践过程中主要使用两种合并方式。 #Git #分支管理

#### 方式一：本地命令行合并（效率最高）

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

#### 方式二：GitHub Pull Request 合并（最规范）

1. 将最新的 `dev` 分支推送到 GitHub：`git push origin dev`
2. 登录 GitHub 网页端，点击 "Compare & pull request"
3. 检查方向：`base: main` ← `compare: dev`
4. 确认无冲突后，点击 "Merge pull request" → "Confirm merge"
5. 回到本地同步主分支：`git checkout main` → `git pull origin main`

#### 善后清理

合并完成后删除已功成身退的 dev 分支：

```powershell
git branch -d dev               # 删除本地 dev 分支
git push origin --delete dev    # 删除 GitHub 远程 dev 分支
```

---

## 心得

> 学到了什么、有什么感悟

这套流程跑通之后，有几个关键洞察值得记录下来。 #Git #经验总结 #AI辅助开发

[来源: 个人经验]

1. **AI 规约文档是跨设备同步的 ==灵魂==**——代码可以重写，但 AI 对项目背景、架构决策、当前进度的理解完全依赖 docs/ 和 openspec/ 中的规约文件。没有这些，换设备后 Claude 就是 ==**"失忆"**== 状态。这和传统 Git 资产管理有本质区别，是 AI 辅助开发独有的需求。

2. **WIP 提交是美德，不是羞耻**——传统开发中，不完整的代码提交往往被视为不专业。但在 AI 辅助开发的场景下，频繁的 dev 分支 push 首先是 ==**"云端备份"**==，其次才是版本管理。把 dev 分支当作同步介质而非代码里程碑，心态上会更轻松。

3. **".claude/ 不同步"是特性，不是 bug**——起初觉得缓存不同步很麻烦，后来意识到每个设备的本地上下文（会话历史、Agent 状态）天然应该是独立的。强制同步 .claude/ 反而可能引入跨设备的状态冲突。关键不是同步缓存，而是用规约文档做 ==**"上下文重建"**==。

4. **SOP 文档化比记忆可靠**——这套流程经历了多次 ==**"忘记步骤 → 翻聊天记录 → 重新整理"**== 的循环。最终写成文档后，每次换设备只需按清单执行，不再依赖大脑记忆。建议用 checkout list 而非 prose 描述步骤。

---

## 踩坑

> [!warning] 坑点：新设备 checkout dev 分支直接报错
> **现象**：在新设备上执行 `git checkout dev` 时，提示 `pathspec 'dev' did not match any file(s) known to git`。
> **原因**：新克隆的仓库本地不存在 dev 分支，Git 无法直接切换到远程分支。必须先 `git fetch origin` 拉取远程分支列表，然后建立本地追踪关系。
> **解决**：使用 `git fetch origin` 刷新远程分支，然后 `git checkout -b dev origin/dev` 建立本地追踪分支。 [来源: 个人经验]

> [!warning] 坑点：新设备上 Claude 对项目完全陌生
> **现象**：切换到新设备后启动 Claude Code，发现它对项目结构、当前任务一无所知，需要从零解释。
> **原因**：.claude/ 缓存（包含会话历史和 Agent 上下文）在 .gitignore 中，不会被同步到新设备。Claude 没有"记忆"可加载。
> **解决**：关键在于提前在仓库中维护好 docs/ 和 openspec/ 这两个 ==**"AI 大脑"**== 目录。换设备后执行上下文唤醒 Prompt，让 Claude 重新读取规约文档重建上下文。 [来源: 个人经验]

> [!warning] 坑点：容易遗漏 .env 配置导致调试失败
> **现象**：代码拉下来后直接运行报错，提示 API Key 未配置。
> **原因**：.env 文件在 .gitignore 中，新设备上没有自动生成。只拉了代码却忘了拉环境配置。
> **解决**：将 `cp .env.example .env` 作为换设备 SOP 的第二步强制执行。如果项目依赖多个环境变量，考虑在 README 中用表格列出每个变量的用途和获取方式。 [来源: 个人经验]

---

## 代码/示例

### `.gitignore` 完整配置

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

### `.env.example` 模板

```ini
# Comet & OpenSpec 凭证配置
COMET_API_KEY=your_comet_api_key_here
OPENSEC_TOKEN=your_opensec_token_here

# LLM API 配置
CLAUDE_API_KEY=your_claude_api_key_here

# 第三方 Skills 路径（若有本地自定义模板）
SKILLS_DIR=./skills
```

---

## 延伸

- 还想深入了解：如何将这套 SOP 进一步自动化，例如用 Git Hooks 在 commit 前自动校验 .env.example 是否和实际 .env 的变量名保持一致
- 下一步计划：梳理团队协作场景下的 Git 规范，包括多人共享 dev 分支时的冲突处理策略。参见 [[分支管理最佳实践]]
- 更多 Git 主题：[[Git MOC]]
- 相关笔记：[[ClaudeCode防遗忘策略-笔记]]

---

## 思考题

1. 假设你的队友在新设备上 clone 了仓库，但忘记执行 `cp .env.example .env`。你会如何设计一个机制自动检测并提醒他？
2. 在什么场景下，你会考虑把 `.claude/` 中的部分内容（例如自定义 skills）加入版本控制？这样做有什么风险？
3. 如果团队成员在 dev 分支上同时工作，推送前没有及时同步，导致 merge 时出现大量冲突。你的解决策略是什么？
4. 这套资产划分原则是否适用于其他 AI 辅助开发工具（如 Cursor、Copilot）？哪些部分需要调整？
