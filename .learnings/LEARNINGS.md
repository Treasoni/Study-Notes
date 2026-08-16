# LEARNINGS.md

## [LRN-20260816-004] knowledge_gap — 本机 perl 处理中文必须显式 utf8，否则字符类正则静默失败

**Logged**: 2026-08-16
**Priority**: high
**Status**: pending
**Area**: scripts

### Summary
Windows/Git Bash 下 python/python3 是商店存根不可用，用 perl 处理含中文 Markdown 时，字符类正则必须 `use utf8;` + `use open ":std", ":encoding(UTF-8)"`，否则按字节匹配导致脚本静默 no-op。

### Details
- 事实：第一次 perl 拆分脚本只加 `-CSD`，`[一二三四五六七]` 匹配不到，输出「无变化」且无报错；补 `use utf8;` 后才真正执行（8 段、74 defs、0 重复）。
- 根因：perl 默认把源码字面量当字节串，中文字符类不匹配 UTF-8 字节序列；且无报错，是静默失败。
- 下次做法：perl 处理非 ASCII 文本，脚本开头固定三件套：`use utf8;`、`use open ":std", ":encoding(UTF-8)"`、文件句柄加 `:encoding(UTF-8)`；先小样本验证匹配数>0。

### Suggested Action
- 需要文本处理脚本时优先考虑 perl/node；perl 处理中文必须带 utf8 三件套并先小样本验证。

---
