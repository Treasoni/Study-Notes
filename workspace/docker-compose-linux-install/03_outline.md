## 学习笔记大纲：《Docker 与 Docker Compose 安装（国内环境）》

> 笔记类型：实战安装教程（practice）
> 预计总篇幅：约 21-27 页（8 章）
> 章节数：8
> 目标读者：有 docker run/pull 基础、Linux 服务器上手安装
> 平台覆盖：Ubuntu/Debian（apt）+ CentOS/RHEL（dnf/yum）双轨
> 写作约束：① 层级不超过 3 级；② 表格不得嵌套在列表项内；③ 重点只讲安装/配置，不展开 Docker 完整教程；④ 镜像加速/代理相关概念引用已有 vault 笔记，不照搬

---

### 第一章：安装前准备——环境检查与方案选型

> 内容概览：先判断自己该走哪条轨道，做一次"系统体检"，避免装到一半才发现内核或架构不匹配。给出统一安装思路（一次装齐全家桶包）。

- **篇幅**：短
- **覆盖要点**：内核版本与 64 位架构检查（`uname -r` / `dpkg --print-architecture`）、发行版识别（`/etc/os-release`）、root/sudo 权限确认、旧版本冲突检查与卸载、安装路径统一（`docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin` 全家桶）、apt 系 / dnf 系双轨选型表
- **素材引用**：§一、§二、§六
- **代码示例**：有（环境检查命令 3-5 条）

### 第二章：安装 Docker Engine——apt（Ubuntu/Debian）

> 内容概览：Ubuntu/Debian 用户的主轨道。以阿里云软件源为主线，给出 deb822（新版）与 docker.list（兼容旧写法）两种配置方式，并对比官方源/清华源。

- **篇幅**：中
- **覆盖要点**：安装前置依赖（ca-certificates/curl/gnupg）、写入阿里云 apt 源（deb822 `docker.sources` 或 `docker.list` + gpg）、`apt update` 后安装全家桶、ECS VPC 内网源（`mirrors.cloud.aliyuncs.com`）、指定版本安装（`apt-cache madison`）、Debian 的 URL/Suites 差异
- **素材引用**：§二、§三、§一
- **代码示例**：有（完整 apt 安装命令序列，约 8-10 条）

### 第三章：安装 Docker Engine——dnf/yum（CentOS/RHEL）

> 内容概览：CentOS/RHEL 用户的主轨道。以阿里云 docker-ce.repo 为主线，覆盖 dnf（RHEL 8/9、Rocky/Alma）与 yum（CentOS 7/Stream 8）两种命令形式，并处理 container-selinux 等依赖。

- **篇幅**：中
- **覆盖要点**：安装 yum-utils / dnf-plugins-core、`yum-config-manager --add-repo` 添加阿里云 repo、`sed` 换源备选、安装全家桶、指定版本安装（`yum list --showduplicates`）、CentOS 9 / Rocky 9 用 `linux/centos/` 路径、RHEL 10/Rocky 10 用 `linux/rhel/` 路径、CentOS 7 EOL 注意事项（vault 源）
- **素材引用**：§二、§三、§六
- **代码示例**：有（完整 dnf/yum 安装命令序列，约 8-10 条）

### 第四章：安装 Docker Compose（v2 plugin 与 standalone）

> 内容概览：Compose 是本次首篇覆盖的内容，重点讲推荐路线 plugin（空格命令），并给出兼容路线 standalone（连字符命令），最后用一张对比表说明选型。

- **篇幅**：中
- **覆盖要点**：Compose v2 plugin 方式（apt/dnf 安装 `docker-compose-plugin`，走软件源绕开 GitHub）、standalone 二进制方式（GitHub 下载、`x86_64`/`aarch64`/`armv7` 架构后缀、国内下载加速方案：ghproxy 前缀/本地下载 + scp）、Engine ≥ 20.10 版本要求、plugin vs standalone 对比表、`docker compose version` 验证
- **素材引用**：§四、§一
- **代码示例**：有（两种安装方式命令 + 版本验证，约 6-8 条）
- **备注**：含 1 张对比表（表格置于顶层，不嵌套列表）

### 第五章：配置国内镜像加速（registry-mirrors）

> 内容概览：安装完成不等于拉镜像快。本章配置 `/etc/docker/daemon.json` 的 registry-mirrors，给出 2026 高可用源与已失效源，并说明加速器的边界（只对 Docker Hub 生效）。

- **篇幅**：中
- **覆盖要点**：daemon.json 写法与 JSON 语法注意、2026 高确认可用源（毫秒 `docker.1ms.run`、轩辕 `docker.xuanyuan.me`、DaoCloud `docker.m.daocloud.io`、1Panel `docker.1panel.live`、阿里云专属）、已失效/不推荐源清单、`systemctl daemon-reload && restart docker` 生效、`docker info | grep -A 5 "Registry Mirrors"` 验证、多仓库代理（ghcr/k8s/quay 前缀）用法、加速器 ≠ 代理（引用已有笔记）
- **素材引用**：§五、§一
- **代码示例**：有（daemon.json 写入、重启、验证、`time docker pull` 测速，约 5-6 条）
- **关联已有笔记**：加速器 vs 代理概念引用 [[docker/镜像加速器vs代理-概念对比]]；Docker Desktop 端配置引用 [[docker/DockerDesktop镜像加速器配置]]（本笔记只讲 Linux daemon.json）

