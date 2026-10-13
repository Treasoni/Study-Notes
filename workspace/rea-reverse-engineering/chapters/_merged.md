<!-- SOURCE: 01_overview.md | 7596 bytes -->
# 第 1 章 这是什么、解决什么问题

看到一个软件里很好用的功能，你想在自己项目里做一个类似的，可它偏偏没有源码——这种时候，你连「从哪下手」都不知道。本章要介绍的 **REA（Reverse Engineer Anything）**，就是让 AI agent 替你回答这个问题的工具。一句话看懂：REA 是一个 **MCP server + CLI**（npm 包名 `rea-agents`），把「逆向下手」的整条能力接给 AI agent，分析跑在你自己这台机器上，每条结论都带着证据和局限。

> [!tip] 大白话
> 把 REA 想成给 AI 装的一个「拆解工具插槽」：AI 本来只会聊天，插上它就能真的拿起螺丝刀，把没有源码的软件一层层拆开看。所以你不必先成为逆向高手，也能让它带你摸清一个软件是怎么实现的。

## 一、它到底解决什么问题

先说清楚「逆向工程」是什么。**逆向工程**（reverse engineering）一句话：没有源码，也把软件「拆开看清楚」它是怎么做的。

平时我们读代码，前提是拿得到源码，这叫「正向」。可现实里很多想学的东西——某个 App 的导出功能、某个网站点一下之后偷偷发出去的请求——你手上只有装好的成品，没有那行源代码。逆向工程就是对付这种「黑箱」的手艺。

> [!tip] 大白话
> 把成品软件想成一台封装好的机器：正向开发是照着图纸造机器，逆向就是捧着这台看不见内部的机器，靠听声音、摸震动、拆外壳，反推它里面装了什么齿轮。所以逆向的价值不是「抄」，而是「看懂我没有源码的东西」。

REA 的第一个价值，官方讲得很直白：你在一个应用里看到一个想要的功能，可以让 agent 用 REA 去调查它——就算没有源码，也能检查它、解释它怎么工作、把证据摆给你看，再为你的项目做一个类似的实现。

## 二、三层覆盖：二进制、应用程序、运行时行为

REA 不是什么都能拆，但它覆盖的范围横跨三层。官方那句定位语把它讲得很准（原文与中译见章末引文表）：

| 层级 | 大白话是什么 | 例子 |
| --- | --- | --- |
| 二进制（binaries） | 编译完、只剩机器码的成品程序 | 原生可执行文件 |
| 应用程序（applications） | 带脚本或中间代码的软件 | JavaScript / Electron 应用、.NET 程序集 |
| 运行时行为（runtime behavior） | 程序真的跑起来时做了什么 | 网站点了之后发出的网络请求 |

顺着这三层，还有一对常出现的术语要顺带分清：**静态分析**是只读文件、不运行程序；**运行时捕获**则是真的把程序或浏览器跑起来，记录它当时的行为。前者安静，后者「动静」都记。

> [!tip] 大白话
> 把这三层想成检查一辆车的三个位置：二进制是「拆开看发动机用的是什么材料」，应用程序是「看电路图和零件规格」，运行时行为是「真的开一圈，看哪个灯会亮」。所以同一台车，可以从材料、图纸、实驾三个角度分别问它问题。

这三层里，本笔记后面重点带跑的两条实战——静态 JS/Electron 和网站观测——都属于「零原生引擎」就能跑的目标：不用装额外的大型分析软件，有 Node.js 环境就够。至于「哪些目标能直接上手」的完整全景，留到第 2 章展开。

## 三、它怎么工作：一条带回证据的回路

REA 的核心工作方式，可以概括成一条回路：

1. **agent 经 MCP 调 REA**——这里出现第二个术语。
2. **REA 检查目标，并追踪相关代码**——把和问题有关的代码、引用、未知项捞出来。
3. **REA 返回「发现 + 证据」**。
4. **agent 据此提问、解释行为，或写出并测试一份实现**。

**MCP** 是什么？Model Context Protocol，一句话：让 AI agent 调用外部工具的一套标准插口。REA 就是通过这个插口把自己「插」进你的 agent 里；CLI 则复用同一套工作流，让习惯命令行的人也能直接跑。

> [!tip] 大白话
> 把 MCP 想成通用的电源插排：不同厂家的 AI agent 是不同形状的插座孔，MCP 就是那把大家都能插的转接头。所以 REA 只要做一次 MCP 插头，就能同时接上很多种 agent，而不必为每个 agent 单独适配一遍。

> [!note] 名词扫盲表
>
> | 术语 | 一句话白话 |
> | --- | --- |
> | 逆向工程 | 没有源码，也把软件「拆开看清楚」它是怎么做的 |
> | MCP | Model Context Protocol，让 AI agent 调用外部工具的一套标准插口 |
> | 证据 / 局限（Evidence / limitation） | REA 不只给结论，还给出「凭什么这么说」和「哪里说不准」 |
> | 静态分析 | 只读文件、不运行程序 |
> | 运行时捕获 | 真的把程序或浏览器跑起来，记录它的行为 |

## 四、最关键的一点：结论自带证据和局限

大多数「黑箱工具」只丢给你一个结论，对不对全凭你信。REA 特意反着来——它给每个结论都配上两样东西：**证据**（它凭什么这么说）和**局限**（哪儿还说不太准）。

更关键的是，这些分析都发生在你的本机：目标文件不会被打包上传到某台服务器去分析。官方原话是「分析在本机运行，结果附带支撑每条结论的证据与局限」（原文与中译见章末引文表）。

> [!tip] 大白话
> 把「证据 + 局限」想成一份体检报告：报告不只写「你血脂偏高」，还附上化验单照片（证据）和「本次未做空腹、结果仅供参考」的备注（局限）。所以你能自己判断这份结论该信几分，而不是被一句斩钉截铁的结论牵着走。

这条「结论自带证据」的设计，正是后面读实战结果时的抓手：看 REA 输出时，别只看它「说了什么」，要连着它「凭什么」一起看。

## 五、这一章讲了什么

- REA = **MCP server + CLI**（npm 包 `rea-agents`），把逆向能力接给 AI agent。
- 它解决的问题：**没有源码，也想看懂一个软件是怎么做的**。
- 覆盖**三层**：二进制、应用程序、运行时行为。
- 工作方式是**一条回路**：agent 经 MCP 调 REA → 检查并追踪代码 → 返回发现 + 证据 → agent 解释或实现。
- 落点：**分析在本机跑，结论自带证据与局限**。
- 顺带给五个术语配了白话解释，后面章节会反复用到。

## 六、下一章预告

知道了 REA 能帮你做什么，下一个问题自然是：**它到底能拆哪些东西？** 第 2 章会把官方列出的 22 类可分析目标整理成一张可扫的全景表，并点出哪些目标「零原生引擎」就能直接上手——这正是本笔记后面两条实战的选型依据。

---

## 引文对照（原文 / 中译 / 出处）

> 「出处」列标注引文逐字所在的来源文件与行号；查不到来源的写 `—`（宁空不猜）。产品文件名（如 `rea-agents`）不是来源件，故不进本表。

| 序号 | 原文 | 中译 | 出处 |
| --- | --- | --- | --- |
| 1 | “One MCP for reverse engineering across binaries, applications, and runtime behavior.” | 一个 MCP，覆盖二进制、应用程序与运行时行为三层的逆向分析。 | `sources/README.md:7` |
| 2 | “Analysis runs locally, and results include the evidence and limitations behind each conclusion.” | 分析在本机运行，结果附带支撑每条结论的证据与局限。 | `sources/README.md:52` |
<!-- END: 01_overview.md -->

<!-- SOURCE: 02_targets.md | 9515 bytes -->
# 第 2 章 能分析什么：22 类目标全景

上一章说清了 REA 是「给 AI 装的拆解工具」。这一章回答下一个最实际的问题：它到底能拆哪些东西？官方 README 里列了 22 类可分析目标，本章把它们整理成一张可扫的全景表，并拆成三组帮你记住——尤其是哪几类「什么都不用另外装」就能直接上手。

> [!tip] 大白话
> 把 REA 想成一套「万能拆解工具箱」：箱子里有很多抽屉，每个抽屉专门对付一类目标——一个抽屉拆手机 App，一个抽屉拆网页，一个抽屉拆数据库。所以你要做的不是背下 22 个名字，而是先判断「我手上这东西属于哪一类」，再拉开对应抽屉。

为什么先摆一张表？因为逆向最容易卡住的地方，恰恰是「我手上这东西到底归哪一类」。先分清目标类别，你才知道要提前准备什么、难度大概多高；也才不会拿一个明明要额外引擎的目标，去硬套第 ① 组的流程空耗半天。这张表就是你后面所有动手前的「选型地图」。

## 先记一个数：22

官方英文 README 的目标表是 **22 行**，每一行就是一类「REA 认得的拆解对象」。这里先埋一个坑的提示：简体中文版 README 的同一张表只有 **19 行**，少了 Go 二进制、WASM 制品、SQLite 数据库这三行（中文版未同步）。本笔记一律以英文的 **22 行**为准，绝不因为中文版缺行就把目标删掉。

## 三组记忆：按「要不要额外装东西」分

22 类初看很多，但按一个直觉标准就能分组：**拆它要不要额外装东西？**

- **第 ① 组 纯静态、零原生引擎**：有 Node.js 环境就能跑，不用装任何大型分析软件。
- **第 ② 组 需要浏览器**：要一个 Chrome 系浏览器配合。
- **第 ③ 组 需要额外工具或引擎**：得另外准备工具（JADX、tshark 等）或分析引擎（Hopper / Ghidra / IDA 等）。

> [!tip] 大白话
> 这三组的差别，就像开抽屉的门槛：第 ① 组是「伸手就够到」的抽屉；第 ② 组要「先搬来一张椅子」（装个浏览器）；第 ③ 组得「先去仓库领专用工具」。所以给零基础读者的建议很简单——先从第 ① 组练手，第 ③ 组等真有需要再碰。

本笔记后面的两条实战，正好各占第 ①、② 组的一类；第 ③ 组只在这里点个名、不展开（留给第 6 章讲 provider 时再说）。三组的整体差别，收成一张对照表：

| 组别 | 要额外准备什么 | 本笔记怎么处理 |
| --- | --- | --- |
| ① 纯静态零引擎 | 几乎不用（有 Node.js / npm 即可） | 两条实战首选，重点展开 |
| ② 需要浏览器 | 一个 Chrome 系浏览器 | 实战二展开 |
| ③ 需要额外工具 / 引擎 | 具体工具（JADX、tshark…）或分析引擎（Hopper / Ghidra / IDA…） | 只列名，留到第 6 章 |

### 第 ① 组：纯静态、零原生引擎

这五类目标，REA 只读文件、不运行程序，也不需要额外引擎。

| # | 目标 | REA 返回 | 要求 / 指南 |
| --- | --- | --- | --- |
| 8 | JavaScript / Electron | 模块、导入、source map、路由、IPC、原生扩展关系 | 仅需 Node.js 和 npm |
| 11 | .NET 程序集 | 元数据、CIL 指令、声明的原生依赖、构建对比 | 无（纯静态） |
| 3 | Go 二进制 | 内嵌编译版本、模块、替换、构建设置 | 内置静态 ELF/PE/thin Mach-O 检查，无需装 Go |
| 16 | Flutter 应用 | Dart 快照哈希、按 ABI 的库摘要、引擎构建溯源 | 无（静态 APK 解析） |
| 6 | SQLite 数据库 | 表、列、索引、视图、触发器、抽样行 | 本地库 / WAL 快照；Node 24.x ≥24.15 或 26+ |

（Go / SQLite / .NET 这三类的对应命令，统一放在第 8 章速查表，本章不写命令。）

### 第 ② 组：需要浏览器

| # | 目标 | REA 返回 | 要求 / 指南 |
| --- | --- | --- | --- |
| 9 | 网站 | 页面结构、脚本、网络观测、按需截图 | Chrome 系浏览器 |

### 第 ③ 组：需要额外工具 / 引擎（只列名，不展开）

下面这些目标的「伪代码」「汇编」等行话，下一节统一扫盲。

