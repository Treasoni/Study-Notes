# 02 深度素材 — REA: Reverse Engineer Anything

> ⚠️ **本文件是中间产物**：引文与数值请回 `sources/` 按行号核对，不要当成权威引用。
> 逐字引文与数值已在 P2 重新核对；下游（大纲 / 写作）引用前仍需回源。
> 主题：REA: Reverse Engineer Anything（`morluto/rea`）｜运行标识：`rea-reverse-engineering`
> 方向：C 概念 + 实战混合｜阶段：P2 深度收集｜日期：2026-10-13
> 自检命令：`python3.12 .claude/scripts/note-citation-check.py workspace/rea-reverse-engineering --mode verbatim --file 02_deep_research.md`

---

## 1. 范围与选择

- **方向 C（概念 + 实战混合）**：先讲清「REA 是什么、解决什么问题」，再给可跟做的零原生引擎实战路径，最后带一遍 provider/平台/安全边界。
- **信源口径**：**官方一手**（README 中英、`docs/*.md`、`rea.tools` 指南与案例的渲染正文）。社区教程/评测在 P1 仅 `snippet-only`，**未抓正文、不作为证据**。
- **零原生引擎主线**：静态 JavaScript/Electron 分析 + 网站（浏览器观测），两者都不需要 Hopper/Ghidra/IDA。
- **方法**：父流程 `curl` 落盘 → 子代理按透镜提取 claim + 行号 → 父流程**重新计数、逐字回源**。
- **P2 抓取规模**：有效来源 20 条（其中 `snippet-only` 未采信者不计入证据），下节开列。

---

## 2. 来源清单

| ID | 文件 | tier | 形态 | 用途 |
| --- | --- | --- | --- | --- |
| S1 | `sources/README.md` | official | fetched | 定位、快速开始、22 行目标表、FAQ、免责 |
| S2 | `sources/README_zh.md` | official | fetched | 简体中文对照（目标表少 3 行，见 §4） |
| S3 | `sources/docs_index.md` | official | fetched | 文档索引、指南分诊表 |
| S4 | `sources/docs_installation.md` | official | fetched | 安装/接入、支持客户端表、Hopper/Ghidra、Node 要求 |
| S5 | `sources/docs_cli.md` | official | fetched | CLI 命令面、snapshot、evidence、退出码 |
| S6 | `sources/docs_mcp-contracts.md` | official | fetched | MCP 会话/工具契约、generated catalog 位置 |
| S7 | `sources/docs_javascript-application-workflows.md` | official | fetched | JS 应用的视图/追踪/对比契约 |
| S8 | `sources/guide_javascript.txt` | official | rendered | 指南：Electron CSV 导出（端到端实战） |
| S9 | `sources/guide_browser.txt` | official | rendered | 指南：浏览器观测「点一下发生了什么」 |
| S10 | `sources/showcase_notion.txt` | official | rendered | 案例：Notion 剪贴板桥 |
| S11 | `sources/docs_browser-observation.md` | official | fetched | CDP 观测规范与边界 |
| S12 | `sources/docs_ghidra-provider.md` | official | fetched | Ghidra provider 语义与平台限制 |
| S13 | `sources/docs_ida-provider.md` | official | fetched | IDA adapter 语义与已验证平台 |
| S14 | `sources/DISCLAIMER.md` | official | fetched | 合法用途白名单与禁项 |
| S15 | `sources/docs_roadmap.md` | official | fetched | 方向与准入标准（辅助） |
| S16 | `sources/SECURITY.md` | official | fetched | 安全边界：能力令牌、非沙箱声明 |
| S17 | `sources/docs_process-capture.md` | official | fetched | 进程捕获的主机前提 |
| S18 | `sources/docs_website-module-trace.md` | official | fetched | 网站模块追踪（补充） |
| S19 | `sources/site_root.txt` | official | rendered | `rea.tools` 首页文本 |
| S20 | `sources/site_guides.txt` | official | rendered | 指南索引页文本 |
| — | `01_explore_result.md` | 中间产物 | — | P1 线索，**不作为证据** |

> 未采信（**不得引用**）：P1 中的 C5（skills.sh 社区页）、C6（社区教程 `snippet-only`）。

---

