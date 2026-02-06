---
tags:
  - linux
  - 软件源
created: 2026-02-06
---

# Linux 换源完全指南

## 一、什么是软件源？

软件源（Repository）是Linux发行版用来存储软件包的服务器。当使用包管理器（如apt、yum、dnf等）安装、更新或升级软件时，系统会从这些源服务器下载相应的软件包及其依赖。

### 软件源的类型

| 类型 | 说明 | 特点 |
|------|------|------|
| **官方源** | 发行版官方维护的源 | 最稳定、最安全，但可能速度较慢 |
| **第三方源** | 社区或组织维护的源 | 可能有更多软件，但需要信任源的安全性 |
| **镜像源** | 官方源的同步镜像 | 内容相同，速度更快，国内常用 |


## 二、为什么要换源？

### 主要原因

1. **下载速度慢**
   - 官方源服务器通常在国外，国内访问速度慢
   - 大文件下载可能频繁中断

2. **访问不稳定**
   - 官方源可能被临时屏蔽或网络波动
   - 部分地区无法直接访问

3. **软件更新延迟**
   - 国内镜像通常同步及时，有时反而比官方源更新快


## 三、常见Linux发行版换源

### 3.1 Debian/Ubuntu 及其衍生版

#### 检查系统版本
```bash
# 查看Ubuntu版本
cat /etc/lsb-release

# 或查看Debian版本
cat /etc/debian_version
```

#### 备份原配置
```bash
sudo cp /etc/apt/sources.list /etc/apt/sources.list.bak
```

#### Ubuntu 常用镜像源
| 原地址                 | 用途    |
| ------------------- | ----- |
| archive.ubuntu.com  | 普通软件包 |
| security.ubuntu.com | 安全更新  |

**清华大学镜像** (推荐)
```bash
sudo sed -i 's|http://archive.ubuntu.com|https://mirrors.tuna.tsinghua.edu.cn|g' /etc/apt/sources.list
sudo sed -i 's|http://security.ubuntu.com|https://mirrors.tuna.tsinghua.edu.cn|g' /etc/apt/sources.list
```

**阿里云镜像**
```bash
sudo sed -i 's|http://archive.ubuntu.com|https://mirrors.aliyun.com|g' /etc/apt/sources.list
sudo sed -i 's|http://security.ubuntu.com|https://mirrors.aliyun.com|g' /etc/apt/sources.list
```

**中科大镜像**
```bash
sudo sed -i 's|http://archive.ubuntu.com|https://mirrors.ustc.edu.cn|g' /etc/apt/sources.list
sudo sed -i 's|http://security.ubuntu.com|https://mirrors.ustc.edu.cn|g' /etc/apt/sources.list
```

#### 更新软件列表
```bash
sudo apt update
```

**这条命令整体在干嘛？**

一句话概括：

> **用 sed 把 sources.list 里所有  
> `http://archive.ubuntu.com`  
> 替换成  
> `https://mirrors.tuna.tsinghua.edu.cn`**

而且是：

- **直接改文件**
- **所有匹配的地方**
- **无需你手动编辑**
#### 代码解读

**从左到右逐块拆解**

**① `sudo**`

`sudo`

- `/etc/apt/sources.list` 属于系统配置
- 普通用户 **没有写权限**
- `sudo` = 以 root 身份执行

👉 不加会直接 `Permission denied`

**② `sed**`

`sed`

全名：**Stream EDitor（流编辑器）**

特点：

- 不打开编辑器
- 不进交互界面
- **按规则批量修改文本**

👉 特别适合：

- 配置文件
- 批量替换
- 自动化脚本

**③ `-i**`

`-i`

含义：**in-place（原地修改）**

对比一下👇

|命令|结果|
|---|---|
|`sed 's/a/b/' file`|只输出到屏幕|
|`sed -i 's/a/b/' file`|**直接改文件本身**|

⚠️ 这是个“危险但高效”的参数  
👉 所以换源前一般会先备份：

```bash
sudo cp /etc/apt/sources.list /etc/apt/sources.list.bak
```

**④ `'s|A|B|g'` —— 核心中的核心**

`'s|http://archive.ubuntu.com|https://mirrors.tuna.tsinghua.edu.cn|g'`

这是 **sed 的替换语法**：

```text
s | 被替换的内容 | 新内容 | 标志
```


**🔹 `s**`

