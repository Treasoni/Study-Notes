# 深度研究素材 - 如何把影视网站导入到本地部署的 lunatv

> 项目：lunatv-import-sites · 阶段 2（深度收集）· 2026-08-25
> 范围：在阶段 1 候选基础上精读 7 个核心来源，补齐源格式、接入标准、实操流程与排错

---

## 1. Scope

回答核心问题「如何把找到的影视网站导入到本地部署的 LunaTV」，覆盖：
1. LunaTV 的源机制（空壳聚合、api_site JSON、订阅源）
2. 影视网站要满足什么条件才能接入（苹果CMS V10 接口）
3. 从「找到影视站」到「能播放」的完整实操路径
4. 常见坑与排错
5. 进阶：被墙源中转（CORSAPI）、源健康检测、自建源

---

## 2. 来源表

| ID | 来源 | URL | tier | 用途 |
|----|------|-----|------|------|
| A2 | LunaTV CONFIGURATION.md | https://raw.githubusercontent.com/hafrey1/LunaTV/main/docs/deployment/CONFIGURATION.md | official | 源格式、环境变量、管理后台功能 |
| B1 | shiyu1314/LunaTV（Enhanced Edition） | https://github.com/shiyu1314/LunaTV | official | 主项目定位、功能清单、部署 |
| B2 | 空壳影视官方文档·苹果CMS 对接 | https://docs.mac-cms.com/cms/cms-connect | official | 苹果CMS V10 接口标准（部分） |
| B3 | DeepWiki·MoonTVPlus 源配置 | https://deepwiki.com/mtvpls/MoonTVPlus/9.4-video-source-configuration | tutorial | SourceConfig 模型、Base58 订阅机制、多源聚合 |
| C1 | 飞牛Docker系列·LunaTV避坑版 | https://bbs.nasdiyer.com/forum.php?mod=viewthread&action=printable&tid=21625 | tutorial | 部署避坑、换源、端口冲突 |
| C2 | 懒猫微服·LunaTV 配置技巧 | https://lazycat.cloud/playground/guideline/1244 | tutorial | **唯一完整实操步骤**（订阅URL→保存） |
| A4 | hafrey1/LunaTV-config | https://github.com/hafrey1/LunaTV-config | community | 真实源清单、健康检测数据、CORSAPI 代理 |

---

## 3. Claim / Source 映射

### 3.1 源格式：`api_site` JSON（A2 + B3 交叉印证）

- 配置文件是内嵌 JSON；`api_site` 是「源标识 → 配置对象」映射（A2）
- 每个源对象字段（A2）：
  - `key`：唯一标识，仅小写字母/数字（A2）；B3 补充保留名：`openlist`、`xiaoya`、`emby*` 前缀
  - `api`：**必填**，资源站 vod JSON API 地址，支持苹果 CMS V10 格式（A2）
  - `name`：**必填**，界面显示名（A2）
  - `detail`：可选，网页详情根 URL（A2）
- 顶层字段（A2）：`cache_time`（接口缓存秒数，建议 3600-7200）、`custom_category`（数组：name/type/query，豆瓣搜索词）
- B3 SourceConfig 扩展字段：`from`（'config'=订阅导入 / 'custom'=手动添加）、`disabled`（排除出搜索）、`proxyMode`（服务端代理 M3U8+TS 分片）、`weight`（0-100 搜索权重）

```json
{
  "cache_time": 7200,
  "api_site": {
    "example_source": {
      "api": "http://example.com/api.php/provide/vod",
      "name": "示例资源站",
      "detail": "http://example.com"
    }
  }
}
```

### 3.2 配置加载与管理后台（A2）

- 部署后为空壳，配置在**管理后台 > 配置文件**运行时填写；无需改代码/重启（A2）
- 管理后台入口：`http://your-domain:3000/admin`，站长账号登录（A2）
- 支持「配置订阅」：订阅 URL、自动拉取远程配置、**Base58 编码 JSON**（A2）
- 视频源支持导入/导出、有效性检测、一键选无效源、拖拽排序（A2）
- 管理面板模块：站点/用户/视频源/直播源/分类/网盘搜索/AI 推荐/YouTube/TVBox 安全/缓存（A2）

### 3.3 苹果CMS V10 接口标准（B2）

