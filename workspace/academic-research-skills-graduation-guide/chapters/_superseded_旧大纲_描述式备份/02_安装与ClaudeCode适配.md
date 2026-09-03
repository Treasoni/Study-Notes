---
title: 第二章 安装与 Claude Code 适配（Windows 实测路线）
chapter_no: 2
tags: [毕业设计, academic-research-skills, nature-skills, 安装, Windows, Claude Code, 实战笔记]
status: draft
source_project: academic-research-skills-graduation-guide
---

# 第二章 安装与 Claude Code 适配（Windows 实测路线）——装到「能用」再谈流程

> **本章定位**：第 1 章给的是地图，本章给的是把车开上路的钥匙。读完并照做后，你的 Windows 机器上会同时跑通「Claude Code + ARS + nature-skills」的最小可用环境，并拿到一张「已装/缺什么」的本地清单。本指南第 3 章起的所有触发都依赖本章成功。
>
> **素材引用约定**：沿用第 1 章，正文 `A-*` / `N-*` 指 `02_deep_research.md` 的源 ID；`§x.y` 指该文件小节。

两套库都是 **agent 技能体系**：装错一步不会当场报错，而是**静默失败**——nature-skills 只拷了 `SKILL.md` 会子路由断裂，缺 Git Bash 会让 ARS 的 `.sh` 关卡不激活，`python3` 命中微软商店假壳会让探测脚本空转。本章的策略是：每装一步，立刻给一个能验证的动作，把「看起来装了」和「真的能用」区分开。

## 2.1 先装 Claude Code 与密钥：一切的最小可用底座

ARS 的推荐形态是 **Claude Code 插件**，nature-skills 的 wrapper 也要挂在 Claude Code 上（素材 §2）。所以第一步先把宿主装好。

**步骤 1：安装 Claude Code（PowerShell）。** 官方现役方式是免 Node、自动更新的安装脚本；npm 方式已弃用（A5）。

```powershell
# Windows PowerShell 执行；安装后会自动更新
irm https://claude.ai/install.ps1 | iex

# 验证版本
claude --version
```

**步骤 2：配置密钥。** ARS 的最小可用 = Claude Code + `ANTHROPIC_API_KEY` + 在一个**含 ARS skill 的项目目录里**运行 `claude`（A5）。密钥放用户环境变量：

```powershell
# 只示例，别把真实密钥写进仓库；下值替换为你的 key
$env:ANTHROPIC_API_KEY = "sk-ant-你的key"
setx ANTHROPIC_API_KEY "sk-ant-你的key"
```

一个影响日常使用的细节：ARS 的 skill 是**挂在 Claude Code 会话**上的，而 Claude Code 默认按「当前项目目录」加载 skills。这意味着**你在哪个目录启动 `claude`，决定这次会话能不能看到 ARS**。建议从本章起统一在毕设仓库根目录启动 `claude`，让插件、`CLAUDE.md` 偏好与后文要建的技能都落在同一个上下文里，少踩「换个目录就找不到技能」的坑。

> [!warning] 密钥纪律：`ANTHROPIC_API_KEY` 以及后文的可选文献检索凭据（PUBMED_EMAIL、Scopus `pybliometrics`）都属于**禁止入库**的敏感信息（N1/N5）。只写进本地 `.env` 或系统环境变量，永远不提交。

> [!tip] 大白话：`/plugin marketplace` 可以想成**手机上的应用商店**——先「添加商店地址」，再「从这个商店安装 App」。Claude Code 本身就是这些 agent 技能的操作系统，装好它，后两节才有地方安家。

**本章先立两条边界（全指南贯穿提醒）**：① **系统开发边界**——本章装的全是「学术线」工具，ARS 与 nature-skills 都**不写代码、不跑实验、不能证明你的系统跑通**，系统开发要另配常规工程工作流（对应第 6 章主战场）；② **AI 诚信**——动手前先确认你所在学校对 AI 辅助写作的披露/比例规范，两库官方立场都是「辅助不代写」。

## 2.2 安装 ARS：推荐 plugin 市场法，手动复制为备选

**方式 A（推荐）：插件市场。** 在含 ARS 的项目里启动 `claude`，在会话内输入（A1/A5）：

```text
/plugin marketplace add Imbad0202/academic-research-skills
/plugin install academic-research-skills
```

装完用 `/plugin` 查看已装插件，并建议在插件面板打开 **auto-update**（具体子命令随 Claude Code 版本略有差异，以面板提示为准），这样 ARS 升级不用手动重装。

