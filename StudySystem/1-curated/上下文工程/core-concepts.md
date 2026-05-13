# 核心概念

## 1. 提示工程 (Prompt Engineering)

**定义** (Wikipedia):
> "the process of structuring natural language inputs (known as prompts) to produce specified outputs from a generative artificial intelligence (GenAI) model."

**最佳实践**:
- 设计清晰的查询
- 优化措辞
- 提供相关上下文
- 指定输出风格
- 分配角色让 AI 模仿

**来源**: doc-01-wikipedia.md

---

## 2. 上下文工程 (Context Engineering)

**定义** (PromptingGuide):
> "the refined evolution of prompt engineering—a systematic approach to designing and optimizing all context provided to an LLM's context window."

**关键洞察**:
> "Context engineering is not just about optimizing your prompt; it's about choosing the right context for the goals you are targeting."

**来源**: doc-08-context-engineering-guide.md

---

## 3. 零样本提示 (Zero-shot Prompting)

**定义**:
不包含任何示例，直接给出指令让模型完成任务。

**适用场景**:
- GPT-3.5、GPT-4、Claude 3 等大型模型
- 简单、明确的任务
- 当不知道如何提供示例时

**来源**: doc-05-zero-shot.md

---

## 4. 少样本提示 (Few-shot Prompting)

**定义**:
通过在提示中提供示例（1-shot、3-shot、5-shot 等）来实现上下文学习。

**关键发现**:
- 标签空间的正确性不重要，重要的是分布
- 随机标签也比没有标签好
- 格式一致性有帮助

**局限**:
复杂推理任务（如多步算术）效果差，建议使用思维链。

**来源**: doc-03-few-shot.md

---

## 5. 思维链提示 (Chain-of-Thought, CoT)

**定义**:
通过展示中间推理步骤来启用复杂推理。

**关键特征**:
- 最佳效果：配合少样本示例
- 大模型的"涌现能力"
- 甚至一个示例也有效

**零样本 CoT**:
只需添加 "Let's think step by step" 即可显著改善推理能力。

**来源**: doc-02-cot.md

---

## 6. 思维树 (Tree of Thoughts, ToT)

**定义**:
保持树结构，其中"思考"是连贯的语言序列，作为中间问题解决步骤。

**关键特性**:
- 使语言模型能够自我评估进展
- 结合搜索算法（BFS、DFS、束搜索）
- 支持前瞻探索和回溯

**最佳场景**:
需要战略规划的复杂任务（如 24 点游戏）。

**来源**: doc-04-tot.md

---

## 7. 角色提示 (Role Prompting)

**定义**:
指示 LLM 如何表现、其意图和身份。

**应用场景**:
- 客服聊天机器人
- 技术支持助手
- 不同复杂度级别的教育导师
- 行业特定专家系统

**来源**: doc-06-role-prompting.md
