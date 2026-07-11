# Git Workflow

## Commit Message Format

```
<type>: <description>

<optional body>
```

### Types

| Type | 说明 | 示例 |
|------|------|------|
| feat | 新功能 | feat: add user authentication |
| fix | 修复 bug | fix: resolve login timeout |
| refactor | 重构代码 | refactor: extract validation logic |
| docs | 文档更新 | docs: update API documentation |
| test | 测试相关 | test: add unit tests for auth |
| chore | 构建/工具 | chore: update dependencies |
| perf | 性能优化 | perf: optimize database queries |
| ci | CI/CD 配置 | ci: add GitHub Actions workflow |

### 示例

```bash
# 简单提交
git commit -m "feat: add user login"

# 带 body 的提交
git commit -m "fix: resolve race condition in data sync

- Add mutex lock for concurrent access
- Add retry logic for failed requests
- Update error handling"

# 关联 issue
git commit -m "feat: add dark mode (#123)"
```

---

## Branch Workflow

### 分支命名

| 分支 | 用途 | 命名格式 |
|------|------|----------|
| main | 生产代码 | `main` |
| develop | 开发集成 | `develop` |
| feature | 新功能 | `feature/<name>` |
| bugfix | 修复 bug | `bugfix/<name>` |
| hotfix | 紧急修复 | `hotfix/<name>` |
| release | 发布准备 | `release/<version>` |

### 分支流程

```
main (生产)
  └── release/v1.0 (发布准备)
      └── develop (开发集成)
          ├── feature/auth (功能开发)
          ├── feature/dashboard
          └── bugfix/fix-login
```

---

## Pull Request Workflow

### 创建 PR

1. **推送分支**
   ```bash
   git push -u origin feature/my-feature
   ```

2. **创建 PR**
   ```bash
   gh pr create --fill
   # 或手动创建
   ```

3. **PR 描述模板**
   ```markdown
   ## 改动说明
   简要描述做了什么

   ## 改动类型
   - [ ] 新功能
   - [ ] Bug 修复
   - [ ] 重构
   - [ ] 文档更新
   - [ ] 其他

   ## 测试计划
   - [ ] 单元测试通过
   - [ ] 手动测试完成
   - [ ] 边界情况验证

   ## 关联 Issue
   Closes #123
   ```

### Code Review 检查项

- [ ] 代码符合项目规范
- [ ] 有必要的注释
- [ ] 测试覆盖率足够
- [ ] 无安全风险
- [ ] 性能无明显问题

---

## 开发工作流

### 1. 开始新功能

```bash
# 确保在最新代码上
git checkout develop
git pull origin develop

# 创建功能分支
git checkout -b feature/my-feature

# 开发、测试、提交
git add .
git commit -m "feat: add new feature"

# 推送
git push -u origin feature/my-feature
```

### 2. 同步最新代码

```bash
# 在功能分支上
git fetch origin
git rebase origin/develop
# 解决冲突后
git rebase --continue
```

### 3. 完成合并

```bash
# 通过 PR 合并到 develop
# 或手动合并
git checkout develop
git merge --no-ff feature/my-feature
git push origin develop
```

---

## Hotfix 流程

```bash
# 从生产分支创建 hotfix
git checkout main
git checkout -b hotfix/fix-critical-bug

# 修复并提交
git commit -m "fix: critical security patch"

# 合并到 main 和 develop
git checkout main
git merge --no-ff hotfix/fix-critical-bug
git tag -a v1.0.1 -m "Hotfix version"

git checkout develop
git merge --no-ff hotfix/fix-critical-bug
```

---

## 常用命令

### 日志查看

```bash
# 简洁日志
git log --oneline

# 图形化日志
git log --graph --oneline --all

# 最近 10 条
git log -10

# 查看某个文件的历史
git log -- path/to/file
```

### 撤销操作

```bash
# 撤销工作区修改
git checkout -- <file>

# 撤销暂存
git reset HEAD <file>

# 修改最后一次提交
git commit --amend

# 回退提交（保留修改）
git reset --soft HEAD~1

# 回退提交（丢弃修改）
git reset --hard HEAD~1
```

### Stash

```bash
# 保存当前修改
git stash

# 查看保存列表
git stash list

# 恢复最近保存
git stash pop

# 删除保存
git stash drop
```

---

## Commit 最佳实践

1. **原子提交**：一个提交只做一件事
2. **有意义的描述**：说明为什么做，而不仅仅是做了什么
3. **使用中文或英文**：团队保持一致
4. **关联 Issue**：使用 `#123` 格式关联

---

## 版本号规范

使用 [Semantic Versioning](https://semver.org/):

```
MAJOR.MINOR.PATCH

MAJOR - 不兼容的 API 修改
MINOR - 向下兼容的功能新增
PATCH - 向下兼容的问题修正
```

示例：`v1.2.3`
