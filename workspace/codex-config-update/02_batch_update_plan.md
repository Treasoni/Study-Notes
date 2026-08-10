# 批量更新计划 - Codex 笔记重构为 Claude Code 教程风格

> 工作流：batch-note-update-flow
> 运行标识：update-codex-config
> 项目标识：codex-config-update
> 创建时间：2026-08-10

## 1. 更新目标与判断依据

- **目标**：将 `AI学习/Codex/` 从"8 章 + 附录 + MOC"扁平结构重构为镜像 `AI学习/Claude Code 教程/` 的子目录结构（`01-入门` / `02-基础功能` / `03-进阶应用` / `04-高级功能`），每篇按 Claude Code 教程模板完整重排。
- **判断依据**：用户明确选择"完整套用模板"（非轻量美化）；9 篇正文内容保留，仅重排结构与增补区块。
- **模板镜像**：`Claude Code 教程/02-基础功能/settings.json 配置详解.md` 与 `03-进阶应用/Claude Code Hooks 使用指南.md` 的区块顺序：frontmatter → 标题 → `> [!info] 文档定位` → 主体分节（`##`/`###` + `---` 分隔）→ 常见问题 → 最佳实践 → 小结 → 相关文档（wikilink）→ 参考资料 → 更新记录。

## 2. 分组（按目标层级）

### 组 01 入门
| 笔记 ID | 动作 | 说明 |
|---------|------|------|
| cdx01 | update | 配置哲学概览，重排套模板 |

### 组 02 基础功能
| 笔记 ID | 动作 | 说明 |
|---------|------|------|
| cdx02 | update | config.toml 核心配置，重排套模板 |
| cdx07 | update | CLI 与调试，重排套模板 |

### 组 03 进阶应用
| 笔记 ID | 动作 | 说明 |
|---------|------|------|
| cdx03 | update | AGENTS.md 分层体系，重排套模板 |
| cdx04 | update | Skills 技能系统，重排套模板 |
| cdx05 | update | Agents 与 MCP，重排套模板 |
| cdx06 | update | Hooks 与插件，重排套模板 |

### 组 04 高级功能
| 笔记 ID | 动作 | 说明 |
|---------|------|------|
| cdx08 | update | 对照表与迁移实战，重排套模板 |
| cdx09 | update | 快速参考卡片，重排套模板 |

### MOC
| 笔记 ID | 动作 | 说明 |
|---------|------|------|
| cdx10 | update | 重命名 `Codex 配置体系 MOC.md` → `Codex MOC.md` 并按 Claude Code MOC 模板重写（P5 阶段执行） |

## 3. 移动 / 改名映射

| 笔记 ID | 旧路径 | 新路径 |
|---------|--------|--------|
| cdx01 | `AI学习/Codex/01 配置哲学概览.md` | `AI学习/Codex/01-入门/Codex 配置哲学概览.md` |
| cdx02 | `AI学习/Codex/02 config.toml 核心配置.md` | `AI学习/Codex/02-基础功能/config.toml 核心配置.md` |
| cdx03 | `AI学习/Codex/03 AGENTS.md 分层体系.md` | `AI学习/Codex/03-进阶应用/AGENTS.md 分层体系.md` |
| cdx04 | `AI学习/Codex/04 Skills 技能系统.md` | `AI学习/Codex/03-进阶应用/Skills 技能系统.md` |
| cdx05 | `AI学习/Codex/05 Agents 与 MCP.md` | `AI学习/Codex/03-进阶应用/Agents 与 MCP.md` |
| cdx06 | `AI学习/Codex/06 Hooks 与插件.md` | `AI学习/Codex/03-进阶应用/Hooks 与插件.md` |
| cdx07 | `AI学习/Codex/07 CLI 与调试.md` | `AI学习/Codex/02-基础功能/Codex CLI 与调试.md` |
| cdx08 | `AI学习/Codex/08 对照表与迁移实战.md` | `AI学习/Codex/04-高级功能/对照表与迁移实战.md` |
| cdx09 | `AI学习/Codex/附录 快速参考卡片.md` | `AI学习/Codex/04-高级功能/快速参考卡片.md` |
| cdx10 | `AI学习/Codex/Codex 配置体系 MOC.md` | `AI学习/Codex/Codex MOC.md` |

## 4. 共享资料包

- **shared_research: no**（纯排版重构，无新资料需求）。跳过 P3。

## 5. 批次编排（batch_size = 3）

| 批次 | 笔记 ID | 说明 |
|------|---------|------|
| 批次 1 | cdx01, cdx02, cdx03 | 入门 + 基础核心 + 进阶第一组 |
| 批次 2 | cdx04, cdx05, cdx06 | 进阶应用续 |
| 批次 3 | cdx07, cdx08, cdx09 | 基础 CLI + 高级对照/速查 |
| P5 阶段 | cdx10 | MOC 重写 + sortspec + 索引更新 |

## 6. 目标输出模式与覆盖风险

- **destination_mode: `patch-in-place`**：直接写入 vault 新路径，就地重构。
- **覆盖风险**：
  1. 原 10 个 flat 文件在 P4 阶段**暂不删除**，待 P5 用户确认后移除（避免中途失败丢数据）。
  2. `AI学习/Codex/sortspec.md` 为新建文件，无覆盖风险。
  3. `AI学习/00-索引/AI学习 MOC.md` 中 10 处旧 wikilink 需在 P5 更新，若遗漏会导致悬空链接。
  4. 新文件名的 wikilink 引用必须全文一致（含每篇的「相关文档」区块与旧「导航」区块）。
- **同名目标文件冲突**：新路径子目录当前不存在，无同名文件冲突。

## 7. 需用户确认项

- [ ] 确认批次分组与移动/改名映射无误
- [ ] 确认 `patch-in-place` 直接写入 vault 新路径
- [ ] 确认 P4 后旧 flat 文件保留、P5 用户确认后再删除
