---
title: "Linux 权限管理基础"
created: 2026-07-29
updated: 2026-07-29
tags: [linux, 权限, chmod]
status: completed
source_project: linux-commands
---

> [!note]
> 本章将带你系统理解 Linux 的权限模型。从文件的 rwx 权限位到 chmod 的数字/符号模式，从所有者管理到 SUID/SGID/Sticky Bit 特殊权限，再到 umask 默认权限控制。学完本章，你将能精准控制谁可以读、写、执行你的文件——这是 Linux 安全的第一道防线，也是日常运维中最容易出问题的地方。

---

## 6.1 理解文件权限模型

在 Linux 中，**一切皆文件**，每个文件都有一套权限位（Permission Bits）来控制访问。这是多用户系统的基石。

### 查看权限位

用 `ls -l` 查看文件的详细信息，第一列就是权限位：

```bash
$ ls -lh /etc/passwd
-rw-r--r-- 1 root root 2.8K Jul 28 10:00 /etc/passwd

$ ls -ld /tmp
drwxrwxrwt 10 root root 4.0K Jul 28 12:00 /tmp

$ ls -l script.sh
-rwxr-xr-x 1 user user 512 Jul 28 09:50 script.sh
```

第一列的 10 个字符可以分解为：

```
- r w x  r - x  r - x
│ └┬┘  └┬┘  └┬┘
│  │     │    └── Others（其他人）
│  │     └─────── Group（所属组）
│  └───────────── User/Owner（所有者）
└──────────────── 文件类型（- 文件，d 目录，l 链接）
```

### 三种权限的含义

| 权限 | 对文件的意义 | 对目录的意义 |
|------|-------------|-------------|
| **r** (读) | 读取文件内容（如 `cat file`） | 列出目录内容（如 `ls dir`） |
| **w** (写) | 修改文件内容 | 在目录中创建/删除文件 |
| **x** (执行) | 作为程序执行 | 进入目录（如 `cd dir`） |

> [!tip] 目录的执行权限是关键
> 很多人以为目录的 `r` 权限就够了，实际上**没有 `x` 权限，你连 `cd` 进目录都不行**。如果你只有目录的 `r` 权限，可以 `ls` 看到文件名，但无法访问文件内容和元数据。
>
> ```bash
> # 创建测试
> $ mkdir testdir && echo "secret" > testdir/file.txt
> $ chmod 644 testdir        # 去掉目录的 x 权限
> $ ls testdir               # 有 r 权限，可以看到文件名
> file.txt
> $ cat testdir/file.txt     # 但无法访问文件内容
> cat: testdir/file.txt: Permission denied
> ```

### 三种主体（ugo）

| 主体 | 缩写 | 说明 |
|------|:----:|------|
| **u**ser | u | 文件所有者（owner） |
| **g**roup | g | 文件所属组的所有成员 |
| **o**thers | o | 其他所有人 |

### 常用权限组合速查

```bash
-rw-------   (600)   # 私密文件，仅所有者可读写
-rw-r--r--   (644)   # 普通文件默认，所有者写，其他人只读
-rwxr-xr-x   (755)   # 可执行文件/脚本
-rwx------   (700)   # 私密脚本，仅所有者可执行
-rw-rw-rw-   (666)   # 全开放读写（极少用）
-rwxrwxrwx   (777)   # ⚠️ 全开放——绝对不要用
```

---

## 6.2 chmod：修改文件权限

`chmod`（change mode）是修改权限的命令，支持**数字模式**和**符号模式**两种写法。建议两种都掌握，数字模式适合快速设置，符号模式适合微调。

### 数字模式

每个权限用一个数字表示：

```
r = 4    w = 2    x = 1
```

三个数字分别代表 u / g / o 的权限，每个数字是三种权限值的**和**：

