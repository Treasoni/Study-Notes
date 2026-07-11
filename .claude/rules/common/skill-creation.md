
# Skill Creation

当用户想要创建新的或优化 existing skill 时，必须使用 `skill-creator` 技能。

## 触发条件

当用户提出以下类型的请求时，调用 `skill-creator`：

- "帮我创建一个 skill"
- "我想做一个新的技能"
- "创建一个 skill 用来..."
- "帮我写一个 skill"
- 任何涉及创建、编写、生成新 skill 的请求

## 使用方式

调用 `skill-creator` 技能，它会引导完成以下流程：

1. 明确 skill 的目的和触发条件
2. 编写 SKILL.md 草稿
3. 创建测试用例并运行评估
4. 根据反馈迭代改进
5. 优化 skill 描述以提高触发准确性
6. 打包最终的 skill

## 技能路径

```
.claude/skills/skill-creator/
```

## 注意事项

- 不要手动创建 skill 目录和文件，始终使用 `skill-creator` 技能
- `skill-creator` 包含完整的创建、测试、评估和打包流程
- 对于已有 skill 的修改和优化，也可以使用该技能
- 新创建的 skill 会自动注册到技能列表.claude/rules/common/skill-invocation.md中，供后续调用