`s`

- **substitute（替换）**
- sed 最常用的命令，没有之一

**🔹 `g**`

`g`

含义：**global（全局）**

|有没有 g|效果|
|---|---|
|没有|每一行只替换第一个|
|有|**一行内所有匹配都替换**|

👉 源文件中一行一般只有一个 URL  
但加 `g` 是**良好习惯**

**⑤ `/etc/apt/sources.list**`

`/etc/apt/sources.list`

- Ubuntu / Debian 的 **主软件源配置文件**
- apt 每次更新都会读它


## 四、执行后真实发生了什么？

假设原来文件里有：

### 3.2 CentOS / RHEL / Fedora

#### CentOS 7
```bash
# 备份
sudo cp /etc/yum.repos.d/CentOS-Base.repo /etc/yum.repos.d/CentOS-Base.repo.bak

# 替换为阿里云镜像
sudo wget -O /etc/yum.repos.d/CentOS-Base.repo https://mirrors.aliyun.com/repo/Centos-7.repo

# 清除缓存并重新生成
sudo yum clean all
sudo yum makecache
```

#### CentOS 8 (已停止维护，推荐迁移到Rocky Linux或AlmaLinux)
```bash
# 使用阿里云的Vault源
sudo sed -i 's/mirrorlist/#mirrorlist/g' /etc/yum.repos.d/CentOS-*.repo
sudo sed -i 's|#baseurl=http://mirror.centos.org|baseurl=http://vault.centos.org|g' /etc/yum.repos.d/CentOS-*.repo
```

#### Fedora
```bash
# 使用清华镜像
sudo sed -i 's|https://download.fedoraproject.org/pub|https://mirrors.tuna.tsinghua.edu.cn|g' /etc/yum.repos.d/fedora*.repo

# 清除缓存
sudo dnf clean all
sudo dnf makecache
```

---

### 3.3 Arch Linux

#### 编辑 pacman 配置
```bash
sudo nano /etc/pacman.conf
```

#### 在文件顶部添加镜像（推荐顺序）
```
[core]
Server = https://mirrors.tuna.tsinghua.edu.cn/archlinux/$repo/os/$arch

[extra]
Server = https://mirrors.tuna.tsinghua.edu.cn/archlinux/$repo/os/$arch

[community]
Server = https://mirrors.tuna.tsinghua.edu.cn/archlinux/$repo/os/$arch
```

#### 更新系统
```bash
sudo pacman -Syy
```

---

### 3.4 openSUSE

#### 使用 zypper 添加镜像
```bash
# 添加清华镜像
sudo zypper ar -fc https://mirrors.tuna.tsinghua.edu.cn/opensuse/tumbleweed/repo/oss/ TUNA-Tumbleweed-OSS
sudo zypper ar -fc https://mirrors.tuna.tsinghua.edu.cn/opensuse/tumbleweed/repo/non-oss/ TUNA-Tumbleweed-NON-OSS

# 刷新
sudo zypper refresh
```

---

## 四、重要知识点

### 4.1 源配置文件位置

| 发行版 | 配置文件 | 说明 |
|--------|----------|------|
| Debian/Ubuntu | `/etc/apt/sources.list` | 主配置文件 |
| Debian/Ubuntu | `/etc/apt/sources.list.d/` | 额外源目录 |
| CentOS/RHEL | `/etc/yum.repos.d/` | 所有.repo文件 |
| Arch Linux | `/etc/pacman.conf` | 统一配置文件 |
| openSUSE | `/etc/zypp/repos.d/` | 仓库配置目录 |

### 4.2 源配置格式

#### apt sources.list 格式
```
deb [选项] URL 发行版 分支
```

**示例：**
```
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ jammy main restricted
deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ jammy main restricted
```

**说明：**
- `deb` - 二进制包源
- `deb-src` - 源码包源
- `URL` - 仓库地址
- `发行版` - 如 jammy (Ubuntu 22.04), focal (20.04)
- `分支` - main, restricted, universe, multiverse

### 4.3 Ubuntu 分支说明

| 分支 | 说明 |
|------|------|
| **main** | 官方支持的软件，开源免费 |
| **restricted** | 官方支持但非完全开源（如显卡驱动） |
| **universe** | 社区维护的软件 |
| **multiverse** | 非自由软件，可能有版权限制 |


## 五、常见问题与解决

