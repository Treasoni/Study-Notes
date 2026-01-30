---
tags:
  - git
---

# Git 是什么？

**Git 是一个「版本控制工具」**，用来做三件核心事情：
>1.  **保存代码的历史版本**（可以回到任何一个过去的状态）
>2.  **多人协作不冲突**（每个人都能同时改代码）
>3.  **安全地实验新功能**（用分支，不怕改坏）

类比：\
Git ≈ 给代码装了一个「无限撤销 + 时间机器 + 协作系统」

# Git 的核心思想（非常重要）

## 本地优先

（这是 Git 和 SVN 最大的区别）

1.  **所有历史记录都在你电脑上**

2.  不联网也能：
	-  提交（commit）

	-   回退版本

    - 切换分支

## Git 管理的是「快照」，不是「差异」

每次 commit：

1.  Git 会记录**整个项目当时的状态**

2.  内部会智能复用没变的文件（不浪费空间）

# Git 配置

Git 提供了一个叫做 **git
config** 的命令，用来配置或读取相应的工作环境变量。

这些环境变量，决定了 Git 在各个环节的具体工作方式和行为。

这些变量可以存放在以下三个不同的地方：

1.  /etc/gitconfig 文件：系统中对所有用户都普遍适用的配置。若使用 git
    config 时用 \--system 选项，读写的就是这个文件。

2.  \~/.gitconfig 文件：用户目录下的配置文件只适用于该用户。若使用 git
    config 时用 \--global 选项，读写的就是这个文件。

3.  当前项目的 Git
    目录中的配置文件（也就是工作目录中的 .git/config 文件）：这里的配置仅仅针对当前项目有效。每一个级别的配置都会覆盖上层的相同配置，所以 .git/config 里的配置会覆盖 /etc/gitconfig 中的同名变量。

在 Windows 系统上，Git 会找寻用户主目录下的 .gitconfig 文件。主目录即
\$HOME 变量指定的目录，一般都是 C:\\Documents and Settings\\\$USER。

此外，Git 还会尝试找寻 /etc/gitconfig 文件，只不过看当初 Git
装在什么目录，就以此作为根目录来定位。

## git config 到底是干嘛的？

你可以把 git config 理解成：

**Git 的"设置中心"**

比如：

- 你是谁？

- 提交代码时用什么名字和邮箱？

- 默认分支叫啥？

- 是否启用彩色输出？

这些都靠 git config 来告诉 Git。

## Git 的三层配置（核心重点）

我先用一句话总结，然后再细讲：

  -----------------------------------------------------------------------
  **级别**                **作用范围**            **比喻**
  ----------------------- ----------------------- -----------------------
  system                  整台电脑                公司制度

  global                  当前用户                你的个人习惯

  local                   当前项目                项目特殊要求
  -----------------------------------------------------------------------

### system（系统级）

📍 文件位置：

/etc/gitconfig

🧠 特点：

1.  **对这台电脑上的所有用户都生效**

2.  一般 **普通用户几乎不会用**

3.  需要管理员权限

🛠 命令：

git config \--system key value

📌 举例（不常见）：

git config \--system core.autocrlf false

👉 **新手可以直接忽略这一层**

### global（用户级）⭐最常用

📍 文件位置：

\~/.gitconfig

Windows 下相当于：

C:\\Users\\你的用户名\\.gitconfig

🧠 特点：

1.  **只对你这个用户生效**

2.  你所有 Git 项目都会用它

3.  **90% 的配置都在这里**

🛠 命令：

git config \--global key value

📌 经典配置（每个人都必须）：

git config \--global user.name \"Liu\"

git config \--global user.email \"liu042901@gmail.com\"

👉 以后你在任何仓库 commit，Git 都知道是你

### local（项目级）⭐⭐⭐优先级最高

📍 文件位置：

当前项目/.git/config

🧠 特点：

1.  **只对当前项目有效**

2.  常用于：

    a)  公司项目

    b)  开源项目

    c)  特殊规范项目

