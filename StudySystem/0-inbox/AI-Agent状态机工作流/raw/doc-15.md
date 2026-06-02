# LangSmith Observability Overview

**URL**: https://www.langchain.com/langsmith

## Core Functionality

LangSmith Observability provides "complete visibility into agent behavior" through step-by-step tracing. Teams can "pinpoint the issues hurting latency, cost, and response quality."

## Key Features

### Tracing
- Native support for popular agent frameworks and OpenTelemetry
- SDKs available for Python, TypeScript, Go, and Java
- Message threading for multi-turn chat interactions

### Monitoring
- Real-time agent performance tracking
- Cost tracking and online LLM-as-judge evaluations
- Tool and agent trajectory monitoring
- Webhook and PagerDuty alerts

### Insights
- Automatic trace analysis and clustering
- Unsupervised topic clustering
- Error analysis templates

## SmithDB

LangSmith's purpose-built database offers significant query performance improvements over general-purpose databases. Example speedups include:
- Trace queries: 860ms → 71ms
- Thread queries: 1.16s → 131ms
- Full-text search: 6.20s → 400ms

## Deployment Options

LangSmith supports managed cloud, bring-your-own-cloud (BYOC), and self-hosted deployments for teams with data residency requirements. The service states it will not train on customer data.
