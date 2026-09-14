"""P7 校验：Docker MOC 里 MusicTagWeb 索引项是否合规。

检查项：
  1. 总目录双链在 MOC 中出现次数（快速导航 1 + 系列节 1 + 更新日志 1 = 3，允许）
  2. 系列节里的索引行是否只有 1 行、不复制正文
  3. 所有 wikilink 目标在 vault 内真实存在
  4. 新增段落没有把表格嵌进列表项
"""
import re, sys, pathlib

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

MOC = pathlib.Path("docker/Docker MOC.md")
TOC = "MusicTagWeb-00-总目录"
SKIP = (".git", ".obsidian", ".claude", ".codex", ".agents", "workspace", ".smart-env", ".llm")

t = MOC.read_text(encoding="utf-8")
lines = t.splitlines()

print("=== 1. 总目录双链出现位置 ===")
for i, ln in enumerate(lines, 1):
    if TOC in ln:
        print("  L%-4d %s" % (i, ln[:110]))

print("\n=== 2. 系列节块 ===")
start = next(i for i, ln in enumerate(lines) if ln.strip() == "### 音乐标签与整理")
blk = []
for ln in lines[start + 1:]:
    if ln.startswith("###") or ln.startswith("## "):
        break
    blk.append(ln)
body = [b for b in blk if b.strip()]
print("  行数 %d（含空行 %d）" % (len(body), len(blk)))
for b in body:
    print("  %s" % b[:160])
print("  每行都 <= 1 条索引：%s" % ("OK" if all(b.startswith("- ") for b in body) else "!!"))
print("  无多段正文：%s" % ("OK" if len(body) <= 2 else "!! 行数偏多"))

print("\n=== 3. wikilink 目标存在性 ===")
vault_md = {p.stem for p in pathlib.Path(".").rglob("*.md")
            if not any(s in p.parts for s in SKIP)}
missing = []
for i, ln in enumerate(lines, 1):
    for tgt in re.findall(r"\[\[([^\]|#]+)", ln):
        if tgt.strip().rstrip(".md") not in vault_md:
            missing.append((i, tgt))
print("  死链：%s" % (sorted(set(missing)) or "无"))

print("\n=== 4. 结构与去重 ===")
dup = [x for x in set(re.findall(r"\[\[([^\]|#]+)", t)) if
       len([1 for ln in lines if ln.strip().startswith("- ") and "[[%s]]" % x in ln]) > 1]
print("  同一目标在索引行里重复出现：%s" % (sorted(dup) or "无"))
print("  行内表格缩进（列表内表格风险）：%s"
      % ("OK" if not any(re.match(r"^\s+[|]", ln) for ln in lines) else "!!"))
print("  总行数 %d（原 171，新增 %+d）" % (len(lines), len(lines) - 171))