```
rwx = 4+2+1 = 7
rw- = 4+2+0 = 6
r-x = 4+0+1 = 5
r-- = 4+0+0 = 4
-wx = 0+2+1 = 3  （极少用）
-w- = 0+2+0 = 2  （极少用）
--x = 0+0+1 = 1  （极少用）
```

**实战示例**：

```bash
# 设置脚本为所有者可读写执行，组和其他人只读执行
chmod 755 script.sh

# 设置配置文件为所有者可读写，其他人只读
chmod 644 config.yml

# 设置私密密钥文件为仅所有者可读
chmod 600 id_rsa

# 递归设置目录下所有文件和子目录
chmod -R 755 /opt/myapp/
```

### 符号模式

格式：`chmod <主体><操作><权限> 文件名`

| 符号 | 含义 |
|:----:|------|
| `u` | user（所有者） |
| `g` | group（组） |
| `o` | others（其他人） |
| `a` | all（所有人，等同于 ugo） |
| `+` | 添加权限 |
| `-` | 移除权限 |
| `=` | 设置精确权限 |

**实战示例**：

```bash
chmod u+x script.sh       # 为所有者添加执行权限
chmod g-w file.txt        # 移除组的写权限
chmod o=r file.txt        # 其他人设置为只读（覆盖原有权限）
chmod a+r file.txt        # 所有人添加读权限
chmod u=rwx,g=rx,o=rx     # 等价于 chmod 755

# 常见微调场景
chmod +x script.sh        # 所有人加执行权限（不指定主体时默认 a）
chmod -R g+w /opt/shared/ # 递归为组添加写权限
```

> [!example] 数字 vs 符号：何时用哪种？
>
> ```bash
> # 数字模式适合：完整设置所有权限
> chmod 644 file.txt      # 清晰、简洁、一次到位
>
> # 符号模式适合：只调整部分权限
> chmod +x script.sh      # 只想加执行位
> chmod g-w file.txt      # 只想移除组的写权限
> chmod -R g+w /shared/   # 递归给组加写权限
> ```
>
> 一个实用的做法：用 `chmod 644` / `chmod 755` / `chmod 600` 三组数字覆盖 90% 的场景，其他情况用符号模式微调。

### 理解 chmod 的递归行为

```bash
chmod 755 /opt/myapp/          # 只改目录本身
chmod -R 755 /opt/myapp/       # 改目录及其所有子文件和子目录

# ⚠️ 但这样有个问题：普通文件不应该有 x 权限
# 更精细的做法是分别设置：
find /opt/myapp/ -type f -exec chmod 644 {} \;   # 文件设 644
find /opt/myapp/ -type d -exec chmod 755 {} \;   # 目录设 755
```

> [!warning] 不要对普通文件加执行权限
> 如果你 `chmod -R 755` 一个目录，里面的所有普通文件（如文本文件、图片等）都会被加上 `x` 执行位。虽然一般不会造成功能性错误，但这是不好的安全习惯。建议对文件和目录分别设置。

---

## 6.3 chown / chgrp：管理文件所有者

### chown — 修改所有者和所属组

```bash
chown user file.txt              # 修改文件所有者为 user
chown user:group file.txt        # 同时修改所有者和组
chown :group file.txt            # 仅修改所属组（省略所有者部分）
chown user: file.txt             # 修改所有者并设为同名的组

# 递归修改目录
chown -R www-data:www-data /var/www/
```

> [!warning] chown 需要 root 权限
> 普通用户无法把自己的文件所有权转给其他用户——这是安全设计，防止你通过"赠送"文件绕过磁盘配额限制。只有 root 可以自由修改所有权。

### chgrp — 仅修改所属组

`chgrp` 是 `chown :group` 的独立版本，功能完全一样，但更语义化：

```bash
chgrp developers project/    # 修改目录的组为 developers
chgrp -R developers /shared/ # 递归修改
```

### 实战场景：部署 Web 应用

这是权限管理最典型的场景。假设你用 `deploy` 用户上传代码，但 Nginx 用 `www-data` 用户运行：

