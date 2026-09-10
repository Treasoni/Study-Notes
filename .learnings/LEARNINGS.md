# LEARNINGS.md

最近一次维护：2026-09-11（`/maintain-learnings`）。已源头修复的条目移入
`.learnings/archive/`，其中 `LRN-20260911-008`（`todo-state.sh` 命令集与
`quality_gate`）、`LRN-20260911-010`（双链目标与锚点校验）已落到
workflow state template、`workflow-health-check.sh` 与 `note-beautifier`；
`LRN-20260905-007` 经核实已在 `chapter-writer.md` 落地。

## [LRN-20260911-009] best_practice — 超大笔记的组装/校验在父进程用 python 做，别指望子 agent 写入

**Logged**: 2026-09-11
**Priority**: medium
**Status**: pending
**Area**: workflow / 学习笔记生产

### Summary
本次成品 43k 汉字 / 228KB，note-assembler 直接拒写。父进程用 python 合并 + 校验可一次做对；但**反向扫描定位插入点时必须同时跳过空行和 `---` 分隔线**，否则扫描停错位置、改动静默不生效。

### Details
- 事实：组装脚本要「把每章末尾的过渡句从『本章来源对照』表格之前移到表格之后」。第一版从 `### 本章来源对照` 反向扫描找第一个非空行，结果撞上 `---` 分隔线，判定「无事可做」，4 条过渡句 0 条被移动且无报错；改为跳过空行 + `---` 后 4 条全部移动。
- 事实：中文字数统计用 `grep -o '[一-龥]' | wc -l` 在 C locale 下按字节匹配，给出 34,855 这类明显失真的数字；改用 `python3 -c "re.findall(r'[一-鿿]', t)"` 才准。
- 根因：反向扫描的终止条件写得太窄；`grep` 的字符类在 C locale 下按字节解释。
- 下次做法：文本组装/统计一律走 python；任何「扫描到某标记就动手」的脚本，先打印「本次改动 N 处」并在 N=0 时人工复核，不要静默通过。

### Suggested Action
- 把「改动计数 + N=0 需复核」作为所有批量文本改写脚本的固定自检项。

---