🛠 命令（不加任何参数）：

git config key value

📌 举例：

git config user.name \"Company Liu\"

git config user.email \"liu@company.com\"

👉 这个项目用公司身份\
👉 其他项目不受影响

## 如何查看当前到底用了哪个配置？

### 查看所有配置（以及来源）

git config \--list \--show-origin

你会看到类似：

file:C:/Users/Liu/.gitconfig user.name=Liu

file:.git/config user.email=liu@company.com

👉 一眼看出：

- 哪个文件

- 提供了哪个配置

# [[Git创建仓库]]

## 什么是"创建仓库"？先统一概念

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

# Git 的 4 个区域（必须背熟）

这是 **90% Git 问题的答案所在**：

工作区 → 暂存区 → 本地仓库 → 远程仓库

## 工作区（Working Directory）

- 你正在写代码的地方

- 文件可以被修改、删除、新建

## 暂存区（Stage / Index）

- 临时存放「**下一次要提交的内容**」

- 不是自动的，要你手动选择

## 本地仓库（Local Repository）

- 你电脑上的 Git 历史库

- 每一次 commit 都会进来

## 远程仓库（Remote Repository）

- GitHub / GitLab / Gitee 上的仓库

- 用来协作、备份

# Git 的 4 种状态

![](assets/git教程/file-20260130182825120.png)

## untracked（未跟踪）

1)  **📌 含义**

<!-- -->

1.  文件 **存在于工作目录**

2.  **Git 完全不知道它**

3.  不会被版本控制

<!-- -->

2)  **什么时候出现？**

touch test.txt

刚创建的文件就是 Untracked

3)  **🔍 查看状态**

git status

你会看到：

Untracked files:

test.txt

4)  **如何处理？**

git add test.txt

## Modified（已修改）

1)  **📌 含义**

<!-- -->

1)  文件 **已经被 Git 跟踪**

2)  你修改了内容

3)  **但还没告诉 Git 要保存这次修改**

<!-- -->

2)  **📍 什么时候出现？**

vim main.py

3)  **🔍 git status 显示：**

modified: main.py

4)  **👉进入下一状态：**

git add main.py

## Staged（已暂存）

1)  **📌 含义（最容易误解）**

- 文件已经被**放入"暂存区"**

- 表示：

> "我确认，这个文件的当前版本，要进入下一次提交"

📌 **暂存区 = 提交清单**

2)  **📍 什么时候出现？**

git add main.py

3)  **🔍 git status 显示：**

Changes to be committed:

modified: main.py

4)  **👉 进入下一状态：**

git commit -m \"update main logic\"

## Committed（已提交）

1)  **📌 含义**

- 文件的当前状态已经：

  - 被写入 Git 历史

  - 有唯一 commit id

- **这是最安全的状态**

2)  **📍 什么时候出现？**

git commit

3)  **🔍 特点**

- 可以随时回退

- 可以切换分支

- 可以 push 到远程

## 用一条"完整生命周期"串起来（关键）

假设你操作一个文件 app.js：

touch app.js → Untracked

git add app.js → Staged

git commit → Committed

vim app.js → Modified

git add app.js → Staged

git commit → Committed

📌 **Modified 和 Staged 可以反复来回**

**\**

## 这 4 种状态和 Git 的 4 个区域的关系

  -----------------------------------------------------------------------
  **状态**                            **所在区域**
  ----------------------------------- -----------------------------------
  Untracked                           工作区

  Modified                            工作区

  Staged                              暂存区

  Committed                           本地仓库
  -----------------------------------------------------------------------

👉 **状态 = 文件状态**\
👉 **区域 = 文件所在位置**

# 添加和提交文件

## 添加文件（git add）详解

###  git add 是干什么的？

👉 **把当前文件的"某一刻状态"放进暂存区（Stage）**

📌 注意：

- add **不是提交**

- add **可以反复执行**

- add 的是"内容"，不是"文件名"

### 常见 add 用法

#### 添加单个文件

git add main.py

