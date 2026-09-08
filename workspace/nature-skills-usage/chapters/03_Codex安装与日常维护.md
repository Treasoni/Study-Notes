# 第三章：Codex 安装与日常维护

> 本章解决一个很实际的问题：装哪些、装到哪、怎么更新、怎么拆、装完怎么确认真的能用。读完你会有两条互相配合的「安装路线」和一张命令矩阵，照着敲即可，不用背。

上一章给了 19 个技能的全景速查，但「认识」不等于「能用」。本章从前置检查开始，先给一条安装路线决策树（§1），再讲 `npx skills` 按技能粒度安装的命令矩阵（§2）、仓库脚本整库同步（§3）、SessionStart 自动更新（§4）、运行时依赖与合规安装（§5），最后是安装验证与「开新会话」规则（§6）。

---

## 1. 前置准备与「安装路线决策树」

### 1.1 装之前先确认三件事

| 前置项 | 要求 | 检查命令 |
|--------|------|----------|
| Node.js | **≥ 18**（`npx skills` 本身就跑在 npx 上） | `node -v` |
| Codex | 本机已可运行 Codex CLI | `codex --version` |
| Git | 推荐安装（私有仓库 / 凭据走 Git credential、`gh` 或 `GITHUB_TOKEN`） | `git --version` |

```bash
node -v          # 期望 v18 或更高，低于 18 先升级 Node
codex --version  # Codex 可用即可继续
```

> [!tip] 大白话
> 把 `npx skills` 想成「上门安装的师傅」：师傅（npx）本身要能跑，前提是 Node.js 这把「工具箱」够新（≥18）。Node 版本太旧，工具箱缺件，师傅来了也干不了活。

### 1.2 安装路线决策树

nature-skills 官方给的是**两条互补路线**，不是二选一的对立关系（S1 §5.1/§5.3）。先想清楚你要哪种「跟上游」的节奏：

```text
只想要 1–3 个技能（轻、快、可挑）
   └─ 路线 1：npx skills add（按技能粒度，记着带 nature-shared）
想要整库长期跟上游、能一键整体升级/清理
   └─ 路线 2：git clone + scripts/update-codex-skills.sh（整库同步）
想每次开 Codex 自动检查更新、不用手动记
   └─ 路线 2 的专用 clone + autoupdate-skills.sh 注册为 SessionStart hook
```

两条路线的最终落点是同一套目录：全局装到 `~/.codex/skills/`，项目级装到 `.agents/skills/`（见 §2.3）。区别只在**管理方式**——路线 1 由第三方 CLI（vercel-labs/skills）按技能管理，路线 2 由仓库自带脚本整库管理（S2；S1 §5.3）。

> [!tip] 大白话
> 把路线 1 想成「按需点菜」——只点今天想吃的几道，后厨（npx skills）单独给你做；把路线 2 想成「整箱搬货」——直接跟厂家（GitHub 仓库）订一整箱，厂家出新版你就整箱换新。怕麻烦、想要最新最全就整箱；只想用两三个技能就点菜，别为了一道菜买一箱。

---

## 2. 路线 1｜`npx skills add / list / update / remove` 命令矩阵

路线 1 的 CLI 是 vercel-labs/skills，通过 `npx skills` 调用；安装源用 GitHub 仓库缩写 `Yuan1z0825/nature-skills`（S1 §5.1；S2）。所有命令以 `--agent codex` 限定装到 Codex。

### 2.1 先看有哪些技能可装（不安装）

```bash
npx skills add Yuan1z0825/nature-skills --list
```

`--list` 只列出可安装技能，**不安装**（S2）。关键点：这里列出的名字是 **frontmatter name**（`SKILL.md` 里声明的触发名），不是仓库目录名（S1 §5.1）。

```text
# 输出示意（以仓库当前索引为准，字段措辞随 CLI 版本可能不同）
Available skills from Yuan1z0825/nature-skills:
  nature-reader          # 读论文全文 Markdown
  researchwrite          # ← 目录名其实是 nature-proposal-writer
  ...
```

