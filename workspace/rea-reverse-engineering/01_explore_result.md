# 01 探测结果 — REA: Reverse Engineer Anything

> **本文件是中间产物**：引文与数值请回 `sources/` 按行号核对，不要直接当权威引用。
> P1 只记录**来源线索**；正文未抓取的条目标 `snippet-only`，P2 才作为证据抓取。
> 主题：REA: Reverse Engineer Anything（morluto/rea）｜运行标识：rea-reverse-engineering
> 阶段：P1 探测式收集｜日期：2026-10-13

---

## 0. 主项目出处核验（upkeep）

- `morluto/rea` 是**官方主项目**（非社区封装脚本）。`pushed_at` = 2026-10-13（当日活跃）、`archived` = false、license MIT、`default_branch` = `main`。
- npm 包 `rea-agents` latest = **6.4.0**（2026-10-11），bin 提供 `rea` 与 `rea-agents` 两个命令。
- **结论**：作为本笔记主线项目**合格**。

---

## 1. 来源记录（三透镜，去重后）

### 透镜 A — 官方一手资料（是什么 / 装 / 跑）
| # | 标题 | URL | tier | 形态 | 日期 | score |
| --- | --- | --- | --- | --- | --- | --- |
| A1 | README（英文） | `https://raw.githubusercontent.com/morluto/rea/main/README.md` | official | fetched | – | 5 |
| A2 | README_zh（简体中文） | `.../README_zh.md` | official | fetched | – | 4 |
| A3 | docs/installation.md | `.../docs/installation.md` | official | fetched | – | 5 |
| A4 | docs/cli.md | `.../docs/cli.md` | official | fetched | – | 5 |
| A5 | npm 包 rea-agents | `https://www.npmjs.com/package/rea-agents` | official | fetched | 2026-10-11 | 4 |

> `...` = `https://raw.githubusercontent.com/morluto/rea/main`。A3 与下表 C1 是**同一文件**，按 canonical URL 合并。

### 透镜 B — 实战指南与案例（零原生引擎路径）
| # | 标题 | URL | tier | 形态 | 日期 | score |
| --- | --- | --- | --- | --- | --- | --- |
| B1 | 指南：JavaScript & Electron（Electron CSV 导出案例） | `https://rea.tools/guides/javascript/` | official | fetched | – | 5 |
| B2 | docs/javascript-application-workflows.md | `.../docs/javascript-application-workflows.md` | official | fetched | – | 4 |
| B3 | 案例：Notion（Electron 剪贴板桥） | `https://rea.tools/showcase/notion/` | official | fetched | – | 4 |
| B4 | 指南：Browser observation（点一下发生了什么） | `https://rea.tools/guides/browser/` | official | fetched | – | 4 |
| B5 | 指南索引 | `https://rea.tools/guides/` | official | fetched | – | 3 |
| B6 | 案例：DX-Ball（原生 x86，门槛偏高） | `https://rea.tools/showcase/dx-ball/` | official | fetched | – | 3 |

### 透镜 C — 生态、provider 与边界
| # | 标题 | URL | tier | 形态 | 日期 | score |
| --- | --- | --- | --- | --- | --- | --- |
| C1 | installation.md → Supported agents（支持客户端表）+ Hopper / MCP registry 小节 | `.../docs/installation.md` | official | fetched | – | 5 |
| C2 | docs/ghidra-provider.md | `.../docs/ghidra-provider.md` | official | fetched | – | 5 |
| C3 | docs/ida-provider.md | `.../docs/ida-provider.md` | official | fetched | – | 4 |
| C4 | DISCLAIMER.md（合法用途白名单与禁项） | `.../DISCLAIMER.md` | official | fetched | – | 5 |
| C5 | skills.sh 技能页 | `https://www.skills.sh/morluto/rea/reverse-engineer-anything` | community | fetched | – | 3 |
| C6 | 社区教程/评测（sitepoint、implicator.ai、apidog blog、dev.to 等） | 多条 | community / reputable-report | **snippet-only** | – | 2–3 |
| C7 | SECURITY.md / CONTRIBUTING.md / docs/roadmap.md（辅助口径） | `.../{SECURITY,CONTRIBUTING}.md`、`.../docs/roadmap.md` | official | fetched | – | 3 |

---