## 3. 关键事实与 claim ↔ 来源对照

### 3.1 这是什么、解决什么问题

- **一句话定位**：REA 是一个 **MCP server + CLI**（npm 包 `rea-agents`），把逆向工程能力接给 AI agent；官方定位句（S1:7）：

  > “One MCP for reverse engineering across binaries, applications, and runtime behavior.”

  中译：**一个 MCP，覆盖二进制、应用程序与运行时行为三层的逆向分析。**

- **落点（官方原话，S1:52）**：

  > “Analysis runs locally, and results include the evidence and limitations behind each conclusion.”

  中译：**分析在本机运行，结果附带支撑每条结论的证据与局限。**

- **工作方式**（S2:121 / S1 对应段）：agent 经 MCP 调 REA → REA 检查目标并追踪相关代码 → 返回「发现 + 证据」→ agent 据此提问、解释行为，或编写并测试实现。CLI 复用同一套工作流。
- **典型价值主张**（S1:50）：看到一个想抄的功能，让 agent 用 REA 调查它——即使没有源码，也能检查、解释、给出证据，并为你的项目实现类似功能。

**术语首现解释（供写作直接用）**
| 术语 | 一句话白话 |
| --- | --- |
| 逆向工程 | 没有源码，也把软件「拆开看清楚」它是怎么做的 |
| MCP | Model Context Protocol，让 AI agent 调用外部工具的一套标准插口 |
| 证据 / 局限（Evidence / limitation） | REA 不只给结论，还给出「凭什么这么说」和「哪里说不准」 |
| 静态分析 | 只读文件、不运行程序 |
| 运行时捕获 | 真的把程序/浏览器跑起来，记录它的行为 |

### 3.2 可分析目标（22 行总表）

来源：S1:153–176。**重新计数：英文 README 目标表 = 22 行数据行**（`Native binaries` … `Process behavior`）；简体中文 S2:133–153 = 19 行（差异见 §4）。

| # | 目标 | REA 返回 | 要求 / 指南 |
| --- | --- | --- | --- |
| 1 | 原生二进制 | 伪代码、汇编、字符串、符号、调用与引用 | Hopper / Ghidra / IDA |
| 2 | 离线 ELF 布局 | 节、段、原始符号/重定位、静态防护候选项 | Linux x64 上调用方提供 pwntools |
| 3 | Go 二进制 | 内嵌编译版本、模块、替换、构建设置 | **内置静态** ELF/PE/thin Mach-O，无需装 Go |
| 4 | WASM 制品 | 校验、节、精确 import/export WAT、解码 WAT | 调用方提供 WABT 1.0.42 |
| 5 | EVM 字节码 | 分派选择器、字节偏移、推断参数、可变性 | Linux x64 本地原始/十六进制载体 |
| 6 | SQLite 数据库 | 表、列、索引、视图、触发器、抽样行 | 本地库/WAL 快照；Node 24.x≥24.15 或 26+ |
| 7 | 已记录的 Linux 崩溃 | 原始 note、各线程寄存器/信号、映射候选项 | Linux x64 pwntools；可选 GDB/pwndbg |
| 8 | JavaScript / Electron | 模块、导入、source map、路由、IPC、原生扩展关系 | 仅需 Node.js 和 npm |
| 9 | 网站 | 页面结构、脚本、网络观测、按需截图 | Chrome 系浏览器 |
| 10 | 已保存的网络捕获 | 请求、响应、可访问载荷、来源位置 | HAR / Fiddler SAZ；原生 mitmproxy 需 Linux |
| 11 | .NET 程序集 | 元数据、CIL 指令、声明的原生依赖、构建对比 | **无（纯静态）** |
| 12 | Android APK | 清单声明、类、反编译方法、引用 | 无界面 JADX + 完整 JDK（Linux/macOS/Windows x64） |
| 13 | Android 设备 | 设备、包、进程、日志、转储、截图、APK/文件传输 | 调用方提供 adb |
| 14 | JEB 项目 | 引擎支持的项目单元、制品摘要、类型/方法伪代码 | 调用方启动的 JEB MCP 客户端（`REA_JEB_MCP_URL`） |
| 15 | Android 资源 | 解码清单、字符串表、语言区域、版本信息 | 调用方提供 Apktool |
| 16 | Flutter 应用 | Dart 快照哈希、按 ABI 的库摘要、引擎构建溯源 | **无（静态 APK 解析）** |
| 17 | 固件 | 分区、提取结果、转交原生分析 | Linux 上 Binwalk / Unblob |
| 18 | 录制的数据包 | 指定字段、重复值、过滤条件、解码规则 | Linux：TShark 4.x + prlimit |
| 19 | 数据包摘要 | 端点、DNS、TLS SNI、协议分布、HTTP 请求 | 调用方提供 tshark / capinfos |
| 20 | 录制的逻辑信号 | 解码注释、样本范围、诊断信息 | Linux：sigrok-cli 0.7.2 + prlimit |
| 21 | 软件包与资源 | 文件清单、摘要、plist、Apple bundle 结构、提取资源 | 制品 / Apple 应用指南 |
| 22 | 进程行为 | 终端输出、交互、退出与文件系统观测、运行对比 | Linux/macOS 带原生 PTY |

