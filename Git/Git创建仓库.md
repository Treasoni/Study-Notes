---
tags:
  - git
---

什么是"创建仓库"？先统一概念
👉 **创建仓库 = 告诉 Git：从这个目录开始，我要用 Git 来管理它**

技术上就是一句话：

在某个目录里生成一个 .git 文件夹

这个 .git 文件夹：

- 存着所有提交历史

- 分支信息

- 配置文件

- 指针（HEAD）

⚠️ **删掉 .git，Git 历史就全没了**

## 创建仓库的三种方式

### 场景 1：本地从 0 开始创建仓库（最常见）

**①创建项目目录**

mkdir my-project

cd my-project

此时只是一个**普通文件夹**，和 Git 没任何关系。

**② 初始化 Git 仓库 ⭐核心命令**

git init

你会看到类似输出：

Initialized empty Git repository in /Users/liu/my-project/.git/

现在：

ls -a

你会看到：

.git

👉 **这一步，仓库就创建完成了**

③ 初始化后发生了什么？（原理）

- Git 在当前目录创建了 .git/

- 默认分支：

  - 新版 Git：main

  - 旧版 Git：master

- 当前还 **没有任何提交**

你可以验证：

git status

输出大概是：

On branch main

No commits yet

**④ 第一次提交（让仓库"活起来"）**

touch README.md

git add README.md

git commit -m \"initial commit\"

📌 **没有 commit 的仓库 ≈ 空壳**

### 场景 2：从远程仓库创建（clone）

如果项目已经在 GitHub / GitLab 上了，你不用git init，而是：

**① 克隆仓库**

git clone 仓库地址

示例：

git clone https://github.com/user/demo.git

Git 会自动：

- 创建目录

- 下载代码

- 初始化 .git

- 设置好远程仓库（origin）

👉 **clone = init + pull + remote add**

**② 验证**

cd demo

git status

git remote -v

### 场景 3：把"已有代码"变成 Git 仓库（非常常见）

比如你已经写了一堆代码，但还没用 Git。

**① 进入已有项目目录**

cd old-project

**② 初始化 Git**

git init

③ 添加并提交现有代码

git add .

git commit -m \"initial commit\"

👉 **历史从这一刻开始**

## .git 目录里到底有什么？

你不用全记，但知道结构很重要：

.git/

├─ config \# 当前仓库配置（local）

├─ HEAD \# 当前分支指针

├─ objects/ \# Git 核心数据

├─ refs/ \# 分支、标签

👉 **90% 的 Git 魔法都在这里**

