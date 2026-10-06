#!/usr/bin/env python3
"""把 chapters/ 的正文发布到 output/ 与 vault（本 run 专用，不是项目脚本）。

变换（保守式，逐字可验证）：
  既有发布件 = 文件头（frontmatter + 章首导航行） + "\\n\\n" + 旧正文 + GAP + "---\\n\\n" + 章末返回导航行
  新发布件   = 同一文件头（仅 title 可覆盖） + "\\n\\n" + 新正文 + 同一 GAP + "---\\n\\n" + 同一章末导航行

GAP 为每篇既有发布件自己的空白约定（社区实际产物里 01 是 "\\n"、02/06 是 ""），
从 `git show HEAD:chapters/<file>` 的旧正文反推，保证「只改正文、不动其他字节」。

入口页（总览）无 chapters 源，且 vault 副本比 output 副本新一句：
以 vault 为权威源，编辑后由 vault 同步回 output。

用法：
  python3 publish_copies.py --check [--only 01 02]
  python3 publish_copies.py --apply [--only 04] [--title 04 "新标题"]
"""
import argparse, os, re, subprocess, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
CH = os.path.join(ROOT, "workspace/xiaoya-fnos-deploy/chapters")
OUT = os.path.join(ROOT, "workspace/xiaoya-fnos-deploy/output")
VAULT = os.path.join(ROOT, "流媒体与影音/小雅 fnOS 单容器部署")
OVERVIEW = "小雅 fnOS 单容器部署（总览）.md"
SEP = "---\n\n"


def git_old_chapter(fn):
    try:
        r = subprocess.run(["git", "show", f"HEAD:workspace/xiaoya-fnos-deploy/chapters/{fn}"],
                           cwd=ROOT, capture_output=True, text=True, check=True)
        return r.stdout
    except Exception:
        return None


def split_tail(published):
    """返回 (head, middle, nav_foot, tail)：tail 为章末导航行之后的剩余字节（通常 "\\n"）。"""
    nav_head = next(l for l in published.split("\n") if l.startswith("> 📖"))
    h = published.index(nav_head) + len(nav_head)
    nav_foot = [l for l in published.split("\n") if l.startswith("> 📖")][-1]
    f = published.rindex(nav_foot)
    return published[:h], published[h:f], nav_foot, published[f + len(nav_foot):]


def rebuild(published, new_body, old_body, new_title=None):
    head, middle, nav_foot, tail = split_tail(published)
    if old_body is None:
        raise SystemExit("缺少旧正文，无法反推 GAP")
    gap = middle[2 + len(old_body.rstrip("\n")): -len(SEP)]
    out = head + "\n\n" + new_body.rstrip("\n") + gap + SEP + nav_foot + tail
    if new_title:
        out = re.sub(r"^title: .*$", f"title: {new_title}", out, count=1, flags=re.M)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--only", nargs="*", default=None)
    ap.add_argument("--title", nargs=2, action="append", default=[], metavar=("XX", "TITLE"))
    a = ap.parse_args()
    titles = dict(a.title)
    rc = 0
    for fn in sorted(os.listdir(CH)):
        if not fn.endswith(".md"):
            continue
        xx = fn.split("_")[0]
        if a.only and xx not in a.only:
            continue
        nm = fn.replace("_", " ")
        op, vp = os.path.join(OUT, nm), os.path.join(VAULT, nm)
        if not (os.path.exists(op) and os.path.exists(vp)):
            print(f"[skip] 缺发布件：{nm}")
            continue
        new_body = open(os.path.join(CH, fn), encoding="utf-8").read()
        old_body = git_old_chapter(fn)
        old_out = open(op, encoding="utf-8").read()
        new_out = rebuild(old_out, new_body, old_body, titles.get(xx))
        old_vault = open(vp, encoding="utf-8").read()
        new_vault = rebuild(old_vault, new_body, old_body, titles.get(xx))
        so, sv = new_out == old_out, new_vault == old_vault
        print(f"[{'OK ' if so else 'DIFF'}] {nm}  output={'=' if so else '≠'}  vault={'=' if sv else '≠'}")
        rc |= 0 if (so and sv) else 1
        if a.apply:
            open(op, "w", encoding="utf-8").write(new_out)
            open(vp, "w", encoding="utf-8").write(new_vault)
    return rc


if __name__ == "__main__":
    sys.exit(main())