**方式 B（备选）：手动复制。** 当你需要直接改技能源码时才走这条路。把 ARS 的 **4 个 skill 目录**——`deep-research` / `academic-paper` / `academic-paper-reviewer` / `academic-pipeline`——**分别**复制进项目的 `.claude/skills/`；每个目录顶层必须有 `SKILL.md`；**切勿把整个仓库嵌进去嵌套复制**（A5）。

> [!warning] ARS 手动法两条硬纪律：一是一个 skill 一个目录、顶层放 `SKILL.md`；二是**别整仓嵌套**——把整个仓库复制成 `.claude/skills/academic-research-skills/` 这种层级，Claude Code 找不到入口。

选哪种？**日常用 plugin 法最省心**：升级、依赖都由插件机制管，适合你只是想「用 ARS」，不想动它的源码。手动法只在两种场景值得：你要给某篇写作指南加 GB/T 7714 之类的自定义引用规则（第 8 章改造路径），或者学校内网不允许连插件市场时。两种方式装好后，后文触发方式完全一样——因为 ARS 的模式/斜杠命令是注册在 skill 里的，与「怎么装进来」无关。

**验证动作**：在项目目录里运行 `claude`，输入 `/plugin`（方式 A）应能看到 ARS 已列出；或直接输入 `/ars-plan` 试探——能进入苏格拉底式澄清对话即说明管道通了（命令来源 A10）。

## 2.3 安装 nature-skills：git clone + 「全目录纪律」

**主路线：稳定 clone。** wrapper 路线需要一个长期不动的本地副本当锚点（N1/N3）：

```bash
# 在 Git Bash 里执行；建议 clone 到一个你记得住的固定位置
git clone https://github.com/Yuan1z0825/nature-skills.git
cd nature-skills
ls skills          # 每个子目录 = 一个可安装技能（nature-*）
```

**全目录纪律（本节最重要）**：nature-skills 里**技能目录 = 安装单元**，一个技能目录含 `SKILL.md`（agent 入口）、README（中英镜像）、`references/`、`static/`、`manifest.yaml`（router 式，负责把请求路由到技能内子功能），并依赖**共享包 `nature-shared`**（N1）。因此**不能只拷 `SKILL.md`**——必须保留完整目录结构，否则共享引用/子路由断裂（N1/N3）。后文凡是「把某技能接到 Claude Code」，指的都是**整目录**而不是单文件。

> [!tip] 大白话：一个技能不是「一个文件」，而是**一个小工具箱**：`SKILL.md` 是箱盖上的使用说明，`references/`、`static/`、`manifest.yaml` 是里面的工具层，`nature-shared` 是几箱共用的一套**通用零件**。只拷使用说明 = 把说明书带到工地但没带工具，agent 读了也不知道该拿什么干活。

**其他官方安装方式（了解即可，不是本指南主线）**：

| 方式 | 用途 | 注意 |
|---|---|---|
| `git clone`（主线） | 稳定副本 + wrapper 接线 | 升级 = clone 内 `git pull` |
| `npx skills add` | 快速抓技能包 | 需 **Node 18+**（N1）；精确用法以官方 README 为准 |
| `scripts/update-codex-skills.sh` | 同步到 Codex runtime | **只写入 `~/.codex/skills`**，不装进 Claude Code（N1/N3） |

注意：你 clone 到的是**整个技能库**（约 19 个可触发技能 + `nature-shared`，N1），不是单个技能。本指南的建议是**用到哪个、接线哪个**：先按第 1 章分工表圈出你的毕设硬依赖（文献管线、ref-verifier、figure、paper2ppt 等），再给这几个写 wrapper，而不是一次接 19 个——wrapper 越多，语义路由越容易撞车。

另外记住：`nature-*` **没有统一斜杠命令**，靠 LLM 语义路由触发（N4–N13）。在 Claude Code 里要让它能被触发，就得走下一节的接线。

## 2.4 接线 Claude Code：wrapper 路线推荐，copy + SessionStart hook 为备选

nature-skills 官方**没有针对 Claude Code 的同步脚本**（`update-codex-skills.sh` 只写 `~/.codex/skills`），所以要自己接线。两条路线（N1/N3、§6）：

**路线 A（推荐）：wrapper——给需要的技能各写一个薄 agent 文件。** 在 `~/.claude/agents/` 下建 `nature-<x>.md`，正文就是一句话契约：「先读 clone 内对应 `SKILL.md` 并遵守，按需读同目录与 `nature-shared`，勿退化为通用回答」（§6）。示例：