**分组记忆（给小白）**：① 纯静态、零引擎也能跑——JS/Electron（8）、.NET（11）、Go（3）、Flutter（16）、SQLite（6）；② 需要浏览器——网站（9）；③ 需要额外工具/引擎——其余原生与嵌入式目标。笔记可在 §3.7 只展开第 ① ② 组。

### 3.3 Node 与包（硬门槛）

- **Node 要求**（S4:848 / S1:131 一致）：

  > “REA supports Node.js 22.x (>=22.19), 24.x (>=24.11), and 26+. Node.js 23, 25, and prereleases are unsupported.”

  中译：**支持 Node 22.x(≥22.19) / 24.x(≥24.11) / 26+；23、25 与预发布版不支持。**（含 `>=`，脚本按体例不逐字校验，但行号已锁。）
- **npm 最新版**：`rea-agents` **6.4.0**（发布检查日 **2026-10-11**，S4:207）。`bin` 提供 `rea` 与 `rea-agents`。
- **持久化注册的版本纪律**（S4:811）：

  > “Persistent registrations should use one exact package version.”

  中译：**写进 agent 配置的注册应锁定一个确切包版本**（避免 `@latest` 漂移）。

### 3.4 安装与接入

- 首跑（S1:65 / S4:17）：`npx rea-agents setup`。
- 交互与确认（S4:20–22）：先选 agent → 复核计划路径与改动 → 批准；npm 的包下载批准与 REA 的 setup 批准是**两次独立确认**，setup 写文件或装 Hopper 前都会先问。

  > “Choose the agents to configure, review the proposed paths and changes, and approve the plan.”

  中译：**先选要配置的 agent，复核计划的路径与改动，再批准该计划。**

- 写配置时的安全行为（S1:68–70）：

  > “Setup adds REA's MCP server and matching workflow instructions, with backups of existing configuration. Restart your agent afterward.”

  中译：**setup 会加入 REA 的 MCP 服务和配套工作流指引，并备份原有配置；完成后重启 agent。**

- **支持客户端表**（S4:266–288，**重新计数 = 21 行数据行**）：Claude Code、Claude Desktop、Codex、Cursor、Gemini CLI、Windsurf、Devin、OpenCode、Antigravity、GitHub Copilot CLI、Command Code、Qwen Code、VS Code、Grok Build、OMP、Pi、Hermes、Qoder、Trae、ZCode、DeepSeek Harness（`dsh`）。其中 `dsh` 为 **main-only，npm 6.4.0 不含**（S4:290）。
- **手动注册 MCP**（S4:799–806）：`mcpServers.rea` = `npx -y rea-agents@6.4.0 mcp`。

### 3.5 CLI 命令面与证据/退出码

- **入口**：`rea --help`；不装全局可用 `npx -y rea-agents@latest <command>`（S5:9–14）。
- **命令清单**（S5 全文，行号为锚点）：

