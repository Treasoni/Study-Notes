#!/usr/bin/env bash
# Crawl4AI 启动器：定位 crawl4ai conda env，把参数透传给 crawl.py。
# 用法:
#   单 URL → stdout:  bash crawl.sh --url <URL>
#   批量 → 输出目录:  bash crawl.sh --url <URL1> --url <URL2> ... --output-dir <dir>
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# ---------------------------------------------------------------------------
# 定位 conda 可执行文件（与 setup.sh 同一套解析逻辑）
# ---------------------------------------------------------------------------
resolve_conda() {
  if [ -n "${CONDA_EXE:-}" ]; then
    printf '%s' "$CONDA_EXE"
    return 0
  fi
  if command -v conda >/dev/null 2>&1; then
    command -v conda
    return 0
  fi
  for c in \
    "$HOME/miniconda3/Scripts/conda.exe" \
    "$HOME/anaconda3/Scripts/conda.exe" \
    "/c/ProgramData/miniconda3/Scripts/conda.exe" \
    "/c/ProgramData/anaconda3/Scripts/conda.exe"
  do
    if [ -f "$c" ]; then
      printf '%s' "$c"
      return 0
    fi
  done
  return 1
}

if ! CONDA_EXE="$(resolve_conda)"; then
  echo "错误: 找不到 conda。请先运行 setup.sh 安装 crawl4ai 环境，或设置 CONDA_EXE。" >&2
  exit 2
fi

# ---------------------------------------------------------------------------
# 用 conda info --base 动态解析 env python 路径
# ---------------------------------------------------------------------------
if ! BASE_WIN="$("$CONDA_EXE" info --base 2>/dev/null)"; then
  echo "错误: conda 不可用（conda info --base 失败）。请先运行 setup.sh。" >&2
  exit 2
fi
if command -v cygpath >/dev/null 2>&1; then
  BASE="$(cygpath -u "$BASE_WIN")"
else
  BASE="$BASE_WIN"
fi
ENV_PY="$BASE/envs/crawl4ai/python.exe"

if [ ! -x "$ENV_PY" ]; then
  echo "错误: 未找到 crawl4ai 环境（$ENV_PY）。请先运行 $SCRIPT_DIR/setup.sh 安装。" >&2
  exit 2
fi

# ---------------------------------------------------------------------------
# 强制 UTF-8 输出（Windows 控制台默认 GBK 会乱码中文正文）
# ---------------------------------------------------------------------------
export PYTHONUTF8=1
export PYTHONIOENCODING=utf-8

# ---------------------------------------------------------------------------
# 透传全部参数给 crawl.py
# ---------------------------------------------------------------------------
exec "$ENV_PY" "$SCRIPT_DIR/crawl.py" "$@"
