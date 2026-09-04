# AI 助手辅助视频剪辑 - 探测式收集结果（P1）

> 项目：ai-assisted-video-editing · 阶段 1 · 收集时间：2026-09-04
> 说明：三个独立镜头并行探测；记录均为候选源，未深读正文。去重按 canonical URL。

## 方向菜单

### A. AI 助手能力盘点与边界
**「AI 剪辑到底能做什么、不能做什么」——先建立全局判断。**
编码 agent（Codex CLI / Claude Code）是**编排层而非剪辑器**：无 GUI、无「眼睛」，通过沙箱化 shell 驱动 ffmpeg/Whisper/Remotion 等确定性工具。能稳定接管的是规则化、可批量的机械后期；不能接管的是节奏、表演、情绪、故事张力与逐帧精剪。适合作为笔记的开篇框架章节。

### B. FFmpeg / 工具链脚本化实战
**「用 FFmpeg + 字幕 + 批处理脚本把单个操作真正跑通」。**
无损剪切走 `-ss 前置 + -c copy`（关键帧吸附），拼接用 concat demuxer（编码参数必须一致），字幕自动化固定链「静音裁剪 → Whisper 转写 → 烧录」，剪映 `draft_content.json` 可被 Python 脚本化（有版本墙）。以 **skill/脚本封装 + `--dry-run`/`--json`** 让 agent 输出稳定。

### C. 人机协作流水线设计
**「把整套剪辑流程建成可编辑、可验证、可回滚的 agent 流水线」。**
主流范式：agent 当操作员、人当决策者。链路：读工程（inspect）→ 出镜头清单/策略（不落盘，供人审）→ 缩略图预览 → 确认 → 事务式写入时间线 → ffmpeg 渲染 → ffprobe 校验 → 人进剪映/PR 精修。安全靠默认只读、工作副本、allow/ask/deny、hooks 门禁。

---

## 候选源清单

### Lens A：AI 助手能力盘点

1. 标题: OpenAI Codex CLI（官方 README）
   URL: https://github.com/openai/codex
   层级: official · 评分: 3
   相关度: 官方能力基底——沙箱化 shell、多档审批、图片输入，解释 agent 为何只能走脚本流程而非 GUI。
2. 标题: ffmpeg-skill（kajisho5）
   URL: https://github.com/kajisho5/ffmpeg-skill
   层级: implementation-report · 评分: 4
   相关度: 面向 Codex/Claude Code 的 ffmpeg 技能包：场景检测/高光、去静音跳切、拼接、字幕烧录、响度、HDR→SDR、多机位对齐。
3. 标题: Claude Code for Video: It Edits, But Not How You Think
   URL: https://nahornyi.ai/en/news/claude-code-video-editing-automation
   层级: implementation-report · 日期: 2026-03-23 · 评分: 4
   相关度: Claude Code 拼装 FFmpeg/Remotion/OpenCV/Whisper 管道，适合批量同质视频；缺架构会退化为易碎脚本。
4. 标题: Agentic AI 剪片實測：Claude Code 能做的事與做不到的事
   URL: https://www.imnobby.com/2026/06/26/agentic-ai-%e5%89%aa%e7%89%87%e5%af%a6%e6%b8%ac/
   层级: community · 日期: 2026-06-26 · 评分: 4
   相关度: 一手中文实测：能批量转码/裁剪/合并/字幕；不能感知节奏、表演、故事张力。
5. 标题: Why AI Agents Can't Fix Video Sync Issues (Yet)
   URL: https://dev.to/wcamon/why-ai-agents-cant-fix-video-sync-issues-yet-a-surgeons-midnight-debugging-session-4j5k
   层级: community · 评分: 4
   相关度: concat 造成音画同步漂移对 agent「静态分析不可见」，会在错误方案里反复调参，需人工换架构。

### Lens B：工具链与脚本化方案

1. 标题: video-editing-skill（6missedcalls）
   URL: https://github.com/6missedcalls/video-editing-skill
   层级: community · 评分: 5
   相关度: FFmpeg+Whisper 纯 Bash skill，裁剪/跳切/字幕/变速，供 Claude Code/Codex 自然语言驱动。
