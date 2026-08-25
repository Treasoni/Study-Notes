# 第一章：先搞懂 lunatv 的「源」机制

你已经把 lunatv 部署起来了，但打开首页大概率是一片空白——别慌，这是正常的。lunatv 天生是一个「空壳聚合播放器」，它自己不存任何视频，一切内容都来自你接进来的「源」。这一章我们先不上手，把「源」这套机制讲明白：它长什么样、影视站要满足什么条件才能接入、怎么一次性订阅一堆源。概念通了，后面第三章的实操才不会懵。

## 1.1 LunaTV 是什么：空壳聚合播放器

先记住一句话：**lunatv 不存储视频，它只负责聚合和播放**。[^c1-1] 项目定位上，它 fork 自 SzeMeng76/LunaTV，基于 MoonTV 深度二开，从 v4.3.1 一路迭代到 v6.6.2，累计 60+ 功能。[^c1-2]

「聚合」体现在它的内容生态上（#B1）：

| 内容类型 | 说明 |
|---|---|
| 网盘搜索 | 聚合网盘直链资源 |
| ACG 种子搜索 | 接入 Mikan 等番剧种子站 |
| IPTV 直播 | 支持 m3u/m3u8、FLV、EPG 电子节目单 |
| Emby 私有库 | 挂自己的 Emby 媒体库 |
| YouTube / Bilibili / Bangumi | 直接接入对应平台 |
| 短剧 | 聚合短剧资源 |

> [!tip] 大白话
> 把 lunatv 想成「电视遥控器」：它自己不生产任何节目，只是把一个个「频道」（也就是源）切到你面前。所以部署完打开首页一片空白是正常的——遥控器还没接上任何频道。

关键含义：**部署完的 lunatv 只是一个空壳，内容源需要你之后在管理后台运行时添加**，不需要改代码、也不用重启。[^c1-3] 后面所有操作，都是往这个空壳里「接源」。

## 1.2 核心源格式：api_site JSON

lunatv 的源配置文件是一段内嵌的 JSON，核心是一个叫 `api_site` 的对象，它是「源标识 → 源配置」的映射。[^c1-4] 每个源对象有 4 个字段：

| 字段 | 必填 | 说明 |
|---|---|---|
| `key` | 是 | 唯一标识，仅小写字母和数字；`openlist`、`xiaoya`、`emby*` 前缀为保留名（#B3） |
| `api` | 是 | 资源站的 vod JSON API 地址，支持苹果 CMS V10 格式 |
| `name` | 是 | 界面上显示的源名称 |
| `detail` | 否 | 网页详情页的根 URL |

顶层还有两个常用字段：`cache_time` 是接口缓存秒数（建议 3600–7200），`custom_category` 是数组，每项含 `name`/`type`/`query`，用于豆瓣搜索分类。[^c1-4]

一个完整的 `api_site` JSON 长这样（`mysite` 为示例占位，实际请换成你的真实站）：

```json
{
  "cache_time": 7200,
  "api_site": {
    "example_source": {
      "api": "http://example.com/api.php/provide/vod",
      "name": "示例资源站",
      "detail": "http://example.com"
    },
    "mysite": {
      "api": "https://mystation.example.com/api.php/provide/vod",
      "name": "我的影视站"
    }
  }
}
```

`key` 就是 `api_site` 里的键名（`example_source`、`mysite`），全局唯一；`name` 是你在界面上看到的名字。`detail` 可不写，比如第二个源就只填了必填的 `api` 和 `name`。

> [!tip] 大白话
> 把 `api_site` 想成一份「点菜单」：每个源就是一道菜，`api` 是去哪家后厨取菜（数据接口），`name` 是菜名。往配置里加一个源，就是在点菜单上添一道菜。

> [!tip] 大白话
> 把 `cache_time` 想成「冰箱冷藏时间」：接口数据取回来后先放冰箱 1–2 小时，不每次都去源站问。设 3600–7200 秒，能明显减轻源站压力、加快加载。

## 1.3 影视站接入标准：苹果CMS V10 接口

不是任何网站都能接入 lunatv。绝大多数国内影视站用的是**苹果CMS**（MacCMS），lunatv 的 `api` 字段支持的就是苹果 CMS V10 的 vod JSON 接口。[^c1-5]

接口标准（#B2）：

- 基础地址格式：`https://域名/api.php/provide/vod/`（注意带尾斜杠）
- `from` 参数以**路径段**追加，只返回该播放源的数据：`/api.php/provide/vod/from/m3u8/`
- 返回 JSON 关键字段：`vod_play_from`（播放源名，逗号分隔）、`type_name`（分类名）

一个实际的接口地址长这样：

```text
# 该站全部视频数据接口
https://example.com/api.php/provide/vod/

# 只取 m3u8 播放源的数据（from 以路径段追加）
https://example.com/api.php/provide/vod/from/m3u8/
```

