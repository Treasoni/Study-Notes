## 第 5 章：工具链速查 —— FFmpeg / Whisper / yt-dlp 的 hard rules

前面几章搭好了「素材工程化 → 策略提案 → 人审 → 安全执行」的骨架，但真正让流水线稳定跑起来的，是这一层命令级细节。本章把支撑流水线的 hard rules 收拢成速查：**核心只有两条主线——「无损」和「不炸音频」**。这些规则听起来不像创意，却恰恰决定了 AI 剪辑能不能稳定工作（S6）。每条规则给最小可用命令 + 一句话解释，按需查阅即可，不必一次背完。

> [!tip] 大白话
> 把这几条 hard rules 想成厨房的「生熟分开」：不是让菜更好吃，是让流程不出食品安全事故。所以……本章没有一条命令在教你怎么剪得「好看」，全在教你怎么剪得「不坏」——不重编码损画质、不爆音、不把字幕叠没。

### 5.1 无损三件套：stream copy、concat demuxer、编码参数一致

**规则：多段素材先分段抽取，再无损 concat（`-c copy` + concat demuxer），避免反复编码；拼接前提是各片段编码参数一致**（S6；无损 concat 前提另见 P1 LensB）。

第一件：单段无损剪切。`-c copy` 表示**不重编码**，只把选中区间的码流原样拷贝进新容器，速度接近实时、画质零损失：

```bash
# 从 take01.mp4 抽出 00:01:23.500 起共 8 秒，不重编码（-ss / -t 放在 -i 之前做输入定位）
ffmpeg -ss 00:01:23.500 -t 8.000 -i take01.mp4 -c copy edit/clip_a.mp4
```

> [!warning] `-c copy` 的代价：切点吸附关键帧
> 不重编码意味着不能精确到任意帧——输出会从**前一个关键帧**开始，实际长度可能比你要的多出几帧到一两秒。它适合「粗切、抽素材、攒预览」；要精确下刀，见 5.2 的重编码版本。这也是第 6 章验证门要逐切点查「多帧/跳帧」的原因。

第二件：无损拼接。先把所有片段写进一个清单文件，再用 concat demuxer 一次性组装：

```bash
# concat.txt（放在项目根目录，路径相对当前工作目录，空格需转义）
file 'edit/clip_a.mp4'
file 'edit/clip_b.mp4'
file 'edit/clip_c.mp4'
```

```bash
# 清单文件做输入，-c copy 不重编码拼接
ffmpeg -f concat -safe 0 -i concat.txt -c copy edit/assembly.mp4
```

第三件是前提，也是最常被忽略的：**concat demuxer 只在各片段编码参数一致时可靠**——同 codec、同分辨率/帧率、同采样率/声道数。来自不同来源（手机、相机、录屏、下载）的片段直接拼，轻则花屏音画错位，重则就是第 1 章那个「agent 看不到的漂移」。所以正规套路是：**在抽取阶段就把片段统一成同一种中间格式**，再 concat：

```bash
# 统一中间格式：H.264 + yuv420p + AAC 48kHz 双声道（只需对要拼接的片段做一次）
ffmpeg -i edit/clip_b.mp4 -c:v libx264 -pix_fmt yuv420p -crf 18 -c:a aac -ar 48000 -ac 2 edit/clip_b_norm.mp4
```

> [!tip] 大白话
> 把 `-c copy` 想成搬家工人只搬箱子、绝不开箱重打包：快且无损；但前提是这批箱子规格得一样，否则搬进同一间屋子根本摞不起来。所以……「无损拼接」真正的功夫在拼接之前——先把各片段统一规格，最后那步 `-c copy` 才敢说无损。

### 5.2 不炸音频规则：30ms fade + 不在词中间下刀

**规则一：每个剪切点加 30ms audio fade，防爆音**（S6）。硬切会产生一个近乎瞬时的音量跳变，听感是「啪」的一声。30ms（0.03 秒）足够把跳变抹平、又短到人耳几乎察觉不到是淡入淡出。