```markdown
---
# ~/.claude/agents/nature-ref-verifier.md —— 最小示例
# frontmatter 必填字段随你的 Claude Code 版本约定，此处给常用两项
name: nature-ref-verifier
description: 当用户要求核对参考文献条目、验证引用字段或处理 CNKI 中文条目时使用。
---

先完整读取 <你的clone路径>/nature-skills/skills/nature-ref-verifier/SKILL.md 并严格遵守其中的流程；
按需读取同目录 references/、static/ 与共享包 ../nature-shared/；
以 SKILL.md 的规则为准，不要退化成泛泛的通用回答。
```

wrapper 路线的**升级 = 在 clone 里 `git pull`**，不用重写 wrapper 文件——这就是它被推荐的原因。

**路线 B（备选）：copy + SessionStart hook。** 把技能整目录同步到 `~/.claude/skills/`，并在 `~/.claude/settings.json` 加一个 **SessionStart hook**，让每次新会话自动重跑同步，保持副本新鲜（§6）。调研中记录的同步命令是 `scripts/autoupdate-skills.sh --force`（§6）；**该脚本是否存在于你 clone 的版本里、以及 hook 的逐字 JSON，素材未给出**——若你的 clone 没有此脚本，就回到路线 A，或手动整目录复制（连带 `nature-shared`）。

> [!tip] 大白话：wrapper 像给每个外国专家配一个**本地接线员**——接线员不自己干活，只负责「这位专家来了，带他去读那份标准作业流程（SKILL.md）」。copy 路线则像把整间办公室搬到本地，每次总部更新都得再搬一次。

两路线取舍：wrapper **改动小、升级靠 git pull、共享包天然在 clone 内**，推荐；copy 不依赖固定 clone 路径，但要维护 hook、升级要重同步。

**接线完怎么确认真的路由了？** 光写文件不够，要实测一次：对刚配好的技能问一个只有它能答的问题，例如「请用 ref-verifier 核对这条 CNKI 参考文献的字段」，然后观察 Claude Code 是否**先读取 clone 内的 `SKILL.md` 再作答**。如果它没读文件就泛泛回答，说明 wrapper 的 `description` 没被触发或路径写错——这正是本章反复强调「装完要验证」的原因。

## 2.5 Windows 依赖与坑：Git Bash、真 Python、可选导出件

**坑 1：`python3` 可能是微软商店的 0 字节占位 stub（假壳）。** ARS 的 guard 在 Windows 上会按 `py -3` → `python3` → `python` 的顺序探测**真 Python**，命中后用环境标记 `ARS_PY_OK` 告诉后续脚本「这是真的」（A6）。你在 Git Bash 里可以这样自测：

```bash
# Git Bash 里探测真 Python；若命中 Store stub 会跳转商店或返回空
py -3 --version && py -3 -c "print('real py ok')"   # 优先（Windows 官方 Python 启动器）
python3 --version                                     # 可能是假壳，谨慎看结果
python --version                                      # 兜底
```

**坑 2：缺 Git Bash，`.sh` 关卡不激活。** ARS 的 guard 依赖 shell hook，**无 Git Bash 时 `.sh` hook 不运行**（属于官方接受的降级，A6）；nature-skills 的 copy/同步脚本也多在 Git Bash 里跑。建议装 Git for Windows（自带 Git Bash），并把 `C:\Program Files\Git\bin` 加入 PATH。

另一个连带提醒：那个假的 `python3` 在 Git Bash 里通常根本不可用，而本指南后文的命令默认在 Git Bash 里执行，所以**建议把 `py -3` 作为你的默认 Python 入口**，并确认 Git Bash 能找到它（找不到就用 `py -3` 的完整路径，或在 `~/.bashrc` 里加别名）。

**坑 3：可选导出件（到第 9/10 章导出 DOCX/PDF 才需要）。** `.docx` 需要 **Pandoc**；PDF 需要 **tectonic** + **CJK 字体**（素材点名的三类：Times New Roman、Source Han Serif TC、Courier New，A5）。缺依赖时 ARS 不会报错，而是**自动降级为 Markdown + 给指引**（A5）。对中文毕设，建议现在就装齐 tectonic 与中文字体，免得最后一章导出中文 PDF 时才乱码。

```powershell
# 示意：Pandoc 可用 winget 查装（确切 ID 以 winget search 结果为准）
winget search pandoc
```

**可选：文献检索 MCP 凭据。** 阶段 1 若用 `nature-academic-search`，需配 `PUBMED_EMAIL` / Scopus `pybliometrics` 凭据（N5）；浏览器类技能需 `playwright chromium`（N1）。这些按需再配，凭据一律不进仓库。

