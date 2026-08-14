# DeepSeek-Harness 教程 · 更新计划（2026-08-14）

> 来源请求：/note-updater，依据官方文档两个页面新增内容：
> 1. https://deepseek-harness.github.io/deepseek-harness/develop/basic/ —— 开发基础：第一个插件
> 2. https://deepseek-harness.github.io/deepseek-harness/reference/subsystems/system-prompt —— system-prompt 子系统参考

## Stale Map

### 1. `AI学习/DeepSeek-Harness 教程/DeepSeek-Harness 配置体系.md`
| 操作 | 位置 | 内容 |
|---|---|---|
| 新增 | 3.8 | 插件开发基础：第一个插件（apply/ctx、cordis.yml 绝对路径、自动清理、inject、三种形态） |
| 新增 | 3.9 | system-prompt 子系统：PromptSection/order 约定/complete 语义/作用域遮蔽/事件 |
| 更新 | frontmatter `updated` | 2026-08-13 → 2026-08-14 |
| 更新 | 本章小结 | 追加进阶要点一行 |
| 追加 | 文末 | `## 更新记录` + 脚注 [^2][^3] |

### 2. `AI学习/DeepSeek-Harness 教程/DeepSeek-Harness 是什么.md`
| 操作 | 位置 | 内容 |
|---|---|---|
| 更新 | 1.2 | 「一切皆插件」补一句第一个插件开发入口（双链到配置体系 3.8） |
| 更新 | frontmatter `updated` | 2026-08-13 → 2026-08-14 |
| 追加 | 文末 | `## 更新记录` |

### 3. MOC 同步（描述行微调）
| 文件 | 位置 | 内容 |
|---|---|---|
| `DeepSeek-Harness MOC.md` | 03 配置体系 行 | 说明追加「插件开发、系统提示词组装」 |
| `AI学习/00-索引/AI学习 MOC.md` | DeepSeek-Harness 教程分区 | 配置体系行说明追加「插件开发、提示词组装」 |

## 不做的事
- 不重写未过时段落（1.1/1.3/1.4、2.x、3.1–3.7、4.x、5.x 保留）
- 不把 system-prompt 全文 API 堆进正文，只提炼教程读者需要的心智模型
- 不新增独立分册（保持 5 篇零散分册模式）

## 来源
- develop/basic：插件是什么、创建/注册（绝对路径）、自动清理、inject、三种形态、启动验证命令
- system-prompt：PromptSection（name/order/text/complete）、order 约定（-100 身份 / 0 人格 / 100–199 工具）、作用域遮蔽、变量插值、assemble/change 事件、knownNames、PromptContext 持久化
