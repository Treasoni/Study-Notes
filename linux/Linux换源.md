---
tags: [linux]
---

# Linux 软件源配置

> [!info] 概述
> **软件源就像应用商店的镜像站点**。将软件源从默认的国外服务器替换为国内镜像，可以大幅提升软件下载和更新速度。

## 核心概念 💡

### 软件源（Repository）
- **是什么**：存储软件包的服务器，包管理器（apt、yum、dnf）从这里下载软件
- **为什么需要**：集中管理软件分发，统一更新和依赖管理
- **与其他概念关系**：配置文件定义了源地址，包管理器读取配置进行操作

### DEB822 格式（Ubuntu 24.04+）
- **是什么**：新的软件源配置格式，使用 `.sources` 文件
- **为什么需要**：更易读、更安全、支持更多特性
- **与传统格式区别**：
  - 传统：`/etc/apt/sources.list`（单文件格式）
  - 新格式：`/etc/apt/sources.list.d/*.sources`（DEB822 格式）

### 镜像源
- **是什么**：官方源的同步副本，内容相同但地理位置更近
- **为什么需要**：提高下载速度，减少网络延迟
- **主流国内镜像**：清华、阿里云、中科大、华为云

## 操作步骤

### Ubuntu 22.04/24.04 换源（传统格式）

#### 1. 备份原配置
```bash
sudo cp /etc/apt/sources.list /etc/apt/sources.list.bak
```

#### 2. 查看系统版本
```bash
lsb_release -a
# 或
cat /etc/os-release
```

**Ubuntu 版本代号**：
| 版本 | 代号 | 状态 |
|------|------|------|
| Ubuntu 24.04 LTS | noble | 最新 LTS |
| Ubuntu 22.04 LTS | jammy | 当前主流 |
| Ubuntu 20.04 LTS | focal | 即将停止支持 |

#### 3. 编辑配置文件
```bash
sudo nano /etc/apt/sources.list
```

#### 4. 替换为镜像源

**清华大学镜像（推荐）**：
```bash
# Ubuntu 24.04 (noble)
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ noble main restricted universe multiverse
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ noble-updates main restricted universe multiverse
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ noble-backports main restricted universe multiverse
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ noble-security main restricted universe multiverse

# Ubuntu 22.04 (jammy)
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ jammy main restricted universe multiverse
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ jammy-updates main restricted universe multiverse
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ jammy-backports main restricted universe multiverse
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ jammy-security main restricted universe multiverse
```

**阿里云镜像**：
```bash
# Ubuntu 24.04
deb https://mirrors.aliyun.com/ubuntu/ noble main restricted universe multiverse
deb https://mirrors.aliyun.com/ubuntu/ noble-updates main restricted universe multiverse
deb https://mirrors.aliyun.com/ubuntu/ noble-backports main restricted universe multiverse
deb https://mirrors.aliyun.com/ubuntu/ noble-security main restricted universe multiverse

# Ubuntu 22.04
deb https://mirrors.aliyun.com/ubuntu/ jammy main restricted universe multiverse
deb https://mirrors.aliyun.com/ubuntu/ jammy-updates main restricted universe multiverse
deb https://mirrors.aliyun.com/ubuntu/ jammy-backports main restricted universe multiverse
deb https://mirrors.aliyun.com/ubuntu/ jammy-security main restricted universe multiverse
```

#### 5. 更新软件列表
```bash
sudo apt update
```

### Ubuntu 一键换源脚本

```bash
# 备份
sudo cp /etc/apt/sources.list /etc/apt/sources.list.bak

# 替换为清华镜像
sudo sed -i 's|http://archive.ubuntu.com|https://mirrors.tuna.tsinghua.edu.cn|g' /etc/apt/sources.list
sudo sed -i 's|http://security.ubuntu.com|https://mirrors.tuna.tsinghua.edu.cn|g' /etc/apt/sources.list

# 更新
sudo apt update
```

### Ubuntu 24.04 DEB822 格式换源

#### 1. 创建新的源配置文件
```bash
sudo nano /etc/apt/sources.list.d/ubuntu.sources
```