| # | 目标 | REA 返回 | 要求 / 指南 |
| --- | --- | --- | --- |
| 1 | 原生二进制 | 伪代码、汇编、字符串、符号、调用与引用 | Hopper / Ghidra / IDA |
| 2 | 离线 ELF 布局 | 节、段、原始符号 / 重定位、静态防护候选项 | Linux x64 + 调用方提供 pwntools |
| 4 | WASM 制品 | 校验、节、精确 import/export WAT、解码 WAT | 调用方提供 WABT 1.0.42 |
| 5 | EVM 字节码 | 分派选择器、字节偏移、推断参数、可变性 | Linux x64 本地原始 / 十六进制载体 |
| 7 | 已记录的 Linux 崩溃 | 原始 note、各线程寄存器 / 信号、映射候选项 | Linux x64 + pwntools；可选 GDB / pwndbg |
| 10 | 已保存的网络捕获 | 请求、响应、可暴露的载荷、来源位置 | HAR / Fiddler SAZ；原生 mitmproxy 需 Linux |
| 12 | Android APK | 清单声明、类、反编译方法、引用 | 无界面 JADX + 完整 JDK（Linux/macOS/Windows x64） |
| 13 | Android 设备 | 设备、包、进程、日志、转储、截图、APK / 文件传输 | 调用方提供 adb |
| 14 | JEB 项目 | 引擎支持的项目单元、制品摘要、类型 / 方法伪代码 | 调用方启动的 JEB MCP 客户端（REA_JEB_MCP_URL） |
| 15 | Android 资源 | 解码清单、字符串表、语言区域、版本信息 | 调用方提供 Apktool |
| 17 | 固件 | 分区、提取结果、转交原生分析 | Linux 上 Binwalk / Unblob |
| 18 | 录制的数据包 | 指定字段、重复值、过滤条件、解码规则 | Linux：TShark 4.x + prlimit |
| 19 | 数据包摘要 | 端点、DNS、TLS SNI、协议分布、HTTP 请求 | 调用方提供 tshark / capinfos |
| 20 | 录制的逻辑信号 | 解码注释、样本范围、诊断信息 | Linux：sigrok-cli 0.7.2 + prlimit |
| 21 | 软件包与资源 | 文件清单、摘要、plist、Apple bundle 结构、提取资源 | 制品 / Apple 应用指南 |
| 22 | 进程行为 | 终端输出、交互、退出与文件系统观测、运行对比 | Linux/macOS + 原生 PTY |

> [!warning] 别被「要求」列吓到
> 第 ③ 组的「要求」列里很多写着「调用方提供 xxx」——意思是 REA 不替你装那个工具，你得自己先有。所以看到某类目标「要先装 JADX / tshark」，就知道它属于第 ③ 组，不在「零引擎」那一档。

## 表里的行话，就近扫一眼

上面三张表冒出不少术语，按出现顺序各配一句白话：

| 术语 | 一句话白话 |
| --- | --- |
| 伪代码（pseudocode） | 把机器码「翻译成人能读的近似代码」，但不是原始源码 |
| 汇编（assembly） | 最贴近机器指令、但仍用人类可读助记符写的低级代码 |
| source map | 把压缩 / 编译后的 JS 映射回原始源码的对照表 |
| IPC | 进程间通信，多个进程之间互相传消息的通道 |
| CIL | .NET 程序编译后、运行前的那层「中间代码」 |
| WAL | SQLite 的预写日志：先写日志再改正式文件；快照 WAL，就是连「最近的改动队列」一起看 |
| WAT | WebAssembly 的文本格式，人可读的「wasm 源码」 |
| ptrace / PTY | ptrace 是「盯住另一个进程看它每条系统调用」的调试接口；PTY 是伪终端，让程序以为自己在跟真终端对话（进程捕获靠它） |
| ELF / Mach-O / PE | 三种可执行文件格式，分别对应 Linux / macOS / Windows 上的成品程序 |
| ABI | 应用程序二进制接口，决定编译出来的库和程序怎么互相调用 |
| plist | Apple 系统常用的属性列表文件，用来存配置和结构信息 |
| 载荷（payload） | 程序真正传输或执行的那部分数据内容本身，而非它的外壳 |

## 怎么挑第一个练手目标

看懂表之后，选目标有个简单顺序：

1. **先看手边有没有现成的第 ① 组目标**——一个 Electron 桌面应用、一个 .NET 程序、一个 SQLite 数据库文件，都能立刻开跑。
2. **想观察「点一下发生了什么」就选第 ② 组**——一个网站，配合浏览器记录点击后的网络请求。
3. **第 ③ 组留到最后碰**——它要你先备好工具或引擎，等把第 ①② 组的手感练出来，再回头对付原生二进制那类硬骨头。

> [!tip] 大白话
> 挑目标有点像学做菜先挑食材：冰箱里有什么、菜谱最基础的那道是什么，就先用它练手。所以第一次别去挑战「要专用刀具」的硬菜（第 ③ 组），拿个「随便切两刀」的（第 ① 组）先建立手感最稳妥。

## 这一章讲了什么

- REA 认得的可分析目标共 **22 类**（以英文 README 全表为准）。
- 按「要不要额外装东西」分三组：① 纯静态零引擎，② 需浏览器，③ 需额外工具 / 引擎。
- 第 ① 组五类：JavaScript / Electron、.NET、Go、Flutter、SQLite；第 ② 组一类：网站。
- 本笔记的两条实战只跑第 ①② 组，第 ③ 组只列名、不展开。
- 中文 README 表少 3 行（Go / WASM / SQLite），一律以英文 22 行为准，不据此删目标。

## 下一章预告

现在你知道 REA 能拆什么了，但工具还没接进你的 agent——下一章讲「装与接」：Node 的硬门槛、一次性接入要做哪几次确认，以及写进配置时要守的版本纪律。
<!-- END: 02_targets.md -->

<!-- SOURCE: 03_setup.md | 12145 bytes -->
# 第 3 章 装与接：Node 门槛、setup、MCP 与 CLI

前两章讲清了 REA 是什么、能拆哪 22 类目标，但工具还停在「货架上」——你的 AI agent 还不知道它的存在。本章就是「装与接」这一步：先过 Node 版本这道硬门槛，再用一条 `setup` 命令把 REA 接进你的 agent，最后分清「配置改了哪里」和「接好之后怎么用」。

> [!tip] 大白话
> 把这一章想成「给新买的电器插电、连 Wi-Fi」：插头规格不对（Node 版本不符），怎么按开关都白搭；连上网络（MCP 注册）之后，你才谈得上用它。所以顺序不能乱——先过门槛，再接入。

## 一、第一道门槛：Node 版本对不上，一切免谈

REA 是靠 Node.js 跑的（npm 包 `rea-agents`），所以它对运行环境有明确要求：支持 **`Node.js` 22.x（≥22.19）、24.x（≥24.11）、26+**；而 **23、25 以及预发布版（prerelease）不支持**（出处见 `sources/docs_installation.md:848`）。

注意这是「偶数大版本 + 补丁下限」的写法：不是「22 以上都行」，而是 22 这一代至少要 22.19、24 这一代至少要 24.11，被跳过的 23、25 干脆不要用。

装之前先自查，免得装到一半才发现版本不符：

```bash
# 在终端查看当前 Node 版本
node -v
```

如果打印出 `v22.19.0`、`v24.11.0`、`v26.0.0` 这类，就合格；若是 `v23.x` / `v25.x`，或 `v22.18.x` 及以下，先换版本再往下走。还有一条省心的提示：REA 只用「跟当前运行时配套的那个 npm」，**从不擅自升级 Node、npm 或 Homebrew**（`sources/docs_installation.md:848`），你不必担心它把你的环境改乱。

> [!tip] 大白话
> 把 Node 版本想成电器插头的规格：22.19、24.11 是「合格插头」的型号，23、25 是「规格怪、插不进」的型号。所以不是越新越好，是「对上号才通电」。

为什么要求长得这么「挑」？因为 REA 要长期跟 Node 的运行时行为打交道，只能承诺在它**测试过**的那几代上工作。把版本写死成「偶数大版本 + 补丁下限」，是为了让「我这一版到底跑不跑得起来」有确切答案，而不是给你一个含糊的「大概能跑」。对读者的实际意义是：**别用奇数版与预发布版冒险**，出了怪问题也很难归因。

## 二、一次接进你的 agent：`setup`

过了门槛，接入就一条命令（`sources/README.md:65`）：

```bash
# 首次接入：把 REA 注册到你的 AI agent
npx rea-agents setup
```

它不是「一键装完不吭声」，而是一段**让你把关的三步交互**（`sources/docs_installation.md:20`）：先选要配置的 agent → 复核它给出的路径与改动计划 → 批准。原文与中译见章末引文表。

这里有两点新手最容易忽略：

- **两次确认是分开的**。npm 下载这个包要你批准一次，REA 的 `setup` 真正改配置（或装 Hopper）前会再问一次（`sources/docs_installation.md:20`）。别以为「点了第一次」后面就自动放行。
- **选择列表本身有讲究**。多选里，已经存在 REA 注册的客户端默认勾选；新检测到的客户端只是「被看到」，默认**不**勾选——检测是给上下文用的，不等于授权你多注册一个（`sources/docs_installation.md:31`）。

`setup` 完成后会做三件事（`sources/README.md:68`，原文与中译见章末引文表）：加入 REA 的 MCP server、加入配套的工作流指引、并**备份**你原有的配置。最后一步别忘：**重启它点名的那几个 agent**，注册才会生效。

顺带记一句：`setup` 是可以重复运行的。以后要升级 REA，重跑一遍当前版本的 `setup`，它会刷新旧的注册，再让你重启客户端（`sources/docs_installation.md:811`）。所以「注册」不是一次性的死配置，而是跟着版本走的。

> [!warning] 接完别急着怪「没反应」
> 配置写好了但没重启 agent，是新手最常见的「明明装了却用不了」。看到 `setup` 的完成信息后，按它点名的客户端逐个重启一遍再验证。

### 怎么确认真的接上了

重启只是第一步，最好再做个「合上回路」的验证：

1. **看客户端**：在 agent 的 MCP / 工具列表里，应该能看到一个名为 `rea` 的 server。
2. **看命令行**：装好后在终端敲 `rea --help`，能列出命令就说明 CLI 这条路也通了。
3. **真问一句**：对你接好的 agent 提一个需要「看目标」的需求，看它是否真的去调 REA，而不是凭记忆瞎编。

三条里有一条不通，就回到上一节核对：是不是版本没换、是不是某个客户端忘了重启。这三步能挡掉绝大多数「以为装好了」的错觉。

## 三、它到底改了你配置里的什么

如果你用的是支持手动配置的客户端，`setup` 本质上就是往 MCP 配置里加了这么一段（`sources/docs_installation.md:799`）：

```json
{
  "mcpServers": {
    "rea": {
      "command": "npx",
      "args": ["-y", "rea-agents@6.4.0", "mcp"]
    }
  }
}
```

也就是说，agent 启动时用 `npx -y rea-agents@6.4.0 mcp` 把 REA 作为一个 MCP server 拉起来。这里有一条**版本纪律**必须知道：持久化的注册要锁定一个**确切**版本，而不是 `@latest`（`sources/docs_installation.md:811`，原文与中译见章末引文表）。

| 写法 | 后果 |
| --- | --- |
| `rea-agents@6.4.0`（确切版本） | 每次启动都是同一版，行为可预期 |
| `rea-agents@latest` | 哪天发新版就悄悄漂移，排查问题时版本对不上 |

`setup` 默认就是这么做的：它写入的注册会**钉在「执行 setup 的那个版本」**上（`sources/docs_installation.md:811`）。写进配置的当前参考版本是 **`rea-agents 6.4.0`**（发布检查日 2026-10-11，`sources/docs_installation.md:207`）。想更新旧注册，就用当前版本的 `setup` 重跑一遍，再重启客户端。

为什么非要钉死版本？因为 MCP 注册是「长期驻留」的配置——写一次，之后每次开 agent 都按它启动。若写成 `@latest`，某天上游发新版，你的 agent 就悄悄换了 REA 的版本，先前跑通的用法可能行为变了却没人提醒。钉死确切版本，等于给整套环境拍了一张**可回溯的快照**，出问题时能以版本为线索定位。

