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

## 常见问题 ❓

**Q: 会话保存在哪里？**

A: 会话数据存储在 `~/.claude/sessions/` 目录下。

**Q: 会话会自动保存吗？**

A: 是的，所有对话都会自动保存到当前会话中。

**Q: 如何删除旧会话？**

A: 直接删除 `~/.claude/sessions/` 下对应的会话文件。

**Q: token 消耗太快怎么办？**

A: 使用 `/clear` 清理历史，或创建新会话减少上下文长度。

## 相关文档
[[如何使用Claude code]] | [[Claude Code 常用功能]]