fade 属于音频重编码，无法 `-c copy`，所以它和「精确剪切」合并在同一条命令里做——只对切出来的短段编码一次，成本可控：

```bash
# 精确切 8 秒 + 首尾各 30ms 音频 fade（afade: in 从 0 开始 0.03s，out 在 7.97s 开始 0.03s）
# 注意：st 用「片段时长 - 0.03」算 fade-out 起点；时长以 ffprobe 实测为准
ffmpeg -ss 00:01:23.500 -t 8.000 -i take01.mp4 \
  -af "afade=t=in:st=0:d=0.03,afade=t=out:st=7.97:d=0.03" \
  -c:v libx264 -crf 18 -c:a aac -b:a 160k edit/clip_a.mp4
```

**规则二：不能切在词中间，剪切点必须贴合逐词时间戳**（S6）。转写层给的逐词时间戳就是这里的「下刀坐标」：把词的起点/终点当作候选切点，宁可多留半个词也不把词拦腰切断（S6）。音频信号层面，「词中间」往往是辅音或气声密集区，切在这里比切在词间静音更容易出爆音。

> [!tip] 大白话
> 30ms fade 像给剪切边贴一条 3 厘米的透明胶带：不让毛边硌手。不在词中间下刀，则是「剪句子挑逗号处剪，别从字中间劈开」。所以……两条都是「把切口弄干净」，前者治物理爆音，后者治听感断字。

### 5.3 字幕的时序与层级：输出时间轴 + 滤镜链最后 + 首版不烧录

字幕有三条独立规则，别混在一起记：

**① 字幕滤镜放滤镜链最后**（S6）。只要后面还跟着 scale / crop / pad 等任何视频滤镜，字幕就可能被二次缩放遮住或裁掉。凡要烧录字幕，`subtitles=` 必须是 `-vf` 链的**最后一个**：

```bash
# 竖版 9:16 + 字幕：scale 先适配、pad 再补边、subtitles 放最后
ffmpeg -i edit/assembly.mp4 \
  -vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2,subtitles=out.srt" \
  -c:v libx264 -crf 20 -c:a copy edit/preview.mp4
```

**② 字幕时间用输出时间轴，不是素材时间轴**（S6）。从源素材切走 1:40 后，原本在 `00:02:00` 的词在成片里是 `00:00:20`。若拿源 SRT 直接烧，字幕会全部错位。正确做法是让字幕从生成起就基于**输出时间线**。

**③ 首版不烧录字幕**（S3）。烧录是把文字焊死在画面上，之后改错别字、断句、样式都要重渲染。第一稿保持 `.srt` / `.ass` 这类可编辑数据；TTS 语音与字幕要从**同一份锁定的脚本**生成，保证词、时间、审阅意见始终对得上（S3）。等文案、断句、时长都过审了，最后导出时再走上面那条烧录命令。

> [!tip] 大白话
> 把「素材时间轴 vs 输出时间轴」想成搬家前后的页码：书在原书架上是第 100 页，搬走前面 90 页后它在新书架是第 10 页，字幕标的是「新书架的页码」。所以……删改越多，越不能拿素材原时间戳硬套，字幕必须跟着输出时间线重排。

### 5.4 素材获取：yt-dlp 下载与 Whisper 转写的最小命令

流水线第一步常是「拿一段参考片或自己的历史素材做 inventory」。下载用 yt-dlp，转写用 Whisper，二者可串成一条最小组合：

```bash
# 只取音频做转写（-x = 抽取音频，需本机已装 ffmpeg；产物进 edit/）
yt-dlp -x --audio-format mp3 -o "edit/ref_%(id)s.%(ext)s" "视频URL"

# 或要整段视频做参考（自动选最佳画质，ffmpeg 负责合并/封装）
yt-dlp -f "bv*+ba/b" -o "edit/ref_%(id)s.%(ext)s" "视频URL"
```