## 2. 关键事实（来自 fetched 正文，P2 仍需回源核对）

- **首跑命令**：`npx rea-agents setup` → 注册 REA 的 MCP server + 配套 workflow 指令，安装时**备份原配置**，完成后需**重启 agent**。
- **Node.js 要求**：22.x(≥22.19) / 24.x(≥24.11) 及 26+；**23、25 与预发布版不支持**。npm 包 `engines.node` = `^22.19.0 || ^24.11.0 || >=26.0.0`（两者一致）。
- **CLI 入口**：`rea --help` 真实存在；已文档化命令含 `setup`、`update`、`analyze`、`analyze-javascript-application`、`search`、`function`、`decompile`、`xrefs`、`trace`、`providers`、`doctor`。
- **更新**：全局装用 `rea update`；`npx` 用户改用 `npx rea-agents@latest setup`（Bun 全局更新需 Bun ≥1.2.17）。
- **零原生引擎**：静态 JavaScript 与 .NET 分析无需 Hopper/Ghidra/IDA。
- **平台限制**（待 P2 逐条回源）：Hopper 无 Windows 版；Ghidra Windows 支持为实验性/只读（Windows P0）；firmware / EVM / WASM 与原生 mitmproxy 解码路径限 Linux x64；`dsh`(DeepSeek Harness) 仅 main 分支、不在 npm 6.4.0。
- **边界**：SECURITY.md 称 per-session capability token，但**「不是沙箱」**；CONTRIBUTING 排除打包/DRM/反作弊/绕过类用途；DISCLAIMER 限定合法研究/教育/互操作性/软件保存，以及分析你拥有或获授权的软件。

---

## 3. 冲突与未采信

- **星标数冲突**：社区来源互相矛盾（约 22k–115k），与官方 API 快照（`stargazers_count` = 180,692 @ 2026-10-13）也不一致 → **本笔记不采用任何星标数**；如确需，只引官方 API 快照并标日期。

---

## 4. 覆盖缺口（P2 按所选方向补）

- 未单独抓到正文：`docs/index.md`、`docs/mcp-contracts.md`、`docs/mcp-prompts.md`、`docs/process-capture.md`、`docs/browser-observation.md`、`docs/website-module-trace.md`、`docs/web-network-captures.md`、`docs/roadmap.md`（roadmap 仅作辅助）。
- README「What you can analyze」**目标类型表**（原生二进制 / Go / WASM / EVM / SQLite / JS-Electron / 网站 / 抓包 / .NET / APK / 固件 / 进程行为…）需**逐行**回源核对再写入。
- 社区教程（C6）仅 `snippet-only`，未抓正文，**不得作为证据**。
- 缺一条**端到端实战命令链**的原始输出/结果结构（P2 优先补）。

---

## 5. 方向菜单（请选一个，P2 按此展开）

| 选项 | 方向 | P2 重点 | 建议 |
| --- | --- | --- | --- |
| **A** | **讲解为主** | REA 是什么 + 能力全景表 + 接入方式（概念扎实，实战仅演示） | ❌ 与已定意图「混合」不符 |
| **B** | **实战为主** | 直接跑通零原生引擎路径：`setup` 接 MCP → 跟 JS/Electron 或浏览器指南做一遍 → CLI 直用 | ✅ 可选 |
| **C** | **混合（推荐）** | 概念与实战各半：是什么/解决什么问题 → 安装接入 → 实战（setup + CLI + 多目标类型）→ 进阶概览（provider/平台限制）→ 边界与安全 | ✅ **推荐，与 00_intent 一致** |

> 你此前已确认「入门→上手、概念+实战混合」，对应**选项 C**。若认可，回「C / 就按 C」即可，我会逐条核对上面的缺口后进入 P2 深度收集。

---

## 6. P2 预计范围

- **抓取正文**：A1–A5、B1–B2 关键小节；按方向补 `mcp-contracts.md`、`index.md`、`process-capture.md` 等。
- **逐行核对**：README 目标类型表、Supported agents 表、平台限制清单、Node 版本数值。
- **产出**：至少 1 条零原生引擎端到端命令链（`setup` → 分析 → 结果字段）+ provider 选择判据 + 引用留档。
- **规模**：约 8–12 个来源；≤3 个 P2 子代理（不按来源逐一派）。
