## 第四章 对照迁移 — 从 Claude Code 一键导入

第三章讲到 Hermes 能**直接识别**项目里已有的 `CLAUDE.md` / `.cursorrules`，但那是"单个文件被顺手复用"。如果你的整套 Claude Code 配置——全局指令、`settings.json` 权限、MCP 服务器、skills——都要搬到 Hermes，手动照前两章的对照表一个个誊抄既慢又容易漏。这一章教你用 `hermes import-agent claude-code` 一条命令完成迁移，并讲清它**导什么、怎么导、坚决不导什么**（密钥永不导入），让你迁移后心里有底。

### 4.1 导入映射表：你的每个配置去了哪

`hermes import-agent claude-code` 读取 `~/.claude`，把 Claude Code 的各类配置按一张固定映射表搬进 Hermes。[^c4-1] 先记住一句话：**它不是魔法，而是照着映射表搬运**——每一类配置都有明确的落点：

| Claude Code（`~/.claude`） | Hermes 落点 | 说明 |
| --- | --- | --- |
| `CLAUDE.md`（**全局**指令） | `~/.hermes/memories/MEMORY.md` 记忆条目 | 注意是**记忆条目**，不是 `SOUL.md` |
| `settings.json` → `permissions.allow`（`Bash(...)` 规则） | `config.yaml` → `command_allowlist` | 只导 `Bash(...)`，非 Bash 规则见 4.3 |
| `settings.json` → `permissions.deny`（`Bash(...)` 规则） | `config.yaml` → `approvals.deny` | 同上，只导 Bash 类 |
| `mcpServers`（来自 `~/.claude.json` **和** `settings.json`） | `config.yaml` → `mcp_servers` | 来源是**两个文件**，不是只看 settings.json |
| `skills/<name>/`（含 `SKILL.md` 的目录） | `~/.hermes/skills/claude-code-imports/<name>/` | 逐个 skill 目录整体拷入 |
| `commands/*.md`（斜杠命令） | **跳过**，附提示 | 官方建议：把它们转成 skill |

两个容易看走眼的地方：

- **全局 `CLAUDE.md` 不会变成 `SOUL.md`。** 第二章说过 `SOUL.md` 是"身份"，它只在缺省时自动 seed、已有文件永不覆盖——导入器不会动它。你在 `~/.claude/CLAUDE.md` 里写的全局指令会被变成 `MEMORY.md` 的记忆条目，在系统提示组装时以记忆快照（slot #5）注入。也就是说：**身份不迁移，全局指令迁移为记忆**。
- **`commands/*.md`（斜杠命令）默认不迁移。** 它只报告"已跳过"，并建议你把常用斜杠命令改造成 skill。如果你依赖大量 slash commands，这一步需要手工整理。

> [!tip] 大白话
> 把 `import-agent` 想成**搬家公司照着清单搬家**：你的每个"物件"（全局指令、权限、MCP、skills）都有固定的新房间（`MEMORY.md`、`config.yaml`、`~/.hermes/skills/...`）。所以它不会猜，只会按 4.1 这张对照表一件件放好——你提前知道每件东西去了哪，就不会搬家后找不到。

先睹为快，完整命令族如下（逐条拆解见 4.2–4.4）：

```bash
hermes import-agent                      # 自动探测 ~/.claude 或 ~/.codex
hermes import-agent claude-code          # 从 ~/.claude 导入
hermes import-agent codex                # 从 ~/.codex 导入
hermes import-agent claude-code --dry-run          # 仅预览，不写任何文件
hermes import-agent codex --source /path/to/.codex # 自定义源目录
hermes import-agent claude-code --overwrite --yes  # 覆盖冲突 + 跳过确认
```

（`codex` 分支同理，映射表见官方文档，本章聚焦 `claude-code`。）

### 4.2 导入行为：预览优先、合并而非替换

导入器和 `hermes claw migrate` 一样遵循 **preview-first（预览优先）** 模式：执行任何写入前，先打印一份**逐条计划**；`--dry-run` 永远不碰磁盘。[^c4-1]

