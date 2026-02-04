# 1. 这个链接到底是什么？
```http
https://raw.githubusercontent.com/ThePBone/tachiyomi-extensions-revived/repo/index.min.json
```

👉 **这是 GitHub 的 raw（原始文件）访问地址**

意思是：

> **直接获取 GitHub 仓库里的某一个文件内容**  
> 不经过网页、不带 UI、纯文本 / JSON

---

# 2. 把这个链接拆开看（很重要）

```text
raw.githubusercontent.com
│
├── ThePBone                     ← GitHub 用户 / 组织名
│
├── tachiyomi-extensions-revived ← 仓库名
│
├── repo                         ← 仓库里的目录
│
└── index.min.json               ← 文件名

```

等价于你在 GitHub 网页上点开：
```http
https://github.com/ThePBone/tachiyomi-extensions-revived
```

然后进入：

`repo/index.min.json`

只不过 **raw** 版本是给程序用的，不是给人看的。


# 3. 这种链接一般是“怎么来的”？

### 3.1  开源项目**官方提供**

最常见的来源：

- README 里写着：
    > Add this repo URL to your app
- 或 Wiki / 文档中写明：
    `https://raw.githubusercontent.com/xxx/xxx/main/index.json`

👉 Tachiyomi、LunaTV、各类插件系统都**只认 raw 链接**

### 3.2  GitHub 文件 → 右键「复制 raw 链接」

流程是这样的：

1. 打开 GitHub 仓库
2. 点进某个文件（如 `index.json`）
3. 点 **Raw**
4. 浏览器地址栏里的 URL  
    👉 就是 `raw.githubusercontent.com/...`