- 标准接口基础地址：`https://域名/api.php/provide/vod/`（带尾斜杠）
- 接口类型：MacCMS V10 / 苹果V10
- `from` 参数以**路径段**追加：`/api.php/provide/vod/from/m3u8/`，只返回该播放源数据
- 返回 JSON 含：`vod_play_from`（播放源名，逗号分隔）、`type_name`（分类名）
- App 侧 `playerName` 映射播放源别名：`"m3u8": "默认", "iframe": "备用"`
- **验证方法**：浏览器直接打开接口地址，返回 JSON 即接口正常（B2）

### 3.4 远程订阅机制（B3 + C2）

- 拉取：`POST /api/admin/config_subscription/fetch`，入参远程 URL（B3）
- 解码链路：响应文本 `bs58.decode` → `TextDecoder` 转 UTF-8 → 存数据库 `ConfigFile` 字段（B3）
- 更新时校验 JSON 语法，`refineConfig` 把外部源**合并进活跃配置**（B3）
- UI 操作：配置文件 → 订阅URL 粘贴 + 开「自动更新」→ 点「拉取配置」→ **点「保存」**（C2）

### 3.5 完整实操流程（C2 唯一可复现）

1. 登录（默认 admin/admin123，懒猫打包版；Compose 部署则由 USERNAME/PASSWORD 决定）
2. 首页空白 → 右上角人像 → **管理面板 → 配置文件**
3. 订阅URL 处粘贴订阅链接，打开「自动更新」，点「拉取配置」
4. **点「保存」**（忘点保存配置不生效——最常见坑，C2 两次强调）
5. 拉取成功后显示配置代码即成功
6. 站点配置：分别设「豆瓣图片代理」「豆瓣数据代理」→ 再次保存
7. 回首页刷新即可追剧

### 3.6 真实源与健康数据（A4）

- 三档配置：jin18=31（无成人）、jingjian=61（含成人）、full=88（含成人）
- 订阅 URL：raw.githubusercontent 直链 + Base58 中转（`https://pz.v88.qzz.io?format=2&source=jin18`），**推荐自部署代理**
- 健康报告（2026-08-25 01:36 CST）：总源 72，可用 65，不可用 7，**平均可用率 ~92%**
  - 100% 可用 39 个；80-99% 档 29 个；50-79% 档 1 个（虎牙 76.7%）；<50% 档 3 个（0%）
  - 完全失效：飘零资源、百万资源、丝袜资源（30 次检测全失败）
  - 连通但搜索无结果：豆瓣资源、茅台资源、杏吧、色猫；不匹配：大地资源
- 结论：**源失效是常态**，需定期更新配置

### 3.7 CORSAPI 代理被墙源（A4）

- 原理：Cloudflare Workers 部署 `_worker.js`，做「API 代理 + JSON api 字段前缀重写」
- 自动去除旧 `?url=` 前缀并替换为新代理前缀，可自定义 `prefix` 接入私有 API/多 Worker
- 参数：`?url=`（代理任意 API）、`?source=`（jin18/jingjian/full）、`?format=`（0 raw / 1 proxy / 2 base58 / 3 proxy-base58）、`?prefix=`
- 限制：Worker 缓存 7200s、默认超时 9s、免费额度 10 万次请求/天

### 3.8 环境变量（A2 + C1）

- 必填：`USERNAME`、`PASSWORD`、`NEXT_PUBLIC_STORAGE_TYPE`（kvrocks/redis/upstash）
- 存储连接：`KVROCKS_URL`、`REDIS_URL`、`UPSTASH_URL`、`UPSTASH_TOKEN`；Vercel 推荐 Upstash
- 可选：`SITE_BASE`、`NEXT_PUBLIC_SITE_NAME`（默认 MoonTV）、`ANNOUNCEMENT`、`NEXT_PUBLIC_SEARCH_MAX_PAGE`（默认 5，1-50）、`NEXT_PUBLIC_DOUBAN_PROXY_TYPE`（默认 direct）、`NEXT_PUBLIC_DOUBAN_IMAGE_PROXY_TYPE`、`NEXT_PUBLIC_DISABLE_YELLOW_FILTER`、`NEXT_PUBLIC_FLUID_SEARCH`、`DISABLE_HERO_TRAILER`、`DISABLE_SSRF_PROTECTION`
- C1 补充：豆瓣代理示例值 `cmliussss-cdn-tencent`（腾讯 CDN）

### 3.9 主项目能力（B1）

