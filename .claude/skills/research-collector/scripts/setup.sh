#!/usr/bin/env bash
# 一键安装 Crawl4AI 精读环境（可重复执行）。
# 幂等：env 已存在时跳过创建，只会升级 crawl4ai / 补齐 Playwright Chromium。
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# ---------------------------------------------------------------------------
# 1. 定位 conda 可执行文件
# ---------------------------------------------------------------------------
resolve_conda() {
  # 优先级: $CONDA_EXE 环境变量 > PATH 中的 conda > 常见安装路径
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
    "/c/Users/zhq/miniconda3/Scripts/conda.exe" \
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
  echo "错误: 找不到 conda。请先安装 Miniconda 或设置 CONDA_EXE 环境变量。" >&2
  exit 1
fi
echo "[1/4] 使用 conda: $CONDA_EXE"

# ---------------------------------------------------------------------------
# 2. 解析 env python 路径（用 conda info --base 动态定位，不硬编码绝对路径）
# ---------------------------------------------------------------------------
if BASE_WIN="$("$CONDA_EXE" info --base 2>/dev/null)"; then
  if command -v cygpath >/dev/null 2>&1; then
    BASE="$(cygpath -u "$BASE_WIN")"
  else
    BASE="$BASE_WIN"
  fi
else
  echo "错误: conda info --base 失败，conda 可能不可用。" >&2
  exit 1
fi
ENV_DIR="$BASE/envs/crawl4ai"
ENV_PY="$ENV_DIR/python.exe"
echo "[2/4] 目标环境: $ENV_DIR"

# ---------------------------------------------------------------------------
# 3. 创建 env（如不存在）；若因 Anaconda TOS 未接受而失败，自动接受后重试
# ---------------------------------------------------------------------------
if [ ! -d "$ENV_DIR" ]; then
  echo "[3/4] 创建 conda env: crawl4ai (python=3.12) ..."
  if ! "$CONDA_EXE" create -n crawl4ai python=3.12 -y 2>"$TMPDIR/crawl4ai-setup-create.log" \
    || grep -qi "CondaToSNonInteractiveError" "$TMPDIR/crawl4ai-setup-create.log" 2>/dev/null; then
    echo "      检测到 Anaconda TOS 未接受，尝试自动接受后重试 ..."
    # shellcheck disable=SC2013
    for url in $("$CONDA_EXE" config --show channels 2>/dev/null | awk -F"'" '/- /{gsub(/^ *- /,"");print}'); do
      [ -z "$url" ] && continue
      "$CONDA_EXE" tos accept --override-channels --channel "$url" >/dev/null 2>&1 || true
    done
    "$CONDA_EXE" create -n crawl4ai python=3.12 -y
  fi
else
  echo "[3/4] env 已存在，跳过创建。"
fi

# ---------------------------------------------------------------------------
# 4. 安装 / 升级依赖
# ---------------------------------------------------------------------------
echo "[4/4] 安装/升级 crawl4ai ..."
"$ENV_PY" -m pip install -U crawl4ai

echo "      安装 Playwright Chromium（若未安装会下载 ~150MB）..."
"$ENV_PY" -m playwright install chromium

echo
echo "✅ crawl4ai 环境就绪: $ENV_PY"
echo "   校验: \"$ENV_PY\" -c \"import crawl4ai; print(crawl4ai.__version__)\""