#### 添加多个文件

git add a.txt b.txt

#### 添加当前目录所有修改（最常用）

git add .

📌 包括：

- 新文件

- 修改过的文件

- 删除的文件

###  add 之后发生了什么？

你可以验证：

git status

状态会变成：

Changes to be committed:

modified: main.py

👉 说明已经进入 **Staged（已暂存）**

### 一个重要细节（新手必懂）

git add file

\# 然后又改了 file

此时：

- 已 add 的内容：**staged**

- 后面改的内容：**modified**

👉 add **不会自动跟踪后续修改**

## 提交文件（git commit）详解

### git commit 是干什么的？

👉 **把暂存区的内容，永久保存到 Git 历史中**

- 生成一个 commit

- 有唯一 ID（hash）

- 可以回退、对比、合并

### 最常见的提交方式

git commit -m \"提交说明\"

示例：

git commit -m \"添加用户登录功能\"

📌 **提交说明非常重要**（以后你会感谢自己）

### 如果忘了写 -m

git commit

Git 会打开编辑器让你写说明。

###  commit 后的状态变化

git status

你会看到：

nothing to commit, working tree clean

👉 当前代码 = 仓库中的代码

# 查看版本

## 什么是 Git 日志？

👉 **Git 日志 = 提交历史记录**

每一条日志（commit）至少包含：

- 提交 ID（hash）

- 作者

- 时间

- 提交说明

你可以把它当成：

**代码的"修改时间线 + 责任人记录"**

## 最基础的查看日志

### 查看完整日志

git log

输出类似：

commit a3f2c1d8f9\...

Author: Liu \<liu042901@gmail.com\>

Date: Mon Jan 20 10:12:00 2026 +0800

完成登录功能

📌 特点：

- 最新的在最上面

- 按时间倒序

### 最常用（强烈推荐）

git log \--oneline

输出：

a3f2c1d 完成登录功能

b91e7a2 初始化项目

👉 **一眼看清提交脉络**

## 常用 log 参数（必须掌握）

### 查看最近 N 条提交

git log -n 5

或：

git log \--oneline -5

### 图形化查看分支（非常重要）

git log \--graph \--oneline \--decorate

示例输出：

\* a3f2c1d (HEAD -\> main) 完成登录功能

\* b91e7a2 初始化项目

📌 **理解分支、merge、rebase 必备**

### 查看某个文件的提交历史

git log 文件名

例子：

git log README.md

# git reset回退版本

## git reset 到底在干嘛？

一句话：

git reset 主要是在移动 **HEAD 指针**（当前所在的提交），并且可选地重置
**暂存区** 和 **工作区**。

你可以把 Git 理解成 3 层：

- **工作区**：你正在编辑的文件

- **暂存区**：git add 选中的内容

- **仓库**：git commit 存下来的历史

reset 的三种模式，就是决定**回退时影响到哪几层**。

## 三种回退模式：soft / mixed / hard（必须搞懂）

  ---------------------------------------------------------------------------------------------------------------------------
  **模式**           **HEAD（提交历史）**   **暂存区（stage）**   **工作区（文件内容）**     **常用场景**
  ------------------ ---------------------- --------------------- -------------------------- --------------------------------
  \--soft            ✅回退                 ✅保留                ✅保留                     只想撤回
                                                                                             commit，准备重新组织提交

  \--mixed（默认）   ✅回退                 ✅清空（取消暂存）    ✅保留                     回退
                                                                                             commit，但不想丢代码（最常用）

  \--hard            ✅回退                 ✅清空                ❌丢弃（强制回到旧版本）   确认改动全不要了（慎用）
  ---------------------------------------------------------------------------------------------------------------------------

记忆口诀：

- **soft：只动"提交"**

- **mixed：动"提交+暂存"**

- **hard：动"提交+暂存+工作区"**

## 回退多个提交：HEAD\~n

回退 3 个提交：

git reset \--mixed HEAD\~3

同理：

- \--soft HEAD\~3：撤回 3 次提交，但改动仍保留在暂存区

