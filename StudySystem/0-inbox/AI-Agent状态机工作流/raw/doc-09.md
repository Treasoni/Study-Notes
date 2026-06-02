# CrewAI Multi-Agent Framework Overview

**URL**: https://docs.crewai.com/concepts/crews

## Core Concept

A **Crew** in CrewAI is a collaborative group of agents working together to accomplish tasks, defining the strategy for task execution, agent collaboration, and overall workflow orchestration.

## Crew Attributes

Crews are configured with parameters including:

- **Agents & Tasks**: Lists defining who does what
- **Process Flow**: Sequential (linear) or Hierarchical (manager-controlled)
- **Memory**: Stores execution memories (short-term, long-term, entity memory)
- **Planning**: Optional planning ability via AgentPlanner before each iteration
- **Checkpointing**: Automatic state saving after key events (task completion) for resumable runs
- **Streaming**: Real-time output during execution
- **Callbacks**: `before_kickoff_callbacks` and `after_kickoff_callbacks` for lifecycle hooks

## Creating Crews

Two approaches exist:

1. **YAML Configuration** (recommended): Uses `@CrewBase` class with decorators (`@agent`, `@task`, `@crew`) that automatically collect agents/tasks
2. **Direct Code Definition**: Manual agent/task creation without decorators

## State Management

- **Memory Utilization**: Crews store and recall execution memories for decision-making
- **Checkpointing**: Pass `checkpoint=True` or `CheckpointConfig` to save state after events; restore via `Crew.from_checkpoint()`
- **Cache**: Stores tool execution results to avoid re-execution

## Orchestration

Execution uses kickoff methods:

- **Synchronous**: `kickoff()`, `kickoff_for_each()`
- **Asynchronous**: `akickoff()` (native async), `kickoff_async()` (thread-based)

The **manager agent** in hierarchical processes coordinates delegation and validation.

## Crew Output

Results accessible via `CrewOutput` class with raw output, JSON/Pydantic formats, individual task outputs, and token usage metrics.