```bash
# 1. 上传代码后，设置所有者
sudo chown -R deploy:www-data /var/www/myapp/

# 2. 文件权限：所有者可写，组和其他人只读
find /var/www/myapp/ -type f -exec chmod 644 {} \;

# 3. 目录权限：所有者可写执行，组和其他人只读执行
find /var/www/myapp/ -type d -exec chmod 755 {} \;

# 4. 让 www-data 用户可以进入目录
chmod g+rx /var/www/myapp/
```

---

## 6.4 特殊权限：SUID / SGID / Sticky Bit

除了基本的 rwx 权限，Linux 还有三个特殊权限位，用于更精细的控制。

### SUID（Set User ID）`u+s`

当可执行文件设置了 SUID，任何用户运行它时，都会以**文件所有者**的身份执行，而不是以运行者的身份。

```
权限位显示：-rwsr-xr-x   （s 出现在所有者的 x 位置）
```

**经典例子：`passwd` 命令**

```bash
$ which passwd
/usr/bin/passwd
$ ls -l /usr/bin/passwd
-rwsr-xr-x 1 root root 67976 Jul 15  2024 /usr/bin/passwd
```

`passwd` 的所有者是 root，普通用户需要修改 `/etc/shadow` 文件（仅 root 可写）。通过 SUID，普通用户运行 `passwd` 时临时获得 root 权限，才能更新自己的密码。

```bash
# 设置 SUID
chmod u+s /path/to/program
# 或用数字模式（4 开头）
chmod 4755 /path/to/program   # rwsr-xr-x
```

### SGID（Set Group ID）`g+s`

SGID 有两种行为：
- **对文件**：以文件所属组的身份执行（类似 SUID 但作用于组）
- **对目录**：在该目录下创建的新文件，自动继承目录的所属组

```
权限位显示：drwxrws---   （s 出现在组的 x 位置）
```

**SGID 对目录是最实用的特性**。在协作项目中，团队成员的文件组保持一致，避免反复 `chgrp`：

```bash
# 设置 SGID
sudo chgrp developers /shared/project/
sudo chmod g+s /shared/project/

# 现在，任何用户在 /shared/project/ 下创建的文件
# 都会自动属于 developers 组
touch /shared/project/test.txt
$ ls -l /shared/project/test.txt
-rw-r--r-- 1 alice developers 0 Jul 28 14:00 test.txt
```

```bash
# 设置 SGID
chmod g+s /shared/dir/
# 或用数字模式（2 开头）
chmod 2755 /shared/dir/   # rwxr-sr-x
```

### Sticky Bit `+t`

Sticky Bit 主要用于**共享目录**。设置了 Sticky Bit 的目录，用户只能删除**自己拥有的文件**，不能删除别人的文件。

```
权限位显示：drwxrwxrwt   （t 出现在其他人的 x 位置）
```

**经典例子：`/tmp` 目录**

```bash
$ ls -ld /tmp
drwxrwxrwt 10 root root 4096 Jul 28 12:00 /tmp
```

`/tmp` 是全局可写的共享目录，任何人都可以创建文件，但 Sticky Bit 确保只有文件所有者（或 root）才能删除它。

```bash
# 设置 Sticky Bit
chmod +t /shared/temp/
# 或用数字模式（1 开头）
chmod 1777 /shared/temp/   # rwxrwxrwt
```

### 特殊权限速查表

| 特殊权限 | 数字位 | 符号 | 显示位置 | 核心用途 |
|----------|:------:|:----:|:--------:|----------|
| SUID | 4 | `u+s` | 所有者 x 位 → `s` | 以文件所有者身份执行 |
| SGID | 2 | `g+s` | 组 x 位 → `s` | 目录下新文件继承组 |
| Sticky Bit | 1 | `+t` | 其他人 x 位 → `t` | 防删除共享目录 |