> [!warning] 中文适配提醒：CJK 字体缺失只在导出 PDF 时爆雷，且爆的是「满屏方块字」这种晚期问题。**安装期顺手装齐**，是成本最低的中文排版保险。参考文献国标格式（GB/T 7714）两库都不直接输出，留到阶段 6 专门改造，不在此章处理。

## 2.6 项目级偏好与验收清单：把「口味」写进 CLAUDE.md

ARS 的**内容偏好没有全局配置文件**，官方途径是在**毕设仓库的 `CLAUDE.md`** 里写 standing preferences 块（引文风格 / 检索范围 / 期刊层级 / OA），两库 agent 每次会话都会继承（A5）。建议在项目一开始就写好：

```markdown
<!-- 毕设仓库根目录 CLAUDE.md 末尾追加；字段为示意，精确 key 以官方 SETUP 文档为准 -->
## Academic Preferences（standing preferences）
- Citation style：学校未强制 GB/T 7714 前，先用 IEEE 顺序编号制顶替，见第 8 章
- Search scope：本领域中文 + 英文核心；工程资料（技术报告/标准/开源文档）与学术文献分开标注
- Source tier：优先同行评审来源；博客/二手解读只当线索
- Open access：优先 OA 可获取全文的来源
```

**最后，用这张清单收尾**（把「装过」和「能用」分开）：

| 组件 | 用途 | 已装/缺 | 检查方式 | 缺失后果 |
|---|---|---|---|---|
| Claude Code | 两库宿主 | ☐ | `claude --version` | 一切无从谈起 |
| `ANTHROPIC_API_KEY` | ARS/nature 调用 | ☐ | 启动 `claude` 不报鉴权错 | 技能无法运行 |
| ARS（plugin 或 4 目录） | 学术流程主调度 | ☐ | `/plugin` 列表 / `/ars-plan` 试探 | 无流程与诚信闸门 |
| nature-skills clone | 技能库锚点 | ☐ | `ls skills` 见 `nature-*` | 无单项成品技能 |
| 至少 1 个 wrapper / copy | nature 进 Claude Code | ☐ | 触发一次技能看是否读 SKILL.md | nature 技能调不动 |
| Git Bash | 跑 `.sh` hook | ☐ | `bash --version` | ARS guard/nature 脚本降级 |
| 真 Python（非 stub） | ARS guard / nature 脚本 | ☐ | `py -3 -c "print(1)"` | 依赖 py 的技能静默失败 |
| Pandoc + tectonic + CJK 字体 | 导出 DOCX/PDF（可选） | ☐ | 按需到第 9/10 章验证 | 导出降级 Markdown / 中文乱码 |
| CLAUDE.md standing prefs | 统一两库输出口味 | ☐ | 项目根目录可见 | 每次会话都要重复交代偏好 |

---

## 本章小结

- **最小可用 = Claude Code + `ANTHROPIC_API_KEY`**；ARS 走 `/plugin marketplace add` + `/plugin install`（推荐），手动复制须 4 目录分开、各带顶层 `SKILL.md`、勿整仓嵌套（A5）。
- **nature-skills 的安装单元是「技能目录」**，必须保留完整目录 + `nature-shared`，**只拷 `SKILL.md` 必断**（N1/N3）；升级在 clone 里 `git pull`。
- **Claude Code 接线优先 wrapper**（`~/.claude/agents/nature-<x>.md` 指向 clone 内 SKILL.md）；copy + SessionStart hook 是备选，需维护同步（N1/N3、§6）。
- **三个 Windows 静默坑**：`python3` 微软商店假壳（按 `py -3`→`python3`→`python` 探测）、缺 Git Bash 导致 `.sh` hook 不激活、缺 tectonic/CJK 字体导致中文 PDF 乱码（A5/A6）。
- **内容偏好写进项目 `CLAUDE.md` 的 standing preferences**，两库会话继承（A5）。

**读者行动项**：
- [ ] 逐项对照 2.6 清单，把「已装/缺」补全，特别是真 Python 与 Git Bash
- [ ] 用一条简单触发确认 ARS 与至少一个 nature 技能真的能路由（不是「看起来装了」）
- [ ] 在毕设仓库 `CLAUDE.md` 写好 standing preferences 块

**下一章预告**：环境就绪，正式进入毕设主线——第 3 章用 ARS `/ars-plan` 的苏格拉底澄清 + nature-proposal-writer，把已定题目收敛成可辩护的研究论点与开题报告骨架。
