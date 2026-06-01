## 1. 创建 docs/todo-state-machine.md 权威文档

- [x] 1.1 创建 `docs/todo-state-machine.md`，包含：状态定义、工具映射（Read/Write/Bash）、三种工作流变体（5-phase / 7-step / REFRESH mini）、路径约定
- [x] 1.2 在文件顶部添加"被引用文件列表"，标注所有引用此文档的文件

## 2. 精简 CLAUDE.md 中的 TODO.md 规则

- [x] 2.1 将 CLAUDE.md 中 TODO.md State Machine 部分（~10 行）替换为一行引用：`See docs/todo-state-machine.md`
- [x] 2.2 验证 CLAUDE.md 行数仍 ≤ 160

## 3. 精简 phases.md 中的 Phase Gate 重复

- [x] 3.1 将 phases.md 中 5 个 Phase Gate 指令（lines 127, 139, 152, 168, 180）替换为引用 `docs/todo-state-machine.md`
- [x] 3.2 将 phases.md 中 `rm TODO.md` 指令替换为引用

## 4. 精简 experience-notes.md 中的重复

- [x] 4.1 将 experience-notes.md 中 7 个 Phase Gate 指令替换为引用 `docs/todo-state-machine.md`
- [x] 4.2 将 experience-notes.md 中 `rm TODO.md` 指令替换为引用

## 5. 合并 update-workflow 与 updating-notes.md

- [x] 5.1 逐行对比 update-workflow/SKILL.md 与 docs/updating-notes.md，识别 30-40% 独特内容
- [x] 5.2 将 update-workflow/SKILL.md 精简为：意图检测 + 路由逻辑 + 引用 docs/updating-notes.md
- [x] 5.3 确保 docs/updating-notes.md 中的 REFRESH mini 循环引用 `docs/todo-state-machine.md`

## 6. Scoring rubric 单一来源

- [x] 6.1 将 collect/SKILL.md 中的 scoring rubric 替换为引用 collector.md
- [x] 6.2 将 phases.md 中 Phase 1 的 scoring rubric 替换为引用 collector.md

## 7. Skill 过滤机制

- [x] 7.1 在 `.study-config.yaml` 中添加 `skills.include` 和 `skills.exclude` 配置项（默认为空）
- [x] 7.2 在 CLAUDE.md 的 Resource Discovery 部分添加过滤步骤说明
- [x] 7.3 添加配置验证逻辑：启动时检查 exclude/include 中的名称是否匹配现有 skill，不匹配时输出警告

## 8. Agent 豁免块标注来源

- [x] 8.1 在 4 个 agent 定义（collector.md、writer.md、curator.md、beautifier.md）的全局指令豁免块中添加注释，标注共同来源
- [x] 8.2 确认 4 个文件的豁免内容一致

## 9. 验证与清理

- [x] 9.1 运行 `bash scripts/validate-structure.sh` 验证结构完整性
- [x] 9.2 检查所有引用路径是否正确（docs/todo-state-machine.md 被正确引用）
- [x] 9.3 验证 .study-config.yaml 新增字段格式正确
- [x] 9.4 验证 CLAUDE.md 行数 ≤ 160
