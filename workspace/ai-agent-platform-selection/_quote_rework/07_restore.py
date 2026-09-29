# -*- coding: utf-8 -*-
"""从 pristine/ 回滚：把 11 个目标文件按原名写回原路径。

为什么要有这个脚本，而不是手敲 `cp`：pristine 里的文件名和目标的文件名一一
对应，但**映射关系只存在于本文件与 05_apply.py 共用的 core.TARGETS 里**。
手敲很容易把某个分章文件漏掉，或者漏掉 03_outline.md，留下一半改过、一半没改
的混合状态——那是最难查的。跑完打印每个文件的行尾与字节数，和 README.txt 对照。

用法：python 07_restore.py        （不带参数；不接受只回滚单个文件）
"""
import pathlib
import shutil
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import rework_core as core

targets = core.TARGETS + [(p, "title_only") for p in core.TITLE_ONLY]
missing = [p.name for p, _k in targets if not (core.PRISTINE / p.name).exists()]
if missing:
    print("pristine 里缺这些文件，拒绝回滚（回滚不完整比不回滚更危险）：")
    for n in missing:
        print("  - %s" % n)
    sys.exit(1)

for path, kind in targets:
    raw = (core.PRISTINE / path.name).read_bytes()
    path.write_bytes(raw)
    eol = "CRLF" if b"\r\n" in raw else "LF"
    dirty = "（仍含附录，未回滚干净！）" if core.APPENDIX_TITLE in raw.decode("utf-8") else ""
    print("  %-44s %-4s %7d bytes %s %s" % (path.name, eol, len(raw), kind, dirty))
print("回滚完成：%d 个文件。" % len(targets))
