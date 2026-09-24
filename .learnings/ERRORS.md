# ERRORS.md

活跃错误记录。**当前无活跃记录** —— 最近一次维护：2026-09-23（`/maintain-learnings`）。

本轮归档三条 2026-09-23 错误记录，均在源头修复：

- `note-assembler：章标题降级未级联到子标题` → Step 4 改为「子树下沉 + 重新解析标题树断言层级」
- `todo-state.sh：workflow 定义调用了未实现的动作` → 脚本补齐 `mode`/`confirm`，并新增探针式动作守卫
- `chapter-writer：官方引文被串成 828 字符引文墙` → 写作规范新增引文摆放阈值与反例边界

原文摘要、修复路径与验证方式见 `.learnings/archive/2026-09-23-maintenance.md`。
更早的 `ERR-20260911-007`（父 agent 转述来源论断导致伪引证）见
`.learnings/archive/2026-09-11-maintenance.md`。

新增错误请按 `digest` 的格式追加到本文件末尾（错误 / 触发场景 / 根因 / 修复 / 预防措施）；
修复落到机制并验证通过后，才可移入 `.learnings/archive/`。

---