> [!tip] 大白话
> 把版本锁定想成配药时记下「药厂 + 批号」：只写「某某药」迟早会拿到换了配方的同名产品；记死批号，疗效对不上时才有据可查。所以配置里那串 `@6.4.0` 不是啰嗦，是你的「批号」。

## 四、接好之后怎么用：CLI 与 MCP 两条路

接入完成后，你有两条等价的路：

- **走 agent（MCP）**：直接对你的 AI agent 提需求，它自己经 MCP 调 REA。
- **走命令行（CLI）**：装好后直接用 `rea` 命令，CLI 复用与 agent 完全相同的那套工作流。

两条路不是「二选一」，而是同一套能力的两个入口：

| | 走 agent（MCP） | 走命令行（CLI） |
| --- | --- | --- |
| 你怎么用 | 用自然语言提需求 | 敲具体命令 |
| 谁来编排步骤 | agent 自己决定调哪个工具 | 你自己选命令、看参数 |
| 适合场景 | 边聊边查、让 agent 顺带解释 | 想可复现、可脚本化，或手上没有 agent |
| 底层工作流 | 同一套 | 同一套（复用） |

命令行的入口很朴素——不知道有哪些命令时：

```bash
rea --help
```

如果不想全局安装，就用 `npx` 临时运行（`sources/docs_cli.md:9`）：

```bash
# <command> 换成具体命令名；这是不装全局的一次性运行方式
npx -y rea-agents@latest <command>
```

本章只讲「入口」，具体命令留到后面实战章和第 8 章速查表。

## 五、必须分清的一对数字：21 个客户端 ≠ 17 个 client IDs

这一节是全篇最容易读错的地方，请停一下。

- **21**：`setup` 可配置的客户端**共 21 个**（`sources/docs_installation.md:266`）。列表里包括 Claude Code、Claude Desktop、Codex、Cursor、Gemini CLI、Windsurf、VS Code、GitHub Copilot CLI、Qwen Code 等。
- **17**：这是 **`6.4.0` 这个版本**的注册表包，实际接受 dry-run 安装计划的 **client ID 数量**（`sources/docs_installation.md:209`，原文与中译见章末引文表）。

两者**作用域不同**：21 说的是「setup 能配多少个客户端」，17 说的是「某一个版本在这一批里实际通过了多少」。它们不是矛盾，更不能合成一句「支持 17/21 个客户端」。

另外单独记一条：客户端表里的 **`dsh`（DeepSeek Harness）只是 main 分支上已支持，npm 6.4.0 里并不包含它**（`sources/docs_installation.md:290`）；拿 `@latest` 去配 `dsh`，会报「不支持的客户端」，得等 6.4.0 之后的发布版本。

> [!warning] 别把两个数缝在一起
> 「21」说的是可配置客户端的宽度，「17」说的是 6.4.0 该版本实际接受的 client ID 数。看到别处写「支持 17/21 个客户端」，那是把两个不同作用域的数混着念了。

## 六、新手常见坑速查

把这一章最容易踩的四个坑收成一张表，装的时候对照着看：

| 症状 | 多半原因 | 怎么办 |
| --- | --- | --- |
| 装不上或报环境错 | Node 版本不在 22.x（≥22.19）/ 24.x（≥24.11）/ 26+ | 用 `node -v` 确认，换到合格版本 |
| 装了但 agent「没反应」 | 忘了重启 agent | 按 `setup` 完成信息点名的客户端逐个重启 |
| 行为时好时坏、排查时版本对不上 | 注册写成了 `@latest` | 改成确切版本，如 `rea-agents@6.4.0` |
| 想配 `dsh` 却报「不支持」 | 6.4.0 里还不含 `dsh` | 等 6.4.0 之后的发布版本 |

## 这一章讲了什么

- 硬门槛：Node **22.x（≥22.19）/ 24.x（≥24.11）/ 26+**；**23、25 与预发布不支持**。
- 接入一条命令 `npx rea-agents setup`，流程是「选 agent → 复核计划 → 批准」，且 npm 下载批准与 setup 批准**各自独立**。
- setup 会加 MCP server + 工作流指引、备份原配置，完成后要**重启 agent**。
- 版本纪律：注册锁定**确切版本**，当前参考 **`rea-agents 6.4.0`**（2026-10-11），手动注册形如 `npx -y rea-agents@6.4.0 mcp`。
- 客户端口径：setup 可配置 **21** 个；**17** 是 6.4.0 该版本 dry-run 实际接受的 client ID 数，**勿混述**；`dsh` 仅 main、6.4.0 不含。

## 下一章预告

工具接好了，该动真格了。第 4 章会带你跑第一条零原生引擎的实战——对一个 JavaScript / Electron 应用做静态分析，看懂「点一下导出」背后跨进程的 IPC 链路，并学会怎么读它返回的证据。

---

## 引文对照（原文 / 中译 / 出处）

> 「出处」列标注引文逐字所在的来源文件与行号；查不到来源的写 `—`（宁空不猜）。产品文件名（如 `rea-agents`）不是来源件，故不进本表。

| 序号 | 原文 | 中译 | 出处 |
| --- | --- | --- | --- |
| 1 | “Choose the agents to configure, review the proposed paths and changes, and approve the plan.” | 先选要配置的 agent，复核计划的路径与改动，再批准该计划。 | `sources/docs_installation.md:20` |
| 2 | “Setup adds REA's MCP server and matching workflow instructions, with backups of existing configuration. Restart your agent afterward.” | setup 会加入 REA 的 MCP 服务和配套工作流指引，并备份原有配置；完成后重启 agent。 | `sources/README.md:68` |
| 3 | “Persistent registrations should use one exact package version.” | 写进 agent 配置的注册应锁定一个确切包版本。 | `sources/docs_installation.md:811` |
| 4 | “The actual registry package accepted dry-run setup plans for the 17 client IDs in that release, including Qwen Code, Pi and Hermes.” | 该版本的注册表包实际接受了针对 17 个 client ID 的 dry-run 安装计划，含 Qwen Code、Pi 与 Hermes。 | `sources/docs_installation.md:209` |
<!-- END: 03_setup.md -->

<!-- SOURCE: 04_js_electron.md | 16032 bytes -->
# 第 4 章 实战一：静态 JS/Electron 分析

本章带你跑通第一篇实战：把一个 Electron 桌面应用「拆开」，看清点一下「导出笔记」之后，程序到底做了什么。你不需要 Hopper、Ghidra、IDA 这类原生引擎，只需要第 3 章装好的 Node 与 REA 本身。读完这章，你应该能自己跑一条命令，并从返回结果里读出「哪个按钮、经过哪几段代码、写出了哪个文件」。

## 4.1 为什么第一站选「静态 JS / Electron」

零基础首跑，最怕两件事：一是「跑起来会不会出乱子」，二是「环境没配好、跑不动」。静态 JS/Electron 这条路把这两个顾虑同时按掉：它既不需要额外的原生引擎，也不启动你正在分析的应用。

先说两条贯穿本章的静态性口径，它们决定了这条路为什么最安全、最适合第一次上手：

| 它管什么 | 官方原文 | 说人话 |
|---------|---------|--------|
| 静态检查怎么运行 | “Static JavaScript and .NET inspection read the supplied files without running the application.” [^c4-1] | 拿到你给的文件就开始读，绝不动手把程序启动起来 |
| 静态图会不会执行代码 | “Static graph workflows do not execute recovered code.” [^c4-2] | 分析只能「看」和「画图」，不会顺手把恢复出来的代码跑一遍 |

**一句话概括**：REA 处理 JavaScript/Electron 时全程只「读文件」——既不起应用，也不执行分析里恢复出来的任何代码，所以你可以随时先做，不必担心「把程序跑起来会怎样」。真要确认「运行时确实干了什么」，那是第 5 章的运行时观测要解决的问题。

> [!tip] 大白话
> 把静态分析想成「只看图纸、不动机器」。工程师拆一台设备有两种做法：一种通电让它真正转起来对着看，另一种只摊开设计图纸逐张核对。静态 JS 分析就是后者——它翻你给的那堆 `.js` 文件，读出模块、导入、IPC 通道、handler 分别在哪儿，全程不按开机键。所以……你可以放心先读一遍，等确实需要「它运行时真的做了什么」时，再上运行时捕获。

还有一层很实用的理由：这条路的门槛只有 Node 和 npm。只要你第 3 章的安装跑通了，本章就能立刻跟着做，不用再去处理 Hopper 的许可、Ghidra 的临时库、IDA 的适配这些进阶话题（那些留给第 6 章）。样例本身甚至不需要装 Electron——它只是被当作一堆 JS 文件来读。

### 名词先扫盲

这一章会反复出现几个词，先各给一句大白话，正文里遇到就不再多解释：

| 名词 | 一句话说明 |
|------|-----------|
| Electron | 用网页技术（HTML/CSS/JS）写桌面应用的框架，界面和逻辑都是 JS |
| 渲染进程（renderer） | 负责「画界面」的前台进程，就是你在窗口里看到、点到的那个页面 |
| 主进程（main） | 负责「干脏活」的后台进程，比如读写文件、调用系统能力 |
| preload | 夹在两者中间的桥接脚本，决定页面能碰到哪些主进程能力 |
| IPC | Inter-Process Communication，两个进程之间「打电话」的通道 |
| handler | 接到电话后负责处理的那个函数 |
| 通道名 / 字面通道 | IPC 通道的名字，比如 `notes:export`；「字面」指它是代码里写死的字符串 |

## 4.2 这个示例应用在做什么

我们分析的样例是一个很小的 Electron 应用，解压后只有六个源文件：`package.json`、`main.js`、`preload.js`、`renderer.js`、`csv.js`、`index.html`。它的功能一句话说清：点界面上的「导出笔记」，把笔记写成一个 CSV 文件。

难点在于，这一次行为**横跨三个文件**：界面代码在 `renderer.js`，中间桥接在 `preload.js`，真正写文件在 `main.js`。人工去搜「CSV 到底在哪写的」，很容易只看到其中一段就下结论。我们要做的，就是让 REA 把这三段串起来。

如果你直接 `grep -r "csv" .` 去搜，其实很容易只命中 `csv.js` 和 `main.js` 这两处，看到「哦，CSV 是在 main.js 写的」就收工；但这样你并没有确认这三段属于**同一次调用**——`renderer.js` 里那个按钮到底有没有连到 `main.js` 这个 handler？通道名中途有没有被改过？静态分析的价值，正在于它不止给你片段，还把片段之间的**调用关系**一并连出来。

下面先逐段看代码。

### 第一段：界面上的按钮（renderer.js）

```javascript
// renderer.js
document.querySelector("#export").addEventListener("click", async () => {
  const destination = await window.notes.exportCsv();
  document.querySelector("#status").textContent = `Saved to ${destination}`;
});
```

读法：渲染进程只知道「有个叫 `window.notes.exportCsv` 的方法」，按钮一点就 `await` 它的返回值，再把结果写到状态行。真正的实现不在这里——它被藏在别处，页面只认这个方法名。

### 第二段：中间的桥（preload.js）

```javascript
// preload.js
contextBridge.exposeInMainWorld("notes", {
  exportCsv: () => ipcRenderer.invoke("notes:export"),
});
```

读法：`preload` 把 `exportCsv` 这个能力暴露给页面，而它内部其实只是调用 `ipcRenderer.invoke("notes:export")`。**注意这里的字面通道名 `notes:export`**——这就是后面结果里 `literal_channels` 要数的东西。

### 第三段：真正干活的 main.js

```javascript
// main.js
ipcMain.handle("notes:export", () => {
  const destination = path.join(app.getPath("downloads"), "notes.csv");
  writeFileSync(destination, toCsv(notes), "utf8");
  return destination;
});
```

读法：主进程用**同一个字符串** `"notes:export"` 注册了 handler，`csv.js` 负责把笔记拼成 CSV，`main.js` 把它写进用户的下载目录 `downloads/notes.csv`。到这里，「导出笔记写在哪」的答案已经明摆着——但前提是你能确认这三段属于同一条链，而不是三个互不相干的片段。

