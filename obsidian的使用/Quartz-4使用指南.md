---
title: Quartz 4 使用指南
tags: [obsidian/发布工具, 静态网站生成器, 数字花园]
created: 2026-04-30
updated: 2026-04-30
lastChecked: 2026-04-30
---

# Quartz 4 使用指南

> [!info] 概述
> **Quartz 4** 是一个快速、功能完备的静态网站生成器，用于将 Markdown 内容转换为可完全运行的网站。
> 就像一个"数字花园的园丁工具"——帮助用户把 Obsidian 笔记播种、培育，最终开花结果展示给全世界。

## 核心概念

### 是什么
Quartz 4 是由 jackyzha0 开发的开源静态网站生成器，专门设计用于将 Obsidian 笔记库发布为在线网站。它支持数字花园、个人笔记网站等场景。

### 为什么需要
- **零成本发布**：将本地笔记免费部署到互联网
- **双向同步**：本地编辑，自动同步到网站
- **原生 Obsidian 支持**：完美支持 wikilinks、callouts 等 Obsidian 特有语法
- **现代化功能**：全文搜索、图谱视图、弹出预览、Latex 公式、代码高亮

### 通俗理解
🎯 **比喻**：Quartz 就像一个"数字花园的温室"。你的 Markdown 笔记是种子，温室（Quartz）负责把这些种子培育成漂亮的植物（网页），然后帮你把整个花园（网站）展示给访客。

📦 **示例**：一行命令发布笔记
```bash
npx quartz sync
```

