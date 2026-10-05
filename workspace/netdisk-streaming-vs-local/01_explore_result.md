# 01 探测结果（阶段 1：探测式收集）

- **主题**: 网盘影视播放与本地存储的取舍（网盘在线播放 vs 302 直链播放 vs 本地下载）
- **项目标识**: netdisk-streaming-vs-local
- **探测时间**: 2026-10-05
- **检索日期（所有来源）**: 2026-10-05
- **探测视角**: 3 个（技术差异与网盘优化功能 / 为何下载到本地 / 风险与成本）

## 候选来源表（已按 canonical URL 去重）

| ID | 标题 | URL | 层级 | 日期 | 得分 | 视角 |
| --- | --- | --- | --- | --- | --- | --- |
| S1 | 基本配置（proxy / webdav_proxy / webdav_direct）— Alist Document | https://alist-doc.nn.ci/docs/driver/base/ | official | 未知 | 5 | 技术差异 |
| S2 | go-emby2openlist（Emby + OpenList 网盘直链反向代理）README | https://github.com/AmbitiousJun/go-emby2openlist | official | 未知 | 5 | 技术差异 |
| S3 | 如何在线预览视频 — 115 帮助 | https://q.115.com/115115/T823179.html | official | 未知 | 5 | 网盘优化功能 |
| S4 | openlist 用两种方式挂载夸克网盘，支持 302 的方式一定更厉害吗？ | https://post.smzdm.com/p/avv46lx9/ | community | 未知 | 4 | 技术差异 |
| S5 | 多网盘管理/音视频播放软件汇总 | https://github.com/oldsento/Multiple-cloud-storage-management-or-mediaplayer-software-collection | community | 未知 | 3 | 网盘优化功能 |
| S6 | 实测 8 款网盘下载速度：非会员疑被限速，开会员即提速（澎湃「马上测」；新浪财经转载 https://finance.sina.com.cn/jjxw/2025-03-31/doc-inerpuqk8199305.shtml） | https://m.thepaper.cn/newsDetail_forward_30512452 | reputable-report | 2025-03-31 | 5 | 成本 / 风险 |
| S7 | 普通用户 96-170KB/s！百度网盘客服回应非会员"龟速"下载 | https://m.thepaper.cn/newsDetail_forward_30513842 | reputable-report | 2025-03-31 | 4 | 成本 |
| S8 | 百度网盘下载常见问题（超级会员不限速、非会员按主端速率限速） | http://tousu.baidu.com/question2?prod_id=257&class=801&id=1002116 | official | 未知 | 3 | 成本 |
| S9 | 还有必要自建 NAS 本地影视库吗？ — V2EX | https://global.v2ex.co/t/1179544 | community | 2025-12-17 | 5 | 本地价值 |
| S10 | 群晖进阶：Emby + SmartStrm 实现 Strm 流媒体播放 | https://post.smzdm.com/p/al35d0we/ | community | 2026-04-17 | 4 | 本地价值 |
| S11 | I switched from streaming to self-hosting my media — it cost more than I expected — XDA | https://www.xda-developers.com/switch-from-streaming-to-self-hosting-media-cost-more-than-expected/ | reputable-report | 2026-03-27 | 5 | 本地价值 / 成本 |
| S12 | 号称"史上最严"的网盘整治，让多少搬运博主连夜跑路？ — 虎嗅 | https://www.huxiu.com/article/4852261.html | reputable-report | 2026-04-20 | 5 | 风险 |
| S13 | 百度网盘会员服务协议（可删除违规内容、限制播放分享、封禁账号，费用不退） | https://pan.baidu.com/disk/vipduty | official | ©2026 | 5 | 风险 |
| S14 | NAS vs 网盘｜谁才是性价比之选？大对比 | https://post.smzdm.com/talk/p/a34k8897/ | community | 2025-02-13 | 4 | 成本 |
| S15 | SmartStrm 常见问题 FAQ（夸克可 302 的直链必为转码、可能压缩画质） | https://smartstrm.github.io/help/faq.md | official（工具项目） | 未知 | 4 | 风险 / 画质 |
| S16 | 百度网盘公告：涉侵权文件全面清理、严重违规永久封禁 | http://pan.baidu.com/res/static/notic.html | official | 2020-06 | 2 | 风险（历史政策，仅参考） |

> S6 与澎湃原文为同一篇报道的两个发布页（新浪财经转载 / 澎湃原文），合并为一条。

## 方向菜单（请选择 P2 深挖方向）

**A. 三方式全景对比 +「为什么还要下载到本地」（推荐）**
以「网盘自带播放 / 302 直链播放 / 本地下载」三条路线为主线，按维度（画质、流畅度、成本、离线、风险、维护）做对比表 + 决策流程，正面回答用户两组问题。覆盖 S1–S11、S13–S15。

**B. 聚焦技术差异：网盘自带播放 vs 302 直链播放**
只深挖「谁在解码/传输、转码与直链的分野、网盘优化功能的代价」，不做存储成本账。覆盖 S1–S5、S15，可加 S3 补充。

**C. 聚焦「网盘 vs 本地」的账与风险**
只做存储选型：限速、费用、内容被删/封号、原盘画质、长期保存。覆盖 S6–S14。

## 覆盖缺口（需在 P2 补，或按社区经验谨慎标注）

1. **网盘自带播放器的「HDR / 画质增强」**：缺官方说明，仅社区播放器汇总（S5）间接佐证。
2. **各网盘官方在线播放清晰度档位**（如"百度在线播放最高约 480p"）：无官方文档，需谨慎标注。
3. **302 直链过期时长**：无官方说明；只能用 S12 的"分享链接一夜失效"替代描述。
4. **隐私泄露 / 网盘播放风控导致封号**：缺权威一手来源，仅 S12 口径间接支撑。
5. **Plex 官方 Direct Play / 转码文档**：多次 403 未取到，缺一个官方"直连 vs 转码"的权威对照。

## P2 预估范围

- 核心深读来源：**4–6 个**（建议 S1、S3、S6、S9、S11、S13）。
- 填补缺口来源：另加 **2–3 个**（优先补"直连 vs 转码"官方说明、网盘在线播放清晰度官方口径）。
- 预计产出：`02_deep_research.md`，含来源表、claim/source 映射、冲突点、实践建议、遗留问题。
