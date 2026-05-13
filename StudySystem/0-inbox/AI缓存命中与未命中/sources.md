# Sources for AI缓存命中与未命中

| # | Title | URL | Author | Date | Type | Notes |
|---|-------|-----|--------|------|------|-------|
| 1 | The Complete Guide to Inference Caching in LLMs | https://machinelearningmastery.com/the-complete-guide-to-inference-caching-in-llms/ | MachineLearningMastery | 2024 | tutorial | LLM inference caching overview, KV cache, prefix caching |
| 2 | Cache (computing) | https://en.wikipedia.org/wiki/Cache_(computing) | Wikipedia | - | official | Core cache hit/miss definitions |
| 3 | Prompt Caching - Claude API | https://platform.claude.com/docs/en/build-with-claude/prompt-caching | Anthropic | 2025 | official | Claude prompt caching, practical implementation |
| 4 | Prompt Caching in LLMs | https://blog.dailydoseofds.com/p/prompt-caching-in-llms | Avi Chawla | 2024 | blog | KV cache mechanics, hash-based indexing, best practices |
| 5 | What is a Cache Miss? | https://hazelcast.com/foundations/caching/cache-miss/ | Hazelcast | - | article | Cache miss policies and impact |

## Coverage Summary

### 已覆盖子主题
- ✅ 缓存命中（Cache Hit）定义
- ✅ 缓存未命中（Cache Miss）定义
- ✅ 缓存在 AI/LLM 中的应用（KV Cache、Prompt Caching）
- ✅ Claude API 的提示缓存机制
- ✅ 缓存命中率与性能关系
- ✅ 缓存失效场景

### 明显缺口
- 源码级别的实现细节（入门阶段不需）
- 多层缓存架构（可作为进阶内容）