💬 **社区**：有问题？加入 [Discord 社区](https://discord.gg/cRFFHYye7t)

## 快速开始

### 环境要求
- **Node.js**：至少 v22
- **npm**：v10.9.2 或更高

> [!tip] 检查版本
> ```bash
> node -v
> npm -v
> ```

### 安装步骤

1. **克隆仓库**
   ```bash
   git clone https://github.com/jackyzha0/quartz.git
   cd quartz
   ```

2. **安装依赖**
   ```bash
   npm i
   ```

3. **初始化内容**
   ```bash
   npx quartz create
   ```

> [!info] 📚 来源
> - [Quartz 官方文档 - 快速开始](https://quartz.jzhao.xyz/)

## 内容写作

### 目录结构
所有内容都放在 `/content` 文件夹中：
- 主页内容：`content/index.md`
- 笔记文件：直接放在 content 目录下

### Markdown 支持

#### 标准 Markdown
Quartz 完全支持标准 Markdown 语法。

#### 扩展支持
- **GitHub Flavored Markdown (GFM)**：脚注、删除线、表格、任务列表
- **Obsidian Flavored Markdown (OFM)**：
  - Callouts（提示块）
  - Wikilinks（双向链接）
  - Mermaid 图表

### Frontmatter 字段

在笔记顶部添加 YAML 元数据：

```markdown
---
title: 示例标题
draft: false
tags:
  - 示例标���
aliases:
  - 别名1
  - 别名2
date: 2026-04-30
---

笔记内容...
```

#### 常用字段说明

| 字段 | 说明 | 示例 |
|------|------|------|
| `title` | 页面标题 | `title: 我的笔记` |
| `draft` | 是否为草稿 | `draft: true`（不发布） |
| `tags` | 标签列表 | `tags: [obsidian, 工具]` |
| `aliases` | 别名（搜索友好） | `aliases: [别名]` |
| `date` | 发布日期 | `date: 2026-04-30` |
| `permalink` | 自定义 URL | `permalink: /custom-url` |
| `description` | 页面描述（SEO） | `description: 简短描述` |

> [!info] 📚 来源
> - [Quartz 官方文档 - Authoring Content](https://quartz.jzhao.xyz/authoring-content)

## 本地预览

### 启动预览服务器
```bash
npx quartz build --serve
```

打开浏览器访问 `http://localhost:8080/` 查看效果。

### 命令行选项

| 选项 | 说明 | 默认值 |
|------|------|--------|
| `-d, --directory` | 内容文件夹 | `content` |
| `-v, --verbose` | 打印详细日志 | - |
| `-o, --output` | 输出文件夹 | `public` |
| `--serve` | 启动热重载服务器 | - |
| `--port` | 服务器端口 | `8080` |
| `--concurrency` | 并发线程数 | - |

> [!warning] 注意
> `--serve` 模式仅用于本地预览，不适合生产环境。

> [!info] 📚 来源
> - [Quartz 官方文档 - Building](https://quartz.jzhao.xyz/build)

## 配置指南

### 配置文件
- `quartz.config.ts`：主要配置
- `quartz.layout.ts`：布局配置

### 基础配置

```typescript
const config: QuartzConfig = {
  configuration: {
    pageTitle: "我的数字花园",
    pageTitleSuffix: " | Quartz",
    enableSPA: true,
    enablePopovers: true,
    baseUrl: "example.com",
    // ...
  },
  plugins: {
    transformers: [...],
    filters: [...],
    emitters: [...],
  },
}
```

### 主题配置

#### 字体配置
```typescript
theme: {
  typography: {
    header: "Schibsted Grotesk",
    body: "Source Sans Pro",
    code: "JetBrains Mono",
  },
}
```

#### 颜色配置
```typescript
theme: {
  colors: {
    light: "#ffffff",
    dark: "#1a1a1a",
    lightgray: "#f5f5f5",
    gray: "#888888",
    darkgray: "#333333",
  },
}
```

### 分析工具配置

Quartz 支持多种分析工具：

| 提供商 | 配置示例 |
|--------|----------|
| Google Analytics | `{ provider: 'google', tagId: '<your-tag>' }` |
| Plausible | `{ provider: 'plausible' }` |
| Umami | `{ provider: 'umami', host: '<host>', websiteId: '<id>' }` |
| Vercel Analytics | `{ provider: 'vercel' }` |
| Microsoft Clarity | `{ provider: 'clarity', projectId: '<your-id>' }` |
| Matomo | `{ provider: 'matomo', siteId: '<your-id>', host: '<host>' }` |
| Rybbit | `{ provider: 'rybbit', siteId: '<your-id>' }` |
| Tinylytics | `{ provider: 'tinylytics', siteId: '<your-id>' }` |
| Cabin | `{ provider: 'cabin' }` |

### 插件系统

Quartz 采用插件架构，分为三类：

| 类型 | 作用 | 示例 |
|------|------|------|
| **Transformers** | 内容映射 | FrontMatter, Latex |
| **Filters** | 内容过滤 | ExplicitPublish |
| **Emitters** | 内容输出 | RSS, Sitemap |

> [!info] 📚 来源
> - [Quartz 官方文档 - Configuration](https://quartz.jzhao.xyz/configuration)

## 部署上线

### Cloudflare Pages（推荐）

1. 登录 [Cloudflare Dashboard](https://dash.cloudflare.com/)
2. 选择 **Workers & Pages** > **Create application** > **Pages** > **Connect to Git**
3. 配置构建：

| 配置项 | 值 |
|--------|-----|
| Production branch | `v4` |
| Framework preset | `None` |
| Build command | `npx quartz build` |
| Build output directory | `public` |

### GitHub Pages

创建 `.github/workflows/deploy.yml`：

```yaml
name: Deploy Quartz site to GitHub Pages
on:
  push:
    branches:
      - v4
permissions:
  contents: read
  pages: write
  id-token: write
concurrency:
  group: "pages"
  cancel-in-progress: false
jobs:
  build:
    runs-on: ubuntu-22.04
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - uses: actions/setup-node@v4
        with:
          node-version: 22
      - name: Install Dependencies
        run: npm ci
      - name: Build Quartz
        run: npx quartz build
      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: public
  deploy:
    needs: build
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

然后在 GitHub Settings > Pages 中选择 **GitHub Actions** 作为 Source。

### Vercel

1. 添加 `vercel.json`：
   ```json
   {
     "cleanUrls": true
   }
   ```

2. Vercel 配置：

| 配置项 | 值 |
|--------|-----|
| Framework Preset | `Other` |
| Root Directory | `./` |
| Build Command | `npx quartz build` |

### Netlify

| 配置项 | 值 |
|--------|-----|
| Build command | `npx quartz build` |
| Publish directory | `public` |

### GitLab Pages

创建 `.gitlab-ci.yml`：

```yaml
stages:
  - build
  - deploy
image: node:22
cache:
  key: $CI_COMMIT_REF_SLUG
  paths:
    - .npm/
build:
  stage: build
  rules:
    - if: '$CI_COMMIT_REF_NAME == "v4"'
  before_script:
    - hash -r
    - npm ci --cache .npm --prefer-offline
  script:
    - npx quartz build
  artifacts:
    paths:
      - public
  tags:
    - gitlab-org-docker
pages:
  stage: deploy
  rules:
    - if: '$CI_COMMIT_REF_NAME == "v4"'
  script:
    - echo "Deploying to GitLab Pages..."
  artifacts:
    paths:
      - public
```

### 自托管

#### Nginx

```nginx
server {
    listen 80;
    server_name example.com;
    root /path/to/quartz/public;
    index index.html;
    error_page 404 /404.html;
    location / {
        try_files $uri $uri.html $uri/ =404;
    }
}
```

#### Apache (.htaccess)

```apache
RewriteEngine On
ErrorDocument 404 /404.html
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteCond %{DOCUMENT_ROOT}/%{REQUEST_URI}.html -f
RewriteRule ^(.*)$ $1.html [L]
RewriteCond %{REQUEST_FILENAME} -d
RewriteRule ^(.*)/$ $1/index.html [L]
```

#### Caddy (Caddyfile)

```
example.com {
    root * /path/to/quartz/public
    try_files {path} {path}.html {path}/ =404
    file_server
    encode gzip
    handle_errors {
        rewrite * /{err.status_code}.html
        file_server
    }
}
```

> [!info] 📚 来源
> - [Quartz 官方文档 - Hosting](https://quartz.jzhao.xyz/hosting)

## GitHub 同步

### 初始设置

1. 在 GitHub 创建新仓库（**不要**初始化 README、license 或 .gitignore）

2. 配置远程仓库：
   ```bash
   git remote -v
   git remote set-url origin YOUR_REMOTE_URL
   git remote add upstream https://github.com/jackyzha0/quartz.git
   ```

3. 首次同步：
   ```bash
   npx quartz sync --no-pull
   ```

### 日常同步

```bash
# 推送到 GitHub
npx quartz sync

# 常用选项
# --commit / --no-commit：是否创建 git 提交
# --push / --no-push：是否推送到远程
# --pull / --no-pull：是否拉取更新
# -v：详细输出
```

> [!tip] 解决常见问题
> - `fatal: --[no-]autostash option is only valid with --rebase`：更新 git 版本
> - `fatal: The remote end hung up unexpectedly`：增加 buffer：`git config http.postBuffer 524288000`

> [!info] 📚 来源
> - [Quartz 官方文档 - GitHub Setup](https://quartz.jzhao.xyz/setting-up-your-GitHub-repository)

## 版本更新

### 更新命令
```bash
npx quartz update
```

这会从官方仓库拉取最新更新。

### 冲突处理

如果遇到合并冲突：
1. Quartz 会自动缓存内容：`npx quartz restore` 可恢复
2. 使用 GitHub Desktop 或 VSCode 解决冲突
3. 手动解决后重新推送

> [!info] 📚 来源
> - [Quartz 官方文档 - Upgrading](https://quartz.jzhao.xyz/upgrading)

## Obsidian 集成

### 原生支持功能

Quartz 4 与 Obsidian 无缝集成：

| 功能 | 说明 |
|------|------|
| Wikilinks | `[[双向链接]]` |
| Callouts | `> [!note] 提示块` |
| Mermaid 图表 | 代码块中的图表 |
| Frontmatter | YAML 元数据 |
| 标签系统 | `#标签` |
| 嵌入语法 | `![[嵌入笔记]]` |

### 工作流程推荐

1. **本地编辑**：在 Obsidian 中撰写和整理笔记
2. **实时预览**：`npx quartz build --serve` 本地预览
3. **同步发布**：`npx quartz sync` 推送到 GitHub
4. **自动部署**：GitHub Actions 自动构建和发布

> [!info] 📚 来源
> - [Quartz 官方文档 - Obsidian Compatibility](https://quartz.jzhao.xyz/features/Obsidian-compatibility)

## 常见问题

### Q: 更改不生效？
确保已执行 `npx quartz sync` 将更改推送到 GitHub。

### Q: 如何添加自定义域名？
- **Cloudflare Pages**：参考 Cloudflare 官方文档
- **GitHub Pages**：Settings > Pages > Custom Domain
- **Vercel**：Domains 页面添加域名

### Q: 如何设置私有页面？
将笔记的 `draft: true` 设为 true，或使用 `ignorePatterns` 忽略特定文件。

### Q: RSS 订阅不工作？
确保在配置中正确设置了 `baseUrl`（不包含 `https://` 前缀）。

### Q: 遇到问题无法解决？

- 搜索网站内置搜索功能查找问题
- [升级](./upgrading)到最新版本
- 提交 [GitHub Issue](https://github.com/jackyzha0/quartz/issues)
- 加入 [Discord 社区](https://discord.gg/cRFFHYye7t) 寻求帮助

## 最佳实践

1. **保持简洁**：使用 wikilinks 建立笔记间的关联
2. **定期同步**：养成 `npx quartz sync` 的习惯
3. **使用草稿**：创作中或不想发布的内容使用 `draft: true`
4. **备份配置**：修改配置前备份原文件
5. **监控更新**：定期运行 `npx quartz update` 获取新功能

## 个人笔记

> [!personal] 💡 我的理解与感悟
> Quartz 4 特别适合已经使用 Obsidian 管理笔记的用户。它让"数字花园"的梦想变得触手可及——不需要学习复杂的网页技术，只需要专注于内容创作，Quartz 会帮你处理剩下的事情。

## 相关文档
- [[Obsidian Smart Connections 使用指南]]
- [[Obsidian-Custom-Sort-自定义排序插件]]
- [[Obsidian-Web-Clipper使用教程]]
- [[如何使用obsidian做笔记]]

## 参考资料
### 官方资源
- [Quartz 官方网站](https://quartz.jzhao.xyz/) - 官方首页
- [Quartz GitHub 仓库](https://github.com/jackyzha0/quartz) - 源代码
- [Quartz 官方文档](https://quartz.jzhao.xyz/) - 完整使用文档

### 社区资源
- [Nicole van der Hoeven 的 Quartz 视频教程](https://www.youtube.com/watch?v=6s6DT1yN4dw) - 视频安装指南
- [数字花园理念](https://jzhao.xyz/posts/networked-thought) - Quartz 作者关于网络化思考的文章