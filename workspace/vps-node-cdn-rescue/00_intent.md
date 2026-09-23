# VPS 被墙节点 CDN 拯救实战（Cloudflare CDN 回源） - 意图文件

## 基本信息

- **主题**: VPS 被墙节点 CDN 拯救实战（Cloudflare CDN 回源）
- **项目标识**: vps-node-cdn-rescue
- **运行标识**: vps-node-cdn-rescue
- **工作流**: learning-note-flow（mode: outline）
- **创建时间**: 2026-09-24
- **当前阶段**: 阶段 0
- **输出目标**: obsidian
- **Vault 路径**: D:\Study-Notes
- **笔记目录**: 自建代理节点
- **MOC 路径**: 自建代理节点/自建代理节点 MOC.md

## 学习目标

### 笔记类型
概念 + 实战混合（CDN 是什么/解决什么问题 → Cloudflare 接入与回源配置全流程 → 被墙判定与加速取舍）

### 学习深度
入门 → 上手

### 用户基础
有网络/软路由基础（已写过旁路由、内网穿透、Tailscale 类笔记）；
同系列面板流节点搭建流程已梳理（`vps-node-panel-tutorial`，进行中）；
CDN 与 Cloudflare 为零基础。

## 来源

### 主来源（视频，无字幕）
- URL: https://www.youtube.com/watch?v=NnyG3DyZbN8
- 标题: 自建节点被墙怎么办？免费CDN拯救被墙节点！| CDN是什么 | CDN作用 | CDN回源加速 | VPS套CDN | Cloudflare CDN
- 频道: 无限芝士 InfiCheesy（第 78 期）｜时长 10:37（637s）｜发布 2026-01-15
- 视频章节（写作主线骨架）:
  - 0:00 开头
  - 0:20 CDN是什么
  - 2:33 获取CDN
  - 3:30 解析域名
  - 4:52 安装面板
  - 6:26 搭建节点
  - 9:22 被墙风险
  - 10:00 加速问题

> **⚠ 字幕不可得**（本次已两次独立核验：watch 页 `ytInitialPlayerResponse` 无 `captionTracks` 字段；
> `yt-dlp --list-subs` 返回 "has no automatic captions / has no subtitles"）。因此**不能获取逐字转录**。
> 后果：视频内的**口播结论必须标注为「据视频章节推断」**，不得伪装成视频原话；
> 可核验的事实性内容一律以 Cloudflare 官方文档、Xray/3x-ui 官方文档为准。

### 作者配套文档（视频描述中的官方链接，可公开访问）
- 视频中所用代码（含域名解析/面板/建节点步骤文档）: https://wise-vegetarian-da6.notion.site/VPS-2daacc0097d38077a769e8a98051fec1
- Cloudflare 官网（中文）: https://www.cloudflare.com/zh-cn/
- IP2Location（IP 归属/风险查询）: https://www.ip2location.com/
- 同系列前置视频（零基础自建节点教程）: https://youtu.be/MuWTmEiNe1g
- 同系列配套视频（低价域名获取）: https://youtu.be/gKQTtY_YQnA
- 同系列配套视频（托管与解析域名教程）: https://youtu.be/x_-76QVuC3c

### 相关既有笔记（需双向互链，内容互补不重叠）
- `自建代理节点/自建代理节点搭建实战.md` — 内核直配向（分层模型、REALITY 原理、VPS 硬化、服务端/客户端配置）
- `自建代理节点/自建代理节点 MOC.md`
- 同系列**进行中**运行：`workspace/workflow-runs/vps-node-panel-tutorial.workflow.md`（面板流全流程，当前 P2）

