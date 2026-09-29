# -*- coding: utf-8 -*-
"""重数成品的体积/字数/锚点/附录行数（写进 workflow state file 的数字必须现算）。"""
import pathlib
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import rework_core as core

p = core.VAULT_NOTE
raw = p.read_bytes()
t = raw.decode("utf-8").replace("\r\n", "\n")
lines = t.split("\n")
print("vault note :", len(lines), "lines |", len(raw), "bytes |",
      "CRLF" if b"\r\n" in raw else "LF")
print("汉字      :", len(re.findall(r"[一-鿿]", t)))
print("research 锚点:", len(re.findall(r"research/[^\s`)|]+:\d", t)))
print("附录标题  :", t.count(core.APPENDIX_TITLE), "| callout:", t.count(core.CALLOUT[0]))

rows = 0
for l in lines:
    if l.startswith("| ") and re.match(r"^\|\s*\d+\s*\|", l) and "`" in l:
        cells = l.split("|")
        if len(cells) == 6 and cells[4].strip():
            rows += 1
print("附录数据行:", rows)

for path, kind in core.TARGETS:
    r = path.read_bytes()
    print("  %-42s %-9s %s" % (path.name, kind,
                               "CRLF" if b"\r\n" in r else "LF"), len(r), "bytes")
