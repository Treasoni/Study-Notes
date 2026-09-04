---
url: "https://developer.aliyun.com/article/1754064"
title: "如何用 Agent Skill 构建一套可编辑、可验证的 AI 视频生产流水线-阿里云开发者社区"
scraped_at: 2026-09-04T11:41:00+00:00
---

# 如何用 Agent Skill 构建一套可编辑、可验证的 AI 视频生产流水线
2026-08-07 245
版权声明：
本文内容由阿里云实名注册用户自发贡献，版权归原作者所有，阿里云开发者社区不拥有其著作权，亦不承担相应法律责任。具体规则请查看《 [阿里云开发者社区用户服务协议](https://developer.aliyun.com/article/768092)》和 《[阿里云开发者社区知识产权保护指引](https://developer.aliyun.com/article/768093)》。如果您发现本社区中有涉嫌抄袭的内容，填写 [侵权投诉表单](https://yida.alibaba-inc.com/o/right)进行举报，一经查实，本社区将立刻删除涉嫌侵权内容。 
**简介：** Timeline Studio 是开源AI视频编辑系统，支持从自然语言需求出发，自动完成素材分析、剪辑决策、时间线修改、浏览器端本地AI推理（Whisper/VITS等）及成片+可编辑`.timeline`工程双重交付，实现专业级自动化视频生产。
> 从一句自然语言需求出发，完成素材分析、剪辑规划、时间线修改、浏览器本地 AI 推理、成片验证，并同时交付视频与可编辑工程。
## 开源项目
### 效果与案例仓库
[Timeline Studio Skills Handbook](https://github.com/MartinDelophy/timeline-studio-handbook)
Handbook 提供参考视频复刻、产品宣传片、多语言本地化、知识科普等案例，并尽量保留提示词、结果视频和可编辑 `.timeline` 工程，适合查看效果、理解剪辑决策和复用工作流。
### Timeline Studio 主仓库
[MartinDelophy/ai-video-editor](https://github.com/MartinDelophy/ai-video-editor)
主仓库包含浏览器视频编辑器、Agent Skill、时间线命令协议、本地 AI 模型集成，以及构建和部署配置。
安装 Skill：

```
npx skills add MartinDelophy/ai-video-editor --skill edit-timeline-studio

```

ScreenShot_2026-08-07_154510_331.png
## 背景：为什么视频生产需要 Agent Skill
生成文案、配音、字幕或者图片，已经不是困难的问题。真正困难的是如何把这些能力组织成一条稳定的视频生产流水线。
一条看似简单的短视频，通常需要完成：
  1. 检查原始素材；
  2. 理解画面、语音和内容结构；
  3. 决定镜头的保留、删除和排序；
  4. 生成或整理旁白；
  5. 建立字幕与语音的时间关系；
  6. 添加音乐、画中画、动画和效果；
  7. 检查时间线连续性；
  8. 导出成片；
  9. 保存可继续编辑的项目。


如果这些步骤分散在多个 AI 服务和剪辑工具中，用户仍然需要承担大量文件传递、格式转换和时间同步工作。
Timeline Studio 的思路，是通过 `edit-timeline-studio` Skill 将专业剪辑流程转换为 Agent 可以执行的工程协议。
Skill 不只是提示词模板。它同时定义：
  * Agent 应该先检查什么；
  * 如何对素材进行分类；
  * 如何生成剪辑决策；
  * 哪些操作可以自动执行；
  * 哪些操作需要浏览器编辑器；
  * 如何验证最终结果；
  * 什么情况下不能宣称任务已经完成。


## 整体架构
系统可以分为五层。

```
flowchart TD
    A["自然语言创作需求"] --> B["Skill 工作流层"]
    B --> C["素材分析与剪辑决策"]
    C --> D["声明式时间线命令层"]
    C --> E["浏览器 AI 与编辑器能力层"]
    D --> F["可移植 .timeline 工程"]
    E --> F
    F --> G["预览、解码与视听验证"]
    G --> H["成片视频 + 可编辑工程"]

```

### 第一层：自然语言需求
用户不需要描述具体按钮操作，只需要说明创作目标，例如：
> 把这些产品演示素材剪成一条40秒左右的竖屏宣传片，保留真实操作过程，添加中文旁白和字幕，突出三个典型使用场景。
Skill 会保留原始需求，并将其转换为结构化创作约束：

```

  "contentType": "product-promotion",
  "targetDuration": 
    "min": 35,
    "max": 45
  },
  "aspectRatio": "9:16",
  "captions": true,
  "voiceoverLanguage": "zh-CN",
  "preserveSourceDialogue": true,
  "deliverables": [
    "video",
    "editable-timeline"
  ]
}

```

其中，一部分字段来自用户明确要求，一部分来自素材分析，还有一部分属于可追踪的默认决策。
### 第二层：Skill 工作流
Skill 根据内容类型选择不同执行路径。
例如：
  * 口播整理侧重语义完整性和语音连续性；
  * 产品宣传侧重问题、产品动作、证据和 CTA；
  * 多镜头集锦侧重动作、节奏和高潮层级；
  * 多说话人内容侧重人物身份和对话轮次；
  * 网站演示侧重页面流程和操作证据；
  * 参考视频复刻侧重镜头结构、速度曲线和主体运动。


这种分类非常重要。
如果所有视频都使用同一套“检测静音并删除”的算法，系统很容易删除刻意保留的停顿、产品结果展示或者人物表情。
Agent Skill 的价值，是让自动化过程具备任务语境。
## 素材分析：建立剪辑证据
在修改时间线前，系统首先检查素材。
基础检查包括：
  * 文件类型；
  * 视频时长；
  * 分辨率和宽高比；
  * 帧率；
  * 是否包含音频；
  * 音频采样率和声道；
  * 素材是否能够正常解码。


根据任务需要，还可以继续分析：
  * 视频代表帧；
  * 语音识别结果；
  * OCR 文字；
  * 镜头切换；
  * 主体位置和尺寸；
  * 画面清晰度；
  * 全局运动；
  * 主体区域光流；
  * 音频能量变化；
  * 人物表情变化。


分析结果不会直接变成剪辑操作，而是先形成源时间决策记录。

```

  "assetId": "demo-recording",
  "sourceRange": 
    "start": 42.8,
    "end": 50.3
  },
  "decision": "keep",
  "role": "primary-peak",
  "reason": "完整展示任务执行后的可见结果",
  "confidence": 0.94,
  "protectedFrames": [
    47.2,
    48.1
  ]
}

```

每一段素材都可以记录：
  * 保留、删除、缩短或重排；
  * 决策原因；
  * 置信度；
  * 是否需要保护原声；
  * 是否包含关键画面；
  * 在叙事中的作用。


这让自动剪辑从“应用固定规则”变成“基于证据做编辑决策”。
## 声音、运动和镜头变化如何参与高光判断
对于集锦、动作和宣传内容，系统可以综合多类局部证据寻找候选高光时刻。
一种可解释的评分方式是：

```
候选分数 =
30% × 音频能量变化
+ 25% × 主体区域运动
+ 20% × 镜头变化置信度
+ 15% × 同一人物表情变化
+ 10% × 主体区域清晰度

```

这里的分数只负责提出候选时刻，不能直接决定最终剪辑。
例如，内容连续性可能要求保留高光动作之前的准备过程；一段没有运动的产品结果画面，也可能比快速移动镜头更重要。
因此，高光判断和叙事判断必须分开。
分析完成后，还需要给保留片段分配叙事角色：
  * `setup`：建立背景；
  * `rise`：提升张力；
  * `pre-impact`：为高潮做准备；
  * `primary-peak`：主要高潮；
  * `secondary-peak`：次要高潮；
  * `aftershock`：展示结果；
  * `bridge`：连接上下文。


最终时间线应形成非平坦的张力曲线，而不是让每个镜头拥有相同权重。
## 声明式时间线命令
Timeline Studio 将可自动化的编辑操作封装为版本化命令。
基本流程如下：

```
npm run agent -- project.inspect /projects/demo.timeline
npm run agent -- project.diff /projects/edit-plan.json
npm run agent -- project.run /projects/edit-plan.json

```

### `project.inspect`
读取现有工程结构，包括：
  * 工程版本；
  * 画布比例；
  * 轨道；
  * 素材；
  * 时间线片段；
  * 字幕；
  * 语音关系；
  * 已归档的媒体文件。


### `project.diff`
验证命令是否受支持，并计算非写入式差异。
它可以在执行前发现：
  * 片段 ID 不存在；
  * 时间范围无效；
  * 轨道类型不兼容；
  * 工程版本不匹配；
  * 操作依赖的素材缺失；
  * 当前渲染器无法处理某项属性。


### `project.run`
在前置条件成立时，事务性执行编辑计划，并输出新的 `.timeline` 工程。
一个命令计划可以包含：

```

  "version": 1,
  "projectRevision": 6,
  "operationId": "product-promo-cut-v3",
  "operations": [
    
      "type": "visual.trim",
      "clipId": "visual-demo",
      "sourceStart": 12.4,
      "sourceEnd": 18.7
    },
    
      "type": "timed.move",
      "clipId": "voice-result",
      "start": 24.2
    },
    
      "type": "caption.update",
      "clipId": "caption-result",
      "text": "从素材到成片，只需要描述目标。",
      "start": 24.2,
      "end": 28.6
    }
  ]
}

```

## 为什么需要版本、事务和幂等性
视频编辑自动化和普通脚本不同。
一次剪辑计划可能同时修改画面、字幕、配音和音乐。如果只成功了一部分，工程就会进入不一致状态。
因此命令层需要具备数据库式的安全特征。
### 工程版本检查
计划基于某个具体工程版本生成。执行时如果发现工程已经变化，系统会拒绝应用旧计划。
### 前置条件
操作可以要求片段仍然位于某个轨道、具有某个时间范围，或者仍然绑定指定音频。
### 事务
一个用户可见意图对应一个事务。任何关键操作失败，整组修改停止。
### 幂等键
每个计划携带稳定的 `operationId`。重复执行相同计划时，不会重复插入素材或字幕。
### 结构化错误
失败信息需要明确指出缺少哪个素材、哪个命令不受支持，以及工程的哪项状态不符合预期。
这些机制是从“演示型 Agent”走向“生产型 Agent”的基础。
## 双路径执行：命令协议与浏览器编辑器
当前系统同时使用两条执行路径。  
| 执行路径  | 适合的任务  |  
| --- | --- |  
| 命令协议  | 工程检查、媒体导入、片段调整、字幕更新、轨道操作和受支持的本地渲染  |  
| 浏览器编辑器  | AI 配音、自动字幕、复杂效果、数字人、完整预览和丰富合成  |  
命令路径具备较强的确定性，适合批处理和自动化。
浏览器路径可以使用 Timeline Studio 已经存在的完整产品能力，但会受到界面状态、文件选择器和浏览器媒体行为影响，因此不能被描述为完全稳定的无头 API。
Skill 的策略是：
  1. 优先检查命令注册表；
  2. 已支持的操作通过命令执行；
  3. 缺少的部分通过编辑器完成；
  4. 执行后重新检查工程；
  5. 解码并验证最终视频。


随着更多操作进入共享命令层，浏览器自动化承担的工作会逐步减少。
##  `.timeline` 可移植工程
Timeline Studio 不把 MP4 当作唯一结果。
`.timeline` 是一个可移植工程包，其中包含：

```
project.timeline
├── project.json
└── media/
    ├── visual-001.mp4
    ├── visual-002.png
    ├── voice-001.wav
    └── music-001.wav

```

`project.json` 记录时间线结构，`media` 保存工程依赖的素材。
相对于只输出成片，这种设计具有几个优势：
  * 用户可以继续手工编辑；
  * Agent 可以读取和修改已有项目；
  * 工程可以在不同设备间迁移；
  * 修改字幕不需要重新生成全部内容；
  * 可以追踪素材与源时间的对应关系；
  * 成片结果能够被工程结构证明。


可编辑工程也是 Agent 和人类剪辑师之间的协作协议。
Agent 可以完成初剪和技术性工作，人类则可以继续调整表达、审美和最终发布策略。
## 字幕与语音的单向约束
自动视频系统经常出现“字幕存在，但没有对应声音”的问题。
Timeline Studio Skills 使用一条明确约束：
> 工程一旦启用字幕，每段可见字幕都必须在完整显示区间内对应一段可听见的语音。
如果字幕来自原视频人物说话，则字幕绑定原始语音。
如果字幕由 Agent 编写，则需要先生成旁白，再将字幕绑定到对应的语音片段。

```

  "captionId": "caption-12",
  "audioClipId": "voice-12",
  "start": 18.2,
  "end": 22.7,
  "text": "重复工作交给 AI，创作者负责真正的表达。"
}

```

按句拆分语音还有一个重要作用：后续调整某句话时，不需要在一段很长的旁白音频中重新定位。
交付前需要检查：
  * 字幕是否存在对应音频；
  * 音频是否真实可听；
  * 字幕是否超出语音区间；
  * 是否重复叠加原声和 AI 旁白；
  * 不同语句的响度是否一致；
  * 左右声道是否出现异常延迟。


## 浏览器本地 AI 推理
Timeline Studio 将多项 AI 能力放在浏览器侧运行，技术栈主要包括：
  * WebGPU；
  * ONNX Runtime Web；
  * Web Worker；
  * Cache Storage；
  * IndexedDB；
  * WebCodecs。


当前能力覆盖自动字幕、多语言配音、本地音乐、主体检测、人像处理、视频修复、人声分离和数字人等方向。
部分模型包括：
  * Whisper Small Q8 ONNX；
  * Piper/VITS 中文语音模型；
  * Kokoro 英文语音模型；
  * Stable Audio 3 Small Q4 ONNX；
  * YOLOS Tiny；
  * MODNet；
  * MI-GAN；
  * NanoVSR；
  * JoyVASA；
  * LivePortrait。


模型采用按需加载方式。用户第一次使用某项能力时下载模型，后续通过浏览器缓存复用。
模型文件可以从 Hugging Face 和 ModelScope 的自有镜像加载，并使用固定版本。两家提供方共享逻辑缓存身份，避免相同模型被重复保存。
对于国内用户，系统可以优先尝试 ModelScope；网络条件变化或者下载失败后，再切换其他镜像。
## 浏览器导出
编辑器使用原生媒体路径进行播放预览，导出时则使用独立的离线合成路径。
WebCodecs 路径负责：
  * 逐帧合成主画面；
  * 应用变换、字幕和 Overlay；
  * 混合配音、音乐和原声；
  * 编码视频；
  * 生成 MP4 或 WebM。


对于不支持完整 WebCodecs 能力的环境，可以使用 MediaRecorder 兼容路径。
预览和导出必须尽量使用相同的时间、属性和合成规则，否则会出现“预览正确、导出错误”的问题。
## 完成标准：成片和工程缺一不可
对于完整的视频编辑任务，Timeline Studio Skills 要求输出：

```
output/
├── result.mp4
└── result.timeline

```

交付前还要执行验证。
### 工程验证
  * 轨道数量是否正确；
  * 主画面是否连续；
  * 片段顺序和时长是否符合计划；
  * 字幕是否绑定正确语音；
  * 媒体文件是否已经归档；
  * 工程是否可以重新打开；
  * 第一帧是否能够在预览中显示。


### 视频验证
  * 容器和编码是否正确；
  * 视频尺寸是否符合要求；
  * 时长是否正确；
  * 视频是否能够完整解码；
  * 音频轨道是否存在；
  * 字幕、Overlay 和效果是否可见；
  * 转场边界是否出现停顿或重复帧；
  * 是否存在声道错位和异常静音。


只有成片和工程均通过检查，任务才被认为完成。
## 这套架构解决了哪些自媒体生产问题  
| 问题  | 技术方案  |  
| --- | --- |  
| 素材太多，不知道如何筛选  | 多模态分析与源时间决策记录  |  
| 自动剪辑缺少内容理解  | 按内容类型选择专业工作流  |  
| AI 修改不可预测  |  `project.diff` 语义预览  |  
| 重复执行导致素材重复  | 幂等操作 ID  |  
| 工程修改一半失败  | 事务和前置条件  |  
| 字幕与声音错位  | 字幕—语音绑定约束  |  
| AI 结果无法修改  | 可移植 `.timeline` 工程  |  
| 工具之间反复导入导出  | 统一多轨时间线  |  
| 素材隐私和远程成本  | 浏览器本地模型推理  |  
| 不知道结果是否真正可用  | 工程检查、解码和视听验证  |  
| 多语言制作成本高  | 复用画面结构并替换配音与字幕  |  
| 无法批量生产  | 版本化声明式命令计划  |  
## 当前边界与后续方向
目前，命令层已经覆盖工程检查、媒体导入、时间调整、字幕、部分属性和可移植渲染子集。
更复杂的字幕渲染、贴纸、Overlay、转场、效果、AI 生成和完整合成，仍可能需要浏览器编辑器参与。
后续可以继续推进：
  * 扩大 `project.render` 的合成覆盖范围；
  * 为 ASR、TTS、视觉分析和导出增加进度事件；
  * 增加真正可取消的长任务；
  * 持久化工程级撤销检查点；
  * 暴露结构化视觉和语音分析记录；
  * 在命令注册表上增加 MCP 传输适配层；
  * 提高命令渲染与浏览器渲染的一致性。


系统当前采用“稳定命令层＋浏览器兼容层”的渐进式架构，而不是将尚未完成的能力描述成全自动无头服务。
## 总结
Timeline Studio Skills 的核心并不是让 Agent 学会操作视频编辑器界面，而是建立一套能够理解素材、描述决策、修改工程和验证结果的视频生产协议。
这套协议包含：
  * 面向不同内容类型的剪辑工作流；
  * 多模态素材分析；
  * 可解释的源时间决策；
  * 声明式时间线命令；
  * 版本、事务和幂等机制；
  * 浏览器本地 AI 推理；
  * 可移植 `.timeline` 工程；
  * 成片与工程双重验证。


对于自媒体创作者，它减少的是剪辑、字幕、配音、检查和多版本制作中的重复劳动。
对于开发者，它提供了一个值得探索的方向：Agent 不一定只能调用生成模型，也可以成为一套专业生产软件的工作流执行者。
最终，AI 负责把创作意图可靠地变成工程；人类继续负责事实、观点、审美和表达。
查看效果和可复现案例：
[Timeline Studio Skills Handbook](https://github.com/MartinDelophy/timeline-studio-handbook)
安装、运行、部署或参与开发：
[Timeline Studio 主仓库](https://github.com/MartinDelophy/ai-video-editor)
热门文章
最新文章
一站式为企业和开发者提供大模型能力体系，大模型原生应用以及最佳解决方案，助力云上开发者轻松完成 AI 落地。
#### [千问AI平台 千问官方 MaaS 平台，为开发者和 Agent 而生，新用户赠送 1 亿 + tokens 额度](https://www.qianwenai.com/)
#### [AI 体验馆 免费体验前沿云上 AI 应用，开启智能创新](https://www.aliyun.com/exp/)
#### 大模型
#####  文本生成
###### [ Qwen3.8-Max _HOT_ 0902 快照版本重磅更新，智能体时代全能旗舰模型](https://platform.qianwenai.com/try-ai?models=qwen3.8-max-0902)###### [ Qwen3.8-Flash _NEW_ 百万级上下文窗口，一次性处理超长文档和代码仓库](https://platform.qianwenai.com/try-ai?models=qwen3.8-flash)###### [ Qwen3-VL-Plus 视觉 Coding、空间感知、多模态思考等全面升级](https://platform.qianwenai.com/try-ai?models=qwen3-vl-plus)
###### [ Kimi-K3 Kimi 最新旗舰模型，长程编程与推理利器](https://www.qianwenai.com/models/kimi%2Fkimi-k3)###### [ Deepseek-v4-pro 旗舰 MoE 大模型，百万上下文与顶尖推理能力](https://platform.qianwenai.com/try-ai?models=deepseek-v4-pro)###### [ GLM-5.2 1M上下文，专为长程任务能力而生](https://platform.qianwenai.com/try-ai?models=glm-5.2)
#####  图片和视频生成
###### [ Wan3.0-Video 四模态全能参考，多种创作一站支持](https://platform.qianwenai.com/try-ai?scene=video&models=wan3.0-video)###### [ Qwen-Image-3.0-Pro _NEW_ 细节真实，知识厚实，让图像生成真正成为可落地的生产力工具](https://platform.qianwenai.com/try-ai/chat?models=qwen-image-3.0-pro)###### [ HappyHorse-1.1-T2V 让文字生成流畅细腻的高质量视频](https://platform.qianwenai.com/try-ai?models=happyhorse-1.1-t2v)
#####  语音识别与合成
###### [ Qwen3-TTS-Flash  离线语音合成大模型，多语言方言自适应，低延迟高稳定](https://platform.qianwenai.com/try-ai?scene=tts&models=qwen3-tts-flash)###### [ Cosyvoice-V3-Flash 高表现力语音合成大模型，语音克隆听感自然](https://platform.qianwenai.com/try-ai?scene=tts&models=cosyvoice-v3-flash)###### [ Fun-ASR 支持中英文自由切换，具备更强的噪声鲁棒性](https://platform.qianwenai.com/try-ai?models=fun-asr)
##### [千问AI平台-Token Plan _NEW_ 个人版上线、团队版降价；千问3.8-Max首发发尝鲜](https://www.qianwenai.com/benefits/tokenplan)##### [千问AI平台-模型体验 在线体验全尺寸、多种模态的模型效果](https://platform.qianwenai.com/try-ai)##### [Happy 系列大模型 新一代 AI 视频生成模型，深度适配广告营销等场景](https://www.aliyun.com/product/happymodel)
##### [大模型服务平台百炼-应用模版 丰富多元化的应用模版和解决方案](https://bailian.console.aliyun.com/?tab=app#/app-market/newTemplate)##### [大模型服务平台百炼-智能体 灵活可视化地构建企业级 Agent](https://bailian.console.aliyun.com/?tab=app#/app-center)##### [人工智能平台 PAI AI Native 的算法工程平台，一站式完成建模、训练、推理服务部署](https://www.aliyun.com/product/bigdata/learn)
#### 大模型原生应用
##### [Qoder _HOT_ 面向真实软件的智能体编程平台](https://www.qianwenai.com/agents/qoder)##### [万镜一刻 AIGC视频创作平台，创意直达成片](https://www.qianwenai.com/agents/wonderclip)##### [伶鹊 智能客服平台，对话机器人、对话分析、智能外呼](https://www.qianwenai.com/agents/voicepica)
##### [千问办公 _NEW_ 一站式AI生产力平台](https://www.qianwenai.com/agents/qwenwork)##### [万有无界 企业级人与Agent协作平台，接入和调度多个数字员工](https://www.qianwenai.com/agents/wanyou)##### [秒悟 云端极速 AI 应用创作平台](https://www.qianwenai.com/agents/meoo)
#### 大模型解决方案
##### [快速部署 Dify，高效搭建 AI 应用 依托云原生高可用架构,实现Dify私有化部署](https://www.aliyun.com/solution/tech-solution/rapidly-deploy-dify-to-accelerate-ai-application-development)##### [10 分钟在聊天系统中增加一个 AI 助手 在企业官网、通讯软件中为客户提供 AI 客服](https://www.aliyun.com/solution/tech-solution/build-a-chatbot-for-your-website-or-chat-system)
##### [10分钟微调：让0.6B模型媲美235B模型 用1%尺寸在特定领域达到大模型90%以上效果](https://www.aliyun.com/solution/tech-solution/qwen3-distill)##### [即刻拥有 DeepSeek-R1 满血版 多种方案随心选，轻松解锁专属 DeepSeek](https://www.aliyun.com/solution/tech-solution/deepseek-r1-for-platforms)
##### [多模态数据信息提取 从文本、图片、视频中提取结构化的属性信息](https://www.aliyun.com/solution/tech-solution/information-extraction)##### [超强辅助，Bolt.diy 一步搞定创意建站 通过自然语言交互简化开发流程,全栈开发支持](https://www.aliyun.com/solution/tech-solution/bolt-diy)
##### [与 AI 智能体进行实时音视频通话 构建支持视频理解的 AI 音视频实时通话应用](https://www.aliyun.com/solution/tech-solution/real-time-interaction)##### [构建大模型应用的安全防护体系 通过阿里云安全产品对 AI 应用进行安全防护](https://www.aliyun.com/solution/tech-solution/build-large-model-application-security-system)
精选产品[人工智能与机器学习](https://ai.aliyun.com/)[计算](https://www.aliyun.com/product/list/ecs)[容器](https://www.aliyun.com/product/aliware/containerservice)[存储](https://www.aliyun.com/storage/storage?spm=5176.19720258.J_2686872250.30.3f0e4ff6AwBQKs)[网络与CDN](https://www.aliyun.com/product/network/network)[安全](https://www.aliyun.com/product/list/security%20)[中间件](https://www.aliyun.com/product/list/aliware)[数据库](https://www.aliyun.com/product/outline/index?spm=5176.19720258.J_2686872250.45.3f0e4ff6AwBQKs)[大数据计算](https://www.aliyun.com/product/bigdata/apsarabigdata)媒体服务[企业服务与云通信](https://www.aliyun.com/product/list/ent-cmc)域名与网站终端用户计算Serverless[开发工具](https://www.aliyun.com/product/list/developertools)[迁移与运维管理](https://www.aliyun.com/product/list/operation-mainenance)[专有云](https://apsara-stack.aliyun.com)
#### 精选产品
##### [大模型服务平台百炼 _大模型_ 大模型服务与应用平台](https://www.aliyun.com/product/bailian)##### [轻量应用服务器 快速构建应用程序和网站，即刻迈出上云第一步](https://www.aliyun.com/product/swas)##### [云数据库 RDS 全托管，含MySQL、PostgreSQL、SQL Server、MariaDB多引擎](https://www.aliyun.com/product/rds)##### [人工智能平台 PAI _大模型_ 一站式AI开发、训练和推理服务](https://www.aliyun.com/product/bigdata/learn)##### [云解析DNS 覆盖公网/内网、递归/权威、移动APP等全场景解析服务](https://www.aliyun.com/product/dns)##### [云原生数据库 PolarDB 100%兼容MySQL、PostgreSQL，兼容Oracle，支持集中和分布式](https://www.aliyun.com/product/polardb)##### [GPU 云服务器 基于神龙架构的弹性GPU算力服务](https://www.aliyun.com/product/egs)
##### [域名与网站 提供智能易用的域名与建站服务](https://wanwang.aliyun.com/)##### [千问大模型 _大模型_ 多元化、高性能、安全可靠的大模型服务](https://www.aliyun.com/product/tongyi)##### [数字证书管理服务（原SSL证书） 实现全站HTTPS与全场景一键证书托管](https://www.aliyun.com/product/cas)##### [短信服务 国内短信简单易用，安全可靠，秒级触达，全球覆盖200+国家和地区。](https://www.aliyun.com/product/sms)##### [Qoder CN 基于千问大模型等，支持代码智能生成、研发智能问答](https://www.aliyun.com/product/lingma)##### [大数据开发治理平台 DataWorks Data Agent 驱动的一站式 Data+AI 开发治理平台](https://www.aliyun.com/product/dide)
##### [云服务器 ECS 安全可靠、弹性可伸缩的云计算服务](https://www.aliyun.com/product/ecs)##### [对象存储 OSS 稳定、安全、高性价比、高性能的云存储服务](https://www.aliyun.com/product/oss)##### [无影云电脑 随时随地安全接入的云上超级电脑](https://www.aliyun.com/product/ecs/gws)##### [Qoder 面向真实软件的智能体编程平台](https://www.aliyun.com/product/qoder)##### [云原生大数据计算服务 MaxCompute 面向分析的企业级SaaS模式云数据仓库](https://www.aliyun.com/product/maxcompute)##### [容器服务 Kubernetes 版 ACK 提供一站式管理容器应用的 K8s 服务](https://www.aliyun.com/product/kubernetes)
[检索分析服务 Elasticsearch 版在阿联酋（迪拜）开服](https://www.aliyun.com/product/news/30567)[阿里云百炼 Qwen3-VL-Rerank 模型价格调整](https://www.aliyun.com/product/news/30572)[EMR Serverless Spark 推出 Daft 算子市场](https://www.aliyun.com/product/news/30576)[云防火墙 NAT 防火墙支持主备模式](https://www.aliyun.com/product/news/30489)[网盘与相册服务阿里云盘企业版支持 API Key 授权](https://www.aliyun.com/product/news/30569)[AgentCore 支持纳管用户本地 Agent](https://www.aliyun.com/product/news/30304)[视频生成模型 Wan3.0 正式上线](https://www.aliyun.com/product/news/30378)
精选解决方案[AI](https://www.aliyun.com/solution/tech-solution/ai)互联网应用开发大数据现代化应用安全网络可观测上云与迁云[企业出海](https://www.aliyun.com/goglobal)政企业务
#### 精选解决方案
##### [ DeepSeek Harness：构建插件化智能体 _NEW_ 快速部署 DeepSeek Harness 开源智能体](https://www.aliyun.com/solution/tech-solution/deepseek-harness)##### [Qwen Audio：打造专属 AI 语音助手 Qwen-Audio-3.0-Realtime 端到端实时语音角色扮演](https://www.aliyun.com/solution/tech-solution/qwen-audio)##### [ 一键部署幻兽帕鲁游戏服务器 _HOT_ 一键购买专属联机服务器，轻松开启游戏](https://www.aliyun.com/solution/tech-solution/palworld)##### [漫剧工坊：一站式动画创作平台 快速生产连贯的高质量长漫剧](https://www.aliyun.com/solution/tech-solution/use-bailian-to-intelligently-create-comics)
##### [ MiniMax-H3：一键部署，即刻创作 _NEW_ 通过计算巢快速部署 MiniMax H3 全模态视频创作环境。](https://www.aliyun.com/solution/tech-solution/minimax-h3-deploy-in-one-click-create-instantly)##### [一句话生成原生可编辑精美 PPT 文稿 输入一句话想法, 轻松生成专业的 PPT](https://www.aliyun.com/solution/tech-solution/vibe-ppt)##### [HappyHorse 打造一站式影视创作平台 可视化编排打通从文字构思到成片全链路闭环](https://www.aliyun.com/solution/tech-solution/infinite-canvas)##### [快速拥有专属 OpenClaw 让AI从“聊天伙伴”进化为能干活的“数字员工”](https://www.aliyun.com/solution/tech-solution/clawdbot)
##### [千问办公，解锁你的工作新方式 企业级Agent产品，直接交付可用成果](https://www.aliyun.com/solution/tech-solution/qwenwork)##### [GLM-5.2：长任务时代开源旗舰模型 真正可用的 1M 上下文,一次完成代码全链路开发](https://www.aliyun.com/solution/tech-solution/glm-for-platforms)##### [Hermes Agent，打造自进化智能体 自主进化，持久记忆，越用越聪明](https://www.aliyun.com/solution/tech-solution/hermes-agent)##### [低代码高效构建企业门户网站 以可视化方式快速构建移动和 PC 门户网站](https://www.aliyun.com/solution/tech-solution/build-a-website)
##### [睿译宝，AI翻译排版一步到位 上传文档即自动完成翻译和格式还原](https://www.aliyun.com/solution/tech-solution/rui-yi-bao)##### [即刻拥有 DeepSeek-V4-Pro 轻松解锁专属 DeepSeek-V4-Pro ](https://www.aliyun.com/solution/tech-solution/deepseek-v4-for-platforms)##### [ 5 分钟轻松部署专属 QwenPaw _HOT_ 从聊天伙伴进化为能主动干活的本地数字员工](https://www.aliyun.com/solution/tech-solution/copaw)##### [10 分钟搭建微信、支付宝小程序 高效部署网站，快速应用到小程序](https://www.aliyun.com/solution/tech-solution/develop-your-wechat-mini-program-in-10-minutes)
上云优选，普惠好价，为开发者和企业提供多款超值优选上云必备产品；超 140 款免费试用产品；初创企业最高可得 100 万抵扣金。
#### 普惠上云
##### [普惠上云 官方力荐 云服务器38元/年起，超值低价云产品抢先购](https://www.aliyun.com/benefit/select/cloud-discount)##### [官方推荐返现计划 推荐新用户得奖励，单订单最高返9万](https://dashi.aliyun.com/)##### [云工开物 高校专属算力普惠，学生认证享300元代金券](https://university.aliyun.com/)
#### 免费试用
##### [解决方案免费试用 新老同享 最高领取价值200元试用点，立即开启云上创新](https://www.aliyun.com/solution/free)##### [AI 产品 免费试用 1亿+ 大模型 tokens 和 30+ 款产品免费体验](https://free.aliyun.com/product/ai)##### [140+云产品 免费试用 产品新客免费试用，最长12个月](https://free.aliyun.com/)##### [大模型ACA认证体验 助力企业全员 AI 认知与能力提升](https://edu.aliyun.com/learning/topic/llm-free-trial)
#### AI 特惠
##### [智启 AI 普惠权益 至高享 1亿+免费 tokens，加速 Al 应用落地](https://www.aliyun.com/benefit/scene/ai-discount)##### [阿里云 OPC 创新助力计划 至高百万元 Token 补贴，加速一人公司成长](https://opc.aliyun.com/)##### [Token Plan 模型订阅计划 _NEW_ Qwen3.8-Max 首发尝鲜，限时加量 10 倍，夜间低至2折](https://www.qianwenai.com/benefits/tokenplan)##### [万小智 AI 建站低至 15元/月 送.CN域名，送备案服务码 ](https://opc.aliyun.com/activity#J_1)##### [Night Plan：3.8-Max/Flash 限时4折 _NEW_ 22:00 后开跑，Qoder / Meoo 客户直接生效](https://www.qianwenai.com/benefits/nightplan)##### [万镜一刻，视频创作低至39元/月 AI 短剧与营销素材高效产出](https://www.aliyun.com/benefit/scene/yikeai)
#### AI 场景体验
##### [AI 电商营销 从图文生成到视频创作，一键激活电商全链路生产力](https://www.aliyun.com/benefit/aiuse/e-commerce)##### [AI Coding 描述需求，智能体自主编程，端到端独立完成](https://www.aliyun.com/benefit/scene/qoder)##### [AI 广告创作 图文、视频一站生成，高效打造优质广告素材](https://www.aliyun.com/benefit/aiuse/ad)##### [AI 建站 0 代码专业建站，无忧落地极速上线](https://www.aliyun.com/benefit/client/website?tid=service-overview)##### [AI 办公 AI智能应用，一键激活高效办公新体验 ](https://www.aliyun.com/product/qwenwork)##### [AI 短剧/漫剧 AI助力短剧漫剧创作，剧本、分镜、视频高效生成](https://www.aliyun.com/benefit/scene/playlet)##### [智能客服 自动承接线索、识别商机，让客服更高效、服务更出色。 ](https://www.aliyun.com/benefit/scene/callcenter)##### [企业知识库 一键入库随问随引，RAG新客享30天免费额度](https://www.aliyun.com/benefit/client/office)
#### AI 活动
##### [AI 生产力先锋 先锋实践拓展 AI 生产力的边界](https://www.aliyun.com/activity/ai-seminar/home)##### [飞天发布时刻 所见，即是所愿](https://summit.aliyun.com/apsaramoment)##### [AI 实训营 从基础到进阶，Agent 创客手把手教你](https://www.aliyun.com/benefit/aihands-on/mainpage)
#### 创新加速
##### [上云场景组合购 覆盖90%+业务场景，专享组合折扣价](https://www.aliyun.com/benefit/client/package)##### [云聚AI 严选权益  精选AI产品，从模型到应用全链提效](https://www.aliyun.com/benefit/client/index)##### [AI 用量加速计划 新老同享，达量后返](https://www.aliyun.com/benefit/client/maas)
提供灵活的计费方式和清晰的计费规则，满足不同的业务场景需求；支持自助估算价格、高效采购；专业的成本管理工具，持续优化云上成本。
#### [产品定价 了解云产品的定价详情](https://www.aliyun.com/price/detail)#### [云上成本管理 管理和优化成本](https://www.aliyun.com/price/cost-management)
#### [价格计算器 自助选配和估算价格](https://www.aliyun.com/price/product)#### [价格优势 推动算力普惠，释放技术红利](https://www.aliyun.com/price/advantage)
#### [配置报价器 一站式生成采购清单，支持单品或批量购买](https://www.aliyun.com/price/cpq/list)
##### [阿里云 OPC 创新助力计划 至高可申请百万元 Token 补贴，五大权益加速 OPC 成功](https://opc.aliyun.com/)
提供与阿里云能力融合和互补的优质伙伴产品和服务，满足企业上云和各类业务应用开发需求。
[网站建设](https://market.aliyun.com/xinxuan/webdesign)[多端小程序](https://market.aliyun.com/xinxuan/application/miniapps)[Salesforce 国际版订阅](https://market.aliyun.com/products/56790007/cmfw00037956.html?innerSource=search_salesforce#sku=yuncode3195600001)[友盟天域](https://market.aliyun.com/products/56842011/cmfw00040027.html)[观测云](https://market.aliyun.com/products/56838014/cmgj00053362.html)[Tuya 物联网平台阿里云版](https://www.aliyun.com/research/tuya)[蓝凌 OA](https://market.aliyun.com/xinxuan/lanling-oa)[电子合同](https://market.aliyun.com/xinxuan/wyy-2023)[畅捷通](https://market.aliyun.com/products/56764034/cmgj00042861.html)[Tableau 订阅](https://market.aliyun.com/products/56024006/cmfw00062543.html)[AI空中课堂在线直播课堂（旗舰版）](https://market.aliyun.com/products/201204006/cmgj00070018.html)
[行业生态解决方案](https://market.aliyun.com/industry)[开发者生态解决方案](https://market.aliyun.com/developer/shouye)[AI 开发和 AI 应用解决方案](https://market.aliyun.com/developer/AIGC)
[数据集](https://market.aliyun.com/dataexchange)[手机三要素](https://market.aliyun.com/products?k=%E6%89%8B%E6%9C%BA%E4%B8%89%E8%A6%81%E7%B4%A0&scene=market)[身份实名认证](https://market.aliyun.com/products?k=%E8%BA%AB%E4%BB%BD%E5%AE%9E%E5%90%8D%E8%AE%A4%E8%AF%81&scene=market)[短信](https://market.aliyun.com/products?k=%E7%9F%AD%E4%BF%A1&scene=market)[OCR 文字识别](https://market.aliyun.com/products?k=OCR%E6%96%87%E5%AD%97%E8%AF%86%E5%88%AB&scene=market)[发票查验](https://market.aliyun.com/products?k=%E5%8F%91%E7%A5%A8%E6%9F%A5%E9%AA%8C&scene=market)[天气预报查询](https://market.aliyun.com/products?k=%E5%A4%A9%E6%B0%94%E9%A2%84%E6%8A%A5%E6%9F%A5%E8%AF%A2&scene=market)[快递物流查询](https://market.aliyun.com/products?k=%E5%BF%AB%E9%80%92%E7%89%A9%E6%B5%81%E6%9F%A5%E8%AF%A2&scene=market)
[ERP](https://market.aliyun.com/products?k=ERP&scene=market)[CRM](https://market.aliyun.com/products?k=CRM&scene=market)[OA 办公系统](https://market.aliyun.com/products?k=OA%E5%8A%9E%E5%85%AC%E7%B3%BB%E7%BB%9F&scene=market)[财税管理](https://market.aliyun.com/products/56764034?page=1&scene=market)[400电话](https://market.aliyun.com/products?k=400%E7%94%B5%E8%AF%9D&scene=market)[广告营销](https://market.aliyun.com/products/56842011?page=1&scene=market)
[Windows](https://market.aliyun.com/products?k=Windows&scene=market)[宝塔 Linux](https://market.aliyun.com/products?k=%E5%AE%9D%E5%A1%94+Linux&scene=market)[CentOS](https://market.aliyun.com/products?k=CentOS&scene=market)[Docker](https://market.aliyun.com/products?k=Docker&scene=market)[JAVA](https://market.aliyun.com/products?k=JAVA&scene=market)[全能环境](https://market.aliyun.com/products?k=%E5%85%A8%E8%83%BD%E7%8E%AF%E5%A2%83&scene=market)[操作系统](https://market.aliyun.com/products?k=%E6%93%8D%E4%BD%9C%E7%B3%BB%E7%BB%9F&scene=market)[WordPress](https://market.aliyun.com/products?k=WordPress&scene=market)[Ubuntu](https://market.aliyun.com/products?k=Ubuntu&scene=market)[Red Hat](https://market.aliyun.com/products?k=Red+Hat&scene=market)[SUSE](https://market.aliyun.com/products?k=SUSE&scene=market)
[模板建站](https://market.aliyun.com/products/56598032?page=1&scene=market)[定制建站](https://market.aliyun.com/products/52738005?page=1&scene=market)[模板小程序](https://market.aliyun.com/products/205798005?page=1&scene=market)[定制小程序](https://market.aliyun.com/products/52752001?page=1&scene=market)[APP 开发](https://market.aliyun.com/products/55514022?page=1&scene=market)[建站系统](https://market.aliyun.com/products/57342011?page=1&scene=market)
[域名](https://market.aliyun.com/products?k=%E5%9F%9F%E5%90%8D&scene=market)[商标](https://market.aliyun.com/products?k=%E5%95%86%E6%A0%87&scene=market)[备案](https://market.aliyun.com/products?k=%E5%A4%87%E6%A1%88&scene=market)[公司注册](https://market.aliyun.com/products?k=%E5%85%AC%E5%8F%B8%E6%B3%A8%E5%86%8C&scene=market)[上云迁移](https://market.aliyun.com/products/52738004?page=1&scene=market)[代维服务](https://market.aliyun.com/products/52732002?page=1&scene=market)
[VPN](https://market.aliyun.com/products?k=VPN&scene=market)[SSL 证书](https://market.aliyun.com/products?k=SSL%E8%AF%81%E4%B9%A6&scene=market)[堡垒机](https://market.aliyun.com/products?k=%E5%A0%A1%E5%9E%92%E6%9C%BA&scene=market)[防火墙](https://market.aliyun.com/products?k=%E9%98%B2%E7%81%AB%E5%A2%99&scene=market)[主机安全](https://market.aliyun.com/products?k=%E4%B8%BB%E6%9C%BA%E5%AE%89%E5%85%A8&scene=market)
#### [AI 应用及服务市场](https://market.aliyun.com/common/ai)
[AI 应用](https://market.aliyun.com/products?k=AI%E5%BA%94%E7%94%A8&scene=market)[大模型](https://market.aliyun.com/products?k=%E5%A4%A7%E6%A8%A1%E5%9E%8B&scene=market)[自然语言处理](https://market.aliyun.com/products?k=%E8%87%AA%E7%84%B6%E8%AF%AD%E8%A8%80%E5%A4%84%E7%90%86&scene=market)[数据标注](https://market.aliyun.com/products/201198004?page=1&scene=market)[机器学习](https://market.aliyun.com/products?k=%E6%9C%BA%E5%99%A8%E5%AD%A6%E4%B9%A0&scene=market)
坚持伙伴优先，为伙伴提供产品、销售和服务的商业合作模式；与伙伴紧密合作，共同为客户提供更完备的产品、更完善的服务。
#### 成为销售伙伴
[分销伙伴](https://partner.aliyun.com/programs/reseller_P)[咨询伙伴](https://partner.aliyun.com/program/consult_partner)
#### 销售伙伴合作计划
[无影生态合作计划](https://partner.aliyun.com/management/epp_wuying)[Salesforce On Alibaba Cloud Consulting Partner 合作计划](https://partner.aliyun.com/program/Salesforce_program)[AI 大模型销售与服务生态合作计划](https://partner.aliyun.com/program/aimsp)
#### 成为产品伙伴
[产品生态集成认证中心](https://partner.aliyun.com/program/PEIC)[产品生态伙伴](https://chanpinshengtai.aliyun.com/partner/partner)[产品生态伙伴工作台](https://aps.aliyun.com/#/)
#### 产品伙伴合作计划
[阿里云MaaS产品伙伴计划（繁花）](https://chanpinshengtai.aliyun.com/partner/ai)[弹性计算合作计划](https://partner.aliyun.com/program/txjs_program)[云存储合作计划](https://partner.aliyun.com/program/cunchu)[数据库合作计划](https://partner.aliyun.com/program/sjk_program)[云网络合作计划](https://chanpinshengtai.aliyun.com/chanpinpartner/network)[Salesforce On Alibaba Cloud ISV 合作计划](https://partner.aliyun.com/program/Salesforce-ISV)
[服务生态伙伴](https://gts.aliyun.com/)
#### 服务伙伴合作计划
[Al MaaS 服务伙伴赋能合作](https://gts.aliyun.com/ai-maas/partner/certification)[伙伴信用分合作计划](https://www.aliyun.com/gts/msp/Creditscoresystem)
#### 更多支持
[合作伙伴培训与认证](https://edu.aliyun.com/certification/partner)[查询合作伙伴](https://partner.aliyun.com/management/query#/)[登录合作伙伴管理后台](https://account.aliyun.com/login/qr_login.htm?oauth_callback=https://partner.aliyun.com/management/v2)
提供多样化的支持计划和专家服务，满足上云咨询、迁移上云、云上运维等场景的全链路服务需求。
#### 售前咨询
[在线服务](https://smartservice.console.aliyun.com/pre-sale/chat?entrance=201&referrer=https%3A%2F%2Fwww.aliyun.com%2F%3Fspm%3Da1z2e.12184483.navigationzhcn.dnavigationzhcn6.469d3247dm8YgK)
#### 售后服务
[自助服务](https://smartservice.console.aliyun.com/tourist-self/self-service-center?from=webnav)[在线服务](https://smartservice.console.aliyun.com/service/robot-chat)[工单服务](https://smartservice.console.aliyun.com/service/create-ticket)[短信专区](https://smartservice.console.aliyun.com/tourist-self/self-service-center/topic?topicCode=dysms&from=webnav)
#### 企业增值服务
[企业支持计划](https://www.aliyun.com/service/supportplans)[专家技术服务](https://www.aliyun.com/service/list)[企业增值服务台](https://custservice.console.aliyun.com/value-added/home)
#### 企业成长
[服务实践](https://www.aliyun.com/service/customer-case)[创新中心](https://chuangke.aliyun.com/)
[大模型认证](https://edu.aliyun.com/certification/llm)[全部认证](https://edu.aliyun.com/certification/)[训练营](https://edu.aliyun.com/trainingcamp)
#### 信息公告
[官网公告](https://www.aliyun.com/notice/)[健康状态](https://status.aliyun.com/)
[博文](https://developer.aliyun.com/indexFeed/)[问答](https://developer.aliyun.com/ask/)[电子书](https://developer.aliyun.com/ebook/)[镜像站](https://developer.aliyun.com/mirror/)
#### 我要反馈
[我要建议](https://www.aliyun.com/connect/home)[我要投诉](https://www.aliyun.com/complaint)
作为全球领先的全栈人工智能服务商，阿里云坚持让计算成为公共服务，助力全球客户加速价值创新。
[什么是云计算](https://www.aliyun.com/about/what-is-cloud-computing)[技术领先](https://www.aliyun.com/why-us/leading-technology)[稳定可靠](https://www.aliyun.com/why-us/reliability)[安全合规](https://www.aliyun.com/why-us/security-compliance)[分析师报告](https://www.aliyun.com/analyst-reports)[研究报告与白皮书](https://www.aliyun.com/reports)
[AI 算法大赛](https://tianchi.aliyun.com/competition/algorithmList/)[云开发大赛](https://tianchi.aliyun.com/competition/programList)[入门学习赛](https://tianchi.aliyun.com/competition/coupleList)
#### 最佳实践
[云上春晚](https://www.aliyun.com/about/gala)[云上奥运之旅](https://www.aliyun.com/about/games)[云栖战略参考](https://www.aliyun.com/about/magazines)[云上的中国](https://www.aliyun.com/about/ysdzg)[看见新力量](https://startup.aliyun.com/special/seenewpower)[金融模力时刻](https://summit.aliyun.com/market/financial-agent)[客户案例](https://www.aliyun.com/customer-stories/customer-case-index)
#### 市场活动
[2026 阿里云峰会](https://summit.aliyun.com/2026)[阿里云中企出海大会](https://summit.aliyun.com/go-global)[云栖大会](https://yunqi.aliyun.com/)[活动全景](https://www.aliyun.com/about/events)
#### 魔搭 ModelScope
[魔搭 ModelScope](https://modelscope.cn/home)
#### 高校合作
[云工开物](https://university.aliyun.com/)[科研合作](https://university.aliyun.com/activity/air)
[Careers](https://careers.aliyun.com/en/home)[社会招聘](https://careers.aliyun.com/off-campus/home)[校园招聘](https://careers.aliyun.com/campus/home)
### [阿里云国际站 www.alibabacloud.com](https://www.alibabacloud.com/)
### 联系我们
4008013260[售前咨询](https://smartservice.console.aliyun.com/pre-sale/chat?entrance=201&referrer=https%3A%2F%2Fdeveloper.aliyun.com%2Farticle%2F1754064)[售后在线](https://smartservice.console.aliyun.com/service/robot-chat?entrance=201&referrer=https%3A%2F%2Fdeveloper.aliyun.com%2Farticle%2F1754064)
### 其他服务
[我要建议](https://www.aliyun.com/connect/home)[我要投诉](https://www.aliyun.com/complaint)