> [!tip] 大白话
> 把三个文件想成一条电话链：`renderer.js` 是按下号码的人，`preload.js` 是接线员，负责把这个号码转出去，`main.js` 的 handler 是真正接电话办事的人。关键在于——两边写的号码必须**一字不差**对得上（都是 `notes:export`），电话才接得通。静态分析干的事，就是核对「谁拨了号、谁在等这个号、号码是否对得上」。

把三段连起来看，你会发现一个关键点：三处代码是靠**同一个字符串** `notes:export` 维系在一起的——`preload.js` 用它拨号，`main.js` 用它接听。字符串一致，链就成立；哪天有人把这边改了、那边没改，这条链就断了。静态分析正是顺着这种「字面名字」去找、去配对的。

## 4.3 跑一次分析（动手实践 · 新手可跳过）

前置条件：第 3 章已经把 Node 与 REA 装好。这个小例子只需要 Node.js 和 npm，**不需要装 Electron**。

把示例下载解压后，在命令行里跑（命令逐字取自官方指南）：

```bash
npx -y rea-agents@latest analyze-javascript-application \
  /absolute/path/to/notes-example --json
```

把 `/absolute/path/to/notes-example` 换成你解压出来的 `notes-example` 文件夹。要分析自己的应用时，把参数换成它的**目录路径**或 **`.asar` 文件路径**，命令形式不变。

> macOS 请替换为你平台的可执行路径。

命令末尾的 `--json` 表示「给我 JSON 格式的结果」，方便程序和 agent 解析；不加它，终端会用人读更舒服的默认格式。命令跑完的退出码：`0` 表示完成（可能有部分证据或警告），`1` 表示没能完成，`128+N` 表示被信号 N 终止。

> [!warning] 常见坑
> 这里给的是**绝对路径**：从根目录写起（Linux/macOS 上以 `/` 开头）。写相对路径、或写到一半的目录，命令会找不到目标。另外别把它当成要「运行」这个 app——这条命令只是读它。

## 4.4 读懂结果：先看摘要，再看源码位置

命令返回的 JSON 里，有两个字段最值得先看：`normalized_result.summary.ipc`（计数摘要）和 `normalized_result.graph`（源码位置）。前者告诉你「有几条链、配没配上」，后者告诉你「每条链具体在哪个文件的哪一行」。

期望结果如下（官方指南记录，由 **REA 4.1.0** 产出）：

```json
{
  "literal_channels": 1,
  "renderer_transmissions": 1,
  "main_handlers": 1,
  "paired_renderer_transmissions": 1,
  "ambiguous_renderer_transmissions": 0
}
```

逐字段读法：

| 字段 | 数字 | 含义 |
|------|------|------|
| `literal_channels` | 1 | 代码里写死的 IPC 通道名有 1 个（就是 `notes:export`） |
| `renderer_transmissions` | 1 | 渲染端往外「拨号」1 次（`ipcRenderer.invoke`） |
| `main_handlers` | 1 | 主进程注册的 handler 有 1 个（`ipcMain.handle`） |
| `paired_renderer_transmissions` | 1 | 成功与 handler 配对的拨号 1 次——发送端和接收端对上了 |
| `ambiguous_renderer_transmissions` | 0 | 没能唯一配对的拨号 0 次——没有歧义 |

**一句话概括**：一个通道、一次拨号、一个 handler，而且成功配对、零歧义。这就是我们要的那条干净链路。

> [!tip] 大白话
> 把这几行数字想成收发室的对账单。`literal_channels` 是「登记过的分机号有几个」，`renderer_transmissions` 是「今天打出几通电话」，`main_handlers` 是「几个分机有人接」，`paired_renderer_transmissions` 是「打出去、且对方确实接起来的通话数」，`ambiguous_renderer_transmissions` 是「号码撞车、分不清接电话的是谁的次数」。全对上号、歧义为零，说明这条链清清楚楚。

### 再看源码位置：normalized_result.graph

`summary.ipc` 只给计数，不给「在哪」。想知道 `notes:export` 这个通道具体写在哪个文件、`notes.exportCsv` 的暴露点在哪，就要看 `normalized_result.graph`。它是一张按文件组织的关系图，把每个模块、每条通道、每个 handler 的**源码位置**挂上去；上一节的配对结论，就是从这张图推出来的。可以把它想成这样一个形状：

```text
normalized_result.graph
├── renderer.js   · 调用 window.notes.exportCsv        → 位置可见
├── preload.js    · 暴露 notes.exportCsv，绑定通道 notes:export
└── main.js       · handler notes:export               → 位置可见
    └── 写文件 downloads/notes.csv
```

有了这张图，你就能按图索骥回到源码逐行核对，而不是只信一个数字。

## 4.5 结论链：三行代码怎么串成一条证据

把上面三段代码接成一条证据，靠的是 REA 的配对逻辑：

| 它管什么 | 官方原文 | 说人话 |
|---------|---------|--------|
| 配对与 API 识别 | “REA matches the literal IPC call to its handler and identifies the exposed API. The path is inferred from code; a runtime capture can check what executes.” [^c4-3] | 按字符串把发送端和接收端对上号，顺便记下页面被暴露了哪些能力；路径靠读代码推出来，想核实就再抓一次真实运行 |

于是整条结论链是：`renderer.js` 调用 `window.notes.exportCsv` → `preload.js` 把它接到字面通道 `notes:export` → `main.js` 用同名通道注册 handler → handler 里 `csv.js` 拼 CSV、`main.js` 写文件。REA 把「字面 IPC 调用」和「唯一匹配的 handler」配成一对，同时识别出被暴露的 API（`notes.exportCsv`）。**路径是从代码里推断出来的**；如果你要确认「实际执行了什么」，就再用运行时捕获去校验一次——这正是第 5 章要做的被动观测。

这一步回答了本章开头的问题：CSV 由 `csv.js` 构造，由主进程写进用户的 `Downloads` 文件夹。

## 4.6 大应用注意：证据可能几百 MB

小例子读起来轻松，但你迟早会拿它去分析真正的大应用。这里有个必须提前知道的坑：**一个真实应用的完整证据可能达到数百 MB**。官方给的例子是——一份 **334 MB** 的 Obsidian 应用证据，投影成摘要视图后只有约 **10 KB**。

正确做法是：先把完整证据**落盘**到文件，再把它**投影**成一个小视图来读，不要直接往终端里灌。

```bash
rea analyze-javascript-application /absolute/path/to/app --json > app-evidence.json
jq -c '{source: {kind: "inline", evidence: .}, view: {kind: "summary"}}' app-evidence.json > app-view.json
rea inspect-analysis-view app-view.json
```

三行分别是：把完整证据存进 `app-evidence.json`；用 `jq` 包成一个「来源 + 视图」结构；再用 `inspect-analysis-view` 把它投影出来读。想换成别的切片时，把 `view` 换成模块页即可，例如 `{"kind": "page", "collection": "modules", "offset": 0, "limit": 32}`。

> [!warning] 常见坑
> 别把几百 MB 的 JSON 直接 `cat` 或整段丢给 AI agent——既读不动也吃满上下文。先落盘、再投影，永远只读那一小块视图。这也是 `inspect-analysis-view` 存在的意义：它是大证据的「取景框」。

还有一点值得记住：这份大证据是可以**复用**的。你先把 `app-evidence.json` 落盘留好，之后想换角度看，只要重新生成一个视图文件、再 `inspect-analysis-view` 一次即可，不必把那个大应用再重跑一遍。

## 本章小结

- 静态 JS/Electron 是零原生引擎的第一次实战：只读文件、不运行应用，也不执行恢复出来的代码。
- 示例场景横跨 `renderer.js → preload.js → main.js`，靠**字面 IPC 通道名**把三段接起来（本例是 `notes:export`）。
- 命令是 `analyze-javascript-application <绝对路径> --json`，参数可以是目录或 `.asar`。
- 读结果先看 `normalized_result.summary.ipc` 的计数（通道数、拨号数、handler 数、配对与歧义数），源码位置在 `normalized_result.graph`。
- 大应用的完整证据可达数百 MB，先落盘再用 `inspect-analysis-view` 投影成小视图来读。
- 路径由代码推断；要确认「实际执行了什么」，用运行时捕获再校验。

## 下一章预告

静态分析告诉我们「代码打算做什么」，但它不会替你验证「点下去那一刻，程序真的做了什么」。下一章我们换一条同样不需要原生引擎的路：给浏览器装个「行车记录仪」，用被动观测的方式，看一次真实的点击究竟发出了哪些请求、由哪段脚本发起、响应长什么样。

## 引文对照（原文 / 中译 / 出处）

> 下表逐字保留本章出现的英文整句引文。出处列指向 `sources/` 的原文文件与行号；`—` 表示查不到来源（宁空不猜）。正文里列举的产品文件名（如 `export.js`）不是来源件，故不进出处列。

| 序号 | 原文 | 中译 | 出处 |
|------|------|------|------|
| 1 | “Static JavaScript and .NET inspection read the supplied files without running the application.” | 静态 JavaScript 与 .NET 检查只读所给文件，不运行应用。 | `sources/README.md:178` |
| 2 | “Static graph workflows do not execute recovered code.” | 静态图工作流不会执行恢复出来的代码。 | `sources/docs_javascript-application-workflows.md:303` |
| 3 | “REA matches the literal IPC call to its handler and identifies the exposed API. The path is inferred from code; a runtime capture can check what executes.” | REA 把字面 IPC 调用与其 handler 配对，并识别被暴露的 API；路径由代码推断，运行时捕获可再校验实际执行了什么。 | `sources/guide_javascript.txt:46-48` |

[^c4-1]: 出处 `sources/README.md:178`。
[^c4-2]: 出处 `sources/docs_javascript-application-workflows.md:303`。
[^c4-3]: 出处 `sources/guide_javascript.txt:46-48`。
<!-- END: 04_js_electron.md -->

<!-- SOURCE: 05_browser.md | 14182 bytes -->
# 第 5 章 实战二：网站与浏览器观测

实战一里，我们用静态分析读懂了 Electron 应用的代码。但静态分析只读文件、不运行程序，它能回答「代码里写了什么」，却回答不了另一个同样常见的问题：在一个网站上点一下按钮，那一刻到底发生了什么？发出了什么请求、服务器返回了什么、又是谁发出的？本章用 REA 的浏览器观测能力，把一次点击背后的网络请求整条抓出来看清楚。

> [!tip] 大白话
> 把浏览器观测想成给浏览器装一台「行车记录仪」：它只负责把画面录下来，绝不替你踩油门、打方向。所以这次调查里，「点哪个按钮、什么时候点」完全由你决定，REA 只在你点下去的那一刻，把当时发出的网络请求、以及发起它的脚本如实记下。

## 一、这一章要抓的：点一下之后发生了什么

官方给的示例是一个叫 Notes browser 的小网页，上面有个 Export notes 按钮。点下去，它做一个很典型的动作：加载 `notes.json`，把里面的两条笔记格式化成 CSV，然后触发一次下载。整条链路浓缩成一行就是：`GET notes.json → 200 → notes[] → CSV`。

这条链路里三个人分工明确：**你**负责动手点，**REA** 负责记录那一刻的请求，**你的 agent** 负责把记录到的请求对回到脚本里那行发起它的代码上。官方把这三步讲得很清楚：

| 谁 | 做什么 |
| --- | --- |
| 你 | 在观测窗口开着的时候，手动点 Export notes |
| REA | 从选中的那页记录请求 URL、响应状态和 JSON 结构 |
| 你的 agent | 把观测到的请求，接到 `export.js` 里发起它的那行代码上 |

有一个顺序必须记牢：**先让观测开始，再点按钮**。观测窗口只覆盖它开着的那段时间——窗口开始之前发生的请求，一律落在记录之外。

> [!tip] 大白话
> 观测窗口就像一段「限时录像」：你按下录像键，它才开始录；你按下停止键，它就收工。所以要在点按钮之前先把录像打开，否则这次点击根本不会被录进去。

那为什么这一步非要用「运行时」的方式？因为发出去的请求、响应回来的状态码和结构，都是程序**跑起来那一刻**才产生的——它们既不在源码里，也不在静态文件里。静态分析能告诉你「有一段代码会去取数据」，但「这次点击实际取的是哪个 URL、服务器回了什么状态」，只有把浏览器真的跑起来、记下它的行为才有答案。这正是运行时观测补上的那一块，也是它和实战一相互配合的地方。

