#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P1 更新清单扫描：只取轻量信息（frontmatter / 标题 / 目录 / 关键词命中 / 体积 / 路径）。

不读全文进上下文；命中行连同行号与整行原文写进清单，供 P2/P4 直接定位。
"""

import csv
import pathlib
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = pathlib.Path("D:/Study-Notes")
VOL = ROOT / "AI学习/Hermes Agent/Hermes × Home Assistant 实战"
WS = ROOT / "workspace/hermes-home-assistant"
OUTDIR = ROOT / "workspace/update-hermes-ha-volume"

# 待补正的错误结论族（本册的错误内容）
STALE = {
    "S1_hub没有现成": re.compile(r"Skills Hub 里没有现成的"),
    "S2_没有可装的东西": re.compile(r"没有可装的东西"),
    "S3_smarthome分类": re.compile(r"smart-home 分类"),
    "S4_openhue": re.compile(r"openhue"),
    "S5_haCLI不存在": re.compile(r"可以让\s*`?skill`?\s*去指挥|不存在一个可以让|并不存在这样一个|不存在可调的|不存在一个可调的"),
    "S6_hasscli": re.compile(r"hass-cli|hass_cli|homeassistant-cli", re.I),
    "S7_这条路不存在": re.compile(r"这条路(不成立|不存在)"),
    "S8_技能不是能力": re.compile(r"skill 不是能力"),
    "S9_装个现成": re.compile(r"装个现成|搜一个 HA skill|现成 HA skill"),
    "S10_HA没机器": re.compile(r"机器.{0,6}还没到货|缺的是机器|没有可装"),
}
# 补正所需锚点（判断该文件要不要动）
ANCHOR = {
    "A1_联邦Hub": re.compile(r"skills\.sh|ClawHub|LobeHub|browse\.sh|联邦|federation", re.I),
    "A2_中央索引": re.compile(r"skills\.json|中央索引|hub\s*index", re.I),
    "A3_openhue前置": re.compile(r"prerequisites|commands:"),
    "A4_hamcp组织": re.compile(r"homeassistant-ai"),
    "A5_本章来源": re.compile(r"^#{2,4}\s*本章来源", re.M),
    "A6_来源表": re.compile(r"HMS-05|COM-01|COM-23"),
}


# 显式覆盖：这两个文件不含错误结论，但有独立的小改动需求
OVERRIDE = {
    "10-附录-核对清单与延伸阅读.md": (
        "candidate", "P3", "无错误结论；附录 C 来源索引需补 Hub 中央索引一条"),
    "README.md": ("skip", "-", "无错误结论命中，导语未复述该结论（原方案列了它，扫描后撤销）"),
}


def frontmatter(text):
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end < 0:
        return {}
    fm = {}
    for line in text[3:end].splitlines():
        m = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", line)
        if m:
            fm[m.group(1)] = m.group(2).strip().strip('"').strip("'")
    return fm


def scan(p, rel):
    raw = p.read_bytes()
    text = raw.decode("utf-8")
    fm = frontmatter(text)
    lines = text.splitlines()
    h1 = next((l.lstrip("# ").strip() for l in lines if re.match(r"^#\s+\S", l)), "")
    heads = [l for l in lines if re.match(r"^#{2,3}\s+\S", l)]
    # 汉字数（不含代码块）
    body = re.sub(r"```.*?```", "", text, flags=re.S)
    hanzi = len(re.findall(r"[一-鿿]", body))

    hits = {}
    for name, pat in {**STALE, **ANCHOR}.items():
        found = [(i + 1, l.strip()) for i, l in enumerate(lines) if pat.search(l)]
        if found:
            hits[name] = found
    return {
        "rel": rel,
        "bytes": len(raw),
        "hanzi": hanzi,
        "title": fm.get("title") or h1,
        "created": fm.get("created", ""),
        "updated": fm.get("updated", ""),
        "status": fm.get("status", ""),
        "heading_count": len(heads),
        "hits": hits,
        "fences": text.count("```") // 2,
    }


def main():
    targets = [(p, p.name) for p in sorted(VOL.glob("*.md"))]
    targets += [
        (WS / "02_deep_research.md", "workspace/hermes-home-assistant/02_deep_research.md"),
        (WS / "01_explore_result.md", "workspace/hermes-home-assistant/01_explore_result.md"),
    ]

    rows = []
    for p, rel in targets:
        if not p.exists():
            print("!! 缺失：{}".format(p))
            continue
        rows.append(scan(p, rel))

    # 按是否命中错误结论 + 体积排序
    def stale_n(r):
        return sum(len(v) for k, v in r["hits"].items() if k.startswith("S"))

    rows.sort(key=lambda r: (-stale_n(r), r["rel"]))

    print("== 扫描 {} 个文件 ==".format(len(rows)))
    for r in rows:
        sn = stale_n(r)
        print("\n[{}] {} B / {} 汉字 / {} 个二级三级标题 / {} 代码块".format(
            r["rel"], r["bytes"], r["hanzi"], r["heading_count"], r["fences"]))
        print("   title={!r} created={} updated={} status={}".format(
            r["title"], r["created"], r["updated"], r["status"]))
        print("   错误结论命中 {} 处：{}".format(
            sn, ", ".join("{}×{}".format(k, len(v)) for k, v in sorted(r["hits"].items())
                          if k.startswith("S")) or "无"))
        for k in sorted(r["hits"]):
            if k.startswith("S"):
                for ln, txt in r["hits"][k]:
                    print("      L{:<5} {:<18} {}".format(ln, k, txt[:110]))
        print("   锚点：{}".format(", ".join(
            "{}×{}".format(k, len(v)) for k, v in sorted(r["hits"].items())
            if k.startswith("A")) or "无"))

    # CSV
    csv_path = OUTDIR / "update_inventory.csv"
    with csv_path.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["id", "relative_path", "title", "updated", "status", "reason",
                    "priority", "size_bytes"])
        for i, r in enumerate(rows, 1):
            sn = stale_n(r)
            if r["rel"] in OVERRIDE:
                st, pri, reason = OVERRIDE[r["rel"]]
            elif sn >= 1:
                st = "ready"
                pri = "P1" if sn >= 3 else "P2"   # 命中越多越靠前
                reason = "命中错误结论 {} 处".format(sn)
            else:
                st, pri, reason = "skip", "-", "无错误结论命中"
            w.writerow(["N{:02d}".format(i), r["rel"], r["title"], r["updated"],
                        st, reason, pri, r["bytes"]])
    print("\n已写出 {}".format(csv_path))


if __name__ == "__main__":
    main()