> [!warning] 特殊权限的安全风险
> - **SUID 是双刃剑**：有 SUID 的程序如果有漏洞，攻击者可能利用它提权。你的系统上应该极少有 SUID 文件（通常只有 `passwd`、`sudo`、`ping` 等几个）。
> - **查找所有 SUID 文件**：
>   ```bash
>   find / -perm -4000 -type f 2>/dev/null
>   ```
> - **如果发现不明 SUID 文件，立刻调查**，可能是系统被入侵的迹象。

---

## 6.5 umask：控制默认权限

每次你创建文件或目录时，系统都会给它一个默认权限。`umask` 定义了要从这个默认权限中"扣掉"哪些位。

### umask 的计算规则

```bash
文件默认最大权限：666  (rw-rw-rw-)
目录默认最大权限：777  (rwxrwxrwx)

最终权限 = 最大权限 - umask 值
```

**最常见的 umask 值：022**

```bash
文件：666 - 022 = 644  (rw-r--r--)
目录：777 - 022 = 755  (rwxr-xr-x)
```

### 查看和设置 umask

```bash
# 查看当前 umask
$ umask
0022

# 以符号形式查看
$ umask -S
u=rwx,g=rx,o=rx
```

### 不同 umask 值的效果

| umask 值 | 文件权限 | 目录权限 | 适用场景 |
|:--------:|:--------:|:--------:|----------|
| 022 | 644 (`rw-r--r--`) | 755 (`rwxr-xr-x`) | 默认——其他人可读 |
| 002 | 664 (`rw-rw-r--`) | 775 (`rwxrwxr-x`) | 团队协作——组内可写 |
| 027 | 640 (`rw-r-----`) | 750 (`rwxr-x---`) | 安全——组内只读，他人无权限 |
| 077 | 600 (`rw-------`) | 700 (`rwx------`) | 私密——仅所有者可访问 |

> [!example] 团队协作的 umask 配置
>
> 假设你和团队成员共享一个开发目录，希望组内成员都能读写：
>
> ```bash
> # 在 ~/.bashrc 或 ~/.zshrc 中设置
> umask 002
>
> # 同时在共享目录设置 SGID
> sudo chgrp -R developers /shared/project/
> sudo chmod -R g+s /shared/project/
> ```
>
> 这样团队新创建的文件自动为 `664`（组内可写），且自动继承 `developers` 组。

### 持久化 umask 设置

```bash
# 对当前用户生效，写入 shell 配置文件
echo "umask 027" >> ~/.bashrc
source ~/.bashrc

# 对系统全局生效（影响所有用户）
# 编辑 /etc/profile 或 /etc/bash.bashrc
# 或 /etc/login.defs 中的 UMASK 配置
```

---

## 6.6 实战：Web 服务器权限设置

把前面学的知识综合起来，模拟一个真实的 Nginx Web 服务器权限配置场景。

### 场景描述

- 你通过 `deploy` 用户上传和管理代码
- Nginx 以 `www-data` 用户运行
- 代码部署在 `/var/www/example.com/`
- 需要确保：
  - `deploy` 用户能读写所有文件（负责更新代码）
  - `www-data` 用户能读取静态文件（负责提供 HTTP 服务）
  - 其他人不能访问（安全要求）
  - 上传目录需要 `www-data` 可写（用户上传文件）

### 完整配置流程

```bash
# 第一步：创建目录并设置所有者和组
sudo mkdir -p /var/www/example.com
sudo chown deploy:www-data /var/www/example.com/

# 第二步：设置目录权限
# 所有者（deploy）完全控制，组（www-data）可进入和读取
sudo chmod 750 /var/www/example.com/

# 第三步：设置 SGID，确保新文件继承组
sudo chmod g+s /var/www/example.com/

# 第四步：部署代码后设置文件权限
# 文件：所有者可读写，组可读
find /var/www/example.com/ -type f -exec chmod 640 {} \;
# 目录：所有者可读写执行，组可读执行
find /var/www/example.com/ -type d -exec chmod 750 {} \;

# 第五步：对上传目录特殊处理（需要组可写）
sudo mkdir -p /var/www/example.com/uploads
sudo chmod 770 /var/www/example.com/uploads/
```