```bash
# 第一步永远是预览：看清单，不落盘
hermes import-agent claude-code --dry-run

# 确认无误后再真正导入（交互式会逐条确认）
hermes import-agent claude-code

# 非交互环境（CI/脚本）：必须显式 --yes 才会越过预览继续
hermes import-agent claude-code --yes
```

四条核心行为，导入报告的"注意"区就靠它们解读：[^c4-1]

| 行为 | 含义 | 你要做的 |
| --- | --- | --- |
| **Preview first, always** | 先打印完整计划；非交互会话**停在预览**，除非传 `--yes` | 先 `--dry-run` 看清单，再正式导入 |
| **Merges, not replaces** | 记忆条目与已有 `MEMORY.md` **去重**；allow/deny 模式与 `config.yaml` 现有内容**合并** | 不会清空你已有的记忆和权限，可放心重复跑 |
| **Conflicts skipped by default** | 已存在的 MCP server / skill 报为 **conflict 并跳过** | 想覆盖就加 `--overwrite` |
| **Malformed files don't abort** | 坏掉的 `settings.json` 变成报告里的**单条错误**，其余照常导入 | 看到单条 error 不必慌张，修好对应文件再重跑即可 |

> [!tip] 大白话
> 把"合并而非替换"想成**往同一个本子上追加笔记**：记忆条目如果跟原来重复就不抄第二遍，权限清单是"添加上去"而不是"先把原来的擦掉"。所以这条命令是**安全的增量操作**，放心用它，最多是清单多几行，不会毁掉你已有的 Hermes 配置。

### 4.3 Bash 前缀规则转 glob

Claude Code 的权限规则长这样：`Bash(npm run test:*)`——括号里是**命令前缀**，意思是"允许/拒绝一切以 `npm run test:` 开头的命令"。Hermes 不用前缀匹配，用的是 **glob（通配符）**，所以导入器会自动做一次翻译：[^c4-1]

| Claude Code（前缀） | Hermes（glob） |
| --- | --- |
| `Bash(npm run test:*)` | `npm run test*` |

翻译规则拆开看：

- `Bash(...)` 外壳被剥掉——Hermes 的 `command_allowlist` / `approvals.deny` 本来只管命令，不需要 Bash 包装。
- 前缀里的 `:` 按 glob 语义处理：`npm run test:*` 变成 `npm run test*`（`*` 匹配任意字符，包括 `:` 之后的整段）。
- `settings.json` 里 `permissions.allow` 的 Bash 规则 → `command_allowlist`；`permissions.deny` 的 Bash 规则 → `approvals.deny`。

**非 `Bash(...)` 的权限规则不会被导入。** `Read(...)`、`WebFetch` 这类规则拦的是 Claude 专用工具，Hermes 里没有一一对应物，所以导入报告会标成 **unmapped（未映射）** 而非导入。[^c4-1]

> [!tip] 大白话
> 把 `Bash(npm run test:*)` 想成**门禁卡上写的一句话**："所有以 `npm run test:` 开头的命令都放行"。Hermes 的保安不认"句子"，只认**通配符清单**，于是导入器把这句话翻译成门禁表里的一行 `npm run test*`。同一个意思，换了一种写法——`Read` / `WebFetch` 这种"别的门的钥匙"在 Hermes 没有对应的门，就被标注"此物未映射"，而不是硬塞进来。

### 4.4 凭证永不导入：密钥要自己补

这是迁移**最重要**的一条边界。[^c4-1]

> [!warning] 凭证安全
> **API 密钥和凭证永不导入。** 凭证文件（`~/.claude/.credentials.json`、`~/.codex/auth.json`）**根本不会被读取**；MCP server 的环境变量或 header 中凡是名字看起来像密钥的（`*_TOKEN`、`*_API_KEY`、`Authorization` 等）都会被**剔除**，并在导入报告里**逐条列出**，让你有意识地重新加回。这样做的目的是防止密钥被静默复制进 Hermes 配置文件——要加，就得你亲手、明确地加。

被剔除的密钥怎么补？官方给了两条路：[^c4-1]

