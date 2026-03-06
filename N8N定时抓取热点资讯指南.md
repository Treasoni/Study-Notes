---
tags: [n8n, 自动化, 工作流, 智谱AI, RSS, 定时任务]
created: 2026-03-06
updated: 2026-03-06
version: 1.2
---

# N8N定时抓取热点资讯指南

> [!info] 概述
> **一句话定义**：N8N 是一款开源的工作流自动化工具，通过可视化节点连接实现定时抓取热点资讯并调用智谱AI进行分析处理。
>
> **通俗比喻**：想象一个"数字搬运工"，每天定时去各大网站收集新闻，然后请"AI分析师"（智谱）帮你总结重点，最后整理成报告发给你。

## 核心概念

### 是什么
N8N（发音 "n-eight-en"）是一款基于节点的开源工作流自动化工具，支持：
- **400+ 官方集成节点**：覆盖主流 SaaS 应用、数据库及消息队列
- **多种触发方式**：定时触发、Webhook 触发、手动触发
- **自托管部署**：数据安全，完全可控
- **可视化编辑**：无需编程，拖拽式构建工作流

### 为什么需要
- **信息过载问题**：每天需要查看多个平台的热点资讯，耗时费力
- **重复性工作**：手动收集、整理、分析新闻内容
- **AI赋能需求**：希望用AI自动总结、分类、提取关键信息

### 通俗理解

**🎯 比喻**：N8N 就像一个"智能管家生产线"
```
[Cron闹钟] → [RSS收集员] → [AI分析师(智谱)] → [整理归档]
   每天早上        收集新闻         总结重点        存入表格
```

**📦 示例**：每日热点资讯自动流水线
```mermaid
graph LR
    A[定时触发<br>每天8点] --> B[RSS Read<br>抓取微博热搜]
    A --> C[RSS Read<br>抓取知乎热榜]
    A --> D[RSS Read<br>抓取36氪]
    B --> E[合并数据]
    C --> E
    D --> E
    E --> F[HTTP Request<br>调用智谱AI分析]
    F --> G[存入飞书表格]
    F --> H[发送通知]
```

## 技术细节

### 1. N8N 部署方式