2. 标题: claude-skill-auto-subtitles（sketch-man）
   URL: https://github.com/sketch-man/claude-skill-auto-subtitles
   层级: community · 评分: 4
   相关度: Whisper 词级时间戳 → 语义分块 → styled ASS → libass 烧录，含幻觉过滤。
3. 标题: JianYingDraft
   URL: https://github.com/Slihao/JianYingDraft
   层级: community · 评分: 4
   相关度: 读写剪映 `draft_content.json`（materials/tracks/微秒时间轴）与批量导出；版本墙：模板≤5.9、导出≤6。
4. 标题: FFmpeg Lossless Concatenation with the concat Demuxer
   URL: https://ffmpeg-cookbook.com/en/articles/concat-protocol/
   层级: implementation-report · 评分: 4
   相关度: concat demuxer + `-c copy` 无损拼接的硬性前提与批量 list.txt 生成模式。
5. 标题: Python yt-dlp automatically using FFmpeg to merge audio and video files
   URL: https://stackoverflow.com/questions/78990962/
   层级: community · 评分: 3
   相关度: yt-dlp 内建 FFmpeg 后处理合并的实操细节（bestvideo+bestaudio）。

### Lens C：人机协作工作流

1. 标题: Codex Automated Video Editing Workflow
   URL: https://www.nemovideo.com/blog/codex-automated-video-editing-workflow
   层级: implementation-report · 评分: 5
   相关度: Codex 当操作员：参考片→镜头清单（提案）→缩略图供人审→JSON/CSV 时间线→人到剪映精修；只读源素材+工作副本+固定版本护栏。
2. 标题: 用 Agent Skill 构建可编辑可验证的 AI 视频生产流水线（Timeline Studio）
   URL: https://developer.aliyun.com/article/1754064
   层级: implementation-report · 日期: 2026-08-07 · 评分: 5
   相关度: inspect / diff（非破坏校验）/ run（事务式+operationId）三段式，渲染视频与 .timeline 双通过才算完成。
3. 标题: video-use：Agent 剪视频的关键，不是「看视频」而是「读视频」
   URL: https://cloud.tencent.com.cn/developer/article/2707362
   层级: implementation-report · 评分: 4
   相关度: 素材转写为带时间戳文本→inventory→提剪辑策略→等用户确认→执行；人保留节奏与审美。
4. 标题: Claude Code 官方安全文档（Security / Hooks）
   URL: https://code.claude.com/docs/en/security
   层级: official · 评分: 4
   相关度: 默认只读、allow/ask/deny（deny 优先）、启动目录边界、PreToolUse hooks 门禁——批量操作安全底座。
5. 标题: Codex 剪视频 10 分钟干完一个月活？创作者实测
   URL: https://post.smzdm.com/p/a5rgg7n3/
   层级: community · 评分: 3
   相关度: 删停顿/对字幕/自动切分提效显著；成片节奏偏平均、不主动建议 B-roll，需人工反复迭代。

---

## 覆盖缺口

- **官方一手文档**：本轮检索未直接返回 ffmpeg.org、yt-dlp 官方 wiki 的具体页面 URL，P2 需补抓官方命令参考页。
- **剪映/CapCut 官方自动化**：仅社区库（JianYingDraft），官方脚本/导出能力边界需核实。
- **实际成本数据**：token/时长成本、渲染耗时缺少量化案例（仅 smzdm 定性）。
- **中文生态 vs 英文生态**：中英文 source 各半，可支撑中文笔记但需在 P2 归类标注语言与适用工具。

## P2 预估范围

- 方向 A/B/C 若都做：深读核心源 8–10 篇（官方 + 高星 implementation-report 为主），产出命令级要点与可复用模板。
- 单一方向侧重：核心源可压缩到 3–5 篇 + 按需补缺口。
- 预计产物：`02_deep_research.md`（scope、source table、claim/source map、contradictions、实践指引、开放问题、下游交接）。
