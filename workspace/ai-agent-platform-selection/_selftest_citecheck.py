# -*- coding: utf-8 -*-
"""负向测试：给引文校验器注入已知缺陷，断言它**确实会红**。

一个从没红过的门禁不是门禁。「跑出 0 处差异」既可能是真干净，也可能是没比到东西。
四个用例：
  A 基线（无缺陷）          → 期望 exit 0
  B 合并件被改一个字母      → 期望 exit 1（副本漂移）
  C 组装件英文引文被改       → 期望 exit 1（逐字回源未命中）
  D 出处列写了产品文件名     → 期望 exit 1（对照表结构）
用完自删 fixture；删除走**显式前缀断言**，不越界。
"""
import pathlib
import re
import subprocess
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = pathlib.Path("D:/Study-Notes")
SRC = ROOT / "workspace/ai-agent-platform-selection"
FIX = ROOT / "workspace/_citecheck_selftest"
CHECK = ROOT / ".codex/scripts/note-citation-check.py"
QUOTE = ("Everything runs in a single Python process served by uvicorn. There is no "
         "external queue (Redis, RabbitMQ, Celery), no separate worker process.")
APPENDIX = """
### 引文对照（原文 / 中译）

下表留档本章引文的逐字原文。

| # | 原文（逐字） | 中译 | 出处 |
| --- | --- | --- | --- |
| 1 | `%s` | 一切都跑在一个由 uvicorn 提供服务的 Python 进程里 | `SOUL.md` |
""" % QUOTE


def read(p):
    return p.read_bytes().decode("utf-8", errors="replace")


def put(p, t):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(t.encode("utf-8"))


def wipe():
    if not FIX.exists():
        return
    for q in sorted(FIX.rglob("*"), reverse=True):
        assert str(q).startswith(str(FIX)), q          # 前缀白名单，绝不越界
        q.rmdir() if q.is_dir() else q.unlink()


def build(ch_body, asm_body, merged_body):
    wipe()
    put(FIX / "chapters/05_x.md", ch_body)
    put(FIX / "chapters/_merged.md", merged_body)
    put(FIX / "output/final_note.md", asm_body)
    # 语料只放**原始来源**（不放项目自己的中间产物）
    put(FIX / "research/octop/docs/adr/001-single-process-model.md",
        "docs\n" + QUOTE + "\n")


def assemble(t):
    t = re.sub(r"(?m)^# 第 5 章", "## 第 5 章", t)
    t = re.sub(r"(?m)^### ", "#### ", t)
    return t + "\n## 相关文档\n\n- [[某文件]]\n"


def run(label, want_exit, want_in):
    r = subprocess.run([sys.executable, str(CHECK), str(FIX)], capture_output=True)
    out = (r.stdout + r.stderr).decode("utf-8", errors="replace")
    ok = (r.returncode == want_exit) and (want_in in out)
    print("%-30s exit=%d（期望 %d）  %s" % (label, r.returncode, want_exit,
                                            "PASS" if ok else "FAIL <<<"))
    if not ok:
        print("\n".join("      " + l for l in out.splitlines()[:45]))
    return ok


base = read(SRC / "chapters/05_Octop回答的是不是另一个问题.md").replace("\r\n", "\n")
allok = True

build(base, assemble(base), base)
allok &= run("A 基线（无缺陷）", 0, "无硬失败")

build(base, assemble(base), base.replace("uvicorn", "Uvicorn"))
allok &= run("B 合并件被改一个字母", 1, "发现 1 处差异")

build(base, assemble(base).replace("uvicorn", "gunicorn"), base)
allok &= run("C 组装件英文引文被改", 1, "未命中 1")

# D：出处列写成正文里列举的**产品文件名**——历史缺陷（ERR 记录过）的形态
withbad = base + APPENDIX
build(withbad, assemble(withbad), withbad)
allok &= run("D 出处列写了产品文件名", 1, "出处列非法")

wipe()
FIX.rmdir()
print("\n总判定：%s" % ("✅ 四个用例全部符合预期（门禁能红）" if allok
                        else "❌ 有用例不符合预期"))
print("清理：%s 已删除 = %s" % (FIX.name, not FIX.exists()))
sys.exit(0 if allok else 1)