| 命令 | 用途 | 锚点 |
| --- | --- | --- |
| `analyze-javascript-application PATH --json` | 静态 JS/Electron 分析（目录或 `.asar`） | S5:13 |
| `inspect-analysis-view VIEW.json` | 投影大证据到摘要/模块页 | S5:30 |
| `inspect-managed-artifact / inspect-managed-members` | .NET：元数据与 CIL，不执行程序集 | S5:48–50 |
| `inspect-sqlite-database PATH [--table N --row-limit 20]` | SQLite 快照，无需原生引擎 | S5:67 |
| `inspect-go-binary PATH` | Go 构建元数据，无需装 Go | S5:79 |
| `analyze / search / function / decompile / xrefs / trace --provider X` | 原生分析六件套 | S5:91–96 |
| `providers --json` / `capabilities --json` | 列能力与 provider | S5:115–116 |
| `doctor --provider ID --json` | 诊断引擎就绪 | S5:143 |
| `evidence-import / evidence-export / compare` | 证据包校验、导出、对比 | S5:198–200 |
| `import-reference-source PATH` | 导入历史源码用于对比（Linux/macOS） | S5:214 |
| `list-browser-targets` / `inspect-web-page` | 浏览器观测（见 §3.7） | S5:245 / S9 |

- **输出与退出码**（S5:254–266）：默认终端格式为 **TOON**；`--json` 在终端缩进、被管道/重定向时紧凑。退出码：`0` 完成（可能含部分证据/警告/未决项）、`1` 未能完成、`128+N` 被信号 N 终止。`setup --dry-run` 返回 `planned` 且退出 `0`；取消 setup 也退出 `0`。
- **会话模型**（S6:681 «Generated catalog» 指向构建期生成的工具目录）：工具/命令全集以 **connected server 的实际工具列表**为准，而非文档快照。

### 3.6 Provider 与平台限制

- **需不需要引擎**（S1:178）：

  > “Static JavaScript and .NET inspection read the supplied files without running the application.”

  中译：**静态 JavaScript 与 .NET 检查只读所给文件，不运行应用。**
- **Ghidra**（S12:3–5）：

  > “REA imports one target into an ephemeral Ghidra database. Linux/macOS support read-only analysis and atomic function-name/entry-comment edits; Windows P0 is read-only.”

  中译：**REA 把单个目标导入临时 Ghidra 库；Linux/macOS 支持只读分析与函数名/入口注释的原子修改，Windows P0 仅只读。**（S12:5 / 安装文档 L513：`Windows P0 remains read-only`。）
- **IDA**（S13:3）：

  > “REA adapts an existing IDA MCP server into its native analysis tools.”

  中译：**REA 把既有的 IDA MCP server 适配成自己的原生分析工具**（REA 不安装/升级/激活/授权 IDA）。已验证组合（S13:143、145）：Windows x64 headless 用 **IDA 9.3**；macOS arm64 用 **IDA 9.1**；原生 Windows 用 **IDA Pro 9.3**。其余平台/版本**未声称支持**。
- **Hopper**：独立商业软件，有自己的许可与免费 demo；出现在支持的原生宿主基线（macOS 12+ / Ubuntu 24.04+ / Fedora 41+ 等，S4:310）。REA 会复用已装 Hopper 并在卸载时保留它。
- **其他平台限制**（S1:186 附近 / 各指南）：
  - 进程行为捕获当前**需 Linux 或 macOS**且要有原生 PTY 后端（S17:17–21）："Capturing a new scenario currently requires Linux or macOS and a working native PTY backend."，中译：**当前捕获新场景需要 Linux 或 macOS 以及可用的原生 PTY 后端**；原生 Windows 不可用。
  - 固件（Binwalk/Unblob）、EVM、部分抓包路径限 **Linux**。
- **provider 选择**（S5:123–131）：只有一个可用 provider 时自动选；多个时用 `--provider` 显式指定，`REA_ANALYSIS_PROVIDER` 设默认，MCP 里传 `provider_id`。

### 3.7 实战路径（零原生引擎）

**路径 A — 静态 JS/Electron（推荐首跑）**，来源 S8（Electron CSV 导出指南）：

1. 目标：一个小 Electron 应用，点「导出笔记」会把笔记写成 CSV，行为跨 `renderer.js → preload.js → main.js`。
2. 命令（S8:150–151）：

   ```bash
   npx -y rea-agents@latest analyze-javascript-application \
     /absolute/path/to/notes-example --json
   ```