> [!warning] 目录名 ≠ frontmatter name
> `nature-proposal-writer` 这个**目录**，它的 frontmatter 触发名是 `researchwrite`。凡是 `npx skills` 系列命令里写技能名的地方（`--skill` / `list` / `update` / `remove`），都用 **frontmatter name**。选技能、报技能名时也是 `researchwrite`，不是目录名（S1 §5.1；S5 §4.4）。

> [!tip] 大白话
> 把「目录名」想成工牌上的**部门+岗位**（nature-proposal-writer），把「frontmatter name」想成平时喊人的**花名**（researchwrite）。CLI 和 Agent 都认花名——你在走廊喊他的部门名，他可能不知道在叫你。

### 2.2 安装（add）

**① 全量装到 Codex（全局）**——一次带上全部技能含 `nature-shared`：

```bash
npx skills add Yuan1z0825/nature-skills --global --agent codex --skill '*' --yes --copy
```

**② 单技能装到当前项目**——省略 `--global` 即项目级，只装 `nature-figure`：

```bash
npx skills add Yuan1z0825/nature-skills --agent codex --skill nature-figure --yes --copy
```

**③ 依赖共享包的技能单独装**——`nature-reader` / `nature-paper2ppt` / `nature-polishing` / `nature-writing` 依赖 `nature-shared`，单独装这类技能时要把共享包一起点名，否则会漏：

```bash
npx skills add Yuan1z0825/nature-skills --global --agent codex --skill nature-reader --skill nature-shared --yes --copy
```

**④ 一次装到 CLI 支持的所有 Agent**（不只 Codex）：

```bash
npx skills add Yuan1z0825/nature-skills --all
```

### 2.3 关键 flag 语义与安装路径

flag 语义以 vercel-labs/skills 文档为准（S2）：

| flag | 含义 |
|------|------|
| `--global` | 装到全局；**省略**则装到当前项目 |
| `--agent codex` | 指定目标 Agent 为 Codex |
| `--skill '<name>'` | 指定技能名，可用 `'*'` 表示全部；可重复出现组合多个技能 |
| `--yes` | 跳过确认提示 |
| `--copy` | **复制**文件而非建 symlink；Windows 无管理员 / symlink 受限时推荐 |
| `--list` | 只列出可安装技能，不安装 |
| `--all` | 等价 `--skill '*' --agent '*' -y` |

路径映射（S2 Supported Agents 表）：

```text
全局安装   ~/.codex/skills/          # 当前机器所有 Codex 项目可见
项目安装   <项目根>/.agents/skills/  # 只对当前项目生效
```

```text
# 全局安装后的目录形态（示意）
~/.codex/skills/
├── nature-reader/
│   ├── SKILL.md          # frontmatter + 路由协议
│   ├── manifest.yaml     # 声明式「轴 → 文件」映射
│   ├── static/
│   ├── references/
│   └── scripts/
├── nature-shared/
└── ...（其余技能目录）
```

> [!warning] 保留完整技能目录
> 无论哪条路线，都要保留技能**整目录**（`SKILL.md` + `references/` + `static/` + `manifest.yaml` + `scripts/` + 依赖的 `nature-shared/`）。**只复制 `SKILL.md` 会坏**——router-style 技能靠 manifest 和按需加载的片段目录工作，单文件是跑不起来的（S1 §5.3）。

> [!tip] 大白话
> `--copy` 想成「把资料复印一份放进自己文件夹」；不写 `--copy`（symlink）想成「在文件夹里贴一张『去资料室取』的便签」。Windows 没开管理员权限时，便签可能贴不上（symlink 受限），所以官方建议复印一份，省心。

### 2.4 查看已安装（list）

```bash
npx skills list --global --agent codex --json
```

`--json` 输出结构化结果，方便核对到底装上了哪些、装在哪个路径（S1 §5.1；S2）。

```json
// 输出示意（字段以实际 CLI 版本为准）
{
  "agent": "codex",
  "global": true,
  "skills": [
    { "name": "nature-reader",  "path": "~/.codex/skills/nature-reader" },
    { "name": "nature-shared",  "path": "~/.codex/skills/nature-shared" },
    { "name": "researchwrite",  "path": "~/.codex/skills/nature-proposal-writer" }
  ]
}
```

