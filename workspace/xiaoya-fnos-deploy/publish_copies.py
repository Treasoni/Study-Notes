#!/usr/bin/env python3
"""把 chapters/ 的正文发布到 output/ 与 vault（本 run 专用，不是项目脚本）。

结构（实测）：
  发布件 = [文件头: frontmatter + 章首导航行] + "\\n\\n" + 正文 + TAILWS + "---\\n\\n" + 章末返回导航行 + 尾

正文区、TAILWS（正文与 --- 之间的空白）都**从发布件自身推导**，不查 git、不假设 GAP 值，
因此对任何既有发布件都逐字保真：未改动篇重算后必须与原文逐字节相同。

用法：
  python3 publish_copies.py --check [--only 01 02]
  python3 publish_copies.py --apply [--only 04] [--title 04 "新标题"]
"""
import argparse, os, re, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
CH = os.path.join(ROOT, "workspace/xiaoya-fnos-deploy/chapters")
OUT = os.path.join(ROOT, "workspace/xiaoya-fnos-deploy/output")
VAULT = os.path.join(ROOT, "流媒体与影音/小雅 fnOS 单容器部署")
SEP = "---\n\n"


def rebuild(published, new_body, new_title=None):
    navs = [l for l in published.split("\n") if l.startswith("> 📖")]
    if not navs:
        raise SystemExit("发布件缺少章首/章末导航行")
    nav_head, nav_foot = navs[0], navs[-1]
    h = published.index(nav_head) + len(nav_head)
    f = published.rindex(nav_foot)
    before = published[:f]
    if not before.endswith(SEP):
        raise SystemExit(f"章末导航行前不是 {SEP!r}，拒绝改写")
    region = before[h:-len(SEP)]                 # "\n\n" + 旧正文 + TAILWS
    tailws = region[len(region.rstrip()):]       # 正文与 --- 之间的空白，原样保留
    out = published[:h] + "\n\n" + new_body.rstrip("\n") + tailws + SEP + published[f:]
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
        old_out = open(op, encoding="utf-8").read()
        old_vault = open(vp, encoding="utf-8").read()
        new_out = rebuild(old_out, new_body, titles.get(xx))
        new_vault = rebuild(old_vault, new_body, titles.get(xx))
        so, sv = new_out == old_out, new_vault == old_vault
        print(f"[{'OK ' if so else 'DIFF'}] {nm}  output={'=' if so else '≠'}  vault={'=' if sv else '≠'}")
        rc |= 0 if (so and sv) else 1
        if a.apply:
            open(op, "w", encoding="utf-8").write(new_out)
            open(vp, "w", encoding="utf-8").write(new_vault)
    return rc


if __name__ == "__main__":
    sys.exit(main())
