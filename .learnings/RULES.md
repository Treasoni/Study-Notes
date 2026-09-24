# Rules

Compressed, deduplicated learnings from past Study System sessions.
Read before starting any new Study System task.

## Do

- 长篇笔记（>30KB 或多于 3 章）组装后主动建议拆分：独立章节文件 + 前后导航双链 + MOC 索引页
- Phase 4 beautify 前主动询问用户是否需要 Canvas/Base 配置
- GitHub 项目类主题，先通过 API 获取基本信息再进 Phase 0 提问
- 混合笔记 concept + cheat_sheet 适合"入门+速查"场景
- 工具对比/迁移类主题优先用 practice + compare 混合类型，每个领域同时提供步骤指南和对比表
- 每个学习笔记为核心概念添加 `[!tip] 大白话` 通俗解释 + 打比方类比（临时工牌 / 门禁卡 / 保险箱 / 双保险 / 岗位说明书 / 料理包 / 千层饼 等）；写作新笔记与 update 旧笔记时都补，用户偏好（3x）
- 教程类笔记「一章一节一文件」：顶级小节对应一个文件/产物；同一文件的字段（package.json 的 name/deps/files 等）收进该文件小节的 `####` 子节，不升格为顶级小节
- 教程代码块用文件头注释标注所属路径，并先展示完整文件（先睹为快）再逐段拆讲
- 用户报命令/路径错误时，先读源码核实路径解析基准与文件真实位置，一次改对再写入笔记；改完全文 grep 确认无残留旧表述
- 用户决策点用紧凑文本菜单 + 推荐默认值，不要用多问题 AskUserQuestion 对话框（用户会拒绝）
- 合并多篇独立章节前/后按章命名空间化脚注 ID（`[^cN-…]`），并 grep 校验无重复
- GitHub 项目取文档优先 `raw.githubusercontent.com/{owner}/{repo}/{branch}/...`；github.io 镜像可能 404
- 本机 `python3` **可用**（原生 CPython 3.14，非微软商店存根；2026-09-11 复核）——中文文本处理优先 python；若用 perl 兜底，必须 `use utf8;` + `use open ":std", ":encoding(UTF-8)"`，否则字符类正则静默 no-op
- 写 OpenWrt/iStoreOS 第三方插件安装步骤前，先用 GitHub API（`curl api.github.com/.../contents`、`/releases/tags/{tag}`）核实软件源 feed 内容与 release 真实文件名，再写命令；示例 URL 必须来自实际存在的文件
- 用户明确说「删掉」误导内容时，直接删除整节并重排编号，不要加 warning 补丁保留
- 解释抽象概念按「它是什么/解决什么问题 → 具体产物长什么样 → 带具体值的可代入例子（目录树/路径/命令输出）→ 对比表 → 大白话类比」落地；正文去掉类比后仍要能让「没懂」的读者靠表格/例子读懂，不只抛抽象结论（默认写作标准，用户当日连续两次明确要求「都要这样」）
- 给子 agent 派活时**不要转述来源论断**：只传来源 ID + 检索位置，要求「先回原文核对再落笔」；确需带结论必须成对标注（原文加引号 / 概述标「待核对」）。章节验收对每处「官方口径是 / 官方说明 / 原文」逐条回源比对，不只看有没有挂来源 ID
- 中文文本的组装、拆分、统计一律走 python（`re.findall(r'[一-鿿]', t)` 计字数）；批量文本改写脚本必须打印「本次改动 N 处」，N=0 时人工复核，不许静默通过
- `02_deep_research.md` 是**中间产物**、不是可信终点：写作者落具体数值/默认值/版本号前回 `sources/` 按行号核对（抓取错位常见——`tcp_ecn` 曾被记成 `tcp_ecn_option_beacon` 的默认值 3）；核对不了就只写语义、不写数值
- RULES 里出现「X 不存在，所以走 Y」这类**绕行规则**时，先查 X 是否本该存在（状态模板、上下游文档、调用点）；能修实现就修，修完把那条绕行规则改写或删除。把缺陷写成规则会让缺口变成「既定契约」，再没人回头
- **官方引文摆放**：一段要摆 ≥3 处引文、或含任一整句英文、或长度 >300 字符时，改用「官方原文 / 说人话」两列对照表 + 结论单独成句 + 关键误读用 `[!warning]`；**只有 1 处短引文时行内保留**，不为形式套表。引文逐字与脚注编号/来源归属一律不动，只改摆放；验收时遮住英文列读一遍「说人话」列，不能只核对引文是否正确（用户反馈「让人很难去理解和看懂啊」）

## Don't

