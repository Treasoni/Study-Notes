# Rules

Compressed, deduplicated learnings from past Study System sessions.
Read before starting any new Study System task.

## Do

- 资料收集时 defuddle 失败则回退到 WebFetch
- beautify 阶段用 Glob 验证双链目标是否存在，避免悬空链接 (3x)
- 用户直接提供完整内容时跳过 collect/curate，直接 write
- 入门级笔记增加渐进式示例提升实用性

## Don't

- 不要硬编码 obsidian-cli 命令 —— 用户可能未启用 CLI
- 不要假设 defuddle 命令存在

## Watch For

- obsidian-cli 返回 "command line interface is not enabled" → 直接写入文件，跳过 CLI
- 收集阶段部分站点 403 → 用 WebFetch 替代
- defuddle exit 127 → 命令未安装，改用 WebFetch
- Phase 2 后用户可能要求补充特定缺口 → 主动询问是否需要补充
- AskUserQuestion 对自由文本输入不够高效 → 用纯文字对话替代