> [!info] 来源
> - [n8n实战营：高频节点解析](https://m.blog.csdn.net/kenter1983/article/details/155388629) - CSDN
> - [AI自动化神器N8N保姆级安装教程](https://post.m.smzdm.com/zz/p/a65v778z/) - 什么值得买
> - [N8N 官方网站](https://n8n.io/) - 最新版本下载

**推荐方式：Docker 部署**
```bash
docker run -d \
  --name n8n \
  -p 5678:5678 \
  -v ~/.n8n:/home/node/.n8n \
  n8nio/n8n:latest
```

> [!warning] 安全提醒
> - **最新稳定版**：n8n@2.9.4（2026年2月25日）
> - **安全更新**：CVE-2026-21858（远程代码执行）需升级到 >= 1.121.0
> - **历史漏洞**：CVE-2026-25049（表达式沙箱逃逸）已在 1.123.17+、2.5.2+ 修复
> - 定期检查 [n8n GitHub Releases](https://github.com/n8n-io/n8n/releases) 获取安全更新

**其他部署方式**：
- npm 安装：`npm install n8n -g`（推荐使用 `n` 工具管理版本）
- Docker Compose（适合生产环境）
- 官方云托管（付费）

**中文界面配置**（社区方案）：
```bash
# 克隆中文汉化包
git clone https://github.com/other-blowsnow/n8n-i18n-chinese

# 挂载汉化文件到容器
docker run -d \
  --name n8n \
  -p 5678:5678 \
  -v ~/.n8n:/home/node/.n8n \
  -v ./n8n-i18n-chinese/dist:/home/node/.n8n/public/locale/zh:ro \
  n8nio/n8n:latest

# 设置环境变量启用中文
# N8N_LANG=zh
```

### 2. Cron 定时触发器

> [!info] 来源
> - [n8n Cron Node超详细教程](https://m.blog.csdn.net/m0_74822402/article/details/155609244) - CSDN
> - [n8n触发节点完全指南](https://m.blog.csdn.net/bennny/article/details/156871532) - CSDN

**Cron 节点配置**：

| 参数 | 说明 | 示例 |
|------|------|------|
| 触发模式 | Cron 表达式 | `0 8 * * *` (每天8点) |
| 时区 | 选择本地时区 | Asia/Shanghai |
| 执行时间 | 支持多种预设 | 每小时/每天/每周 |

**常用 Cron 表达式**：
```cron
# 每天 8:00 执行
0 8 * * *

# 每 2 小时执行一次
0 */2 * * *

# 每周一 9:00 执行
0 9 * * 1

# 工作日 9:00 执行
0 9 * * 1-5
```

### 3. 抓取热点资讯

> [!info] 来源
> - [n8n定时获取RSS数据详细教程](https://m.blog.csdn.net/2408_89348881/article/details/151754291) - CSDN
> - [手把手教学：用n8n+RSS+飞书实现多平台热点自动抓取](https://cloud.tencent.com/developer/article/2574814) - 腾讯云开发者

**方案一：RSS Read 节点（推荐）**

常用 RSS 源：
```javascript
// 微博热搜
https://weibo.com/ajax/side/hotSearch

// 知乎热榜（需第三方RSS服务）
https://rsshub.app/zhihu/hotlist

// 36氪快讯
https://36kr.com/feed

// 百度热点
https://top.baidu.com/api/rss

// 今日头条热榜（需第三方RSS服务）
https://rsshub.app/toutiao/hot-news
```

**RSS Read 节点配置**：
```json
{
  "url": "https://rsshub.app/zhihu/hotlist",
  "itemLimit": 20
}
```

**方案二：HTTP Request 节点**

适用于无 RSS 的网站：
```json
{
  "method": "GET",
  "url": "https://api.example.com/news",
  "headers": {
    "User-Agent": "Mozilla/5.0..."
  }
}
```

### 4. 集成智谱AI API

> [!info] 来源
> - [智谱AI HTTP API调用官方文档](https://docs.bigmodel.cn/cn/guide/develop/http/introduction)
> - [智谱AI 使用概述](https://docs.bigmodel.cn/cn/api/introduction)
> - [n8n大模型集成完全指南](https://m.blog.csdn.net/bennny/article/details/156952682) - CSDN

**智谱AI API 信息**：
```yaml
端点: https://open.bigmodel.cn/api/paas/v4/chat/completions
认证方式: Bearer Token
请求头:
  Content-Type: application/json
  Authorization: Bearer YOUR_API_KEY
```

**可用模型**（2026年3月）：

| 模型 | 发布时间 | 特点 | 适用场景 |
|------|----------|------|----------|
| **GLM-5** | 2026年2月 | 744B参数，40B激活，MoE架构，开源SOTA | 编程、Agent、复杂推理 |
| **GLM-4.7** | 2025年12月 | 开源SOTA，编程能力强 | 通用对话、代码生成 |
| **GLM-4.6V** | 2025年 | 视觉推理模型 | 图像理解 |
| **GLM-Flash** | 持续更新 | 低成本快速响应 | 简单问答 |

> [!tip] 免费额度
> - **新用户注册**：2000万 Tokens 免费额度（永久有效）
> - 适用于 GLM-4.7、4.6、4.5 等主流模型
> - 注册地址：[智谱AI开放平台](https://open.bigmodel.cn/)

> [!info] 📚 来源
> - [GLM-5 官方文档](https://docs.bigmodel.cn/cn/guide/models/text/glm-5) - 完整调用示例
> - [智谱AI开放平台](https://bigmodel.cn/) - 模型详情

**N8N HTTP Request 节点配置**：

```json
{
  "method": "POST",
  "url": "https://open.bigmodel.cn/api/paas/v4/chat/completions",
  "authentication": "genericCredentialType",
  "genericAuthType": "httpBearerAuth",
  "headerParameters": {
    "parameters": [
      {
        "name": "Content-Type",
        "value": "application/json"
      }
    ]
  },
  "bodyParameters": {
    "parameters": [
      {
        "name": "model",
        "value": "glm-5"
      },
      {
        "name": "messages",
        "value": "={{JSON.stringify([{\"role\": \"system\", \"content\": \"你是新闻分析助手，请总结以下热点资讯的关键信息\"}, {\"role\": \"user\", \"content\": $json.title + \"\\n\" + $json.content}])}}"
      },
      {
        "name": "thinking",
        "value": "={{JSON.stringify({\"type\": \"enabled\"})}}"
      },
      {
        "name": "temperature",
        "value": "0.7"
      },
      {
        "name": "max_tokens",
        "value": "65536"
      }
    ]
  }
}
```

> [!info] 模型选择建议
> - **GLM-5**：推荐用于复杂分析、深度推理场景（如新闻事件影响分析）
>   - 支持 `thinking` 参数启用深度思考模式
>   - `max_tokens` 可设置最高 65536
> - **GLM-4.7**：适合通用对话和摘要任务
> - **GLM-Flash**：适合快速响应、低成本场景

**在 N8N 中配置凭证**：
1. 进入 `Credentials` → `New` → `Header Auth`
2. Name: `智谱AI API`
3. Name: `Authorization`
4. Value: `Bearer YOUR_API_KEY`

### 5. 完整工作流示例

```mermaid
graph TB
    A[Cron<br>每天8点] --> B1[RSS Read<br>微博热搜]
    A --> B2[RSS Read<br>知乎热榜]
    A --> B3[RSS Read<br>36氪快讯]

    B1 --> C[Merge<br>合并数据]
    B2 --> C
    B3 --> C

    C --> D{Filter<br>过滤重复}

    D --> E[Loop Over Items<br>逐条处理]

    E --> F[HTTP Request<br>智谱AI分析]

    F --> G{IF<br>分析成功?}

    G -->|是| H[Set<br>格式化结果]
    G -->|否| I[Error Trigger]

    H --> J[Google Sheets<br>写入表格]
    H --> K[Webhook<br>发送通知]
```

**节点配置详情**：

**1. Cron 节点**
```json
{
  "triggerTimes": {
    "item": [
      {
        "mode": "everyX",
        "value": 12,
        "unit": "hours"
      }
    ]
  }
}
```

**2. RSS Read 节点（多个源）**
```json
// 知乎热榜
{
  "url": "https://rsshub.app/zhihu/hotlist"
}

// 微博热搜
{
  "url": "https://rsshub.app/weibo/search/hot"
}
```

**3. Merge 节点**
```json
{
  "mode": "combine",
  "combineBy": "combineAll"
}
```

**4. Code 节点（数据处理）**
```javascript
// 提取关键信息
const items = $input.all();
const processed = items.map(item => ({
  json: {
    title: item.json.title || item.json.question,
    link: item.json.link || item.json.url,
    pubDate: item.json.pubDate || item.json.created,
    source: item.json.source || '未知来源',
    summary: item.json.description || ''
  }
}));
return processed;
```

**5. HTTP Request 节点（智谱AI）**
```javascript
// 动态构建请求体
{
  "method": "POST",
  "url": "https://open.bigmodel.cn/api/paas/v4/chat/completions",
  "body": {
    "model": "glm-5",
    "messages": [
      {
        "role": "system",
        "content": "你是新闻分析专家，请对以下热点资讯进行分析：\n1. 提取核心事件\n2. 分析影响和意义\n3. 给出简短评论\n\n请用JSON格式返回：{\"核心事件\":\"\",\"意义\":\"\",\"评论\":\"\"}"
      },
      {
        "role": "user",
        "content": "标题：{{ $json.title }}\n内容：{{ $json.summary }}"
      }
    ],
    "thinking": {
      "type": "enabled"
    },
    "temperature": 0.7,
    "max_tokens": 65536
  }
}
```

### 6. 数据存储与通知

> [!info] 来源
> - [n8n实战：批量获取多平台热点资讯](https://m.blog.csdn.net/igtea/article/details/155129117) - CSDN

**存储到飞书多维表格**：
```json
{
  "operation": "append",
  "tableId": "你的表格ID",
  "app_token": "你的应用Token",
  "records": [
    {
      "fields": {
        "标题": "{{ $json.title }}",
        "来源": "{{ $json.source }}",
        "AI分析": "{{ $json.analysis }}",
        "链接": "{{ $json.link }}",
        "抓取时间": "{{ $now.toISO() }}"
      }
    }
  ]
}
```

**发送 Webhook 通知**：
```json
{
  "method": "POST",
  "url": "你的webhook地址",
  "body": {
    "msg_type": "interactive",
    "card": {
      "header": {
        "title": {
          "content": "📰 每日热点资讯汇总",
          "tag": "plain_text"
        }
      },
      "elements": [
        {
          "tag": "div",
          "text": {
            "content": "{{ $json.summary }}",
            "tag": "lark_md"
          }
        }
      ]
    }
  }
}
```

## 与其他概念的关系

| 概念 | 关系 |
|------|------|
| [[RSS使用指南]] | RSS 是 N8N 抓取热点资讯的主要数据来源 |
| [[MCP协议]] | N8N 的节点集成类似于 MCP 的工具概念，都是服务间的连接 |
| [[Agent智能体]] | N8N 工作流可以视为一种"固定逻辑的智能体" |
| [[Prompt提示词]] | 在智谱AI节点中需要良好的 Prompt 设计 |

## 最佳实践

### 1. API 凭证管理
```bash
# 在环境变量中存储 API Key
export ZHIPU_API_KEY="your-api-key"

# 在 N8N 中使用凭证管理器
Credentials → New → Header Auth
```

### 2. 错误处理
- 添加 `Error Trigger` 节点捕获异常
- 设置重试机制（HTTP Request 节点支持）
- 使用 `IF` 节点进行条件判断

### 3. 性能优化
- 使用 `Split In Batches` 节点批量处理
- 设置合理的 `itemLimit` 限制数据量
- 启用工作流执行历史记录清理
- 使用 `Switch` 节点实现多路分发，减少不必要的 API 调用

### 4. 成本优化
- 对于简单任务使用 GLM-Flash 模型（更低成本）
- 设置合理的 `max_tokens` 限制（推荐 2048-65536）
- 启用响应缓存，避免重复分析相同内容
- 利用智谱AI 新用户 2000万 Tokens 免费额度
- GLM-5 的 `thinking` 模式适合复杂任务，简单任务可关闭

### 5. 安全建议
- **及时更新**：确保 n8n 版本 >= 2.9.4（最新稳定版）
- **安全漏洞修复**：>= 1.121.0 修复 CVE-2026-21858 远程代码执行漏洞
- **限制表达式执行**：在可信环境中使用 Code 节点
- **API Key 轮换**：定期更换 API 凭证
- **访问控制**：配置 n8n 的用户认证和权限管理

### 6. 数据去重
```javascript
// 在 Code 节点中实现去重
const seen = new Set();
return items.filter(item => {
  const key = item.json.link;
  if (seen.has(key)) return false;
  seen.add(key);
  return true;
});
```

## 常见问题

**Q: 智谱AI 调用返回 401 错误？**
A: 检查 API Key 是否正确，确认 `Authorization` 头格式为 `Bearer YOUR_API_KEY`

**Q: RSS 源无法访问？**
A: 部分网站需要使用第三方 RSS 服务（如 RSSHub），或使用 HTTP Request 模拟浏览器请求

**Q: 工作流执行超时？**
A: 增加执行超时时间设置，或使用 `Split In Batches` 分批处理大量数据

**Q: 如何调试工作流？**
A: 使用 `Manual Trigger` 手动执行，查看每个节点的输出结果

**Q: n8n 安全漏洞如何处理？**
A: 升级到 n8n >= 2.9.4 最新版本，>= 1.121.0 已修复 CVE-2026-21858 远程代码执行漏洞，避免在不可信输入中使用表达式

**Q: GLM-5 模型调用失败？**
A: 确认 API Key 已开通 GLM-5 权限，部分新模型需要单独申请

**Q: 中文界面配置后不生效？**
A: 检查汉化文件路径是否正确挂载，确保环境变量 `N8N_LANG=zh` 已设置

## 相关文档
- [[AI学习/00-索引/MOC|AI学习索引]]

## 参考资料

### 官方资源
- [N8N 官方文档](https://docs.n8n.io/) - 完整技术文档
- [N8N GitHub Releases](https://github.com/n8n-io/n8n/releases) - 版本发布记录
- [N8N 官网](https://n8n.io/) - 产品主页和模板库
- [智谱AI 开放平台](https://docs.bigmodel.cn/cn/api/introduction) - API 文档
- [GLM-5 官方文档](https://docs.bigmodel.cn/cn/guide/models/text/glm-5) - GLM-5 完整调用示例
- [智谱AI HTTP调用指南](https://docs.bigmodel.cn/cn/guide/develop/http/introduction) - 完整调用说明
- [智谱AI 特价专区](https://open.bigmodel.cn/special_area) - 优惠活动

### 社区资源
- [n8n Cron Node 超详细教程](https://m.blog.csdn.net/m0_74822402/article/details/155609244) - CSDN
- [n8n 大模型集成完全指南](https://m.blog.csdn.net/bennny/article/details/156952682) - CSDN
- [手把手教学：n8n+RSS+飞书热点抓取](https://cloud.tencent.com/developer/article/2574814) - 腾讯云
- [热点捕手：用n8n打造智能资讯流水线](https://juejin.cn/post/7564051354244497427) - 掘金
- [保姆级教程：n8n私人新闻秘书](https://m.blog.csdn.net/m0_65555479/article/details/150448752) - CSDN
- [N8N教程：2026最新自动化工作流配置指南](https://www.cnblogs.com/whatai/p/19590639) - 博客园
- [n8n一站式部署指南（含中文界面）](https://m.blog.csdn.net/weixin_29234423/article/details/157748528) - CSDN
- [智谱GLM-5深度解析](https://m.blog.csdn.net/weixin_43107715/article/details/157981548) - CSDN
- [2026大模型API免费额度汇总](https://cloud.tencent.com/developer/article/2626756) - 腾讯云

### 第三方服务
- [RSSHub](https://docs.rsshub.app/) - 开源 RSS 生成服务
- [RSSHub 实战教程](https://m.blog.csdn.net/rnn9storyteller/article/details/155008473) - CSDN
- [飞书开放平台](https://open.feishu.cn/) - 消息推送和表格存储
- [N8N 中文汉化项目](https://github.com/other-blowsnow/n8n-i18n-chinese) - GitHub

### 安全公告
- [CVE-2026-25049：n8n表达式沙箱逃逸漏洞](https://m.blog.csdn.net/2301_79319459/article/details/157978420) - CSDN
- [n8n 安全更新公告](https://github.com/n8n-io/n8n/security) - GitHub Security