- \--hard HEAD\~3：直接回到 3 个提交之前，改动全部丢弃

## 回退到某个指定版本（用 commit id）

先 git log \--oneline 找到目标提交，比如 b91e7a2：

git reset \--mixed b91e7a2

- 你会回到 b91e7a2 这个提交

- 之后的提交会"从当前分支历史中消失"（但通常还能用 reflog 找回）

如果你想彻底丢掉后面的改动：

git reset \--hard b91e7a2

## 救命：reset 错了怎么找回？（reflog）

如果你 reset 之后后悔了，大概率能救回来：

git reflog

你会看到 HEAD 曾经到过的提交，比如：

a3f2c1d HEAD@{0}: reset: moving to HEAD\~1

d4e5f6a HEAD@{1}: commit: xxx

想回到 d4e5f6a：

git reset \--hard d4e5f6a

# 删除文件

## 先说清楚一个核心结论（先记住）

**Git 里"删除文件"有两种：**

1️⃣ 只在本地删（Git 不知道）\
2️⃣ 正确删除（Git 记录删除历史）

👉 **正确方式是：让 Git 知道你删除了文件**

## 最推荐、最标准的方式：git rm

### 删除文件（同时告诉 Git）

git rm 文件名

例子：

git rm test.txt

这一步做了两件事：

- ✅ 从 **工作区** 删除文件

- ✅ 自动加入 **暂存区**（等于帮你 add 了删除动作）

你可以马上看状态：

git status

会看到：

deleted: test.txt

### 提交删除记录（非常重要）

git commit -m \"删除 test.txt\"

📌 这一步之后：

- 文件真的从 Git 历史的"当前版本"中消失

- 但 **历史版本里仍然能找到它**

## 用普通 rm 删除文件行不行？

### 可以，但要多一步（不推荐新手）

rm test.txt

此时：

- 文件在工作区没了

- **Git 还不知道你"确认删除"**

你再看：

git status

会显示：

deleted: test.txt

但这是 **"未暂存的删除"**

你还需要：

git add test.txt

\# 或

git add .

然后再：

git commit -m \"删除 test.txt\"

📌 所以总结：

  -----------------------------------------------------------------------
  **方法**                            **是否推荐**
  ----------------------------------- -----------------------------------
  git rm file                         ✅ 强烈推荐

  rm file + git add                   ⚠️ 可以，但容易忘
  -----------------------------------------------------------------------

## 只从 Git 中删除，但本地保留文件（非常重要）

1)  **场景：**

"这个文件不想被 Git 管了，但我本地还要用"

例如：

- 配置文件

- 本地缓存

- 私密信息

2)  **正确做法：**

git rm \--cached 文件名

例子：

git rm \--cached config.json

效果：

- ❌ Git 不再跟踪这个文件

- ✅ 本地文件仍然存在

通常要 **配合 .gitignore 使用**：

echo config.json \>\> .gitignore

git commit -m \"停止跟踪 config.json\"

# git diff查看差异

## 理解 git diff

**git diff = 查看"两个状态之间"的代码差异**

最常见的三种状态：

- 工作区

- 暂存区

- 最近一次提交（HEAD）

## 5 个最常用 diff 命令（重点）

### 查看「工作区 vs 暂存区」（最常用）

git diff

**看什么？**\
👉 你已经改了，但**还没 git add** 的内容

📌 提交前必看

### 查看「暂存区 vs HEAD」（即将提交什么）

git diff \--staged

\# 或

git diff \--cached

**看什么？**\
👉 如果现在 git commit，**会提交哪些改动**

📌 非常重要

### 查看「工作区 vs HEAD」（所有改动）

git diff HEAD

**看什么？**\
👉 所有改动（已 add + 未 add）

### 只看某一个文件（高频）

git diff 文件名

git diff \--staged 文件名

例子：

git diff app.js

git diff \--staged app.js

### 只看改了哪些文件（不看内容）

git diff \--name-only

