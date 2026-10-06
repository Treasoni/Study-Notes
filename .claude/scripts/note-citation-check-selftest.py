#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""`note-citation-check.py` 的负向自测：注入已知缺陷，断言门禁**确实会红**。

**一个从没红过的门禁不是门禁。**「跑出 0 处差异」既可能是真干净，也可能是没比到
东西——两种情形在报告里长得一模一样。所以校验器要自带一个自造 fixture 的自测，
每个用例只证明一件事，且必须证明它**因为该理由**而红。

用例（fixture 全部自己生成，不依赖任何真实项目）：

    A 基线（无缺陷）            → exit 0
    B 合并件被改一个字母         → exit 1，多副本比对报「发现 1 处差异」
    C 三份副本**同改**一处引文    → exit 1 且副本**零差异**，只有逐字回源能红
    D 出处列写了产品文件名        → exit 1，对照表结构报「出处列非法」
    E 引文只在**自己的中间产物**里 → exit 1，weak 按硬失败处理（ERR-20260929-013 那一族）
    F 同 E 但加 `--allow-weak`    → exit 0（显式降级确实有效）

C 与 E 是关键用例：B 红得靠副本漂移，C 把副本拉平后仍然红，才说明 V 不是摆设；
E 证明「中间件自己错了一手」这类**最隐蔽**的缺陷会被拦住，F 证明拦住它的方式
是显式开关而不是没人知道的隐式行为。

用法（在项目根目录）：

    python .claude/scripts/note-citation-check-selftest.py

fixture 落在 `workspace/_citecheck_selftest/`，跑完自删；删除走**前缀白名单 +
越界即断言失败**，不用 `rm -rf`。
"""
import pathlib
import re
import subprocess
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = pathlib.Path(__file__).resolve()
CHECK = HERE.with_name("note-citation-check.py")
FIX = pathlib.Path("workspace/_citecheck_selftest")
CORPUS_REL = "research/octop/docs/adr/001-single-process-model.md"
POINTER_MD = CORPUS_REL + ":14"
POINTER_PY = "research/octop/src/octop/infra/users/permissions.py:3-4"

SENT_A = ("Everything runs in a single Python process served by uvicorn. There is no "
          "external queue (Redis, RabbitMQ, Celery), no separate worker process.")
SENT_B = "Read access and agent use in chat are never gated."

CHAPTER = """# 第 5 章 测试章：逐字回源

本章只用来验证校验器能不能红。

Octop 的文档把进程模型说得很直白：`%(a)s`（`%(pmd)s`）

另一处硬边界：`%(b)s`（`%(ppy)s`）

## 5.1 小结

- 进程模型是单进程，没有独立 worker

## 引文对照（原文 / 中译）

下表留档本章引文的逐字原文。