> 说明：`from` 参数 B2 官方文档用路径段形式；部分资料把它写成 query 参数（如 `?from=m3u8`）。两种可能都被支持，具体以源站实现为准。

### 怎么判断一个影视站能不能接入

非常简单：浏览器直接打开它的接口地址，如果返回一段 JSON，说明接口正常、可以接入。[^c1-6] 这是后面第二章「找站」的核心判据。

> [!tip] 大白话
> 把苹果CMS V10 想成「行业统一的插座规格」：影视站只要按这个规格预留好插座（接口），lunatv 这个插头插上就能通电。所以判断一个站能不能接，就去看它有没有这个插座——浏览器打开接口地址，返回 JSON 就有电。

## 1.4 远程订阅与多源聚合

一个个手动加源太累了，lunatv 支持**远程订阅**：把别人维护好的一大份源配置，用一条订阅 URL 拉回来。[^c1-7]

拉取和合并的链路（#B3）：

1. 客户端向 `POST /api/admin/config_subscription/fetch` 提交远程 URL
2. 拿到响应文本后做 `bs58.decode` 解码
3. 用 `TextDecoder` 转成 UTF-8 字符串
4. 存入数据库的 `ConfigFile` 字段
5. 更新时校验 JSON 语法，再通过 `refineConfig` 把外部源**合并进活跃配置**

因为订阅内容常用 **Base58 编码的 JSON** 来传输，所以订阅链接看起来是一串短码而不是明文 JSON。[^c1-8]

聚合到同一份配置后，每个源还有几个扩展字段控制行为（#B3）：

| 字段 | 取值 | 作用 |
|---|---|---|
| `from` | `config` / `custom` | 标记源是订阅导入还是手动添加 |
| `disabled` | true/false | 设为 true 时从搜索中排除该源 |
| `proxyMode` | true/false | 服务端代理 M3U8+TS 分片，解决跨域/被墙 |
| `weight` | 0–100 | 搜索权重，数值越高结果排越前 |

> [!tip] 大白话
> 把远程订阅想成「朋友发给你的点菜单」：不用自己一个个菜名敲进去，拉取一下整份菜单就自动合并进你的点菜单。所以一键订阅 = 批量加源，后面第三章会手把手走一遍。

## 本章小结

- lunatv 是**空壳聚合播放器**，不存视频，内容全靠「源」；部署完首页空白是正常的。[^c1-1]
- 源配置的核心是 **`api_site` JSON**：每个源要 `key`（唯一标识）、`api`（必填接口）、`name`（必填显示名），`detail` 可选；顶层 `cache_time` 建议 3600–7200。[^c1-4]
- 影视站的接入标准是 **苹果CMS V10 接口**，浏览器打开 `/api.php/provide/vod/` 返回 JSON 即可接入。[^c1-6]
- 多源可以靠 **远程订阅** 批量导入：Base58 解码 → UTF-8 → 存库 → `refineConfig` 合并。[^c1-7]
- 每个源还有 `weight`/`disabled`/`proxyMode` 等扩展字段，用来控制搜索权重、排除与代理。[^c1-9]

下一章我们就要真正动手找源了：怎么判断一个影视站能不能接入、有哪些现成的订阅源可以直接用，以及怎么用健康检测数据挑出靠谱的源。

[^c1-1]: #B1 shiyu1314/LunaTV（Enhanced Edition）· https://github.com/shiyu1314/LunaTV —— 项目定位：空壳聚合、不存储视频
[^c1-2]: #B1 同上 —— fork 自 SzeMeng76/LunaTV，v4.3.1→v6.6.2，60+ 功能
[^c1-3]: #A2 LunaTV CONFIGURATION.md · https://raw.githubusercontent.com/hafrey1/LunaTV/main/docs/deployment/CONFIGURATION.md —— 配置在管理后台运行时填写，无需改代码/重启
[^c1-4]: #A2 同上 —— `api_site` 字段与顶层 `cache_time`/`custom_category`
[^c1-5]: #A2 + #B2 空壳影视官方文档·苹果CMS 对接 · https://docs.mac-cms.com/cms/cms-connect —— `api` 字段支持苹果 CMS V10 格式
[^c1-6]: #B2 同上 —— 浏览器打开接口地址返回 JSON 即接口正常
[^c1-7]: #B3 DeepWiki·MoonTVPlus 源配置 · https://deepwiki.com/mtvpls/MoonTVPlus/9.4-video-source-configuration —— fetch 接口与解码合并链路
[^c1-8]: #A2 —— 支持 Base58 编码 JSON 的远程订阅
[^c1-9]: #B3 —— SourceConfig 扩展字段 `weight`/`disabled`/`proxyMode`/`from`