git diff \--staged \--name-only

## git diff 输出你应该怎么看（快速读懂）

示例输出：

diff \--git a/app.js b/app.js

index e69de29..3b18e9a 100644

\-\-- a/app.js

+++ b/app.js

@@ -1,3 +1,4 @@

+console.log(\"hello\")

内容解释：

1)  **第一行：diff 的对象是谁？**

diff \--git a/app.js b/app.js

👉 含义：

**对比的是同一个文件 app.js 的两个版本**

- a/app.js：修改前

- b/app.js：修改后

📌 这里的 a / b 只是 Git 的内部命名\
📌 **不是目录，也不是分支**

1)  第二行：index（可以忽略，但我给你解释）

index e69de29..3b18e9a 100644

👉 含义：

- e69de29：修改前内容的哈希

- 3b18e9a：修改后内容的哈希

- 100644：文件权限（普通文件）

📌 **新手完全可以忽略这一行**

2)  **第三 & 四行：旧文件 vs 新文件**

\-\-- a/app.js

+++ b/app.js

含义：

- \-\--：旧版本

- +++：新版本

📌 这两行只是在说：

"下面开始展示 app.js 的变化了"

3)  **第5行 最关键的一行：@@ -1,3 +1,4 @@**

@@ -1,3 +1,4 @@

这一行**是 diff 的坐标信息**，非常重要。

拆开来看：

-1,3 +1,4

a)  -1,3（旧文件）

- 从第 **1 行** 开始

- 一共 **3 行**

b)  +1,4（新文件）

- 从第 **1 行** 开始

- 一共 **4 行**

👉 **新文件比旧文件多了一行**

4)  **真正的代码差异（你最该看的）**

+console.log(\"hello\")

5)  **结合起来，用一句完整的人话说**

这段 diff 表示：

在 app.js 文件中，\
从第 1 行开始，\
原来有 3 行，\
现在变成了 4 行，\
新增的那一行是：\
console.log(\"hello\")

总结：

你只需要记住 3 件事：

- \+ 开头：**新增**

- \- 开头：**删除**

- 没符号：上下文

# 拉取

## git fetch：最安全的"只看下载"

fetch 只是将远程仓库的最新内容下载到本地的"远程追踪分支"中（如
origin/main），但**不会修改**你当前正在写的代码。

- **用法：** git fetch origin

- **优点：** 安全。你可以先用 git log 或 git diff
  看看别人改了什么，确认没问题后再合并。

- **状态变化：**

## git pull：一键更新（Fetch + Merge）

这是最常用的命令。它会自动执行 git fetch，紧接着立即执行 git
merge，将远程更改直接合并到你当前的分支中。

- **用法：** git pull origin \<分支名\>

- **注意：** 如果你和同事改了同一行，这个命令会直接触发 **Merge
  Conflict（合并冲突）**，需要你手动解决。

# gitignore的用法

## .gitignore 是干嘛的？（先给结论）

一句话：

**.gitignore 用来告诉 Git：哪些文件我不想被版本控制**

典型不想提交的东西：

- 编译产物

- 日志

- 本地配置

- 缓存

- 系统垃圾文件

## .gitignore 的基本规则（必须知道）

### 每一行是一条规则

node_modules/

dist/

### 注释用 \#

\# 忽略日志文件

\*.log

### 支持通配符（最常用）

  -------------------------
  **规则**   **含义**
  ---------- --------------
  \*         任意字符串

  ?          任意一个字符

  \*\*       任意多级目录
  -------------------------

示例：

\*.log

temp-\*.txt

## 最常用的 .gitignore 写法（直接能用）

### 忽略某一类文件（后缀）

\*.log

\*.tmp

\*.swp

\*.bak

### 忽略目录（非常常见）

node_modules/

dist/

build/

target/

📌 结尾的 / 很重要，表示目录。

###  忽略某个具体文件

config.json

.env

### 忽略所有，但保留一个（反向规则）

\*

!.gitignore

!README.md

📌 ! 表示"例外（不忽略）"

### 忽略某目录下的某类文件

logs/\*.log

### 忽略多级目录中的文件（\*\*）

\*\*/\*.log

**\**

## .gitignore 的"优先级 & 生效规则"（新手最容易踩坑）

### .gitignore **不会**影响已经被 Git 跟踪的文件

❌ 错误理解：

"我把文件写进 .gitignore 了，怎么 Git 还在管？"

✅ 正确理解：

**.gitignore 只对"未被跟踪的文件"有效**

### 正确做法（非常重要）

git rm \--cached 文件名

然后再提交：

git commit -m \"ignore xxx file\"

###  .gitignore 规则是从上到下匹配

- 先匹配到的规则生效

- 后面的 ! 可以反转

### 不同层级的 .gitignore

Git 会按顺序读取：

1.  项目里的 .gitignore

2.  .git/info/exclude（项目私有）

3.  全局忽略文件（\~/.config/git/ignore 或 \~/.gitignore_global）

**\**

# ssh配置和克隆仓库

## SSH 的工作原理

1)  你电脑生成一对钥匙：

    a)  🔐 私钥（留在你电脑，绝不外传）

    b)  🔓 公钥（交给 GitHub）

