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