记不清装了哪些名字时，先 `list --json` 再动手，不要凭目录名猜。

### 2.5 更新（update）

```bash
npx skills update --global --yes                    # 更新全部全局技能
npx skills update nature-reader --global --yes      # 只更新单个技能
# 项目级更新在项目目录内执行，作用域默认 --project
```

`update` 支持全量、单技能与项目作用域（`--project`），按需选用（S1 §5.1；S2）。

### 2.6 删除（remove）

```bash
npx skills remove <skill>              # 用 frontmatter name，不是目录名
npx skills remove <skill> --global --agent '*'   # 指定作用域与 Agent
npx skills remove <skill> --all        # 全 Agent 范围删除
```

`remove` 的语义来自 S2：同样支持 `--global` / `--agent` / `--all` 作用域。删之前先 `list --json` 确认技能名拼写。

---

## 3. 路线 2｜仓库脚本整库同步（官方 Codex 推荐）

想整库跟上游、能整体校验和清理，用仓库自带脚本 `scripts/update-codex-skills.sh`（S1 §5.3 官方 Codex 路线）。它只处理**本仓库的技能目录**，不碰你别的配置。

### 3.1 首次同步

```bash
git clone https://github.com/Yuan1z0825/nature-skills.git
cd nature-skills
scripts/update-codex-skills.sh --pull
```

### 3.2 三个子命令

| 子命令 | 作用 |
|--------|------|
| `--pull` | clone 后全量同步到 Codex 技能目录 |
| `--check` | 校验本机技能与仓库的一致性（只检查不写入） |
| `--pull --prune` | 同步，并清理上游已删除的技能目录 |

```bash
scripts/update-codex-skills.sh --check        # 校验一致性
scripts/update-codex-skills.sh --pull --prune # 同步 + 清理上游已删目录
```

### 3.3 脚本行为与 Windows 注意点

脚本内部特性（S1 §5.3；S5 §4.2）：

- 用 `rsync -a --delete` 同步，只动本仓库的技能目录；
- 同步后写一份清单记录，`diff -qr` 校验一致性；
- 跑完打印可选的 Python 依赖安装提示（不会自动装）。

Windows Git Bash 注意：

- `update-codex-skills.sh` **依赖 `rsync`**。Windows 的 Git Bash 不一定自带 rsync，首次跑 `--pull` 前先确认 `rsync --version` 可用；不可用则需自备 rsync 或退回路线 1（S1 §5.3；P2 §5 实践指导）。
- 多技能安装优先 `--copy`（避开 Windows symlink 权限问题）。
- 该脚本**只同步 Codex**；Claude Code 用户不能拿它同步自家环境（那是 Claude Code 路线，走本地 clone + wrapper，本节不展开）（S1 §5.2/§5.3）。

> [!note] `--prune` 的删除语义
> `--prune` 只删「脚本此前记录过、但仓库里已不存在」的技能目录；**首跑不猜删**，不会误删你没同步过的东西（S1 §5.3）。

> [!tip] 大白话
> `rsync -a --delete` 想成「拿仓库当母本做整盘镜像」：本地多出来的、母本已删的旧技能会被清掉（`--prune` 时）。正因为是镜像式同步，它要求你有个**专用、干净**的 clone，别在这个仓库目录里自己乱改文件。

---

## 4. 自动更新：autoupdate-skills.sh + SessionStart hook

想要「每次开工自动检查有没有新版」，官方方案是把 `scripts/autoupdate-skills.sh` 注册成 Codex 的 **SessionStart hook**（S1 §5.3）。

### 4.1 手动触发一次

```bash
scripts/autoupdate-skills.sh --dest ~/.codex/skills --force
```

### 4.2 脚本的自我保护行为