2)  GitHub 以后看到你的私钥签名：

    a)  就知道是你

    b)  允许你操作仓库

## SSH 配置

下面以 **macOS / Linux** 为例

### ①检查是否已有 SSH Key

ls \~/.ssh

如果你看到类似：

id_ed25519

id_ed25519.pub

👉 说明你**已经有 SSH key**\
可以直接跳到 **第 ③ 步**

### ② 生成新的 SSH Key（推荐 ed25519）

ssh-keygen -t ed25519 -C \"你的GitHub邮箱\"

例如：

ssh-keygen -t ed25519 -C \"liu042901@gmail.com\"

过程说明：

- -t ed25519：更安全、更新

- -C：注释，用来标识这把 key

提示时：

- Enter file in which to save the key → **直接回车**

- Enter passphrase → 可以留空（新手建议留空）

生成后会得到：

\~/.ssh/id_ed25519 （私钥）

\~/.ssh/id_ed25519.pub （公钥）

### ③ 启动 ssh-agent 并加载私钥（macOS 推荐）

eval \"\$(ssh-agent -s)\"

ssh-add \~/.ssh/id_ed25519

👉 这一步是为了让 Git 在后台能用你的私钥。

### ④ 把公钥添加到 GitHub

1)  **复制公钥内容**

cat \~/.ssh/id_ed25519.pub

复制输出的 **全部内容**（以 ssh-ed25519 开头）。

2)  **GitHub 页面操作**

<!-- -->

1.  GitHub → **Settings**

2.  **SSH and GPG keys**

3.  **New SSH key**

4.  Title：随便（如 MacBook）

5.  Key：粘贴公钥

6.  Save

### ⑤ 验证 SSH 是否配置成功（非常重要）

ssh -T git@github.com

第一次会问：

Are you sure you want to continue connecting?

输入：

yes

成功的话你会看到：

Hi yourname! You\'ve successfully authenticated, but GitHub does not
provide shell access.

👉 **看到这行，说明 SSH 配置完成**

## 用 SSH 克隆仓库（重点）

### 获取 SSH 地址（不是 HTTPS）

在 GitHub 仓库页面：

- 点击 **Code**

- 选择 **SSH**

- 复制类似：

git@github.com:yourname/demo.git

![](assets/git教程/file-20260130182825119.png)

### 克隆仓库

git clone git@github.com:yourname/demo.git

Git 会：

- 创建同名目录

- 下载代码

- 自动配置 origin

- 关联远程分支

### 验证克隆结果

cd demo

git remote -v

你应该看到：

origin git@github.com:yourname/demo.git (fetch)

origin git@github.com:yourname/demo.git (push)

👉 说明你现在是 **SSH 方式连接远程仓库**

# 关联本地仓库和远程仓库

