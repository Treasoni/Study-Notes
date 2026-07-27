# Node.js 基础概念零基础入门

---

## 目录

1. **第一章：Node.js 初识 —— 它到底是什么**
   - 1.1 一句话定义
   - 1.2 为什么需要 Node.js？—— 一个简短的历史背景
   - 1.3 Node.js 的三大支柱
   - 1.4 Node.js vs 浏览器 JavaScript：有什么区别？
   - 1.5 npm：全球最大的"代码超市"
   - 1.6 Node.js 能做什么？
   - 本章小结
   - 下一章预告

2. **第二章：环境搭建与第一个 Node.js 程序**
   - 2.1 选择 Node.js 版本：LTS 还是 Current？
   - 2.2 安装 Node.js
   - 2.3 验证安装
   - 2.4 创建你的第一个 Node.js 项目
   - 2.5 理解 package.json
   - 2.6 编写并运行 Hello World
   - 2.7 node 命令的基本用法
   - 本章小结
   - 下一章预告

3. **第三章：模块系统 —— CommonJS 与 ESM**
   - 3.1 为什么需要模块化？
   - 3.2 CommonJS —— Node.js 的传统模块系统
   - 3.3 ESM —— 现代 JavaScript 模块系统
   - 3.4 如何在项目中选择：CommonJS vs ESM
   - 3.5 两种模块的互操作
   - 3.6 node: 前缀与推荐实践
   - 本章小结
   - 下一章预告

4. **第四章：异步编程 —— 从回调到 async/await**
   - 4.1 同步 vs 异步 —— 先搞懂"等"和"不等"
   - 4.2 回调函数 —— Node.js 最早的异步方案
   - 4.3 Promise —— 更优雅的异步方案
   - 4.4 Promise 并行方法
   - 4.5 async/await —— 异步编程的终极形态
   - 4.6 并发控制
   - 4.7 常见异步陷阱
   - 本章小结
   - 下一章预告

5. **第五章：核心 API（一）—— 文件与路径操作**
   - 5.1 path 模块 —— 路径的正确打开方式
   - 5.2 __dirname vs import.meta.url
   - 5.3 fs 模块 —— 操作文件系统的三套 API
   - 5.4 目录操作 —— 创建、读取、删除
   - 5.5 文件信息查询（stat）
   - 5.6 综合实战 —— 日志工具
   - 5.7 大文件处理思路 —— Stream 的概念引入
   - 本章小结
   - 下一章预告

6. **第六章：事件循环 —— 理解 Node.js 异步的核心**
   - 6.1 为什么需要事件循环
   - 6.2 事件循环的六大阶段
   - 6.3 微任务与 nextTick
   - 6.4 setTimeout(0) vs setImmediate 对比实验
   - 6.5 线程池：谁在背后搬砖
   - 6.6 阻塞事件循环的危害
   - 本章小结
   - 下一章预告

7. **第七章：网络编程与 Express 框架入门**
   - 7.1 从 http 模块开始：你的第一个 Web 服务器
   - 7.2 自己处理路由：体会"手动"的痛苦
   - 7.3 Express 登场：3 行代码替代手写路由
   - 7.4 路由详解：GET、POST 与参数
   - 7.5 中间件：流水线上的工位
   - 7.6 常用中间件
   - 7.7 错误处理
   - 7.8 项目分层结构建议
   - 7.9 输入验证：别相信用户发来的数据
   - 本章小结
   - 下一章预告

8. **第八章：环境配置、调试与最佳实践 —— 从"能跑"到"专业"**
   - 8.1 开发效率工具 —— 告别手动重启
   - 8.2 环境变量管理 —— 不要把密码写在代码里
   - 8.3 npm 常用命令速查表
   - 8.4 新手最容易踩的坑
   - 8.5 错误处理分类 —— 两种完全不同的错误
   - 8.6 结构化日志入门 —— 告别 console.log
   - 8.7 安全基础配置 —— 给应用穿上盔甲
   - 8.8 性能注意事项
   - 8.9 本章小结
   - 下一章预告

9. **第九章：项目实战与学习路径**
   - 9.1 项目实战总览
   - 9.2 实战一：文件批量重命名 CLI 工具
   - 9.3 实战二：简易 HTTP 服务器多路由
   - 9.4 实战三：便签 REST API
   - 9.5 学习路径总览
   - 9.6 推荐学习资源
   - 9.7 进阶方向
   - 结语

---

# 第一章：Node.js 初识 —— 它到底是什么

你大概已经听说过 Node.js 这个词，可能知道它和 JavaScript 有关，但又不太清楚它究竟做什么用。这很正常 —— 很多人学了几个月 JavaScript 后，突然发现 JavaScript 还能在"浏览器外面"跑，这个转折本身就很容易让人困惑。

本章的目标很简单：用最直白的方式说清楚 Node.js 是什么、它由哪些部分组成、它能做什么、以及它和你已经知道的浏览器 JavaScript 有什么不同。读完这一章，你不会写任何 Node.js 代码，但你会对它的全貌有一个清晰的认识。

---

## 1.1 一句话定义

**Node.js 是一个让你用 JavaScript 编写服务端程序的运行时环境。**

拆开来看这句话的三个关键词：

- **JavaScript**：你写的还是 JavaScript 代码 —— 语法、变量、函数、Promise，全都一样。
- **服务端程序**：代码跑在服务器上，而不是浏览器里。这意味着你可以用它读写文件、处理网络请求、操作数据库。
- **运行时环境**：JavaScript 本身只是一门语言，它需要一个"环境"来解释执行。浏览器就是一个运行时环境，Node.js 是另一个。

> [!note] 类比理解
> 想象 JavaScript 是一个会说"中文"的演员。浏览器就像一个剧场，演员只能在剧场里表演。Node.js 就像把同一个演员请出来，让他也能在电影院、录音棚、街头等各种场地表演。语言没变，但舞台完全不同了。

---

## 1.2 为什么需要 Node.js？—— 一个简短的历史背景

1995 年，JavaScript 诞生，被设计为"在浏览器里让网页动起来"的脚本语言。此后的二十年里，它的活动范围几乎被锁定在浏览器这个围城里。

如果你想让服务器处理一个 HTTP 请求，当时的做法是用其他语言 —— PHP、Java、Python、Ruby。前端工程师和后端工程师说的是两套完全不同的技术栈。

转折点出现在 2009 年。一位叫 **Ryan Dahl** 的开发者做了一个决定：**把 Google Chrome 浏览器的 JavaScript 引擎（V8）从浏览器里"挖"出来，让它能在服务器上运行**。这就是 Node.js 的起点。

它的意义在于：**前端工程师终于可以用同一门语言写前端和后端了。**

这种"全栈用 JavaScript"的可能性，迅速改变了 Web 开发的格局。到今天，Node.js 已经成为服务器端开发的主流选择之一，被 Netflix、Uber、PayPal、LinkedIn 等公司广泛使用。

---

## 1.3 Node.js 的三大支柱

Node.js 不是一个简单的程序，它是由三个核心组件组合而成的。理解这三者的分工，就理解了 Node.js 的底层逻辑。

### V8 引擎 —— JavaScript 的翻译官

JavaScript 是人类可读的代码，但计算机只认识机器码。V8 引擎的任务就是：**把 JavaScript 代码翻译成计算机能执行的机器指令**。

V8 是由 Google 开发的开源 JavaScript 引擎，原本是 Chrome 浏览器的心脏。它有两个显著特点：

- **快**：V8 会把 JavaScript 编译成高效的机器码，而不是逐行解释执行。这就是为什么 Chrome 比早期浏览器快很多的原因之一。
- **标准兼容**：V8 严格遵循 ECMAScript 标准，这意味着你写的 JavaScript 在 Chrome 和 Node.js 中行为一致。

> [!tip] 你不需要深入理解 V8 的内部机制
> 对初学者来说，你只需要记住：**Node.js 自己不执行 JavaScript，它把代码交给 V8 去执行**。V8 是那个真正"干活"的引擎。

### libuv —— 幕后英雄

这可能是整本笔记中最容易被忽略但最重要的组件。

JavaScript 在设计上是**单线程**的 —— 一次只能做一件事。但服务器经常需要同时处理很多事情：读取文件的同时响应另一个用户的请求，查询数据库的同时处理第三个请求的数据。

libuv 是一个用 C 语言编写的库，它解决了这个问题。它的核心能力是：

- **事件循环（Event Loop）**：一个不停转动的"调度轮盘"，负责决定什么时候执行什么任务。
- **线程池（Thread Pool）**：默认 4 个线程，专门处理文件读写、密码哈希等"重活"。JavaScript 主线程把脏活累活交给 libuv，自己继续处理新来的请求。

> [!note] 理解"单线程"的真正含义
> 经常有人说"Node.js 是单线程的"。这句话不完全准确。更准确的说法是：**执行你写的 JavaScript 代码的是单线程，但底层 I/O（输入/输出）操作由 libuv 用线程池和操作系统的异步能力扛着**。这意味着你用 Node.js 写网络服务时，虽然只用了一根"主线程"，但它背后有一整个后勤团队在帮忙。

### 核心绑定层 —— 搭桥者

V8 只懂 JavaScript，libuv 只懂 C 语言。为了让 JavaScript 代码能调用 libuv 的功能（比如读写文件），需要一层"胶水"代码来搭桥。这就是 Node.js 的核心绑定层（Core Binding Layer）。

当你写下 `const data = await fs.readFile('file.txt')` 时，Node.js 内部的实际流程是：

```
你的 JavaScript 代码
    ↓
Node.js JS API（fs 模块）
    ↓
核心绑定层（C++/JS 桥接）
    ↓
libuv（C 语言，执行实际文件读取）
    ↓
操作系统（真正读写磁盘）
```

你完全不需要记住这个流程，但要知道：**你在 JavaScript 中调用的每一个 API，底层都可能经过多层翻译才最终执行**。

---

## 1.4 Node.js vs 浏览器 JavaScript：有什么区别？

这是初学者最容易混淆的问题。你已经知道 JavaScript 可以在浏览器里跑，也可以在 Node.js 里跑 —— 那么它们到底有什么不同？

下面这张表格可以帮你快速建立对比：

| 对比维度 | 浏览器中的 JavaScript | Node.js 中的 JavaScript |
|----------|---------------------|------------------------|
| **运行目的** | 操作网页 DOM、响应用户交互 | 处理服务器任务（文件、网络、数据库） |
| **全局对象** | `window`、`document` | `global`、`process` |
| **可访问 API** | DOM API（`getElementById`、`fetch` 等） | 系统 API（`fs` 文件系统、`http` 网络模块、`path` 路径处理等） |
| **模块系统** | 通过 `<script>` 标签或 import 加载 | CommonJS（`require`）或 ESM（`import`） |
| **包管理** | CDN 加载第三方库 | **npm**（全球最大的包管理器） |
| **运行环境** | 用户电脑上的浏览器 | 服务器上安装的 Node.js 运行时 |
| **能做什么** | 控制网页行为、发送网络请求 | 构建 Web 服务器、CLI 工具、桌面应用后台 |

> [!warning] 不在浏览器里，就没有 DOM！
> 很多初学者刚开始用 Node.js 时会下意识想用 `document.getElementById()` —— 但 Node.js 里没有 `document` 对象。浏览器中的 DOM API、`window` 对象、CSS 相关的操作，在 Node.js 中通通不存在。反之，浏览器中不能直接读写文件系统，而 Node.js 可以。

**它们共享的核心部分**：

尽管 API 不同，但 JavaScript 语言的**核心语法完全一致**：

- 变量声明（`let`、`const`、`var`）
- 函数与箭头函数
- 对象、数组、Map、Set
- Promise 与 async/await
- 类与继承
- 模板字符串、解构赋值等 ES6+ 特性

> [!tip] 先打好 JavaScript 基础再学 Node.js
> 这是几乎所有 Node.js 学习路线中反复强调的第一条建议。如果你对 Promise 和 async/await 还不熟悉，建议先去巩固一下 JavaScript 异步基础。Node.js 是一个重度异步的平台，异步编程的理解程度直接决定你能否顺畅地使用它。

---

## 1.5 npm：全球最大的"代码超市"

npm（Node Package Manager）是 Node.js 自带的包管理器，它在 2009 年随 Node.js 一同诞生。**它不是 Node.js 的语言特性，而是它的生态核心。**

可以这样理解 npm：

- 你写程序时经常需要别人已经写好的功能模块 —— 比如处理日期、解析 Excel、发送邮件。
- npm 就是全世界最大的"代码超市"，里面有超过 200 万个这样的现成模块（称为"包"，package）。
- 你只需要一个命令 `npm install <包名>`，就能把需要的模块下载到你的项目里，直接使用。

```bash
npm install lodash
npm install express
npm install axios
```

> [!note] 一句话理解 npm
> 没有 npm 的话，你想用别人写的代码就得手动复制粘贴。有了 npm，只需要一行命令就能下载、更新和管理所有依赖。它相当于 JavaScript 世界的 App Store。

npm 的详细使用方法会在第二章中讲解，这里你只需要知道它是什么就够了。

---

## 1.6 Node.js 能做什么？

Node.js 的应用场景非常广泛。以下是最常见的几类：

### 构建 Web API 和 RESTful 服务（最主流）

Node.js 最常见的用途就是写后端 API。你可以用几行代码就启动一个 HTTP 服务器，处理来自前端或移动端的请求。

典型案例：Netflix 用 Node.js 处理用户界面和数据聚合层；Uber 用 Node.js 构建其核心的行程调度服务。

### 实时应用

Node.js 的事件驱动特性非常适合处理实时通信场景 —— 聊天应用、在线协作工具、实时数据看板。

典型案例：Slack 的桌面端基于 Node.js 构建；Trello 的卡片实时同步功能依赖 Node.js。

### CLI 工具（命令行工具）

Node.js 可以用来写各种命令行工具。实际上，很多你可能已经在用的工具（Webpack、Gulp、ESLint、Prettier）都是基于 Node.js 构建的。

### 后端服务与中间层

很多公司把 Node.js 当作"胶水层" —— 前端请求先到达 Node.js 服务，它再把请求转发给后端的其他服务（Java 或 Go 写的业务服务），起到聚合和转发的角色。

典型案例：PayPal 和 LinkedIn 都从原先的后端语言迁移到 Node.js 作为其中间层。

### 不适合的场景

Node.js 并非万能。以下场景不太适合用 Node.js：

| 不适合的场景 | 原因 |
|-------------|------|
| CPU 密集型计算（视频编码、图像处理、大规模数据分析） | 单线程模型在密集计算时会阻塞事件循环 |
| 对延迟极其敏感的实时系统 | JavaScript 的动态类型和 GC（垃圾回收）暂停可能导致不可预测的延迟 |
| 需要精细控制内存和性能的底层系统 | Node.js 隐藏了底层细节，不提供细粒度的内存管理 |

> [!tip] 对初学者而言，先专注于 Web API 开发
> 你最应该关注的是 Node.js 最主流、最适合的场景：**构建 Web 服务**。掌握这个核心场景后，再根据实际需要探索 CLI 工具、实时应用等其他方向。

---

## 本章小结

- **Node.js 是一个让你用 JavaScript 编写服务端程序的运行时环境**，它把 JavaScript 从浏览器中解放了出来。
- Node.js 由三大组件构成：**V8 引擎**（执行 JavaScript 代码）、**libuv**（处理异步 I/O 操作）、**核心绑定层**（搭桥连接 JS 和 C++）。
- Node.js 中的 JavaScript **没有 DOM API**，但拥有文件系统、网络模块等服务器端 API。两者共享同一套核心语法。
- **npm** 是 Node.js 自带的包管理器，提供超过 200 万个现成的代码模块，让开发者不必重复造轮子。
- Node.js 最主流的应用场景是**构建 Web API 和 RESTful 服务**，但不适合 CPU 密集型计算。

---

## 下一章预告

你已经知道了 Node.js "是什么"，现在我们来把它装到你的电脑上。下一章将带你完成 Node.js 和 npm 的安装，并写出你的第一个 Hello World 程序。


---

通过第一章的铺垫，你对 Node.js 的全貌有了清晰的认知。现在，让我们把 Node.js 装到你的电脑上，写第一行真正的代码。

# 第二章：环境搭建与第一个 Node.js 程序

第一章让你知道了 Node.js 是什么、它由哪些部分组成、它能做什么。但光知道概念还不够 —— 要真正开始学 Node.js，第一步永远是"把它装到你的电脑上"。很多新手卡在安装这一步，要么装错了版本，要么装了却不知道如何验证。这一章的目标很明确：让你在 30 分钟内完成安装、创建一个项目、并成功运行你的第一行 Node.js 代码。

---

## 2.1 选择 Node.js 版本：LTS 还是 Current？

打开 Node.js 官网（https://nodejs.org），你会看到两个下载按钮：

- **LTS（长期支持版）**：推荐绝大多数用户使用。LTS 版本会获得 3 年的安全更新和错误修复，稳定性有保障。
- **Current（当前最新版）**：包含最新的语言特性，但可能不够稳定，不适合生产环境。