| # | 原文（逐字） | 中译 | 出处 |
| --- | --- | --- | --- |
| 1 | `%(a)s` | 一切都跑在一个由 uvicorn 提供服务的 Python 进程里 | `%(pmd)s` |
| 2 | `%(b)s` | 聊天中的读取访问与 agent 使用从不设门禁 | `%(pmd)s` |
""" % {"a": SENT_A, "b": SENT_B, "pmd": POINTER_MD, "ppy": POINTER_PY}


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


def assemble(t):
    """模拟组装件相对章文件的合法装饰：标题整体下沉一级 + 文末追加 `## 相关文档`。"""
    t = re.sub(r"(?m)^(#+)", r"\1#", t)
    return t + "\n## 相关文档\n\n- [[某文件]]\n"


def build(corpus, derived="", chapter=CHAPTER):
    """corpus / derived：语料与「自己的中间产物」的内容；chapter：章文件正文。"""
    wipe()
    asm = assemble(chapter)
    put(FIX / "chapters/05_selftest.md", chapter)
    put(FIX / "chapters/_merged.md", chapter)
    put(FIX / "output/final_note.md", asm)
    if corpus:
        put(FIX / CORPUS_REL, "# ADR 001: single process model\n\n" + corpus + "\n")
    if derived:
        put(FIX / "02_deep_research.md", derived)


def run(label, want_exit, must_in=(), must_not=(), extra=()):
    cmd = [sys.executable, str(CHECK), str(FIX)] + list(extra)
    r = subprocess.run(cmd, capture_output=True)
    out = (r.stdout + r.stderr).decode("utf-8", errors="replace")
    ok = (r.returncode == want_exit
          and all(s in out for s in must_in)
          and not any(s in out for s in must_not))
    print("%-34s exit=%d（期望 %d）  %s" % (label, r.returncode, want_exit,
                                            "PASS" if ok else "FAIL <<<"))
    if not ok:
        print("\n".join("      " + l for l in out.splitlines()[:50]))
    return ok


def main():
    if not CHECK.is_file():
        print("找不到校验器：%s" % CHECK)
        return 2
    allok = True

    combo = SENT_A + "\n\n" + SENT_B

    # A 基线：两句引文都在原始语料里，两条出处指针都不该被当成引文 → 零硬失败。
    #     （指针回归就藏在这个用例里：漏掉 CITE_FULL / CITE_PATH 过滤，A 会立刻红。）
    build(combo)
    allok &= run("A 基线（无缺陷）", 0,
                 must_in=("判定：✅ 无硬失败", "未命中 0", "仅自己中间产物命中 0"),
                 must_not=("❌", "未命中按硬失败处理"))

    # B 只改合并件：副本漂移必须报出来（且只报这一处）。
    build(combo)
    put(FIX / "chapters/_merged.md", CHAPTER.replace("uvicorn", "Uvicorn"))
    allok &= run("B 合并件被改一个字母", 1, must_in=("发现 1 处差异", "❌"))

    # C 三份副本同改：副本全平，只剩逐字回源能红。
    build(combo)
    for rel in ("chapters/05_selftest.md", "chapters/_merged.md"):
        put(FIX / rel, CHAPTER.replace("uvicorn", "gunicorn"))
    put(FIX / "output/final_note.md",
        assemble(CHAPTER.replace("uvicorn", "gunicorn")))
    allok &= run("C 三份同改（只靠 V 红）", 1,
                 must_in=("发现 0 处差异", "未命中按硬失败处理", "❌"))

    # D 出处列写产品文件名——正文里出现过、但不是来源。历史缺陷形态。
    build(combo, chapter=CHAPTER.replace("| `%s` |" % POINTER_MD, "| `SOUL.md` |", 1))
    allok &= run("D 出处列写了产品文件名", 1,
                 must_in=("出处列非法", "发现 0 处差异", "❌"))

    # E 引文只在**自己的中间产物**里命中：语料拿掉 SENT_A，改放进 02_deep_research.md。
    #     这正是 ERR-20260929-013：中间件把来源的 `and argue that` 写成 `we argue that`，
    #     下游照抄；只查「有没有挂来源 ID」是查不出来的。
    build(SENT_B, derived=SENT_A)
    allok &= run("E 只在中间产物命中（weak）", 1,
                 must_in=("仅中间产物命中按硬失败处理", "❌"))

    # F 同 E，但显式降级：语料确实拿不到时，`--allow-weak` 是**说出来**的例外。
    build(SENT_B, derived=SENT_A)
    allok &= run("F 同 E + --allow-weak", 0,
                 must_in=("判定：✅ 无硬失败",),
                 must_not=("仅中间产物命中按硬失败处理",),
                 extra=("--allow-weak",))

    wipe()
    FIX.rmdir()
    print("\n总判定：%s" % ("✅ 六个用例全部符合预期（门禁能红）" if allok
                            else "❌ 有用例不符合预期"))
    print("清理：%s 已删除 = %s" % (FIX, not FIX.exists()))
    return 0 if allok else 1


if __name__ == "__main__":
    sys.exit(main())