## 先给你一张"最常用流程图

本地仓库（已有 commit）

↓

git remote add origin \<url\>

↓

git push -u origin main

👉 **90% 情况你只需要这 2 条命令**

## 前提条件

在关联远程仓库之前，本地必须满足：

git init

git add .

git commit -m \"initial commit\"

⚠️ **没有 commit，后面的 push 一定会失败**

## 关联本地仓库和远程仓库（核心内容）

### 添加远程仓库地址

git remote add origin \<远程仓库地址\>

示例（SSH，推荐）：

git remote add origin git@github.com:yourname/demo.git

示例（HTTPS）：

git remote add origin https://github.com/yourname/demo.git

📌 说明：

- origin：远程仓库的**别名**

- 不是固定名字，但**强烈建议用 origin**

### 检查是否关联成功

git remote -v

正确输出应类似：

origin git@github.com:yourname/demo.git (fetch)

origin git@github.com:yourname/demo.git (push)

### 第一次推送并建立分支关联

git push -u origin main

📌 这条命令做了三件事：

1.  把本地 main 推送到远程

2.  在远程创建 origin/main

3.  建立 **本地 main ↔ 远程 origin/main 的跟踪关系**

### 以后最常用的推送命令（你会天天用）

git push

因为已经有 -u 关联过了。

## 几个你必须会的"关联相关命令

### 查看本地分支和远程分支的关系

git branch -vv

你会看到：

\* main a3f2c1d \[origin/main\] initial commit

👉 \[origin/main\] 就是关联关系

### 查看远程仓库信息

git remote show origin

### 修改已存在的远程仓库地址（非常常用）

git remote set-url origin 新地址

例子（HTTPS → SSH）：

git remote set-url origin git@github.com:yourname/demo.git

### 删除远程仓库关联（不常用，但要知道）

git remote remove origin

# 分支简介和基本操作

## 分支是什么？

**分支 = 一条独立的开发线路**

- 不影响主线（main）

- 用来开发新功能、修 Bug、做实验

📌 **现实类比**：\
main 是正式道路，分支是临时施工便道。

## 你必须认识的 3 种分支

  -----------------------------------------------------------------------
  **分支**                            **用途**
  ----------------------------------- -----------------------------------
  main                                稳定、可发布的代码

  feature/\*                          新功能开发

  bugfix/\*                           修复问题
  -----------------------------------------------------------------------

👉 **不要直接在 main 开发**（这是职业习惯）

## 最常用的分支命令（核心）

### 查看分支（第一个要会）

git branch

- 当前分支前有 \*

查看本地 + 远程：

git branch -a

### 创建分支（不切换）

git branch feature-login

### 创建并切换分支（最常用）

git checkout -b feature-login

👉 一步到位：**创建 + 切换**

（新版本 Git 也推荐）

git switch -c feature-login

###  切换分支

git checkout main

或：

git switch main

📌 切换前：

- 工作区必须是干净的（已提交或 stash）

## 合并分支（merge）--- 必会

### 合并分支的基本命令

git merge 分支名

⚠️ 记住一句话：

**在哪个分支上合并，就把"别的分支"合并进来**

示例：

git checkout main

git merge feature-login

这里就是把feature-login分支合并到main分支。

## 解决冲突（一定会遇到）

冲突原因：

- 两个分支修改了同一行

解决步骤：

\# 打开冲突文件，手动修改

git add 冲突文件

git commit

## 删除分支（收尾工作）

### 删除本地分支

git branch -d feature-login

⚠️ 未合并会失败（安全机制）

强制删除：

git branch -D feature-login

### 删除远程分支（常用）

git push origin \--delete feature-login

**把远程仓库 origin 上的 feature-login 分支删除掉**

⚠️ **只删远程分支，不删本地分支**

**逐段拆解（非常重要）**

1️⃣ git push

👉 本质含义：

**对远程仓库做"写操作"**

通常是推送代码，这里是**推送一个"删除请求"**。

2️⃣ origin

👉 远程仓库的名字（别名）

