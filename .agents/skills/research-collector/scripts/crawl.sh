#!/usr/bin/env bash
# Crawl4AI 启动器：定位 crawl4ai conda env，把参数透传给 crawl.py。
# 用法:
#   单 URL → stdout:  bash crawl.sh --url <URL>
#   批量 → 输出目录:  bash crawl.sh --url <URL1> --url <URL2> ... --output-dir <dir>
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# ---------------------------------------------------------------------------
# 定位 conda 可执行文件（与 setup.sh 同一套解析逻辑，覆盖 Unix/Windows 布局）
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
    "$HOME/miniconda3/bin/conda" \
    "$HOME/anaconda3/bin/conda" \
    "$HOME/miniforge3/bin/conda" \
    "$HOME/mambaforge/bin/conda" \
    "/opt/miniconda3/bin/conda" \
    "/opt/anaconda3/bin/conda" \
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
# 用 conda info --base 动态解析 env 路径（Windows 下用 cygpath 转 unix）
# ---------------------------------------------------------------------------
if ! CONDA_BASE="$("$CONDA_EXE" info --base 2>/dev/null)"; then
  echo "错误: conda 不可用（conda info --base 失败）。请先运行 setup.sh。" >&2
  exit 2
fi
if command -v cygpath >/dev/null 2>&1; then
  CONDA_BASE="$(cygpath -u "$CONDA_BASE")"
fi
ENV_DIR="$CONDA_BASE/envs/crawl4ai"

# ---------------------------------------------------------------------------
# 定位 env 内 python（Windows: python.exe；Unix/macOS: bin/python）
# ---------------------------------------------------------------------------
if [ -f "$ENV_DIR/python.exe" ]; then
  ENV_PY="$ENV_DIR/python.exe"
elif [ -x "$ENV_DIR/bin/python" ]; then
  ENV_PY="$ENV_DIR/bin/python"
else
  echo "错误: 未找到 crawl4ai 环境（$ENV_DIR）。请先运行 $SCRIPT_DIR/setup.sh 安装。" >&2
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