> [!tip] 初学者选 LTS
> 对于零基础入门，**永远选择 LTS 版本**。截至 2026 年 7 月，Node.js 22.x 是当前的 LTS 活跃版本。你不需要追求最新，稳定才是开发环境的第一原则。[Scrimba 学习指南](https://scrimba.com/articles/how-to-learn-nodejs/)

---

## 2.2 安装 Node.js

### macOS 安装

**方法一：官网安装包（推荐初学者）**

1. 打开 https://nodejs.org
2. 页面会自动识别你的操作系统。点击左侧的 **LTS** 按钮（写着 "Recommended For Most Users"），下载 `.pkg` 安装包。
3. 双击下载的 `.pkg` 文件，按照安装向导一路点击"继续"和"安装"即可。安装过程中可能需要输入你的电脑密码。
4. 安装完成后，打开**终端**（Terminal）应用。你可以在"启动台" > "其他"中找到它，或按 `Cmd + 空格` 搜索 "Terminal"。

**方法二：Homebrew（适合有编程经验的 Mac 用户）**

如果你已经安装了 Homebrew（一个 macOS 上的包管理器），可以更直接：

```bash
# 安装 Node.js LTS 版本
brew install node@22

# 将 Node.js 加入系统路径
brew link --overwrite node@22
```

### Windows 安装

1. 打开 https://nodejs.org
2. 点击左侧的 **LTS** 按钮，下载 `.msi` 安装包。
3. 双击 `.msi` 文件，安装向导启动后，一路点击 "Next"。**重要：在安装向导中，确保 "Add to PATH" 选项是勾选状态**（默认已勾选）。
4. 安装完成后，打开**命令提示符**（Command Prompt）或 **PowerShell**。你可以按 `Win + R`，输入 `cmd` 然后回车。

> [!warning] Windows 用户：不要勾错选项
> 安装时如果取消了 "Add to PATH" 选项，安装完成后在终端里输入 `node` 命令会提示"不是内部或外部命令"。如果遇到这种情况，最简单的办法是重新运行安装包，重新勾选该选项。

---

## 2.3 验证安装

打开终端（macOS）或命令提示符/PowerShell（Windows），输入以下两条命令：

```bash
node -v
```

你应该看到类似这样的输出：

```
v22.x.x
```

然后输入：

```bash
npm -v
```

输出类似：

```
10.x.x
```

> [!note] 这里发生了什么？
> - `node -v`：`node` 是 Node.js 运行时的命令，`-v` 是 `--version` 的缩写，让程序打印当前版本号。
> - `npm -v`：同理，检查 npm 包管理器是否安装成功。

**如果看到版本号**：恭喜！Node.js 和 npm 已经成功安装，可以进入下一节。

**如果提示 "command not found" 或 "不是内部或外部命令"**：
- macOS：检查是否完成了安装向导的全部步骤。如果是从官网安装的，尝试重启终端。
- Windows：最常见的原因是安装时未勾选 "Add to PATH"。解决办法：重新运行安装包，在安装向导中确保该选项已勾选，或手动将 Node.js 的安装目录（通常是 `C:\Program Files\nodejs\`）添加到系统环境变量中。

---

## 2.4 创建你的第一个 Node.js 项目

安装完成后，我们来创建一个项目目录并初始化它。

### 创建项目文件夹

在终端中执行以下命令：

```bash
# 创建一个项目目录（名字可以自己取）
mkdir my-first-node-app

# 进入这个目录
cd my-first-node-app

# 确认当前目录位置
pwd            # macOS
# 或
cd              # Windows 下用 cd 命令查看当前路径
```

### 初始化项目

```bash
npm init -y
```

你会看到类似这样的输出：

```
Wrote to /Users/你的用户名/my-first-node-app/package.json:

{
  "name": "my-first-node-app",
  "version": "1.0.0",
  "main": "index.js",
  "scripts": {
    "test": "echo \"Error: no test specified\" && exit 1"
  },
  "keywords": [],
  "author": "",
  "license": "ISC"
}
```

> [!note] `npm init -y` 是什么意思？
> `npm init` 是 npm 的初始化命令，它会引导你创建一个 `package.json` 文件。加上 `-y` 参数（`--yes` 的缩写）表示"全部使用默认值"，跳过交互式问答，直接生成文件。如果你不加 `-y`，npm 会逐个问你项目名称、版本、描述等信息。

---

## 2.5 理解 package.json

`package.json` 是 Node.js 项目中**最重要的配置文件**。它就像是项目的"身份证"加"说明书"。让我们看看刚才生成的文件中每个字段的含义：

```json
{
  "name": "my-first-node-app",   // 项目名称，安装依赖时用到
  "version": "1.0.0",            // 项目版本号，遵循语义化版本（主版本.次版本.补丁）
  "main": "index.js",            // 项目的入口文件
  "scripts": {                   // 可执行的命令脚本
    "test": "echo \"Error: no test specified\" && exit 1"
  },
  "keywords": [],                // 搜索关键词（发布到 npm 时有用）
  "author": "",                  // 作者信息
  "license": "ISC"               // 开源许可证
}
```

下面重点解释几个你马上就会用到的字段：

### name
项目的名字。如果你将来要把这个项目发布到 npm，这个名字必须是唯一的（不能和别人已发布的包重名）。

### version
遵循"语义化版本"规范：`主版本.次版本.补丁号`。例如 `1.0.0` 表示第一个大版本。

| 版本变动 | 含义 | 示例 |
|---------|------|------|
| 补丁号 +1 | 修复了 bug，不改变已有功能 | 1.0.0 → 1.0.1 |
| 次版本号 +1 | 增加了新功能，但向后兼容 | 1.0.0 → 1.1.0 |
| 主版本号 +1 | 做了不兼容的修改 | 1.0.0 → 2.0.0 |

### main
指明项目的入口文件。当你用 `require('my-first-node-app')` 导入这个项目时，Node.js 会加载 `main` 指向的文件。对于初学者来说，把主文件命名为 `index.js` 是最常见的选择。

### scripts
这是一个非常重要的字段。你可以在 `scripts` 中定义常用命令的快捷方式：

```json
{
  "scripts": {
    "start": "node index.js",
    "dev": "node --watch index.js"
  }
}
```

定义之后，你就可以用 `npm run start` 或 `npm run dev` 来执行这些命令，而不必每次都手动输入完整的 `node index.js`。

> [!tip] 一个常用的 scripts 初始配置
> 建议你把 `package.json` 中的 `scripts` 字段改成这样：
> ```json
> "scripts": {
>   "start": "node index.js",
>   "dev": "node --watch index.js"
> }
> ```
> 这样后续运行代码只需 `npm run start`（生产环境）或 `npm run dev`（开发模式，文件变化自动重启）。

### dependencies 与 devDependencies

这两个字段在安装第三方包时才会出现，用来记录项目的依赖：

```json
{
  "dependencies": {           // 生产环境依赖
    "express": "^4.18.0"
  },
  "devDependencies": {        // 开发环境依赖（仅开发时使用）
    "nodemon": "^3.0.0"
  }
}
```

- `dependencies`：项目运行时必须的包（比如 Express、Axios）
- `devDependencies`：仅在开发时需要的包（比如测试工具、代码格式化工具）

通过 `npm install <包名>` 安装的包会进入 `dependencies`，而 `npm install -D <包名>`（`-D` 是 `--save-dev` 的缩写）会进入 `devDependencies`。

---

## 2.6 编写并运行 Hello World

现在我们来写真正运行的第一行 Node.js 代码。

### 创建 index.js

在 `my-first-node-app` 目录下，创建一个新文件并命名为 `index.js`。你可以用任何文本编辑器（记事本、VS Code、Sublime Text 等），写入以下内容：

```javascript
// 第一个 Node.js 程序：向控制台输出文字
console.log('Hello, Node.js!');
```

保存文件后，回到终端，确保当前目录在 `my-first-node-app`，然后运行：

```bash
node index.js
```

你应该看到输出：

```
Hello, Node.js!
```

> [!note] 发生了什么？
> `node index.js` 命令让 Node.js 运行时读取并执行 `index.js` 文件。`console.log()` 是 JavaScript 的标准输出方法 —— 和在浏览器中一样，它会将内容打印到终端控制台。区别在于：浏览器中的 `console.log` 打印在开发者工具的控制台面板里，而 Node.js 中的 `console.log` 打印在你正在操作的终端窗口里。

### 进阶：传递参数

Node.js 允许你在运行脚本时传递参数，脚本内部通过 `process.argv` 获取：

修改 `index.js`：

```javascript
// 获取命令行参数（前两个是固定参数：node 路径和脚本路径）
const args = process.argv.slice(2);
console.log('Hello,', args[0] || 'Node.js', '!');
```

在终端中运行：

```bash
node index.js 世界
```

输出：

```
Hello, 世界 !
```

> [!tip] 理解 process.argv
> `process.argv` 是一个数组，包含启动 Node.js 进程时的所有命令行参数。它的前两个元素是：
> - `process.argv[0]`：Node.js 可执行文件的路径
> - `process.argv[1]`：正在执行的脚本文件路径
> - 从 `process.argv[2]` 开始才是你真正传入的参数
>
> 所以我们用 `slice(2)` 来截取有效参数。

### 进阶：创建一个最简单的 HTTP 服务器（预览）

虽然这超出了 Hello World 的范围，但感受一下 Node.js 一个经典用途 —— 启动 Web 服务器 —— 只需要这几行代码：

```javascript
// 引入 Node.js 内置的 http 模块
const http = require('http');

// 创建一个服务器：收到请求就返回 "Hello World"
const server = http.createServer((req, res) => {
  res.end('Hello, Node.js!');
});

// 启动服务器，监听 3000 端口
server.listen(3000, () => {
  console.log('服务器已启动：http://localhost:3000');
});
```

保存后用 `node index.js` 运行，然后在浏览器中打开 `http://localhost:3000`，你会看到页面上显示 "Hello, Node.js!"。

按 `Ctrl + C`（macOS 和 Windows 通用）可以停止这个服务器。

> [!warning] 为什么现在看这个？
> 这里只是让你先感受一下几行代码就能启动一个 Web 服务器的体验。**不需要理解每一行的含义**。第七章会详细讲解 `http` 模块和 Express 框架。

---

## 2.7 node 命令的基本用法

`node` 命令是你和 Node.js 运行时交互的主要方式。以下是几个最常用的用法：

### 直接运行 JS 文件

这是最常见的用法：

```bash
node 文件名.js
```

### REPL 交互模式

不指定文件，直接输入 `node` 再回车，你会进入一个交互式编程环境（REPL，Read-Eval-Print Loop）：

```bash
node
```

终端光标会变成 `>`，你可以直接输入 JavaScript 代码并立即看到结果：

```
> console.log('Hello')
Hello
undefined
> 1 + 2
3
> const name = 'Node.js'
undefined
> `Hello, ${name}`
'Hello, Node.js'
```

按两次 `Ctrl + C` 或输入 `.exit` 可以退出 REPL 模式。

> [!tip] REPL 模式有什么用？
> REPL 非常适合用来**快速验证一段 JavaScript 代码的行为**，而不需要创建文件。比如你忘了 `Array.flat()` 的行为，直接在终端输入 `node` 然后测试几行代码，很方便。

### 使用 --watch 自动重启（Node.js 18+）

Node.js 18 及以上版本内置了文件监听功能。修改代码后，Node.js 会自动重启进程，不需要你手动按 `Ctrl + C` 再重新运行：

```bash
node --watch index.js
```

试试修改 `index.js` 中的文字，保存后观察终端 —— 你会看到类似这样的输出：

```
Restarting 'index.js'
Hello, Modified Node.js!
```

> [!note] 这就是前面 package.json 中 `"dev": "node --watch index.js"` 的作用
> 在 `scripts` 中配置好后，你只需要运行 `npm run dev`，效果完全等同于 `node --watch index.js`。

### 使用 -e 直接执行代码（不创建文件）

如果你想执行一行简单的代码但不想创建文件，可以用 `-e` 参数：

```bash
node -e "console.log('Hello from -e')"
```

这会直接输出 `Hello from -e`。适合偶尔的快速测试。

### npm 常用命令速查

| 命令 | 用途 | 示例 |
|------|------|------|
| `npm init -y` | 快速初始化项目，生成 package.json | `npm init -y` |
| `npm install <包名>` | 安装包并记录到 dependencies | `npm install express` |
| `npm install -D <包名>` | 安装开发依赖 | `npm install -D nodemon` |
| `npm uninstall <包名>` | 卸载包 | `npm uninstall express` |
| `npm run <脚本名>` | 运行 scripts 中的命令 | `npm run start` |
| `npm ls` | 列出已安装的依赖 | `npm ls` |
| `npm ci` | 根据 lockfile 精确安装（CI 环境推荐） | `npm ci` |

> **来源**：腾讯云入门教程、Scrimba 学习指南

---

## 本章小结

- **安装 Node.js 应选择 LTS 版本**（目前是 22.x），而非 Current 版本。官网下载安装包是最简单的方式，macOS 和 Windows 都有对应的安装程序。
- 安装后用 `node -v` 和 `npm -v` **验证安装是否成功**。能输出版本号就说明一切就绪。
- **`npm init -y` 可以快速生成 `package.json`**，这是 Node.js 项目的配置核心，包含 name、version、main、scripts、dependencies 等关键字段。
- **`node index.js` 是运行 JS 文件的标准方式**；`node --watch index.js` 可以监听文件变化自动重启。
- npm 的 `scripts` 字段很实用 —— 把常用命令定义为脚本后，只需 `npm run <脚本名>` 即可执行，不必每次手动输入完整命令。

---

## 下一章预告

环境已经搭好，第一个程序也已跑通。接下来要回答一个核心问题：当你用 `const fs = require('fs')` 导入一个模块时，Node.js 背后究竟做了什么？第三章将深入 Node.js 的模块系统，揭开 `require` 和 `import` 的秘密。


---

环境搭建好了，你的第一个 Node.js 程序也跑起来了。但你可能会好奇：`require` 究竟是怎么工作的？为什么有的文件用 `require`、有的用 `import`？下一章我们来解答这个问题。

# 第三章：模块系统 —— CommonJS 与 ESM

当你开始写稍微复杂一点的程序时，很快会遇到一个问题：所有代码都塞在一个文件里，很快就变得混乱不堪。变量命名冲突、代码难以复用、想找某段逻辑要在几百行里上下翻找。模块系统就是为了解决这些问题而生的。

Node.js 历史上存在过两套模块系统：一套叫 **CommonJS**，它是 Node.js 自诞生之初就自带的"原生"模块系统；另一套叫 **ESM（ES Modules）**，它是 JavaScript 语言标准本身定义的模块系统，从 Node.js 12 开始稳定支持。**2026 年的推荐实践是新项目使用 ESM**，但理解 CommonJS 仍然很重要 —— 你会遇到大量现存的代码和教程用的是它。

---

## 3.1 为什么需要模块化？

在进入语法细节之前，先想一个问题：为什么不能把代码全写在一个文件里？

### 没有模块的世界

假设你写了一个简单的程序：一个文件工具，能读取文件、统计单词数、写入结果。如果不做模块化，你的代码可能长这样：

```javascript
// 没有模块化 —— 所有代码在一个文件里
const fs = require('fs');  // 等一下，require 本身也是模块化语法
```

就算只是提笔写几行，你也立刻会发现：你的 `countWords` 函数、`readFile` 函数、`writeResult` 函数全部挤在同一个全局作用域里。当你引入第三方库时，万一它们的函数和你的函数同名，就会相互覆盖。这就是 **全局命名空间污染**。

### 模块化的三大好处

> [!note] 模块化用一句话概括
> 把代码拆成多个文件，每个文件只对外暴露必要的部分，隐藏内部实现细节。

具体来说，模块化带来三个核心好处：

1. **隔离作用域**：每个模块有自己的作用域，变量不会互相污染。你在文件 A 里定义的 `count` 和文件 B 里的 `count` 互不干扰。
2. **明确依赖关系**：每个文件的开头清晰声明"我用到了哪些其他文件"，别人看你的项目结构时一目了然。
3. **可复用**：写好的模块可以在不同项目中重复使用。npm 生态就是建立在这个基础上的。

> [!tip] 类比理解
> 想象你在厨房做饭。没有模块化就像把所有食材、调料、厨具全部堆在一个台面上 —— 想做一道菜得在混乱中翻找。模块化就像把厨房整理成多个柜子：一个柜子放调料，一个柜子放厨具，一个柜子放干货。每个柜子只通过"门"（接口）对外提供东西，内部怎么摆放你不用管。

---

## 3.2 CommonJS —— Node.js 的传统模块系统

CommonJS 是 Node.js 在 2009 年诞生时就采用的模块规范。它的核心是两个关键字：`require` 用于导入，`module.exports` 用于导出。

### 第一个 CommonJS 示例

我们先从一个最简单的例子开始。创建两个文件：

```javascript
// math.js —— 导出一个模块
function add(a, b) {
  return a + b;
}

function subtract(a, b) {
  return a - b;
}

// 导出函数，让其他文件可以使用
module.exports = {
  add,
  subtract
};
```

```javascript
// app.js —— 导入并使用模块
const math = require('./math.js');  // 使用相对路径引入

console.log(math.add(5, 3));        // 输出: 8
console.log(math.subtract(10, 4));  // 输出: 6
```

运行方式：

```bash
node app.js
# 输出:
# 8
# 6
```

**关键理解**：
- `require('./math.js')` 告诉 Node.js："把当前目录下 math.js 文件导出的内容拿给我"。
- `require` 的参数是文件路径，`./` 表示当前目录，不能省略。
- `module.exports` 是一个对象，你可以把任何值（函数、对象、字符串等）赋值给它。

### module.exports 的几种写法

`module.exports` 非常灵活，以下是常见的导出模式：

```javascript
// 写法 1：导出一个对象（最常用）
module.exports = {
  add,
  subtract,
  multiply: (a, b) => a * b
};
```

```javascript
// 写法 2：导出一个单独的函数
module.exports = function(a, b) {
  return a + b;
};
// 使用时: const add = require('./add.js');
```

```javascript
// 写法 3：逐个导出（exports 是 module.exports 的简写引用）
exports.add = (a, b) => a + b;
exports.subtract = (a, b) => a - b;
```

> [!warning] exports vs module.exports 的区别
> `exports` 初始是 `module.exports` 的一个引用。如果你给 `exports` 重新赋值，它就会断开与 `module.exports` 的连接，导致导出失效。**始终用 `module.exports` 是最安全的做法**。
>
> ```javascript
> // 这样不行！—— exports 被重新赋值了
> exports = { add: (a, b) => a + b };
>
> // 这样才行
> module.exports = { add: (a, b) => a + b };
> ```

### CommonJS 加载机制：同步

CommonJS 最显著的特性之一是 **同步加载**。当你写 `const math = require('./math.js')` 时，Node.js 会：

1. 暂停当前代码的执行
2. 读取并执行 `math.js` 文件
3. 拿到 `module.exports` 的值
4. 再继续执行当前代码

这就意味着：**在 require 之后的代码，一定是在模块加载完成之后才执行的**。这个机制简单直观，但对于大型应用来说，所有模块依次同步加载可能会影响启动速度。

### 每个文件都被包裹在一个函数里

你可能会奇怪：为什么在 CommonJS 中，每个文件的变量不会互相污染？答案藏在 Node.js 的一个内部机制里。

实际上，Node.js 在执行你的文件之前，会用这样一个函数把它包裹起来：

```javascript
// Node.js 内部做的事情（伪代码）
(function(exports, require, module, __filename, __dirname) {
  // 你的代码被放在这里
  const math = require('./math.js');
  // ...
});
```

这就是为什么你可以在 CommonJS 文件中直接使用 `require`、`module`、`__dirname`、`__filename` —— 它们是这个包裹函数的参数，而不是全局变量。

> [!note] __dirname 和 __filename
> `__dirname` 表示当前文件所在的目录路径，`__filename` 表示当前文件的完整路径。这两个变量在后几章处理文件路径时会非常有用。在 ESM 中，它们不存在，需要用 `import.meta.url` 替代（后文会讲）。

---

## 3.3 ESM —— 现代 JavaScript 模块系统

ESM（ES Modules）是 ECMAScript 语言标准中定义的官方模块系统。也就是说，它是 JavaScript 语言本身的一部分，而不是 Node.js 特有的。你在浏览器里用的 `import`／`export` 和 Node.js 里的 ESM 是同一套语法。

### 启用 ESM

ESM 不是 Node.js 的默认模块系统。你需要通过 `package.json` 来告诉 Node.js："这个项目使用 ESM"：

```json
{
  "name": "my-project",
  "type": "module",    // 关键：声明项目使用 ESM
  "version": "1.0.0"
}
```

加上 `"type": "module"` 之后，项目中的所有 `.js` 文件都会被当作 ESM 来处理。

### 第一个 ESM 示例

还是刚才的数学模块，用 ESM 语法重写：

```javascript
// math.js —— 使用 ESM 导出
export function add(a, b) {
  return a + b;
}

export function subtract(a, b) {
  return a - b;
}
```

```javascript
// app.js —— 使用 ESM 导入
import { add, subtract } from './math.js';

console.log(add(5, 3));       // 输出: 8
console.log(subtract(10, 4)); // 输出: 6
```

最基本的区别一目了然：
- CommonJS 用 `require()` 和 `module.exports`
- ESM 用 `import` 和 `export`

### 命名导出 vs 默认导出

ESM 提供了两种导出方式，理解两者的区别很重要。

**命名导出（Named Exports）**：每个模块可以有多个命名导出，导入时必须使用相同的名称（或通过 `as` 重命名）：

```javascript
// helpers.js
export const PI = 3.14159;
export function double(n) {
  return n * 2;
}
export class Counter {
  constructor() { this.count = 0; }
}
```

```javascript
// 导入方式 1：按需导入
import { PI, double } from './helpers.js';

// 导入方式 2：用 as 重命名
import { double as twice } from './helpers.js';

// 导入方式 3：全部导入为一个命名空间对象
import * as helpers from './helpers.js';
console.log(helpers.PI);     // 3.14159
console.log(helpers.double(5)); // 10
```

**默认导出（Default Export）**：每个模块只能有一个默认导出，导入时可以任意命名：

```javascript
// logger.js
export default function log(message) {
  console.log(`[LOG]: ${message}`);
}
```

```javascript
// 导入时可以任意命名
import myLogger from './logger.js';
myLogger('Hello');  // 输出: [LOG]: Hello
```

> [!tip] 优先使用命名导出
> 命名导出有几个好处：导入时名称明确、编辑器自动补全效果好、静态分析时可以"摇树优化"（tree-shaking，打包时去掉未使用的代码）。在团队项目中，建议默认使用命名导出，仅在模块公开一个主要功能时使用默认导出。

### ESM 加载机制：异步

与 CommonJS 的同步加载不同，ESM 是 **异步加载** 的。这意味着：

1. `import` 声明会被提升到模块顶部先解析（静态分析阶段）
2. 模块之间的依赖关系在执行之前就建立好了
3. 实际加载和执行是异步的，不会阻塞其他操作

这个差异在两种场景下影响明显：

**场景一：条件导入**

CommonJS 可以在条件语句中动态加载：

```javascript
// CommonJS —— 可以条件判断后再加载
if (process.env.NODE_ENV === 'production') {
  const config = require('./config.prod.js');
} else {
  const config = require('./config.dev.js');
}
```

ESM 的静态 `import` 不支持这样做：

```javascript
// ESM —— 这样会报错！
if (someCondition) {
  import { something } from './module.js'; // SyntaxError
}
```

但 ESM 提供了动态 `import()` 来解决这个需求（见后文 3.6 节）。

**场景二：顶层 await**

因为 ESM 是异步的，所以它支持 **顶层 await** —— 在模块的最顶层直接使用 `await`，而不需要包裹在 async 函数里：

```javascript
// config.mjs —— ESM 中可以直接在顶层使用 await
import { readFile } from 'node:fs/promises';

// 顶层 await —— CommonJS 做不到
const config = JSON.parse(await readFile('./config.json', 'utf-8'));

export default config;
```

在 CommonJS 中，你必须这样写：

```javascript
// config.cjs —— CommonJS 必须包裹在 async 函数里
const { readFile } = require('fs/promises');

async function loadConfig() {
  const config = JSON.parse(await readFile('./config.json', 'utf-8'));
  module.exports = config;
}

loadConfig();
// 注意：此时 module.exports 可能还是空的！
```

### 两种模块系统的对比

| 特性 | CommonJS | ESM |
|------|----------|-----|
| 语法 | `require()` / `module.exports` | `import` / `export` |
| 启用方式 | 默认（无需配置） | 在 `package.json` 中设置 `"type": "module"` |
| 加载方式 | 同步 | 异步 |
| 顶层 await | 不支持 | 支持 |
| 静态分析 | 不支持（动态加载） | 支持（可 tree-shaking） |
| 导出值 | 值的拷贝（原始值类型） | Live binding（实时绑定） |
| 浏览器支持 | 不支持 | 支持 |
| 适用场景 | 遗留项目、Node.js 特定工具 | 新项目、前端/全栈项目 |

> [!note] Live Binding 是什么意思？
> 在 ESM 中，导出的值是一个"活的引用"。如果导出模块在后续运行时修改了某个值，导入方看到的是最新值。而在 CommonJS 中，`require()` 拿到的是导出值的一份拷贝（原始类型）或引用（对象类型）。

---

## 3.4 如何在项目中选择：CommonJS vs ESM

### 通过 package.json 的 type 字段控制

`package.json` 中的 `type` 字段决定 Node.js 如何解析项目中的 `.js` 文件：

```json
// 情况 1：没有 type 字段（默认是 CommonJS）
{
  "name": "cjs-project"
}
// 所有 .js 文件都是 CommonJS

// 情况 2：type: "module"
{
  "name": "esm-project",
  "type": "module"
}
// 所有 .js 文件都是 ESM

// 情况 3：type: "commonjs"
{
  "name": "explicit-cjs",
  "type": "commonjs"
}
// 显式声明 CommonJS（与不加 type 效果相同）
```

### 通过文件扩展名强制指定

如果你不想修改 `package.json`，或者项目同时使用了两种模块系统，可以通过文件扩展名来控制：

| 扩展名 | 强制解释为 | 适用场景 |
|--------|-----------|---------|
| `.cjs` | CommonJS | 在 ESM 项目中嵌入 CommonJS 文件 |
| `.mjs` | ESM | 在 CommonJS 项目中嵌入 ESM 文件 |
| `.js` | 由 `package.json` 的 `type` 字段决定 | 默认 |

### 2026 年的推荐实践

> [!tip] 新项目默认使用 ESM
> 2026 年，ESM 已成为 Node.js 生态的主流选择。所有主流框架、工具库、官方文档都已全面支持 ESM。除非你正在维护一个遗留的 CommonJS 项目，否则新建项目时应在 `package.json` 中添加 `"type": "module"`。
>
> 选择 ESM 的理由：
> 1. 它是 JavaScript 语言标准，浏览器和 Node.js 统一语法
> 2. 支持静态分析和 tree-shaking（打包优化）
> 3. 支持顶层 await
> 4. 与前端代码共享同一套模块语法
> 5. Node.js 官方和社区都推荐

---

## 3.5 两种模块的互操作

现实中你很可能遇到这种情况：项目是 ESM 的，但某个 npm 包只提供了 CommonJS 版本；或者反过来。Node.js 提供了一些互操作机制来解决这个问题。

### 从 ESM 加载 CommonJS

ESM 的 `import` 可以直接加载 CommonJS 模块：

```javascript
// 这是一个 ESM 文件 (type: "module")
import lodash from 'lodash';  // lodash 是 CommonJS 包，可以直接 import

// 也可以加载本地的 CJS 文件
import config from './config.cjs';  // 加载 .cjs 文件
```

但如果需要更灵活的控制（比如像 CommonJS 那样动态加载），可以用 `createRequire`：

```javascript
// ESM 文件中使用 createRequire 来获得 require 能力
import { createRequire } from 'node:module';

const require = createRequire(import.meta.url);  // 创建一个 require 函数

// 现在你可以像在 CommonJS 中一样使用 require 了
const lodash = require('lodash');
const config = require('./config.cjs');
```

### 从 CommonJS 加载 ESM

CommonJS 的 `require` **不能直接加载 ESM 模块**。需要用动态 `import()` 来代替，它返回一个 Promise：

```javascript
// 这是一个 CommonJS 文件
async function loadESMModule() {
  try {
    // 动态 import() 可以加载 ESM
    const esmModule = await import('./esm-file.mjs');
    console.log(esmModule.someExport);
  } catch (err) {
    console.error('加载 ESM 模块失败:', err);
  }
}

loadESMModule();
```

> [!warning] 动态 import() 与静态 import 的区别
> ESM 的 `import something from './module.js'` 是静态的、声明式的，必须在文件顶层使用。而 `import('./module.js')` 是一个函数调用，返回 Promise，可以在任何地方使用，两种模块系统都支持。
>
> 动态 `import()` 的使用场景：
> - 按需加载（用户点击后才加载某个模块）
> - 条件加载（根据环境加载不同配置）
> - 在 CommonJS 中加载 ESM 模块

---

## 3.6 node: 前缀与推荐实践

### 使用 node: 前缀导入核心模块

Node.js 内置的核心模块（如 `fs`、`path`、`http`）可以通过 `node:` 前缀来导入：

```javascript
// 推荐写法 —— 加上 node: 前缀
import fs from 'node:fs/promises';
import path from 'node:path';
import http from 'node:http';

// 传统写法 —— 没有前缀也能用，但不够清晰
import fs from 'fs';
import path from 'path';
```

`node:` 前缀的作用是 **明确告诉你和 Node.js：这个模块是内置的，不是 npm 包**。假设你安装了一个名为 `fs` 的 npm 包（虽然不太可能），不带前缀的写法就会产生歧义。

> [!tip] 推荐：始终使用 node: 前缀
> 从 Node.js 16 开始，官方推荐在导入核心模块时使用 `node:` 前缀。这既提高了代码的可读性，也避免了潜在的名字冲突。在编写本笔记的所有示例时，我们都会使用这个风格。

### 推荐实践总结

结合以上所有内容，以下是 2026 年使用 Node.js 模块系统的推荐做法：

```json
// package.json —— 新项目标准配置
{
  "name": "modern-node-app",
  "version": "1.0.0",
  "type": "module",           // 使用 ESM
  "description": "一个现代 Node.js 应用"
}
```

```javascript
// 示例：一个现代 ESM 模块的完整写法
import { readFile, writeFile } from 'node:fs/promises';
import { join } from 'node:path';
import { createRequire } from 'node:module';

// 只在需要加载 CommonJS 包时才创建 require
const require = createRequire(import.meta.url);

// 命名导出优先
export async function loadConfig(configPath) {
  const fullPath = join(process.cwd(), configPath);
  const data = await readFile(fullPath, 'utf-8');
  return JSON.parse(data);
}

export const VERSION = '1.0.0';
```

**几条核心建议**：

1. **新项目用 ESM**：在 `package.json` 中添加 `"type": "module"`
2. **核心模块加 `node:` 前缀**：`import fs from 'node:fs'`
3. **优先命名导出**：保持接口清晰，便于 tree-shaking
4. **遗留项目保持 CJS**：不要为了"升级"而重写稳定的 CJS 项目
5. **用扩展名区分**：在混合项目中，`.mjs` 和 `.cjs` 可以精确控制模块类型

---

## 本章小结

- **模块化**解决了代码组织中的三大问题：全局命名空间污染、依赖关系不清晰、代码难以复用。
- **CommonJS** 使用 `require()` 和 `module.exports`，是 Node.js 的传统模块系统，采用**同步加载**机制，每个文件被包裹在一个函数中以隔离作用域。
- **ESM** 使用 `import` 和 `export`，是 JavaScript 语言标准定义的模块系统，采用**异步加载**机制，支持静态分析和顶层 await。
- 通过 `package.json` 的 `"type": "module"` 字段启用 ESM；通过 `.mjs` 和 `.cjs` 扩展名可以强制指定文件类型。
- **互操作**：ESM 可以直接 `import` CommonJS 模块；CJS 需要用动态 `import()` 来加载 ESM 模块。
- **推荐实践**：新项目默认使用 ESM，核心模块使用 `node:` 前缀导入，优先使用命名导出。

---

## 下一章预告

模块系统解决了代码组织的问题，但真正让 Node.js 强大的，是它的异步编程能力。下一章将进入 Node.js 最核心也最容易让人困惑的部分：从回调到 Promise，再到 async/await，彻底搞懂 Node.js 异步编程的演进之路。


---

现在你掌握了两种模块系统的写法。不过，你写的很多代码还不是真正的"异步"——要理解 Node.js 为什么适合做 Web 服务器，必须先搞懂异步编程。

# 第四章：异步编程 —— 从回调到 async/await

在上一章中，你学会了怎么组织代码文件（模块系统）。但真正让 Node.js 与众不同的，是它的**异步编程模型**。

你大概在网上见到过这样的代码片段：

```javascript
setTimeout(() => console.log('3 秒后执行'), 3000)
```

你大概也知道它会"等 3 秒再执行"。但如果你再往下学一点，就会遇到 `.then()`、`await`、`Promise.all()` 这些概念，它们看起来都在"等"但又等得不一样，很容易让人一头雾水。

这一章的目标就是帮你彻底搞清楚 Node.js 异步编程的全貌。我们会从最简单的生活类比入手，然后沿着**回调 → Promise → async/await** 这条技术演进路线一步步走上来。读完之后，你不仅能看懂异步代码，还能写出干净、高效、不出错的异步逻辑。

> [!note] 这一章是整本笔记中最核心也最容易卡住的一章
> 不要追求一次完全理解。先跟着示例代码动手敲一遍，让"手"先记住，等学到事件循环（第六章）再回来看，很多疑问会自然解开。

---

## 4.1 同步 vs 异步 —— 先搞懂"等"和"不等"

### 生活类比：排队点餐 vs 取号等叫

想象你在一个快餐店。

**同步（Synchronous）模式** —— 排队点餐：
- 你站在柜台前排队，前面的人点完你才能点。
- 轮到你时，你点完餐，站在原地等餐做好，拿到餐才离开。
- 整个过程你**什么事都做不了**，就干等着。

**异步（Asynchronous）模式** —— 拿号等叫：
- 你进店先拿号，然后去旁边坐着玩手机。
- 叫到你的号时，你去取餐。
- 整个过程你**可以做其他事情**（刷手机、聊天），不用干等。

这两种模式对应到程序里就是：
- **同步代码**：程序从上往下执行，前一句没做完，后一句就不执行。
- **异步代码**：程序发出一个"需要等待"的操作（比如读文件、发网络请求）后，不等着结果，而是继续执行后面的代码。等结果回来了，再通过某种机制通知你。

### 用代码验证同步行为

新建一个文件 `sync-demo.js`：

```javascript
// sync-demo.js
const start = Date.now()

console.log('第 1 步：开始')

// 模拟一个耗时 2 秒的同步操作
const waitUntil = start + 2000
while (Date.now() < waitUntil) {
  // 空转，什么也不做，就是干等
}

console.log('第 2 步：2 秒后才到这里')

console.log('第 3 步：结束')
```

运行它：

```bash
node sync-demo.js
```

输出：

```
第 1 步：开始
// （卡了 2 秒）
第 2 步：2 秒后才到这里
第 3 步：结束
```

这个 `while` 循环让程序卡了 2 秒。在卡住的 2 秒里，程序**什么都做不了**。这就是同步阻塞。

### 用代码验证异步行为

新建 `async-demo.js`：

```javascript
// async-demo.js
console.log('第 1 步：开始')

setTimeout(() => {
  console.log('第 2 步：2 秒后执行这个回调')
}, 2000)

console.log('第 3 步：setTimeout 不阻塞，我立即执行')

console.log('第 4 步：结束')
```

运行它：

```bash
node async-demo.js
```

输出：

```
第 1 步：开始
第 3 步：setTimeout 不阻塞，我立即执行
第 4 步：结束
// （过了 2 秒）
第 2 步：2 秒后执行这个回调
```

注意到了吗？`setTimeout` 发出"等 2 秒"的指令后，程序**没有停下来等**，而是继续执行第 3 步和第 4 步。2 秒后，传给 `setTimeout` 的那个函数才被执行。

这个传给 `setTimeout` 的函数，就是**回调函数（callback function）**—— 异步编程的起点。

> [!summary] 到现在，你需要记住：
> - **同步**：排队点餐，等前面的做完才轮到你。
> - **异步**：拿号等叫，你做自己的事，叫到你再响应。
> - **回调函数**：你留给系统的"回头再叫你"的联系方式。

---

## 4.2 回调函数 —— Node.js 最早的异步方案

### 什么是回调

**回调函数**就是一个被当作参数传给另一个函数，等条件满足时再被"叫回来"执行的函数。

你刚才看到的 `setTimeout` 就是最典型的例子：

```javascript
setTimeout(
  () => console.log('2 秒后被回调'),  // 这个函数就是回调
  2000
)
```

Node.js 的核心模块大量使用回调模式。来看一个实际的例子 —— 用 `fs` 模块读文件：

```javascript
// callback-readfile.js
const fs = require('fs')

console.log('开始读文件...')

fs.readFile('package.json', 'utf-8', (err, data) => {
  if (err) {
    console.error('读取出错：', err.message)
    return
  }
  console.log('文件内容：', data.substring(0, 50) + '...')
})

console.log('读文件的请求已经发出，继续做其他事')
```

运行：

```bash
node callback-readfile.js
```

输出：

```
开始读文件...
读文件的请求已经发出，继续做其他事
// （文件读完后）
文件内容：{"name": "my-project",...
```

注意输出顺序：`"继续做其他事"` 在文件内容之前打印。`fs.readFile` 不会等文件读完再继续 —— 它把结果通过回调函数送回来，自己则立即返回。

### Callback Hell（回调地狱）

回调模式有一个致命问题：**当多个异步操作有前后依赖关系时，回调会一层层嵌套下去。**

假设你要做三件事，而且必须按顺序做：
1. 读取用户配置
2. 根据配置读取对应的数据文件
3. 把数据写入新文件

用回调写法是这样的：

```javascript
// callback-hell.js
const fs = require('fs')

fs.readFile('config.json', 'utf-8', (err, configData) => {
  if (err) {
    console.error('读配置失败：', err.message)
    return
  }

  const config = JSON.parse(configData)
  console.log('配置已读取：', config)

  fs.readFile(config.dataFile, 'utf-8', (err, data) => {
    if (err) {
      console.error('读数据失败：', err.message)
      return
    }

    console.log('数据已读取，开始处理...')
    const processed = data.toUpperCase()

    fs.writeFile('output.txt', processed, (err) => {
      if (err) {
        console.error('写入失败：', err.message)
        return
      }

      console.log('全部完成！')
    })
  })
})
```

这就是传说中的**回调地狱（callback hell）** —— 代码不断向右缩进，形成一个大三角。每层嵌套都要处理一次错误，代码的可读性和可维护性急剧下降。

> [!warning] 回调地狱的危害
> 1. **难以阅读**：嵌套逻辑把"顺序执行"变成了"金字塔"，眼睛很难跟踪流程。
> 2. **难以复用**：嵌套在里面的逻辑没法单独提取出来复用。
> 3. **错误处理分散**：每一层都要单独处理 `err`，容易遗漏。
> 4. **难以排查**：当嵌套达到 5 层以上时，出错了很难定位。

正是因为回调地狱的存在，JavaScript 社区在 ES6（2015 年）引入了一个新的异步方案 —— **Promise**。

---

## 4.3 Promise —— 更优雅的异步方案

### 什么是 Promise

Promise（承诺）是一个对象，它代表**一个尚未完成但未来会完成的操作**。

> [!note] 类比：点外卖
> 你下单后，商家给你一个"取餐号"。这个取餐号就是一个 Promise：
> - **Pending（待定）**：餐还在做，等待完成。
> - **Fulfilled（已兑现）**：餐做好了，你可以取餐。
> - **Rejected（已拒绝）**：做不了，告诉你原因（比如食材没了）。
>
> 一旦 Promise 变成 fulfilled 或 rejected，它的状态就**永远不再改变**。

### 创建一个 Promise

```javascript
// promise-basic.js
const myPromise = new Promise((resolve, reject) => {
  // 这里是"异步操作"的代码
  const success = true

  setTimeout(() => {
    if (success) {
      resolve('操作成功！这是返回的数据')
    } else {
      reject(new Error('操作失败！这是错误信息'))
    }
  }, 2000)
})

console.log('Promise 已创建，状态：pending')

// 用 .then() 处理成功结果
myPromise.then((result) => {
  console.log('成功：', result)
})

// 用 .catch() 处理失败
myPromise.catch((error) => {
  console.log('失败：', error.message)
})
```

运行：

```bash
node promise-basic.js
```

输出：

```
Promise 已创建，状态：pending
// （2 秒后）
成功：操作成功！这是返回的数据
```

如果把 `success` 改为 `false`，输出是：

```
Promise 已创建，状态：pending
// （2 秒后）
失败：操作失败！这是错误信息
```

### Promise 的三种状态

| 状态 | 含义 | 何时进入 | 后续触发 |
|------|------|---------|---------|
| **Pending（待定）** | 操作还在进行中 | 刚创建 Promise 时 | 还未确定 |
| **Fulfilled（已兑现）** | 操作成功完成 | 调用 `resolve()` 时 | 触发 `.then()` |
| **Rejected（已拒绝）** | 操作失败 | 调用 `reject()` 时 | 触发 `.catch()` |

> [!tip] Promise 状态不可逆
> 一旦 `resolve()` 或 `reject()` 其中之一被调用，Promise 的状态就**固定了**。你再调用 `resolve('第二次')` 不会起任何作用。

### 链式调用 —— 解决回调地狱

Promise 最强大的特性是 **`.then()` 可以链式调用**。每个 `.then()` 返回一个新的 Promise，可以继续 `.then()`。

把刚才的回调地狱用 Promise 重写：

```javascript
// promise-chain.js
const fs = require('fs/promises')  // 注意：用到的是 promise 版 fs

console.log('开始处理...')

fs.readFile('config.json', 'utf-8')
  .then((configData) => {
    const config = JSON.parse(configData)
    console.log('配置已读取：', config)
    return fs.readFile(config.dataFile, 'utf-8')  // 返回新 Promise
  })
  .then((data) => {
    console.log('数据已读取，开始处理...')
    const processed = data.toUpperCase()
    return fs.writeFile('output.txt', processed)  // 返回新 Promise
  })
  .then(() => {
    console.log('全部完成！')
  })
  .catch((err) => {  // 一个 catch 捕获所有错误
    console.error('处理失败：', err.message)
  })
```

对比回调地狱版本，好处显而易见：
- **扁平的链式结构**：没有嵌套，逻辑是"从上往下"读的。
- **统一的错误处理**：一个 `.catch()` 就能捕获链中任何一个环节的错误。
- **更容易复用**：每个 `.then()` 里的逻辑都可以独立提取成函数。

> [!note] `fs/promises` 是 Node.js 提供的 Promise 版文件系统 API
> 从 Node.js 14 开始，`fs` 模块额外提供了 Promise 风格的 API，可以直接用 `import fs from 'node:fs/promises'` 或 `const fs = require('fs/promises')` 导入。这是官方推荐的用法。

---

## 4.4 Promise 并行方法

有时候多个异步操作之间**没有依赖关系**，比如同时读三个文件。这时如果逐个等待，会浪费大量时间。Promise 提供了四个静态方法来处理并行操作。

### Promise.all —— 全部成功才算成功

`Promise.all` 接收一个 Promise 数组，**等所有 Promise 都成功**后才执行 `.then()`，返回结果是每个 Promise 结果的数组。**任何一个失败**，立即进入 `.catch()`。

```javascript
// promise-all.js
const fs = require('fs/promises')

async function demoAll() {
  const file1 = fs.readFile('file1.txt', 'utf-8')
  const file2 = fs.readFile('file2.txt', 'utf-8')
  const file3 = fs.readFile('file3.txt', 'utf-8')

  console.log('三个读文件操作已同时发起')

  const results = await Promise.all([file1, file2, file3])

  console.log('全部读完：')
  console.log(results[0].substring(0, 30))
  console.log(results[1].substring(0, 30))
  console.log(results[2].substring(0, 30))
}
```

如果在这个过程中**有一个文件读失败了**，`Promise.all` 会立即失败，不会等待其他文件：

```javascript
// 如果 file2.txt 不存在，Promise.all 会立即 reject
Promise.all([
  fs.readFile('file1.txt', 'utf-8'),
  fs.readFile('不存在的文件.txt', 'utf-8'),
  fs.readFile('file3.txt', 'utf-8'),
])
  .then((results) => console.log('全部成功'))
  .catch((err) => console.error('有一个失败，全部作废：', err.message))
```

输出：

```
有一个失败，全部作废：ENOENT: no such file or directory, open '不存在的文件.txt'
```

> [!tip] `Promise.all` 的"一票否决"机制
> 全部成功或一个失败就全部失败 —— 这个特性非常有用，适合**事务性操作**。比如：转账时要同时扣款和加款，任何一个失败都应该回滚。

### Promise.allSettled —— 等所有操作做完

`Promise.allSettled` 也是等所有 Promise 完成，但它**不关心成功还是失败**，而是等所有操作都"尘埃落定"。

```javascript
// promise-allsettled.js
const fs = require('fs/promises')

Promise.allSettled([
  fs.readFile('file1.txt', 'utf-8'),
  fs.readFile('不存在的文件.txt', 'utf-8'),
  fs.readFile('file3.txt', 'utf-8'),
]).then((results) => {
  results.forEach((result, index) => {
    if (result.status === 'fulfilled') {
      console.log(`任务 ${index + 1} 成功：`, result.value.substring(0, 20))
    } else {
      console.log(`任务 ${index + 1} 失败：`, result.reason.message)
    }
  })
})
```

输出示例：

```
任务 1 成功：这是 file1 的内容...
任务 2 失败：ENOENT: no such file or directory
任务 3 成功：这是 file3 的内容...
```

每个结果对象都包含 `status`：`'fulfilled'`（成功）或 `'rejected'`（失败）。成功时通过 `value` 取数据，失败时通过 `reason` 取错误。

> [!summary] `Promise.all` vs `Promise.allSettled`
> - **`Promise.all`**：一荣俱荣，一损俱损。适合所有操作都必需的场景。
> - **`Promise.allSettled`**：各自安好，互不影响。适合需要知道每个操作结果的场景。

### Promise.race —— 谁先到就听谁的

`Promise.race` 接收多个 Promise，**谁先确定状态（成功或失败），就用谁的结果**。

最常见的用途是**超时控制**：

```javascript
// promise-race.js
function delay(ms, value) {
  return new Promise((resolve) => setTimeout(() => resolve(value), ms))
}

function timeout(ms) {
  return new Promise((_, reject) =>
    setTimeout(() => reject(new Error(`操作超时（${ms}ms）`)), ms)
  )
}

// 模拟一个可能很慢的操作
async function fetchData() {
  // 假设这是一个网络请求，可能快也可能慢
  await delay(Math.random() * 5000)  // 0-5 秒随机延迟
  return '服务器返回的数据'
}

// 使用 race：3 秒内没返回就算超时
Promise.race([fetchData(), timeout(3000)])
  .then((result) => console.log('成功：', result))
  .catch((err) => console.error('失败：', err.message))
```

运行几次，你可能看到两种结果之一：

```
成功：服务器返回的数据
```

或者（如果随机延迟超过 3 秒）：

```
失败：操作超时（3000ms）
```

### Promise.any —— 只要有一个成功就行

`Promise.any` 接收多个 Promise，**只等待第一个成功的**。如果所有都失败，才进入 reject。

```javascript
// promise-any.js
function delay(ms, value) {
  return new Promise((resolve) => setTimeout(() => resolve(value), ms))
}

Promise.any([
  delay(3000, '服务器 A'),
  delay(1000, '服务器 B'),  // 这个最快，会用它的结果
  delay(2000, '服务器 C'),
]).then((fastest) => {
  console.log('最快的服务器是：', fastest)
})
```

输出：

```
最快的服务器是：服务器 B
```

适合场景：多个备用服务器同时请求，用最先响应的那个。

### 四种方法对比

| 方法 | 等待策略 | 成功条件 | 失败条件 | 适合场景 |
|------|---------|---------|---------|---------|
| `Promise.all` | 全等 | 全部成功 | 任一失败 | 所有操作缺一不可 |
| `Promise.allSettled` | 全等 | 各自独立 | 各自独立 | 需要知道每个结果 |
| `Promise.race` | 最先完成 | 首个完成就成功 | 首个失败就失败 | 超时控制 |
| `Promise.any` | 最先成功 | 首个成功 | 全部失败 | 备用服务切换 |

---

## 4.5 async/await —— 异步编程的终极形态

Promise 虽然解决了回调地狱的嵌套问题，但链式调用的写法依然不够"自然"。ES2017 年引入的 `async/await` 让异步代码**看起来像同步代码一样** —— 从上往下读，不用再通过 `.then()` 跳来跳去。

### 基本语法

```javascript
// async-demo.js
function delay(ms, value) {
  return new Promise((resolve) => setTimeout(() => resolve(value), ms))
}

async function main() {
  console.log('开始...')

  const result1 = await delay(1000, '第一步完成')
  console.log(result1)

  const result2 = await delay(1000, '第二步完成')
  console.log(result2)

  console.log('全部完成')
}

main()
```

运行：

```bash
node async-demo.js
```

输出：

```
开始...
// （1 秒后）
第一步完成
// （再 1 秒后）
第二步完成
全部完成
```

关键理解：

- `async` 声明这个函数是异步的。`async function` 总是返回一个 Promise。
- `await` 告诉 JavaScript："在这里等一下，等这个 Promise 完成再继续往下走"。
- `await` **只能在 `async` 函数内部使用**。

> [!note] `await` 不会阻塞整个程序
> 虽然 `await` 让代码"看起来"像在等待，但它**不会阻塞事件循环**。当 `await` 等待时，程序可以去处理其他任务（比如接收 HTTP 请求）。这是 `await` 和前面那个 `while` 循环阻塞的根本区别。

### 用 async/await 重写文件操作

```javascript
// async-file.js
const fs = require('fs/promises')

async function processFiles() {
  try {
    console.log('开始处理...')

    const configData = await fs.readFile('config.json', 'utf-8')
    const config = JSON.parse(configData)
    console.log('配置已读取：', config)

    const data = await fs.readFile(config.dataFile, 'utf-8')
    console.log('数据已读取，开始处理...')
    const processed = data.toUpperCase()

    await fs.writeFile('output.txt', processed)
    console.log('全部完成！')
  } catch (err) {
    console.error('处理失败：', err.message)
  }
}

processFiles()
```

对比之前的 Promise 链和回调地狱版本，看看这个版本的代码是不是**最接近"正常人的思维"**？就是"先做 A，等 A 完成再做 B，等 B 完成再做 C" —— 和同步代码的写法一模一样。

### 错误处理：try/catch

`async/await` 的另一个好处是可以用标准的 `try/catch` 来捕获错误，而不是 `.catch()`。

```javascript
// async-error.js
const fs = require('fs/promises')

async function readConfig() {
  try {
    const data = await fs.readFile('不存在的文件.json', 'utf-8')
    console.log('文件内容：', data)
  } catch (err) {
    // err.code 是 Node.js 系统错误码
    if (err.code === 'ENOENT') {
      console.error('文件不存在，请检查路径')
    } else if (err.code === 'EACCES') {
      console.error('没有读取权限')
    } else {
      console.error('未知错误：', err.message)
    }
  }
}

readConfig()
```

运行：

```
文件不存在，请检查路径
```

> [!tip] 不要忘记在每个 `async` 函数里加 try/catch
> 如果一个 `async` 函数中的 `await` 失败但没有被 `try/catch` 捕获，这个函数返回的 Promise 就会处在 rejected 状态。如果你也没有 `.catch()` 它，就会得到一个 **Unhandled Promise Rejection** 警告，在未来的 Node.js 版本中会导致进程崩溃。

### async/await + Promise.all —— 最佳组合

`await` 有一个隐藏陷阱：**它会阻塞当前 async 函数中的后续代码**。如果多个操作没有依赖关系，逐个 `await` 就相当于把并行变成了串行。

**错误写法** —— 串行执行（慢）：

```javascript
// async-serial.js
const fs = require('fs/promises')

async function readAllSerial() {
  const start = Date.now()

  // 一个一个读，每个都要等
  const a = await fs.readFile('file-a.txt', 'utf-8')
  const b = await fs.readFile('file-b.txt', 'utf-8')
  const c = await fs.readFile('file-c.txt', 'utf-8')

  console.log(`串行耗时：${Date.now() - start}ms`)
}
```

三个文件逐个等待，总耗时 = 三个文件耗时之和。

**正确写法** —— 并行执行（快）：

```javascript
// async-parallel.js
const fs = require('fs/promises')

async function readAllParallel() {
  const start = Date.now()

  // 同时发起三个读操作，不等结果
  const promiseA = fs.readFile('file-a.txt', 'utf-8')
  const promiseB = fs.readFile('file-b.txt', 'utf-8')
  const promiseC = fs.readFile('file-c.txt', 'utf-8')

  // 在这里一起等结果
  const [a, b, c] = await Promise.all([promiseA, promiseB, promiseC])

  console.log(`并行耗时：${Date.now() - start}ms`)
}
```

三个文件同时读，总耗时约等于最慢那个文件的时间。

> [!warning] 核心原则
> 用 `await Promise.all([...])` 代替逐个 `await`，是 Node.js 异步编程中最重要的性能优化原则之一。

---

## 4.6 并发控制

### 什么时候需要并发控制？

`Promise.all` 可以一次性发起大量并行操作。但如果操作数量太多（比如要处理 1000 个文件、发 1000 个 HTTP 请求），**同时发起所有操作可能导致问题**：

- 文件系统/网络连接数超过系统限制
- 内存使用飙升
- 目标服务器被压垮

这就需要 **并发控制（concurrency control）** —— 限制同时进行的操作数量，比如一次最多处理 5 个，处理完再接下 5 个。

### 方法一：分组分批

最简单的并发控制是分批执行：

```javascript
// batch-concurrency.js
async function processInBatches(items, batchSize, handler) {
  const results = []

  for (let i = 0; i < items.length; i += batchSize) {
    const batch = items.slice(i, i + batchSize)
    console.log(`处理第 ${i / batchSize + 1} 批（共 ${batch.length} 项）`)

    const batchResults = await Promise.all(batch.map(handler))
    results.push(...batchResults)
  }

  return results
}

// 模拟一个异步操作（比如读文件、发请求）
async function processItem(item) {
  const delay = Math.random() * 1000
  return new Promise((resolve) =>
    setTimeout(() => resolve(`${item} 处理完成（耗时 ${delay.toFixed(0)}ms）`), delay)
  )
}

// 100 个任务，一次最多处理 10 个
const items = Array.from({ length: 100 }, (_, i) => `任务 ${i + 1}`)

processInBatches(items, 10, processItem).then((results) => {
  console.log(`全部完成，共 ${results.length} 项`)
})
```

### 方法二：使用 p-limit 库

[`p-limit`](https://www.npmjs.com/package/p-limit) 是一个专门做并发控制的 npm 包，用法更加灵活（不是分批，而是维持一个固定并发数的"水龙头"）。

```bash
npm install p-limit
```

```javascript
// p-limit-demo.js
import pLimit from 'p-limit'

// 创建一个限制器，最多同时运行 5 个任务
const limit = pLimit(5)

// 模拟异步任务
function fetchData(id) {
  return new Promise((resolve) => {
    const delay = Math.random() * 2000
    setTimeout(() => resolve(`数据 ${id}（${delay.toFixed(0)}ms）`), delay)
  })
}

// 往限制器里添加 20 个任务
const tasks = Array.from({ length: 20 }, (_, i) =>
  limit(() => fetchData(i + 1))
)

console.time('并发控制')
Promise.all(tasks).then((results) => {
  console.log(results)
  console.timeEnd('并发控制')
})
```

观察运行结果，你会发现控制台里同一时间最多只有 5 个任务在执行。

> [!tip] 类似的库
> - **`p-map`**：`p-map` 内置 `concurrency` 选项，用法类似 `Array.map()` 但支持并发控制。
> - **`p-queue`**：功能最丰富，支持优先级、暂停/恢复、超时等高级特性。

---

## 4.7 常见异步陷阱

学完上面的内容，你已经能写出正确的异步代码了。但有一些"看似正确"的写法，实际上是坑。下面列出最常见的几个。

### 陷阱一：忘记 await

```javascript
// 错误写法
async function loadData() {
  const data = fs.readFile('data.json', 'utf-8')  // 忘了 await！
  console.log('文件内容：', data)  // 输出：Promise { <pending> }
  return data
}
```

`fs.readFile` 返回的是一个 Promise。不加 `await`，你得到的是 Promise 对象本身，而不是它里面的数据。

**解决方案**：检查代码，确认每个 Promise 前面都有 `await`（除非你确实想拿到 Promise 对象本身）。

### 陷阱二：串行化并行操作（经典面试题）

```javascript
// 错误写法 —— 逐个等待，效率极低
async function loadAllUsers_wrong(userIds) {
  const users = []
  for (const id of userIds) {
    const user = await fetchUser(id)  // 一个一个等
    users.push(user)
  }
  return users
}

// 正确写法 —— 同时发起，一起等待
async function loadAllUsers_correct(userIds) {
  return Promise.all(userIds.map((id) => fetchUser(id)))
}
```

> [!warning] 循环中使用 `await` 几乎总是错的
> 除非你确实需要"前一个操作的结果作为后一个操作的输入"，否则不要在循环里 `await`。改用 `Promise.all` + `map`。

### 陷阱三：忘记处理 Promise reject

```javascript
// 危险写法
async function risky() {
  throw new Error('出错了')
}

risky()  // 这个 rejected Promise 没人管！

// 正确做法 1：用 await + try/catch
try {
  await risky()
} catch (err) {
  console.error('捕获到：', err.message)
}

// 正确做法 2：加 .catch()
risky().catch((err) => console.error('捕获到：', err.message))
```

在 Node.js 中，未处理的 Promise reject 会在终端打印警告，从 Node.js 15 开始，这会导致进程直接崩溃。

### 陷阱四：混用 .then() 和 await

```javascript
// 混搭写法 —— 不推荐，容易混乱
async function confusing() {
  const data = await fetchData().then((d) => d.toUpperCase())
  return data
}

// 更清晰的写法 —— 选一种风格
async function clear() {
  const data = await fetchData()
  return data.toUpperCase()
}
```

建议：**新代码统一用 `async/await`**，除非你非常清楚自己在做什么。

### 陷阱五：在回调中使用 async 但不处理

```javascript
// 错误写法 —— async 回调产生的 rejected Promise 无人捕获
array.forEach(async (item) => {
  await processItem(item)
  // 如果 processItem 失败，错误不会在这里被捕获
})

// 正确做法 —— 改用 Promise.all
await Promise.all(array.map(async (item) => {
  await processItem(item)
}))
```

`forEach` 中的 `async` 回调产生的 Promise 被直接丢弃了。如果回调中有错误发生，你完全不知道。

---

## 本章小结

- **同步 vs 异步**：同步是"排队点餐"，异步是"拿号等叫"。Node.js 的核心优势就是异步非阻塞 I/O。
- **回调函数**：异步编程的最初方案，但多层嵌套会形成"回调地狱"，导致代码难以阅读和维护。
- **Promise**：ES6 引入的异步方案，通过 `.then()` 链式调用解决嵌套问题。有三种状态：**pending**（待定）、**fulfilled**（已兑现）、**rejected**（已拒绝），状态不可逆。
- **Promise 并行方法**：`Promise.all`（全部成功）、`Promise.allSettled`（全部完成）、`Promise.race`（最快的）、`Promise.any`（第一个成功的），各有适用场景。
- **async/await**：ES2017 引入的语法糖，让异步代码看起来像同步代码。配合 `try/catch` 处理错误，配合 `Promise.all` 实现并行。
- **并发控制**：当并行操作太多时，用分批处理或 `p-limit` 库来限制同时运行的数量。
- **常见陷阱**：忘记 `await`、循环中逐个 `await` 导致串行、不处理 Promise reject、混用 `.then()` 和 `await`、`forEach` 中使用 `async`。

---

## 下一章预告

你现在已经学会了异步编程的核心概念 —— 回调、Promise、async/await。但你可能还有一个疑问："`await` 等待的时候，程序到底在做什么？它为什么没有卡住？"

下一章我们将回到 Node.js 的底层，探索**事件循环（Event Loop）** —— 那个在幕后默默调度所有异步操作的"大总管"。理解了事件循环，你对 Node.js 异步编程的理解将上一个台阶。

> [!note] 中间还有一章
> 在推荐的学习顺序中，下一章其实是**第五章：文件与路径操作**。异步编程作为核心基础被提前到第四章，是希望你掌握 async/await 之后，在第五章的实际文件操作中就能直接运用。如果你觉得这章内容较多，也可以先跳到第五章做具体的 fs 练习，再回来学事件循环。


---

异步编程的概念你已经清楚了，但"纸上得来终觉浅"——让我们用 Node.js 最常用的文件操作来实践 async/await 的真实用法。

# 第五章：核心 API（一）—— 文件与路径操作

前几章我们学习了 Node.js 的模块系统和异步编程，但还缺少一个关键的拼图：**怎么操作文件？** 无论是读取配置文件、写入日志、处理上传的图片，还是遍历项目目录，文件操作几乎是每个 Node.js 程序都绕不开的任务。本章将系统学习两个最常用的内置模块——`path` 和 `fs`，学完你就能写出真正"有用"的 Node.js 程序了。

---

## 5.1 path 模块 —— 路径的正确打开方式

初学者最常犯的错误之一就是用字符串硬编码路径：

```javascript
// 这样写很危险
const filePath = './data/info.txt'
```

这段代码在你本地可能跑得好好的，但换到另一个操作系统、或者从不同目录启动程序时，就会报错"文件不存在"。为什么？因为**不同操作系统使用的路径分隔符不同**：

| 系统 | 路径示例 | 分隔符 |
|------|---------|--------|
| Windows | `C:\Users\name\file.txt` | 反斜杠 `\` |
| macOS / Linux | `/Users/name/file.txt` | 正斜杠 `/` |

`path` 模块就是用来解决这个问题的。它是 Node.js 内置模块，不需要额外安装，直接导入就能用。

### 5.1.1 path.join —— 安全拼接路径片段

`path.join()` 把多个路径片段拼接成一个完整的路径，它会**自动处理分隔符**：

```javascript
import path from 'node:path'

// macOS/Linux 输出: data/info.txt
// Windows 输出:      data\info.txt
const file1 = path.join('data', 'info.txt')
console.log(file1)

// 处理上级目录 ..
// macOS/Linux 输出: /project/data
const file2 = path.join('/project', 'src', '..', 'data')
console.log(file2)
```

`path.join` 的核心原则是：**传入片段，它负责拼好**。你不需要关心当前是什么操作系统，也不需要自己拼接字符串。

> [!note]
> 在 ESM 中导入核心模块时，推荐使用 `node:` 前缀 —— 如 `import path from 'node:path'`。这能清晰表明它是 Node.js 内置模块，避免与同名 npm 包冲突。

### 5.1.2 path.resolve —— 解析为绝对路径

`path.resolve()` 和 `path.join()` 看起来很像，但有一个关键区别：**`resolve` 会把相对路径解析为绝对路径**。

```javascript
import path from 'node:path'

// join: 只是拼接
console.log(path.join('data', 'info.txt'))
// 输出: data/info.txt（保持相对）

// resolve: 解析为绝对路径
console.log(path.resolve('data', 'info.txt'))
// 输出: /Users/你的用户名/当前目录/data/info.txt（转为绝对）
```

**什么时候用哪个？**

| 函数 | 行为 | 推荐场景 |
|------|------|---------|
| `path.join()` | 按规则拼接路径片段，不生成绝对路径 | 组合任意路径片段时 |
| `path.resolve()` | 从右向左解析，生成绝对路径 | 需要最终得到一个绝对路径时 |

看一个更具体的对比：

```javascript
import path from 'node:path'

// join：只是按顺序拼接
const j1 = path.join('/base', '/sub', 'file.txt')
// 输出: /base/sub/file.txt（第二个 /sub 被当做普通片段）

// resolve：从右向左找绝对路径，找到就停止
const r1 = path.resolve('/base', '/sub', 'file.txt')
// 输出: /sub/file.txt（遇到 /sub 是绝对路径，不再管左边的 /base）

// 典型用法：基于当前工作目录拼出绝对路径
const r2 = path.resolve('data', 'info.txt')
// 输出: /Users/xxx/当前工作目录/data/info.txt
```

> [!tip] 新手记忆技巧
> 把 `join` 想成"搭积木"——它只是按顺序把积木块拼在一起。把 `resolve` 想成"导航到目的地"——它从最右边开始找，一旦遇到绝对路径（以 `/` 开头）就当成了最终目的地，忽略左边所有的内容。

### 5.1.3 path.basename 和 path.extname —— 提取文件名和扩展名

这两个函数从一个路径中提取你感兴趣的部分：

```javascript
import path from 'node:path'

const filePath = '/project/src/index.html'

// 获取文件名（包含扩展名）
console.log(path.basename(filePath))  // 输出: index.html

// 获取文件名（去掉扩展名）
console.log(path.basename(filePath, '.html'))  // 输出: index

// 获取扩展名
console.log(path.extname(filePath))  // 输出: .html

// 获取目录部分
console.log(path.dirname(filePath))  // 输出: /project/src
```

这四个函数（`join`、`resolve`、`basename`、`extname`）覆盖了日常路径操作的 90% 需求。

---

## 5.2 __dirname vs import.meta.url

在第三章学习模块系统时提到过，CommonJS 和 ESM 有一些语法上的区别。`__dirname` 就是其中典型的一个。

### CommonJS 中的 __dirname

在 CommonJS 模块中，`__dirname` 是一个全局变量，表示当前文件所在的目录：

```javascript
// 文件位置: /project/src/utils.js
console.log(__dirname)
// 输出: /project/src
```

这在拼接路径时非常有用：

```javascript
const path = require('path')
const fullPath = path.join(__dirname, 'data', 'config.json')
// fullPath = /project/src/data/config.json
```

### ESM 中没有 __dirname

如果你使用 ESM（`"type": "module"` 或 `.mjs` 文件），`__dirname` 是不存在的。你需要用 `import.meta.url` 配合 `fileURLToPath` 来替代：

```javascript
import path from 'node:path'
import { fileURLToPath } from 'node:url'

// 获取当前文件的绝对路径
const __filename = fileURLToPath(import.meta.url)
// 输出: /project/src/utils.js

// 获取当前文件所在的目录
const __dirname = path.dirname(__filename)
// 输出: /project/src

// 然后就能像 CommonJS 一样拼接路径了
const fullPath = path.join(__dirname, 'data', 'config.json')
```

> [!note]
> 你不需要死记这段代码。当你在 ESM 项目中需要获取当前文件路径时，回来复制这个模式就行。Node.js 官方也知道这个写法有点啰嗦，未来版本可能会提供更简洁的方案。

---

## 5.3 fs 模块 —— 操作文件系统的三套 API

`fs`（File System）是 Node.js 中做文件操作的核心模块。它提供了**三套 API**，初学者很容易搞混。

### 三套 API 对比

| API 风格 | 写法 | 是否推荐 |
|----------|------|---------|
| 回调式 | `fs.readFile(path, (err, data) => {})` | ❌ 不推荐 |
| 同步式 | `fs.readFileSync(path)` | ⚠️ 特定场景可用 |
| Promise 式 | `fs.promises.readFile(path)` | ✅ **推荐** |

看一个直观的对比，同样是读取一个文件：

```javascript
import fs from 'node:fs'

// 1. 回调式（Callback）—— 不推荐
fs.readFile('info.txt', 'utf-8', (err, data) => {
  if (err) {
    console.error('读取失败:', err)
    return
  }
  console.log(data)
})

// 2. 同步式（Sync）—— 阻塞事件循环
const data = fs.readFileSync('info.txt', 'utf-8')
console.log(data)

// 3. Promise 式（Promises）—— 推荐
import fs from 'node:fs/promises'

try {
  const data = await fs.readFile('info.txt', 'utf-8')
  console.log(data)
} catch (err) {
  console.error('读取失败:', err)
}
```

**为什么推荐 Promise 式？**

- 回调式容易陷入"回调地狱"（第四章已经讲过了）
- 同步式会**阻塞事件循环**，在服务器场景下意味着所有其他用户都要等待文件读完
- Promise 式配合 `async/await`，代码最清晰、最安全

> [!warning] 同步 API 在什么场景下能用？
> 唯一适合使用同步 API 的场景是**程序启动时的一次性读取** —— 比如在服务器启动时读取配置文件。在请求处理过程中，永远使用异步 API。

### 5.3.1 使用 fs.promises 读写文件

推荐的做法是直接从 `node:fs/promises` 导入：

```javascript
import { readFile, writeFile } from 'node:fs/promises'

// 读取文件
try {
  const data = await readFile('hello.txt', 'utf-8')
  console.log('文件内容:', data)
} catch (err) {
  console.error('读取失败:', err.message)
}

// 写入文件（覆盖写入）
await writeFile('hello.txt', 'Hello, Node.js!', 'utf-8')
console.log('写入成功')

// 追加写入（在已有内容后添加）
import { appendFile } from 'node:fs/promises'
await appendFile('hello.txt', '\n第二行内容', 'utf-8')
```

**完整的读写实战**，创建一个笔记读写程序：

```javascript
import { readFile, writeFile, appendFile } from 'node:fs/promises'

const FILE_PATH = 'memo.txt'

// 写入笔记（覆盖）
await writeFile(FILE_PATH, '这是我的第一条笔记。\n', 'utf-8')
console.log('笔记已创建')

// 追加内容
await appendFile(FILE_PATH, '这是第二天追加的内容。\n', 'utf-8')
console.log('内容已追加')

// 读取全部内容
const content = await readFile(FILE_PATH, 'utf-8')
console.log('--- 当前笔记 ---')
console.log(content)
console.log('--- 笔记结束 ---')
```

预期输出：

```
笔记已创建
内容已追加
--- 当前笔记 ---
这是我的第一条笔记。
这是第二天追加的内容。

--- 笔记结束 ---
```

**编码参数 `'utf-8'` 是什么意思？**

如果不传 `'utf-8'`，`readFile` 返回的是一个 **Buffer** 对象（二进制数据），而不是字符串：

```javascript
const data = await readFile('memo.txt')
console.log(data)        // <Buffer e6 88 91 e7 9a 84...>
console.log(data.toString())  // 手动转成字符串
```

大部分文本操作场景都需要传 `'utf-8'`。只有处理图片、音频等二进制文件时才不传编码。

> [!note] 为什么叫 Buffer？
> 可以把 Buffer 想象成一个"搬运箱"——Node.js 从硬盘读取数据时，先把数据装进这个箱子（Buffer），然后你可以决定怎么处理它：转成字符串、传给图片处理库、或者通过网络发送。Buffer 专门用于处理二进制数据，是 Node.js 中非常重要的概念。

---

## 5.4 目录操作 —— 创建、读取、删除

### 5.4.1 创建目录（mkdir）

```javascript
import { mkdir } from 'node:fs/promises'

// 创建单层目录
await mkdir('my-data')
console.log('目录已创建')

// 递归创建多层目录（非常重要）
await mkdir('project/src/components', { recursive: true })
console.log('多层目录已创建')
```

`{ recursive: true }` 这个选项在不传的情况下，如果要创建的目录的上级目录不存在，会报错。加上 `recursive: true` 后，它会像 `mkdir -p` 一样自动创建所有不存在的父目录。

### 5.4.2 读取目录内容（readdir）

```javascript
import { readdir } from 'node:fs/promises'

// 读取当前目录下的所有文件和子目录
const files = await readdir('.')
console.log('当前目录内容:', files)

// 读取指定目录
const srcFiles = await readdir('./src')
console.log('src 目录内容:', srcFiles)

// 递归读取（需要自己实现递归，或者用第三方库）
// readdir 默认只读一层，不递归子目录
```

**用读目录 + 文件信息做一个"简易 ls"命令：**

```javascript
import { readdir } from 'node:fs/promises'
import path from 'node:path'

async function listDir(dirPath) {
  const items = await readdir(dirPath)
  for (const item of items) {
    console.log(item)
  }
}

await listDir('.')
```

### 5.4.3 删除文件与目录

```javascript
import { unlink, rmdir, rm } from 'node:fs/promises'

// 删除文件
await unlink('temp.txt')

// 删除空目录
await rmdir('empty-dir')

// 递归删除非空目录（推荐）
await rm('project', { recursive: true, force: true })
```

`rm` 是 Node.js 14.14+ 引入的，可以替代 `rmdir` 的大部分用途。`force: true` 的含义是：如果目录不存在，不会报错。

> [!warning] rm 是危险操作
> `await rm('node_modules', { recursive: true })` 会删除整个目录且不可恢复，使用时务必小心。

---

## 5.5 文件信息查询（stat）

有时你需要知道一个文件的信息：它是文件还是目录？有多大？什么时候修改的？`stat` 就是做这个的：

```javascript
import { stat } from 'node:fs/promises'

try {
  const stats = await stat('memo.txt')

  console.log('文件信息:')
  console.log('  是文件吗?', stats.isFile())       // true
  console.log('  是目录吗?', stats.isDirectory())  // false
  console.log('  文件大小:', stats.size, '字节')     // 单位：字节
  console.log('  创建时间:', stats.birthtime)        // 返回 Date 对象
  console.log('  修改时间:', stats.mtime)

  // 人类可读的大小
  const sizeKB = (stats.size / 1024).toFixed(2)
  console.log('  文件大小:', sizeKB, 'KB')
} catch (err) {
  console.error('无法获取文件信息:', err.message)
}
```

**一个实用场景：检查文件或目录是否存在**

```javascript
import { stat } from 'node:fs/promises'

async function exists(path) {
  try {
    await stat(path)
    return true
  } catch {
    return false
  }
}

if (await exists('config.json')) {
  console.log('配置文件存在')
} else {
  console.log('配置文件不存在')
}
```

> [!tip] 为什么不直接用 fs.existsSync？
> Node.js 有一个 `fs.existsSync()` 函数，但它被标记为"已废弃"（deprecated）。推荐的做法是用 `stat()` 加 try/catch 来判断文件是否存在。

---

## 5.6 综合实战 —— 日志工具

把本章的知识点串起来，写一个简单的日志工具：

```javascript
import { appendFile, readFile, mkdir, stat } from 'node:fs/promises'
import path from 'node:path'
import { fileURLToPath } from 'node:url'

// 在 ESM 中模拟 __dirname
const __dirname = path.dirname(fileURLToPath(import.meta.url))

const LOG_DIR = path.join(__dirname, 'logs')
const LOG_FILE = path.join(LOG_DIR, 'app.log')

// 确保 logs 目录存在
await mkdir(LOG_DIR, { recursive: true })

// 写入一条日志（带时间戳）
function getTimestamp() {
  return new Date().toISOString()
}

await appendFile(
  LOG_FILE,
  `[${getTimestamp()}] 应用启动了\n`,
  'utf-8'
)
console.log('日志已写入')

// 稍后再写一条
await appendFile(
  LOG_FILE,
  `[${getTimestamp()}] 用户登录成功\n`,
  'utf-8'
)

// 读取并打印所有日志
const logs = await readFile(LOG_FILE, 'utf-8')
console.log('--- 日志内容 ---')
console.log(logs)

// 查询日志文件大小
const stats = await stat(LOG_FILE)
console.log(`日志文件大小: ${(stats.size / 1024).toFixed(2)} KB`)
```

预期输出：

```
日志已写入
--- 日志内容 ---
[2026-07-27T12:00:00.000Z] 应用启动了
[2026-07-27T12:00:00.100Z] 用户登录成功

日志文件大小: 0.12 KB
```

---

## 5.7 大文件处理思路 —— Stream 的概念引入

以上所有的 `readFile` 和 `writeFile` 都是**一次性加载全部数据到内存**。这对于小文件（几 MB 以内）完全没问题，但如果要处理几百 MB 甚至 GB 级别的文件，你就会遇到问题：

```javascript
// 处理 1GB 的文件 —— 内存会爆炸！
const hugeData = await readFile('large-file.mp4')
```

Node.js 在这种情况下提供了 **Stream（流）** 的解决方案。Stream 的核心思路是：**不一次性读取整个文件，而是分块处理**。

```javascript
import { createReadStream, createWriteStream } from 'node:fs'
import { createGzip } from 'node:zlib'

// 创建一个读取流和一个写入流
const readStream = createReadStream('large-file.mp4')
const writeStream = createWriteStream('large-file.mp4.gz')
const gzip = createGzip()

// 管道连接：读取 → 压缩 → 写入
readStream.pipe(gzip).pipe(writeStream)

console.log('压缩任务已启动，内存占用极低')
```

Stream 的精髓在于 `pipe`（管道）—— 就像 Unix 命令 `cat file | grep pattern` 一样，数据像水流一样从一个管道流向下一个。

> [!note] 本章只是引入 Stream 的概念
> 你现在只需要知道：**小文件用 `readFile` / `writeFile`，大文件要用 Stream**。Stream 的详细用法会在后续章节深入讲解。这是 Node.js 中最强大的特性之一，也是初学者最容易忽略的。

---

## 本章小结

- **`path.join()` 安全拼接路径**，自动处理不同操作系统的分隔符差异；**`path.resolve()` 生成绝对路径**，从右向左解析。
- **`path.basename()` 提取文件名**，**`path.extname()` 提取扩展名**，`path.dirname()` 提取目录路径。
- **ESM 中没有 `__dirname`**，用 `fileURLToPath(import.meta.url)` 加 `path.dirname()` 替代。
- **推荐使用 `fs.promises`**（从 `node:fs/promises` 导入），配合 `async/await` 读写文件，避免回调嵌套和事件循环阻塞。
- **`{ recursive: true }` 递归创建目录**，这是创建多层目录时的标准写法。
- **`stat()` 获取文件信息**，可以用来判断文件/目录类型、文件大小、修改时间等。
- **小文件用 readFile/writeFile，大文件用 Stream** —— 这是处理文件时的核心决策点。

---

## 下一章预告

文件操作时我们说"大文件用 Stream"，但 Stream 到底是什么？它为什么能处理大文件而不会占满内存？下一章我们将回到 Node.js 最核心的机制——**事件循环**，理解异步操作在底层究竟是如何被调度执行的。这是区分"会用 Node"和"理解 Node"的分水岭。


---

文件操作你已经用得比较熟练了。但你可能还有一个疑问挥之不去：JavaScript 明明是单线程的，为什么它能同时处理文件读写、网络请求、定时器？这背后的秘密就是事件循环。

# 第六章：事件循环 —— 理解 Node.js 异步的核心

上一章我们学习了用 `fs` 模块读写文件、操作路径。当时我们写了很多 `async/await` 代码，假设你已经知道"异步"是什么意思。

但你可能一直有一个疑问：**JavaScript 明明是单线程的，一次只能做一件事，为什么它能同时处理网络请求、文件读写、定时器这些互不干扰的任务？是谁在背后调度这一切？**

答案是：**事件循环（Event Loop）**。

---

## 6.1 为什么需要事件循环

先回顾一下第 4 章学过的内容：异步编程。我们当时用 setTimeout、Promise、async/await 实现了"先不等待，等结果好了再处理"。但有一个关键问题我们没有讨论 —— **这些"等结果好了"的机制，是谁在背后盯着结果是否就绪？**

假设你在一个餐厅吃饭：

- 你点了餐（发起了一个异步操作，比如读文件）
- 服务员把你的单子交给了厨房（Node.js 把任务交给了 libuv）
- 你继续坐着喝茶刷手机（主线程继续执行其他代码）
- 厨房做好菜后，传菜员把菜送到你桌上（回调被执行）

这个"餐厅"里必须有一个**调度员**，他负责：
1. 看看哪些菜做好了（检查 I/O 事件是否完成）
2. 把做好的菜端到对应顾客桌上（执行回调函数）
3. 再看看有没有新订单（处理新的请求）

在 Node.js 中，这个"调度员"就是**事件循环**。

> [!note] 事件循环的定义
> 事件循环是一个永不停歇的循环机制，它负责**协调** JavaScript 代码的执行、异步事件的回调、定时器触发和 I/O 操作的结果处理。它不是 V8 引擎的一部分，而是由 **libuv** 库实现的。

事件循环像一个运转不息的**传送带**。JavaScript 主线程把各种任务放到传送带上，传送带把它们送到对应的处理站，处理完成后又把结果送回来。主线程则继续处理新的请求，不会被阻塞。

---

## 6.2 事件循环的六大阶段

libuv 实现的事件循环每一轮（称为一个 tick）会依次走过六个阶段。每个阶段都有一个**队列**，存放着该阶段需要执行的回调函数。

```
   ┌───────────────────────────┐
┌─>│          timers           │  setTimeout / setInterval 回调
│  └─────────────┬─────────────┘
│  ┌─────────────┴─────────────┐
│  │     pending callbacks     │  系统级回调（如 TCP 错误）
│  └─────────────┬─────────────┘
│  ┌─────────────┴─────────────┐
│  │       idle, prepare       │  内部使用，业务透明
│  └─────────────┬─────────────┘
│  ┌─────────────┴─────────────┐
│  │           poll            │  ← 核心：取 I/O 事件、执行回调
│  └─────────────┬─────────────┘
│  ┌─────────────┴─────────────┐
│  │           check           │  setImmediate 回调
│  └─────────────┬─────────────┘
│  ┌─────────────┴─────────────┐
└──┤     close callbacks       │  socket.on('close') 等
   └───────────────────────────┘
```

这个图看起来可能有点吓人，但好消息是：**对日常业务开发来说，你只需要重点关注三个阶段：timers、poll、check**。其他三个阶段要么是系统内部使用的，要么是你的代码很少直接触及的。

下面逐一介绍这六个阶段，但我们会把重点放在那三个核心阶段上。

### timers 阶段

这是每一轮事件循环的起点。在这个阶段，Node.js 会检查是否有到期的 `setTimeout()` 或 `setInterval()` 回调。如果有，就执行它们。

```javascript
console.log('开始')
setTimeout(() => {
  console.log('定时器回调执行')
}, 1000)
console.log('结束')
// 输出顺序：开始 → 结束 → （等待约 1 秒）→ 定时器回调执行
```

当你调用 `setTimeout(cb, 1000)` 时，Node.js 并不是"等 1 秒后执行"，而是"把这个回调注册进去，等 1 秒后把回调放到 timers 队列，等事件循环到了 timers 阶段就执行它"。

> [!tip] setTimeout 的延迟是"最短等待时间"，不是"精确延迟时间"
> 如果你设置 `setTimeout(cb, 1000)`，它保证**至少**等 1000 毫秒，但实际执行时间可能更晚。因为前面阶段的任务可能还没处理完，事件循环要等当前阶段结束后才能进入 timers 阶段。

### pending callbacks 阶段

这个阶段执行一些系统级别的回调。比如 TCP 连接出错时，错误回调会在这里被执行。

> [!note] 你很少需要直接接触这个阶段
> 除非你在写底层网络库，否则平时几乎感受不到这个阶段的存在。把它当作"系统处理一些善后工作"的环节就好。

### idle, prepare 阶段

这是 libuv 内部使用的阶段，用来做一些准备工作。对你的业务代码来说完全透明。

### poll 阶段（核心）

**poll 阶段是事件循环中最重要、最忙碌的阶段**。它主要做两件事：

1. **等待新的 I/O 事件** —— 比如文件读取完成、网络数据到达
2. **执行 I/O 相关的回调** —— 比如 `fs.readFile` 的回调

Node.js 的事件循环大部分时间都停留在这个阶段。如果没有定时器需要处理，它会在这里等待新的事件到来。

```javascript
const fs = require('fs')

console.log('开始读文件')

fs.readFile('hello.txt', 'utf8', (err, data) => {
  console.log('文件读取完成')
})

console.log('继续做其他事')

// 输出顺序：
// 开始读文件
// 继续做其他事
// （等待文件读取完成）
// 文件读取完成
```

> [!note] poll 阶段是"中转站"
> poll 阶段不仅执行自己的 I/O 回调，还负责检查 timers 和 check 阶段是否有待处理的任务。如果 poll 阶段的队列为空，事件循环会在这里等待，直到有新的任务到来，或者定时器到期、setImmediate 被调用。

### check 阶段

这个阶段专门执行 `setImmediate()` 注册的回调。

```javascript
const fs = require('fs')

fs.readFile('hello.txt', () => {
  console.log('1. 文件读取完成')

  setTimeout(() => {
    console.log('2. setTimeout')
  }, 0)

  setImmediate(() => {
    console.log('3. setImmediate')
  })
})
```

猜猜输出顺序？答案是 `1 → 3 → 2`。原因我们在第 6.4 节会详细解释，这里先记住结论：**在 I/O 回调中，check 阶段永远在下一轮 timers 阶段之前执行**。

### close callbacks 阶段

这是每一轮事件循环的最后一站。它执行一些关闭相关的回调，比如 `socket.on('close')`。

```javascript
const net = require('net')
const server = net.createServer()

server.on('close', () => {
  console.log('服务器关闭了')
})

server.close() // 这会触发 close 事件
```

---

## 6.3 微任务与 nextTick

现在你知道了事件循环的六个阶段。但聪明的你可能会问：**Promise 的 `.then()` 回调在哪里执行？`process.nextTick()` 又是在哪个阶段？**

答案是：**它们不属于任何阶段**。

微任务（Microtask）和 `process.nextTick` 的回调不在六个阶段的队列里。它们有自己的**独立队列**，而且优先级非常高 —— 在每个阶段的**间隙**被清空。

理解这个顺序至关重要：

```
当前阶段回调执行完毕
    ↓
清空 process.nextTick 队列（全部）
    ↓
清空 Promise 微任务队列（全部）
    ↓
进入事件循环的下一个阶段
```

> [!warning] 注意执行顺序
> **`process.nextTick` 的优先级高于 Promise 微任务**。在同一批微任务中，`process.nextTick` 的回调永远先于 Promise 的 `.then()` 执行。

下面来看一道经典的面试题，它能帮助你彻底理解这个顺序：

```javascript
console.log('1')

setTimeout(() => console.log('2'), 0)

Promise.resolve().then(() => console.log('3'))

process.nextTick(() => console.log('4'))

console.log('5')

// 输出顺序是什么？
```

我们一步步分析：

1. 同步代码先执行：打印 `1` 和 `5`
2. `setTimeout(0)` 注册了一个定时器回调 —— 放到 timers 队列
3. `Promise.resolve().then()` 注册了一个微任务 —— 放到 Promise 微任务队列
4. `process.nextTick()` 注册了一个回调 —— 放到 nextTick 队列
5. 同步代码执行完毕，开始清空微任务队列
6. **先清空 nextTick 队列**：打印 `4`
7. **再清空 Promise 队列**：打印 `3`
8. 微任务队列清空，进入事件循环的 timers 阶段
9. timers 阶段执行 setTimeout 回调：打印 `2`

**最终输出：`1 5 4 3 2`**

> [!note] process.nextTick 听起来像"下一轮"，实际是"立刻执行"
> `process.nextTick` 的名字有很大误导性。它并不是"等到下一轮事件循环才执行"，而是"在当前同步代码执行完毕后、在事件循环进入下一个阶段之前，**立刻**执行"。递归调用 `process.nextTick` 会**饿死**事件循环，因为它永远不把控制权交还给事件循环。

看一个饿死事件循环的"坏例子"：

```javascript
function evilLoop() {
  process.nextTick(() => {
    console.log('nextTick 又来了')
    evilLoop() // 递归调用，永远不结束
  })
}

evilLoop()

setTimeout(() => {
  console.log('这个定时器永远不会被执行！')
}, 1000)

// 输出：nextTick 又来了（无限循环，永远不会执行定时器）
```

这个例子中，`process.nextTick` 的递归调用导致事件循环**永远没有机会**进入 timers 阶段。定时器的回调被彻底饿死。在实际项目中，这种代码会导致服务器完全停止响应。

> [!tip] 优先使用 setImmediate，而不是 process.nextTick
> 除非你有非常明确的理由（比如需要在 Promise 之前执行某个回调），否则优先使用 `setImmediate` 而不是 `process.nextTick`。`setImmediate` 的回调在 check 阶段执行，不会阻塞事件循环的推进，更加安全和可控。

---

## 6.4 setTimeout(0) vs setImmediate 对比实验

这两个 API 看起来功能很相似：都是"尽快执行一个回调"。但它们在事件循环中的位置完全不同。

```javascript
// 在主模块中调用
setTimeout(() => {
  console.log('setTimeout')
}, 0)

setImmediate(() => {
  console.log('setImmediate')
})
```

如果你多次运行上面的代码，可能会发现 **setTimeout 和 setImmediate 的输出顺序不确定**，有时 setTimeout 先输出，有时 setImmediate 先输出。

这是为什么？

原因在于：**从启动事件循环到进入 timers 阶段的时间不确定**。如果进程启动比较快（比如你的机器性能好），事件循环在进入 timers 阶段时，定时器的延迟还没到（连 0 毫秒都没到），那么 poll 期间等待完成后会先进入 check 阶段执行 setImmediate，下一轮再执行 setTimeout。

但在 **I/O 回调内部**，情况就完全确定了：

```javascript
const fs = require('fs')

fs.readFile(__filename, () => {
  setTimeout(() => {
    console.log('setTimeout')
  }, 0)

  setImmediate(() => {
    console.log('setImmediate')
  })
})
```

无论运行多少次，结果都是 **`setImmediate` 先输出，`setTimeout` 后输出**。

原因很简单：`fs.readFile` 的回调在 poll 阶段执行。当 poll 阶段执行完成后，事件循环自然进入 check 阶段（执行 setImmediate），然后才进入下一轮的 timers 阶段（执行 setTimeout）。

```
I/O 回调执行完毕（poll 阶段）
    ↓
进入 check 阶段，执行 setImmediate     ← 先执行
    ↓
进入下一轮 timers 阶段，执行 setTimeout  ← 后执行
```

> [!warning] 不要依赖主模块中的 setTimeout(0) 和 setImmediate 的顺序
> 在主模块（全局作用域）中，两者的执行顺序是不确定的。但如果你在 I/O 回调中使用，**setImmediate 永远先于 setTimeout(0)**。

---

## 6.5 线程池：谁在背后搬砖

你可能会好奇：**文件读取真的不需要线程吗？JavaScript 主线程不就是在等着文件读完吗？**

要回答这个问题，我们需要回到 Node.js 的架构。

事件循环管理的是**非阻塞 I/O** —— 像网络请求这样的操作，操作系统提供了非阻塞的接口。Node.js 可以把请求发出去，然后继续做其他事，等数据到了再回来处理。

但有些操作，操作系统**没有提供非阻塞接口**。比如：

- 读取本地文件
- DNS 解析（`dns.lookup()`）
- 密码哈希（`crypto.pbkdf2()`）

这些操作只能"老老实实等结果"。如果让主线程等，就会阻塞事件循环。

Node.js 的解决方案是：**把这些阻塞操作丢给线程池**。

> [!note] 什么是线程池？
> 线程池就是一群预先创建好的"工人线程"。它们专门负责执行那些会阻塞的操作。主线程把任务交给它们，然后继续做自己的事。工人们干完活后，通过事件循环把结果送回主线程。

**默认情况下，线程池有 4 个线程**。这意味着：

- 如果你同时发起 4 个文件读取操作，它们可以并行执行
- 但如果你同时发起 5 个，第 5 个会排队，等前 4 个中某个完成后才能开始

```javascript
const fs = require('fs')

// 同时读取 5 个文件
for (let i = 0; i < 5; i++) {
  fs.readFile(`file${i}.txt`, 'utf8', (err, data) => {
    console.log(`文件 ${i} 读取完成`)
  })
}
```

上面这个例子中，即使你 5 个文件同时读取，也只有前 4 个是真正并行的。第 5 个在等待线程池中出现空闲线程。

### 哪些操作走线程池？

| 使用线程池（阻塞操作） | 不走线程池（真正的异步 I/O） |
|---|---|
| 文件系统操作（`fs.*`，除 `fs.watch`） | 网络 I/O（TCP、UDP、HTTP） |
| `dns.lookup()` | `dns.resolve*()` 系列 |
| `crypto.pbkdf2()`、`scrypt`、`randomBytes` | — |
| zlib 压缩/解压 | — |

> [!tip] 调整线程池大小
> 如果项目需要大量并行文件操作，可以通过环境变量调整线程池大小（上限 1024）：
> ```bash
> UV_THREADPOOL_SIZE=8 node app.js
> ```
> 注意：这个变量必须在进程启动前设置，在代码中修改无效。

### 主线程 vs 线程池：谁在做什么？

总结一下 Node.js 的"分工体系"：

```
你写的 JavaScript 代码
    ↓ 由 V8 执行
主线程（单线程）
    ├── 执行同步代码
    ├── 管理事件循环
    └── 处理回调函数
        ↑
线程池（默认 4 线程） ──── 处理文件读写、密码哈希、压缩等
操作系统（内核）   ──── 处理网络 I/O、管道、信号等
```

- **主线程**：执行你的 JavaScript 代码，管理事件循环。**一次只能做一件事**。
- **线程池**：执行阻塞操作。多个线程可以**并行工作**。
- **操作系统内核**：处理真正的异步 I/O（网络请求等），比线程池更高效。

---

## 6.6 阻塞事件循环的危害

理解了事件循环的工作原理后，一个至关重要的结论就呼之欲出了：**如果 JavaScript 主线程长时间不把控制权还给事件循环，整个应用就会"卡死"**。

考虑一个最简单的 Web 服务器：

```javascript
const http = require('http')

const server = http.createServer((req, res) => {
  if (req.url === '/compute') {
    // 一个非常耗时的同步计算
    let sum = 0
    for (let i = 0; i < 1e10; i++) {
      sum += i
    }
    res.end(`结果：${sum}`)
  } else {
    res.end('正常响应')
  }
})

server.listen(3000)
```

这个服务器有一个 `/compute` 路由。当用户访问这个路由时，Node.js 开始执行一个巨大的循环来计算累加和。

**在这期间会发生什么？**

答案是：**事件循环被完全阻塞了**。

- 事件循环现在卡在这个 `for` 循环里，无法进入任何阶段
- 新的 HTTP 请求到达了，但没有机会执行回调
- 定时器到时间了，但没有机会执行
- 文件读完了，回调也没有机会执行
- 服务器的其他所有用户都只能"干等着"

这就是阻塞事件循环的后果 —— **一个慢请求拖垮所有请求**。

### 如何避免阻塞事件循环？

**方案一：把 CPU 密集任务拆分成小块**

用 `setImmediate` 把大任务拆成多个小任务，每执行一小块就把控制权还给事件循环：

```javascript
function processLargeArray(array, callback) {
  let index = 0

  function processChunk() {
    const chunkSize = 100
    const end = Math.min(index + chunkSize, array.length)

    for (let i = index; i < end; i++) {
      // 处理这一小块数据
      array[i] = array[i] * 2
    }

    index = end

    if (index < array.length) {
      setImmediate(processChunk) // 让出控制权
    } else {
      callback(array)
    }
  }

  processChunk()
}

// 使用
const bigArray = new Array(10000000).fill(1)
processLargeArray(bigArray, (result) => {
  console.log('处理完成，数组长度：', result.length)
})
```

> [!note] setImmediate 让出控制权
> 通过在每处理 100 个元素后调用 `setImmediate`，我们把后续的处理推迟到 check 阶段。在这期间，事件循环可以处理其他用户的请求、执行定时器回调等。这是"协作式多任务"的一种实现。

**方案二：使用 Worker Threads（工作线程）**

对于真正的 CPU 密集型任务（视频编码、图像处理、大数据分析），最合适的方案是把任务分发给独立的工作线程：

```javascript
// worker.js
const { parentPort } = require('worker_threads')

parentPort.on('message', (data) => {
  let sum = 0
  for (let i = 0; i < data.iterations; i++) {
    sum += i
  }
  parentPort.postMessage(sum)
})
```

```javascript
// main.js
const { Worker } = require('worker_threads')

const worker = new Worker('./worker.js')

worker.postMessage({ iterations: 1e10 })

worker.on('message', (result) => {
  console.log('计算结果：', result)
})

console.log('主线程继续处理其他请求...')
// 不会阻塞！主线程可以继续接受新请求
```

Worker Threads 是 Node.js 提供的真正的多线程方案，适合处理 CPU 密集型任务。但它的使用场景相对特定 —— 对于大多数 Web 应用，**先确保你的代码不会无意中阻塞事件循环**，比引入工作线程更重要。

> [!warning] 阻塞事件循环的"隐形杀手"
> 不止是 `for` 循环会阻塞事件循环。以下操作都可能成为"隐形杀手"：
> - JSON.parse 一个巨大的 JSON 字符串
> - 正则表达式回溯导致灾难性的慢匹配
> - 同步的 `fs.readFileSync()`、`crypto.pbkdf2Sync()` 等
> - 密集的字符串操作（拼接、正则替换、加密）
>
> 在不必要的时候，**永远使用异步版本**的 API。

---

## 本章小结

- **事件循环**是 Node.js 异步能力的核心调度机制，由 libuv 库实现。它像餐厅里的传菜转盘，协调着各种任务的执行时机。
- 事件循环每轮依次走过六个阶段，但对业务开发最重要的是三个：**timers**（定时器回调）、**poll**（I/O 回调）、**check**（setImmediate 回调）。
- **微任务队列**（`process.nextTick` 和 Promise）不属于任何阶段，在每个阶段切换的间隙被清空。`process.nextTick` 的优先级高于 Promise 微任务。
- 在 I/O 回调中，`setImmediate` 永远先于 `setTimeout(0)` 执行。但在主模块中，两者的顺序不确定。
- **线程池**（默认 4 线程）负责处理文件系统、密码哈希等阻塞操作。网络 I/O 不走线程池，由操作系统内核直接处理。
- 长时间占用主线程会**阻塞事件循环**，导致整个应用无法响应。应该用 `setImmediate` 拆分大任务，或用 Worker Threads 处理 CPU 密集型工作。

---

## 下一章预告

这一章我们深入 Node.js 的"心脏"，理解了事件循环的工作机制。你可能已经注意到，我们频繁提到了一个模块：`http`。下一章我们就来正式学习 **用 Node.js 构建 Web 服务** —— 从最简单的 HTTP 服务器开始，逐步掌握路由、请求处理、中间件等核心概念。准备好写出你的第一个后端服务了吗？


---

理解了事件循环，你就真正理解了 Node.js 的"心脏"。现在，让我们用最主流的方式——构建 Web 服务——把这个能力发挥出来。

# 第七章：网络编程与 Express 框架入门

在之前六章里，你学会了读写文件、操作路径、理解异步编程和事件循环。现在你已经有能力写一个运行在命令行中的程序了。但 Node.js 最主流的用途不是写 CLI 工具，而是 **构建 Web 服务** —— 也就是别人可以通过浏览器或手机 App 来访问你的程序。

这一章会带你从零开始搭建一个 Web 服务器。我们会先使用 Node.js 内置的 `http` 模块手写一个原始服务器，体会一下"处理 HTTP 请求"到底是怎么回事。然后你会发现自己处理路由（分发请求）有多麻烦，这时我们再来引入 Express 这个框架，看看它是怎么让我们的生活变得轻松的。

> [!note] 这一章你会学到什么
> 学完本章后，你就能用 Express 搭建一个真实可用的 Web 服务，理解路由、中间件、请求/响应处理的核心概念。即使你从没用过任何 Web 框架，也不需要担心 —— 我们会从最底层一步步来。

---

## 7.1 从 http 模块开始：你的第一个 Web 服务器

在你的项目目录中创建一个新文件 `server-raw.js`，写入以下代码：

```javascript
const http = require('http');

const server = http.createServer((req, res) => {
  res.end('Hello, World!');
});

server.listen(3000, () => {
  console.log('服务器已启动：http://localhost:3000');
});
```

现在在终端运行：

```bash
node server-raw.js
```

你会在控制台看到"服务器已启动"的提示。打开浏览器，访问 `http://localhost:3000`，你会看到页面上显示 **Hello, World!**。

> [!note] localhost:3000 是什么意思
> - **localhost** 表示"本机"—— 你的程序只接受你自己电脑发出的请求，别人访问不到。
> - **3000** 是端口号，可以理解为"门牌号"。一台服务器上可以有多个程序同时运行，通过不同的端口来区分。3000 是开发中最常用的端口号之一。
> - 合在一起，`http://localhost:3000` 就是"访问本机上 3000 号门的那扇门"。

> [!tip] 端口被占用了怎么办？
> 如果运行时报错 `listen EADDRINUSE :::3000`，表示 3000 端口正在被其他程序占用。换成其他数字试试，比如 3001、3002、8080 都可以。改一下 `server.listen` 的第一个参数就行。

恭喜你 —— 你刚刚写出了你的第一个 Web 服务器！虽然只有几行代码，但它的意义不小。当你在浏览器中输入地址并按下回车时，实际发生的事情是：

```
浏览器 → 发送 HTTP 请求 → 你的 Node.js 程序
                                    ↓
浏览器 ← 收到 "Hello, World!" ← 你的程序返回响应
```

### 理解 req 和 res

`http.createServer` 的回调函数接收两个参数：`req` 和 `res`。

- **`req`（Request）**：代表**请求**对象，包含了浏览器发来的所有信息 —— 比如请求的网址（URL）、请求方法（GET/POST/等）、请求头（headers）等。
- **`res`（Response）**：代表**响应**对象，用来设置返回给浏览器的数据 —— 比如状态码、响应头、正文内容。

现在我们来改造一下上面的代码，看看 `req` 里到底有什么：

```javascript
const http = require('http');

const server = http.createServer((req, res) => {
  // 打印请求信息
  console.log('=== 收到新请求 ===');
  console.log('请求方法:', req.method);
  console.log('请求地址:', req.url);
  console.log('请求头:', JSON.stringify(req.headers, null, 2));

  res.end('看你的终端输出，那里打印了请求信息！');
});

server.listen(3000, () => {
  console.log('服务器已启动：http://localhost:3000');
});
```

重启服务器（按 Ctrl+C 停掉再重新运行），然后访问 `http://localhost:3000/hello`，你会看到终端中打印出的请求信息：

```
=== 收到新请求 ===
请求方法: GET
请求地址: /hello
请求头: {
  "host": "localhost:3000",
  "user-agent": "Mozilla/5.0 ...",
  ...
}
```

> [!note] 核心理解
> `req` 对象是你**收到的信息**，`res` 对象是你**返回的内容**。所有的 Web 编程本质上就是：**读取 `req` 中的信息 -> 决定做什么 -> 通过 `res` 返回结果**。

---

## 7.2 自己处理路由：体会"手动"的痛苦

现在假设你的服务器需要提供两个不同的页面：
- 访问 `/` 时显示 "欢迎来到首页"
- 访问 `/about` 时显示 "关于我们"

用 `http` 模块怎么做？你需要手动解析 `req.url`，然后通过 `if/else` 来分发：

```javascript
const http = require('http');

const server = http.createServer((req, res) => {
  const url = req.url;
  const method = req.method;

  if (url === '/') {
    res.end('欢迎来到首页');
  } else if (url === '/about') {
    res.end('关于我们');
  } else {
    res.statusCode = 404;
    res.end('404 - 页面不存在');
  }
});

server.listen(3000, () => {
  console.log('服务器已启动：http://localhost:3000');
});
```

访问 `http://localhost:3000/` 会显示"欢迎来到首页"，`http://localhost:3000/about` 会显示"关于我们"。其他的路径则返回 404。

> [!note] 状态码（Status Code）
> 上面的 `res.statusCode = 404` 就是在设置 HTTP 状态码。状态码是服务器告诉浏览器"本次请求的结果如何"的一种标准方式：
>
> | 状态码 | 含义 | 说明 |
> |--------|------|------|
> | 200 | OK | 请求成功 |
> | 201 | Created | 创建成功（常用于 POST） |
> | 301/302 | Redirect | 重定向 |
> | 400 | Bad Request | 客户端请求有误 |
> | 401 | Unauthorized | 未认证 |
> | 403 | Forbidden | 无权限 |
> | 404 | Not Found | 资源不存在 |
> | 500 | Internal Server Error | 服务器内部错误 |

### 中文乱码问题

如果你尝试让上面的服务器返回中文，比如把首页改成"欢迎来到首页"，你可能会在浏览器中看到乱码，像这样：`æ¬¢è¿æ¥å°é¦é¡µ`。

这是因为浏览器不知道服务器返回的内容用什么编码。解决方法是在响应头中告诉浏览器："我返回的内容用的是 UTF-8 编码"：

```javascript
res.setHeader('Content-Type', 'text/plain; charset=utf-8');
```

改到完整代码中：

```javascript
const http = require('http');

const server = http.createServer((req, res) => {
  const url = req.url;

  // 设置编码，解决中文乱码
  res.setHeader('Content-Type', 'text/plain; charset=utf-8');

  if (url === '/') {
    res.end('欢迎来到首页');
  } else if (url === '/about') {
    res.end('关于我们');
  } else {
    res.statusCode = 404;
    res.end('404 - 页面不存在');
  }
});

server.listen(3000, () => {
  console.log('服务器已启动：http://localhost:3000');
});
```

> [!warning] 初学者最容易忘的两件事
> 1. **忘记设置 `charset=utf-8`**：返回中文时就会乱码。
> 2. **忘记设置状态码**：如果你不设置 `res.statusCode`，默认是 200。这意味着即使返回"页面不存在"，状态码还是 200，浏览器会认为请求成功。

现在，想象一下你的服务器需要处理 20 个、50 个不同的路由，还要区分 GET 和 POST 请求、提取 URL 参数、处理 JSON 请求体…… 手动解析一切很快就会变得难以维护。这正是 Express 框架要解决的问题。

---

## 7.3 Express 登场：3 行代码替代手写路由

Express 是 Node.js 生态中最流行的 Web 框架。它基于 `http` 模块构建，但提供了更高层次的抽象，让你**不用手动解析 URL、不用手动设置 `Content-Type`、不用手写一大串 if/else**。

> [!note] 框架 vs 原生
> 用 `http` 模块写服务器，就像用砖头和水泥盖房子 —— 你可以做任何事，但每件事都很费劲。
> 用 Express 写服务器，就像用预制板搭房子 —— 框架帮你处理了 80% 的重复工作，你把精力放在业务逻辑上。
> 先学 `http` 模块不是为了让你一直用它，而是为了让你理解 Express 在背后帮你做了什么。

### 安装 Express

在你的项目目录中打开终端，运行：

```bash
npm init -y     # 初始化项目（如果还没做过）
npm install express
```

> [!tip] 装包的时候报错了？
> 确保你已经在项目目录中创建了 `package.json`（`npm init -y` 会帮你创建）。如果网络慢，可以试试国内的淘宝镜像：`npm config set registry https://registry.npmmirror.com`。

### 第一个 Express 服务器

安装完成后，创建文件 `server-express.js`：

```javascript
const express = require('express');
const app = express();

// 定义路由
app.get('/', (req, res) => {
  res.send('欢迎来到首页');
});

app.get('/about', (req, res) => {
  res.send('关于我们');
});

// 启动服务器
app.listen(3000, () => {
  console.log('Express 服务器已启动：http://localhost:3000');
});
```

运行：

```bash
node server-express.js
```

现在访问 `http://localhost:3000/` 和 `http://localhost:3000/about`，效果和之前手写的 http 模块版本一样，但是代码清晰多了。注意到几个关键变化：

1. **不需要手动设置 `Content-Type`**：`res.send()` 会自动判断类型并设置编码，中文不会乱码。
2. **不需要手写 if/else 路由分发**：`app.get('/about', ...)` 一眼就能看出哪个 URL 对应什么处理逻辑。
3. **404 自动处理**：访问不存在的路径，Express 会自动返回 404。

> [!note] Express 的 API 风格
> `app.get()` 中的 `get` 对应 HTTP 的 GET 请求方法。同理还有 `app.post()`、`app.put()`、`app.delete()` 等，分别对应不同的请求方法。这种把"请求方法 + 路径"组合成函数调用的方式，叫**路由定义（Route Definition）**。

---

## 7.4 路由详解：GET、POST 与参数

### 基本的 GET 和 POST 路由

新建文件 `server-routes.js`：

```javascript
const express = require('express');
const app = express();

// 为了让 POST 请求能解析 JSON 请求体
app.use(express.json());

// GET 请求
app.get('/users', (req, res) => {
  res.send('返回所有用户列表');
});

// POST 请求：创建新用户
app.post('/users', (req, res) => {
  // req.body 里就是客户端发来的 JSON 数据
  console.log('收到新用户数据:', req.body);
  res.status(201).send('用户创建成功');
});

app.listen(3000, () => {
  console.log('服务器已启动：http://localhost:3000');
});
```

现在你的服务器不仅能响应 GET 请求了，还能处理 POST 请求 —— 也就是客户端向服务器"提交数据"的请求。你可以用下面的命令测试（打开一个新的终端窗口）：

```bash
# 测试 GET
curl http://localhost:3000/users

# 测试 POST
curl -X POST http://localhost:3000/users \
  -H "Content-Type: application/json" \
  -d '{"name": "张三", "age": 25}'
```

> [!note] 什么是 POST 请求
> 在浏览器地址栏输入网址回车，发送的是 GET 请求 —— 用来**获取**数据。而 POST 请求用来**提交**数据 —— 比如注册时填写表单、发布一条评论。POST 请求的数据放在请求体（body）中，浏览器地址栏看不到。

### 路由参数（URL 参数）

很多时候路径中有一部分是动态的，比如"获取 ID 为 123 的用户信息"，URL 可能是 `/users/123`。Express 用冒号语法来表示这类动态参数：

```javascript
// :id 是一个动态参数
app.get('/users/:id', (req, res) => {
  const userId = req.params.id;
  res.send(`你查询的用户 ID 是：${userId}`);
});
```

访问 `http://localhost:3000/users/42`，你会看到"你查询的用户 ID 是：42"。

如果有多个参数，也是类似的写法：

```javascript
// 匹配 /posts/123/comments/456
app.get('/posts/:postId/comments/:commentId', (req, res) => {
  console.log(req.params.postId);   // 123
  console.log(req.params.commentId); // 456
  res.send('参数已收到');
});
```

### 查询参数（Query String）

URL 中 `?` 后面的部分叫查询参数，比如 `/search?q=node&page=1`。Express 会自动解析这些参数，放在 `req.query` 中：

```javascript
app.get('/search', (req, res) => {
  const keyword = req.query.q;
  const page = req.query.page || 1;

  res.send(`搜索关键词：${keyword}，第 ${page} 页`);
});
```

访问 `http://localhost:3000/search?q=express&page=2`，你会看到"搜索关键词：express，第 2 页"。

> [!tip] 路由参数 vs 查询参数
> - **路由参数**（`req.params`）：用于标识**特定的资源**，比如用户的 ID、文章的编号。写死在路径里：`/users/:id`。
> - **查询参数**（`req.query`）：用于**筛选或排序**，比如搜索关键词、页码。跟在 `?` 后面：`?q=xxx&page=1`。
> - 两者的区别不是技术上的，而是**约定上的**。都合理，但遵循约定能让你的 API 更容易被其他人理解。

---

## 7.5 中间件：流水线上的工位

中间件（Middleware）是 Express 中最重要、也最容易被初学者理解的概念。我们用一个生活类比来说明。

### 流水线类比

想象你开了一家汉堡店。做汉堡的过程是一条流水线：

```
接收订单 → 烤面包 → 加肉饼 → 加蔬菜 → 包装 → 交给顾客
```

流水线上的每一个工位，都是一个"中间件"。每个工位做三件事：
1. **接收**上一道工序送来的半成品。
2. **处理**它负责的那部分（烤面包、加肉饼等）。
3. **传递给**下一道工序，或者直接**结束**流程（交给顾客）。

在 Express 中完全一样。一个 HTTP 请求到达服务器后，会依次经过一系列中间件函数。每个中间件可以：
- 修改 `req` 或 `res` 对象（比如解析请求体、添加安全头）
- 结束请求-响应周期（返回响应给客户端）
- 调用 `next()` 把控制权交给下一个中间件

> [!note] 一句话理解中间件
> 中间件就是**请求到达你的路由处理函数之前，需要经过的一系列预处理步骤**。

### 写一个自定义中间件

```javascript
const express = require('express');
const app = express();

// 这是一个简单的日志中间件
// 它记录了每个请求的方法和 URL，然后调用 next() 放行
app.use((req, res, next) => {
  console.log(`[${new Date().toISOString()}] ${req.method} ${req.url}`);
  next();  // 不调用 next()，请求就会卡在这里！
});

// 这是一个计时中间件
app.use((req, res, next) => {
  req.startTime = Date.now();  // 在 req 上添加自定义属性
  next();
});

app.get('/', (req, res) => {
  const elapsed = Date.now() - req.startTime;
  res.send(`首页（处理耗时：${elapsed}ms）`);
});

app.listen(3000, () => {
  console.log('服务器已启动：http://localhost:3000');
});
```

当访问 `/` 时，请求的流转过程是：

```
请求到达
    ↓
日志中间件（打印日志）→ 调用 next()
    ↓
计时中间件（记录开始时间）→ 调用 next()
    ↓
路由处理函数（处理请求，返回响应）
```

> [!warning] 不要忘记调用 next()！
> 如果你在中间件中既不调用 `next()` 也不返回响应（`res.send()`），请求就会"卡死"在那里，客户端会一直等待直到超时。这是初学中间件时最常见的 bug 之一。

### 中间件的执行顺序

中间件的注册顺序**极其重要**。中间件按照它们被 `app.use()` 注册的顺序依次执行。例如：

```javascript
// 错误示例：把路由写在中间件前面
app.get('/', (req, res) => {
  res.send('首页');
});

// 这个中间件永远不会被执行！
// 因为前面的路由已经结束了请求-响应周期
app.use((req, res, next) => {
  console.log('这行代码永远不会被打印');
  next();
});
```

正确的做法是：**把全局中间件放在路由定义之前，把错误处理中间件放在路由定义之后**。我们会在 7.7 节详细解释错误处理的顺序。

---

## 7.6 常用中间件

在实际开发中，你通常不需要自己写中间件 —— 社区已经提供了大量现成的中间件，你只需要 `npm install` 然后再 `app.use()` 一下就好。

下面介绍四个最常用的中间件。

### helmet —— 安全头

在 Web 开发中，有一些安全相关的 HTTP 响应头可以帮助防止常见攻击（比如 XSS、点击劫持）。手动设置这些头很麻烦，`helmet` 帮你一键搞定。

```bash
npm install helmet
```

```javascript
const helmet = require('helmet');
app.use(helmet());  // 自动设置多个安全相关的 HTTP 响应头
```

只需要这一行，你的服务器就会自动添加 `X-Content-Type-Options`、`X-Frame-Options` 等多个安全头。初学者可能一时半会儿看不懂这些头的作用，没关系 —— 记住"加 helmet 会让你的服务器更安全"就够了。

### cors —— 跨域配置

先解释一下什么是"跨域"。假设你写了一个前端页面运行在 `http://my-app.com`，这个页面想请求你的 API（运行在 `http://localhost:3000`）。浏览器的安全策略会阻止这种"从一个域名请求另一个域名"的行为 —— 这就是跨域问题。

```bash
npm install cors
```

```javascript
const cors = require('cors');
app.use(cors());  // 允许所有来源的跨域请求
```

> [!note] 开发阶段用默认配置就够了
> 上面这行代码允许所有来源的跨域请求，这在开发阶段完全没问题。上线时，你可能需要限制只允许你的前端域名访问：
> ```javascript
> app.use(cors({ origin: 'https://my-app.com' }));
> ```

### morgan —— 请求日志

`console.log` 打印的日志太粗糙了 —— 没有时间戳、没有状态码、没有响应时间。`morgan` 是一个专业的请求日志中间件：

```bash
npm install morgan
```

```javascript
const morgan = require('morgan');
app.use(morgan('dev'));  // 'dev' 是一种简洁的日志格式
```

现在每次收到请求，控制台会输出类似这样的信息：

```
GET /users 200 5.234 ms
GET /about 404 1.023 ms
POST /users 201 8.456 ms
```

一目了然：请求方法、路径、状态码、处理耗时。

### express.json —— 解析 JSON 请求体

你已经在 7.4 节的 POST 路由示例中见过它了。当客户端通过 POST 请求发送 JSON 数据时，数据以字符串形式存放在请求体中。`express.json()` 帮你把 JSON 字符串解析成 JavaScript 对象，挂载到 `req.body` 上：

```javascript
// limit 参数限制请求体大小，防止恶意的大请求
app.use(express.json({ limit: '1mb' }));
```

### 把它们组合起来

下面是一个使用了所有常用中间件的完整示例。这也将是你学习 Express 阶段最常用的"起手式"：

```javascript
const express = require('express');
const helmet = require('helmet');
const cors = require('cors');
const morgan = require('morgan');

const app = express();

// === 全局中间件（顺序重要） ===
app.use(helmet());              // 安全头
app.use(cors());                // 跨域
app.use(morgan('dev'));         // 日志
app.use(express.json({ limit: '1mb' }));  // JSON 解析

// === 路由 ===
app.get('/', (req, res) => {
  res.json({ message: '欢迎使用 API' });
});

// === 启动 ===
app.listen(3000, () => {
  console.log('服务器已启动：http://localhost:3000');
});
```

> [!tip] 开发阶段的"标配"起手式
> 以后你每次新建一个 Express 项目，都可以从上面这个模板开始。`helmet`、`cors`、`morgan`、`express.json()` 这四个中间件几乎适用于所有 Web API 项目。

---

## 7.7 错误处理

在实际项目中，很多操作都可能出错 —— 数据库连接失败、用户输入无效、文件不存在。如果每个路由都自己写 try/catch，代码会变得非常臃肿。一套好的错误处理机制，能帮你省去大量重复代码。

### 同步错误的处理 —— Express 自动搞定

对于同步代码中抛出的错误，Express 会自动捕获并返回 500 响应：

```javascript
app.get('/error', (req, res) => {
  throw new Error('出错了！');
  // Express 会自动捕获这个错误，返回 500 状态码和错误信息
});
```

### 异步错误的处理 —— asyncHandler

但对于异步代码（async/await），情况就不一样了。看这个例子：

```javascript
app.get('/users/:id', async (req, res) => {
  const user = await findUserById(req.params.id);
  if (!user) {
    throw new Error('用户不存在');  // ❌ 这个错误 Express 捕获不到！
  }
  res.json(user);
});
```

在 `async` 函数中抛出的错误，如果不手动捕获，Express 无法处理 —— 服务器会悄无声息地挂掉（至少 Node.js 16 之前是这样）。

解决办法有两种。第一种是每个路由都包上 try/catch：

```javascript
app.get('/users/:id', async (req, res) => {
  try {
    const user = await findUserById(req.params.id);
    if (!user) {
      return res.status(404).json({ error: '用户不存在' });
    }
    res.json(user);
  } catch (err) {
    res.status(500).json({ error: '服务器内部错误' });
  }
});
```

但如果你有 20 个路由，每个都写一遍 try/catch，很烦人。更好的方案是写一个 **asyncHandler 包装器**：

```javascript
// 这个函数接收一个异步函数作为参数
// 它返回一个带有 try/catch 的新函数
const asyncHandler = (fn) => (req, res, next) => {
  Promise.resolve(fn(req, res, next)).catch(next);
};
```

使用方式：

```javascript
app.get('/users/:id', asyncHandler(async (req, res) => {
  const user = await findUserById(req.params.id);
  if (!user) {
    // 这里 throw 的错误会被 catch 捕获，然后传递给 next()
    throw new Error('用户不存在');
  }
  res.json(user);
}));
```

> [!note] asyncHandler 的作用
> 它本质上就是把"每个异步路由都要写 try/catch"这件事集中处理了。你只需用 `asyncHandler` 包裹路由处理函数，所有异常都会被自动传递给 Express 的错误处理机制。

### 全局错误处理中间件

前面说到，中间件是按照注册顺序执行的。错误处理中间件是一种**特殊的中间件**，它有**4 个参数**（而不是普通中间件的 3 个）：

```javascript
// 注意：必须写 4 个参数，Express 才能识别这是错误处理中间件
app.use((err, req, res, next) => {
  console.error('发生错误:', err.message);
  res.status(err.statusCode || 500).json({
    error: err.message || '服务器内部错误'
  });
});
```

这个中间件要**注册在所有路由之后**。当任何路由或中间件调用 `next(err)` 时（或者被 asyncHandler 自动传入错误时），Express 会跳过所有普通中间件，直接跳到错误处理中间件：

```
请求进入
    ↓
安全头中间件（helmet）—— 通过 next()
    ↓
日志中间件（morgan）—— 通过 next()
    ↓
JSON 解析中间件 —— 通过 next()
    ↓
路由处理函数 —— 调用 next(err)
    ↓
       ↙ 跳过后续所有普通中间件
错误处理中间件（返回统一的错误响应）
```

### 完整的错误处理示例

```javascript
const express = require('express');
const morgan = require('morgan');

const app = express();

// 全局中间件
app.use(morgan('dev'));
app.use(express.json());

// asyncHandler 包装器
const asyncHandler = (fn) => (req, res, next) => {
  Promise.resolve(fn(req, res, next)).catch(next);
};

// 模拟一个异步数据库查询
async function findUserById(id) {
  if (id === '999') {
    throw new Error('数据库连接失败');
  }
  if (id !== '1') {
    return null;
  }
  return { id: 1, name: '张三' };
}

// 使用 asyncHandler 包装的路由
app.get('/users/:id', asyncHandler(async (req, res) => {
  const user = await findUserById(req.params.id);
  if (!user) {
    // 手动抛出一个错误，asyncHandler 会捕获并传给 next()
    const err = new Error('用户不存在');
    err.statusCode = 404;
    throw err;
  }
  res.json(user);
}));

// 全局错误处理中间件（必须在所有路由之后）
app.use((err, req, res, next) => {
  console.error(`[错误] ${err.message}`);
  res.status(err.statusCode || 500).json({
    error: err.message || '服务器内部错误'
  });
});

app.listen(3000, () => {
  console.log('服务器已启动：http://localhost:3000');
});
```

试试看：
- `GET http://localhost:3000/users/1` —— 返回用户数据
- `GET http://localhost:3000/users/2` —— 返回 404，提示"用户不存在"
- `GET http://localhost:3000/users/999` —— 返回 500，提示"数据库连接失败"

> [!warning] 错误处理中间件必须写在最后
> 如果错误处理中间件注册在路由之前，它根本捕获不到任何错误 —— 因为请求还没走到错误处理，先被路由处理并返回了。记住：**普通中间件在先，路由在中间，错误处理在最后**。

---

## 7.8 项目分层结构建议

当你的项目只有三五个路由时，把所有代码写在一个文件里完全没问题。但当项目增长到几十个路由、几十个处理函数时，挤在一个文件里就变成了一场噩梦。

社区经过多年实践，总结出了一套推荐的分层结构。这套结构的核心理念是**分离关注点** —— 每一层只负责自己该做的事。

```
src/
  routes/         — 路由定义（薄层，只做 URL 和方法的分发）
  controllers/    — 请求/响应逻辑编排（接收参数、调用服务、返回响应）
  services/       — 业务逻辑（纯粹的代码逻辑，不关心 HTTP）
  middleware/     — 可复用中间件（认证、日志、错误处理等）
  models/         — 数据模型/schema（如数据库表结构定义）
  config/         — 环境配置
  utils/          — 工具函数
```

我们来逐层看一下，每层大概长什么样。

### routes —— 只做分发

```javascript
// src/routes/userRoutes.js
const express = require('express');
const router = express.Router();
const userController = require('../controllers/userController');

// 路由层只负责"什么方法和路径，交给哪个控制器"
router.get('/', userController.getAllUsers);
router.get('/:id', userController.getUserById);
router.post('/', userController.createUser);

module.exports = router;
```

### controllers —— 协调请求和响应

```javascript
// src/controllers/userController.js
const userService = require('../services/userService');

const getAllUsers = async (req, res) => {
  const users = await userService.listUsers();
  res.json(users);
};

const getUserById = async (req, res) => {
  const user = await userService.findUser(req.params.id);
  if (!user) {
    return res.status(404).json({ error: '用户不存在' });
  }
  res.json(user);
};

const createUser = async (req, res) => {
  const newUser = await userService.createUser(req.body);
  res.status(201).json(newUser);
};

module.exports = { getAllUsers, getUserById, createUser };
```

### services —— 纯粹的"业务逻辑"

```javascript
// src/services/userService.js
// 这一层不关心 req 和 res，只关心数据和业务规则

const users = [];  // 假设这是一个数据库

const listUsers = async () => {
  return users;
};

const findUser = async (id) => {
  return users.find(u => u.id === id) || null;
};

const createUser = async (data) => {
  const newUser = { id: users.length + 1, ...data };
  users.push(newUser);
  return newUser;
};

module.exports = { listUsers, findUser, createUser };
```

### middleware —— 可复用的中间件

```javascript
// src/middleware/errorHandler.js
const errorHandler = (err, req, res, next) => {
  console.error(`[错误] ${err.message}`);
  res.status(err.statusCode || 500).json({
    error: err.message || '服务器内部错误'
  });
};

module.exports = errorHandler;
```

### 在入口文件中组装

```javascript
// src/index.js (入口文件)
const express = require('express');
const helmet = require('helmet');
const cors = require('cors');
const morgan = require('morgan');
const userRoutes = require('./routes/userRoutes');
const errorHandler = require('./middleware/errorHandler');

const app = express();

// 全局中间件
app.use(helmet());
app.use(cors());
app.use(morgan('dev'));
app.use(express.json());

// 路由
app.use('/users', userRoutes);

// 错误处理（必须在所有路由之后）
app.use(errorHandler);

app.listen(3000, () => {
  console.log('服务器已启动：http://localhost:3000');
});
```

> [!note] 为什么这样分层？
> - **routes** 只做分发 → 当你想改 URL 结构时，只改这一个地方。
> - **controllers** 只处理请求/响应 → 当你需要从 JSON 改成 XML 时，只改这里。
> - **services** 只做业务逻辑 → 当你换数据库时，业务代码不用动。
> - 每一层的修改**不会影响其他层**，项目越大，分层的好处越明显。

---

## 7.9 输入验证：别相信用户发来的数据

假设你的 API 接收一个 POST 请求来创建用户，期望的格式是：

```json
{
  "name": "张三",
  "email": "zhangsan@example.com",
  "age": 25
}
```

但用户可能发来什么？可能是 `{ "name": "" }`（空名字）、`{ "age": "不是数字" }`（类型不对）、甚至是一大堆你不需要的字段。如果不对输入做验证，这些脏数据就会一路流进你的业务逻辑和数据库，造成各种奇怪的问题。

> [!warning] 永远不要信任用户输入
> 这是 Web 开发的第一条安全铁律。不管是你的前端页面、手机 App、还是别人的程序发来的请求，你都必须假设数据可能是恶意或无效的。

### 使用 Zod 做验证

Zod 是一个流行的输入验证库。它的使用方式非常直观：

```bash
npm install zod
```

```javascript
const { z } = require('zod');

// 定义一个"用户创建"的数据模式（schema）
const createUserSchema = z.object({
  name: z.string().min(1, '名字不能为空'),
  email: z.string().email('邮箱格式不正确'),
  age: z.number().int().positive('年龄必须是正整数').optional(),
});
```

然后在控制器中使用：

```javascript
// src/controllers/userController.js
const { z } = require('zod');
const userService = require('../services/userService');

const createUserSchema = z.object({
  name: z.string().min(1, '名字不能为空'),
  email: z.string().email('邮箱格式不正确'),
  age: z.number().int().positive().optional(),
});

const createUser = async (req, res) => {
  try {
    // 解析并验证 —— 如果不符合 schema，会抛出 ZodError
    const validData = createUserSchema.parse(req.body);
    const newUser = await userService.createUser(validData);
    res.status(201).json(newUser);
  } catch (err) {
    if (err instanceof z.ZodError) {
      return res.status(400).json({
        error: '输入验证失败',
        details: err.errors.map(e => ({
          field: e.path.join('.'),
          message: e.message
        }))
      });
    }
    throw err;
  }
};
```

如果用户发来无效数据，响应会是这样的：

```json
{
  "error": "输入验证失败",
  "details": [
    { "field": "name", "message": "名字不能为空" },
    { "field": "email", "message": "邮箱格式不正确" }
  ]
}
```

> [!tip] Zod 还是 Joi？
> 社区中有两个主流的验证库：**Zod** 和 **Joi**。两者功能类似，但 Zod 的语法更接近 TypeScript 的类型系统，如果你的项目将来迁移到 TypeScript，Zod 会非常自然。对于纯 JavaScript 项目，两者都可以，选择你觉得顺手的。

---

## 本章小结

- Node.js 内置的 **`http` 模块**可以创建原始 Web 服务器。`req` 是请求对象，`res` 是响应对象，所有 Web 编程都围绕这二者展开。
- 手动用 `http` 模块做路由分发（if/else 判断 URL）非常繁琐。**Express 框架**在此基础上提供了优雅的路由定义方式，让代码更清晰。
- Express 路由支持 **GET/POST** 等方法，**路由参数**（`/users/:id` 中的 `:id`）和**查询参数**（`?key=value`）通过 `req.params` 和 `req.query` 获取。
- **中间件**是 Express 的核心机制，可以理解为"流水线上的工位"。中间件通过 `next()` 传递控制权，**注册顺序决定执行顺序**。
- 常用中间件包括：**helmet**（安全头）、**cors**（跨域配置）、**morgan**（请求日志）、**express.json**（JSON 解析）。
- 异步路由需要用 **asyncHandler 包装器**来捕获异常。**错误处理中间件**（4 个参数的 `(err, req, res, next)`）必须注册在所有路由之后。
- 项目推荐分层结构：`routes` 做分发、`controllers` 做协调、`services` 做业务逻辑、`middleware` 放可复用中间件 —— 各层职责分明，便于维护。
- **永远不要信任用户输入**。使用 Zod 或 Joi 等验证库，在数据进入业务逻辑之前进行验证。

---

## 下一章预告

你的服务器已经能跑起来了，但在实际开发中还有很多"杂活"需要处理 —— 代码改了要手动重启太麻烦、密码和密钥直接写在代码里不安全、日志乱糟糟的看不清楚…… 下一章会带你解决这些实际问题，内容包括 `nodemon` 自动重启、环境变量管理、结构化日志、以及一些安全方面的基础配置。


---

你的 Express 服务器已经能处理各种路由和中间件了。但在真实的开发中，光让程序"能跑"是不够的——还需要让它"跑得稳"。环境配置、错误处理、安全、日志...这些专业工具会让你从新手变成合格的开发者。

# 第八章：环境配置、调试与最佳实践 —— 从"能跑"到"专业"

恭喜你走到了这里。前七章我们走了一条很长的路：从 Node.js 是什么，到模块系统、异步编程、文件操作，再到用 Express 构建 API。如果你一路跟下来并动手写了代码，现在的你已经能用 Node.js 写一个能用的 Web 服务了。

但是，"能用"和"专业"之间还有一段距离。真实开发中，你不会每改一行代码就手动重启一次程序，不会把数据库密码直接写在代码里，也不会在出问题时只用 `console.log` 到处插桩调试。

本章的目标就是帮你跨越这段距离。我们会覆盖一个专业 Node.js 开发者日常用到的那套工具链和最佳实践。学完本章，你的开发体验会从"磕磕绊绊"变成"行云流水"。

---

## 8.1 开发效率工具 —— 告别手动重启

### 8.1.1 nodemon —— 最流行的自动重启工具

在之前的学习中，你每次修改代码后都要手动执行 `node index.js` 来重启程序。一次两次还好，一天几十次就让人崩溃了。

**nodemon** 就是用来解决这个问题的：它监听项目文件的变化，一旦检测到文件被修改，就自动重启 Node 进程。

安装非常简单（作为开发依赖）：

```bash
npm install -D nodemon
```

> [!tip] `-D` 是什么意思？
> `-D` 是 `--save-dev` 的简写，表示"开发依赖"（devDependencies）。这意味着这个包只在开发阶段使用，生产环境部署时不会被安装。像 nodemon、测试框架、代码格式化工具都属于这一类。

安装后，在 `package.json` 中添加一个 `dev` 脚本：

```json
{
  "scripts": {
    "start": "node index.js",
    "dev": "nodemon index.js"
  }
}
```

然后只需要运行：

```bash
npm run dev
```

每次修改代码并保存后，nodemon 会自动重启程序。你会看到这样的输出：

```
[nodemon] 3.1.0
[nodemon] to restart at any time, enter `rs`
[nodemon] watching path(s): *.*
[nodemon] watching extensions: js,mjs,cjs,json
[nodemon] starting `node index.js`
服务器已启动: http://localhost:3000
[nodemon] restarting due to changes...
[nodemon] starting `node index.js`
```

> [!note] nodemon 的原理
> nodemon 的核心机制很简单：它用 `fs.watch`（来自第五章学过的 fs 模块）监听文件系统的变更事件。一旦有文件被修改、创建或删除，它就杀掉当前的 Node 进程，再启动一个新的。你不需要关心底层细节，只需要知道：**有了 nodemon，改代码后只管保存，剩下的它帮你做**。

### 8.1.2 node --watch —— Node.js 内置的替代方案

从 Node.js 18 开始，Node.js 内置了一个轻量的文件监听模式，不需要安装任何第三方包：

```bash
node --watch index.js
```

效果和 nodemon 类似：修改文件后自动重启。它的优势是零依赖、零配置。那为什么大部分人还在用 nodemon？

| 对比维度 | `node --watch` | nodemon |
|----------|---------------|---------|
| 安装 | 内置，无需安装 | 需要 `npm install -D` |
| 配置 | 无配置选项 | 支持忽略文件、延迟重启、自定义监视频率 |
| 稳定性 | 较新功能，早期版本有 bug | 非常成熟稳定 |
| 额外功能 | 仅自动重启 | 支持非 Node 程序、自定义命令等 |

> [!tip] 初学者推荐用 nodemon
> 对于刚起步的你，推荐用 nodemon。它更稳定、更灵活，社区中也更主流。`node --watch` 可以作为备选方案 —— 当你临时在一个没有安装 nodemon 的环境里，它能救急。

---

## 8.2 环境变量管理 —— 不要把密码写在代码里

### 8.2.1 为什么要用环境变量？

想一想你之前写代码的方式：数据库连接地址、API 密钥、端口号，是不是直接写在代码里？

```javascript
// 这样写有什么问题？
const PORT = 3000
const DB_URL = 'mongodb://localhost:27017/myapp'
const API_KEY = 'sk-123456789'
```

这段代码有三个问题：

1. **不安全**：如果你把代码提交到 GitHub，API 密钥就暴露给全世界了。
2. **不可移植**：你在本地用的数据库地址、端口，和部署到服务器上用的不一样。每次切换环境都要改代码。
3. **难以协作**：团队里每个人的本地配置可能不同，但代码中只有一个值。

**环境变量（Environment Variables）** 就是解决这些问题的标准方案。它把配置从代码中抽离出来，放到运行环境里。代码读取变量，而变量的值由运行环境决定。

### 8.2.2 dotenv 和 .env 文件

[dotenv](https://www.npmjs.com/package/dotenv) 是最流行的环境变量管理工具，它从一个 `.env` 文件中读取配置，注入到 `process.env` 中。

安装：

```bash
npm install dotenv
```

在项目根目录创建一个 `.env` 文件：

```bash
# .env 文件
PORT=3000
DB_URL=mongodb://localhost:27017/myapp
API_KEY=sk-123456789
NODE_ENV=development
```

然后在你的入口文件（如 `index.js`）的最顶部加载：

```javascript
import 'dotenv/config'

// 现在可以读取环境变量了
const port = process.env.PORT || 3000
const dbUrl = process.env.DB_URL
const apiKey = process.env.API_KEY

console.log(`服务器将在端口 ${port} 启动`)
```

> [!note] process.env 是什么？
> `process.env` 是一个对象，包含当前 shell 中设置的所有环境变量。你可以在终端中设置它（如 `PORT=4000 node index.js`），也可以通过 dotenv 从文件加载。`||` 运算符提供了默认值 —— 如果 `process.env.PORT` 不存在，就用 `3000`。

### 8.2.3 .env.example 和 .gitignore

`.env` 文件**不应该提交到 Git 仓库**，因为它可能包含密钥等敏感信息。但你的队友需要知道这个项目需要哪些环境变量。解决方案是创建一个 `.env.example` 文件：

```bash
# .env.example —— 提交到 Git，只包含变量名和占位值，不含真实密钥
PORT=3000
DB_URL=your-database-url-here
API_KEY=your-api-key-here
NODE_ENV=development
```

同时确保 `.env` 被 `.gitignore` 忽略：

```gitignore
# .gitignore
.env
.env.local
node_modules/
```

> [!warning] 忘记忽略 .env 的后果
> 如果在网上搜索 "accidentally committed .env"，你会看到无数开发者把 AWS 密钥、数据库密码暴露到 GitHub 的故事。有人因此收到数千美元的账单。**启动新项目后的第一件事，就是把 `.env` 加到 `.gitignore` 里。**

**最佳实践清单**：

1. 真实密钥放在 `.env`（已忽略，不提交）
2. 变量模板放在 `.env.example`（提交到 Git）
3. 项目文档中注明"复制 `.env.example` 为 `.env` 并填写真实值"
4. 在 `index.js` 顶部尽早加载 dotenv

---

## 8.3 npm 常用命令速查表

在之前的章节中你已经用过一些 npm 命令了。这里把它们汇总成一张速查表，方便你随时查阅。

| 命令 | 用途 | 示例 |
|------|------|------|
| `npm init -y` | 快速初始化项目，生成 `package.json` | `npm init -y` |
| `npm install <包名>` | 安装包并记录到 `dependencies` | `npm install express` |
| `npm install -D <包名>` | 安装开发依赖 | `npm install -D nodemon` |
| `npm install` | 安装 `package.json` 中所有依赖 | `npm install` |
| `npm ci` | 根据 lockfile 精确安装（CI 环境推荐） | `npm ci` |
| `npm uninstall <包名>` | 卸载包 | `npm uninstall express` |
| `npm update` | 更新包到符合 semver 的最新版本 | `npm update` |
| `npm run <脚本名>` | 运行 `scripts` 中的命令 | `npm run dev` |
| `npm test` | 运行测试脚本（等同于 `npm run test`） | `npm test` |
| `npm list --depth=0` | 列出顶层依赖 | `npm list --depth=0` |
| `npm outdated` | 检查哪些包有新版本 | `npm outdated` |
| `npm audit` | 检查依赖中的安全漏洞 | `npm audit fix` |
| `npx <包名>` | 临时执行一个包而不安装 | `npx create-react-app my-app` |

> [!note] npm ci vs npm install
> `npm ci` 是 `npm install` 的"更严格"版本。它完全按照 `package-lock.json` 安装，不会修改 lockfile。这确保了 CI/CD 服务器和你的本地环境使用完全相同的依赖版本。**日常开发用 `npm install`，自动化部署用 `npm ci`。**

---

## 8.4 新手最容易踩的坑

以下这些错误几乎所有 Node.js 初学者都遇到过。提前了解它们，能帮你省下大量调试时间。

### 8.4.1 路径问题 —— 相对路径不是相对于当前文件

这是 **最常见的 Node.js 新手错误**，没有之一。

```javascript
// 假设文件在 /project/src/utils.js
import { readFile } from 'node:fs/promises'

// 你想读 /project/data/config.json
// 但你写了：
const data = await readFile('./data/config.json') // 错了！
```

`readFile('./data/config.json')` 中的相对路径是相对于**当前工作目录**（你在哪里运行 `node` 命令），而不是相对于当前文件。

**解决方案**：使用 `path.join(__dirname, ...)`（CommonJS）或 `fileURLToPath(import.meta.url)`（ESM）：

```javascript
// ESM 中获取当前文件所在的目录
import path from 'node:path'
import { fileURLToPath } from 'node:url'

const __dirname = path.dirname(fileURLToPath(import.meta.url))
const configPath = path.join(__dirname, '..', 'data', 'config.json')

const data = await readFile(configPath, 'utf-8')
```

> [!tip] 记住这个规则
> **`require()` 导入模块用相对路径，`readFile()` / `writeFile()` 永远用绝对路径**。或者至少用 `path.resolve()` 转成绝对路径。

### 8.4.2 导入自己的模块忘记加 `./`

```javascript
// 错误的写法 —— Node 会去 node_modules 里找
import utils from 'utils'

// 正确的写法 —— 告诉 Node 这是本地文件
import utils from './utils.js'
```

Node.js 的模块解析规则是：

- 以 `./` 或 `../` 开头的 → 本地文件
- 以字母开头的 → `node_modules` 中的第三方包

> [!warning] 记住加 `./`
> `import express from 'express'` 正确（第三方包），但 `import utils from 'utils'` 错误（除非你有一个叫 `utils` 的 npm 包）。自己的文件永远加 `./` 前缀。

### 8.4.3 端口占用

```bash
node index.js
# 输出：
# Server running on http://localhost:3000
# 过一会儿又跑一次：
# Error: listen EADDRINUSE :::3000
```

`EADDRINUSE` 错误意味着端口 3000 已经被占用了。解决方案：

```bash
# 查找占用进程
lsof -i :3000

# 终止进程（macOS / Linux）
kill -9 <PID>

# 或者换一个端口
PORT=3001 node index.js
```

> [!tip] 开发时可以加个端口冲突自动处理
> 如果你经常遇到端口占用，可以在代码里加一个简单的 fallback：
> ```javascript
> const port = process.env.PORT || 3000
> // 如果端口被占，server 的 'error' 事件会触发
> ```

### 8.4.4 修改代码后忘记重启

你改了一个变量名，保存文件，刷新浏览器 —— 发现还是旧的结果。你愣住了，想了五分钟，然后才想起来没重启服务器。

这是每个 Node 初学者（以及很多老手）都会反复经历的事。解决方案就是本章开头讲的 **nodemon** 或 `node --watch`。从现在开始，开发时永远用 `npm run dev` 而不是 `node index.js`。

### 8.4.5 异步代码没等结果就继续执行

```javascript
import { readFile } from 'node:fs/promises'

function loadConfig() {
  let config = null
  readFile('config.json', 'utf-8').then(data => {
    config = JSON.parse(data) // 这里确实赋值了
  })
  console.log(config) // 输出 null —— 因为 readFile 还没执行完！
}

loadConfig()
```

问题在于：`readFile` 是异步的，`console.log(config)` 在它完成之前就执行了。

**解决方案**：始终使用 `await`：

```javascript
async function loadConfig() {
  const data = await readFile('config.json', 'utf-8')
  const config = JSON.parse(data)
  console.log(config) // 正确，等读取完成才输出
  return config
}
```

---

## 8.5 错误处理分类 —— 两种完全不同的错误

错误处理不是简单地写 `try/catch`。专业的 Node.js 开发者会把错误分为两类，并分别对待。

### 操作性错误（Operational Errors）

这类错误**是可以预见的**，虽然你不希望它们发生，但它们属于应用的正常运行时范畴：

- 用户输入了无效数据（如邮箱格式不对）
- 数据库连接超时
- 请求的文件不存在
- 网络请求返回 404

**处理方式**：在合适的层级 catch，返回友好的错误信息，必要时重试。

```javascript
app.get('/user/:id', async (req, res) => {
  try {
    const user = await findUserById(req.params.id)
    if (!user) {
      return res.status(404).json({ error: '用户不存在' })
    }
    res.json(user)
  } catch (err) {
    // 记录日志
    console.error('查询用户失败:', err.message)
    // 返回友好信息
    res.status(500).json({ error: '服务器内部错误，请稍后重试' })
  }
})
```

### 程序员错误（Programmer Errors）

这类错误是**代码中的 bug**，不是运行时状态导致的：

- 访问未定义的变量（`undefined.name`）
- 给函数传了错误类型的参数
- 忘记 `await` 异步函数
- 拼写错误

**处理方式**：这类错误**不应该被 catch 并吞掉**。正确的做法是让程序崩溃（crash），然后立即重启。因为程序的内部状态可能已经损坏了，继续运行只会导致更严重的问题。

```javascript
// 错误做法 —— 吞掉程序员的 bug
try {
  const result = someUndefinedVariable.doSomething()
} catch (err) {
  // 这个错误不应该被优雅处理！应该崩溃！
  console.error('发生错误:', err)
}

// 正确做法 —— 使用全局错误处理，记录日志后退出
process.on('uncaughtException', (err) => {
  console.error('未捕获的异常，程序将退出:', err)
  // 记录日志、清理资源
  process.exit(1)
})
```

> [!note] 如何区分？
> 有一个简单的判断标准：**如果这个错误由用户操作触发，通常是操作性错误；如果由代码逻辑触发，通常是程序员错误。** 操作性错误应该用 try/catch 处理；程序员错误应该让进程崩溃，然后用进程管理器（如 PM2、Docker）自动重启。

---

## 8.6 结构化日志入门 —— 告别 console.log

### 8.6.1 console.log 的局限性

到目前为止，我们一直在用 `console.log` 打印信息。它在学习阶段够用，但在真正的应用中有三个严重问题：

1. **没有日志级别**：信息、警告、错误全部混在一起，无法过滤。
2. **没有结构化**：输出纯文本，无法被日志分析工具解析。
3. **没有时间戳**：默认不包含精确的时间信息。

```javascript
// 混在一起的日志，难以分析
console.log('用户登录成功')
console.error('数据库连接失败')
console.log('请求耗时 230ms')
```

### 8.6.2 用 Pino 做结构化日志

[Pino](https://getpino.io/) 是目前最快的 Node.js 日志库。它的输出是 JSON 格式，每条日志都是一个独立的结构化对象。

安装：

```bash
npm install pino
```

基本使用：

```javascript
import pino from 'pino'

// 创建一个日志实例
const logger = pino({
  level: 'info',       // 只输出 info 及以上级别
  transport: {
    target: 'pino-pretty'  // 美化输出（开发环境用）
  }
})

// 使用不同的日志级别
logger.info('服务器启动成功')
logger.warn('磁盘空间不足: %s', '/data')
logger.error({ err: new Error('数据库连接失败') }, '数据库错误')
logger.debug('这条不会输出')  // level 是 info，debug 级别不输出
```

输出示例（JSON 格式，生产环境）：

```json
{"level":30,"time":1722051234567,"pid":12345,"hostname":"myhost","msg":"服务器启动成功"}
{"level":40,"time":1722051234567,"pid":12345,"hostname":"myhost","msg":"磁盘空间不足: /data"}
{"level":50,"time":1722051234567,"pid":12345,"hostname":"myhost","msg":"数据库错误","err":{"message":"数据库连接失败","stack":"..."}}
```

这样每条日志都包含时间戳、进程 ID、服务器名和结构化的错误信息。你可以用工具（如 `jq`）或日志平台（如 ELK、Datadog）来搜索和分析。

> [!tip] 开发环境用美化输出，生产环境用 JSON 格式
> 在开发时使用 `pino-pretty`（`npm install -D pino-pretty`）把 JSON 日志转成易读格式。在生产环境去掉美化插件，输出纯 JSON 方便日志采集系统处理。

### 8.6.3 日志级别速查

| 级别 | 数字值 | 用途 |
|------|--------|------|
| `fatal` | 60 | 程序即将崩溃，必须立即处理 |
| `error` | 50 | 操作失败，但程序还能继续运行 |
| `warn` | 40 | 不正常的现象，但程序能自动恢复 |
| `info` | 30 | 正常的运行信息 |
| `debug` | 20 | 调试信息，方便定位问题 |
| `trace` | 10 | 最详细的跟踪日志 |

---

## 8.7 安全基础配置 —— 给应用穿上盔甲

Node.js 应用如果不做任何安全配置，就像把家门敞开着。下面这几步可以在几分钟内让你的应用安全很多。

### 8.7.1 helmet —— 设置安全 HTTP 头

[helmet](https://helmetjs.github.io/) 是一个安全中间件集合，它通过设置一系列 HTTP 头来防御常见的 Web 攻击。

安装：

```bash
npm install helmet
```

使用：

```javascript
import express from 'express'
import helmet from 'helmet'

const app = express()

// 放在最前面，在所有路由之前
app.use(helmet())

app.get('/', (req, res) => {
  res.send('Hello, secure world!')
})
```

这一行代码做了很多事情：禁用了 `X-Powered-By: Express` 头（防止攻击者知道你的技术栈）、设置了内容安全策略（CSP）、防止点击劫持（X-Frame-Options）等等。

### 8.7.2 CORS —— 控制谁能访问你的 API

CORS（Cross-Origin Resource Sharing，跨源资源共享）控制哪些域名可以访问你的 API。如果部署了前端页面（比如 `http://my-app.com`），你的 API 在 `http://api.my-app.com`，浏览器会阻止前端跨域请求 —— 除非服务器明确允许。

安装：

```bash
npm install cors
```

使用：

```javascript
import cors from 'cors'

// 允许所有来源（开发环境可以，生产环境太宽松）
app.use(cors())

// 生产环境 —— 只允许特定域名
app.use(cors({
  origin: 'https://my-app.com',
  methods: ['GET', 'POST', 'PUT', 'DELETE'],
  allowedHeaders: ['Content-Type', 'Authorization']
}))
```

> [!warning] 生产环境不要用 cors() 无参数模式
> 无参数模式允许所有域名访问你的 API。如果数据库 API 被随意访问，后果严重。**明确指定允许的来源。**

### 8.7.3 限流 —— 防止暴力请求

[express-rate-limit](https://www.npmjs.com/package/express-rate-limit) 可以限制同一 IP 在单位时间内的请求次数，防止暴力破解和 DoS 攻击。

安装：

```bash
npm install express-rate-limit
```

使用：

```javascript
import rateLimit from 'express-rate-limit'

// 全局限流：每个 IP 每 15 分钟最多 100 次请求
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000,  // 15 分钟
  max: 100,                   // 最多 100 次
  message: { error: '请求过于频繁，请稍后重试' }
})
app.use(limiter)

// 针对登录接口的严格限流：每个 IP 每分钟最多 5 次
const loginLimiter = rateLimit({
  windowMs: 60 * 1000,
  max: 5,
  message: { error: '登录尝试过于频繁' }
})
app.use('/api/login', loginLimiter)
```

### 8.7.4 密码哈希 —— 永远不要存明文密码

如果你在数据库中存了用户的明文密码，一旦数据泄露，用户的账户和其他网站（很多人重复使用密码）全都会暴露。正确的做法是使用哈希算法。

推荐使用 `bcrypt`：

安装：

```bash
npm install bcrypt
```

使用：

```javascript
import bcrypt from 'bcrypt'

// 注册时：哈希密码再存储
const saltRounds = 10
const hashedPassword = await bcrypt.hash('用户输入的密码', saltRounds)
// 把 hashedPassword 存到数据库

// 登录时：比较密码
const isMatch = await bcrypt.compare('用户输入的密码', hashedPassword)
if (isMatch) {
  console.log('密码正确，登录成功')
} else {
  console.log('密码错误')
}
```

> [!note] 为什么用 bcrypt 而不是普通哈希（如 SHA-256）？
> bcrypt 是**慢哈希** —— 它故意设计得很慢（每次大约 100ms），这使得攻击者即使拿到数据库也极难暴力破解所有密码。普通的 SHA-256 很快，一秒钟能算几百万次，攻击者可以快速尝试各种密码组合。**在这个场景下，"慢"就是安全。**

---

## 8.8 性能注意事项

### 8.8.1 不要阻塞事件循环

Node.js 的性能核心原则非常简单：**不要阻塞事件循环**。

回顾第一章学过的内容：Node.js 执行你的 JavaScript 代码是单线程的。如果这个线程被某个耗时操作占用了，所有其他请求都得排队等着。

```javascript
// 危险 —— 这会阻塞事件循环
function heavyComputation() {
  for (let i = 0; i < 1e10; i++) {
    // 疯狂计算
  }
}

app.get('/compute', (req, res) => {
  heavyComputation()  // 这时其他用户全部卡住！
  res.send('完成')
})
```

当一个请求触发 `heavyComputation()` 时，所有其他请求（包括那些只想要个静态页面的）都必须等它执行完。

**哪些操作会阻塞事件循环？**

- 大量的循环和数学计算（> 几十毫秒）
- 大规模的 JSON 解析或数据转换
- 同步的文件操作（`fs.readFileSync`）
- JSON 序列化超大对象

**解决方案**：

1. **小任务拆分**：用 `setImmediate` 让出控制权

```javascript
function processLargeArray(items) {
  if (items.length === 0) return

  const item = items.shift()
  // 处理一个 item
  console.log('处理:', item)

  // 把剩下的任务放回事件队列
  setImmediate(() => processLargeArray(items))
}
```

2. **CPU 密集型任务**：用 Worker Threads

### 8.8.2 Worker Threads 概念简介

Worker Threads 是 Node.js 提供的"多线程"机制。注意引号 —— Node.js 本身是单线程的，但 Worker Threads 可以让你创建额外的 JavaScript 执行线程，每个线程有自己独立的 V8 实例和事件循环。

```javascript
import { Worker } from 'node:worker_threads'

// 主线程
const worker = new Worker('./heavy-task.js', {
  workerData: { amount: 1e9 }
})

worker.on('message', (result) => {
  console.log('计算完成:', result)
})

worker.on('error', (err) => {
  console.error('工作线程出错:', err)
})
```

```javascript
// heavy-task.js —— 在单独的线程中执行
import { parentPort, workerData } from 'node:worker_threads'

// 这里的计算不会阻塞主线程！
let sum = 0
for (let i = 0; i < workerData.amount; i++) {
  sum += i
}

parentPort.postMessage(sum)
```

> [!note] 你不需要现在就学会 Worker Threads
> 这里只是让你知道 Node.js 有处理 CPU 密集任务的能力。对于 90% 的场景 —— 比如构建 Web API、数据库查询、文件读写 —— 你根本用不上 Worker Threads。只有当你遇到像图像处理、视频编码、大规模数据分析这类场景时，才需要考虑它。

**简单记忆**：

```
Web API 请求处理        → 用普通 async/await，不用操心
文件/数据库操作          → 异步 I/O，libuv 自动处理
短时间计算（< 10ms）    → 直接在主线程执行
长时间计算（> 100ms）   → 考虑 Worker Threads
```

---

## 8.9 本章小结

- **nodemon**（或 `node --watch`）自动监听文件变化并重启程序，开发时永远不要手动重启。
- **dotenv + .env 文件**管理环境变量，把配置从代码中分离；`.env.example` 提交到 Git，真实的 `.env` 永远忽略。
- **npm 命令速查表**随用随查，特别记住 `npm ci` 用于自动化部署、`npx` 用于临时执行包。
- **五个新手常见错误**：路径相对于工作目录而非文件、导入本地模块忘加 `./`、端口占用、忘记重启、异步代码没等结果。
- **操作性错误** try/catch 优雅处理；**程序员错误**不该被吞掉，应该让进程崩溃并自动重启。
- **结构化日志**用 Pino 替代 console.log，开发环境美化输出，生产环境输出 JSON 格式。
- **安全基础四件套**：helmet（安全 HTTP 头）、cors（跨域控制）、rate-limit（限流）、bcrypt（密码哈希）。
- **永远不要阻塞事件循环**，CPU 密集任务交给 Worker Threads。

---

## 下一章预告

第八章的内容比较"散"——它覆盖了从工具链到安全、从日志到性能的方方面面。这不是跑题，而是因为**一个专业的 Node.js 开发者需要同时掌握这些技能**，它们共同决定了你的代码质量、安全性和可维护性。

到目前为止，我们已经覆盖了一个完整的 Node.js Web 开发者所需的核心知识。下一章将回顾整个课程，帮你建立起完整的知识地图，并告诉你接下来可以朝哪些方向继续深入。


---

从工具链到安全配置，你已经具备了专业开发的必备素养。最后，让我们把所有知识串联起来——通过三个实战项目，把前面八章学到的内容真正变成你自己的技能。

# 第九章：项目实战与学习路径

恭喜你走到了这里。从最初连 Node.js 是什么都不清楚，到现在你已经掌握了模块系统、异步编程、文件操作、事件循环、Express 框架、环境配置与调试——这八个章节的知识，共同构成了 Node.js 开发者的核心能力底座。

但学完知识和真正会用之间，还差一个关键的步骤：**动手做项目**。

这一章的目标很简单：带你做三个实战项目，从简单到复杂，把前面学过的所有知识串联起来。然后在最后一章里，我们一起来回顾整条学习路径，看看接下来还能往哪些方向深入。

---

## 9.1 项目实战总览

先给你一张全景图，看看从易到难有哪些项目可以练手：

| 阶段 | 项目 | 练习目标 | 涉及章节 |
|------|------|---------|---------|
| 核心模块 | 文件批量重命名 CLI 工具 | `fs` + `path` 综合运用 | 第五章 |
| 核心模块 | 简易 HTTP 服务器（多路由） | `http` 模块理解请求/响应 | 第七章 |
| Express | 便签 REST API | RESTful 接口 + 路由 + JSON + 中间件 | 第七章、第八章 |
| Express | 天气查询 API | 调用外部服务 + 环境配置 | 第八章 |
| 组合 | 全栈博客系统 | Express + 数据库 + 认证 | 进阶 |
| 进阶 | 实时聊天应用 | WebSocket + 认证 + 部署 | 进阶 |

> [!tip] 不要跳过任何阶段
> 每个项目都针对特定的知识点设计。即使你觉得"CLI 工具太简单了"，也值得亲手敲一遍——写代码和读代码是两种完全不同的体验。

本章我们会详细展开前三个项目。它们覆盖了你目前学过的全部核心知识，做完这三个，你就可以自信地说自己"会用 Node.js 了"。

---

## 9.2 实战一：文件批量重命名 CLI 工具

### 项目目标

写一个命令行工具，把指定目录下的所有文件批量重命名。比如把 `photo-001.jpg`、`photo-002.jpg` 改为 `vacation-001.jpg`、`vacation-002.jpg`。

### 核心知识点

- `fs.promises.readdir` 读取目录
- `fs.promises.rename` 重命名文件
- `path.parse` 解析文件名和扩展名
- `path.join` 拼接路径
- `process.argv` 获取命令行参数

### 代码骨架

```javascript
import fs from 'node:fs/promises';
import path from 'node:path';

const directory = process.argv[2];      // 目标目录
const prefix = process.argv[3];         // 新文件名前缀

async function batchRename(dir, newPrefix) {
  try {
    const files = await fs.readdir(dir);
    let count = 0;

    for (const file of files) {
      const { ext } = path.parse(file);          // 获取扩展名
      const oldPath = path.join(dir, file);
      const stat = await fs.stat(oldPath);

      // 只处理文件，跳过子目录
      if (stat.isFile()) {
        count++;
        const newName = `${newPrefix}-${String(count).padStart(3, '0')}${ext}`;
        const newPath = path.join(dir, newName);
        await fs.rename(oldPath, newPath);
        console.log(`[OK] ${file} -> ${newName}`);
      }
    }

    console.log(`\n完成！共重命名 ${count} 个文件。`);
  } catch (err) {
    console.error('出错了：', err.message);
  }
}

batchRename(directory, prefix);
```

### 怎么运行

```bash
node rename.mjs ./my-photos vacation
```

> [!note] 程序做了什么
> 1. 读取 `./my-photos` 目录下的所有文件和子目录
> 2. 只处理文件（跳过子目录），按顺序编号
> 3. 用 `path.parse` 提取扩展名，保留原始后缀
> 4. 用 `fs.rename` 把旧文件名改为新文件名
> 5. 每改一个就在控制台打印一条日志

### 扩展练习

完成了上面的基础版本后，你可以试着给它加上更多功能：

- 添加 `--dry-run` 参数：只预览要改的名字，不实际执行重命名
- 添加 `--revert` 参数：撤销上一次重命名操作
- 添加 `--filter` 参数：只处理特定扩展名的文件（如只处理 `.jpg`）
- 添加递归选项：处理子目录中的文件

> [!tip] 练习建议
> 这个项目虽然小，但涉及了 `fs`、`path`、`process.argv`、异步编程中的 `try/catch` 等多个知识点。如果遇到 `fs.stat` 或 `path.parse` 用法不记得了，回去翻翻第五章，这也是复习的好机会。

---

## 9.3 实战二：简易 HTTP 服务器多路由

### 项目目标

用原生的 `http` 模块搭建一个小型 HTTP 服务器，能够根据不同的 URL 路径返回不同的内容。这个项目帮你深入理解"服务器收到请求后到底发生了什么"。

### 核心知识点

- `http.createServer` 创建服务器
- `req.url` 解析请求路径
- `req.method` 区分 HTTP 方法
- `res.writeHead` 设置状态码和响应头
- `res.end` 返回响应体

### 代码骨架

```javascript
import http from 'node:http';

const PORT = 3000;

const server = http.createServer((req, res) => {
  const { method, url } = req;

  // 设置统一的响应头，解决中文乱码
  res.setHeader('Content-Type', 'text/html; charset=utf-8');

  // ---- 路由分发 ----
  if (url === '/' && method === 'GET') {
    res.writeHead(200);
    res.end(`
      <h1>欢迎来到我的第一个 Node.js 服务器</h1>
      <ul>
        <li><a href="/about">关于</a></li>
        <li><a href="/weather">天气</a></li>
        <li><a href="/api/time">当前时间 (JSON)</a></li>
      </ul>
    `);

  } else if (url === '/about' && method === 'GET') {
    res.writeHead(200);
    res.end('<h1>关于本站</h1><p>这是用 Node.js 原生 http 模块搭建的简易服务器。</p>');

  } else if (url === '/api/time' && method === 'GET') {
    // 返回 JSON 格式的当前时间
    res.setHeader('Content-Type', 'application/json; charset=utf-8');
    res.writeHead(200);
    res.end(JSON.stringify({
      time: new Date().toLocaleString('zh-CN'),
      timestamp: Date.now()
    }));

  } else if (url === '/weather' && method === 'GET') {
    // 模拟天气预报——在实际项目中这里会调用外部天气 API
    res.setHeader('Content-Type', 'application/json; charset=utf-8');
    res.writeHead(200);
    res.end(JSON.stringify({
      city: '北京',
      temperature: '26°C',
      condition: '晴',
      humidity: '45%'
    }));

  } else {
    // 404 处理
    res.writeHead(404);
    res.end('<h1>404 - 页面未找到</h1><p>你访问的页面不存在。</p>');
  }
});

server.listen(PORT, () => {
  console.log(`服务器已启动：http://localhost:${PORT}`);
});
```

### 怎么运行

```bash
node server.mjs
```

然后在浏览器里打开 `http://localhost:3000`，你会看到一整个可点击的页面。

### 关键知识点回顾

| 代码片段 | 作用 |
|---------|------|
| `http.createServer((req, res) => {})` | 创建服务器，每次收到请求都会执行回调 |
| `req.url` 和 `req.method` | 获取客户端请求的路径和 HTTP 方法 |
| `res.writeHead(200)` | 设置 HTTP 状态码（200 表示成功） |
| `res.setHeader('Content-Type', ...)` | 告诉浏览器返回内容的格式 |
| `res.end('...')` | 发送响应体并结束请求 |
| `server.listen(PORT, callback)` | 启动服务器，在指定端口监听 |

> [!warning] 一个常见陷阱
> 使用原生的 `http` 模块时，常见的错误是**忘记调用 `res.end()`**。如果路由分支里没有 `res.end()`，浏览器会一直转圈等待响应，直到超时。写每个路由分支时，记得检查是否已经调用了 `res.end()`。

### 扩展练习

- 添加一个 `/api/todo` 路由：用数组模拟一个待办列表，返回 JSON 格式的待办项
- 添加 `/search?q=xxx` 的查询参数解析功能（提示：用 `url` 模块的 `new URL(req.url, 'http://localhost')`）
- 添加一个简单的 POST 路由，能接收 JSON 格式的 POST 请求体

---

## 9.4 实战三：便签 REST API

### 项目目标

用 Express 构建一个完整的 RESTful API——一个简单的便签（Note）管理服务。支持创建、读取、更新、删除便签（即 CRUD 操作）。

这是三个实战项目中最重要的一个，它覆盖了 Express 路由、中间件、错误处理、JSON 数据操作、项目结构分层等你在第七章和第八章中学过的几乎所有知识点。

> [!note] 为什么选便签 API？
> 便签 API 是所有 CRUD 应用的"Hello World"。它足够简单（一个资源、几个字段），但又完整地覆盖了 RESTful 设计的全部核心概念。学会做便签 API，博客系统、任务管理、评论系统这些本质上都是一样的套路。

### 项目结构

```
notes-api/
├── package.json
├── index.js          # 入口文件，启动服务器
├── routes/
│   └── notes.js      # 便签路由
├── controllers/
│   └── notes.js      # 便签控制器
├── middleware/
│   └── errorHandler.js  # 错误处理中间件
└── data/
    └── notes.json    # 模拟数据库（文件存储）
```

### 第一步：初始化项目

```bash
mkdir notes-api && cd notes-api
npm init -y
npm install express
```

### 第二步：入口文件（index.js）

```javascript
import express from 'express';
import notesRouter from './routes/notes.js';
import { errorHandler } from './middleware/errorHandler.js';

const app = express();
const PORT = process.env.PORT || 3000;

// 全局中间件：解析 JSON 请求体
app.use(express.json());

// 路由
app.use('/api/notes', notesRouter);

// 健康检查
app.get('/', (req, res) => {
  res.json({ message: '便签 API 服务运行中', version: '1.0.0' });
});

// 错误处理中间件（必须在路由之后注册）
app.use(errorHandler);

app.listen(PORT, () => {
  console.log(`服务器已启动：http://localhost:${PORT}`);
});
```

### 第三步：路由层（routes/notes.js）

路由层只负责"分发请求到对应的控制器方法"，本身不包含业务逻辑：

```javascript
import { Router } from 'express';
import * as notesController from '../controllers/notes.js';

const router = Router();

router.get('/',        notesController.getAllNotes);
router.get('/:id',     notesController.getNoteById);
router.post('/',       notesController.createNote);
router.put('/:id',     notesController.updateNote);
router.delete('/:id',  notesController.deleteNote);

export default router;
```

### 第四步：控制器层（controllers/notes.js）

控制器负责组织请求和响应的逻辑——解析参数、调用数据操作、返回结果：

```javascript
import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const DATA_FILE = path.join(__dirname, '../data/notes.json');

// 读取所有便签
export async function getAllNotes(req, res, next) {
  try {
    const notes = await readNotes();
    res.json({ success: true, data: notes, count: notes.length });
  } catch (err) {
    next(err);  // 交给错误处理中间件
  }
}

// 根据 ID 获取单条便签
export async function getNoteById(req, res, next) {
  try {
    const notes = await readNotes();
    const note = notes.find(n => n.id === req.params.id);

    if (!note) {
      return res.status(404).json({ success: false, message: '便签不存在' });
    }

    res.json({ success: true, data: note });
  } catch (err) {
    next(err);
  }
}

// 创建便签
export async function createNote(req, res, next) {
  try {
    const { title, content } = req.body;

    // 简单验证
    if (!title || !content) {
      return res.status(400).json({
        success: false,
        message: '标题和内容不能为空'
      });
    }

    const notes = await readNotes();
    const newNote = {
      id: String(Date.now()),        // 用时间戳做简单 ID
      title,
      content,
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString()
    };

    notes.push(newNote);
    await writeNotes(notes);

    res.status(201).json({ success: true, data: newNote });
  } catch (err) {
    next(err);
  }
}

// 更新便签
export async function updateNote(req, res, next) {
  try {
    const notes = await readNotes();
    const index = notes.findIndex(n => n.id === req.params.id);

    if (index === -1) {
      return res.status(404).json({ success: false, message: '便签不存在' });
    }

    const { title, content } = req.body;
    notes[index] = {
      ...notes[index],
      title: title ?? notes[index].title,
      content: content ?? notes[index].content,
      updatedAt: new Date().toISOString()
    };

    await writeNotes(notes);
    res.json({ success: true, data: notes[index] });
  } catch (err) {
    next(err);
  }
}

// 删除便签
export async function deleteNote(req, res, next) {
  try {
    const notes = await readNotes();
    const filtered = notes.filter(n => n.id !== req.params.id);

    if (filtered.length === notes.length) {
      return res.status(404).json({ success: false, message: '便签不存在' });
    }

    await writeNotes(filtered);
    res.json({ success: true, message: '删除成功' });
  } catch (err) {
    next(err);
  }
}

// ---- 数据读写辅助函数 ----

async function readNotes() {
  try {
    const raw = await fs.readFile(DATA_FILE, 'utf-8');
    return JSON.parse(raw);
  } catch {
    // 文件不存在或内容为空时返回空数组
    return [];
  }
}

async function writeNotes(notes) {
  await fs.writeFile(DATA_FILE, JSON.stringify(notes, null, 2), 'utf-8');
}
```

### 第五步：错误处理中间件（middleware/errorHandler.js）

```javascript
export function errorHandler(err, req, res, next) {
  console.error('[错误]', err.message);
  res.status(500).json({
    success: false,
    message: '服务器内部错误',
    ...(process.env.NODE_ENV === 'development' && { detail: err.message })
  });
}
```

### 怎么运行和测试

```bash
# 启动服务
node index.js

# 在另一个终端里用 curl 测试

# 创建便签
curl -X POST http://localhost:3000/api/notes \
  -H "Content-Type: application/json" \
  -d '{"title":"买菜清单","content":"鸡蛋、牛奶、面包"}'

# 获取所有便签
curl http://localhost:3000/api/notes

# 更新便签（将上面的返回 ID 替换到 :id 位置）
curl -X PUT http://localhost:3000/api/notes/1234567890 \
  -H "Content-Type: application/json" \
  -d '{"title":"超市购物","content":"鸡蛋、牛奶、面包、香蕉"}'

# 删除便签
curl -X DELETE http://localhost:3000/api/notes/1234567890
```

> [!tip] 用 Postman 或 Insomnia 替代 curl
> 如果你觉得终端输入 curl 不太方便，可以安装 Postman 或 Insomnia（免费）。它们提供图形界面，方便你发送 GET/POST/PUT/DELETE 请求，还能保存请求历史。

### 这个项目教会了你什么

| 知识点 | 实际应用 |
|--------|---------|
| Express 路由 | `router.get/post/put/delete` 定义 RESTful 接口 |
| 中间件 | `express.json()` 解析 body，自定义错误处理中间件 |
| 异步编程 | 控制器所有方法都用 async/await |
| 错误处理 | `try/catch` + `next(err)` 传递给全局错误中间件 |
| HTTP 状态码 | 201 创建成功、400 参数错误、404 未找到、500 服务器错误 |
| JSON 数据操作 | 读写 JSON 文件模拟数据库，`JSON.parse` 和 `JSON.stringify` |
| 项目结构分层 | routes → controllers 各司其职 |

### 扩展练习

- 添加 Zod 输入验证：用 Zod 定义便签的 schema，在路由层做严格的参数校验
- 添加搜索功能：`GET /api/notes?q=xxx` 按关键词搜索便签标题
- 添加分页功能：`GET /api/notes?page=1&limit=10`
- 给便签添加标签（tags）字段，支持按标签筛选
- 把 JSON 文件存储替换为 SQLite 数据库（用 `better-sqlite3` 或 `sql.js`）

---

## 9.5 学习路径总览

你已经走完了从零到实战的完整路径。站在现在这个节点，回头看一眼整条路线：

```
安装 Node.js LTS
      │
      ▼
核心模块（fs / path / http）
      │
      ▼
模块系统（CommonJS → ESM）
      │
      ▼
npm 包管理
      │
      ▼
异步编程（回调 → Promise → async/await）
      │
      ▼
事件循环（理解"为什么这样写"）
      │
      ▼
Express 框架（路由 + 中间件 + REST API）
      │
      ▼
环境配置与最佳实践（nodemon + dotenv + 日志 + 安全）
      │
      ▼
项目实战（CLI 工具 → HTTP 服务器 → REST API）
      │
      ▼
下一步（数据库 → 认证 → 测试 → 部署）
```

你现在的位置就在这里——最后一个箭头之前，"下一步"的门槛已经在你面前。

> [!note] 这张图的价值
> 很多初学者学了一段时间后会陷入"不知道自己学到哪了"的迷茫。这张图就是你的地图。无论什么时候回头看，你都能清楚地知道自己在哪个阶段、下一个目标是什么。

---

## 9.6 推荐学习资源

接下来你可能有几个方向想继续深入。以下是经过筛选的学习资源，按类别排列：

### 免费课程

| 资源 | 时长 | 特点 |
|------|------|------|
| [Scrimba — Learn Node.js + Express](https://scrimba.com/) | 7.5 小时 | 交互式录屏，边看边改代码，可获免费证书 |
| [freeCodeCamp — Back End Development](https://www.freecodecamp.org/) | 300 小时 | 5 个实战项目，完成可获可验证认证 |
| [The Odin Project — NodeJS Path](https://www.theodinproject.com/) | 自定进度 | 项目驱动，强调读文档 + 亲手构建 |
| [Fullstack Open（赫尔辛基大学）](https://fullstackopen.com/) | ~40 小时 | 学术级课程，可获 ECTS 学分 |
| [Node.js 官方文档](https://nodejs.org/) | — | 最权威的参考，新版 Beta 内置搜索 |

### 付费课程（高性价比）

| 资源 | 价格 | 时长 | 特点 |
|------|------|------|------|
| Andrew Mead — Complete Node.js Developer | ~$10-15（Udemy 促销） | 35+ 小时 | 循序渐进，非常适合初学者 |
| Jonas Schmedtmann — Node/Express/MongoDB | ~$10-15（Udemy 促销） | 42+ 小时 | 生产导向，项目丰富 |

> [!tip] Udemy 课程不要原价买
> Udemy 几乎每周都有促销活动，课程价格通常在 $10-15 左右。千万不要原价购买——把课程加入心愿单，等打折时再买。

### 书籍

- **《Node.js Design Patterns - Fourth Edition》**（Luciano Mammino, 2025）：732 页的权威之作，覆盖回调、Streams、测试、微服务等进阶主题。适合有一定基础后阅读，不适合入门阶段。
- **《Efficient Node.js 实战》**（中国电力出版社，2026 年 5 月）：覆盖模块、事件驱动架构、数据流、子进程与扩展部署。
- **《Node.js Web 开发实战（慕课版 第 2 版）》**（人民邮电出版社，2026 年 5 月）：融入 AIGC 辅助编程内容。

### 参考资源

- **[goldbergyoni/nodebestpractices](https://github.com/goldbergyoni/nodebestpractices)**（GitHub 105K+ stars）：80+ 条最佳实践，涵盖架构、错误处理、安全、测试、部署等方方面面。建议在有一定项目经验后再读，效果更好。
- **[Node.js 官方中文文档](https://nodejs.cn/)**：中文翻译版官方文档。
- **[Node.js 新版 Beta 文档](https://beta.docs.nodejs.org)**：新版官方文档，内置搜索功能。

---

## 9.7 进阶方向

学会了基础之后，接下来的路怎么走？以下是你最可能感兴趣的七个方向，按推荐顺序排列：

### 数据库集成

Node.js 最常搭配的数据库有两种：**MongoDB**（文档型，NoSQL）和 **PostgreSQL**（关系型，SQL）。推荐从 MongoDB + Mongoose 开始，上手曲线较低；之后学习 PostgreSQL + Prisma（现代 ORM，类型安全）。

```javascript
// 用 Prisma 操作数据库的简洁性（预习）
const user = await prisma.user.create({
  data: { name: '小明', email: 'xiao@example.com' }
});
```

### 认证与授权

学习 JWT（JSON Web Token）和 Session 两种认证方式的实现。这是构建真实 Web 应用的必备技能。推荐学完 JWT 后，尝试给便签 API 加上用户注册和登录功能。

### 测试

用 **Jest**（测试框架）和 **Supertest**（HTTP 测试工具）为你的 API 编写自动化测试。测试不仅能帮你发现 bug，更重要的是让你有底气放心重构代码。

```javascript
// 一个简单的 API 测试示例
import request from 'supertest';
import app from '../index.js';

describe('GET /api/notes', () => {
  it('应该返回便签列表', async () => {
    const res = await request(app).get('/api/notes');
    expect(res.status).toBe(200);
    expect(res.body.success).toBe(true);
  });
});
```

### 部署

将 Node.js 应用部署到生产环境。核心工具链：**Docker**（容器化）、**PM2**（进程守护）、**CI/CD**（自动部署）。推荐从免费的云服务开始（如 Render、Railway、Vercel）。

### Streams

Stream（流）是 Node.js 中处理大数据的核心机制。用 `fs.createReadStream` 和 `fs.createWriteStream` 处理 GB 级别的文件，避免一次性加载到内存。这是区分初级和中级 Node.js 开发者的重要分水岭。

### WebSocket

WebSocket 是实现实时通信（聊天、通知、协作编辑）的标准方案。推荐学习 **Socket.IO**，它是 WebSocket 的上层封装，自动处理降级和重连，对新手非常友好。

### 微服务

当你构建的应用越来越大时，可以考虑将一个庞大的单体应用拆分为多个小型服务。推荐从 **Fastify**（比 Express 更快的框架）和消息队列（如 BullMQ、RabbitMQ）开始了解。

> [!tip] 不要贪多
> 很多初学者看到这么多方向会感到焦虑，担心自己"还有太多不会的"。这是完全正常的。关键是**挑一个方向深入，不要同时追七个兔子**。我的建议是：先学数据库 + 认证，因为绝大多数 Web 应用都需要这两个。有了真实项目经验后，再根据工作需要去学测试、部署、Streams 等其他方向。

---

## 结语

到这里，整本笔记就结束了。我想用最后这几句话，和你聊聊从"学完"到"真正会"之间的距离。

**第一个真相：读完笔记只是开始。**

你读完了九个章节，了解了 Node.js 的架构、模块系统、异步编程、文件操作、事件循环、Express 框架、环境配置和项目实战——这些知识形成了一个完整的知识框架。但框架是骨架，真正的血肉需要你在写代码的过程中一点点填充。读完笔记不代表你会了 Node.js，**只有在笔记本之外独立完成过项目，才算真正开始入门**。

**第二个真相：遇到困难是正常的。**

你一定会在某个项目里遇到无法理解的报错，一定会在某个深夜卡在一个看起来"明明代码都是对的"的 bug 上。这是每个开发者——包括那些你崇拜的技术大牛——都经历过的过程。区别只在于，他们选择了继续调试，而不是放弃。

**第三个真相：动手才是最好的学习方法。**

这不是一句鸡汤，而是一条被无数次验证的学习法则。每完成一个项目，你对知识的理解就会加深一层。哪怕只是改了几行代码，你的收获也比读十篇教程更大。

> [!note] 最后送你一句话
> 计算机科学中，真正重要的不是你读了多少本书，而是你写了多少行代码。每个软件工程师的成长路径都只有一条：**想清楚，写出来，跑起来，改对它。**

这本笔记的 GitHub 仓库里有一个 `projects/` 目录，里面包含了本章三个实战项目的完整代码。如果你在动手过程中卡住了，可以去参考一下——但建议你先自己尝试至少 30 分钟，再去看答案。

祝你编码愉快。

