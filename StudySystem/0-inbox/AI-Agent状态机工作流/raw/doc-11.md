# LLM Agent Design Patterns (Lilian Weng)

**URL**: https://lilianweng.github.io/posts/2023-06-23-agent/

## Agent System Components

An LLM-powered autonomous agent system has three key components:
- **Planning**: Subgoal decomposition and self-reflection/refinement
- **Memory**: Short-term (in-context learning) and long-term (external vector store)
- **Tool Use**: Calling external APIs for information beyond model weights

## ReAct Pattern

"ReAct integrates reasoning and acting within LLM by extending the action space to be a combination of task-specific discrete actions and the language space." The prompt format uses: "Thought: ... Action: ... Observation: ..."

## Planning Methods

- Chain of Thought (CoT) for step-by-step decomposition
- Tree of Thoughts exploring multiple reasoning paths
- Self-reflection via Reflexion and Chain of Hindsight

## Memory & State

Short-term memory uses in-context learning within transformer's context window; long-term memory leverages external vector stores with fast retrieval (MIPS) using algorithms like HNSW or FAISS.

## Tool Use Frameworks

MRKL systems route queries to expert modules; HuggingGPT uses ChatGPT as task planner to select models. API-Bank evaluates tool-augmented LLMs at three levels: calling, retrieving, and planning APIs.

## Key Takeaway

ReAct provides a simple but unbounded approach to agent control. For production systems requiring strict control over agent behavior, state machine approaches (like LangGraph) provide better guardrails by making state transitions explicit and inspectable.
