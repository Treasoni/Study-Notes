# 探测结果 - 如何把影视网站导入到本地部署的 lunatv

> 项目：lunatv-import-sites · 阶段 1（探测式收集）· 2026-08-25
> 已确认方向：A（源类型/格式）+ B（影视站接入）+ C（常见坑排查）

---

## 候选来源清单（按视角分组，已按 URL 去重）

### A. 片源/订阅源类型与配置格式

| # | 标题 | 来源 | tier | 评分 | 相关点 |
|---|------|------|------|------|--------|
| A1 | [LunaTV 官方仓库 README（hafrey1/LunaTV）](https://github.com/hafrey1/LunaTV) | GitHub | official | 5 | 官方源类型清单：m3u/m3u8、FLV、EPG、M3U 导入导出；Emby 集成 |
| A2 | [LunaTV CONFIGURATION.md（raw）](https://raw.githubusercontent.com/hafrey1/LunaTV/main/docs/deployment/CONFIGURATION.md) | GitHub | official | 5 | **核心**：api_site JSON 格式、必填环境变量、DOCKER_ENV 加载策略 |
| A3 | [DeepWiki - MoonTV Configuration System](https://deepwiki.com/senshinya/MoonTV/8-configuration-system) | DeepWiki | tutorial | 4 | ApiSite 接口 4 属性；cache_time/api_site/custom_category 顶层字段 |
| A4 | [hafrey1/LunaTV-config](https://github.com/hafrey1/LunaTV-config) | GitHub | community | 4 | 现成苹果CMS 源聚合（jin18/jingjian/full），Base58 订阅串 + CORSAPI 代理 |
| A5 | [KTV（chris202010）二创](https://github.com/chris202010/KTV) | GitHub | community | 3 | 后台可导入/导出 config.json、拖拽排序、实时生效 |

### B. 主流影视站资源接入方式

| # | 标题 | 来源 | tier | 评分 | 相关点 |
|---|------|------|------|------|--------|
| B1 | [LunaTV（shiyu1314/LunaTV）仓库](https://github.com/shiyu1314/LunaTV) | GitHub | official | 5 | 主项目本体：JSON api_site 指向苹果CMS API；支持订阅源、网盘搜索（PanSou） |
| B2 | [空壳影视官方文档「苹果CMS 对接」](https://docs.mac-cms.com/cms/cms-connect) | 官方文档 | official | 5 | **核心**：标准接口 `/api.php/provide/vod/`，`$` 聚合多站，`from=m3u8` 筛选 |
| B3 | [MoonTVPlus Video Source Configuration](https://deepwiki.com/mtvpls/MoonTVPlus/9.4-video-source-configuration) | DeepWiki | tutorial | 4 | 源字段含 key/name/api/detail/from/proxyMode/weight；远程订阅 Base58 解码合并 |
| B4 | [苹果CMS搬家笔记（177IDC）](https://www.177idc.com/post/597.html) | 博客 | community | 4 | 主流资源站快但易限流；备份 `data/collect` 或 `mac_collect` 表恢复 |
| B5 | [ocean2025/tBox 影视源订阅 JSON](https://github.com/ocean2025/tBox) | GitHub | community | 3 | 可直接用网盘源订阅（夸克/UC/天翼），含会员/IP 限制提示 |

### C. 常见坑与排查

| # | 标题 | 来源 | tier | 评分 | 相关点 |
|---|------|------|------|------|--------|
| C1 | [飞牛Docker系列：LunaTV部署教程（避坑版）](https://bbs.nasdiyer.com/forum.php?mod=viewthread&action=printable&tid=21625) | 论坛 | tutorial | 5 | 源失效→换源可恢复；豆瓣代理环境变量；官方镜像选择；端口冲突 |
| C2 | [LunaTV的配置与使用技巧（懒猫微服）](https://lazycat.cloud/playground/guideline/1244) | 博客 | tutorial | 5 | 空壳到有源全流程；**忘点"保存"源不生效**；豆瓣代理不设首页空白 |
| C3 | [KatelyaTV（MoonTV 二创）](https://github.com/haogege8888/KatelyaTV) | GitHub | community | 4 | 修复 OrionTV 源无法播放、源一键导入导出；已移除内置源需自配 |
| C4 | [stazeng/LunaTV-EE（增强版）](https://github.com/stazeng/LunaTV-EE) | GitHub | community | 3 | 确认空壳无内置源；内置源浏览器/测试模块便于排查 |

> 去重说明：`hafrey1/LunaTV-config` 在 A4 与 C 视角重复出现，保留在 A 组并在 P2 复用其健康检测数据。

---

## 方向菜单（P2 深挖候选）

- **A. 源类型与配置格式**（推荐）→ 深读 A1/A2/A3，把 api_site JSON、环境变量、DOCKER_ENV 讲透
- **B. 影视站接入方式** → 深读 B1/B2/B3，覆盖苹果CMS 标准接口、订阅源、网盘源、聚合源
- **C. 常见坑与排查** → 深读 C1/C2/C3，整理源失效、保存不生效、豆瓣代理、换源等排错清单

用户已在阶段 0 选择 **A+B+C 全做**。

---

## 覆盖缺口（Gaps）

1. **官方排错文档缺失**：LunaTV 无官方 troubleshooting，最接近"官方"的是各 fork 的 README。
2. **自定义环境变量加源**（CUSTOM_SOURCE_*）的具体格式缺少一手来源，仅 A2 部分提及。
3. **源失效量化数据**：LunaTV-config 健康检测（72 API，92% 可用率）说明失效是常态，但"如何自行验证一个源可用"缺少系统方法。
4. **豆瓣代理问题**：懒猫教程评论区有未解决的社区反馈（选遍选项仍失败）。

---

## 预计 P2 范围

- **核心深读 4-5 个源**：A2（官方配置）、B2（苹果CMS 对接标准）、B1（主项目）、A4/LunaTV-config（真实源清单+健康检测）、C1/C2（实操避坑）。
- **补齐缺口**：源可用性验证方法、CUSTOM_SOURCE 环境变量、换源/排错流程。
- **产出 `02_deep_research.md`**：scope、来源表、claim/source 映射、矛盾点、实操指引、开放问题。
