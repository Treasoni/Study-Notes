---
name: moc-organizer
description: 为 Obsidian 生成或更新 MOC（Map of Content）目录笔记。用于用户要求“生成 MOC”“整理目录”“把新笔记加入目录”“每次加入笔记自动更新索引”等场景。只维护索引、分组、双链和简短说明，不复制正文。
category: Obsidian 相关
---

# MOC Organizer

维护 Obsidian MOC 目录笔记。

## Inputs

优先从用户或 `00_intent.md`/发布配置中确认：

- `vault_path`: Obsidian vault 根目录
- `moc_path`: MOC 文件路径
- `note_path`: 新增或更新的笔记路径
- `topic`: 主题
- `tags`: 标签
- `summary`: 一句话说明

## Workflow

1. **定位 MOC**
   - 如果 `moc_path` 存在，读取标题和现有分组。
   - 如果不存在，创建最小 MOC 模板。
2. **生成索引项**
   - 格式：`- [[笔记标题]] - 一句话说明 #tag`
   - 只保留 1 行，不复制正文。
3. **去重更新**
   - 如果已存在同名双链，更新摘要/标签，不重复追加。
4. **分组**
   - 优先按主题或学习阶段分组。
   - 不确定时放入 `## Inbox`。
5. **验证**
   - 检查双链标题与笔记文件名一致。
   - 检查 MOC 没有长段落堆积。

## Minimal MOC Template

```markdown
---
type: moc
status: active
updated: {date}
---

# {topic} MOC

## Inbox

- [[{note_title}]] - {summary} {tags}
```

## Automation Boundary

“自动执行”在本项目中指：每次阶段 6 发布或更新笔记后，工作流必须调用本 skill 同步 MOC。不要依赖全局 Claude Code 配置。