相当于在说：

"我要操作的是 GitHub 上那个仓库"

3️⃣ \--delete

👉 告诉 Git：

"这次 push 不是上传代码，而是删除远程内容"

4️⃣ feature-login

👉 要删除的**远程分支名**

完整意思连起来就是：

**请把 GitHub（origin）上的 feature-login 分支删除**

## 和远程分支配合（最常用）

### 推送新分支到远程

git push -u origin feature-login

### 拉取远程分支

git fetch

git checkout feature-login

# 解决合并冲突

## 什么是合并冲突

**两个分支改了同一个文件的同一部分，Git 不知道该选谁**

所以它停下来让你来决定。

最常见的冲突产生场景（99% 情况）

git checkout main

git merge feature-login

如果你看到：

CONFLICT (content): Merge conflict in app.js

Automatic merge failed; fix conflicts and then commit the result.

👉 **这就叫合并冲突**

**\**

## 解决合并冲突的标准流程（必背）

### 步骤 1️⃣：确认有哪些文件冲突了

git status

你会看到：

both modified: app.js

### 步骤 2️⃣：打开冲突文件（关键）

文件里会看到这种结构：

\<\<\<\<\<\<\< HEAD

main 分支的内容

=======

feature-login 分支的内容

\>\>\>\>\>\>\> feature-login

解释：

1.  \<\<\<\<\<\<\< HEAD\
    👉 当前分支（你在哪个分支 merge，就代表哪个分支）

2.  =======\
    👉 分隔线

3.  \>\>\>\>\>\>\> feature-login\
    👉 被合并进来的分支

### 步骤 3️⃣：手动修改代码（你来裁决）

你需要做三选一：

✅ 保留当前分支

main 分支的内容

✅ 保留合并分支

feature-login 分支的内容

✅ 两个都要（最常见）

main 分支的内容

feature-login 分支的内容

⚠️ **必须删除所有冲突标记**：

\<\<\<\<\<\<\<

=======

\>\>\>\>\>\>\>

### 步骤 4️⃣：标记为"已解决"（非常重要）

git add app.js

📌 这一步不是提交，而是告诉 Git：

"这个冲突我已经处理好了"

### 步骤 5️⃣：完成合并提交

git commit

Git 会自动生成 merge commit 信息，直接保存即可。

## 合并冲突时你最常用的 5 个命令

git status \# 看冲突文件

git diff \# 看冲突内容

git add \<file\> \# 标记已解决

git commit \# 完成合并

git merge \--abort \# 放弃这次合并

## 如果你不想解决，想"撤销这次合并"

场景：冲突太多 / 合错分支

git merge \--abort

👉 效果：

- 回到 merge 之前

- 所有冲突消失

- 工作区恢复原样

# 回退和rebase

## 先给你一张"决策表"（先会用）

  -----------------------------------------------------------------------
  **你遇到的情况**                    **用什么**
  ----------------------------------- -----------------------------------
  提交还没 push，想回退               git reset

  已经 push，不想改历史               git revert

  想整理提交记录（更干净）            git rebase

  分支合并前，让历史变直              git rebase
  -----------------------------------------------------------------------

👉 **80% 情况：reset + rebase 就够了**

## 回退（reset / revert）------解决"后悔"

### git reset（最常用，本地回退）

**reset = 移动 HEAD 指针（改历史）**

⚠️ **只建议在"没 push"时使用**

**之前讲了，看前面的。**

### git revert（已 push 的回退，安全）

**revert = 用一次新提交，抵消旧提交**

git revert 提交ID

特点：

- 不改历史

- 团队协作最安全

- 会生成一个"反向提交"

📌 **已 push 的提交，优先用 revert**

## rebase 是什么？（一句话就够）

**rebase = 把你的提交"挪到"另一个提交后面**

目标：

- 历史更干净

- 没有多余的 merge commit

如下所示：

![](assets/git教程/file-20260130182825117%201.png)
![](assets/git教程/file-20260130182825116.png)
