#!/bin/bash
# Stop hook reference: 对话结束时自动提交改动
# 遵循 git-workflow 规范：<type>: <description>

set -euo pipefail

# 确保在 git 仓库中
git rev-parse --is-inside-work-tree &>/dev/null || exit 0

# 无改动则跳过
git diff --quiet HEAD 2>/dev/null && git diff --quiet --cached 2>/dev/null && exit 0

# 检查是否有已暂存的文件
has_staged=$(git diff --cached --name-only 2>/dev/null)

if [ -z "$has_staged" ]; then
  # 没有已暂存文件，暂存所有改动（排除不追踪的大文件/敏感文件）
  git add -A
fi

# 获取改动的文件列表
changed_files=$(git diff --cached --name-only)
file_count=$(echo "$changed_files" | wc -l | tr -d ' ')

# 根据文件路径和内容判断 commit type
type="chore"

# 检查是否全是新增文件
all_new=true
while IFS= read -r f; do
  if git cat-file -e HEAD:"$f" 2>/dev/null; then
    all_new=false
    break
  fi
done <<< "$changed_files"

if [ "$all_new" = true ]; then
  type="feat"
else
  # 按文件路径推断类型
  has_docs=false
  has_test=false
  has_config=false
  has_source=false

  while IFS= read -r f; do
    case "$f" in
      *.md|docs/*)          has_docs=true ;;
      *test*|*spec*)        has_test=true ;;
      *.json|*.yaml|*.yml|*.toml|*.sh|Makefile|.gitignore) has_config=true ;;
      *.js|*.ts|*.jsx|*.tsx|*.py|*.go|*.rs|*.java|*.c|*.cpp|*.h) has_source=true ;;
    esac
  done <<< "$changed_files"

  if [ "$has_docs" = true ] && [ "$has_source" = false ] && [ "$has_test" = false ]; then
    type="docs"
  elif [ "$has_test" = true ] && [ "$has_source" = false ]; then
    type="test"
  elif [ "$has_source" = true ]; then
    type="refactor"
  elif [ "$has_config" = true ]; then
    type="chore"
  fi
fi

# 生成 description: 列出关键文件名
if [ "$file_count" -le 3 ]; then
  desc=$(echo "$changed_files" | sed 's|.*/||' | paste -sd ", " -)
else
  first=$(echo "$changed_files" | head -2 | sed 's|.*/||' | paste -sd ", " -)
  desc="$first and $((file_count - 2)) more files"
fi

# 构建 commit message
msg="$type: $desc"

# 提交。Claude Code 侧不添加 Claude Code co-author，避免污染提交来源。
git commit -m "$msg"