## 二、先扫盲：四个词

这一节出现的词，第一次见面就先记住它们的白话意思：

| 术语 | 一句话白话 |
| --- | --- |
| CDP（Chrome DevTools Protocol） | Chrome 系浏览器对外开的一个「调试插座」，外部程序接上它，就能读取页面信息 |
| target（页面 target） | 浏览器里一个可被观测的页面；你得先点名「盯哪一个页面」 |
| 观测窗口（observation window） | 一段限定时长的记录区间，只记这段时间里发生的事 |
| 被动（passive）/ attach | 只「接上」已经在跑的目标做记录，不启动它、不驱动它、不改动它 |

REA 要接的，是**你自己拥有的**浏览器：它通过 CDP 接到一个已经在运行的 Chrome 系浏览器上，对现有页面产出**有边界**的证据。既然是「接上去」，那这个浏览器得先由你启动好、由你控制——REA 全程不启动、不拥有、也不关闭它。

这里最需要分清的是「主动」和「被动」两条路。主动的浏览器自动化（Playwright 那类工具）是自己去启动浏览器、替你把动作做一遍；REA 走的是相反的路——它接上一个**已经由你开好、由你操作**的浏览器，只当观察者。官方把这两条路严格分开，正因为它们的「权责」不同：一个拥有并驱动整个运行时，另一个只是挂上去记录。记住这条分界，你就能理解本章后半段为什么要反复强调「它不是浏览器自动化」。

## 三、动手实践：四步抓一次点击（新手可跳过）

下面四步在 Linux 上演示，命令取自官方指南原文、逐字保留。如果你在 macOS 上，请把命令里的 `google-chrome` 换成你平台安装的浏览器可执行路径（官方原话是「用你平台安装的浏览器可执行路径」，原文与中译见章末引文表）——这一步只换路径，命令的其余部分不变。

### 步骤 1：用独立 profile 起一个可控的浏览器

```bash
google-chrome \
  --remote-debugging-port=9222 \
  --user-data-dir=/tmp/rea-notes-browser \
  https://rea.tools/examples/notes-web/
```

三个参数分别管什么：

- `--remote-debugging-port=9222`：在本地开一个调试端口，REA 后面要连的就是它（对应端点 `http://127.0.0.1:9222`）。
- `--user-data-dir=/tmp/rea-notes-browser`：让这次调查用一个全新、独立的浏览器 profile，不碰你日常登录的那套数据。
- 最后的 URL：要打开的页面，你可以换成任何想检查的页面。

再强调一次：REA 不启动、不拥有、也不终止这个浏览器，它只是接上去。页面由你控制，动作由你执行，调查结束时浏览器也由你自己关掉。

> [!warning] 别把调试端口开到公网
> 调试端口只连本机回环地址，不要把它暴露到非回环的网络接口上；本次调查请用一个专用 profile，别拿你日常浏览器的 profile 来开。

### 步骤 2：找到那一页的 target

```bash
npx -y rea-agents@latest list-browser-targets \
  http://127.0.0.1:9222 --json
```

这条命令列出该端点下**所有符合条件的页面 target**。从中挑出 URL 是 Notes 示例的那个，记下它的 ID——下一步要用它（下文用 `TARGET_ID` 代指）。

### 步骤 3：打开观测窗口，再点 Export notes

```bash
npx -y rea-agents@latest inspect-web-page \
  http://127.0.0.1:9222 TARGET_ID \
  --observation-ms 10000 \
  --include-accessibility-text \
  --include-json-body-shapes --json
```

三个要点：

- 把 `TARGET_ID` 换成上一步记下的那个 ID。
- `--observation-ms 10000`：观测窗口开 **10 秒**。
- `--include-accessibility-text` 与 `--include-json-body-shapes`：顺便把可访问性文本、以及 JSON 响应的结构也记下来。

命令连上后会给几秒缓冲——**先等它连上，再切回浏览器点 Export notes**。结果会在观测窗口结束后返回。窗口之外的请求不算数。

### 步骤 4：读结果

官方在本地 Notes 示例上用 REA 4.1.0 记录到的结果，是下面四项：

| 抓到的项 | 值 |
| --- | --- |
| 请求 | `GET /examples/notes-web/notes.json` |
| 响应 | `200 · application/json` |
| 请求发起者 | `export.js · script` |
| 响应结构 | `notes[]`，含 `id`、`title` 字段 |

把这张表连起来读：这次点击发出了一个对 `notes.json` 的 GET 请求，返回 `200` 且内容是 `application/json`，发起它的是 `export.js`，响应体是一个 `notes[]` 数组，每条含 `id`、`title`。一句话结论：**这次点击请求了 `notes.json`**，而 CSV 是由 `export.js` 在页面里构造出来的。

那行发起请求的脚本长这样：

```javascript
// export.js · 示例源码节选（只保留与发起请求直接相关的两行）
const response = await fetch("./notes.json");
const { notes } = await response.json();
```

脚本拿到 JSON 之后，把每条笔记拼成一行 CSV，再造一个 Blob 对象、生成一个临时下载链接、触发一次点击，下载就开始了。这几步都发生在页面内部——网络观测能证明「这次点击请求了 `notes.json`」，证明不了 CSV 具体是拼的。

想直接看脚本源码，可以再跑一次并加上 `--include-script-sources`：

```bash
npx -y rea-agents@latest inspect-web-page \
  http://127.0.0.1:9222 TARGET_ID \
  --include-script-sources --json
```

## 四、跑不通时，先查这四个坑

第一次跑，多半会在一两个小地方卡住。下面四个是最常见的现象，对号入座即可（下表也是「现象 → 原因 → 对策」）：

| 现象 | 大概率原因 | 怎么办 |
| --- | --- | --- |
| 结果里什么请求都没有 | 观测窗口是在点击**之后**才开的 | 回到步骤 3，**先让命令连上、再点按钮** |
| 结果不完整、漏了那次点击 | 观测窗口太短 | 把 `--observation-ms` 调大（示例里给的 10000 毫秒 = 10 秒） |
| 记到的是别的页面 | 浏览器开着多个页面 target | 回步骤 2，按 URL 选中 Notes 示例那一页，用它的 ID |
| Linux 上 Chrome 卡在首次导航前 | 桌面钥匙环（keyring）被锁住 | 给这个专用 profile 加 `--password-store=basic` 绕过钥匙环 |

最后一行是 Linux 特有的环境问题：官方说明里专门提过，一个可达但被锁住的桌面钥匙环，会让 Chrome 卡在第一次导航之前；对「专用调查 profile」这种场景，加上 `--password-store=basic` 就能绕过它。

> [!tip] 大白话
> 这四条可以压成一句口诀：**窗口先开、时间给够、目标选对、环境放行**。前三步都是操作顺序或选择的问题，最后一条是 Linux 环境特有的；很多时候换一个干净的专用 profile 重来，问题就消失了。

## 五、当场划清边界

链路跑通之后，很容易让人以为它是个「浏览器机器人」。它不是。官方对它的定性非常明确：**这是一种被动的逆向能力，不是通用的浏览器自动化或远程控制面**（英文原文与中译见章末引文表）。

这句话不是客套，它对应一长串「刻意不做」的清单：它**不**提供通用 CDP 命令、不提供 `Runtime.evaluate`、不做页面导航、不注入输入、不触发下载、不关闭页面或浏览器；截图是唯一的像素输出，而且只在你明确要求时才返回。一次观测结束后，REA 会把自己启用过的域关掉、断开目标会话，并且只关闭它自己那条 WebSocket。

> [!tip] 大白话
> 这就像行车记录仪：它能证明「你刚才往哪开了」，但它本身不会开车、不会替你拐弯。所以别指望用它去自动点按钮、跑测试——那不是它的活儿。

还有一层更容易被忽略的边界：**它不是浏览器沙箱，也不做网络隔离**（英文原文与中译见章末引文表）。被接上的页面和浏览器，仍然以它们原有的权限继续运行，可以独立于 REA 向外部发请求；而 CDP 对选中的浏览器 profile 有很深的访问权。所以官方的建议是：**用专用 profile，只纳入你打算检查的那些 origin**，并把同一操作系统用户下的其它进程，视为这条边界之外的东西。

顺带记一个实操细节：观测默认的范围是所选 target 的**当前 origin**，而 origin 过滤只认「协议 + 主机 + 端口」三段——路径、凭据、查询串、片段、通配符都不算合法 origin。也就是说，你写不出一条「只盯某个路径」的过滤规则；要把观察范围收窄，靠的是「只起一个专用 profile、只打开你要看的那一页」。这也正是官方那句建议落在「专用 profile + 只纳入要检查的 origin」上的原因。

> [!warning] 三条边界，记牢
> ① **被动**——只记录，不自动化、不远程控制；② **非沙箱**——挡不住本来就以同一用户身份在跑的恶意进程；③ **非网络隔离**——页面该向外发的请求照发。这三条在第 7 章讲安全时还会再呼应一次。

## 六、这一章讲了什么

- 浏览器观测回答的是「点一下之后发生了什么」，抓的是**运行时**的网络行为，和静态分析互补。
- 三步主线：用**独立 profile** 起 Chrome 远程调试 → `list-browser-targets` 找页面 target → `inspect-web-page` 开观测窗口并点击。
- 观测窗口只在开着的那段时间记录，并且必须**先开始观测、再点按钮**。
- 示例结果：点击发出 `GET notes.json`（响应 `200 · application/json`），发起者是 `export.js`，响应是 `notes[]`（含 `id`、`title`）；结论是「**这次点击请求了 `notes.json`**」。
- 边界：**被动**能力，**非**自动化 / 远程控制面、**非**沙箱、**非**网络隔离；请用专用 profile、只纳入要检查的 origin。

## 七、下一章预告

到这里，两条「零原生引擎」的实战都跑通了：静态 JS/Electron 和网站观测，两者都不需要额外装分析引擎。可一旦目标换成原生二进制（ELF、PE、Mach-O），REA 就需要一个「分析引擎」来接棒——Hopper、Ghidra、IDA 到底怎么选、各自在哪些平台可用、哪些平台会踩坑？这是下一章《进阶：provider 选择与平台限制》要讲的内容。

---

## 引文对照（原文 / 中译 / 出处）

> 「出处」列标注引文逐字所在的来源文件与行号；查不到来源的写 `—`（宁空不猜）。产品文件名（如 `export.js`、`notes.json`）不是来源件，故不进本表。

| 序号 | 原文 | 中译 | 出处 |
| --- | --- | --- | --- |
| 1 | “This is a passive reverse-engineering capability, not a general browser automation or remote-control surface.” | 这是一种被动的逆向能力，不是通用的浏览器自动化或远程控制面。 | `sources/docs_browser-observation.md:9` |
| 2 | “This feature is not a browser sandbox or network containment mechanism.” | 这个功能不是浏览器沙箱，也不做网络隔离。 | `sources/docs_browser-observation.md:229` |
| 3 | “Use your installed browser's executable path on macOS or Windows.” | 用你平台上已安装的浏览器可执行路径（macOS 或 Windows）。 | `sources/guide_browser.txt:62` |
| 4 | “The download is constructed in the page using the JSON response.” | 这次下载是在页面内用 JSON 响应构造出来的。 | `sources/guide_browser.txt:160` |
<!-- END: 05_browser.md -->

<!-- SOURCE: 06_providers.md | 16144 bytes -->
# 第 6 章 进阶：provider 选择与平台限制

前五章跑通的目标——静态 JS/Electron、网站观测，还有第 2 章点名过的 .NET、Go、SQLite——都属于「零原生引擎」：有 Node.js 环境就能跑，不用额外装大型分析软件。可一旦目标换成**原生二进制**（编译完只剩机器码的那种 ELF、PE、Mach-O 文件），REA 就得请一个「分析引擎」来接棒。本章回答三个问题：什么时候真的需要引擎、Hopper/Ghidra/IDA 三个引擎怎么选、哪些平台能跑哪些跑不了。

> [!note] 进阶内容，可以晚点读
> 如果你现在只想分析 JS/Electron 应用或网站，这一章可以直接跳到第 7 章。原生二进制分析不是入门必经之路——**新手可跳过**，等真遇到「只有一堆没源码的二进制」时再回来。

