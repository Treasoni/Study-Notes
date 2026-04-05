---
title: OpenCLI 使用指南
created: 2026-04-05
tags: [CLI工具, 浏览器自动化, AI工具]
---

# OpenCLI 使用指南

> [!info] 概述
> **一句话定义**: OpenCLI 是一个能将任何网站、Electron 应用或本地 CLI 工具转化为统一命令行界面的开源工具。
>
> **通俗比喻**: 想象一下，如果你的浏览器、桌面应用和各种命令行工具都能像乐高积木一样，通过统一的命令接口拼接组合，让 AI 代理能直接操控它们，这就是 OpenCLI 做的事情。

## 核心概念

### 是什么

OpenCLI 是一个创新的命令行工具，旨在消除浏览器、应用和 CLI 工具之间的界限。它通过浏览器扩展和守护进程架构，实现了以下核心特性：

- **Zero Risk** - 零风险设计，不涉及敏感操作
- **Reuse Chrome/Chromium Login** - 复用现有浏览器登录状态，无需重复认证
- **AI-powered Discovery** - AI 驱动的命令发现机制
- **Universal CLI Hub** - 通用 CLI 命令中心，统一管理所有工具

### 为什么需要

传统使用浏览器和应用的痛点：

- 需要在不同应用间切换，打断工作流
- 无法通过脚本自动化浏览器操作
- AI 代理难以直接控制图形界面
- 各平台 API 参差不齐，学习成本高

**OpenCLI 的解决方案**：

- 将所有操作统一到命令行界面
- 支持 **79+ 内置适配器**，覆盖主流平台
- 专为 AI Agents 设计，让 AI 能直接控制浏览器
- 提供标准化输出格式（JSON、CSV、YAML、Markdown、Table）

### 通俗理解

🎯 **比喻**: OpenCLI 就像是给浏览器和各种应用装上了"命令行遥控器"。

**具体场景**：

- 想查看 Bilibili 热门视频 → 不用打开浏览器，直接 `opencli bilibili hot`
- 想搜索小红书内容 → 命令行直接 `opencli xiaohongshu search "AI"`
- 想批量操作 GitHub PR → `opencli gh pr list --limit 10`
- AI 助手想帮你操作网页 → 直接调用 OpenCLI 命令即可

📦 **示例**：

```bash
# 查看热搜
opencli bilibili hot --limit 5

# 下载视频
opencli bilibili download BV1xx411c7mD --output ./videos

# 搜索内容
opencli xiaohongshu search "人工智能" --limit 10

# 查看推特趋势
opencli twitter trending
```

## 安装与配置

> [!warning] 前置要求
> - Node.js 环境
> - Chrome 或 Chromium 浏览器
> - npm 或 npx 包管理器

### 三步安装流程

#### 步骤 1: 安装 Browser Bridge Extension