```bash
# 方式一：手动写进 .env
# 先用命令确认 .env 路径（通常是 ~/.hermes/.env）
hermes config env-path
# 然后编辑该文件，例如：
#   ANTHROPIC_API_KEY=sk-ant-...
#   YOUR_MCP_SERVER_TOKEN=...

# 方式二：交互式引导补全
hermes setup          # 完整向导（首次运行/重配，当前值作默认，回车保留）
hermes setup model    # 只补模型/provider 段
```

> [!tip] 大白话
> 把 `.credentials.json` 想成**保险箱**：搬家公司根本不打开它，也不把里面的钱搬走。他们只会在清单上写"这个保险箱你没搬"，并把保险箱外壳上贴的标签（`*_TOKEN`、`*_API_KEY`）念给你听——意思是"这些钥匙你回头自己放进 Hermes 的保险柜（`~/.hermes/.env`）"。**所以：迁移永远不会替你保管密钥，也永远不会让你的密钥躺进别人的配置文件。**

### 4.5 导入后核对清单

跑完导入，对照这份清单逐项验收（前几项靠导入报告，后几项靠命令验证）：

- [ ] **报告逐条看一遍**：哪些条目会写入、哪些被跳过（`commands/*.md`）、哪些标了 `unmapped`、哪些密钥名被剔除。
- [ ] **记忆已合并**：`~/.hermes/memories/MEMORY.md` 里出现了新记忆条目，且与原有条目去重（不重复）。
- [ ] **权限已合并**：`config.yaml` 的 `command_allowlist` / `approvals.deny` 已包含翻译后的 glob（用 `hermes config get` 抽查，如 `hermes config get command_allowlist`）。
- [ ] **MCP 已列出**：`config.yaml` → `mcp_servers` 有对应 server；同时确认其**密钥名**（`*_TOKEN` / `*_API_KEY` / `Authorization`）确实没被带入。
- [ ] **skills 已落位**：`~/.hermes/skills/claude-code-imports/<name>/` 目录存在；报告里的 conflict 项，决定是否用 `--overwrite` 重跑。
- [ ] **斜杠命令被跳过**：`commands/*.md` 未迁移；把常用的那几个转成 skill（`hermes skills`）。
- [ ] **密钥已手工补**：`~/.hermes/.env`（`hermes config env-path` 确认路径）或 `hermes setup model`。
- [ ] **基础验证**：`hermes doctor` 无致命错误（第六章会系统讲验证命令族）。

> [!summary] 本章小结
> - `hermes import-agent claude-code` 按一张固定映射表迁移：全局 `CLAUDE.md` → `MEMORY.md` 记忆、`Bash(...)` 权限 → `command_allowlist` / `approvals.deny`、`mcpServers` → `mcp_servers`、skills → `~/.hermes/skills/claude-code-imports/`，`commands/*.md` 跳过。
> - 行为是**预览优先 + 合并而非替换**：先 `--dry-run` 看计划；记忆去重、allow/deny 合并；冲突默认跳过（`--overwrite` 覆盖）；坏文件只报单条错误，不中止整体导入。
> - `Bash(npm run test:*)` 这类**前缀规则**会被翻译成 glob `npm run test*`；`Read(...)` / `WebFetch` 等非 Bash 规则标注 **unmapped**，不导入。
> - **凭证永不导入**：`.credentials.json` 不读、密钥名（`*_TOKEN` / `*_API_KEY` / `Authorization`）剔除并列出，由你手动补到 `~/.hermes/.env` 或 `hermes setup`。
> - 迁移完按 4.5 核对清单验收，重点确认密钥没有静默流入配置。

**下一步**：配置导进来只是起点——导入的 `config.yaml` 里其实还有一大块没讲的能力：**hooks**。下一章进入第五章，用 `config.yaml` 的 `hooks:` 配置 shell hooks，实现对危险命令的拦截与自动化。

[^c4-1]: [Import from other agents | Hermes Agent](https://hermes-agent.nousresearch.com/docs/user-guide/import-from-other-agents) — 映射表、导入行为、Bash 前缀转 glob、凭证永不导入
[^c4-2]: [CLI Commands Reference | Hermes Agent](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/reference/cli-commands.md) — `hermes import-agent` 选项、`hermes setup`、`hermes config env-path`