- **6 小时节流**：同一仓库 6 小时内不重复同步；
- **断网即退**：连不上网络时 exit 0，不打扰你开工；
- **仅 HEAD 变化才同步**：远端没有新提交就不折腾；
- **拒绝脏 clone**：仓库目录有未提交改动时拒绝执行。

### 4.3 注册到 SessionStart hook

官方建议把它合并进 Codex 的 `~/.codex/hooks.json` 的 `SessionStart`（S1 §5.3）。每次开新 Codex 会话时，hook 自动触发脚本检查更新。

```json
// ~/.codex/hooks.json —— 结构示意
// Codex 不同版本的 hook schema 字段可能有差异，以你本机版本为准（需实测）
{
  "SessionStart": [
    {
      "hooks": [
        {
          "type": "command",
          "command": "bash ~/nature-skills/scripts/autoupdate-skills.sh --dest ~/.codex/skills"
        }
      ]
    }
  ]
}
```

> [!warning] 需实测项
> `hooks.json` 的**具体 JSON 结构与字段名**随 Codex 版本可能有差异，也可能你本机用的是 `config.toml` 的 hook 写法。上表是「合并进 SessionStart」的**结构示意**，落地前先对照你本机 Codex 的 hook 文档确认一次，别照抄后静默失败。

> [!tip] 大白话
> 把自动更新想成**小区物业的定时巡检**：每次你进门（SessionStart）它先看一眼有没有新公告（仓库新版本），有就顺手更新，但每 6 小时最多跑一次，不会每次进门都大动干戈；没联网它就安静退下，不挡你路。

---

## 5. 运行时依赖与合规安装

`npx skills` / 仓库脚本**只负责把技能文件放到位，不会自动装运行依赖**。技能真正跑起来还差一层：Python 包、浏览器、MCP server、密钥。官方明示：按各技能 README 单独装（S1 §5.3；S5 §2.1）。

### 5.1 依赖速查

| 技能 / 组件 | 额外依赖 | 典型安装命令 |
|-------------|----------|--------------|
| `nature-paper-to-patent`（最重） | Python 依赖 + Playwright chromium | `pip install -r skills/nature-paper-to-patent/requirements.txt` |
| 同上（可选国知局检索） | CNIPA 附加依赖 + chromium | `pip install -r skills/nature-paper-to-patent/disclosure/requirements-cnipa.txt` + `python -m playwright install chromium` |
| `nature-academic-search`（MCP server） | MCP server 的 Python 依赖 | `pip install -r skills/nature-academic-search/mcp-server/requirements.txt` |
| `nature-figure` | R 后端可选；AI 示意图要 OpenRouter key | R 按需装；OpenRouter key 配置见技能 README |
| 通用 | Node.js ≥18、Python 3.x、Git | 见 §1.1 |

（CNIPA / MCP 依赖的具体相对路径以仓库内实际目录为准；`.../disclosure/...`、`.../mcp-server/...` 为官方文档缩写，安装时先 `ls` 确认。）

### 5.2 凭据与合规边界

- **`PUBMED_EMAIL`**：`nature-academic-search` 的 MCP server 需要配置一个真实邮箱（PubMed 对检索请求要求联系邮箱），按技能 README 提示设置即可。
- **Scopus / ScienceDirect**：用**本机已有的机构凭据/登录态**，不要把 key 写进仓库（S1 §5.3）。
- **OpenRouter key**：`nature-figure` 生成 AI 示意图走付费 API，费用与账号风险由使用者承担（S5 §2.1）。
- **`nature-downloader` 的「合法获取」**：它只负责在你已有权限的前提下帮你拿全文（图书馆 / CARSI / 开放获取），**账号与合规边界由使用者负责**——没有权限的文献它不该也不应绕过（S1 §5.3；S5 §5.2）。

> [!tip] 大白话
> 把 `PUBMED_EMAIL`、机构登录态、API key 想成**门禁卡**：技能是帮你刷卡的助手，但卡得是你自己的、且你得有进那扇门的权限。技能不负责替你「配钥匙」，更不会帮你翻墙进不该进的房间——配卡和门禁权限都是你自己的事。

### 5.3 一个「最小依赖闭环」示例

