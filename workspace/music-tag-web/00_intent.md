# 如何使用 Music Tag Web - 意图文件

## 基本信息

- **主题**: 如何使用 Music Tag Web（自托管音乐标签编辑器）
- **项目标识**: music-tag-web
- **来源项目**: https://github.com/xhongc/music-tag-web （默认分支 `dev_1.0`）
- **创建时间**: 2026-09-14
- **当前阶段**: 阶段 0（意图澄清，等待用户确认）
- **输出目标**: 项目 output（待用户确认是否发布到 Obsidian vault）
- **Vault 路径**: 待指定
- **笔记目录**: 待指定
- **MOC 路径**: 待指定

## 学习目标

### 笔记类型
实战笔记（面向使用者的部署 + 上手操作指南）

### 学习深度
上手（能独立部署、跑通「挂载曲库 → 刮削 → 批量改标签 → 整理」主流程）

### 用户基础
待确认（推测：有 Docker/NAS 基础，未用过本项目）

## 已核实事实（2026-09-14 经 GitHub API + raw README）

| 项 | 值 |
| --- | --- |
| 仓库 | `xhongc/music-tag-web` |
| 描述 | 音乐标签编辑器，可编辑本地音乐文件元数据、音乐刮削 |
| 语言 | Python |
| Stars / Forks | 6041 / 428 |
| License | GPL-3.0（含附加条款：禁止商业用途） |
| 默认分支 | `dev_1.0` |
| 最近推送 | 2026-09-04 |
| 官网 | http://www.musictagweb.com |
| Docker 镜像 | `xhongc/music_tag_web:latest`（amd64 / arm64） |
| 容器端口 | V1 = 8001，V2 = 8002（README 内两套并存） |
| 卷挂载 | `/app/media`（曲库）、`/app/data`（配置持久化） |
| 管理后台 | `/admin`，默认 admin/admin |
| 官方手册 | https://xiers-organization.gitbook.io/music-tag-web/ （V1）、…/music-tag-web-v2/ （V2） |

## 研究计划

### 探索方向
1. **项目定位与能力边界**：它解决什么问题，与 MP3Tag / MusicBrainz Picard / Navidrome 的关系，能做什么、不能做什么
2. **部署方式**：`docker run` 与 `docker-compose`（`compose/local`、`compose/prod`），NAS（群晖/威联通）容器管理器路径，V1 与 V2 的端口与 `command: /start` 差异
3. **核心操作流程**：挂载曲库 → 扫描 → 刮削匹配 → 批量编辑/替换 → 整理分类 / 繁简转换 / 格式转换 / 整轨分轨 → 移动端访问
4. **常见坑与排错**：端口、卷路径、文件权限、中文乱码、封面与歌词源、默认密码、镜像 tag、Navidrome 联动
5. **工具链与生态**：Navidrome / Jellyfin 边车用法、ffmpeg、音乐指纹识别、CUE 分轨、播放统计

### 重点收集
- **核心概念**: self-hosted、Docker 卷挂载、音频元数据/ID3 标签、音乐刮削（scraping）、音乐指纹识别、整轨 CUE 分轨、Navidrome 边车
- **实战配置**: 可复制粘贴的 `docker run` 与 `docker-compose.yml`，NAS 容器管理器配置项
- **常见坑**: 端口混淆、卷路径写错、权限不足、默认密码未改、镜像名与 tag 误用、版权数据的 24h 清除约定
- **工具链**: `xhongc/music_tag_web` 镜像、官方 GitBook 手册（V1/V2）、Navidrome、Jellyfin、ffmpeg

### 信源偏好
- 官方文档: 是（GitBook 手册优先）
- 项目 README / 仓库文件: 是（但需交叉核实，见下方备注）
- GitHub Issues / 社区讨论: 是（排错素材）
- 第三方博客/教程: 是（补充实拍步骤，需标注来源层级）

## 备注

1. **README 不可直接照抄**：`dev_1.0` 分支的 README 有明显 SEO 化改写痕迹，且同一文件内 V1/V2 部署说明并存、端口不一致（8001 vs 8002）。收集阶段必须回源核实：Docker Hub 镜像 tag、仓库 `compose/local` 与 `compose/prod` 内实际文件、`local.yml`/`local.bak.yml`、GitBook 手册，逐条确认后再落笔。
2. **禁止商业用途**：项目为 GPL-3.0 且带附加条款，笔记中应如实记录许可与免责声明要点，不暗示可商用。
3. 本项目只编辑本地已有音乐文件的元数据，不提供音乐下载——笔记需明确这一能力边界，避免误导。
