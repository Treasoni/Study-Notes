# AI 助手辅助视频剪辑 - 深度收集（P2）

> 项目：ai-assisted-video-editing · 阶段 2 · 收集时间：2026-09-04
> 主攻方向：**C 人机协作流水线**（A 能力边界 / B 工具链作为支撑）
> 用途：供 P3 outline-generator 生成大纲；引用以 [S#] 标注。

## Scope

回答一个核心问题：**想让 AI 助手（Codex CLI / Claude Code 等编码 agent）帮自己剪视频，正确的人机协作工作流长什么样？**
聚焦：agent 能/不能做什么 → 素材如何让 agent「读」→ 执行前如何预览/确认 → 执行如何做到安全可回滚 → 如何验证产物 → 人工在哪个环节收尾。工具链只收录支撑该工作流的必要命令级事实。

## Source Table

| ID | 来源 | 层级 | 日期 | 本地缓存 |
|----|------|------|------|----------|
| S1 | OpenAI Codex CLI 官方 README (github.com/openai/codex) | official | 持续更新 | p2_sources/04_github_com.md |
| S2 | Claude Code 官方 Security / Hooks (code.claude.com/docs/en/security) | official | 2026-09 检索 | p2_sources/05_code_claude_com.md |
| S3 | NemoVideo: Codex Automated Video Editing Workflow | implementation-report（厂商，偏营销） | 未知 | p2_sources/06_www_nemovideo_com.md |
| S4 | 什么值得买：Codex 剪视频创作者实测 | community（二手聚合） | 未知 | p2_sources/01_post_smzdm_com.md |
| S5 | Timeline Studio（阿里云开发者）：Agent Skill 构建可编辑可验证视频流水线 | implementation-report | 2026-08-07 | p2_sources/02_developer_aliyun_com.md |
| S6 | video-use（腾讯云开发者）：Agent 剪视频的关键是「读视频」 | implementation-report（二手解读） | 未知 | p2_sources/03_cloud_tencent_com_cn.md |

补充候选（P1 发现，未深读，仅作工具链线索）：ffmpeg-skill、video-editing-skill、claude-skill-auto-subtitles、JianYingDraft、ffmpeg-cookbook concat 文、yt-dlp SO 帖。

## Claim / Source Map（按主线组织）

### 1. AI 剪辑到底能做什么、不能做什么
- agent = 编排层/操作员，不是剪辑器：无 GUI、无「眼睛」，通过沙箱化 shell 驱动 ffmpeg/Whisper 等确定性工具 [S1][S3]
- **能稳定接管**：批量转码/裁剪/拼接、删停顿/口误/废话、切分拆条、字幕识别与烧录、响度/格式/比例统一、多平台导出、缩略图与代理生成 [S3][S4]
- **不能接管**：节奏（平均化、无「呼吸感」）、情绪与故事张力、逐帧精剪、判断 B-roll 是否该插、品牌准确性、权利审查 [S3][S4]
- **结构性盲区**：concat 音画同步漂移等「静态分析不可见」错误会让 agent 在错误方案内反复调参（实测漂移可累计到 14.86s）[P1 LensA / dev.to]
- 效率真相：模板化内容（口播/拆条/带货/知识讲解）提效显著（实测 11.2h 口播机器 10min、人工操作 40s；日产出 6→30 条）；创意内容则需人反复迭代（反例：改 6 版花 6 小时）[S4]

### 2. 核心反模式：让 agent「读」视频，不是「看」视频
- 丢几万帧给 LLM = token 噪音、难复盘；正确做法：先把视频变成 agent 擅长的材料——**文本 + 时间轴 + 结构化决策** [S6]
- 实现：ASR 逐词时间戳转写（停顿/口误/笑声/掌声变可读信号）→ 多素材压成单个 `takes_packed.md` → 需要判断画面时按需生成局部 timeline 合成视图（胶片帧+波形+词标签+静音间隔）而非全片抽帧 [S6]
- 专业版：多模态分析（ASR/OCR/镜头切换/光流/表情）后写入「源时间决策记录」= sourceRange + keep/cut + reason + confidence + protectedFrames + 叙事 role，使剪辑成为「基于证据的决策」而非固定规则 [S5]

### 3. 人机协作的标准流水线（多源收敛骨架）
```
素材(只读源 + 受控项目夹) → inventory(转写/盘点) → 提剪辑策略/镜头清单(提案，非真相)
→ 人审候选(缩略图/边界) → 生成 JSON/CSV 中间时间线或 EDL → 校验 → 渲染 preview
→ 逐切点自检 → 人工进剪映/PR 精修 → 锁 master → 平台变体导出
```
- 关键：agent 产出的是**提案/粗剪**，人保留方向、审美与最终批准 [S3][S5][S6]
- 镜头清单字段建议：beat_type / source_in-out / asset_id / voice_line / caption_id / review_status；拒一镜只换一个引用而非重建 [S3]
- 参考片拆「功能拍」（hook/context/proof/objection/transition/CTA）而非逐镜头抄 [S3]

### 4. 安全执行模型（让 agent 批量跑命令不翻车）
- 官方安全底线：默认只读 + 工作目录边界（只能写启动目录）+ 修改/联网类命令不默认放行 + 用户人工审查命令 [S1][S2]
- Claude Code 具体机制：Manual 只读默认、内置只读命令免问、沙箱化 bash、`/sandbox` 自治边界、Accept Edits 模式、allowlist 缓解提示疲劳、可疑 bash 即使 allowlist 仍人工批、fail-closed、permissions.deny 硬拦、ConfigChange hooks 审计 [S2]
- 媒体批量操作护栏（社区+工程共识）：**只读源素材、复制工作副本、固定 agent/ffmpeg/工具版本、写权限只限指定输出目录、密钥不落项目文件** [S3][S4]
- 事务式写入：projectRevision 拒旧计划 + 操作前置条件 + 一个意图一个事务（关键失败整组停）+ operationId 幂等 + 结构化错误 [S5]
- 代码/命令级预览：project.inspect 读结构 → project.diff 非写入校验（提前发现 ID 不存在/时间范围无效/轨道不兼容/素材缺失）→ project.run 执行 [S5]

### 5. 可复用的 hard rules（工具层落地要点）
- 字幕滤镜放**滤镜链最后**，防被其它处理遮挡 [S6]
- 每个剪切点 **30ms audio fade**，防爆音 [S6]
- **不能切在词中间**，贴合逐词时间戳下刀 [S6]
- 字幕时间用**输出时间轴**而非原始素材时间轴 [S6]
- 多段素材先**分段抽取再无损 concat**（-c copy + concat demuxer），避免反复编码；拼接前提：各片段编码参数一致 [S6][P1 LensB]
- 首版**不烧录字幕**，保持可编辑数据（TTS/字幕从单一锁定脚本生成以保关联）[S3]
- 产物隔离到 `edit/` 或独立输出目录，保持 skill 目录干净 [S6]
- 输出「成片 + 可编辑工程」双交付（`.timeline` 工程包 / edit 目录 + preview.mp4），预览与导出用同一合成规则 [S5][S6]

### 6. 验证门（什么才算「完成」）
- 工程验证：轨道数/主画面连续/顺序与时长/字幕绑定语音/媒体归档/可重开/首帧显示 [S5]
- 视频验证：容器编码/尺寸时长/完整解码/音频轨/转场停顿重复帧/声道错位静音 [S5]
- 逐剪切点自检：跳帧/爆音/字幕遮挡 [S6]
- 剪映草稿适配属版本敏感：先备份、一次性草稿测试；NemoVideo 明示无法验证稳定公开 schema [S3]

### 7. 角色与分工（笔记的价值观主线）
- agent 把「不可读的视频堆」变成「可检查的剪辑工程」；人做最终判断、审美、平台发布 [S5][S6]
- 剪辑者从「鼠标搬运工」变「指令架构师」：盯逻辑写剧本而非盯屏拉片 [S4]
- 判断标准一条：模板化内容用 agent；创意表达留自己 [S4]

## Contradictions / Tensions

1. **剪映互操作分歧**：S3 保守（无稳定 schema、要备份测试）；S4 生态大量素材把「Codex+ChatCut 直接操剪映自动成片」当现实。
2. **效率叙事**：峰值「10 分钟干一个月/几百倍」vs 反例「6 小时改 6 版」——都真，取决于内容类型 + 是否接受精调；二手聚合数字带营销水分需降权。
3. **无人值守 vs 人审**：S6 明说保留「先策略后执行」的确认点使其不适于完全无人批量；但 S4 中有相当比例用户想要一键自动。取舍应写入笔记。
4. **「看」与「读」**：S5 用多模态分析（含视觉），S6 强调「读文本、按需看局部」——非冲突，是视觉成本分层，可统一表述为「全片文本化 + 关键帧按需视觉化」。

## Open Questions / Gaps

- OpenAI Codex CLI 官方安全/审批文档入口迁移中（developers.openai.com → learn.chatgpt.com 指向的是 Codex Security 应用安全产品），CLI 沙箱/approval_policy 细节未能从官方文档确认；落地时以安装版本 `codex --help` 与配置文档为准。[S1 缺口]
- 剪映/CapCut 官方自动化边界未经官方确认；JianYingDraft 等社区库的版本墙（模板≤5.9、导出≤6）需实操验证。
- 成本数据缺量化：token/时长成本、渲染耗时缺系统测量（仅 S4 定性）。
- ffmpeg.org / yt-dlp 官方命令页未深读；如最终笔记需要「命令权威引用」，P3 后在写作阶段补 1-2 篇官方页。

## 下游交接（给 outline-generator / chapter-writer）

**建议章节骨架种子**（方法/工作流笔记，按 C 主线 + A/B 支撑）：
1. 预期管理：AI 剪辑能/不能做什么（A + S4 效率真相 + 结构性盲区）
2. 素材工程化：让 agent「读」视频（转写/盘点/takes_packed/按需视觉，S6/S5）
3. 流水线设计：从需求到成片的阶段与角色分工（S3/S5 骨架 + 功能拍 + 中间时间线/EDL）
4. 安全执行：权限、沙箱、只读源、事务式命令（S1/S2/S5）
5. 工具链速查：FFmpeg 无损剪切/拼接 + Whisper 字幕 + yt-dlp（hard rules，S6/P1 LensB）
6. 验证与精修：工程/视频双验证 + 人进剪映/PR 收尾（S5/S6/S3）
7. 反模式与实战问答：6 小时 6 版、音画漂移、剪映互操作、成本账（S4/S3）

**术语表种子**：stream copy / concat demuxer / EDL / shot manifest / 源时间决策记录 / inventory / takes_packed / .timeline / operationId / allow-ask-deny / 无损拼接。

**素材引用约定**：正文引用用 [S1]–[S6]，本地深读缓存位于 `workspace/ai-assisted-video-editing/p2_sources/`（不进最终 Obsidian 笔记）。
