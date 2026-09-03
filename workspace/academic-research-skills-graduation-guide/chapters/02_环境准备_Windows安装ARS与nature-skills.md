---
title: 第 2 章 环境准备：Windows 下安装 ARS 与 nature-skills 并接线 Claude Code
chapter_no: 2
tags: [毕业设计, academic-research-skills, nature-skills, 环境安装, Windows, Claude Code, 实战笔记]
status: draft
source_project: academic-research-skills-graduation-guide
---

# 第 2 章 环境准备：Windows 下安装 ARS 与 nature-skills 并接线 Claude Code

> 篇幅：~1100 字 ｜ 素材：A5、A6、A1、N1、N3；02§6 ｜ 代码示例：PowerShell 安装命令、/plugin 命令、git clone、wrapper 文件、autoupdate-skills.sh
>
> **本章定位**：在 Windows 上把「Claude Code + ARS + nature-skills」三件套装到可用的最小环境。本指南后续每一章的触发都依赖本章成功——装错一步（缺共享包、缺 Git Bash、`python3` 指向商店 stub）通常不报错，而是让技能**静默失败**。

软件类毕设最怕的不是「没装」，而是「装到一半，命令全通过、技能就是不干活」。ARS 与 nature-skills 都是 agent 技能体系，安装单位、触发方式各不相同，先花十几分钟把地基打对，比后面边做边排错省得多。本章按 5 步走：装 Claude Code → 装 ARS → 装 nature-skills → 排 Windows 依赖坑 → 写项目偏好；每一步都给验证方法，装完你会得到一张「装了什么、装在哪、如何升级」的本地清单。

> [!warning] AI 诚信：动手前先确认学校规矩
> 两库官方立场都是「AI 是副驾驶、辅助不代写」（A1/N1）。装工具之前，先查清你所在学校对 AI 辅助写作的**披露/比例要求**，明确哪些阶段能用、怎么披露。装环境是小问题，「用了 AI 怎么如实交代」才是大问题——本指南默认你全程如实披露。

## 2.1 装 Claude Code 并配置密钥

ARS 的最小可用环境只有三样：Claude Code + `ANTHROPIC_API_KEY` + 在含 ARS 技能的仓库里运行 `claude`（A5）。先装 Claude Code。Windows 官方推荐用 PowerShell 脚本，**免装 Node、自带自动更新**（A5）：

```powershell
# PowerShell 执行；会写进用户级安装并自动更新
irm https://claude.ai/install.ps1 | iex
```

**验证**：新开终端执行 `claude --version`，能打印版本号即装好。

接着把密钥写入用户环境变量：

```powershell
setx ANTHROPIC_API_KEY "sk-ant-你的密钥"   # 用户级持久化；改后需新开终端才生效
$env:ANTHROPIC_API_KEY = "sk-ant-你的密钥"  # 仅当前会话生效，适合临时测试
```

**验证**：新开 PowerShell 执行 `echo $env:ANTHROPIC_API_KEY`，回显非空即配置成功；再运行 `claude` 能正常进入会话即可。

## 2.2 装 ARS：plugin 法为主，手动法备选

ARS 推荐用 Claude Code 的插件市场安装（A1/A5）。在 `claude` 会话里依次输入：

```text
/plugin marketplace add Imbad0202/academic-research-skills
/plugin install academic-research-skills
```

装完到插件面板把 **auto-update 打开**（来源：02§6），以后跟随上游更新。

**验证**：输入 `/plugin`，确认 `academic-research-skills` 在列且 auto-update 为开；再输入 `/ars-plan`，能进入苏格拉底式澄清对话即命令已注册（`/ars-plan` 为官方实录命令，A10）。

不想走插件市场时，可选手动复制（A5）：把 ARS 的 4 个技能目录 `deep-research` / `academic-paper` / `academic-paper-reviewer` / `academic-pipeline` **分别**复制进毕设仓库的 `.claude/skills/`，每目录顶层必须自带 `SKILL.md`；**勿把整个 ARS 仓库嵌套复制进去**：