## 一、先判一件事：这个目标需不需要引擎

在挑引擎之前，先别急着装。因为很多目标其实**根本不需要引擎**。官方的边界划得很清楚：

| 它管什么 | 官方原文 | 说人话 |
|---------|---------|--------|
| 谁不需要引擎 | “Static JavaScript and .NET inspection read the supplied files without running the application.” [^c6-1] | 静态的 JavaScript 与 .NET 检查只读你给的文件、不运行程序，所以无需分析引擎 |

换句话说，**.NET 和 JS 走的是一条「只读文件」的路**：REA 直接读那些脚本和程序集，把它们拆开看，而不去执行。这条口径和第 4 章一致——静态分析安静、不运行应用。本章要讲的 provider，只对**另一条路**的目标才登场：那些必须真的把机器码读进来做反汇编、反编译的原生二进制。

> [!tip] 大白话
> 把目标想成两种车：JS/.NET 像一辆电路图齐全的车，翻图纸就能看懂（只读文件）；原生二进制像一辆只剩发动机、没有图纸的车，你得上举升机、拿专用工具拆。**provider 就是那台举升机**——目标不需要拆发动机的时候，你根本不用把它开出来。

## 二、三类 provider：Hopper、Ghidra、IDA

**provider** 这个词第一次出现，一句话解释：它是 REA 对接某个**分析引擎**的适配层——REA 自己不造引擎，而是把已有的引擎「接」进来，再把它翻译成统一的 `analyze` / `decompile` 等命令。三个 provider 对应三种引擎，定位差别很大：

| provider | 它是什么 | 谁负责装 / 谁负责留 | 平台上要注意的 |
|---------|---------|-------------------|--------------|
| **Hopper** | 独立商业软件，有自己的许可与免费 demo | REA 复用你**已经装好**的 Hopper，卸载时也**保留**它，不会替你删 | 属于支持的原生宿主基线：macOS 12+、Ubuntu 24.04+、Fedora 41+ 等 |
| **Ghidra** | 开源引擎，REA 把目标导入一个**临时库** | REA 自己起临时 Ghidra 库 | Linux/macOS 支持只读分析 **+** 函数名/入口注释的原子修改；**Windows P0 仅只读** |
| **IDA** | 商业反汇编器，通过**既有的 IDA MCP server** 接入 | REA **不**安装、不升级、不激活、不授权 IDA | 需要你自己先把 IDA 和上游 MCP 配好 |

先把两条最容易被误读的官方原话摆出来，对照着看：

| 它管什么 | 官方原文 | 说人话 |
|---------|---------|--------|
| Ghidra 的能力边界 | “REA imports one target into an ephemeral Ghidra database. Linux/macOS support read-only analysis and atomic function-name/entry-comment edits; Windows P0 is read-only.” [^c6-2] | REA 把**单个**目标导进一个**临时**库；Linux/macOS 除了只读分析，还能把函数名、入口注释这类改动**原子地**写进去；Windows P0 阶段只能读 |
| IDA 的接入方式 | “REA adapts an existing IDA MCP server into its native analysis tools.” [^c6-3] | REA 是把**你已经装好的** IDA 的 MCP server **适配**成自己的分析工具，而不是替你装一个 |

两条读完，三个引擎的性格就出来了：**Hopper 是「你有我就用」**（独立商业软件，REA 只做复用和保留）；**Ghidra 是「我自带临时库」**（REA 自己起库，改完即走，还能在 Linux/macOS 上落一点注释）；**IDA 是「我只串你现有的」**（复用你配好的 IDA MCP，绝不碰它的安装与授权）。

上面两句里冒出了两个需要当场解释的词。**headless**（无界面）指引擎不是开着一个图形窗口让你手点，而是在命令行 / 后台方式下被驱动——下一节 IDA 的已验证组合里就会用到这个说法。**P0** 指 REA 给 Windows 上的 Ghidra 划的一条**实验性阶段边界**：这个阶段只开放「只读」这一档能力，先把基础稳住再谈写。所以「Windows P0 仅只读」的正确读法是「Windows 上的 Ghidra 目前处于只读的实验阶段」，而不是「Windows 永远只能读」——阶段是会往前走的。

如果一时记不住三个引擎各自的脾气，可以反过来从目标倒推：先问「我这个目标属于哪一类」，再决定要不要请引擎。

| 你的目标 | 走哪条路 |
|---------|---------|
| JavaScript / Electron 应用 | 不用引擎，静态分析（第 4 章） |
| .NET 程序集 | 不用引擎，静态检查（只读文件、不运行） |
| Go 二进制 / SQLite / Flutter | 不用引擎（第 2 章点名的零引擎目标） |
| 原生二进制 ELF / PE / Mach-O | **需要引擎**：Hopper、Ghidra、IDA 三选一 |

这张图的用法是：只要你的目标落在前三行，本章后面的 provider 选择对你都「用不上」——真正需要对着这张表往下走的，只有最后一行那类「只剩机器码」的原生二进制。

> [!warning] Ghidra 的两处「限定」
> 官方原话里还跟着两句必须一起记住的限定：GUI 控件与持久库修改**不可用**，且**可执行字节保持不变**。意思是——在 Ghidra 里你得到的是「临时的一份分析」，改动（函数名、入口注释）写回的是 REA 的库而不是目标文件本身，目标二进制的字节始终不动。

> [!tip] 大白话
> 把三个引擎想成修车时借工具的三种关系：Hopper 像「用你自己车库里的那台专用设备」（是你的，我只是借用），Ghidra 像「我自带一台便携桌、现搭现拆、拆完就收走」，IDA 像「我只用你已经接好的那套仪器，绝不碰你的电源和授权」。

## 三、IDA 的已验证组合：别把「没测过」当「支持」

IDA 这条路最需要小心，因为它是**复用你已有的环境**——你手上的 IDA 版本和平台，未必是官方真正验证过的那一组。官方把**已验证组合**列得很窄：

| 平台 / 运行方式 | 已验证的 IDA | 出处依据 |
|----------------|-------------|---------|
| Windows x64 headless | IDA 9.3 | `sources/docs_ida-provider.md:145` |
| macOS arm64（headless） | IDA Professional 9.1（build 9.1.250226） | `sources/docs_ida-provider.md:143` |
| 原生 Windows（非 headless） | IDA Pro 9.3 | `sources/docs_ida-provider.md:145` |

关键在于官方接下去的定性：**其它 IDA 版本、其它架构、Linux headless 引擎、以及现代「附加式」GUI 工具，都需要各自的真实工作流跑过之后才能声称支持**。这不是保守的说辞，而是把「验证过」和「没验证过」明确分开。换句话说，表里那三行之外的一切——哪怕听起来只是换了个小版本——都还停留在「等一次真实工作流来证明」的状态。

> [!warning] 常见坑：没测过 ≠ 不支持，但也不等于支持
> 别把 macOS arm64 上验证过的 **9.1** 直接搬到 Windows，也别以为「IDA 能连上」就等于「这个版本被支持」。官方说的是「其余平台/版本**未声称支持**」——你可以自己试，但要清楚这是在支持范围之外，出问题别归因到 REA。

> [!tip] 大白话
> 这就像药品说明书上的「适应人群」：它只对做过临床试验的那几组（这里的几个平台 × 版本组合）背书；你换一组人吃，未必出事，但那不在「已验证」的名单里。**名单窄，是诚实，不是能力弱。**

## 四、怎么选：能自动就自动，要指定就显式

选 provider 的规则很朴素，一句话：**只有一个可用就自动，多个可用才要你点名**。REA 会看目标支持哪些 provider——若只有一个支持，它直接用；若有多个，就得你显式指定，否则会返回一个「选择有歧义」的错误。

指定有四个落点，任选其一或按优先级叠用（以下命令，**新手可跳过**，等真正调用时再照抄）：

```bash
# 1) 单次命令里用 --provider 显式指定
rea analyze /absolute/path/to/program --provider hopper
```

```bash
# 2) 用环境变量设一个「长期默认」，免得每次都打 --provider
export REA_ANALYSIS_PROVIDER=ghidra
```

```json
// 3) 在 MCP 里调用 open_binary 时传 provider_id
//    （你的 agent 经 MCP 调 REA 时，这里填 provider 的标识）
{ "open_binary": { "path": "/absolute/path/to/program", "provider_id": "ida" } }
```

优先级要记牢：**显式的 `--provider` 会覆盖环境变量 `REA_ANALYSIS_PROVIDER`**。也就是说，环境变量设的是「平时默认用哪个」，命令行上临时写的那一个优先级更高，用来应对例外情况。

> [!tip] 大白话
> 把这三个落点想成「临时决定 / 个人习惯 / 系统设定」三层：`--provider` 是这次临时拍的板，`REA_ANALYSIS_PROVIDER` 是你平时的默认口味，MCP 里的 `provider_id` 是 agent 代你下单时写的备注。**临时的板永远压过平时的口味。**

## 五、平台限制：这几个坑先知道

引擎选好了，还得看**这个平台上这条能力能不能跑**。最容易踩的一类限制，是「运行时捕获」（进程行为捕获）——它当前**只支持 Linux/macOS**：

| 它管什么 | 官方原文 | 说人话 |
|---------|---------|--------|
| 进程捕获的主机前提 | “Capturing a new scenario currently requires Linux or macOS and a working native PTY backend.” [^c6-4] | 当前要捕获一个新的运行场景，需要 Linux 或 macOS，外加一个可用的**原生 PTY 后端** |

所谓 **PTY 后端**，一句话解释：它是让程序以为自己连在一个「终端」上的底层机制，REA 靠它来驱动并记录进程行为。官方还补了缘由——**原生 Windows 捕获暂不可用**，是因为 PTY 适配器还无法验证「子进程是否被彻底清理」；重装 Windows 的 PTY 二进制也**不会**让这条路变得可用。想在 Windows 上做，官方给的迂回是：**在 WSL 里用 Linux 版 REA**，并把场景适配到那个 Linux 宿主上（这仍不等于捕获了原生 Windows 的进程树）。

除了进程捕获，还有几条能力被限定在 Linux 上：

| 能力 | 平台限制 |
|------|---------|
| 进程行为捕获 | 目前需 Linux 或 macOS，且要有原生 PTY 后端（原生 Windows 不可用） |
| 固件分析（Binwalk / Unblob） | 限 Linux |
| EVM 字节码 | 限 Linux |
| 部分抓包路径 | 限 Linux |

> [!tip] 大白话
> 把这些限制想成「某些工具只在特定车间能用」：进程捕获那台仪器需要一种叫 PTY 的「终端插座」，目前只有 Linux/macOS 车间配了；固件、EVM、部分抓包则干脆只在 Linux 车间开箱。**在 Windows 车间硬试，不是配置问题，是这台仪器还没搬过来。**

## 六、自查：三条命令把「能不能跑」问清楚

与其猜，不如直接问 REA。三条命令各管一件事（**新手可跳过**，遇到问题再回来查）：

```bash
rea providers --json      # 列出可用的 provider（有哪些引擎可选）
rea capabilities --json   # 列出能力项（哪些辅助能力可用，附带前提）
rea doctor --provider ID --json   # 诊断指定引擎是否就绪（ID 换成 hopper / ghidra / ida）
```

- `providers --json` / `capabilities --json`：官方说明它们描述的是「二进制会话的 provider」与「辅助能力」。想拿到**完整的 MCP 面**（agent 实际能调的全部工具），要看**连上的 server 返回的工具列表**，而不是文档快照——文档可能滞后于你手上这个版本。
- `doctor --provider ID --json`：当你遇到 `provider_unavailable`（引擎不可用）时，用它来诊断选中的引擎到底卡在哪。
- 若报的是「选择有歧义」（`ambiguous`），就从错误里的 `details.candidate_ids` 里挑一个，再用 `--provider` 明确指定。

> [!tip] 大白话
> 这三条命令像进车间前的「开工前检查」：`providers` 看有哪几台机器在、`capabilities` 看今天开哪些工位、`doctor` 则是给某台机器做一次通电自检。**先自检、再开工**，比拆到一半发现引擎没就绪划算得多。

## 本章小结

