---
tags: [claude, ai]
---

# Claude Code 会话管理

> [!info] 概述
> **会话管理让你灵活控制对话上下文** - 支持创建新会话、恢复历史会话、查看状态等功能，提高工作效率。

## 核心概念 💡

### 什么是会话管理

**是什么**：Claude Code 的多会话管理功能

**为什么需要**：
- 隔离不同项目的上下文
- 保存重要的对话历史
- 管理 token 消耗
- 快速切换工作状态

**会话类型**：
| 类型 | 说明 | 使用场景 |
|------|------|----------|
| 匿名会话 | 自动生成的临时会话 | 快速测试、一次性任务 |
| 命名会话 | 用户指定名称的会话 | 特定项目、长期工作 |

### 会话生命周期

```
创建 → 使用 → 暂停 → 恢复 → 清理
  ↓                            ↓
 存储 ←←←←← 自动保存 ←←←←←←←←←←←←
```

**生命周期说明**：
- **创建**：使用 `/new` 或 `/new <name>` 创建
- **使用**：在会话中进行对话和操作
- **暂停**：退出 Claude Code 时自动暂停
- **恢复**：使用 `/resume <name>` 恢复历史会话
- **清理**：使用 `/clear` 清除当前会话内容

### 会话数据结构

```json
{
  "id": "session-abc123def456",
  "name": "my-project",
  "messages": [
    {
      "role": "user",
      "content": "帮我实现登录功能"
    },
    {
      "role": "assistant",
      "content": "好的，我来帮你..."
    }
  ],
  "createdAt": "2024-02-23T10:00:00Z",
  "updatedAt": "2024-02-23T15:30:00Z",
  "metadata": {
    "model": "deepseek-chat",
    "provider": "deepseek"
  }
}
```

## 操作步骤

### 创建新会话

```bash
# 创建空白会话
/new

# 创建命名会话
/new my-project
/new feature-xyz
```

### 管理历史会话

```bash
# 列出所有会话
/resume

# 恢复指定会话
/resume my-project

# 清除当前会话
/clear
```

### 查看会话状态

```bash
# 查看当前会话信息
/status

# 显示 token 使用情况
/context
```

## 会话存储与管理

### 会话文件结构
```
~/.claude/sessions/
├── session-abc123.json    # 匿名会话
├── my-project.json        # 命名会话
└── feature-login.json     # 功能会话
```

### 查看会话文件
```bash
# 列出所有会话文件
ls ~/.claude/sessions/

# 查看特定会话内容
cat ~/.claude/sessions/my-project.json | jq '.'
```

### 会话数据格式
```json
{
  "id": "session-xxx",
  "name": "my-project",
  "messages": [...],
  "createdAt": "2024-02-23T10:00:00Z",
  "updatedAt": "2024-02-23T15:30:00Z"
}
```

## Token 管理策略

### Token 消耗分析
| 操作 | 大约消耗 | 说明 |
|------|----------|------|
| 创建新会话 | ~100 tokens | 初始化系统提示 |
| 恢复历史会话 | 取决于历史长度 | 每条消息约 50-500 tokens |
| /clear 清理 | ~100 tokens | 重置为初始状态 |
| 文件读取 | ~1-10 tokens/KB | 取决于文件大小 |
| 代码生成 | ~100-1000 tokens/次 | 取决于生成代码长度 |

### 优化建议

**监控 Token 使用**：
```bash
# 实时查看 token 消耗
/context

# 查看当前会话状态
/status
```

**定期清理**：
```bash
# 清理当前会话
/clear

# 清理后重新开始
/new fresh-session
```

**为不同任务创建独立会话**：
```bash
# 开发会话
/new dev-auth
/new dev-payment

# 学习会话
/new learn-react

# 调试会话
/new debug-bug-123
```

**会话合并策略**：
- 短期任务：使用匿名会话，完成后 `/clear`
- 长期项目：使用命名会话，定期清理
- 学习记录：保留完整会话历史

## 会话备份与恢复

### 手动备份
```bash
# 备份单个会话
cp ~/.claude/sessions/my-project.json ~/backup/sessions/

# 备份所有会话
cp -r ~/.claude/sessions/ ~/backup/sessions-$(date +%Y%m%d)/
```

### 自动备份脚本
```bash
#!/bin/bash
# backup-sessions.sh

BACKUP_DIR="$HOME/backups/claude-sessions"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p "$BACKUP_DIR"
cp -r ~/.claude/sessions/ "$BACKUP_DIR/sessions_$DATE/"

echo "会话已备份至: $BACKUP_DIR/sessions_$DATE/"
```

### 跨设备同步
```bash
# 同步到其他机器
scp ~/.claude/sessions/*.json user@remote:~/.claude/sessions/

# 使用 rsync 同步
rsync -av ~/.claude/sessions/ user@remote:~/.claude/sessions/

# 从 Git 仓库同步
git clone https://github.com/yourname/claude-sessions.git
cp Claude Code 会话管理.json ~/.claude/sessions/
```

### 会话恢复示例
```bash
# 查看备份的会话
ls ~/backup/sessions/

# 恢复指定会话
cp ~/backup/sessions/my-project.json ~/.claude/sessions/

# 在 Claude Code 中恢复
/resume my-project
```

## 实用场景

### 场景一：项目隔离
```bash
# 为不同项目创建独立会话
/new project-a     # 项目 A
/new project-b     # 项目 B
/resume project-a  # 切换回项目 A
```