3. 期望结果（S8:105–113，REA 4.1.0 记录）：

   ```json
   {
     "literal_channels": 1,
     "renderer_transmissions": 1,
     "main_handlers": 1,
     "paired_renderer_transmissions": 1,
     "ambiguous_renderer_transmissions": 0
   }
   ```

   读法：**1 个字面 IPC 频道 + 1 个匹配的主进程 handler**，位于 `normalized_result.summary.ipc`；源码位置在 `normalized_result.graph`（S8:155–156）。
4. 结论链：REA 把字面 IPC 调用与唯一匹配的 handler 配对，并识别被暴露的 API；路径由代码推断，运行时捕获可再校验「实际执行了什么」（S8:46–48）。
5. 大应用注意（S5:23–31）：完整证据可能达数百 MB（示例：334 MB 的 Obsidian 证据 → 摘要视图约 10 KB），先落盘再 `inspect-analysis-view` 投影。

**路径 B — 网站/浏览器观测（次跑）**，来源 S9：

1. 用独立 profile 起 Chrome 远程调试（S9:57–60）：

   ```bash
   google-chrome --remote-debugging-port=9222 \
     --user-data-dir=/tmp/rea-notes-browser \
     https://rea.tools/examples/notes-web/
   ```

2. 找页面 target ID（S9:92–93）：

   ```bash
   npx -y rea-agents@latest list-browser-targets http://127.0.0.1:9222 --json
   ```

3. 观测窗口内点「Export notes」（S9:101–105）：

   ```bash
   npx -y rea-agents@latest inspect-web-page \
     http://127.0.0.1:9222 TARGET_ID \
     --observation-ms 10000 \
     --include-accessibility-text \
     --include-json-body-shapes --json
   ```

4. 期望结果（S9:121–137）：请求 `GET /examples/notes-web/notes.json`、响应 `200 · application/json`、发起脚本 `export.js`、响应结构 `notes[]`（含 `id`、`title`）。结论：**这次点击请求了 `notes.json`**，CSV 由 `export.js` 构造（S9:152–162）。

**路径 C — 进阶（可选，非零引擎）**：`.NET` 用 `inspect-managed-artifact/-members`（S5:48–50）、`SQLite` 用 `inspect-sqlite-database`（S5:67）、`Go` 用 `inspect-go-binary`（S5:79）。三者都**不需要** Hopper/Ghidra/IDA。

### 3.8 边界与安全

- **合法用途白名单**（S14:5–10）：

  > “security research, malware and incident analysis, vulnerability research and coordinated disclosure, CTFs and education, interoperability, software preservation, and debugging or auditing software you own or are authorized to examine.”

  中译：**安全研究、恶意软件与事件分析、漏洞研究与协调披露、CTF 与教学、互操作性、软件保存，以及对你拥有或获授权检查的软件做调试/审计。**
- **明令不帮的用途**（S14:11–18）：绕过 DRM/许可校验/反作弊；做游戏外挂或篡改在线服务；未授权绕过认证/机器人防护/访问控制；抄专有软件或复现其受保护代码资产；规避 AI 模型供应商的使用政策；转售/共享 AI 账号或 API。
- **非沙箱声明**（S16:33–34）：

  > “This is not a sandbox and does not protect against malicious processes already running as the same operating-system user.”

  中译：**这（能力令牌机制）不是沙箱，不能防御已经以同一操作系统用户身份运行的恶意进程。**
  安全边界机制（S16:27–32）：Hopper/Ghidra 桥用**每会话随机能力令牌**；POSIX 走当前用户 Unix socket；令牌经私有会话描述符传递，不走进程参数或环境变量。
- **本地性 / 不上传**（S1 FAQ）：REA 在本机分析目标；agent 收到工具结果，其模型供应商有自己的数据政策。
- **浏览器观测边界**（S11:9 / S11:229）：

  > “This is a passive reverse-engineering capability, not a general browser automation or remote-control surface.”

  > “This feature is not a browser sandbox or network containment mechanism.”

  中译：**这是**被动**式逆向能力，不是通用浏览器自动化/远程控制面**；**它不是浏览器沙箱，也不做网络隔离**——建议用专用 profile、只纳入你要检查的 origin。