- 不要把表格嵌套在列表项内（带缩进），Obsidian 无法渲染列表内的表格

## Domain

- GitHub Packages / GHCR 认证只支持 Classic PAT（`write:packages` 等 scope）；Fine-grained PAT 无 packages 权限项，遇到"expected scopes"报错先认 `github_pat_` 前缀换 classic

## Watch For

- YAML frontmatter 的 sources 字段中所有含特殊字符（`[]`, `:`）的值必须正确引用，否则 Obsidian 解析失败
- 并行派发 chapter-writer 时，章节过渡语必须自包含（按大纲），不要依赖读取上一章文件
- `todo-state.sh` 动作为 `start|complete|skip|block|mode|confirm`：常规走 `start PN` → `complete PN`；`mode PN <值>` 只改 frontmatter `mode` 键、`confirm PN "说明"` 只追加一行到 `## 用户确认记录`，**两者都不动阶段状态行、不要求前置阶段闭幕**；**最后一个阶段**还需 frontmatter 写 `quality_gate: passed`（走豁免则同时补 `quality_gate_owner` + `quality_gate_due`）
- 并行写作 ≥2 章前先冻结**跨章共享口径**（字段名、术语、命名风格）并写进每个 dispatch：各章「忠于自己手边的来源」合起来可能互相矛盾（官方示例写 `network: "tcp"`、权威文档只文档化 `method` → 同一篇笔记里两章打架）；交付后对「可照抄的配置块」做一次跨章 grep
- note-assembler 等 writer 子 agent 无 Bash/Edit 且 Write 有输出上限；>100KB 长文档由父进程 python 合并；反向扫描定位插入点时必须**同时跳过空行和 `---` 分隔线**，否则扫描停错位置且静默不生效
- 组装脚本调整标题层级时必须**级联到子标题**：只把章标题降一级、不管章内 `## N.M` 与 `## 小结`，会让章标题与节标题同级、大纲整体塌陷；降级后要重新解析标题树逐层校验
- 「合并/保留外部条目」的生成器，校验必须跑在**合并结果**上，不是只跑本次渲染的子集，否则保留路径天然免检（`.agent-sync/bootstrap.py --check` 曾对指向已删脚本的 hook 注册报 `[OK]`）
- 并行子 agent 不得直接修改共享 workflow state file；状态推进由 orchestrator 集中经 todo-state.sh 处理
- workflow 已 `done` 的笔记再被 note-updater 单篇更新时，workspace 侧 `chapters/`、`output/` 副本**不会**跟着变，两边同名文件必然长期漂移：至少登记「vault 已于 <日期> 更新，workspace 副本停留在 <日期>」，并让用户二选一（重跑 note-assembler 同步 / 明确弃用副本），不要默认「以 vault 为准」就收工
- P6 发布前校验最终产物并**建议**拆分：>30KB 或多于 3 章时给出「分册子目录 + README + 每章独立文件 + 前后导航 + MOC 指向 README」方案，但**用户明确选单文件就按单文件发布**（2026-09-11 一篇 43k 汉字 / 228KB 笔记经用户确认单文件落地，非违规）
- iStoreOS 官方 iStore 商店不含代理插件；Passwall SourceForge 源只含 passwall_luci/passwall_packages/passwall2（不含 OpenClash）；OpenClash `.run` 包 `+core` 表示内置内核
- WebFetch 拦截的域名（raw.githubusercontent.com、github.com）改用 `curl api.github.com` 替代
- 往 Obsidian 笔记加双链前，先核实目标笔记**真实存在**（逐条 `os.path.exists` 断言），不要给 vault 里不存在的概念词埋死链；章级锚点**避开含反引号/箭头/竖线的标题**（如 `2.7.3 主路径：导出 \`.reg\` → …`），改链到不含特殊字符的上级标题
- 文本比对工具一律**行尾不敏感**比较：本机 `core.autocrlf=true`，工作区是 CRLF，而 `Path.read_text` 会把 CRLF 折成 LF——按原始字节比较的工具在这里会**永久误报**（`[DRIFT] updated: CLAUDE.md` 拖了整轮），把本该可信的门变成人人忽略的噪音。`--check` 退出 1 就先怀疑换行符，别先改内容
- 把某个区域纳入同步范围前，**先双向 diff 两侧**再决定 canonical 方向：`.claude/agents/` 曾严格领先于 `.codex/agents/`（多出 5 处经验），若直接以 `.codex` 为 canonical 跑 `--apply` 会静默删掉它们。正确顺序是「先把领先侧回收进 canonical → 再加 `paths.<area>` 与 `canonical_scopes` → 再 apply」，并用「apply 后镜像逐字节不变」证明回收完整
- 在 canonical 文档里**不要写死 canonical/目标路径字面量**：同步的路径替换会把镜像里那句 `.codex/agents/` 改写成 `.claude/agents/`，于是「canonical 是 X」在镜像里变成「canonical 是 Y」——方向说反。描述方向时用 profile 键名（`paths.agents`、`canonical_scopes`），或写成「哪一侧由 profile 决定」
- 校验脚本**绝不能依赖 `rg`**：在本运行时里 `rg` 只是交互式 shell 上的一个 Claude Code 函数（`type -a rg` 会显示 `rg is a function`），任何**子进程**（`bash script.sh`、pre-commit、CI、别的 runtime）里都是 `command not found`。此时 `if rg ...; then fail; fi` 会退化成「无命中 = 通过」，守卫**静默失效且永远绿灯**。用 `command -v` 探测 + `grep -rnE --exclude-dir=...` 兜底，或让工具缺失直接失败退出；判断命中用 `[ -s "$tmp" ]` 而不是命令退出码
- 守卫和文档引用的路径**必须指向 canonical/现行目录**，指向已退役目录（如 `.codex/skills` 之于 `.agents/skills`）等于零覆盖：被扫的是过期副本，canonical 改动永远不会被抓到。改同步范围或搬迁目录后，grep 一遍 `scripts/`、`rules/`、`agents/` 里的旧路径字面量
- 退役/搬迁目录前先**枚举消费者**，不能只扫源码：**已打包的第三方产物**（`.obsidian/plugins/*/main.js` 这类 bundle）各自持有硬编码路径常量，既不随项目同步、也不出现在 diff 里——Claudian 插件就同时硬编码了 `.codex/skills` 与 `.agents/skills` 两个扫描根。若某消费者还有「默认写回该路径」的行为（插件新建 skill 的弹窗默认根是 `.codex/skills`，且没有可持久化的默认根设置），删除时必须同时记下规避方式（改哪个 UI 选项），否则退役目录会被下游悄悄重建
- 「每台机器一份」的生成物，**默认值必须可移植**：生成器不要把自己的运行时绝对路径（`sys.executable`、`/Library/...`）写进**受跟踪**产物——那会把仓库钉死在最后跑生成器的那台机器上（本仓库因此把一个 macOS 解释器路径提交进 Windows 检出，SessionStart hook 长期是死的）；机器身份只写进明确 untracked 的文件（如 `.agent-sync/local/`）。校验器**不能跳过**生成出来的受跟踪产物（`GENERATED_HOOK_CONFIGS`）：宿主绝对路径恰好出现在那里，跳过它们等于放过唯一会中招的文件；正确做法是**解析**配置取 hook `command` 的可执行 token 再判绝对性（`/Library/...` 通不过 `ABSOLUTE_PATH` 那种只认 `/Users/`·`/home/`·盘符的通用正则），且**不要**顺手放宽通用正则——`/opt/...conda` 之类「候选探针清单」是可移植代码
- 守卫写完要**问三件事：谁调用它、它在本仓库能不能变绿、绿是不是空绿**。三条任一不成立就等于没有守卫：`validate_portability.py` 曾同时三缺（无调用点；`core.autocrlf=true` 下按工作区字节判换行 → 每次调用 567 条全红 → 必然被无视；查表失败也会「绿」）。落地方式：接进 `workflow-health-check.sh`；换行符改判 `git ls-files --eol` 的 `i/` 字段（提交的是索引内容，工作区 CRLF 是策略产物不是缺陷）；用程序化断言证明查表真读到数据（条数 > 0），再配双向注入证明该层承重
- 双向注入测试**要确认注入物真的进了被检对象**：Git Bash 会把 `/Library/...` 这种 POSIX 绝对路径实参自动改写成 `C:/Program Files/Git/Library/...`，于是「通用正则」也会命中，看起来通过了、实际测的不是新写的那层。加 `MSYS2_ARG_CONV_EXCL='*'` 让路径原样落盘，再看 findings 是否仍由目标层产生
- 会打印 `.learnings`／笔记内容的脚本**必须自己把输出流设成 UTF-8**：Windows 上 `print()` 继承 ANSI 代码页（GBK），而学习记录全是中文 → `UnicodeEncodeError` → 脚本非零退出，提醒**静默消失**。入口处 `sys.stdout.reconfigure(encoding="utf-8", errors="replace")`（stderr 同理），不要指望宿主设 `PYTHONUTF8`。核实「某脚本在这台机器上能不能跑」要看**退出码**，不能只看它打出了标题行——`read_learnings.py` 就是先正常打印头部、再在第一个汉字处崩掉
