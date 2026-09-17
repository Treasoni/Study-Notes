#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""从 Hermes Skills Hub 的中央索引里抽出与 Home Assistant 相关的 skill。

为什么需要这一步：HMS-05（features/skills.md）写明 Hub 的搜索由一份**联邦索引**回答，
索引覆盖外部注册表（skills.sh / ClawHub / LobeHub / browse-sh），而不只是 Hermes 仓库内的
official optional skills。分册第 1、3 章的「Skills Hub 里没有现成的 HA skill」只查了 official
那一支，因此需要回到这份索引本身核对。

索引：https://nousresearch.github.io/hermes-agent/docs/api/skills.json（约 60 MB 单行 JSON）
用法：curl 下到 _hub_index.json 后运行本脚本；脚本只保留抽出的记录，随后可删索引大文件。
"""

import json
import re
import sys
import pathlib

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

HERE = pathlib.Path(__file__).resolve().parent
INDEX = HERE / "sources" / "_hub_index.json"
OUT = HERE / "sources" / "HUB-homeassistant-skills.json"
INDEX_URL = "https://nousresearch.github.io/hermes-agent/docs/api/skills.json"

# 明确指向 Home Assistant 的词（含常见误写）
HA_EXPLICIT = re.compile(r"home[\s\-_]?assistant|\bhass\b|\bhomeassistant\b", re.I)


def blob(rec):
    parts = [
        str(rec.get("name", "")),
        str(rec.get("description", "")),
        str(rec.get("overview", "")),
        str(rec.get("identifier", "")),
        str(rec.get("installIdentifier", "")),
        " ".join(rec.get("tags", []) or []),
    ]
    return " ".join(parts)


def main():
    recs = json.loads(INDEX.read_text(encoding="utf-8"))
    print("索引条目总数：{}".format(len(recs)))

    by_source = {}
    for r in recs:
        by_source[r.get("source", "?")] = by_source.get(r.get("source", "?"), 0) + 1
    print("按 source 分布：")
    for k, v in sorted(by_source.items(), key=lambda kv: -kv[1]):
        print("  {:<12} {}".format(k, v))

    tier_a = [r for r in recs if HA_EXPLICIT.search(blob(r))]
    tier_b = [r for r in recs
              if r.get("category") == "smart-home" and r not in tier_a]

    print()
    print("== A 类：明确提到 Home Assistant（{} 条） ==".format(len(tier_a)))
    for r in sorted(tier_a, key=lambda x: (x.get("source", ""), x.get("name", ""))):
        print("  [{}] {}".format(r.get("source", "?"), r.get("name", "")))
        print("      {}".format((r.get("description") or "")[:150]))
        print("      install: {}".format(r.get("installCmd", "")))

    print()
    print("== B 类：smart-home 分类下、未点名 HA（{} 条） ==".format(len(tier_b)))
    for r in sorted(tier_b, key=lambda x: (x.get("source", ""), x.get("name", ""))):
        print("  [{}] {}".format(r.get("source", "?"), r.get("name", "")))

    OUT.write_text(json.dumps({
        "source_index": INDEX_URL,
        "note": "由 extract_hub_ha.py 从中央索引抽取；索引为 60MB 单行 JSON，未随本文件保留。",
        "total_index_records": len(recs),
        "source_distribution": by_source,
        "home_assistant_explicit": tier_a,
        "smart_home_category_other": [
            {k: r.get(k) for k in ("name", "source", "identifier", "installCmd",
                                   "tags", "description")}
            for r in tier_b
        ],
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print()
    print("已写出 {} （{} B）".format(OUT.name, OUT.stat().st_size))


if __name__ == "__main__":
    main()
