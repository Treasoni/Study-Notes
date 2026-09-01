---
url: "https://docs.deeptutor.info/zh-cn/cli/agent-handoff/"
title: "代理交接 | DeepTutor"
scraped_at: 2026-09-01T15:28:58+00:00
---

[跳转到内容](https://docs.deeptutor.info/zh-cn/cli/agent-handoff/#_top)
DeepTutor 从设计之初就是为了 **被其他 agent 驱动** 的：turn 执行可以输出结构化 JSON，session 能跨进程恢复，受支持的 surface 都集中在一个 skill 文件里 —— 任何会用 tool 的 LLM 读完就能直接上手。
这一页就是那套 playbook。
## 基本套路
[Section titled “基本套路”](https://docs.deeptutor.info/zh-cn/cli/agent-handoff/#%E5%9F%BA%E6%9C%AC%E5%A5%97%E8%B7%AF)
根目录 [`SKILL.md`](https://github.com/HKUDS/DeepTutor/blob/main/SKILL.md) 是精简交接，不是穷尽 contract：列表漏了 `ask_questions`、`immersive_reading`、`course_study`、`immersive_watching`。实时 capability 查 `plugin list` / `--help`，JSON 查本页。`--tool` 只影响用户 toggle；`rag`、`code_execution` 满足条件才自动挂载。
把 `SKILL.md` 丢给你选的 agent，它就能：
  * 跑 capability（`deep_solve`、`deep_research`、`deep_question`、……）
  * 管理知识库（`kb create`、`kb search`、`kb add`）
  * 用 `--session` 跑长程多轮会话
  * 把 JSON 输出管道给下游工具
  * 在一个任务中途切换 capability 和 tool


## Claude Code
[Section titled “Claude Code”](https://docs.deeptutor.info/zh-cn/cli/agent-handoff/#claude-code)
[Claude Code](https://docs.claude.com/en/docs/claude-code) 看到项目根目录有 `SKILL.md` 时会自动读它。
Terminal window
```


cd/your-project



# DeepTutor 的 SKILL.md 在 DeepTutor/SKILL.md；复制或软链过来：



ln-s/path/to/DeepTutor/SKILL.md./SKILL.md




# 或者更简单：通过 Claude Code 的 allowed-skills 配置带进来

```

一旦 Claude Code 看到 `SKILL.md`，它就理解 CLI 了。你可以自然语言提示：

```

> 给我做一个未来两周关于线性代数的学习计划。用 DeepTutor：


> 从 ./textbooks/ 里的 PDF 创建一个 KB，然后出 10 道测验题，


> 分布在三个难度上。

```

Claude Code 会把它翻译成：
Terminal window
```


deeptutorkbcreatelinalg--docs-dir./textbooks/




# 第一次出题 —— 开一个新 session，从 'done' 事件里抓 session id，


# 后两轮复用它。



SESSION_ID=$(deeptutorrundeep_question"Linear algebra fundamentals"\




--kblinalg\




--confignum_questions=4--configdifficulty=easy\




--formatjson|jq-r'select(.type=="done") | .session_id')





deeptutorrundeep_question"Linear algebra eigenvectors"\




--kblinalg--session"$SESSION_ID"\




--confignum_questions=3--configdifficulty=medium





deeptutorrundeep_question"Linear algebra advanced theorems"\




--kblinalg--session"$SESSION_ID"\




--confignum_questions=3--configdifficulty=hard


```

它用 `--session` 把三轮出题串在一起。
### 把 deeptutor CLI 接成 Claude Code 的 subagent
[Section titled “把 deeptutor CLI 接成 Claude Code 的 subagent”](https://docs.deeptutor.info/zh-cn/cli/agent-handoff/#%E6%8A%8A-deeptutor-cli-%E6%8E%A5%E6%88%90-claude-code-%E7%9A%84-subagent)
如果你想在 Claude Code 里有一个固定的 “学习 agent”，永远走 `deeptutor`：
.claude/agents/study-agent.yaml
```


name: study-agent




description: Use this agent for any learning, study planning, or quiz generation task. It drives DeepTutor.




tools: [Bash, Read, Write]




system_prompt: |




You are a study planner. You have access to the `deeptutor` CLI via the Bash tool.




Read SKILL.md before doing anything else. Then build study plans, generate quizzes,




and run research turns by calling `deeptutor run <capability> "..."` with the right




flags. Always pass `--format json` for parsing.


```

## Codex（OpenAI Codex CLI）
[Section titled “Codex（OpenAI Codex CLI）”](https://docs.deeptutor.info/zh-cn/cli/agent-handoff/#codexopenai-codex-cli)
Codex 走类似的套路。把 `SKILL.md` 放到项目根目录，然后提示：

```

codex "Read SKILL.md, then run a deep research turn on transformer attention mechanisms. Use the 'papers' knowledge base if it exists; if not, just web search."

```

对于走 OAuth 的 provider（比如 OpenAI Codex 自己），DeepTutor 内置了登录命令：
Terminal window
```


deeptutorproviderloginopenai-codex



# 浏览器打开做 OAuth，token 存到工作区

```

之后就可以用拿到的 token 通过 DeepTutor 使用 OpenAI Codex。
## OpenCode
[Section titled “OpenCode”](https://docs.deeptutor.info/zh-cn/cli/agent-handoff/#opencode)
[OpenCode](https://opencode.ai) 同样的玩法。把项目的 `SKILL.md` 加进来：
Terminal window
```


opencodeinit




ln-s/path/to/DeepTutor/SKILL.md./SKILL.md




opencode"Plan a study session on quantum mechanics using deeptutor"


```

## Hermes / 通用 agent 框架
[Section titled “Hermes / 通用 agent 框架”](https://docs.deeptutor.info/zh-cn/cli/agent-handoff/#hermes--%E9%80%9A%E7%94%A8-agent-%E6%A1%86%E6%9E%B6)
对于原生不认 `SKILL.md` 的 agent 框架（LangChain agent、AutoGen、自定义 loop），把 `deeptutor` 包成一个 tool 定义就行。一个最小化的 LangChain 封装：

```


from langchain.tools import Tool




import subprocess




import json





defdeeptutor_run(args_json: str) -> str:




args = json.loads(args_json)




cmd =[




"deeptutor", "run",




args["capability"],




args["message"],




"--format", "json",





for tool in args.get("tools",[]):




cmd.extend(["--tool", tool])




for kb in args.get("knowledge_bases",[]):




cmd.extend(["--kb", kb])




if args.get("session_id"):




cmd.extend(["--session", args["session_id"]])




for key, value in args.get("config", {}).items():




cmd.extend(["--config", f"{key}={json.dumps(value)}"])





result = subprocess.run(cmd,capture_output=True,text=True)




return result.stdout





deeptutor_tool =Tool(




name="deeptutor_run",




description=(




"Run a DeepTutor capability. Args: JSON object with "




"{capability, message, tools, knowledge_bases, session_id, config}. "




"Returns one JSON event per line."





func=deeptutor_run,



```

然后你的 agent loop 就可以直接用了。
## Session 交接 pattern
[Section titled “Session 交接 pattern”](https://docs.deeptutor.info/zh-cn/cli/agent-handoff/#session-%E4%BA%A4%E6%8E%A5-pattern)
最强的一种用法：让 agent **在同一个 session 里串起多次 capability 调用** ，让每个新的 turn 继承前一个的上下文。
Terminal window
```

# Step 1 —— 研究



SESSION_ID=$(deeptutorrundeep_research"Survey 2026 papers on RAG"\




--toolweb_search--kbpapers\




--configmode=report--configdepth=standard\




--formatjson|\




jq-r'select(.type=="done") | .session_id')




# Step 2 —— 总结（同一 session，不同 capability）



deeptutorrunchat"Summarize the top three findings as bullet points"\




--session"$SESSION_ID"--formatjson




# Step 3 —— 出题（同一 session）



deeptutorrundeep_question"The findings from this session"\




--session"$SESSION_ID"\




--confignum_questions=5\




--formatjson


```

每一步都会继承：
  * 完整对话历史
  * 相同的 session 身份与对话分支


每次 `run` 都发送自己的选择：省略 flag 就是 `tools=[]`、`knowledge_bases=[]`、`language="en"`，会覆盖 session 偏好。需要时重复 `--tool`、`--kb`、`--language`；对话上下文仍有状态。
## JSON 事件解析
[Section titled “JSON 事件解析”](https://docs.deeptutor.info/zh-cn/cli/agent-handoff/#json-%E4%BA%8B%E4%BB%B6%E8%A7%A3%E6%9E%90)
`--format json` 按行解析；无头 `ask_user` 暂停会自动收到空回复。最小 Python 消费者：

```


import json




import subprocess





proc = subprocess.Popen(




["deeptutor", "run", "deep_solve", "Find d/dx [sin(x²)]",




"--tool", "reason", "--format", "json"],




stdout=subprocess.PIPE,




text=True,






answer =""




for line in proc.stdout:




event = json.loads(line)




if event["type"] =="result":




answer = event.get("metadata", {}).get("response","")




elif event["type"] =="tool_call":




print(f"→ Tool: {event['content']}({event['metadata']['args']})")




elif event["type"] =="error":




print(f"× Error: {event['content']}")




break




elif event["type"] =="done":




session_id = event["session_id"]




break


```

或者用 `jq`：
Terminal window
```

# 拿到最终答案



deeptutorrunchat"Hello"--formatjson|\




jq-r'select(.type == "result") | .metadata.response // empty'




# 拿到 session id



deeptutorrunchat"Hello"--formatjson|\




jq-r'select(.type=="done") | .session_id'




# 流式打印每个 stage 完成的瞬间



deeptutorrundeep_research"..."\




--configmode=report--configdepth=quick\




--formatjson|\




jq-r'select(.type=="stage_end") | "Stage finished: " + .stage'


```

## 你的 SKILL.md 里到底放什么
[Section titled “你的 SKILL.md 里到底放什么”](https://docs.deeptutor.info/zh-cn/cli/agent-handoff/#%E4%BD%A0%E7%9A%84-skillmd-%E9%87%8C%E5%88%B0%E5%BA%95%E6%94%BE%E4%BB%80%E4%B9%88)
仓库内置的 [`SKILL.md`](https://github.com/HKUDS/DeepTutor/blob/main/SKILL.md) 覆盖：
  1. **When to Use** —— 哪些用户请求应该触发 DeepTutor
  2. **Prerequisites** —— Python 3.11+、安装方式、`deeptutor init`
  3. **Commands** —— Chat & Capabilities、Knowledge Bases、Partners、Skills、Books、Memory、Sessions、Notebooks、Providers、System
  4. **REPL Slash Commands** —— `deeptutor chat` 内部可用的命令
  5. **Typical Workflows** —— 一组 agent 可以照着复刻的端到端 recipe


整份共 203 行，按 “一次吞下去” 写的 —— 主流会用 tool 的 agent（Claude Sonnet/Opus、GPT-4/5、Gemini Pro）读一遍就能上手。
## 给云端 agent 准备的 provider token
[Section titled “给云端 agent 准备的 provider token”](https://docs.deeptutor.info/zh-cn/cli/agent-handoff/#%E7%BB%99%E4%BA%91%E7%AB%AF-agent-%E5%87%86%E5%A4%87%E7%9A%84-provider-token)
DeepTutor 本地 CLI 命令不需要浏览器，但模型 / 搜索功能会去访问你配的 provider。如果你的 agent 跑在沙箱环境里，确认下面这些是可达的：  
| Provider  | 需要放行的 endpoint  |  
| --- | --- |  
| OpenAI  | `api.openai.com:443`  |  
| Anthropic  | `api.anthropic.com:443`  |  
| Google Gemini  | `generativelanguage.googleapis.com:443`  |  
| Azure OpenAI  | `<your-resource>.openai.azure.com:443`  |  
| 本地 Ollama / vLLM  |  `data/user/settings/model_catalog.json` 或进程环境变量里配的 endpoint  |  
如果是 RAG 密集型工作流，还要放行你配置的搜索 provider（Tavily、Brave、Jina、Serper、Perplexity、SearXNG 或 DuckDuckGo）。
## 另见
[Section titled “另见”](https://docs.deeptutor.info/zh-cn/cli/agent-handoff/#%E5%8F%A6%E8%A7%81)
  * [**命令参考**](https://docs.deeptutor.info/zh-cn/cli/commands/) —— 完整 CLI 参考
  * [**交互式 REPL**](https://docs.deeptutor.info/zh-cn/cli/chat-repl/) —— 人工驱动的会话
  * [**Memory**](https://docs.deeptutor.info/zh-cn/explore/memory/) —— 持久状态怎么在 session 之间流动


