# Rules

Compressed, deduplicated learnings from past Study System sessions.
Read before starting any new Study System task.

## Do

- 资料收集时 defuddle 失败则回退到 WebFetch
- WebFetch 对返回 403 的站点（如 machinelearningmastery.com）也能获取部分内容

## Don't

- 不要硬编码 obsidian-cli 命令 —— 用户可能未启用 CLI
- 不要假设 defuddle 命令存在

## Watch For

- obsidian-cli 返回 "command line interface is not enabled" → 直接写入文件，跳过 CLI
- 收集阶段部分站点 403 → 用 WebFetch 替代
- defuddle exit 127 → 命令未安装，改用 WebFetch