- **静态图不执行代码**（S7:303）：

  > “Static graph workflows do not execute recovered code.”

  中译：**静态图工作流不会执行恢复出来的代码。**

### 3.9 生态与路线图（辅助）

- **MCP Registry**（S4:786–792）：官方注册名 `io.github.morluto/rea`；注册表客户端装的仍是公开 npm 包 `rea-agents`，不引入第二分发物。
- **路线图**（S15）：平台、进程/Hopper、浏览器三条 tracker；优先级含「扩展原生架构/类型/间接调用验证」「打通静态发现与运行时观测」「改进混淆托管代码对比」「扩展进程/协议/文件系统/构建对比覆盖」。准入标准（S15）要求新能力经共享 CLI/MCP 交付证据、保留观测与未知、声明真实权限与生命周期。

---

## 4. 冲突与存疑（已记录，不采信不确定项）

| # | 现象 | 处理 |
| --- | --- | --- |
| 1 | **目标表行数：英文 22 行 vs 中文 19 行**（S1:153–176 / S2:133–153）。中文缺 Go 二进制、WASM 制品、SQLite 数据库 3 行 | 以**英文 README 为准（22 行）**；中文表未同步，写作不据此删目标 |
| 2 | **「17 client IDs」vs 支持客户端表 21 行**（S4:209 vs S4:266–288） | **作用域不同**：21 行是「setup 可配置的客户端」；17 是「6.4.0 该版本注册表包实际通过 dry-run 计划检查的 client ID」（S4:209–212）。**不是矛盾**，写作时须分别表述，勿混为「支持 17/21 个」 |
| 3 | **星标数冲突**：社区来源互矛盾（约 22k–115k），与官方 API 快照（180,692 @2026-10-13）亦不一致 | **本笔记不采用任何星标数**；若要提热度，只说「活跃维护」并给 `pushed_at` 日期 |
| 4 | `dsh`(DeepSeek Harness) 在客户端表中，但 npm 6.4.0 不含 | 表述为「main 分支已支持，需等 6.4.0 之后的版本」 |

---

## 5. 未决问题（P2 → P3 前可知，写作时回避或标注）

1. `docs/mcp-contracts.md` 的 **generated catalog** 为构建期产物，未取全量表；MCP 工具全集以**运行时** server 工具列表为准（S6:681）。
2. **Hopper provider 无独立 `hopper-provider.md`**：其语义散在 `installation.md#hopper`，未单独抓全；写作如需 Hopper 细节需回该节补。
3. **浏览器观测在 macOS/Windows 的具体操作差异**未单列（指南给的是 Linux 命令 + 「用你平台的可执行路径」，S9:62）。
4. `site_root.txt` / `site_guides.txt` 为 HTML→文本渲染，**行号不稳定**，仅作叙述参考、不作引文出处。

---

## 6. 下游交接（给 outline-generator / chapter-writer）

- **建议章节骨架（对应方向 C）**：
  1. 这是什么、解决什么问题（§3.1）
  2. 能分析什么：22 类目标全景（§3.2）
  3. 装与接：`setup` → MCP/CLI（§3.3、§3.4）
  4. 实战一：静态 JS/Electron（§3.7 路径 A）
  5. 实战二：网站/浏览器观测（§3.7 路径 B）
  6. 进阶：provider 与平台限制（§3.6）
  7. 边界与安全（§3.8）
  （可选）附录：CLI 速查（§3.5）
- **强制口径（跨章冻结）**：
  - 目标类型总数 **22**（英文 README）；「17 client IDs」与「21 支持客户端」**不得混述**。
  - Node：`22.x(≥22.19) / 24.x(≥24.11) / 26+`；**23、25 不支持**。
  - npm 版本：`rea-agents 6.4.0`（2026-10-11）。
  - `dsh`：main-only，npm 6.4.0 不含。
  - 零原生引擎目标：JS/Electron、.NET、Go、Flutter、SQLite。
  - **不使用任何星标数**。
- **写作纪律**：正文成句英文引文**必须给中译**，章末留「引文对照（原文/中译/出处）」表；出处取下表 `sources/...:<行号>`。

---

## 7. 英文引文对照（原文 / 中译 / 出处）

