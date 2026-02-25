# OpenClaw 安装教程

> 更新时间：2026年2月
> 本文档基于 OpenClaw 官方文档及社区最新资料整理

## 目录

- [一、OpenClaw 简介](#一openclaw-简介)
- [二、推荐安装方法（官方一键脚本）](#二推荐安装方法官方一键脚本)
- [三、npm/pnpm 全局安装](#三npmpnpm-全局安装)
- [四、Docker 部署](#四docker-部署)
- [五、源码编译安装（开发者）](#五源码编译安装开发者)
- [六、阿里云一键部署](#六阿里云一键部署)
- [七、汉化版安装](#七汉化版安装)
- [八、安装后配置](#八安装后配置)
- [九、常见问题与解决方案](#九常见问题与解决方案)
- [十、参考链接](#十参考链接)

---

## 一、OpenClaw 简介

### 什么是 OpenClaw？

OpenClaw 是一个现代化的 AI 网关和服务编排平台，提供了简洁易用的界面来管理和部署 AI 应用。它支持多种 AI 模型集成，提供统一的 API 接口，帮助开发者快速构建 AI 原生应用。

### 核心特性

- **统一网关**：提供统一的 API 入口，支持多种 AI 模型和服务
- **可视化配置**：通过 Web 控制台进行可视化配置和管理
- **插件系统**：支持自定义插件扩展功能
- **多模型支持**：集成 OpenAI、Claude、Gemini 等主流 AI 模型
- **本地部署**：支持本地部署，数据完全自主可控

### 系统要求

- **Node.js**: ≥ 22.0.0（推荐使用最新 LTS 版本）
- **操作系统**：
  - macOS 10.15+
  - Linux（Ubuntu 20.04+, Debian 11+, CentOS 8+）
  - Windows 10/11（WSL2 或原生支持）
- **内存**：建议 ≥ 4GB RAM
- **磁盘空间**：≥ 500MB 可用空间

---

## 二、推荐安装方法（官方一键脚本）

### ⭐ 为什么推荐一键脚本？

官方一键脚本是最简单、最可靠的安装方式，具有以下优势：

- ✅ 自动检测系统环境
- ✅ 自动安装所需依赖
- ✅ 自动配置环境变量
- ✅ 启动配置向导
- ✅ 支持跨平台
- ✅ 提供国内镜像加速

### 2.1 macOS / Linux 安装

#### 方法一：官方脚本（国际网络）

```bash
curl -fsSL https://openclaw.bot/install.sh | bash
```

#### 方法二：国内镜像（推荐国内用户使用）

```bash
curl -fsSL https://gitee.com/openclaw-mirror/install-script/raw/main/install.sh | bash
```

**安装过程说明：**

1. 脚本会自动检测系统类型和架构
2. 检查 Node.js 版本，如不符合要求会提示安装
3. 下载最新版本的 OpenClaw
4. 配置环境变量
5. 启动配置向导

**安装完成后：**

```bash
# 验证安装
openclaw --version

# 查看帮助信息
openclaw --help
```

### 2.2 Windows 安装

#### 方法一：PowerShell 一键安装

```powershell
# 以管理员身份运行 PowerShell
iwr -useb https://openclaw.ai/install.ps1 | iex
```

#### 方法二：使用 Chocolatey

```powershell
choco install openclaw
```

#### 方法三：使用 Scoop

```powershell
scoop bucket add openclaw
scoop install openclaw
```

### 2.3 国内用户注意事项

如果遇到网络问题，可以：

1. **使用国内镜像脚本**（如上所示）
2. **配置 npm 镜像**：

```bash
# 配置 npm 使用淘宝镜像
npm config set registry https://registry.npmmirror.com

# 安装完成后再使用一键脚本
```

3. **手动下载安装包**：

   访问 [Gitee 发布页](https://gitee.com/openclaw/openclaw/releases) 下载最新版本

---

## 三、npm/pnpm 全局安装

如果你已经熟悉 Node.js 开发，可以直接使用 npm 或 pnpm 进行全局安装。

### 3.1 前置准备

#### 检查 Node.js 版本

```bash
node --version
```

确保版本 ≥ 22.0.0。如果版本过低，请先升级 Node.js：

**使用 nvm 安装/升级 Node.js（推荐）：**

```bash
# 安装 nvm（如果没有）
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash

# 重新加载 shell 配置
source ~/.bashrc  # 或 source ~/.zshrc

# 安装最新 LTS 版本的 Node.js
nvm install --lts

# 使用最新版本
nvm use --lts
```

**Windows 用户安装 Node.js：**

访问 [Node.js 官网](https://nodejs.org/) 下载安装包，或使用 nvm-windows。

### 3.2 使用 npm 安装

```bash
# 安装最新版本
npm install -g openclaw@latest

# 或安装特定版本
npm install -g openclaw@1.0.0
```

### 3.3 使用 pnpm 安装（推荐）

pnpm 更快速、节省磁盘空间：

```bash
# 安装 pnpm（如果没有）
npm install -g pnpm

# 安装 OpenClaw
pnpm add -g openclaw@latest
```

### 3.4 解决 sharp 库编译问题

在某些系统上，sharp（图像处理库）可能需要编译，如果遇到问题：

**Linux:**

```bash
# 安装编译依赖
sudo apt-get update
sudo apt-get install -y build-essential python3 libvips-dev

# 然后重新安装
npm install -g openclaw@latest
```

**macOS:**

```bash
# 安装 Xcode 命令行工具
xcode-select --install

# 然后重新安装
npm install -g openclaw@latest
```

**Windows:**

```bash
# 安装 windows-build-tools
npm install -g windows-build-tools

# 然后重新安装
npm install -g openclaw@latest
```

---

## 四、Docker 部署

Docker 部署适合服务器环境和生产环境，提供更好的隔离性和可管理性。

### 4.1 使用 Docker 镜像

#### 拉取并运行

```bash
# 拉取最新镜像
docker pull openclaw/openclaw:latest

# 运行容器
docker run -d \
  --name openclaw \
  -p 18789:18789 \
  -v openclaw-data:/app/data \
  openclaw/openclaw:latest
```

#### 使用 docker-compose（推荐）

创建 `docker-compose.yml` 文件：

```yaml
version: '3.8'

services:
  openclaw:
    image: openclaw/openclaw:latest
    container_name: openclaw
    ports:
      - "18789:18789"
    volumes:
      - openclaw-data:/app/data
      - openclaw-logs:/app/logs
    environment:
      - NODE_ENV=production
      - PORT=18789
    restart: unless-stopped
    networks:
      - openclaw-network

  # 可选：添加数据库
  postgres:
    image: postgres:15-alpine
    container_name: openclaw-db
    environment:
      POSTGRES_DB: openclaw
      POSTGRES_USER: openclaw
      POSTGRES_PASSWORD: your_password_here
    volumes:
      - postgres-data:/var/lib/postgresql/data
    restart: unless-stopped
    networks:
      - openclaw-network

volumes:
  openclaw-data:
  openclaw-logs:
  postgres-data:

networks:
  openclaw-network:
    driver: bridge
```

**启动服务：**

```bash
# 启动所有服务
docker-compose up -d

# 查看日志
docker-compose logs -f openclaw

# 停止服务
docker-compose down
```

### 4.2 容器管理命令

```bash
# 查看运行状态
docker ps

# 查看容器日志
docker logs openclaw

# 进入容器
docker exec -it openclaw sh

# 重启容器
docker restart openclaw

# 停止并删除容器
docker stop openclaw
docker rm openclaw
```

### 4.3 数据持久化

所有重要数据都会挂载到命名卷中：

- `/app/data` - 配置和数据
- `/app/logs` - 日志文件

备份命令：

```bash
# 备份数据卷
docker run --rm \
  -v openclaw-data:/data \
  -v $(pwd):/backup \
  alpine tar czf /backup/openclaw-backup.tar.gz /data
```

---

## 五、源码编译安装（开发者）

开发者可以从源码编译安装，方便自定义和调试。

### 5.1 克隆仓库

```bash
# 使用 GitHub
git clone https://github.com/openclaw/openclaw.git
cd openclaw

# 或使用 Gitee（国内用户）
git clone https://gitee.com/openclaw/openclaw.git
cd openclaw
```

### 5.2 安装依赖

```bash
# 安装 pnpm（如果没有）
npm install -g pnpm

# 安装项目依赖
pnpm install
```

### 5.3 构建项目

```bash
# 开发模式构建
pnpm build

# 生产模式构建
pnpm build:prod
```

### 5.4 运行

```bash
# 开发模式（热重载）
pnpm dev

# 生产模式
pnpm start

# 使用自定义配置
pnpm start -- --config ./config/custom.config.js
```

### 5.5 开发者工具

```bash
# 运行测试
pnpm test

# 代码格式化
pnpm format

# 代码检查
pnpm lint

# 类型检查
pnpm type-check
```

---

## 六、阿里云一键部署

阿里云用户可以使用预置镜像快速部署。

### 6.1 使用阿里云镜像市场

1. 登录阿里云控制台
2. 进入「镜像市场」
3. 搜索 "OpenClaw"
4. 选择合适的镜像规格
5. 一键部署到 ECS 实例

### 6.2 手动在 ECS 上部署

```bash
# 连接到 ECS 实例
ssh root@your-ecs-ip

# 安装 Docker（如果没有）
curl -fsSL https://get.docker.com | bash

# 运行 OpenClaw 容器
docker run -d \
  --name openclaw \
  -p 18789:18789 \
  -v openclaw-data:/app/data \
  --restart=unless-stopped \
  openclaw/openclaw:latest
```

### 6.3 配置安全组

在阿里云控制台配置安全组规则：

- 入方向：TCP 18789 端口开放
- 授权对象：0.0.0.0/0（或指定 IP）

---

## 七、汉化版安装

对于需要中文界面的用户，可以安装社区维护的汉化版。

### 7.1 安装 openclaw-cn

```bash
# 使用 npm 安装汉化版
npm install -g openclaw-cn@latest

# 使用 pnpm 安装（推荐）
pnpm add -g openclaw-cn@latest
```

### 7.2 使用汉化版

```bash
# 启动汉化版网关
openclaw-cn gateway --port 18789

# 访问控制台即可看到中文界面
# http://127.0.0.1:18789/
```

### 7.3 汉化版特性

- 完全中文界面
- 中文文档和提示
- 符合国内用户习惯的配置选项
- 集成国内常用的 AI 服务

---

## 八、安装后配置

### 8.1 运行配置向导

首次安装后，运行配置向导完成基本设置：

```bash
# 运行配置向导并安装守护进程
openclaw onboard --install-daemon
```

配置向导会引导你完成：

1. 设置管理员账户
2. 配置 API 密钥
3. 设置网关端口（默认 18789）
4. 配置数据存储路径
5. 启用/禁用特定功能

### 8.2 启动网关服务

```bash
# 启动网关（默认端口 18789）
openclaw gateway

# 指定端口
openclaw gateway --port 8080

# 后台运行
openclaw gateway --daemon

# 使用自定义配置
openclaw gateway --config /path/to/config.json
```

### 8.3 访问控制台

安装完成并启动服务后，访问 Web 控制台：

```
http://127.0.0.1:18789/
```

首次访问会提示你：
1. 创建管理员账户
2. 配置第一个 AI 模型
3. 创建第一个 API 端点

### 8.4 配置守护进程（开机自启）

#### Linux (systemd)

```bash
# 安装守护进程
openclaw onboard --install-daemon

# 启用服务
sudo systemctl enable openclaw

# 启动服务
sudo systemctl start openclaw

# 查看状态
sudo systemctl status openclaw

# 查看日志
sudo journalctl -u openclaw -f
```

#### macOS (launchd)

```bash
# 安装守护进程
openclaw onboard --install-daemon

# 服务会自动配置并启动
```

#### Windows (Windows Service)

```powershell
# 以管理员身份运行
openclaw onboard --install-daemon

# 管理服务
# 打开「服务」管理工具，找到 OpenClaw Gateway 服务
```

### 8.5 环境变量配置

创建 `.env` 文件或设置环境变量：

```bash
# OpenClaw 配置
OPENCLAW_PORT=18789
OPENCLAW_HOST=0.0.0.0
OPENCLAW_DATA_DIR=/var/lib/openclaw
OPENCLAW_LOG_LEVEL=info

# API 密钥
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key

# 数据库（可选）
DATABASE_URL=postgresql://user:password@localhost:5432/openclaw
```

---

## 九、常见问题与解决方案

### 9.1 网络连接问题

**问题：** 无法下载安装包或拉取 Docker 镜像

**解决方案：**

1. 使用国内镜像源
2. 配置代理
3. 手动下载安装包

```bash
# 使用国内 npm 镜像
npm config set registry https://registry.npmmirror.com

# 使用国内 Docker 镜像
sudo mkdir -p /etc/docker
sudo tee /etc/docker/daemon.json <<-'EOF'
{
  "registry-mirrors": [
    "https://docker.m.daocloud.io",
    "https://dockerproxy.com"
  ]
}
EOF
sudo systemctl daemon-reload
sudo systemctl restart docker
```

### 9.2 权限问题

**问题：** EACCES 权限错误

**解决方案：**

```bash
# 修复 npm 全局目录权限
mkdir ~/.npm-global
npm config set prefix '~/.npm-global'
echo 'export PATH=~/.npm-global/bin:$PATH' >> ~/.bashrc
source ~/.bashrc

# 或使用 sudo（不推荐）
sudo npm install -g openclaw@latest
```

### 9.3 Node.js 版本问题

**问题：** Node.js 版本过低

**解决方案：**

```bash
# 使用 nvm 安装最新版本
nvm install 22
nvm use 22
nvm alias default 22

# 验证版本
node --version
```

### 9.4 WSL2 相关问题

**问题：** WSL2 中网络或权限问题

**解决方案：**

```bash
# 更新 WSL2
wsl --update

# 在 WSL2 中设置正确的权限
sudo chown -R $USER:$USER ~/.npm-global

# 配置 Windows 防火墙允许 WSL2 网络访问
```

### 9.5 端口被占用

**问题：** 端口 18789 已被使用

**解决方案：**

```bash
# 查找占用端口的进程
lsof -i :18789

# 或使用其他端口
openclaw gateway --port 8080
```

### 9.6 sharp 库编译失败

**问题：** 安装时 sharp 库编译错误

**解决方案：**

```bash
# Linux - 安装依赖
sudo apt-get install -y build-essential python3 libvips-dev

# macOS - 安装 Xcode 命令行工具
xcode-select --install

# 或使用预编译的 sharp
npm install --sharp-binary-host=https://npmmirror.com/mirrors/sharp/
npm install -g openclaw@latest
```

### 9.7 Docker 容器无法启动

**问题：** Docker 容器启动失败

**解决方案：**

```bash
# 查看详细日志
docker logs openclaw

# 检查端口是否被占用
docker ps -a

# 尝试使用不同的端口映射
docker run -d --name openclaw -p 8080:18789 openclaw/openclaw:latest
```

### 9.8 如何卸载

```bash
# 卸载全局安装的 OpenClaw
npm uninstall -g openclaw

# 或
pnpm remove -g openclaw

# 删除配置和数据
rm -rf ~/.openclaw
rm -rf /usr/local/lib/node_modules/openclaw

# 停止并删除守护进程
sudo systemctl stop openclaw
sudo systemctl disable openclaw
sudo rm /etc/systemd/system/openclaw.service
```

---

## 十、参考链接

### 官方资源

- **官方网站**: https://openclaw.ai
- **官方文档**: https://docs.openclaw.ai
- **中文社区**: https://www.moltcn.com
- **GitHub 仓库**: https://github.com/openclaw/openclaw
- **Gitee 仓库**: https://gitee.com/openclaw/openclaw

### 社区资源

- **官方论坛**: https://forum.openclaw.ai
- **Discord 社区**: https://discord.gg/openclaw
- **Twitter**: https://twitter.com/openclaw_ai

### 相关教程

- **掘金 - OpenClaw 入门教程**: [掘金搜索 OpenClaw](https://juejin.cn/search?query=OpenClaw)
- **CSDN - OpenClaw 部署指南**: [CSDN 搜索 OpenClaw](https://www.csdn.net/search?q=OpenClaw)
- **阿里云 - 云原生部署**: 阿里云镜像市场搜索 "OpenClaw"

### 常用命令速查

```bash
# 查看版本
openclaw --version

# 查看帮助
openclaw --help

# 启动网关
openclaw gateway

# 配置向导
openclaw onboard

# 查看日志
openclaw logs

# 重启服务
openclaw restart
```

---

## 获取帮助

如果遇到问题：

1. 查看[常见问题](#九常见问题与解决方案)章节
2. 搜索[官方文档](https://docs.openclaw.ai)
3. 在[中文社区](https://www.moltcn.com)提问
4. 加入 [Discord 社区](https://discord.gg/openclaw)寻求帮助
5. 提交 [GitHub Issue](https://github.com/openclaw/openclaw/issues)

---

**最后更新**: 2026年2月
**文档版本**: v1.0.0
**维护者**: OpenClaw 中文社区
