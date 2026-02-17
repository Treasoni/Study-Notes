---
tags: [linux]
---

# Linux 文件权限管理

> [!info] 概述
> **Linux 文件权限就像房子的门锁系统** - 房主（所有者）有万能钥匙，家庭成员（所属组）有部分钥匙，其他人（others）只能进入开放区域。

## 核心概念 💡

### 权限三要素
| 要素 | 英文 | 说明 |
|------|------|------|
| **所有者** | User (u) | 文件创建者或拥有者 |
| **所属组** | Group (g) | 与文件关联的用户组 |
| **其他人** | Others (o) | 既不是所有者也不在所属组的用户 |

### 三种权限
| 权限 | 字母 | 数字 | 含义 |
|------|------|------|------|
| **读** | r | 4 | 可以查看文件内容或列出目录内容 |
| **写** | w | 2 | 可以修改文件内容或在目录中创建/删除文件 |
| **执行** | x | 1 | 可以运行文件或进入目录 |

### 权限表示方式
```bash
-rw-r--r-- 1 alice alice 4096 file.txt
↑↑↑↑↑↑↑↑↑ ↑ ↑ ↑    ↑    ↑
│││││││││ │ │ │    │    └─ 文件名
│││││││││ │ │ │    └────── 文件大小
│││││││││ │ │ └─────────── 所属组
│││││││││ │ └───────────── 所有者
││││││││└─────────────── 硬链接数
│└┬┘└┬┘└┬┘
│ │  │  └─ 其他用户权限
│ │  └──── 所属组权限
└ └──────── 所有者权限
```

## 操作步骤

### 方法一：chmod - 修改权限

#### 数字方式（推荐）
```bash
# 常用权限数字速查
chmod 600 file.txt   # 仅所有者可读写（密钥文件）
chmod 644 file.txt   # 所有者读写，其他人只读（配置文件）
chmod 700 script.sh  # 仅所有者可执行（私有脚本）
chmod 755 script.sh  # 所有着可执行，其他人可读可执行（公共程序）

# 计算方式：数字 = 权限之和
# 644 = 6(4+2, rw) 4(4, r) 4(4, r)
# 755 = 7(4+2+1, rwx) 5(4+1, r-x) 5(4+1, r-x)
```

#### 字母方式
```bash
# 基本语法
chmod u+x script.sh     # 给所有者添加执行权限
chmod g-w file.txt      # 移除所属组的写权限
chmod o=r-- file.txt    # 设置其他人为只读

# 组合操作
chmod u+x,g-x,o=r file.txt  # 同时设置多个权限
chmod a+x script.sh         # a = all，给所有人添加执行权限
```

#### 递归修改
```bash
# 递归修改目录及其所有内容
chmod -R 755 /var/www/html
chmod -R go-rwx /home/secret  # 移除组和其他人的所有权限
```

### 方法二：chown - 修改所有者和所属组

#### 修改所有者
```bash
# 将 file.txt 的所有者改为 bob
sudo chown bob file.txt

# 递归修改目录
sudo chown -R bob /home/bob/data
```

#### 修改所属组
```bash
# 将 file.txt 的所属组改为 developers
sudo chown :developers file.txt

# 同时修改所有者和所属组
sudo chown bob:developers file.txt
```

#### 递归修改
```bash
# 递归修改目录及其所有内容
sudo chown -R bob:developers /project
```

### 方法三：用户组管理（推荐用于多用户协作）

#### 创建用户组
```bash
# 创建新组
sudo groupadd developers

# 查看组信息
getent group developers
```

#### 将用户添加到组
```bash
# 将用户添加到组
sudo usermod -aG developers alice
sudo usermod -aG developers bob

# 注意：-a 表示 append（追加），不加会覆盖其他组
# 修改后需要重新登录才能生效
```

#### 查看组成员
```bash
# 查看组的所有成员
getent group developers

# 输出示例：developers:x:1001:alice,bob
```

### 实用场景示例

