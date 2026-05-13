# Claude Prompt Caching Documentation

## Overview

Prompt caching allows resuming from specific prefixes in prompts, significantly reducing processing time and costs for repetitive tasks or prompts with consistent elements.

## Two Methods of Enabling Cache

1. **Automatic caching**: Add `cache_control` at the request's top level. The system automatically applies the cache breakpoint to the last cacheable block.

2. **Explicit cache breakpoints**: Place `cache_control` directly on individual content blocks for fine-grained control.

## How It Works

1. System checks if a prompt prefix up to the cache breakpoint is cached from a recent query
2. If found, cached version is used (reducing cost and latency)
3. Otherwise, processes full prompt and caches the prefix once response begins

## Pricing

| Model | Base Input | 5m Cache Writes | 1h Cache Writes | Cache Hits |
|-------|------------|------------------|-----------------|------------|
| Claude Opus 4.7 | $5/MTok | $6.25/MTok | $10/MTok | $0.50/MTok |
| Claude Sonnet 4.6 | $3/MTok | $3.75/MTok | $6/MTok | $0.30/MTok |
| Claude Haiku 4.5 | $1/MTok | $1.25/MTok | $2/MTok | $0.10/MTok |

- 5-minute cache write tokens = 1.25x base input price
- 1-hour cache write tokens = 2x base input price
- Cache read tokens = 0.1x base input price (90% discount!)

## Cache Limitations

**Minimum token thresholds:**
- **4,096 tokens**: Claude Opus 4.7, 4.6, 4.5, Claude Haiku 4.5
- **1,024 tokens**: Claude Sonnet 4.6, 4.5, Opus 4.1
- **2,048 tokens**: Claude Haiku 3.5

**Cannot be cached:**
- Thinking blocks
- Sub-content blocks like citations
- Empty text blocks

**Invalidates cache:**
- Tool definition changes
- Web search/citations toggles
- Speed setting changes
- `tool_choice` parameter changes
- Adding/removing images
- Thinking parameter changes

## Tracking Cache Performance

Response usage fields:
- `cache_creation_input_tokens`: Tokens written to cache
- `cache_read_input_tokens`: Tokens retrieved from cache
- `input_tokens`: Tokens after last cache breakpoint

**Formula:** `total_input_tokens = cache_read + cache_creation + input_tokens`

## Cache Pre-Warming

Eliminate first-request latency by pre-loading cache with `max_tokens: 0`.

## Key Best Practices

- Place `cache_control` on the **last block that stays identical** across requests
- Avoid placing breakpoints on blocks with varying content (timestamps, per-request context)
- Cache stable, reusable content (system prompts, large contexts, tool definitions)