### 5.1 GPG 密钥错误

**问题：**
```
W: GPG error: https://mirrors.xxx.com ... NO_PUBKEY XXXXXXXXXXXXXXXX
```

**解决方法：**
```bash
# 方法1：自动修复（apt 2.0+）
sudo apt update --allow-releaseinfo-change

# 方法2：添加密钥
sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys XXXXXXXXXXXXXXXX
```

### 5.2 源同步失败

**问题：** 更新后软件包版本不对或找不到

**原因：** 镜像同步延迟

**解决：**
```bash
# 等待一段时间后再试，或者换其他镜像源
# 检查同步状态（清华镜像）
curl https://mirrors.tuna.tsinghua.edu.cn/archlinux/lastupdate
```

### 5.3 恢复官方源

**Ubuntu:**
```bash
sudo cp /etc/apt/sources.list.bak /etc/apt/sources.list
sudo apt update
```

**CentOS:**
```bash
sudo yum reinstall centos-release
sudo yum clean all
sudo yum makecache
```

### 5.4 403 Forbidden 错误

**原因：** 源地址错误或镜像不支持该架构

**解决：** 检查架构和URL是否正确
```bash
uname -m  # 查看系统架构
```

---

## 六、最佳实践

### 6.1 选择镜像源的原则

1. **地理位置** - 优先选择距离近的镜像
2. **同步频率** - 选择同步及时的镜像（清华、阿里云、华为云）
3. **带宽** - 选择有充足带宽的镜像
4. **稳定性** - 选择长期维护的镜像

### 6.2 推荐的国内镜像源

| 镜像 | URL | 特点 |
|------|-----|------|
| 清华大学 | https://mirrors.tuna.tsinghua.edu.cn | 全覆盖，速度快 |
| 阿里云 | https://mirrors.aliyun.com | 稳定，覆盖广 |
| 中科大 | https://mirrors.ustc.edu.cn | 教育网友好 |
| 华为云 | https://mirrors.huaweicloud.com | 企业级稳定 |
| 网易 | https://mirrors.163.com | 老牌镜像 |

### 6.3 换源前必做

1. ✅ 备份原始配置文件
2. ✅ 确认系统版本
3. ✅ 记录原源地址（方便回滚）
4. ✅ 确保有多个备选镜像

### 6.4 换源后必做

1. ✅ 执行更新命令（apt update / yum makecache）
2. ✅ 检查是否有错误信息
3. ✅ 测试安装一个小软件
4. ✅ 验证源地址正确

---

## 七、快速参考

### Ubuntu 一键换源脚本

```bash
#!/bin/bash
# Ubuntu 换源为清华镜像

if [ "$(id -u)" -ne 0 ]; then
    echo "请使用 sudo 运行此脚本"
    exit 1
fi

# 备份
cp /etc/apt/sources.list /etc/apt/sources.list.bak.$(date +%Y%m%d)

# 替换为清华镜像
sed -i 's|http://archive.ubuntu.com|https://mirrors.tuna.tsinghua.edu.cn|g' /etc/apt/sources.list
sed -i 's|http://security.ubuntu.com|https://mirrors.tuna.tsinghua.edu.cn|g' /etc/apt/sources.list

# 更新
apt update

echo "换源完成！原配置已备份到 /etc/apt/sources.list.bak.$(date +%Y%m%d)"
```

---

## 八、相关命令速查

```bash
# apt 系列
apt update          # 更新软件列表
apt upgrade         # 升级软件包
apt full-upgrade    # 完整升级
apt install pkg     # 安装软件
apt remove pkg      # 删除软件
apt autoremove      # 清理不需要的依赖

# yum/dnf 系列
yum clean all       # 清理缓存
yum makecache       # 生成缓存
yum update          # 更新系统
yum install pkg     # 安装软件
yum remove pkg      # 删除软件

# pacman 系列
pacman -Syy         # 强制更新数据库
pacman -Syu         # 同步并升级
pacman -S pkg       # 安装软件
pacman -R pkg       # 删除软件
```

---

## 参考资源

- [清华大学开源软件镜像站](https://mirrors.tuna.tsinghua.edu.cn/)
- [阿里云镜像站](https://developer.aliyun.com/mirror/)
- [Debian官方文档](https://www.debian.org/doc/)
- [Ubuntu官方文档](https://help.ubuntu.com/)
