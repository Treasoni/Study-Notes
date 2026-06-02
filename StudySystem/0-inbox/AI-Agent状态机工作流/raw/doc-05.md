# LangGraph Functional API

**URL**: https://docs.langchain.com/oss/python/langgraph/functional-api

## Overview

The **Functional API** enables adding LangGraph's core features—persistence, memory, human-in-the-loop, and streaming—to existing code using familiar Python constructs like `if` statements and function calls, without restructuring into explicit pipelines or DAGs.

## Key Building Blocks

**`@entrypoint`** marks a workflow's starting point, encapsulating logic and managing execution flow. "Decorating a function with an `entrypoint` produces a `Pregel` instance which helps to manage the execution of the workflow."

**`@task`** represents discrete units of work that execute asynchronously, returning a future-like object that can be awaited or resolved synchronously.

## Entrypoint Features

- Accepts a single positional argument (use a dictionary for multiple inputs)
- Requires a checkpointer for persistence and human-in-the-loop features
- Supports injectable parameters: `previous`, `store`, `writer`, and `config`

## Short-Term Memory

"When an `entrypoint` is defined with a `checkpointer`, it stores information between successive invocations on the same thread id in checkpoints." The `previous` parameter provides access to the previous invocation's return value.

## Task Characteristics

Tasks are useful for:
- Checkpointing long-running operations
- Human-in-the-loop workflows requiring non-deterministic operations
- Parallel execution of I/O-bound operations
- Observability and retryable work

## Critical Requirements

**Serialization**: Both entrypoint inputs/outputs and task outputs must be JSON-serializable for checkpointing support.

**Determinism**: Non-deterministic operations (random values, time-based logic) must be encapsulated in tasks. "Encapsulate side effects (e.g., writing to a file, sending an email) in tasks to ensure they are not executed multiple times when resuming a workflow."

## When to Use Tasks

Place API calls, random operations, and side effects inside `@task` decorated functions. This ensures checkpointing, proper resume behavior, and idempotency.
