# 批量更新汇总报告（run: update-xiaoya-fnos-alist）

对应 `02_batch_update_plan.md` 与 `03_batch_update_log.md`。本文件是 P5 的收口件。

| 项 | 值 |
| --- | --- |
| workflow_id | `batch-note-update-flow` |
| run_id | `update-xiaoya-fnos-alist` |
| project_slug | `xiaoya-fnos-deploy` |
| 主题 | 小雅 fnOS 单容器部署笔记集：monlor 路线 → `xiaoyaDev/xiaoya-alist`（DDSRem）整合脚本路线 |
| 输出模式 | **patch-in-place**（`updated_note` 即 `chapters/{file}`） |
| 完成日期 | 2026-10-07 |
| 最终判定 | ✅ 全部完成，引文校验无硬失败 |

## 1. 数量汇总

| 指标 | 数量 | 说明 |
| --- | --- | --- |
| 范围内笔记 | **8** | 7 章（`chapters/01..07`）+ 总览（`output/…（总览）.md`，**不在 `chapters/`**） |
| 更新 | **8** | 全部 update，无 skip |
| 跳过 | 0 | — |
| 失败 | 0 | — |
| 需复核 | 0 | 各章遗留项均已在 `updates/*/update_report.md` 逐条记录，无阻塞项 |
| 引文对照表扩编 | 4 章 | ch01 8→13、ch02 17→28、ch05 23/24/28 行换源、ch06 12→22 |

## 2. 每篇输出路径与风险

| # | note_id | 源（=输出） | 发布副本 | 动作 | 主要风险 / 取舍 |
| --- | --- | --- | --- | --- | --- |
| 1 | ch01 | `chapters/01_开篇定位.md` | `output/01 开篇定位.md`、vault 同名 | update | 术语校正：**官方 = `xiaoyaliu/alist`**；整合脚本为非官方社区脚本（author DDSRem） |
| 2 | ch02 | `chapters/02_选型对比.md` | `output/02 选型对比.md`、vault 同名 | update | §2.3.3 硬解结论**反转**（旧「不支持硬解」作废）；§2.4 撤回 monlor 硬件数字（**有意不给 CPU/内存数**） |
| 3 | ch03 | `chapters/03_动手前准备.md` | `output/03 动手前准备.md`、vault 同名 | update | 端口口径反转（容器内 `80` / 宿主 `5678`）；凭据注入方式由 env 改为菜单 |
| 4 | ch04 | `chapters/04_部署实战.md` | `output/04 部署实战.md`、vault 同名 | update（重写） | 两张 monlor 界面截图经 Obsidian 回收站删除；主线改一键脚本 |
| 5 | ch05 | `chapters/05_前端接入.md` | `output/05 前端接入.md`、vault 同名 | update（轻） | 5.6 三处限速/转存论据换源；前端工具链（SmartStrm / MediaWarp / fntv-proxy）**未动** |
| 6 | ch06 | `chapters/06_避坑清单.md` | `output/06 避坑清单.md`、vault 同名 | update（轻） | 6.2 清理口径分两处；新增 6.5 坑五（WebDAV 端口/用户名）；**章名扩为「…、UA 与登录」** |
| 7 | ch07 | `chapters/07_运维与收尾.md` | `output/07 运维与收尾.md`、vault 同名 | update | 转存缓存清理口径换源（小雅助手 / 115清理助手） |
| 8 | overview | `output/小雅 fnOS 单容器部署（总览）.md` | vault 同名（**两处手改**） | update | 章节目录第 4、6 条与读前须知换源；`updated` → 2026-10-07 |

## 3. 主线换源的核心改动（跨章）

- **部署形态**：monlor 社区镜像（`ghcr.io/monlor/xiaoya-alist`，项目 `monlor/docker-xiaoya`，最后提交 2025-03-27）→ **`xiaoyaDev/xiaoya-alist` 一键菜单脚本**（DDSRem 社区整合脚本，内部使用官方镜像 `xiaoyaliu/alist`）。
- **术语边界**：`xiaoyaDev/xiaoya-alist` 是**社区整合脚本，不是官方**；「官方」仅指镜像 `xiaoyaliu/alist`（内容源 `alist.xiaoya.pro`）。monlor 仅出现在整合脚本 README 的「小雅周边工具集合」中。
- **诚实用例（撤回而非改写）**：凡只有 monlor 一处来源支撑的结论，一律从正文撤回并记入更新记录——ch02 §2.4 硬件门槛表、ch02 §2.3.3 硬解结论、ch05 §5.6 限速论据、ch06 §6.2 清理口径。

## 4. 验收规则核对（plan §2.6）

规则：正文残留 `rg monlor` 应为空，仅允许出现在**更新记录**与 `sources/`。

对 vault 成品全量扫描（`rg -n "monlor" 流媒体与影音/小雅 fnOS 单容器部署/`）结果：

| 文件 | 命中 | 归类 |
| --- | --- | --- |
| ch06 | **0** | 正文/记录均无 monlor |
| ch01 / ch02 / ch05 / ch07 | 各 1–2 | **全部在「更新记录」** |
| ch03 | 4 | L82 **3.2 旧路线端口对照 warning**（有意保留）+ 3 行更新记录 |
| ch04 | 7 | L24 **4.1 换路线背景** + L40 **「周边工具集合」note** + L118 **旧端口对照 note** + L173 **引文对照第 7 行**（逐字引 `monlor/docker-xiaoya` + 出处 `README:295`）+ 3 行更新记录 |
| overview | 1 | L54 **读前须知**：说明早期 monlor 路线已停维护、步骤已整体替换（有意保留） |

**结论**：无一处「未加说明的正文遗留」；6 处正文例外均为「早期路线 vs 本路线」的对照说明，来源可回源（`sources/01_raw_githubusercontent_com.md:295`）。