#### 2. 添加以下内容
```text
Types: deb
URIs: https://mirrors.tuna.tsinghua.edu.cn/ubuntu
Suites: noble noble-updates noble-backports
Components: main restricted universe multiverse
Signed-By: /usr/share/keyrings/ubuntu-archive-keyring.gpg

Types: deb
URIs: https://mirrors.tuna.tsinghua.edu.cn/ubuntu
Suites: noble-security
Components: main restricted universe multiverse
Signed-By: /usr/share/keyrings/ubuntu-archive-keyring.gpg
```

#### 3. 更新软件列表
```bash
sudo apt update
```

### 其他发行版换源

#### Debian
```bash
# 备份
sudo cp /etc/apt/sources.list /etc/apt/sources.list.bak

# 替换为清华镜像
sudo sed -i 's|http://deb.debian.org|https://mirrors.tuna.tsinghua.edu.cn|g' /etc/apt/sources.list

# 更新
sudo apt update
```

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

#### Arch Linux
```bash
# 编辑 pacman 配置
sudo nano /etc/pacman.conf

# 在文件顶部添加镜像（清华镜像）
[core]
Server = https://mirrors.tuna.tsinghua.edu.cn/archlinux/$repo/os/$arch

[extra]
Server = https://mirrors.tuna.tsinghua.edu.cn/archlinux/$repo/os/$arch

[community]
Server = https://mirrors.tuna.tsinghua.edu.cn/archlinux/$repo/os/$arch

# 更新系统
sudo pacman -Syy
```

## 注意事项 ⚠️

### 常见错误

**GPG 密钥错误**：
```bash
W: GPG error: https://mirrors.xxx.com ... NO_PUBKEY XXXXXXXXXXXXXXXX

# 解决方法 1：自动修复（apt 2.0+）
sudo apt update --allow-releaseinfo-change

# 解决方法 2：添加密钥
sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys XXXXXXXXXXXXXXXX
```

**403 Forbidden 错误**：
- 原因：源地址错误或镜像不支持该架构
- 解决：检查架构和 URL 是否正确
```bash
uname -m  # 查看系统架构
```

**版本代号不匹配**：
```bash
# 查看正确的版本代号
lsb_release -cs

# 确保源配置中的代号与此输出一致
```

### 关键配置点

**Ubuntu 分支说明**：
| 分支 | 说明 |
|------|------|
| **main** | 官方支持的软件，开源免费 |
| **restricted** | 官方支持但非完全开源（如显卡驱动） |
| **universe** | 社区维护的软件 |
| **multiverse** | 非自由软件，可能有版权限制 |

**选择镜像源的原则**：
1. **地理位置** - 优先选择距离近的镜像
2. **同步频率** - 选择同步及时的镜像
3. **带宽** - 选择有充足带宽的镜像
4. **稳定性** - 选择长期维护的镜像

**推荐国内镜像源**：
| 镜像 | URL | 特点 |
|------|-----|------|
| 清华大学 | https://mirrors.tuna.tsinghua.edu.cn | 全覆盖，速度快 |
| 阿里云 | https://mirrors.aliyun.com | 稳定，覆盖广 |
| 中科大 | https://mirrors.ustc.edu.cn | 教育网友好 |
| 华为云 | https://mirrors.huaweicloud.com | 企业级稳定 |

## 常见问题 ❓

**Q: 换源后软件版本不对怎么办？**

A: 可能是镜像同步延迟，解决方法：
```bash
# 等待一段时间后再试，或换其他镜像源
# 检查同步状态（清华镜像）
curl https://mirrors.tuna.tsinghua.edu.cn/archlinux/lastupdate
```

**Q: 如何恢复官方源？**

A: 使用备份文件恢复：
```bash
sudo cp /etc/apt/sources.list.bak /etc/apt/sources.list
sudo apt update
```

**Q: sed 命令是什么意思？**

A: `sed` 是流编辑器，用于批量文本替换：
```bash
sudo sed -i 's|旧地址|新地址|g' 文件
# -i: 直接修改文件
# s: 替换命令
# g: 全局替换（一行内所有匹配）
```

**Q: DEB822 格式有什么优势？**

A: 主要优势：
- 更易读：键值对格式
- 更安全：内置签名验证
- 更灵活：支持多源配置
- 标准化：RFC 822 兼容

**Q: 如何测试哪个镜像源最快？**

A: 使用 `netselect-apt` 工具：
```bash
# 安装工具
sudo apt install netselect-apt

# 测试 fastest mirror
sudo netselect-apt noble
```

## 相关文档
[[linux如何修改网络信息]] | [[linux的文件权限]]