- **先判需不需要引擎**：静态 JS 与 .NET 检查只读文件、不运行应用，不需要引擎；本章讲的 provider 只服务「原生二进制」这类需要反汇编的目标。
- **三个 provider**：Hopper（独立商业软件，REA 复用你已装的并保留）、Ghidra（REA 起临时库；Linux/macOS 可只读分析 + 原子改函数名/入口注释，Windows P0 仅只读）、IDA（适配你既有的 IDA MCP server，REA 不装/不升级/不激活/不授权）。
- **IDA 的已验证组合很窄**：Windows x64 headless = IDA 9.3、macOS arm64 = IDA 9.1、原生 Windows = IDA Pro 9.3；**其余平台/版本未声称支持**。
- **选择规则**：只有一个可用就自动选；多个则用 `--provider` 显式指定，`REA_ANALYSIS_PROVIDER` 设默认，MCP 里传 `provider_id`；显式 `--provider` 覆盖环境变量。
- **平台限制**：进程行为捕获需 Linux/macOS + 原生 PTY 后端（原生 Windows 不可用）；固件、EVM、部分抓包路径限 Linux。
- **自查三连**：`providers --json`、`capabilities --json`、`doctor --provider ID --json`。

## 下一章预告

到这里，「能分析什么、怎么装、两条实战、引擎与平台」都讲完了，但还有一条最重要的边界没正面谈：REA 明确**不帮**你做哪些事、它的安全机制又能挡住什么、挡不住什么。下一章《边界与安全》会把这些红线一次说清，尤其是那个容易被误解的点——它**不是沙箱**。

---

## 引文对照（原文 / 中译 / 出处）

> 下表逐字保留本章出现的英文整句引文。出处列指向 `sources/` 的原文文件与行号；`—` 表示查不到来源（宁空不猜）。正文里列举的产品名与文件名（如 `REA_ANALYSIS_PROVIDER`、`provider_id`、`open_binary`）不是来源件，故不进出处列。

| 序号 | 原文 | 中译 | 出处 |
|------|------|------|------|
| 1 | “Static JavaScript and .NET inspection read the supplied files without running the application.” | 静态 JavaScript 与 .NET 检查只读所给文件，不运行应用。 | `sources/README.md:178` |
| 2 | “REA imports one target into an ephemeral Ghidra database. Linux/macOS support read-only analysis and atomic function-name/entry-comment edits; Windows P0 is read-only.” | REA 把单个目标导入临时 Ghidra 库；Linux/macOS 支持只读分析与函数名/入口注释的原子修改，Windows P0 仅只读。 | `sources/docs_ghidra-provider.md:3` |
| 3 | “REA adapts an existing IDA MCP server into its native analysis tools.” | REA 把既有的 IDA MCP server 适配成自己的原生分析工具。 | `sources/docs_ida-provider.md:3` |
| 4 | “Capturing a new scenario currently requires Linux or macOS and a working native PTY backend.” | 当前捕获新场景需要 Linux 或 macOS 以及可用的原生 PTY 后端。 | `sources/docs_process-capture.md:17` |

[^c6-1]: 出处 `sources/README.md:178`。
[^c6-2]: 出处 `sources/docs_ghidra-provider.md:3`（该句跨原文第 3–5 行）。
[^c6-3]: 出处 `sources/docs_ida-provider.md:3`。
[^c6-4]: 出处 `sources/docs_process-capture.md:17`（该句跨原文第 17–18 行）。
<!-- END: 06_providers.md -->

<!-- SOURCE: 07_boundaries.md | 12320 bytes -->
# 第 7 章 边界与安全

前面六章讲的都是 REA「能做什么」。这一章补上另一半：**能做什么，和你有权拿它做什么，是两回事**。REA 是一把能撬开软件的「手术刀」——刀没有立场，切病灶还是伤人，取决于握刀的手。本章把三件事讲清楚：官方列出的**合法用途白名单**、**明令不帮的用途**，以及 REA 内部那套安全机制到底防什么、**不防什么**。

## 一、先分清「能做什么」和「允许做什么」

REA 在 `DISCLAIMER.md` 里用一句话划出了它的适用范围：它只为**合法分析**而建。这不是客套话，而是一份「授权清单」——只有落在清单里的用途，它才提供帮助。

### 合法用途白名单

打个比方：进公司大楼要刷卡，卡能开哪扇门，你才能进哪扇门。「技术上打得开」不等于「有权打开」。REA 的白名单就是这张门禁清单：

| 官方原文 | 说人话 |
|---|---|
| “security research, malware and incident analysis, vulnerability research and coordinated disclosure, CTFs and education, interoperability, software preservation, and debugging or auditing software you own or are authorized to examine.” | 安全研究；恶意软件与事件分析；漏洞研究与协调披露；CTF 竞赛与教学；互操作性；软件保存；以及——调试或审计**你自己拥有、或获授权检查**的软件。 |

把这七项读一遍会发现一条共同线：**它们都要求你对目标有权限**——要么是你自己的软件，要么是获授权检查、或在合法框架内研究的目标。

> [!tip] 大白话
> 把「授权」想成小区门禁卡：刷卡开得了哪扇门，你才进得了哪扇。拿别人的卡、或撬门进去，即使技术上行得通，也不叫合法使用。REA 的白名单，就是先问你「这张卡是不是你的」。

### 明令不帮的用途

白名单之外，官方还**点名列出六类不帮**的用途。这些都是「技术上 REA 做得到，但项目明确不参与」的请求：

| 官方原文 | 说人话 |
|---|---|
| “circumventing DRM, license checks, anti-cheat systems or other technical protection measures” | 绕过 DRM、许可校验、反作弊系统等其它技术保护措施 |
| “developing game cheats or tampering with online services” | 做游戏外挂，或篡改在线服务 |
| “bypassing authentication, bot protection or access controls on systems you are not authorized to test” | 在你**未获授权测试**的系统上，绕过认证、机器人防护或访问控制 |
| “copying proprietary software or reproducing its protected code and assets” | 抄袭专有软件，或复现它受保护的代码与资产 |
| “evading the usage policies or safety measures of AI model providers” | 规避 AI 模型供应商的使用政策或安全措施 |
| “reselling or sharing AI accounts or API access” | 转售或共享 AI 账号、API 使用权 |

官方对这类请求的处理很直接：在 issue 与讨论区会被**不回复直接关闭**，严重时可能被移出社区。还有一点要特别记住——**REA 不提供任何商业工具（如 `IDA Pro`、`Hopper`）的许可、密钥或激活权益**。它只是复用你**已经合法装好**的工具，不会帮你搞到破解副本或盗来的密钥。

## 二、内部安全机制：一次性的「能力令牌」

划完「该不该做」，再来看 REA 自己是怎么护住这条边界的。第 6 章提过，REA 会通过 `Hopper`、`Ghidra` 桥去驱动本机的分析引擎。这些桥不能谁都能连，它们有一套认证机制。

一句话概括：**每个会话发一张随机的「能力令牌」，只对本次会话有效。** `POSIX` 系统上，双方走当前用户的 `Unix socket`；在 `Windows` 上，`Ghidra` 用带认证的回环 TCP，配一个只有当前用户和 SYSTEM 能访问的私有运行时目录。关键在**令牌怎么传**——官方明确说，令牌通过**私有会话描述符**传递，**不走进程参数，也不走环境变量**。

> [!tip] 大白话
> 把能力令牌想成一张「一次性工牌」：每次开工现发一张，只对这一次会话有效。而且它是从内部通道递过去的，不挂在脖子上（进程参数）、也不贴在大厅墙上（环境变量）——这两个地方别人一眼就能看到。

为什么强调「不走进程参数或环境变量」？因为进程参数和环境变量在同机、同用户下往往可读。改走私有会话描述符，等于把令牌藏进只有双方能看到的通道里。

## 三、必须记住的事实：它不是沙箱

上面这套机制听起来挺严密，但它有一个**极其重要的边界**，官方专门用一句话点破：**这不是沙箱，它不能防御「已经以同一操作系统用户身份运行」的恶意进程。**

换句话说，令牌机制防的是「外部程序冒充你去连 `Hopper`/`Ghidra` 桥」，防不了「本来就和你同一个用户、已经在跑的恶意进程」。REA 的 `Ghidra` 会话确实做了不少收敛：用隔离的临时工程、私有 home / cache / runtime 目录，限制启动与消息大小，会话结束就删掉临时工程。但官方对这些控制的定性同样清醒——它们**只减少意外持久化和资源占用，并不把 `Ghidra` 变成沙箱**。

> [!tip] 大白话
> 把「不是沙箱」想成合租房的门锁：它能挡住你随手走错房间，却挡不住**本来就有房门钥匙的室友**。同一个操作系统用户下的恶意进程，就属于「有钥匙的室友」，这套机制管不了它。

所以当你打开一个**来路不明的二进制**时，要明白：解析和分析被交给了本机分析引擎，而引擎是以**你当前用户的权限**在跑。对不可信的目标，官方建议放到合适的环境里处理。

## 四、数据去哪了：本地分析 ≠ 不上网

很多人会问：REA 会不会把我的 App 传走？官方 FAQ 的回答是：**REA 在本机分析目标**。但紧接着还有半句，同样重要：**你的 agent 会收到工具结果，而 agent 背后的模型供应商，有它自己的数据政策。**

> [!tip] 大白话
> 把「本地分析」想成在自己家厨房做菜——下锅、翻炒都在你家；但做好的菜（工具结果）会端给 agent 的「外卖平台」（模型供应商），那个平台的卫生标准，是它自己定的。

也就是说，「本地」只描述了**分析这一步**发生在你机器上，它**不是整条链路的隐私保证**。是否上传、怎么用，取决于你接入的 agent 和它背后的模型服务商。

## 五、呼应第 5 章：浏览器观测的边界

第 5 章讲网站观测时，我们先把边界划在了前面；这里再收一次口，因为它是本章「非沙箱」主题的同一根线：

- **被动**：它是一种**被动的逆向能力**，不是通用的浏览器自动化或远程控制面——它只「接上」你开好的浏览器做记录，不替你操作。
- **非沙箱**：它**不是浏览器沙箱，也不做网络隔离**；被接上的页面和浏览器，仍以原有权限继续运行，可以独立于 REA 向外部发请求。
- 因此官方建议：**用专用 `profile`，只纳入你打算检查的那些 `origin`**，并把同一用户下的其它进程视为这条边界之外。

## 本章小结

- REA 只为**合法分析**服务；白名单包括安全研究、恶意软件与事件分析、漏洞研究与协调披露、CTF 与教学、互操作性、软件保存，以及调试 / 审计你拥有或获授权检查的软件。
- 六类明确不帮的用途：绕过 DRM / 许可校验 / 反作弊、外挂与篡改在线服务、未授权绕过认证 / 机器人防护 / 访问控制、抄专有软件、规避 AI 供应商使用政策、转售 / 共享 AI 账号或 API。
- 安全机制是「每会话随机能力令牌」：`POSIX` 走当前用户 `Unix socket`，令牌经私有会话描述符传递，不走进程参数或环境变量。
- **它不是沙箱**：管不了已以同一操作系统用户身份运行的恶意进程；那些控制只减少意外持久化与资源占用。
- 「本地分析」只指分析这一步在本机完成；结果会交给 agent，其模型供应商有自己的数据政策。
- 浏览器观测同样是被动、非沙箱、非网络隔离的能力——与第 5 章口径一致。

## 下一章预告

到这里，全篇的概念、接入、实战和边界都讲完了。最后一章把散落各处的**名词、CLI 命令、输出格式与退出码**收进几张可回查的表里，让你以后不必翻正文，也能一眼找到那条命令。

## 引文对照（原文 / 中译 / 出处）

> 下表收录本章出现的全部英文引文，原文逐字保留。出处列取 `sources/文件名:行号`；「—」表示查不到来源、宁空不猜（本章所有条目均有明确出处，故未出现「—」）。