#### 场景 1：团队协作目录
```bash
# 创建共享目录
sudo mkdir /project/shared

# 创建项目组
sudo groupadd project-team

# 将目录所属组改为项目组
sudo chown :project-team /project/shared

# 设置权限：组内可读写，其他人无权限
sudo chmod 770 /project/shared

# 将团队成员添加到组
sudo usermod -aG project-team alice
sudo usermod -aG project-team bob
```

#### 场景 2：Web 服务器配置
```bash
# /var/www/html 目录标准配置
sudo chown -R www-data:www-data /var/www/html
sudo chmod -R 755 /var/www/html

# 上传目录需要写权限
sudo chmod -R 775 /var/www/html/uploads
```

#### 场景 3：SSH 密钥权限
```bash
# SSH 私钥必须只有所有者可读写
chmod 600 ~/.ssh/id_rsa

# 公钥可以公开
chmod 644 ~/.ssh/id_rsa.pub

# .ssh 目录权限
chmod 700 ~/.ssh
```

## 注意事项 ⚠️

### 常见错误

**777 权限的危害**：
```bash
# ❌ 危险：任何人都能读写执行
chmod 777 file.txt

# ✅ 正确：按需分配权限
chmod 750 file.txt  # 所有者和组可用，其他人无权限
```

**忘记设置执行权限**：
```bash
# 创建脚本后忘记添加执行权限
echo '#!/bin/bash\necho "Hello"' > script.sh

# 运行时会报错：Permission denied
./script.sh

# 解决方法
chmod +x script.sh
```

**chown 误操作**：
```bash
# ❌ 危险：递归修改系统文件所有权
sudo chown -R $USER /usr/bin

# ✅ 正确：只修改需要的目录
sudo chown $USER ~/project
```

### 关键配置点

**umask（默认权限掩码）**：
```bash
# 查看当前 umask
umask
# 通常输出：0002 或 0022

# 新建文件权限 = 666 - umask
# 新建目录权限 = 777 - umask

# 临时修改 umask
umask 077  # 新文件默认 600（仅所有者可读写）

# 永久修改：添加到 ~/.bashrc
echo "umask 077" >> ~/.bashrc
```

**特殊权限位**：
```bash
# SUID（Set User ID）：以文件所有者身份执行
chmod 4755 /usr/bin/sudo

# SGID（Set Group ID）：新建文件继承目录所属组
chmod 2770 /project/shared

# Sticky Bit：只有所有者能删除自己的文件
chmod 1777 /tmp
```

## 常见问题 ❓

**Q: 如何查看文件的详细权限？**

A: 使用 `ls -l` 查看详细权限，`stat` 查看完整信息：
```bash
ls -l file.txt
stat file.txt
```

**Q: 为什么我用 root 创建的文件，普通用户无法删除？**

A: 权限取决于文件本身的权限，而非创建者：
```bash
# root 创建文件
sudo touch /tmp/test.txt

# 设置权限
sudo chmod 644 /tmp/test.txt  # 其他人只能读，不能写/删除

# 让普通用户可删除
sudo chmod 666 /tmp/test.txt
# 或更改所有者
sudo chown $USER /tmp/test.txt
```

**Q: 如何批量修改目录权限但保持文件权限不变？**

A: 使用 `find` 命令：
```bash
# 只修改目录
find /path -type d -exec chmod 755 {} \;

# 只修改文件
find /path -type f -exec chmod 644 {} \;
```

**Q: 777 权限为什么很危险？**

A: 777 意味着任何用户都可以：
- 修改文件内容（植入恶意代码）
- 删除文件（数据丢失）
- 执行文件（安全漏洞）

**Q: 如何查看某个用户在哪些组？**

A: 使用 `groups` 或 `id` 命令：
```bash
# 查看当前用户所在的组
groups

# 查看指定用户所在的组
groups alice
# 或
id alice
```

## 相关文档
[[linux磁盘相关的知识]] | [[linux的LVM管理]]