```bash
# Git Bash，在毕设仓库根目录执行；<src> 指向 ARS 源码里对应技能目录的实际位置
mkdir -p .claude/skills
for s in deep-research academic-paper academic-paper-reviewer academic-pipeline; do
  cp -r "<src>/$s" .claude/skills/
done
```

**验证**：`ls .claude/skills/*/SKILL.md` 应列出 4 个文件；重启会话后让 Claude 按 `deep-research` 技能起手，能读到 SKILL.md 即接线成功。

## 2.3 装 nature-skills：clone + 两条 Claude Code 接线路线

nature-skills 不是 Claude Code 插件，先 `git clone` 到本地一个稳定路径（N1、02§6）：

```bash
# Git Bash 中执行
git clone https://github.com/Yuan1z0825/nature-skills.git
```

> [!tip] 大白话：把每个技能想成**一套带说明书和配件的工具箱**。`SKILL.md` 只是贴在箱子外的说明书，`references/`、`static/`、`manifest.yaml` 和共享包 `nature-shared` 才是里面的工具。只拷 SKILL.md = 只拿说明书不拿工具，agent 照着念却找不到东西，子路由和共享引用立刻断（N1/N3）。

它的安装单位是**完整技能目录**：每个 `skills/nature-*` 目录 = 一个技能，内含 SKILL.md（agent 入口）+ `references/` + `static/` + `manifest.yaml`，并依赖共享包 `nature-shared`（N1）。**不能只拷 SKILL.md**，必须保留完整目录与 nature-shared（N1/N3）。把技能接进 Claude Code 有两条官方路线（N3、02§6）：

**路线 A：wrapper（推荐）**。按需给技能写 `~/.claude/agents/nature-<x>.md`，让 agent 先读 clone 内完整 SKILL.md 再执行。以 `nature-figure` 为例：

```markdown
# ~/.claude/agents/nature-figure.md
你负责调用 nature-skills 的 nature-figure 技能：
1. 先阅读 <nature-skills clone 路径>/skills/nature-figure/SKILL.md，严格按其流程执行。
2. 按 SKILL.md 指引继续读取同目录 references/、static/，以及共享包 nature-shared。
3. 不要退化为通用回答；产出必须满足 SKILL.md 的契约与自动审计步骤。
```

升级 = 在 clone 目录里 `git pull`，wrapper 不用动。**验证**：新开会话输入 `@nature-figure …`，观察它先加载 SKILL.md 再走流程。

**路线 B：copy 脚本**。用官方脚本一次性同步到 `~/.claude/skills`，并在 `settings.json` 加 SessionStart hook，每次开会话自动再同步（N3、02§6）：

```bash
# 在 nature-skills clone 根目录执行
bash scripts/autoupdate-skills.sh --force
```

`settings.json` 里的 hook（示意；具体 schema 以你的 Claude Code 版本为准）：

```json
{
  "hooks": {
    "SessionStart": [
      { "hooks": [{ "type": "command",
                    "command": "bash <nature-skills clone>/scripts/autoupdate-skills.sh --force" }] }
    ]
  }
}
```

**验证**：`ls ~/.claude/skills/nature-figure/` 能看到完整目录（SKILL.md、references、static），且 `nature-shared` 也已同步。

## 2.4 依赖与 Windows 坑

两库的脚本都假设你有能跑 shell 的环境，Windows 上最常踩 4 个坑：

- **Git Bash**：ARS 的 `.sh` hook（如 PreToolUse guard）靠 Git Bash 执行；缺失时 hook 不激活，ARS 降级运行（A6）。装 Git for Windows 自带。**验证**：`bash --version` 能输出。
- **真实 Python**：Windows 的 `python3` 常是微软商店 **0 字节占位符**。ARS guard 会按 `py -3` → `python3` → `python` 顺序探测真 Python，探到才置 `ARS_PY_OK`（A6）。**验证**：

  ```powershell
  py -3 --version     # 应打印真实版本号
  python3 --version   # 若弹出商店页 = stub：改用 py -3，或装 python.org 版并勾 Add to PATH
  ```