### 本篇相对既有笔记的差异化定位
| 维度 | 面板流（vps-node-panel-tutorial） | 内核直配旧笔记 | **本篇（CDN 篇）** |
|---|---|---|---|
| 主线 | VPS 选购 → SSH → 面板 → 建节点 → 带域名 | 分层模型与内核配置 | **CDN 概念 → Cloudflare 接入 → 回源加速 → 被墙场景** |
| CDN | 未覆盖（被墙方案只有「换 IP」） | 未覆盖 | **本篇核心** |
| 面板安装/建节点 | 本篇主线，逐步展开 | 手写 JSON | **不复述**，只写「前置已完成」并链回面板流笔记 |
| 受众 | 零基础跑通 | 有基础重原理 | 已完成节点搭建、想抗封锁/加隐藏的人 |

## 研究计划

### 探索方向
1. 概念层：CDN 是什么、解决什么问题、回源（origin pull）与边缘节点、CDN 为什么能隐藏真实 IP、CDN 加速与抗封锁的边界
2. 落地层：Cloudflare 账号与站点接入 → 域名 NS 切换与解析 → 节点套 CDN 的配置（端口/协议选择、TLS 模式、代理开关）
3. 运维层：被墙的判定依据（IP/端口被封 vs 域名被污染）、CDN 方案的失效场景与代价（延迟、证书、协议限制）、加速问题的取舍

### 重点收集
- **核心概念**: CDN、边缘节点、回源、CNAME/NS 接入、代理状态（proxied / DNS only）、TLS 模式（Flexible/Full/Full Strict）、SNI 与证书、真实 IP 隐藏、Cloudflare 免费版限制（支持的端口、协议）
- **实战步骤**: Cloudflare 注册与站点添加、NS 修改、DNS 记录（A/AAAA/CNAME）、开启小黄云、源站端口与协议调整、面板侧建节点时如何填地址、客户端侧配置与验收
- **常见坑**: NS 未生效、代理端口不在 Cloudflare 支持列表、TLS 模式不匹配导致 525/526 或回环、开了 CDN 反而变慢、CF 到源站仍走明文、免费版对非标准端口的限制、被墙后套 CDN 为什么可能仍然不通（域名污染 vs IP 封锁的区别）
- **工具链**: Cloudflare Dashboard、dig/nslookup 与在线 DNS 检查、IP2Location、3x-ui / Xray-core、客户端（Clash/Mihomo、sing-box、Shadowrocket 等）
- **边界与风险**: CDN 免费版的合规与限速、Cloudflare 对代理流量的态度、免费域名的风险、不要裸奔的说明

### 信源偏好
- 官方文档: 是（**Cloudflare 官方文档优先**：proxy status、支持的端口、TLS 模式；Xray/3x-ui 官方文档）
- 技术博客: 是（仅作补充，须回源核对）
- 社区讨论: 谨慎（仅用于踩坑点佐证）
- 学术论文: 否
- 作者配套文档: 是（视频步骤的对应书面来源）

## 备注

- **来源纪律**：向 `research-collector` 与 `chapter-writer` 派活时只传来源 ID + 检索位置，要求先回原文核对再落笔；凡出现「官方口径 / 官方说明 / 原文」处，验收时逐条回源比对。视频口播不可得，凡视频结论必须标注「据视频章节推断」。
- **与进行中运行的去冲突**（需在 P2/P3 执行）：`vps-node-panel-tutorial` 的「节点被墙」章节只写**判定 + 一句“CDN 方案见 [[CDN 拯救被墙节点]]”**，展开留给本篇；本篇不复述面板安装与建节点步骤。若那边已写入 CDN 细节，按此口径回改。
- **互链**：Phase 6 发布时与 `自建代理节点搭建实战.md`、`自建代理节点搭建实战（面板流）` 建立双向链接；Phase 7 同步 MOC，归入「节点搭建」或新增「抗封锁与加速」分组。
- **Phase 1 可精简**：学习方向已由视频章节结构 + 用户确认锁定，探测式收集按「核验可写性」执行，不再发散铺开方向菜单。
- **待用户确认项**（Phase 0 检查点）: ① CDN 概念部分按「概念+实战」混合写还是纯实战；② 域名前置（免费域名获取/解析）只做指路还是展开一节；③ 是否纳入 Cloudflare 免费版限制的完整端口表。
