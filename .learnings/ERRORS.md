# ERRORS.md

## [2026-06-01] OpenSpec 学习笔记 - Session Errors

### 问题记录
- 无重大错误。WebFetch 无法访问 github.com，需改用 GitHub API 替代方案

## [2026-07-11] Codex 手动配置指南 - Session Errors

### 问题记录
- beautify 阶段 YAML frontmatter 中 `sources` 字段的 `[来源: doc-XX]` 标记未正确引用，导致 Obsidian 解析失败。修复方法：将整个值用双引号包裹，或改用纯字符串列表格式。教训：YAML frontmatter 中所有含特殊字符（`[]`, `:`）的值都必须正确引用