1. 下载扩展包
   - 访问 [GitHub Releases](https://github.com/jackwener/opencli/releases)
   - 下载 `opencli-extension.zip`

2. 安装到 Chrome
   ```bash
   # 在浏览器地址栏输入
   chrome://extensions/
   ```
   - 启用右上角"开发者模式"
   - 点击"加载已解压的扩展程序"
   - 选择解压后的扩展目录

#### 步骤 2: 安装 OpenCLI

```bash
# 全局安装
npm install -g @jackwener/opencli

# 安装 AI skills（可选，用于 AI 集成）
npx skills add jackwener/opencli
```

> [!tip] 提示
> 安装过程中如遇权限问题，可能需要使用 `sudo`（Linux/macOS）或以管理员身份运行（Windows）。

#### 步骤 3: 验证安装

```bash
# 检查扩展和守护进程连接状态
opencli doctor

# 查看守护进程状态
opencli daemon status

# 查看所有可用命令
opencli list
```

### 更新 OpenCLI

```bash
npm install -g @jackwener/opencli@latest
```

**相关链接**：
- [OpenCLI GitHub 仓库](https://github.com/jackwener/opencli)
- [OpenCLI NPM 包](https://www.npmjs.com/package/@jackwener/opencli)
- [Browser Bridge 扩展下载](https://github.com/jackwener/opencli/releases)

## 基础命令使用

### 命令分类

OpenCLI 命令分为两类：

1. **公共 API 命令** - 无需浏览器，直接调用 API
   ```bash
   opencli hackernews top --limit 5
   ```

2. **浏览器命令** - 需要 Browser Bridge 扩展
   ```bash
   opencli bilibili hot --limit 5
   ```

### 常用命令

| 命令 | 功能 | 示例 |
|:-----|:-----|:-----|
| `opencli list` | 查看所有可用命令 | `opencli list` |
| `opencli doctor` | 检查系统状态 | `opencli doctor` |
| `opencli daemon status` | 查看守护进程 | `opencli daemon status` |
| `opencli <adapter> <action>` | 执行适配器命令 | `opencli bilibili hot` |

### 输出格式

支持 5 种标准化输出格式：

```bash
# JSON 格式（适合脚本处理）
opencli bilibili hot -f json

# CSV 格式（适合导入表格）
opencli bilibili hot -f csv

# YAML 格式（适合配置文件）
opencli bilibili hot -f yaml

# Markdown 格式（适合文档）
opencli bilibili hot -f md

# 表格格式（默认，适合终端查看）
opencli bilibili hot -f table
```

## 内置适配器生态

OpenCLI 内置 **79+ 适配器**，覆盖多个领域：

### 中国平台

| 平台 | 命令前缀 | 功能示例 |
|:-----|:---------|:---------|
| 小红书 | `xiaohongshu` | 搜索、浏览笔记 |
| Bilibili | `bilibili` | 热门、下载视频 |
| 百度贴吧 | `tieba` | 帖子浏览 |
| 虎扑 | `hupu` | 热门话题 |
| 知乎 | `zhihu` | 问题、回答 |
| 闲鱼 | `xianyu` | 商品搜索 |

### 国际平台

| 平台 | 命令前缀 | 功能示例 |
|:-----|:---------|:---------|
| Twitter | `twitter` | 趋势、推文 |
| Reddit | `reddit` | 热门帖子 |
| Amazon | `amazon` | 商品搜索 |
| Spotify | `spotify` | 音乐操作 |

### AI 工具

| 工具 | 命令前缀 | 用途 |
|:-----|:---------|:-----|
| Gemini | `gemini` | Google AI 交互 |
| 元宝 | `yuanbao` | 字节 AI 工具 |
| NotebookLM | `notebooklm` | Google 笔记 AI |

### CLI Hub（命令行工具集成）

| 工具 | 命令前缀 | 说明 |
|:-----|:---------|:-----|
| GitHub CLI | `gh` | GitHub 操作 |
| Obsidian | `obsidian` | 笔记管理 |
| Docker | `docker` | 容器管理 |
| 飞书 | `lark-cli` | 协作办公 |
| 钉钉 | `dingtalk` | 团队沟通 |
| 企业微信 | `wecom` | 企业通讯 |
| Vercel | `vercel` | 部署管理 |

### 桌面应用

支持将 Electron 应用转化为 CLI：

- Cursor、Codex、Antigravity
- ChatGPT、Notion、Discord

## 浏览器自动化命令

OpenCLI 提供 **13 个底层命令**，用于精细控制浏览器：

> [!info] 说明
> 以下命令需要 Browser Bridge 扩展支持。

### 页面操作

```bash
# 打开网页
opencli init https://example.com

# 后退
opencli back

# 滚动页面
opencli scroll down
opencli scroll up
```

### 交互操作

```bash
# 点击元素
opencli click selector

# 输入文本
opencli type selector "文本内容"

# 选择下拉项
opencli select selector "选项"

# 发送按键
opencli keys "Enter"
```

### 状态获取

```bash
# 获取页面状态
opencli state

# 获取元素内容
opencli get selector

# 截图
opencli screenshot output.png
```

### 高级功能

```bash
# 等待条件
opencli wait selector

# 执行 JavaScript
opencli eval "document.title"

# 监控网络请求
opencli network
```

### 管理命令

```bash
# 初始化会话
opencli init

# 验证连接
opencli verify

# 关闭浏览器
opencli close
```

## 退出码说明

OpenCLI 使用标准化退出码，便于脚本判断执行结果：

| 退出码 | 含义 | 说明 |
|:-----:|:-----|:-----|
| 0 | 成功 | 命令正常执行 |
| 1 | 通用错误 | 未分类的错误 |
| 2 | 使用错误 | 命令参数错误 |
| 66 | 空结果 | 查询无结果 |
| 69 | 服务不可用 | Browser Bridge 未连接 |
| 75 | 临时失败 | 超时等临时问题 |
| 77 | 需要认证 | 未登录目标站点 |

**脚本示例**：

```bash
# 根据退出码处理结果
opencli bilibili hot --limit 5
if [ $? -eq 66 ]; then
    echo "查询无结果"
elif [ $? -eq 77 ]; then
    echo "请先登录 Bilibili"
fi
```

## 最佳实践

### 1. 选择合适的输出格式

- **脚本处理**: 使用 `-f json` 便于解析
- **人类阅读**: 使用默认表格格式或 `-f md`
- **数据导入**: 使用 `-f csv` 导入 Excel

### 2. 处理认证问题

遇到退出码 77 时：

```bash
# 在浏览器中登录目标站点
# OpenCLI 会复用浏览器登录状态
opencli xiaohongshu search "AI"
```

> [!tip] 技巧
> OpenCLI 会自动复用 Chrome 中已登录的账号，无需重复登录。

### 3. 调试技巧

```bash
# 检查系统状态
opencli doctor

# 查看守护进程日志
opencli daemon logs

# 重启守护进程
opencli daemon restart
```

### 4. AI Agent 集成

OpenCLI 专为 AI Agents 设计，可以：

- 让 AI 直接调用浏览器命令
- 实现网页自动化操作
- 统一管理各种工具的调用接口

## 常见问题

### Q: 为什么有些命令需要浏览器？

A: 部分适配器（如 Bilibili、小红书）需要模拟浏览器操作来获取数据，这些命令依赖 Browser Bridge 扩展。

### Q: 如何查看所有可用命令？

A: 使用 `opencli list` 查看完整命令列表。

### Q: 退出码 69 怎么解决？

A: 退出码 69 表示 Browser Bridge 未连接，解决步骤：

1. 检查 Chrome 扩展是否启用
2. 运行 `opencli doctor` 诊断
3. 重启守护进程：`opencli daemon restart`

### Q: 支持自定义适配器吗？

A: 是的，OpenCLI 支持创建自定义适配器，具体可参考[官方文档](https://github.com/jackwener/opencli)。

## 与其他工具的关系

| 工具 | 关系 |
|:-----|:-----|
| [[Puppeteer]] | OpenCLI 底层使用类似技术，但提供更高层抽象 |
| [[Selenium]] | OpenCLI 更轻量，专注于 CLI 集成而非完整测试框架 |
| [[Playwright]] | OpenCLI 复用现有浏览器，无需独立启动 |

## 参考资料

- [OpenCLI GitHub 仓库](https://github.com/jackwener/opencli)
- [OpenCLI NPM 包](https://www.npmjs.com/package/@jackwener/opencli)
- [Browser Bridge 扩展下载](https://github.com/jackwener/opencli/releases)

## 个人笔记

> [!personal] 💡 我的理解与感悟
> （此处记录个人学习心得，更新时会被保留）
