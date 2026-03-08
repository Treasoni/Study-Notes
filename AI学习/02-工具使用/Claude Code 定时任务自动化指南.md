---
tags: [claude-code, 自动化, 定时任务, launchd, hooks, 调度, macos, loop]
created: 2026-03-07
updated: 2026-03-08
---

> [!tip] 更新说明
> **🚀 重大更新（2026年3月）**：Claude Code 现已内置 **`/loop` 命令**，支持官方定时任务功能！任务可运行最长 **3 天**，使用 cron 风格调度。详见 [[#10-官方方案-loop-命令推荐]]
>
> **macOS 用户注意**：对于需要长期运行或系统级的定时任务，仍推荐使用 **launchd**（详见 [[#6-macos-定时任务使用-launchd-替代-cron]]）

# Claude Code 定时任务自动化指南

> [!info] 概述
> **一句话定义**：通过结合操作系统级定时任务（macOS 使用 launchd，Linux 使用 Cron）和 Claude Code 的命令行能力，实现代码审查、依赖监控、自动重构等任务的定时自动化执行。
>
> **通俗比喻**：就像给 Claude Code 配了一个"智能闹钟"，每天固定时间自动醒来干活——晚上帮你检查代码、周末生成报告、周一早上推送分析结果。

## 核心概念

### 是什么

**Claude Code 定时任务自动化** 有两种实现方式：

| 方案 | 适用场景 | 特点 |
|------|----------|------|
| **`/loop` 命令**（官方推荐） | 会话内短期任务、代码监控、状态轮询 | 内置功能、最长运行 3 天、cron 风格调度 |
| **launchd/cron**（系统级） | 长期运行、跨会话、夜间批处理 | 系统原生、无时间限制、需手动配置 |

**核心能力**：
- **定时执行**：每天、每周、每月自动运行任务
- **无人值守**：夜间自动处理代码分析、备份等工作
- **持续改进**：定期代码审查、依赖更新检查

> [!important] macOS 用户注意
> **推荐使用 launchd 而非 cron**。Cron 在 Mac 上是"二等公民"，无法正确处理系统休眠状态：
> - 要么在不该启动时因 Power Nap 唤醒执行
> - 要么在睡眠期间直接错过任务
>
> **launchd 是苹果原生方案**，核心优势：如果任务计划执行时 Mac 正在休眠，它会在 Mac 醒来后**立即补执行**。详见 [[#6-macos-定时任务使用-launchd-替代-cron]]

### 为什么需要

| 问题 | 手动方式 | 自动化方式 |
|------|----------|------------|
| 代码审查 | 每次手动运行命令 | 每天早上自动执行并生成报告 |
| 依赖监控 | 定期手动检查 npm/pip | 自动检测安全漏洞并通知 |
| 报告生成 | 周末手动汇总 | 周一早上自动推送到邮箱 |
| 备份验证 | 手动执行备份脚本 | 每晚自动备份+分析变更 |

### 通俗理解

**🎯 比喻**：Claude Code + 定时调度器 就像一个"夜间值守的程序员"

```
[你的工作日]          [夜间的 Claude Code]
    ↓                      ↓
下班回家休息  →  自动检查代码质量
                      自动分析依赖安全
                      自动生成报告
                      第二天早上推送结果
```

**📦 示例**：每日代码审查自动化流程

```mermaid
graph LR
    A[launchd/Cron 定时触发<br>每天9:00] --> B[Shell 脚本]
    B --> C[Claude Code CLI]
    C --> D[分析项目代码]
    D --> E[生成审查报告]
    E --> F[发送通知/存储日志]
```

## 技术细节

### 1. 前置准备

> [!info] 📚 来源
> - [Claude Code + Cron Automation Complete Guide](https://smartscope.blog/en/generative-ai/claude/claude-code-cron-schedule-automation-complete-guide-2025/) - SmartScope
> - [launchd.info](https://www.launchd.info/) - launchd 完整教程

**环境检查**：
```bash
# macOS: 检查 launchd 是否正常（默认总是可用）
launchctl version

# Linux: 检查 Cron 是否可用
crontab -l

# 验证 Claude Code 安装
claude --version

# 创建工作目录
mkdir -p ~/claude-automation/{scripts,logs,config,reports}
cd ~/claude-automation
```

### 2. 基础定时脚本

**daily-code-review.sh**：
```bash
#!/bin/bash

# Claude Code 定时代理脚本
LOG_FILE="$HOME/claude-automation/logs/daily-$(date +%Y%m%d).log"
PROJECT_PATH="$HOME/projects/my-app"

echo "=== Claude Code Daily Review: $(date) ===" >> "$LOG_FILE"

cd "$PROJECT_PATH" || exit 1

# 执行代码审查
claude code . --prompt "检查项目整体代码质量，输出改进建议：
1. 代码规范问题
2. 潜在的安全风险
3. 性能优化建议
4. 测试覆盖率评估" \
  --output "$HOME/claude-automation/reports/review-$(date +%Y%m%d).md" \
  >> "$LOG_FILE" 2>&1

echo "=== Review Completed: $(date) ===" >> "$LOG_FILE"
```

### 3. 定时任务配置

#### macOS 用户：使用 launchd（推荐）

> [!info] 📚 来源
> - [Apple Developer - Creating Launch Daemons and Agents](https://developer.apple.com/library/archive/documentation/MacOSX/Conceptual/BPSystemStartup/Chapters/CreatingLaunchdJobs.html) - 官方文档
> - [launchd.plist(5) man page](https://www.manpagez.com/man/5/launchd.plist/) - 参数参考
> - [launchd.info](https://www.launchd.info/) - 完整教程

**第一步：停止现有的 Cron 任务（如果有）**

```bash
# 查看当前 cron 任务
crontab -l

# 编辑并注释掉相关任务
crontab -e
# 在行首添加 # 注释掉定时任务
```

**第二步：创建 Launchd 配置文件 (Plist)**

launchd 使用 `.plist` 文件定义任务，存放位置：
- **用户级任务**：`~/Library/LaunchAgents/`（推荐）
- **系统级任务**：`/Library/LaunchDaemons/`（需要 root）

```bash
# 创建用户级 LaunchAgent 配置
nano ~/Library/LaunchAgents/com.user.claude-daily-review.plist
```

**完整配置示例**：
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <!-- 任务唯一标识符（必填） -->
    <key>Label</key>
    <string>com.user.claude-daily-review</string>

    <!-- 要执行的程序及参数 -->
    <key>ProgramArguments</key>
    <array>
        <string>/bin/bash</string>
        <string>/Users/你的用户名/claude-automation/scripts/daily-code-review.sh</string>
    </array>

    <!-- 定时计划：每天凌晨 2:00 执行 -->
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>2</integer>
        <key>Minute</key>
        <integer>0</integer>
    </dict>

    <!-- 标准输出日志 -->
    <key>StandardOutPath</key>
    <string>/Users/你的用户名/claude-automation/logs/launchd-stdout.log</string>

    <!-- 错误日志 -->
    <key>StandardErrorPath</key>
    <string>/Users/你的用户名/claude-automation/logs/launchd-stderr.log</string>

    <!-- 防止子进程被终止 -->
    <key>AbandonProcessGroup</key>
    <true/>

    <!-- 设置环境变量 -->
    <key>EnvironmentVariables</key>
    <dict>
        <key>PATH</key>
        <string>/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin</string>
    </dict>
</dict>
</plist>
```

**关键参数说明**：

| 参数 | 说明 |
|------|------|
| `Label` | 唯一标识符，建议使用反向域名格式如 `com.user.taskname` |
| `ProgramArguments` | 要执行的命令，第一个是可执行文件路径，后续是参数 |
| `StartCalendarInterval` | 类似 cron 的时间调度，支持 `Hour`、`Minute`、`Day`、`Weekday`、`Month` |
| `StartInterval` | 间隔执行，如 `3600` 表示每 3600 秒执行一次 |
| `StandardOutPath` | 标准输出日志路径 |
| `StandardErrorPath` | 错误日志路径 |
| `AbandonProcessGroup` | 设为 `true` 防止 launchd 在任务结束后杀死子进程 |

**时间调度示例**：

```xml
<!-- 每天 9:00 执行 -->
<key>StartCalendarInterval</key>
<dict>
    <key>Hour</key>
    <integer>9</integer>
    <key>Minute</key>
    <integer>0</integer>
</dict>

<!-- 每周一 10:00 执行 -->
<key>StartCalendarInterval</key>
<dict>
    <key>Weekday</key>
    <integer>1</integer>
    <key>Hour</key>
    <integer>10</integer>
    <key>Minute</key>
    <integer>0</integer>
</dict>

<!-- 每月 1 号 8:00 执行 -->
<key>StartCalendarInterval</key>
<dict>
    <key>Day</key>
    <integer>1</integer>
    <key>Hour</key>
    <integer>8</integer>
    <key>Minute</key>
    <integer>0</integer>
</dict>

<!-- 每小时执行一次 -->
<key>StartInterval</key>
<integer>3600</integer>
```

> [!tip] 休眠补偿机制
> **launchd 的核心优势**：如果任务计划执行时 Mac 正在休眠，它会在 Mac 醒来后**立即补执行**。
>
> 例如：设置凌晨 2:00 执行，但你盖上了笔记本。当你早上 8:00 打开盖子时，launchd 会检测到错过了一次任务并立即补跑。
>
> *来源：官方文档 "Unlike cron which skips job invocations when the computer is asleep, launchd will start the job the next time the computer wakes up."*

**第三步：加载并激活任务**

```bash
# 加载任务（使其生效）
launchctl load ~/Library/LaunchAgents/com.user.claude-daily-review.plist

# 验证任务已加载
launchctl list | grep claude

# 立即测试执行（不等待定时）
launchctl start com.user.claude-daily-review

# 卸载任务
launchctl unload ~/Library/LaunchAgents/com.user.claude-daily-review.plist
```

**常用 launchctl 命令**：

| 命令 | 说明 |
|------|------|
| `launchctl load <plist>` | 加载任务 |
| `launchctl unload <plist>` | 卸载任务 |
| `launchctl start <label>` | 立即执行一次 |
| `launchctl stop <label>` | 停止运行中的任务 |
| `launchctl list` | 列出所有已加载任务 |
| `launchctl list | grep <label>` | 查找特定任务 |
| `launchctl print gui/$(id -u)/<label>` | 查看任务详情（macOS 10.10+） |

#### Linux 用户：使用 Cron

```bash
# 编辑 crontab
crontab -e

# 配置示例
# 每天 9:00 执行代码审查
0 9 * * * /home/user/claude-automation/scripts/daily-code-review.sh

# 每周一 10:00 执行全面扫描
0 10 * * 1 /home/user/claude-automation/scripts/weekly-scan.sh

# 每月 1 号 8:00 生成月度报告
0 8 1 * * /home/user/claude-automation/scripts/monthly-report.sh

# 每小时执行轻量检查
0 * * * * /home/user/claude-automation/scripts/hourly-check.sh
```

### 4. 实用自动化模式

> [!info] 📚 来源
> - [GitHub Issue #30649 - Scheduled/Cron Support](https://github.com/anthropics/claude-code/issues/30649) - 功能请求
> - [Scheduled Tasks: How to Put Claude on Autopilot](https://atalupadhyay.wordpress.com/2026/03/02/scheduled-tasks-how-to-put-claude-on-autopilot/) - 教程

#### 模式一：自动备份 + 代码分析

```bash
#!/bin/bash

BACKUP_DIR="$HOME/backups/$(date +%Y%m%d)"
PROJECT_DIR="$HOME/projects/webapp"
LOG_FILE="$HOME/claude-automation/logs/backup-$(date +%Y%m%d).log"

# 创建备份
mkdir -p "$BACKUP_DIR"
rsync -av "$PROJECT_DIR/" "$BACKUP_DIR/" >> "$LOG_FILE"

# 用 Claude Code 分析变更
cd "$PROJECT_DIR" || exit 1

claude code . --prompt "
分析自昨天的变更：
1. 新增功能概述
2. 潜在安全风险
3. 性能改进建议
4. 测试覆盖建议

用中文输出报告。" \
  --output "$HOME/claude-automation/reports/daily-analysis-$(date +%Y%m%d).md" \
  >> "$LOG_FILE" 2>&1
```

#### 模式二：依赖监控与更新

```bash
#!/bin/bash

PROJECT_DIR="$HOME/projects/webapp"
ALERT_WEBHOOK="https://hooks.slack.com/services/YOUR/WEBHOOK"

cd "$PROJECT_DIR" || exit 1

# 检查依赖安全性
ANALYSIS_RESULT=$(claude code . --prompt "
分析 package.json 中的依赖：
1. 有安全漏洞的包
2. 有重大更新的包
3. 已废弃的包
4. 推荐的安全更新列表

用 JSON 格式输出结果。" --format json)

# 高危漏洞告警
if echo "$ANALYSIS_RESULT" | jq -r '.security_issues[]' | grep -q "critical"; then
    curl -X POST -H 'Content-type: application/json' \
      --data '{"text":"🚨 检测到严重安全漏洞！"}' \
      "$ALERT_WEBHOOK"
fi

# 保存报告
echo "$ANALYSIS_RESULT" > "$HOME/claude-automation/reports/dependency-$(date +%Y%m%d).json"
```

#### 模式三：自动重构

```bash
#!/bin/bash

PROJECT_DIR="$HOME/projects/api-server"
BRANCH_NAME="auto-refactor-$(date +%Y%m%d)"

cd "$PROJECT_DIR" || exit 1

# 创建新分支
git checkout -b "$BRANCH_NAME"

# 执行重构
claude code . --prompt "
按以下标准重构代码：
1. 消除重复代码
2. 拆分过长函数（超过100行）
3. 改善变量命名
4. 添加必要注释
5. 优化 TypeScript 类型定义

输出变更文件列表和变更原因。" \
  --execute \
  --output "$HOME/claude-automation/reports/refactor-log-$(date +%Y%m%d).md"

# 如果有变更则提交
if git diff --quiet; then
    echo "无变更需要提交"
    git checkout main
    git branch -d "$BRANCH_NAME"
else
    git add .
    git commit -m "🤖 自动重构: $(date +%Y-%m-%d)

    Claude Code 自动重构：
    - 代码重复消除
    - 函数分解
    - 变量命名改进
    - 类型定义优化"

    git push origin "$BRANCH_NAME"

    # 创建 PR（使用 GitHub CLI）
    gh pr create --title "🤖 自动重构 $(date +%Y-%m-%d)" \
      --body "Claude Code + Cron 自动代码改进" \
      --base main --head "$BRANCH_NAME"
fi
```

### 5. 高级技巧

#### 条件执行

```bash
#!/bin/bash

PROJECT_DIR="$HOME/projects/webapp"
CONFIG_FILE="$HOME/claude-automation/config/settings.json"

# 读取上次处理的 commit
LAST_COMMIT=$(jq -r '.last_processed_commit' "$CONFIG_FILE")
CURRENT_COMMIT=$(cd "$PROJECT_DIR" && git rev-parse HEAD)

# 仅在有新提交时执行
if [ "$LAST_COMMIT" != "$CURRENT_COMMIT" ]; then
    echo "检测到新提交，开始分析..."

    cd "$PROJECT_DIR" || exit 1

    CHANGED_FILES=$(git diff --name-only "$LAST_COMMIT" HEAD)

    claude code . --prompt "
    以下文件发生变更：
    $CHANGED_FILES

    分析变更：
    1. 影响范围评估
    2. 需要的测试
    3. 部署前检查清单
    4. 潜在风险评估
    " --output "$HOME/claude-automation/reports/change-analysis-$(date +%Y%m%d-%H%M).md"

    # 更新配置
    jq --arg commit "$CURRENT_COMMIT" '.last_processed_commit = $commit' \
      "$CONFIG_FILE" > tmp.json && mv tmp.json "$CONFIG_FILE"
else
    echo "无新提交，跳过分析"
fi
```

#### 并行执行与锁机制

```bash
#!/bin/bash

LOCK_FILE="/tmp/claude-automation.lock"
MAX_PARALLEL=3

# 获取锁
exec 200>"$LOCK_FILE"
if ! flock -n 200; then
    echo "另一个实例正在运行，退出..."
    exit 1
fi

# 并行处理多个项目
PROJECTS=(
    "$HOME/projects/frontend"
    "$HOME/projects/backend"
    "$HOME/projects/mobile-app"
)

for project in "${PROJECTS[@]}"; do
    claude code "$project" --prompt "安全分析" \
      --output "$HOME/claude-automation/reports/security-$(basename "$project")-$(date +%Y%m%d).md" &

    # 限制并行数
    job_count=$(jobs -r | wc -l)
    if [ "$job_count" -ge $MAX_PARALLEL ]; then
        wait -n
    fi
done

wait
flock -u 200
```

### 6. macOS 定时任务：使用 launchd 替代 cron

> [!info] 📚 来源
> - [launchd.plist(5) - StartCalendarInterval](https://www.manpagez.com/man/5/launchd.plist/) - 官方 man page
> - [launchd.info - Scheduling](https://www.launchd.info/) - 教程

#### 为什么 Mac 上 cron 有问题？

**核心问题**：Mac 的休眠机制导致 cron 执行异常：

| 问题 | 表现 |
|------|------|
| Power Nap 唤醒 | Mac 在睡眠期间可能因 Power Nap 功能唤醒，导致 cron 在非预期时间执行 |
| 睡眠期间错过 | 如果 Mac 在计划执行时间处于睡眠状态，cron 会直接跳过该次执行 |
| 无补偿机制 | cron 不会在 Mac 唤醒后补执行错过的任务 |

**结论**：cron 在 macOS 上是"二等公民"，它无法处理系统的休眠和唤醒状态。

#### 为什么 launchd 是更好的选择？

**launchd** 是苹果专门为 macOS 设计的守护进程管理器，核心优势：

1. **休眠补偿**：如果任务计划执行时 Mac 正在休眠，它会在 Mac 醒来后立即补执行
2. **事件合并**：如果多次触发时间都在睡眠期间，唤醒后只执行一次（避免重复）
3. **原生集成**：与 macOS 深度集成，正确处理用户登录/注销、系统休眠/唤醒
4. **更丰富的触发条件**：支持路径监控、网络状态、挂载事件等

#### 迁移步骤：从 cron 到 launchd

**第一步：停止现有的 Cron 任务**

```bash
# 在终端输入
crontab -e

# 注释掉或删除那行定时任务（在行首添加 #）
# 0 9 * * * /home/user/scripts/daily-task.sh

# 保存并退出
```

**第二步：创建 Launchd 配置文件**

```bash
# 创建用户级任务配置
nano ~/Library/LaunchAgents/com.user.myscript.plist
```

粘贴以下内容（根据需求修改路径和时间）：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.user.myscript</string>
    <key>ProgramArguments</key>
    <array>
        <string>/bin/bash</string>
        <string>/Users/你的用户名/claude-automation/scripts/daily-code-review.sh</string>
    </array>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>2</integer>
        <key>Minute</key>
        <integer>0</integer>
    </dict>
    <key>AbandonProcessGroup</key>
    <true/>
</dict>
</plist>
```

**第三步：加载并激活任务**

```bash
# 加载任务
launchctl load ~/Library/LaunchAgents/com.user.myscript.plist

# 验证加载成功
launchctl list | grep myscript

# 立即测试执行
launchctl start com.user.myscript
```

#### Cron 与 launchd 对照表

| 需求 | Cron 语法 | launchd 配置 |
|------|-----------|-------------|
| 每天凌晨 2:00 | `0 2 * * *` | `StartCalendarInterval` + `Hour: 2, Minute: 0` |
| 每周一 10:00 | `0 10 * * 1` | `StartCalendarInterval` + `Weekday: 1, Hour: 10, Minute: 0` |
| 每月 1 号 8:00 | `0 8 1 * *` | `StartCalendarInterval` + `Day: 1, Hour: 8, Minute: 0` |
| 每小时 | `0 * * * *` | `StartInterval: 3600` |
| 每 5 分钟 | `*/5 * * * *` | 需要列出所有时间点或使用 `StartInterval: 300` |

### 7. 错误处理与通知

```bash
#!/bin/bash

set -euo pipefail

LOG_FILE="$HOME/claude-automation/logs/main-$(date +%Y%m%d).log"
ERROR_LOG="$HOME/claude-automation/logs/error-$(date +%Y%m%d).log"
WEBHOOK_URL="https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK"

# 错误处理器
error_handler() {
    local line_no=$1
    local error_code=$2

    echo "第 $line_no 行出错，退出码: $error_code" | tee -a "$ERROR_LOG"

    # Slack 通知
    curl -X POST -H 'Content-type: application/json' \
      --data "{\"text\":\"Claude Code 自动化失败：第 $line_no 行，错误码 $error_code\"}" \
      "$WEBHOOK_URL"

    exit "$error_code"
}

trap 'error_handler ${LINENO} $?' ERR

# 主流程
{
    echo "=== 开始执行: $(date) ==="

    # 执行各项检查
    # run_security_scan
    # run_performance_analysis
    # run_code_quality_check

    echo "=== 执行完成: $(date) ==="

    # 成功通知
    curl -X POST -H 'Content-type: application/json' \
      --data '{"text":"✅ Claude Code 自动化执行成功"}' \
      "$WEBHOOK_URL"

} 2>&1 | tee -a "$LOG_FILE"
```

### 8. Claude Code Hooks 集成

> [!info] 📚 来源
> - [Hooks reference - Claude Code Docs](https://code.claude.com/docs/en/hooks) - 官方文档
> - [Get started with Claude Code hooks](https://code.claude.com/docs/en/hooks-guide) - 入门指南
> - [Claude Code Hooks Complete Guide (February 2026)](https://smartscope.blog/en/generative-ai/claude/claude-code-hooks-guide/) - 最新教程

Claude Code 的 Hooks 功能可以在特定生命周期事件触发时执行自定义操作，与定时任务结合使用更强大。

> [!success] 2026 年更新
> Hooks 现已支持 **14 种生命周期事件**、**3 种处理器类型**和异步模式，成为完整的自动化平台。

**完整的 Hook 事件列表（2026年2月）**：

| 事件 | 触发时机 | 用途 |
|------|----------|------|
| `SessionStart` | 会话开始时 | 初始化环境、加载配置 |
| `PreToolUse` | 工具调用前 | 验证参数、阻止危险操作 |
| `PostToolUse` | 工具调用成功后 | 格式化文件、记录日志 |
| `PostToolUseFailure` | 工具调用失败后 | 错误通知、回滚操作 |
| `Stop` | 会话结束时 | 清理资源、发送报告 |
| `Notification` | 收到通知时 | 自定义通知处理 |
| `PreCompact` | 上下文压缩前 | 保存重要信息 |
| `PostCompact` | 上下文压缩后 | 恢复关键数据 |
| `SubAgentStart` | 子代理启动时 | 记录子任务 |
| `SubAgentStop` | 子代理结束时 | 汇总结果 |
| `UserInputRequest` | 请求用户输入时 | 自动填充、验证 |
| `ToolCall` | 任意工具调用时 | 通用拦截器 |
| `FileChange` | 文件变更时 | 自动格式化、测试触发 |
| `TaskComplete` | 任务完成时 | 通知、报告生成 |

**3 种处理器类型**：
1. **Command** - 执行 shell 命令
2. **Script** - 运行 Python/Node.js 脚本
3. **HTTP** - 发送 HTTP 请求（新增）

**配置示例** (`.claude/settings.json`)：
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "echo '任务完成: $(date)' >> $HOME/claude-automation/logs/hooks.log"
          }
        ]
      }
    ]
  }
}
```

### 9. 官方方案：/loop 命令（推荐）

> [!info] 📚 来源
> - [Run prompts on a schedule - Claude Code Docs](https://code.claude.com/docs/en/scheduled-tasks) - 官方文档
> - [Claude Code Scheduled Tasks: Complete Setup Guide (2026)](https://claudefa.st/blog/guide/development/scheduled-tasks) - 完整教程

> [!success] 🎉 原生支持
> Claude Code 现已内置 `/loop` 命令，无需再依赖外部调度工具即可实现定时任务！

#### 核心特性

| 特性 | 说明 |
|------|------|
| **最长运行时间** | 3 天（任务自动过期并删除） |
| **调度方式** | Cron 风格时间表达式 |
| **运行范围** | 会话级（会话结束后任务终止） |
| **后台执行** | 支持，可最小化窗口 |

#### 基本语法

```bash
# 基本用法
/loop <cron表达式> <任务描述>

# 示例
/loop "0 9 * * *" "检查所有 PR 状态，测试通过后自动合并"
/loop "*/30 * * * *" "每 30 分钟检查服务健康状态"
/loop "0 0 * * 1" "每周一早上生成周报"
```

#### 实用示例

**示例一：PR 自动监控与合并**
```
/loop "0 */2 * * *" "
检查我所有待处理的 PR：
1. 查看测试状态
2. 检查代码审查进度
3. 如果测试通过且有人 approve，自动合并
4. 发送汇总通知
"
```

**示例二：服务健康检查**
```
/loop "*/15 * * * *" "
每 15 分钟检查：
- API 响应时间
- 错误日志
- 资源使用情况

如果发现异常，记录到 /logs/health-alerts.md
"
```

**示例三：每日代码质量报告**
```
/loop "0 8 * * *" "
每天早上 8 点：
1. 分析昨天的代码提交
2. 检查测试覆盖率变化
3. 识别技术债务
4. 生成报告保存到 /reports/daily-{date}.md
"
```

#### `/loop` vs 系统级调度对比

| 维度 | `/loop` 命令 | launchd/cron |
|------|-------------|--------------|
| **配置复杂度** | 简单，自然语言 | 需编写配置文件 |
| **最长运行** | 3 天 | 无限制 |
| **会话依赖** | 依赖会话存在 | 独立运行 |
| **适用场景** | 开发时辅助、短期监控 | 生产环境、长期任务 |
| **调试便利** | 即时反馈 | 需查看日志 |
| **推荐用途** | 日常开发辅助 | 夜间批处理、CI/CD |

#### 最佳实践

1. **短期任务优先用 `/loop`**：开发过程中的监控、轮询等
2. **长期任务用 launchd/cron**：每日备份、夜间分析、周期报告
3. **组合使用**：`/loop` 做实时监控，launchd 做深度分析

```bash
# 组合示例：白天用 /loop 监控，晚上用 launchd 做深度分析
# /loop 命令（开发时）
/loop "*/30 * * * *" "快速检查服务状态"

# launchd 任务（夜间深度分析）
# 配置在 ~/Library/LaunchAgents/ 中，凌晨 2 点执行完整代码审查
```

#### 注意事项

> [!warning] 会话限制
> - `/loop` 任务在会话结束后会终止
> - 如果关闭 Claude Code，任务不会继续运行
> - 需要长期运行的任务仍应使用系统级调度

> [!tip] 3 天限制的意义
> 这个限制是为了防止"遗忘的循环"无限运行。任务到期后会自动触发最后一次执行然后删除。

## 与其他概念的关系

| 概念 | 关系 |
|------|------|
| [[N8N定时抓取热点资讯指南]] | N8N 是可视化工作流工具，Claude Code + Cron 是命令行自动化方案，两者可互补 |
| [[Claude Code 自定义斜杠命令教程]] | 斜杠命令可封装常用 prompt，在定时脚本中调用 |
| [[Claude MCP 使用指南]] | MCP 扩展可增强 Claude Code 能力，在定时任务中使用 |
| [[../01-基础概念/Agent智能体]] | 定时自动化可视为"固定逻辑的智能体" |

## 最佳实践

### 1. 渐进式引入
- 从轻量任务开始（如日志分析）
- 验证稳定后再增加复杂任务
- 先手动测试脚本，再配置 Cron

### 2. 环境变量处理
```bash
#!/bin/bash
# Cron 环境变量有限，需显式设置
export PATH="/usr/local/bin:/usr/bin:/bin:$HOME/.local/bin"
export NODE_PATH="/usr/local/lib/node_modules"

# 执行前验证环境
which claude || exit 1
```

### 3. 日志管理
```bash
# 日志轮转脚本
LOG_DIR="$HOME/claude-automation/logs"
RETENTION_DAYS=30

# 归档 30 天前的日志
find "$LOG_DIR" -name "*.log" -mtime +$RETENTION_DAYS -exec gzip {} \;
```

### 4. 安全建议
- 敏感信息使用环境变量存储
- 定期轮换 API Key
- 限制脚本执行权限 (`chmod +x`)
- 使用文件锁防止重复执行

### 5. 监控与告警
- 配置 Slack/邮件通知
- 记录执行指标（成功率、耗时）
- 定期审查日志

## 非交互模式下的权限确认问题（⚠️ 核心痛点）

> [!info] 📚 来源
> - [GitHub Issue #581 - Non-interactive mode permissions bug](https://github.com/anthropics/claude-code/issues/581) - 官方已知问题
> - [Claude Code --dangerously-skip-permissions Guide](https://morphllm.com/claude-code-dangerously-skip-permissions) - 完整权限指南

> [!note] 适用于所有调度方式
> 无论是 launchd（macOS）还是 cron（Linux），在非交互式环境中都会遇到此问题。

### 问题现象

当通过 cron 执行 Claude Code 时，可能会遇到以下情况：

```bash
# cron 日志中的错误
I need permission to use the Bash tool to run these commands.
I need permission to read files in this directory.
# 任务卡住，等待用户确认
```

这是因为 Claude Code 默认会请求工具使用权限，在非交互式环境中无法获得确认。

### 解决方案

#### 方案一：使用 `--dangerously-skip-permissions`（推荐用于 Cron）

这是最直接的解决方案，跳过所有权限确认：

```bash
#!/bin/bash
# daily-automation.sh

claude code . --prompt "分析代码质量并生成报告" \
  --dangerously-skip-permissions \
  --output "$HOME/reports/daily-$(date +%Y%m%d).md" \
  >> "$HOME/logs/cron-$(date +%Y%m%d).log" 2>&1
```

**Crontab 配置**：
```bash
# 每天 9:00 执行，跳过权限确认
0 9 * * * /home/user/claude-automation/scripts/daily-review.sh --dangerously-skip-permissions
```

**安全建议**：
- 结合 Docker 容器使用，隔离环境
- 配置 `--max-turns` 限制执行轮次
- 使用 Git 版本控制，便于回滚

#### 方案二：使用 `--allowedTools` 限制工具范围

```bash
#!/bin/bash

# 只允许特定的安全工具
claude code . --prompt "分析代码" \
  --allowedTools "Read,Edit,Write,Bash(npm test)" \
  --output "$HOME/reports/report.md"
```

#### 方案三：配置 `settings.json` 预设权限

在项目的 `.claude/settings.json` 中配置：

```json
{
  "permissions": {
    "allow": [
      "Bash(npm test)",
      "Bash(npm run build)",
      "Bash(git *)",
      "Read(./src/**)",
      "Edit(./src/**)",
      "Write(./reports/**)"
    ],
    "deny": [
      "Bash(rm *)",
      "Bash(curl *)",
      "Read(./.env*)",
      "Read(**/secrets/**)"
    ]
  }
}
```

**注意**：根据 GitHub Issue #581，非交互模式可能不完全尊重此配置，建议与方案一结合使用。

#### 方案四：结合 Docker 容器隔离（最安全）

```bash
#!/bin/bash
# docker-automation.sh

docker run --rm -v "$PWD:/workspace" \
  -w /workspace \
  --user "$(id -u):$(id -g)" \
  claude-code:latest \
  claude code . --prompt "分析代码" \
    --dangerously-skip-permissions \
    --max-turns 50
```

**Dockerfile 示例**：
```dockerfile
FROM ubuntu:24.04

# 安装 Claude Code
RUN curl -fsSL https://code.claude.com/install.sh | sh

# 创建非 root 用户
RUN useradd -m -u 1000 claude
USER claude
WORKDIR /workspace

ENTRYPOINT ["claude"]
```

### 完整的定时任务自动化脚本模板

```bash
#!/bin/bash
# claude-automation-template.sh
# 安全的 Claude Code 定时任务自动化脚本模板
# 适用于 launchd (macOS) 和 cron (Linux)

set -euo pipefail

# === 配置区域 ===
PROJECT_DIR="/home/user/projects/myapp"
LOG_DIR="$HOME/claude-automation/logs"
REPORT_DIR="$HOME/claude-automation/reports"
MAX_TURNS=50  # 防止无限循环
TIMEOUT_SEC=3600  # 1小时超时

# === 环境设置 ===
export PATH="/usr/local/bin:/usr/bin:/bin:$HOME/.local/bin"
mkdir -p "$LOG_DIR" "$REPORT_DIR"

TIMESTAMP=$(date +%Y%m%d-%H%M%S)
LOG_FILE="$LOG_DIR/automation-$TIMESTAMP.log"
LOCK_FILE="/tmp/claude-automation.lock"

# === 锁机制（防止重复执行） ===
exec 200>"$LOCK_FILE"
if ! flock -n 200; then
    echo "[$(date)] 另一个实例正在运行，退出" >> "$LOG_FILE"
    exit 0
fi

# === 主执行函数 ===
main() {
    echo "=== Claude Code 定时任务执行开始: $(date) ===" | tee -a "$LOG_FILE"

    cd "$PROJECT_DIR" || exit 1

    # 使用超时和权限跳过执行
    timeout "$TIMEOUT_SEC" claude code . \
        --prompt "检查项目代码质量：
        1. 代码规范问题
        2. 潜在安全风险
        3. 性能优化建议
        4. 测试覆盖率评估

        用中文输出 Markdown 格式报告。" \
        --dangerously-skip-permissions \
        --max-turns "$MAX_TURNS" \
        --output "$REPORT_DIR/analysis-$TIMESTAMP.md" \
        2>&1 | tee -a "$LOG_FILE"

    EXIT_CODE=${PIPESTATUS[0]}

    if [ $EXIT_CODE -eq 0 ]; then
        echo "=== 执行成功: $(date) ===" | tee -a "$LOG_FILE"
        # 可选：发送成功通知
        # notify_send "✅ Claude Code 自动化完成"
    else
        echo "=== 执行失败 (退出码: $EXIT_CODE): $(date) ===" | tee -a "$LOG_FILE"
        # 可选：发送失败通知
        # notify_send "❌ Claude Code 自动化失败"
    fi

    return $EXIT_CODE
}

# === 执行并记录 ===
main
EXIT_CODE=$?

flock -u 200
exit $EXIT_CODE
```

### 定时任务配置示例

#### macOS launchd 配置

```xml
<!-- ~/Library/LaunchAgents/com.user.claude-daily.plist -->
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.user.claude-daily</string>
    <key>ProgramArguments</key>
    <array>
        <string>/bin/bash</string>
        <string>/Users/你的用户名/claude-automation/scripts/daily-review.sh</string>
    </array>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>9</integer>
        <key>Minute</key>
        <integer>0</integer>
    </dict>
    <key>StandardOutPath</key>
    <string>/Users/你的用户名/claude-automation/logs/launchd.log</string>
    <key>StandardErrorPath</key>
    <string>/Users/你的用户名/claude-automation/logs/launchd-error.log</string>
    <key>EnvironmentVariables</key>
    <dict>
        <key>PATH</key>
        <string>/usr/local/bin:/usr/bin:/bin</string>
    </dict>
</dict>
</plist>
```

```bash
# 加载任务
launchctl load ~/Library/LaunchAgents/com.user.claude-daily.plist
```

#### Linux Crontab 配置

```bash
# 编辑 crontab
crontab -e

# 添加定时任务（带完整路径和环境变量）
HOME=/home/user
PATH=/usr/local/bin:/usr/bin:/bin:/home/user/.local/bin

# 每天早上 9:00 执行代码审查
0 9 * * * /home/user/claude-automation/scripts/daily-review.sh >> /home/user/claude-automation/logs/cron.log 2>&1

# 每周一 10:00 执行依赖安全检查
0 10 * * 1 /home/user/claude-automation/scripts/dependency-check.sh

# 每小时执行轻量健康检查
0 * * * * /home/user/claude-automation/scripts/health-check.sh
```

### 调试技巧

```bash
# 1. 手动测试脚本（模拟非交互环境）
env -i PATH="$PATH" HOME="$HOME" /home/user/claude-automation/scripts/test.sh

# 2. macOS launchd 调试
# 查看任务状态
launchctl list | grep claude
# 查看任务详情
launchctl print gui/$(id -u)/com.user.claude-daily
# 查看日志
tail -f ~/claude-automation/logs/launchd-*.log
# 查看系统日志中的 launchd 信息
log show --predicate 'subsystem == "com.apple.launchd"' --last 1h

# 3. Linux cron 调试
# 查看 cron 执行日志
tail -f /var/log/syslog | grep CRON
tail -f ~/claude-automation/logs/automation-*.log

# 4. 测试权限跳过是否生效
claude code . --prompt "echo test" --dangerously-skip-permissions --dry-run

# 5. 检查 Claude 版本
claude --version
```

## 常见问题

**Q: macOS 上应该用 cron 还是 launchd？**

A: **强烈推荐使用 launchd**。cron 在 Mac 上无法正确处理系统休眠：
- 可能在 Power Nap 唤醒时意外执行
- 可能在睡眠期间错过任务
- 不会在唤醒后补执行错过的任务

launchd 是苹果原生方案，支持休眠补偿机制。

---

**Q: 任务执行失败，提示找不到 claude 命令？**

A: 非交互环境变量有限，需在脚本开头显式设置 `PATH`：
```bash
export PATH="/usr/local/bin:/usr/bin:/bin:$HOME/.local/bin"
# 或使用完整路径
/usr/local/bin/claude --version
```

---

**Q: 如何调试定时任务脚本？**

A:
```bash
# 添加调试信息
DEBUG_LOG="$HOME/claude-automation/debug-$(date +%Y%m%d-%H%M).log"
{
    echo "=== Debug Info: $(date) ==="
    echo "User: $(whoami)"
    echo "PATH: $PATH"
    which claude || echo "Claude not found"
} >> "$DEBUG_LOG" 2>&1

# macOS launchd: 查看任务日志
tail -f ~/claude-automation/logs/launchd-stderr.log

# Linux cron: 查看系统日志
tail -f /var/log/syslog | grep CRON
```

---

**Q: 定时任务执行时间过长怎么办？**

A: 使用 `timeout` 限制执行时间，或拆分为多个小任务
```bash
timeout 3600 claude code . --prompt "分析代码"  # 最多1小时
```

---

**Q: 如何避免重复执行？**

A: 使用文件锁
```bash
LOCK_FILE="/tmp/claude-task.lock"
[ -f "$LOCK_FILE" ] && exit 0
touch "$LOCK_FILE"
# ... 执行任务 ...
rm "$LOCK_FILE"
```

---

**Q: launchd 任务加载后不执行？**

A: 检查以下几点：
```bash
# 1. 验证 plist 语法
plutil -lint ~/Library/LaunchAgents/com.user.claude.plist

# 2. 检查任务是否已加载
launchctl list | grep claude

# 3. 查看错误日志
cat ~/claude-automation/logs/launchd-stderr.log

# 4. 手动触发测试
launchctl start com.user.claude-daily

# 5. 检查文件权限（plist 文件不应有 group/other 写权限）
chmod 644 ~/Library/LaunchAgents/com.user.claude.plist
```

---

**Q: Claude Code 有原生定时任务支持吗？**

A: **有了！** 2026 年 Claude Code 新增了 **`/loop` 命令**，支持 cron 风格的定时调度，任务最长运行 3 天。详见 [[#9-官方方案-loop-命令推荐]]

---

**Q: `/loop` 和 launchd/cron 该选哪个？**

A:
- **`/loop`**：适合开发时短期监控、PR 跟踪、状态轮询等会话内任务
- **launchd/cron**：适合长期运行的夜间批处理、每日备份、跨会话任务

---

**Q: `/loop` 任务会话关闭后还会继续运行吗？**

A: **不会**。`/loop` 是会话级的，关闭 Claude Code 后任务终止。需要长期运行的任务应使用 launchd（macOS）或 cron（Linux）。

## 相关文档
- [[AI学习/00-索引/MOC|AI学习索引]]
- [[如何使用Claude code|Claude Code 使用指南]]
- [[Claude Code 自定义斜杠命令教程]]

## 参考资料

### 官方资源
- [Run prompts on a schedule - Claude Code Docs](https://code.claude.com/docs/en/scheduled-tasks) - 官方定时任务文档 ⭐ **新增**
- [Claude Code Hooks 官方文档](https://code.claude.com/docs/en/hooks) - Hooks 参考文档
- [Claude Code Hooks 入门指南](https://code.claude.com/docs/en/hooks-guide) - 入门教程
- [GitHub Issue #30649 - Scheduled/Cron Support](https://github.com/anthropics/claude-code/issues/30649) - 功能请求
- [GitHub Issue #581 - Non-interactive permissions bug](https://github.com/anthropics/claude-code/issues/581) - 权限已知问题

### `/loop` 命令相关
- [Claude Code Scheduled Tasks: Complete Setup Guide (2026)](https://claudefa.st/blog/guide/development/scheduled-tasks) - 完整教程 ⭐ **新增**
- [Reddit: Claude Code just shipped /loop](https://www.reddit.com/r/ClaudeCode/comments/1rn94wp/claude_code_just_shipped_loop_schedule_recurring/) - 社区讨论
- [The Decoder: Claude Code as background worker](https://the-decoder.com/anthropic-turns-claude-code-into-a-background-worker-with-local-scheduled-tasks/) - 新闻报道
- [YouTube: Claude Code Loops in 7 Minutes](https://www.youtube.com/watch?v=pWZh37iRnDA) - 视频教程

### macOS launchd 资源
- [Apple Developer - Creating Launch Daemons and Agents](https://developer.apple.com/library/archive/documentation/MacOSX/Conceptual/BPSystemStartup/Chapters/CreatingLaunchdJobs.html) - 官方文档
- [launchd.plist(5) man page](https://www.manpagez.com/man/5/launchd.plist/) - 参数参考手册
- [launchd.info](https://www.launchd.info/) - 完整教程与示例

### 社区资源
- [Claude Code + Cron Automation Complete Guide](https://smartscope.blog/en/generative-ai/claude/claude-code-cron-schedule-automation-complete-guide-2025/) - SmartScope 完整教程
- [Claude Code Hooks Complete Guide (February 2026)](https://smartscope.blog/en/generative-ai/claude/claude-code-hooks-guide/) - 14 种生命周期事件 ⭐ **更新**
- [Claude Code Hooks: All Lifecycle Events Explained](https://www.pixelmojo.io/blogs/claude-code-hooks-production-quality-ci-cd-patterns) - CI/CD 模式
- [Scheduled Tasks: How to Put Claude on Autopilot](https://atalupadhyay.wordpress.com/2026/03/02/scheduled-tasks-how-to-put-claude-on-autopilot/) - 自动化教程
- [Claude Code --dangerously-skip-permissions Guide](https://morphllm.com/claude-code-dangerously-skip-permissions) - 权限系统完整指南
- [Reddit: Claude now works my night shift](https://www.reddit.com/r/ClaudeAI/comments/1qflv3y/claude_now_works_my_night_shift_heres_how_i_set/) - 用户实践经验
- [TheNeuron: Automate Recurring Tasks](https://www.theneuron.ai/explainer-articles/claude-code-recurring-automations-tutorial/) - 非技术用户教程
- [Claude Code CLI Cheatsheet](https://shipyard.build/blog/claude-code-cheat-sheet/) - 命令速查表

### 视频教程
- [The AI Agent Cron Job Inception Strategy](https://www.youtube.com/watch?v=0Y0jbaoREHc) - YouTube
- [Claude Code Commands & Cron Jobs Tutorial](https://www.youtube.com/watch?v=l6V0u3ZIgDI) - YouTube