```bash
# Whisper 转写出 SRT（语言 zh，模型 small，产物统一落 edit/transcripts/）
whisper "edit/ref_音频或视频文件" --model small --language zh --output_format srt --output_dir edit/transcripts/
```

转写是整套流水线的「读」底座（S6 中视频-use 用的是 ElevenLabs Scribe，这里换成本地 Whisper 同理）——**转写错了，后面所有剪辑判断跟着偏**。两条补充：

- Whisper 官方 CLI 默认给的是**句子级**时间戳；要拿 5.2 需要的**逐词**时间戳，得走 Python API 的 `word_timestamps=True`（推断，具体以你安装的版本 `whisper --help` / 官方文档为准）。
- 下载视频的版权按第 1 章口径处理：只拿你有权使用的素材，自动化不清除权利问题（S3）。

### 5.5 目录卫生：产物一律进独立输出目录

**规则：所有输出放素材目录旁的 `edit/`（或独立输出目录），源素材目录保持干净只读**（S6）。这既避免中间产物污染素材，也让 agent 的写权限能精确圈定在 `edit/` 内——呼应第 4 章「写权限只限指定输出目录」的护栏（S3/S6）。约定俗成的结构：

```text
my-project/
├── take01.mp4  take02.mp4   # 源素材：只读，不进脚本改
├── concat.txt               # 中间清单：可随时重生成
├── edit/                    # 所有产物：抽取段、归一化段、assembly、preview、字幕
│   ├── clip_a.mp4
│   ├── assembly.mp4
│   ├── out.srt
│   ├── preview.mp4
│   └── transcripts/
└── shots.csv                # 镜头清单（第 3 章产物）
```

因为源素材从不被改写，`edit/` 可以随时整目录清空重来——这就是幂等与可回滚在目录层面的落地。

### 本章小结

- 无损拼接三件套：`-c copy` 抽段、concat demuxer 组装、各片段编码参数一致是前提；参数不齐先统一中间格式（S6 + P1 LensB）。
- 每个剪切点 30ms audio fade 防爆音；剪切点贴合逐词时间戳、不切在词中间（S6）。
- 字幕三条：滤镜链最后、用输出时间轴、首版不烧录、TTS/字幕从单一锁定脚本生成（S6/S3）。
- 素材获取最小组合：yt-dlp 下载 + Whisper 转写出 SRT；转写质量是整个流程的底座（S6）。
- 目录卫生：源素材只读、所有产物进 `edit/`，呼应第 4 章的最小写权限护栏（S3/S6）。

### 下一章预览

命令写对了，下一个问题是「怎么证明剪对了」。第 6 章讲两层验证门：工程级与视频级 checklist、逐剪切点自检（跳帧/爆音/字幕遮挡），以及人进剪映/PR 精修前该验到什么程度。

### 本章素材索引

- S6 — video-use（腾讯云开发者）：hard rules 出处——字幕滤镜最后、30ms fade、不切词中间、字幕用输出时间轴、先分段抽取再无损 concat、产物进 `edit/`。https://cloud.tencent.com.cn/developer/article/2707362
- S3 — NemoVideo: Codex Automated Video Editing Workflow：首版不烧字幕、TTS/字幕从单一锁定脚本生成、权利审查留给人。https://www.nemovideo.com/blog/codex-automated-video-editing-workflow
- P1 LensB（非 S 源）— ffmpeg-cookbook 关于 concat demuxer + `-c copy` 无损拼接前提的说明（写作期未深读，仅转引前提）：https://ffmpeg-cookbook.com/en/articles/concat-protocol/
- ffmpeg / yt-dlp / Whisper 官方命令页在 P2 未深读；本章命令为常见标准用法，落地时以你安装版本的 `ffmpeg -h`、`yt-dlp --help`、`whisper --help` 及官方命令文档为权威依据（不贴官方深链）。
- 5.4「Whisper CLI 默认句子级时间戳、逐词需走 Python API `word_timestamps=True`」为推断项，未在 P2 源中核对。