## 5. 校验结果

| 校验 | 命令 | 结果 |
| --- | --- | --- |
| 副本一致性 | `publish_copies.py --check`（7 章 output + vault） | ✅ 7/7 `OK`（output==、vault==） |
| 装配件一致 | `assemble_final.py --check`（`output/final_note.md`） | ✅ `需更新 0 章` |
| Markdown 结构 | `check-md-structure.py`（output 9 文件、vault 8 文件） | ✅ 0 处可疑 |
| 引文纪律 | `note-citation-check.py workspace/xiaoya-fnos-deploy` | ✅ **无硬失败**（V 6/6 命中、S4 0 处、C 0 差异） |
| 校验器自测 | `note-citation-check-selftest.py` | ✅ 七个用例全部符合预期 |
| 配置同步 | `sync_agents.py --check` | ✅ synchronized |

候选清单人工判（S1/S2/S3 非硬失败）：
- **S1 边界叠字**：0 处。
- **S2 LCS 撞车（10 处）**：全部为「引导语点名某条目 + 随后逐字引用同一条目」（如「适配 飞牛影视」←`- [x] 适配 飞牛影视`）或**功能名重复**（「小雅的夸克分享区」）。判为**良性**，非「引导语把引文又说一遍」的缺陷形态。
- **S3 反引号外 ASCII 词串（去重 5 个）**：`raw Markdown`、`Open Token`、`folder id`、`alist tvbox`、`Docker Hub` —— 均为**保留类术语 / 产品名**，或位于「」引文内，判为**保留**。

## 6. P5 期间的工具修正（非笔记缺陷）

两处**校验器误报**在本轮暴露并修复（canonical 改 `.codex/scripts/`，同步至 `.claude/scripts/`）：

| # | 误报 | 根因 | 修法 |
| --- | --- | --- | --- |
| 1 | S4「出处列非法」72 处 | 出处取值域只认 `.md/.txt/.html/.json`，而本主题的逐字引文出自一键脚本 `sources/xiaoyaDev/all_in_one.sh`（`.sh`） | `CITE_FULL` 扩展为 `(?:md\|txt\|html\|json\|sh)` |
| 2 | S4「管道数 != 5」4 处 | 引文里引用一行 shell 管道或一行 Markdown 表格时，单元格内竖线写成**转义** `\|`（正确写法），被按原始 `\|` 计数 | 只计**未转义**竖线（`(?<!\\)\|`），并按未转义竖线切列；新增自测用例 **G** 守住该回归 |

另修 ch05 §5.4.2 的 `docker compose config` 报错：由行内反引号改为**带语言标识的代码块**（命令输出不是英文散文引文），既符合 `note-system.md` 的代码块要求，也消除 V 的误判。

## 7. MOC 同步

`流媒体与影音 MOC.md` 已含小雅条目（指向 `小雅 fnOS 单容器部署（总览）`），描述为「单容器部署步骤 + 避坑与运维」，**不含 monlor / 旧路线字样**，本轮无需改动；`updated: 2026-10-07` 已是当日。**未复制正文**，符合 `note-system.md` 的 MOC 规则。

## 8. 遗留（不阻塞，供后续参考）

| # | 项 | 说明 |
| --- | --- | --- |
| 1 | 各章 `遗留 / 风险` 小节 | 见 `updates/{01..07}/*/update_report.md`；多为「vault 侧表格列宽由 Obsidian 自动补空格」这类渲染层差异 |
| 2 | ch02 §2.4 不给硬件数字 | 有意取舍：原数字出自停更项目，不采用 |
| 3 | ch05 前端链路整体未动 | SmartStrm / MediaWarp / fntv-proxy 与部署主线正交 |
| 4 | ch06 坑五与 ch03 §3.3.2 的边界 | 完整端口/用户名对照在 ch03，ch06 只讲避法并交叉引用，不重复整表 |
| 5 | ch04 副本曾滞留旧锚点 | 已在 P4 收口发现并重发布（详见 `03_batch_update_log.md` P4 收口行） |

## 9. 收口健康检查（`.claude/scripts/workflow-health-check.sh`）

P5 收口时运行一次，结果**与本次笔记改写无关**，均为**本机环境 / 运行时会话配置**层面：

| 检查项 | 结果 | 判定 |
| --- | --- | --- |
| todo-state 动作守卫 | 15 个调用探测通过 | ✅ |
| manifest 注册校验 | 60 个工件通过 | ✅ |
| 跨机器可移植性 | shared agent sources portable | ✅ |
| workflow-routing 表 | **FAIL「表已过期」** | ⚠️ **误报**：本机 `python3` 是 macOS 自带 **3.9.6**，`sync-workflow-routing.sh` 要求 **3.10+**，因而**没能真正比对**就判红。用 3.10+ 解释器重跑：`PYTHON=$HOME/.local/bin/python3.12 .claude/scripts/sync-workflow-routing.sh --check` → `up to date`（✅ 表其实是同步的） |
| prompt-cache 守卫 | **FAIL knob drift**：`effortLevel` / `thinkingBudget` 会话值 `high` ≠ 冻结基线 `medium` | ⚠️ **环境/会话配置**：本仓库 `.llm/` 与 settings 在本次运行中**未被改动**（`git status` 无 `.llm/`），与笔记内容无关 |

**结论**：本 run 产出的笔记、其副本一致性、引文纪律、结构自检、装配件、配置同步**全部通过**；健康检查的两处 FAIL 属于解释器选择与运行时旋钮，需在**环境/配置层**另行处理，不在本次批量更新范围内。本机若想一键跑通健康检查，可先 `export PYTHON=$HOME/.local/bin/python3.12`。