### 第六章：安装验证与基础检查

> 内容概览：装完后的"体检清单"。跑通 hello-world、配置非 root 用户权限、设置开机自启，确保环境真正可用。

- **篇幅**：短
- **覆盖要点**：`docker run hello-world` 验证、`sudo usermod -aG docker $USER` + 重新登录（newgrp）使权限生效、`systemctl enable --now docker` 开机自启、`docker version`/`docker compose version` 双确认、服务状态检查（`systemctl status docker`）
- **素材引用**：§二、§六、§一
- **代码示例**：有（验证命令 4-6 条）

### 第七章：常见坑与排查（避坑手册）

> 内容概览：按"现象 → 根因 → 解决"条目式组织 6 个高频坑，遇到问题时可对照排查。这是本章节的信息密度最高处。

- **篇幅**：长
- **覆盖要点**：① `container-selinux >= 2:2.74` 依赖失败（启用 extras 源）；② `bridge-nf-call-iptables is disabled` 网络告警（br_netfilter 模块 + sysctl 持久化，`/etc/modules-load.d/` 加载顺序）；③ daemon.json 配了镜像源仍走官方（加速器"优先尝试"回退机制 + JSON 语法）；④ `docker: 'compose' is not a docker command`（插件路径/未装 plugin）；⑤ `permission denied /var/run/docker.sock`（usermod 需重登，禁止 chmod 666）；⑥ cgroup driver 不一致（K8s 场景 `exec-opts` 对齐）；加速器失效排查顺序
- **素材引用**：§六、§五
- **代码示例**：有（每个坑 1-3 条修复命令）
- **备注**：建议采用"坑 → 现象 → 根因 → 解决"卡片式结构；其中 ② 含 1 段持久化配置代码块

### 第八章：速查附录

> 内容概览：把全文命令浓缩成可复制粘贴的速查卡片，并集中列出镜像源清单与官方/参考文档链接，方便日后单独查阅。

- **篇幅**：短
- **覆盖要点**：apt 系一键命令速查、dnf/yum 系一键命令速查、换源 sed 命令、2026 可用镜像加速器清单表、已失效源清单表、官方文档链接（Docker Engine install / Compose install）+ 阿里云/清华镜像站帮助页
- **素材引用**：§二、§三、§五、§七
- **代码示例**：有（速查命令块）
- **备注**：含 2 张表格（可用源、失效源），均置于顶层，不嵌套列表

---

## 学习路径说明

### 前置要求
- 一台 Linux 服务器：Ubuntu 20.04+ / Debian 11+，或 CentOS 7.9 / Stream 9 / Rocky 8+ / RHEL 8+（任选一条轨道）
- root 权限或 sudo 权限
- 服务器可正常联网（国内网络环境），可用 curl/wget
- 基础 Linux 命令行操作能力（cd、ls、cat、vim/nano、sudo）
- 已了解 `docker run` / `docker pull` 基础命令（安装/Compose 不熟没关系）

### 学完能做什么
- 在 Ubuntu/Debian 上用阿里云源装好 Docker Engine + Buildx + Compose plugin 全家桶
- 在 CentOS/RHEL 上用 yum/dnf 装好同款环境
- 配置好 registry-mirrors 国内镜像加速，`docker pull` 不再超时
- 能独立排查安装常见坑（权限、systemd、container-selinux、compose 命令找不到、镜像源不生效）
- 会用 `docker compose version` / `docker compose up` 跑通基础编排（为后续 Compose 深入打底）

### 建议学习顺序
- 第一章（准备）→ 按你的发行版选 **第二章（apt）** 或 **第三章（dnf/yum）**，二选一即可 → 第四章（Compose）→ 第五章（镜像加速）→ 第六章（验证）→ 第七章（遇到问题时再查）→ 第八章（备用速查）
- 预计总耗时：顺走一遍约 30-60 分钟；只走单发行版轨道可再缩短
- 与已有 vault 笔记的分工：本笔记只讲 **Linux 原生安装与配置**；Windows 桌面版安装见 [[docker/Windows-DockerDesktop安装指南-国内网络版]]；加速器 vs 代理概念对比见 [[docker/镜像加速器vs代理-概念对比]]；Docker Desktop 镜像加速配置见 [[docker/DockerDesktop镜像加速器配置]]

### 覆盖边界说明（防止越界）
- 本笔记不展开 Docker 使用教程（容器/镜像/网络原理），相关概念在涉及处只做一句话带过
- 不覆盖 K8s 安装，只在第七章坑 ⑥ 顺带说明 cgroup driver 对齐，供后续学习衔接