只跑读论文场景的话，最小闭环是 `nature-reader` + `nature-shared`，外加确认 Codex 会话能联网访问 PDF 即可，通常不需要装 Playwright。等用到 `nature-paper-to-patent` 这类重技能，再回来补 §5.1 的安装命令即可——**按技能补齐，别一上来全装**。

---

## 6. 安装验证与「开新会话」规则

### 6.1 装完必须开新会话

技能是在 **Codex 会话启动时**被发现的。装完 / 更新完技能，**必须开一个新的 Codex 会话**，再自然描述任务；在旧会话里继续聊，Agent 很可能根本看不到新技能（S1 §5.3；P2 §5 实践指导）。

### 6.2 最小验证三步走

**第 1 步：确认文件到位**

```bash
npx skills list --global --agent codex --json     # 看技能名与路径
ls ~/.codex/skills/nature-reader/SKILL.md         # 确认是整目录，不是单文件
```

**第 2 步：开新会话，丢一句官方模板提示词**——挑一个最贴近你工作的技能做冒烟测试。例如测 `nature-reader`：

```text
把这篇 PDF 做成图文对应的中英文对照 Markdown reader
```

（官方模板提示词见 S1 §4；更多模板在下一章。）

**第 3 步：确认产物形态**——看是否产出该技能承诺的产物，而不是空话：

| 技能 | 期望产物形态 |
|------|--------------|
| `nature-reader` | 图文对应、带来源锚点的 Markdown |
| `nature-paper2ppt` | `.pptx` |
| `nature-citation` | `.enw` / `.ris` / Zotero RDF + 浏览器 HTML |
| `nature-figure` | `.svg` / 图件文件 |

产物形态（`.md` / `.pptx` / `.svg` / `.enw`）冒烟通过，才算「真的能用」；只回了一段文字没有产物，先回查 §5 依赖是否漏装（P2 §5 实践指导）。

### 6.3 验证清单

- [ ] `node -v` ≥ 18、Codex 可运行
- [ ] 按决策树选了路线，技能装到预期路径（`~/.codex/skills/` 或 `.agents/skills/`）
- [ ] 依赖技能（`nature-shared`）一起装了
- [ ] 运行时依赖按技能 README 补齐（含 `PUBMED_EMAIL` 等凭据）
- [ ] **开了新会话**，官方模板提示词冒烟通过，产物形态正确
- [ ] 保留的是完整技能目录，不是只拷了 `SKILL.md`

---

## 本章小结

- **两条路线互补**：1–3 个技能用 `npx skills` 按需点菜（记着带 `nature-shared`）；整库跟上游用 `update-codex-skills.sh`；要自动更新再加 SessionStart hook。
- **命令矩阵核心**：`add --global --agent codex --skill '*' --yes --copy` 全量装；省略 `--global` 是项目级；`list --global --agent codex --json` 核对；`update` / `remove` 都支持 `--global` / `--project` / `--all` 作用域。
- **名字用 frontmatter name**：`nature-proposal-writer` 目录的触发名是 `researchwrite`；`list` 显示的就是这个名字。
- **路径**：全局 `~/.codex/skills/`，项目级 `.agents/skills/`；Windows 优先 `--copy`，`update-codex-skills.sh` 依赖 rsync 需实测。
- **运行时依赖不会自动装**：Python 包 / Playwright chromium / MCP server / `PUBMED_EMAIL` / 机构凭据按各技能 README 补齐，合规与账号边界归使用者。
- **装完开新会话再验证**：`list --json` + 官方模板提示词冒烟，确认 `.md` / `.pptx` / `.svg` / `.enw` 产物形态。

**下一章预告**：装好之后怎么「用得对」？第四章「典型科研场景实操」给出官方 8 类场景的可复制提示词、技能→场景映射，以及一条从 PDF 到引文产物的端到端工作流解剖。

---

> 本章素材来源：S1（nature-skills 官方 README §5.1/§5.3）、S2（vercel-labs/skills CLI 文档）、S5（zhang-yd 项目解读 §4.2/§5.1）。
