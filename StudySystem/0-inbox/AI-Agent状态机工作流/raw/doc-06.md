# LangGraph Observability with LangSmith

**URL**: https://docs.langchain.com/oss/python/langgraph/observability

## Overview

LangSmith visualizes execution traces (runs from input to output) for debugging, evaluating, and monitoring applications.

## Setup Prerequisites

- LangSmith account at smith.langchain.com
- API key created via the account dashboard

## Enable Tracing

Set environment variables:
```
LANGSMITH_TRACING=true
LANGSMITH_API_KEY=<your-api-key>
```

By default traces log to the "default" project. Configure custom projects via `LANGSMITH_PROJECT` or programmatically with `tracing_context`.

## Selective Tracing

Use `ls.tracing_context(enabled=True)` to trace specific invocations without affecting others.

## Metadata & Tags

Attach custom data via config parameters to annotate traces with user IDs, session info, environment details, or custom tags.

## Data Privacy

Anonymizers (regex-based) can mask sensitive data like SSNs before traces reach LangSmith using `create_anonymizer()`.