- **可选导出依赖**：导出 DOCX 需要 Pandoc，导出 PDF 需要 tectonic + CJK 字体（Times New Roman / Source Han Serif TC / Courier New）；缺失时 ARS 自动降级为 Markdown 并给指引（A5）。**验证**：`pandoc --version`、`tectonic --version`。
- **MCP 凭据**：nature-academic-search 等文献检索技能需要 `PUBMED_EMAIL` / Scopus（`pybliometrics`）凭据——**禁止写进仓库**，放本地 `.env` 或已 gitignore 的文件（N1/N5、02§6）。

> [!tip] 大白话：MS Store 的 `python3` 占位符像**贴着「Python」门牌的空房间**——一敲门就弹商店页。`py -3` 探测 = 先敲真门牌号：敲得开（返回版本号）就用它，敲不开就装 python.org 的真 Python。

## 2.5 项目级偏好：在 CLAUDE.md 写 standing preferences 块

两库的内容偏好（引文风格、检索范围、来源层级、OA）**没有全局配置**，官方途径是在毕设仓库的 `CLAUDE.md` 写 standing preferences 块（A5），两库的 agent 会话都会继承项目级设置。示意：

```markdown
# 毕设仓库 CLAUDE.md 追加
## Research Standing Preferences
- 引文风格：先按学校模板；目标 GB/T 7714（两库均无国标直接输出，最终需人工/脚本校验——推断建议）
- 检索范围：软件工程、教育信息化，含相关标准与工程资料；区分「学术文献」与「工程资料」两类引用
- 来源层级：优先顶会/顶刊/学位论文；工程资料仅作背景
- 开放获取：优先 OA；付费文献走学校图书馆 / CARSI 通道
```

> [!warning] 系统开发边界：本章装好的是「学术线」的地基，不是「开发线」的替身。ARS 与 nature-skills 都**不写代码、不跑你的实验、不能证明系统跑通**（02§2；A1/N1）。系统实现必须另配一套常规软件工程工作流（需求 / 架构 / 编码 / 测试），两库只负责把「已实现的结果」登记成可写进论文的 claim——第 6 章专讲这条双线怎么配合。

---

## 本章小结

- 最小环境三件套：Claude Code（PowerShell 一行装 + 自动更新）+ `ANTHROPIC_API_KEY` + ARS（plugin 首选）+ nature-skills（git clone + wrapper 接线）。
- ARS 手动备选 = 把 `deep-research` / `academic-paper` / `academic-paper-reviewer` / `academic-pipeline` 四个目录**分别**复制进 `.claude/skills/`，勿整仓嵌套。
- nature-* 的安装单位是**完整技能目录**（SKILL.md + references + static + manifest + nature-shared），只拷 SKILL.md 会断子路由。
- 两条接线路线：wrapper（推荐，`git pull` 即升级）与 `autoupdate-skills.sh --force` + SessionStart hook（copy 路线）。
- 四个 Windows 坑：Git Bash、MS Store `python3` stub（用 `py -3` 探测）、Pandoc/tectonic + CJK（缺则降级 Markdown）、MCP 凭据禁止入库。

**读者行动项**：
- [ ] 装好 Claude Code 并配好密钥，`claude --version` 与 `echo $env:ANTHROPIC_API_KEY` 均通过
- [ ] plugin 法装好 ARS（或手动复制 4 目录），`/ars-plan` 能唤起
- [ ] clone nature-skills，用 wrapper 接好毕设硬依赖技能（如 `nature-figure`、`nature-ref-verifier`）
- [ ] 确认 Git Bash + 真实 Python；把 MCP 凭据写入 gitignore

**下一章预告**：环境就绪，进入毕设主线。第 3 章是阶段 0「选题与开题」（开题报告已交可略读）；你当前所在的**阶段 1 文献调研**对应第 4 章，那才是接下来要主攻的实操章。
