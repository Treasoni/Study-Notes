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
