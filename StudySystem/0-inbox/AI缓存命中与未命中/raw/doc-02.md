# Cache (computing) - Wikipedia

## Cache Hit & Cache Miss Definitions

**Cache hit:** "occurs when the requested data can be found in a cache" — served faster by reading from cache instead of recomputing or accessing slower storage.

**Cache miss:** "occurs when it cannot" be found in cache — requires the more expensive access to the backing store, after which data is typically copied into cache for future use.

## How Cache Works

A cache stores data entries, each containing:
- **Data**: a copy from the backing store
- **Tag**: identifies which data in the backing store the entry represents

When a cache client (CPU, browser, OS) needs data, it checks the cache first. A matching tag means a cache hit. The percentage of hits is the **hit rate**.

During misses, a replacement policy (like LRU) evicts an entry to make room for newly retrieved data.

### Write Policies
- **Write-through**: writes synchronously to cache and backing store
- **Write-back**: writes only to cache initially; backing store updated only when the modified data is evicted

## Relevant for AI/LLM Context

The article discusses **memoization** — storing results of function calls for reuse — which parallels how LLMs handle repeated computations. **Distributed caching** provides "scalability, reliability and performance" across networked hosts, relevant for scaling AI inference. The concept of **prefetching** (predicting and loading data ahead of time) also applies to LLM context window management and attention mechanisms.