| 序号 | 原文 | 中译 | 出处 |
|---|---|---|---|
| 1 | “security research, malware and incident analysis, vulnerability research and coordinated disclosure, CTFs and education, interoperability, software preservation, and debugging or auditing software you own or are authorized to examine.” | 安全研究；恶意软件与事件分析；漏洞研究与协调披露；CTF 竞赛与教学；互操作性；软件保存；以及调试或审计你自己拥有、或获授权检查的软件。 | `sources/DISCLAIMER.md:5-8` |
| 2 | “circumventing DRM, license checks, anti-cheat systems or other technical protection measures” | 绕过 DRM、许可校验、反作弊系统等其它技术保护措施 | `sources/DISCLAIMER.md:12-13` |
| 3 | “developing game cheats or tampering with online services” | 做游戏外挂，或篡改在线服务 | `sources/DISCLAIMER.md:14` |
| 4 | “bypassing authentication, bot protection or access controls on systems you are not authorized to test” | 在你未获授权测试的系统上，绕过认证、机器人防护或访问控制 | `sources/DISCLAIMER.md:15-16` |
| 5 | “copying proprietary software or reproducing its protected code and assets” | 抄袭专有软件，或复现它受保护的代码与资产 | `sources/DISCLAIMER.md:17` |
| 6 | “evading the usage policies or safety measures of AI model providers” | 规避 AI 模型供应商的使用政策或安全措施 | `sources/DISCLAIMER.md:18` |
| 7 | “reselling or sharing AI accounts or API access” | 转售或共享 AI 账号、API 使用权 | `sources/DISCLAIMER.md:19` |
| 8 | “REA authenticates its Hopper and Ghidra bridges with per-session random capability tokens.” | REA 用每会话随机的能力令牌，对它自己的 Hopper 与 Ghidra 桥做认证。 | `sources/SECURITY.md:27-28` |
| 9 | “Tokens are transferred through private session descriptors rather than process arguments or environment variables.” | 令牌经由私有会话描述符传递，而不是通过进程参数或环境变量。 | `sources/SECURITY.md:31-32` |
| 10 | “This is not a sandbox and does not protect against malicious processes already running as the same operating-system user.” | 这不是沙箱，不能防御已经以同一操作系统用户身份运行的恶意进程。 | `sources/SECURITY.md:33-34` |
| 11 | “These controls limit accidental persistence and resource use; they do not make Ghidra a sandbox.” | 这些控制只限制意外的持久化与资源占用，并不把 Ghidra 变成沙箱。 | `sources/SECURITY.md:42-43` |
| 12 | “REA analyzes targets locally. Your agent receives the tool results, and its model provider has its own data policy.” | REA 在本机分析目标。你的 agent 会收到工具结果，而它背后的模型供应商有自己的数据政策。 | `sources/README.md:281-282` |
| 13 | “This is a passive reverse-engineering capability, not a general browser automation or remote-control surface.” | 这是一种被动的逆向能力，不是通用的浏览器自动化或远程控制面。 | `sources/docs_browser-observation.md:9` |
| 14 | “This feature is not a browser sandbox or network containment mechanism.” | 这个功能不是浏览器沙箱，也不做网络隔离。 | `sources/docs_browser-observation.md:229` |
<!-- END: 07_boundaries.md -->

<!-- SOURCE: 08_reference.md | 8860 bytes -->
# 第 8 章 小结与速查附录：名词表、CLI 速查、退出码

前七章从「REA 是什么」一路走到「边界与安全」，信息密度不低。这一章不讲新概念，只做一件事：把全篇用到的术语、命令、输出与退出码收成几张能随时回查的表。读到某个词想不起什么意思、跑命令忘了参数、看到退出码不确定是否成功，翻到这里即可。若要复习一遍主线，回到第 1 章的「一句话看懂」，再顺着第 3→4/5→6→7 章走。

> [!summary] 一句话看懂
> 这一章是**回查手册**，不是新内容：三张主表（名词、命令、退出码）＋两条口径（会话模型、生态分发）。术语与数字全部与前面各章一致。

## 8.1 名词扫盲表

书名对应的核心词都在下表。这里只保留一句话版本；要完整背景，按「详见」列回跳对应章节。

| 术语 | 一句话说明 | 详见 |
| --- | --- | --- |
| 逆向工程 | 没有源码，也把软件「拆开看清楚」它是怎么做的 | 第 1 章 |
| MCP | Model Context Protocol，让 AI agent 调用外部工具的一套标准插口 | 第 1 章 |
| 证据 / 局限 | REA 不只给结论，还给出「凭什么这么说」和「哪里说不准」 | 第 1 章 |
| 静态分析 | 只读文件、不运行程序 | 第 1 章 |
| 运行时捕获 | 真的把程序或浏览器跑起来，记录它的行为 | 第 1 章 |
| provider | 提供原生分析能力的后端引擎，如 Hopper / Ghidra / IDA | 第 6 章 |
| IPC | 进程间通信；在 Electron 里指 renderer 与 main 之间传消息的通道[^c8-1] | 第 4 章 |
| CDP | Chrome DevTools Protocol；REA 通过它连接你自己开的 Chrome 系浏览器观测页面[^c8-2] | 第 5 章 |
| TOON | REA 终端输出的默认格式；要把结果喂给 JSON 消费者时改用 `--json`[^c8-3] | 本章 8.3 |

另有几个只在个别章节出现的词（伪代码、汇编、WAT、CIL、WAL 等），已在对应章节就地解释，这里不重复收录。

## 8.2 CLI 命令速查表

不装全局时，把下表的 `rea <命令>` 换成 `npx -y rea-agents@latest <命令>` 即可[^c8-4]。

| 分类 | 命令 | 用途 / 备注 |
| --- | --- | --- |
| 静态 JS/Electron | `analyze-javascript-application PATH --json` | 静态分析 JS/Electron 应用；`PATH` 为目录或 `.asar` |
| 静态 JS/Electron | `inspect-analysis-view VIEW.json` | 把大证据投影成摘要／模块页，先落盘再投影 |
| 零引擎其他 | `inspect-managed-artifact` / `inspect-managed-members` | .NET 元数据与 CIL，不执行程序集 |
| 零引擎其他 | `inspect-sqlite-database PATH [--table N --row-limit 20]` | 读 SQLite 快照，无需原生引擎 |
| 零引擎其他 | `inspect-go-binary PATH` | 读 Go 构建元数据，无需安装 Go |
| 原生分析 | `analyze` | 原生二进制分析入口（需 provider） |
| 原生分析 | `search` | 在分析结果里检索 |
| 原生分析 | `function` | 定位／查看函数 |
| 原生分析 | `decompile` | 反编译出伪代码 |
| 原生分析 | `xrefs` | 查交叉引用 |
| 原生分析 | `trace --provider X` | 运行时追踪，用 `--provider` 指定引擎 |
| Provider / 诊断 | `providers --json` | 列出可用 provider |
| Provider / 诊断 | `capabilities --json` | 列出能力 |
| Provider / 诊断 | `doctor --provider ID --json` | 诊断指定引擎是否就绪 |
| 证据 | `evidence-import` | 校验／导入证据包 |
| 证据 | `evidence-export` | 导出证据包 |
| 证据 | `compare` | 对比证据（如构建前后） |
| 证据 | `import-reference-source PATH` | 导入历史源码用于对比（Linux/macOS） |
| 浏览器 | `list-browser-targets` | 列出可观测的浏览器页面 target |
| 浏览器 | `inspect-web-page` | 观测选定页面（被动、非自动化） |

命令取值一律来自官方 CLI 文档，未在此列出的命令以你连接的 server 实际工具列表为准（见 8.4）[^c8-5]。

**怎么用这张表**：想跑「零原生引擎」的目标，只用前两类——静态 JS/Electron 与「零引擎其他」；其中 .NET、SQLite、Go 三条都不需要 Hopper / Ghidra / IDA。等到要动原生二进制（伪代码、反编译、交叉引用）时，才需要装一个 provider，走「原生分析」一类，并先用 `doctor` 确认引擎就绪。浏览器一类是第 5 章的被动观测，只记录、不自动化、不远程控制。

## 8.3 输出格式与退出码

**输出格式**：默认终端格式是 **TOON**。要保存给 JSON 程序消费时加 `--json`——它在终端里是缩进的，被管道或重定向时变紧凑，从而让大结果对 agent 与脚本更小；需要缩进文件就再过一道 `jq .`。输出格式的选择**不改变操作状态**，成败只看退出码[^c8-3]。一句话概括：TOON 面向终端阅读，`--json` 面向程序消费，两者只是展示层不同，同一份结果的内容一致。

**退出码**（下表同属「Output and exit status」一节）[^c8-6]：

| 退出码 | 含义 |
| --- | --- |
| `0` | 操作完成。结果里可能仍含部分证据、警告或未决问题 |
| `1` | 操作未能完成。有结构化输出时会指出无效输入、权限、取消、超时或其它失败 |
| `128 + N` | 进程被信号 `N` 终止（shell 或运行时保留这一约定状态） |

几个容易记混的边界情形：

- `setup --dry-run` 返回 `planned` 并**退出 `0`**；**取消 setup 也退出 `0`**。
- `setup` 在 `needs_confirmation` 或 `needs_human` 时返回 `1`。
- `doctor` 在所选就绪范围内必需检查失败时返回 `1`；无关任务下不可用的可选 provider 只是信息提示。
- 若在下游接了格式化命令，记得开启 shell 的 `pipefail`——默认情况下「管道前段失败、后段成功」会被算作整条成功，开了它才能让上游的失败状态传下来[^c8-6]。

关于两条容易误读的语义：`0` 的含义是「操作完成了」，**不等于**「一切干净」——结果里可能仍带着部分证据、警告或未决问题，要读内容自己判断；反过来 `1` 是「没能完成」，REA 会尽量在结构化输出里说明原因（无效输入、权限、取消、超时等）。

## 8.4 会话模型：以运行时工具列表为准

REA 有一份构建期生成的机器可读目录（`docs/public/product-catalog.json`），但**它不是权威**——它描述的是被构建的那次源码修订，并非签入的快照。对正在运行的 server，`binary_session` 才是目录标识与工具可用性的权威来源。所以：**工具／命令全集以你 connected server 的实际工具列表为准，而非某一版文档或目录文件**[^c8-7]。为什么以运行时为准——那份构建期目录会随源码修订变化，而文档快照又可能落后于你实际装的版本；只有正在运行的 server 自报的工具列表，才反映你此刻真正能调用的能力。本节 8.2 的表是稳定入口，完整清单请以连接后的实际列表核对。

## 8.5 生态补充：注册表装的是同一个包

REA 在官方 MCP Registry 上的名字是 `io.github.morluto/rea`。注册表客户端能发现这个 server 并安装**已有的公开 npm 包 `rea-agents`**——注册表条目**不引入第二分发物**；它发布的元数据仍是用 `npx` 拉起同一个 stdio server 的 `mcp` 命令[^c8-8]。换句话说：无论走 npm 直装还是走注册表发现，落到机器上的都是同一个 `rea-agents` 包——你不必在两者之间做「装哪个」的选择，它们最终指向同一套包与工具。这样你无论从哪种客户端出发，本手册里出现的包名、命令与退出码都是同一套。

## 小结

- **名词**：逆向工程 / MCP / 证据与局限 / 静态分析 / 运行时捕获 / provider / IPC / CDP / TOON，见 8.1。
- **命令**：静态 JS/Electron、零引擎其他、原生分析、provider 诊断、证据、浏览器六类，共 20 条，见 8.2。
- **输出**：默认 TOON；`--json` 终端缩进、管道紧凑；退出码 `0` 完成 / `1` 未完成 / `128+N` 被信号终止；`setup --dry-run` 与取消 setup 都退 `0`。
- **口径**：工具全集以 **connected server 实际列表**为准；注册表装的是同一个 npm 包，无第二分发物。

全书到这里结束。想动手时，从第 3 章的 `setup` 起步，再跑第 4 章（静态 JS/Electron）与第 5 章（浏览器观测）两条实战；遇到原生目标或平台限制，回查第 6 章与本章速查表。

---

[^c8-1]: `sources/README.md:162`
[^c8-2]: `sources/docs_browser-observation.md:9`
[^c8-3]: `sources/docs_cli.md:256`
[^c8-4]: `sources/docs_cli.md:9`
[^c8-5]: `sources/docs_cli.md:103`
[^c8-6]: `sources/docs_cli.md:254`
[^c8-7]: `sources/docs_mcp-contracts.md:681`
[^c8-8]: `sources/docs_installation.md:784`
<!-- END: 08_reference.md -->