### 验证权限配置

```bash
# 以 deploy 用户身份测试
$ su deploy
$ ls -la /var/www/example.com/
total 20K
drwxr-s--- 4 deploy www-data 4.0K Jul 28 15:00 .
drwxr-xr-x 3 root   root     4.0K Jul 28 14:00 ..
-rw-r----- 1 deploy www-data  256 Jul 28 15:00 index.html
drwxr-x--- 2 deploy www-data 4.0K Jul 28 15:00 css
drwxrwx--- 2 deploy www-data 4.0K Jul 28 15:00 uploads

# deploy 可以写任何文件
$ echo "update" >> index.html    # 成功

# 以 www-data 用户测试
$ su www-data
$ cat /var/www/example.com/index.html   # 可以读取
$ rm /var/www/example.com/index.html    # 不能删除（没有 w 权限）
rm: remove write-protected regular file 'index.html'? y
rm: cannot remove 'index.html': Permission denied

# www-data 可以写入 uploads 目录
$ touch /var/www/example.com/uploads/test.txt   # 成功

# 其他用户无法访问
$ su nobody
$ ls /var/www/example.com/
ls: cannot open directory '/var/www/example.com/': Permission denied
```

### 简化检查脚本

```bash
#!/bin/bash
# 检查 /var/www/example.com 的文件权限是否合规
DIR="/var/www/example.com"
echo "=== 权限检查报告 ==="

echo ""
echo "目录结构概览："
ls -laR "$DIR" 2>&1 | head -20

echo ""
echo "合规检查："
# 检查是否存在 777 的权限
BAD_PERMS=$(find "$DIR" -perm /777 -type f 2>/dev/null)
if [ -n "$BAD_PERMS" ]; then
    echo "[WARNING] 发现 777 权限文件："
    echo "$BAD_PERMS"
fi

# 检查所有者是否都是 deploy
BAD_OWNER=$(find "$DIR" ! -user deploy 2>/dev/null)
if [ -n "$BAD_OWNER" ]; then
    echo "[WARNING] 发现非 deploy 所有的文件："
    echo "$BAD_OWNER"
fi
```

> [!tip] 权限管理的黄金法则
> 1. **最小权限原则**：只给所需的最小权限，不给多余的
> 2. **先拒绝再允许**：从严格的权限开始，按需放宽
> 3. **文件 640 / 目录 750**：这是 Web 服务最常用的组合
> 4. **SGID 避免组混乱**：共享目录一定要设 `g+s`
> 5. **定期审计 SUID**：用 `find / -perm -4000` 检查异常

---

## 本章总结

- **文件权限三要素**：读（r=4）、写（w=2）、执行（x=1），分别对文件所有者（u）、所属组（g）、其他人（o）设置
- **chmod 数字模式**（如 `644`、`755`、`600`）适合完整设置，**符号模式**（如 `u+x`、`g-w`）适合微调
- **chown** 修改文件所有者/组，需要 root 权限；**chgrp** 只改所属组
- **特殊权限**：SUID（以所有者身份执行）、SGID（目录下新文件继承组）、Sticky Bit（防删除共享目录）
- **umask** 控制新建文件的默认权限，团队协作时设为 `002`，安全敏感环境设为 `027` 或 `077`
- **Web 服务器权限场景**：所有者完全控制 + 组只读 + 其他人无权限（640/750），配合 SGID 保持组一致性

## 下一步

第七章将进入**磁盘与存储管理**，学习如何查看磁盘空间（`df`/`du`）、分区操作（`fdisk`）、格式化（`mkfs`）、挂载卸载（`mount`/`umount`），以及磁盘空间告警的排查流程。这些是服务器运维的基本功，当你遇到"磁盘满了"的告警时，第七章就是你的救援手册。