| # | 原文（英文） | 中译 | 出处 |
| --- | --- | --- | --- |
| 1 | “One MCP for reverse engineering across binaries, applications, and runtime behavior.” | 一个 MCP，覆盖二进制、应用程序与运行时行为三层的逆向分析。 | `sources/README.md:7` |
| 2 | “Analysis runs locally, and results include the evidence and limitations behind each conclusion.” | 分析在本机运行，结果附带支撑每条结论的证据与局限。 | `sources/README.md:52` |
| 3 | “Choose the agents to configure, review the proposed paths and changes, and approve the plan.” | 先选要配置的 agent，复核计划的路径与改动，再批准该计划。 | `sources/docs_installation.md:20` |
| 4 | “Setup adds REA's MCP server and matching workflow instructions, with backups of existing configuration. Restart your agent afterward.” | setup 会加入 REA 的 MCP 服务和配套工作流指引，并备份原有配置；完成后重启 agent。 | `sources/README.md:68` |
| 5 | “Persistent registrations should use one exact package version.” | 写进 agent 配置的注册应锁定一个确切包版本。 | `sources/docs_installation.md:811` |
| 6 | “The actual registry package accepted dry-run setup plans for the 17 client IDs in that release, including Qwen Code, Pi and Hermes.” | 该版本的注册表包实际接受了针对 17 个 client ID 的 dry-run 安装计划，含 Qwen Code、Pi 与 Hermes。 | `sources/docs_installation.md:209` |
| 7 | “Static JavaScript and .NET inspection read the supplied files without running the application.” | 静态 JavaScript 与 .NET 检查只读所给文件，不运行应用。 | `sources/README.md:178` |
| 8 | “REA imports one target into an ephemeral Ghidra database. Linux/macOS support read-only analysis and atomic function-name/entry-comment edits; Windows P0 is read-only.” | REA 把单个目标导入临时 Ghidra 库；Linux/macOS 支持只读分析与函数名/入口注释的原子修改，Windows P0 仅只读。 | `sources/docs_ghidra-provider.md:3` |
| 9 | “REA adapts an existing IDA MCP server into its native analysis tools.” | REA 把既有的 IDA MCP server 适配成自己的原生分析工具。 | `sources/docs_ida-provider.md:3` |
| 10 | “Capturing a new scenario currently requires Linux or macOS and a working native PTY backend.” | 当前捕获新场景需要 Linux 或 macOS 以及可用的原生 PTY 后端。 | `sources/docs_process-capture.md:17` |
| 11 | “This is not a sandbox and does not protect against malicious processes already running as the same operating-system user.” | 这不是沙箱，不能防御已经以同一操作系统用户身份运行的恶意进程。 | `sources/SECURITY.md:33` |
| 12 | “These controls limit accidental persistence and resource use; they do not make Ghidra a sandbox.” | 这些控制限制意外持久化与资源占用；它们并不使 Ghidra 成为沙箱。 | `sources/SECURITY.md:42` |
| 13 | “This is a passive reverse-engineering capability, not a general browser automation or remote-control surface.” | 这是被动式逆向能力，不是通用浏览器自动化或远程控制面。 | `sources/docs_browser-observation.md:9` |
| 14 | “This feature is not a browser sandbox or network containment mechanism.” | 该功能不是浏览器沙箱，也不做网络隔离。 | `sources/docs_browser-observation.md:229` |
| 15 | “Static graph workflows do not execute recovered code.” | 静态图工作流不会执行恢复出来的代码。 | `sources/docs_javascript-application-workflows.md:303` |

> 出处列**宁空不猜**：本表全部逐字回源锁定到 `sources/` 行号；无把握的引文一律不列。产品文件名（如 `export.js`）不是来源件，故不进本表。

---

## 8. P2 自检记录

- 逐字回源：**15 条**英文整句引文逐字核对（归一化后）→ 见下轮自检命令结果；
- 数值重计：目标表 **22**（英）/ **19**（中）、支持客户端 **21**、npm **6.4.0**（2026-10-11）、Node **22.x(≥22.19)/24.x(≥24.11)/26+**；
- 未采信：星标数、社区教程（`snippet-only`）；
- 中间产物声明已在文首给出，下游引用前须回源。