### 场景二：功能开发
```bash
/new feature-login    # 登录功能开发
/new feature-payment  # 支付功能开发
/resume feature-login # 继续登录功能
```

### 场景三：问题排查
```bash
/new bug-investigation  # 专门用于排查问题
/clear                  # 问题解决后清理
```

### 场景四：长期项目跟踪
```bash
# 为长期项目创建专用会话
/new project-crm-2024

# 定期恢复以更新进度
/resume project-crm-2024

# 项目里程碑节点
/new project-crm-v1.0    # 版本发布
/new project-crm-v2.0    # 下一版本
```

### 场景五：教学/演示会话
```bash
# 教学专用会话
/new teach-react-hooks

# 演示专用会话
/new demo-cli-features

# 准备演示内容后，可以直接演示
# 无需担心历史对话干扰
```

### 场景六：A/B 测试不同方案
```bash
# 方案 A 会话
/new solution-a-rest-api
# 讨论和开发 REST API 方案

# 方案 B 会话
/new solution-b-graphql
# 讨论和开发 GraphQL 方案

# 对比两个方案的结果
# 然后决定最终方案
```

## 注意事项 ⚠️

### 常见错误

**会话恢复失败**：
- ❌ 会话名称拼写错误
- ❌ 会话已被删除

**Token 超限**：
- ❌ 会话历史过长
- ❌ 未及时清理无用上下文

### 最佳实践

**命名规范**：
```bash
# ✅ 推荐命名
/new project-auth
/new feature-api-v2
/new bug-fix-2024-02-23

# ❌ 不推荐
/new test
/new temp
/new 123
```

**定期清理**：
- 使用 `/clear` 清理不需要的历史
- 使用 `/context` 监控 token 使用

**会话组织**：
- 按项目分类创建会话
- 按功能模块隔离上下文
- 定期归档旧会话

## 高级技巧

### 会话模板创建

**创建项目模板**：
```bash
# 创建模板会话
/new template-web-app

# 配置初始上下文
"这是一个 Web 应用项目，使用 React + TypeScript + Vite"
"项目结构遵循 feature-first 模式"
```

**从模板创建新会话**：
```bash
# 复制模板会话
cp ~/.claude/sessions/template-web-app.json \
   ~/.claude/sessions/new-project.json

# 恢复并重命名
/resume new-project
```

### 环境变量与会话

**会话特定的环境变量**：
```bash
# 在会话中设置临时环境
export PROJECT_ENV=development
export DEBUG=true

# 这些设置会在会话中持续有效
# 直到会话结束或被清除
```

**会话配置文件**：
```bash
# .claude-env 项目级配置
echo "PROJECT_NAME=my-app" > .claude-env
echo "USE_TYPESCRIPT=true" >> .claude-env

# Claude Code 会自动读取项目级配置
```

### 与 Git 工作流结合

**分支与会话对应**：
```bash
# 创建与分支对应的会话
/new feature-user-auth

# 切换到对应分支
git checkout feature/user-auth

# 在会话中开发功能
# 完成后提交代码
/commit

# 功能完成后清理会话
/clear
```

**Commit 后清理**：
```bash
# 开发功能
/new feature-xyz
# ... 开发过程 ...
/commit "Add feature XYZ"

# 提交后清理会话，准备下一个任务
/clear
```

**Code Review 会话**：
```bash
# 为 PR 创建专用会话
/new pr-review-123

# 恢复 PR 上下文
/resume pr-review-123
/review-pr 123

# Review 完成后清理
/clear
```

### 会话搜索与过滤

**搜索会话内容**：
```bash
# 搜索包含特定内容的会话
grep -r "登录功能" ~/.claude/sessions/

# 查找最近修改的会话
ls -lt ~/.claude/sessions/ | head -10
```

**按日期过滤**：
```bash
# 查找今天的会话
find ~/.claude/sessions/ -newermt "today" -ls

# 查找本周的会话
find ~/.claude/sessions/ -newermt "week ago" -ls
```

## 常见问题 ❓

**Q: 会话保存在哪里？**

A: 会话数据存储在 `~/.claude/sessions/` 目录下。

**Q: 会话会自动保存吗？**

A: 是的，所有对话都会自动保存到当前会话中。

**Q: 如何删除旧会话？**

A: 直接删除 `~/.claude/sessions/` 下对应的会话文件。

**Q: token 消耗太快怎么办？**

A: 使用 `/clear` 清理历史，或创建新会话减少上下文长度。

**Q: 会话可以共享吗？**

A: 可以，通过复制会话文件来共享：
```bash
# 导出会话
cp ~/.claude/sessions/my-project.json ./shared-session.json

# 导入会话
cp ./shared-session.json ~/.claude/sessions/
```

**Q: 会话有大小限制吗？**

A: 会话文件本身没有大小限制，但过长的历史会影响 token 消耗和响应速度。建议定期使用 `/clear` 清理。

**Q: 如何在会话间复制内容？**

A: 可以使用 `/resume` 切换会话查看历史，然后手动复制需要的内容到新会话。

**Q: 会话文件可以编辑吗？**

A: 技术上可以编辑 JSON 文件，但不建议手动修改。格式错误可能导致会话无法加载。

## 相关文档
[[如何使用Claude code]] | [[Claude Code 常用功能]] | [[Claude MCP 使用指南]]