- LunaTV Enhanced Edition fork 自 SzeMeng76/LunaTV，基于 MoonTV 深度二开，v4.3.1→v6.6.2，60+ 功能
- 内容生态：网盘搜索、ACG 种子搜索（Mikan）、IPTV 直播（m3u/m3u8、FLV、EPG）、Emby 私有库、YouTube、Bilibili、Bangumi、短剧
- 技术栈：Next.js 16 + React 19 + TS + Tailwind；ArtPlayer + HLS.js；存储 Upstash/Kvrocks/SQLite
- 许可：CC BY-NC-SA 4.0，仅供学习交流，不存储视频

---

## 4. 矛盾与冲突（写作时需并列呈现）

1. **豆瓣代理**：C1 推荐配置（腾讯 CDN）以获得更好展示 vs C2 评论区反馈「试了全部选项仍提示获取豆瓣分类数据失败」→ 该坑可能未根治
2. **配置加载方式**：A2 明确「运行时管理后台配置，无需改代码/重启」 vs 早期搜索结果与部分 fork 提及的 `DOCKER_ENV`/`config.json` 静态加载 → **A2/B1 均未出现 DOCKER_ENV 与 CUSTOM_SOURCE_\***，暂以 A2 运行时配置为准
3. **源数量口径**：A4 README 自述 jingjian=61，但正文又说「去除污染源后剩 57 个可用源」
4. **`from` 参数位置**：B2 用路径段（`/from/m3u8/`）；部分资料视为 query 参数 → 两者可能都支持
5. **默认账号**：C2 懒猫版 admin/admin123 vs C1 Compose 部署要求自设强密码 → 取决于部署方式

## 5. 开放问题（Gaps）

| 缺口 | 影响 | 建议补源 |
|------|------|---------|
| 苹果CMS 完整 API 规格（ac=/h=/t=/pg=、响应包装 code/msg/page、list 内 vod_*、`$`/`$$$` 分隔符、token 签名） | 影响「如何验证/调试一个源」章节深度 | B2 页面链接的 `/cms/cms-api.html` |
| `CUSTOM_SOURCE_*` / `DOCKER_ENV` 加源机制 | 部分资料声称存在，A2/B1 未覆盖 | fork 的 `.env.example`、README 部署段 |
| PanSou 网盘源确切 JSON 字段 | 网盘源配置章节 | B1 的 docs/ 目录文档 |
| 豆瓣代理问题的确定性方案 | 首页空白排错 | 更多社区实测 |
| TVBox 集成与 api_site 的关系 | 可选章节 | B1 的 docs/integration/TVBOX.md |

## 6. 实操指引（给章节写作的提炼）

- **判断影视站能否接入**：浏览器打开 `站点/api.php/provide/vod/`，返回 JSON = 可接入（苹果CMS V10）
- **最简导入方式**：找一个现成订阅源（如 A4 的 jin18/jingjian/full）→ 管理面板 → 配置文件 → 订阅URL → 拉取配置 → **保存**
- **手动加单个站**：管理面板 → 配置文件 → 在 api_site JSON 中加一个源对象（api/name 必填）→ 保存
- **源失效处理**：播放页「换源」；「无测速数据」红字 = 该源不可用；定期更新订阅/用健康检测报告挑源
- **被墙源**：用 CORSAPI（Cloudflare Worker）中转，给 api 字段加代理前缀
- **部署排错**：登录失败查密码/Redis-Kvrocks；端口冲突改宿主侧映射；数据丢失查 volumes；镜像拉取失败配加速器

## 7. 下游交接（Handoff）

供 outline-generator / chapter-writer 使用，建议章节骨架：
- **Ch1 LunaTV 是什么**：空壳聚合播放器定位、功能矩阵（B1/A2）
- **Ch2 源机制原理**：api_site JSON、苹果CMS V10 接口、Base58 订阅合并、多源聚合权重（A2/B2/B3）
- **Ch3 实操：把影视站导进来**：判断接口可用 → 订阅URL 法 / 手动 JSON 法 → 保存 → 验证（C2/A2/A4）
- **Ch4 常见坑与排错**：忘保存、源失效换源、豆瓣代理、端口/镜像/登录、健康检测（C1/C2/A4）
- **Ch5 进阶**：CORSAPI 中转被墙源、自建源、网盘/Emby/IPTV（A4/B1）

素材文件：`00_intent.md`（意图）、`01_explore_result.md`（候选来源）、`02_deep_research.md`（本文）。
