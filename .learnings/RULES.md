# Rules

Compressed, deduplicated learnings from past Study System sessions.
Read before starting any new Study System task.

## Do

- 长篇笔记（>30KB 或多于 3 章）组装后主动建议拆分：独立章节文件 + 前后导航双链 + MOC 索引页
- Phase 4 beautify 前主动询问用户是否需要 Canvas/Base 配置
- GitHub 项目类主题，先通过 API 获取基本信息再进 Phase 0 提问
- 混合笔记 concept + cheat_sheet 适合"入门+速查"场景
- 工具对比/迁移类主题优先用 practice + compare 混合类型，每个领域同时提供步骤指南和对比表
- 每个学习笔记为核心概念添加 `[!tip] 大白话` 通俗解释 + 打比方类比（临时工牌 / 门禁卡 / 保险箱 / 双保险 / 岗位说明书 / 料理包 / 千层饼 等）；写作新笔记与 update 旧笔记时都补，用户偏好（3x）
- 教程类笔记「一章一节一文件」：顶级小节对应一个文件/产物；同一文件的字段（package.json 的 name/deps/files 等）收进该文件小节的 `####` 子节，不升格为顶级小节
- 教程代码块用文件头注释标注所属路径，并先展示完整文件（先睹为快）再逐段拆讲
- 用户报命令/路径错误时，先读源码核实路径解析基准与文件真实位置，一次改对再写入笔记；改完全文 grep 确认无残留旧表述
- 用户决策点用紧凑文本菜单 + 推荐默认值，不要用多问题 AskUserQuestion 对话框（用户会拒绝）
- 合并多篇独立章节前/后按章命名空间化脚注 ID（`[^cN-…]`），并 grep 校验无重复
- GitHub 项目取文档优先 `raw.githubusercontent.com/{owner}/{repo}/{branch}/...`；github.io 镜像可能 404
- perl 处理含中文文本必须 `use utf8;` + `use open ":std", ":encoding(UTF-8)"`，否则字符类正则静默 no-op

## Don't

- 不要把表格嵌套在列表项内（带缩进），Obsidian 无法渲染列表内的表格

## Domain

- GitHub Packages / GHCR 认证只支持 Classic PAT（`write:packages` 等 scope）；Fine-grained PAT 无 packages 权限项，遇到"expected scopes"报错先认 `github_pat_` 前缀换 classic

## Watch For

- YAML frontmatter 的 sources 字段中所有含特殊字符（`[]`, `:`）的值必须正确引用，否则 Obsidian 解析失败
- 并行派发 chapter-writer 时，章节过渡语必须自包含（按大纲），不要依赖读取上一章文件；todo-state.sh 完成阶段前先 `confirm PN` 再 `complete PN`
- note-assembler 等 writer 子 agent 无 Bash/Edit 且 Write 有输出上限；>100KB 长文档组装预判拆分，由父进程合并
- 并行子 agent 不得直接修改共享 workflow state file；状态推进由 orchestrator 集中经 todo-state.sh 处理
