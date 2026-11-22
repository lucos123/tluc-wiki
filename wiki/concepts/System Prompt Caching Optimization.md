---
title: "System Prompt Caching Optimization"
date: 2026-08-10
tags:
  - concept
  - context-engineering
  - cost-optimization
  - claude-code
source: "wiki/sources/Modifying system prompts.md"
---

# System Prompt Caching Optimization

**System Prompt Caching Optimization** is the context engineering technique of separating static system instructions from dynamic per-session environment metadata to achieve maximum API prompt cache hit rates.

---

## Architectural Mechanics (`excludeDynamicSections`)

```mermaid
graph TD
    Default["Default Setup (Cache Miss Across Hosts)"] --> System1["System Prompt: [Static Preset] + [Working Dir: /foo] + [Branch: main]"]
    Optimized["Optimized Setup (excludeDynamicSections: true)"] --> System2["System Prompt: [Static Preset Only] (Shared Cache Hit)"]
    Optimized --> User1["User Message: [Working Dir: /foo] + [Branch: main]"]
```

## Core Benefits

1. **Distributed Agent Fleets**: Fleet agents running on different containers/machines share identical system prompt cache entries.
2. **Cost Reduction**: Substantially lowers input token costs on subsequent turn calls across multi-tenant worker nodes.

See [Modifying system prompts](../sources/Modifying%20system%20prompts.md), [Context Window Management](Context%20Window%20Management.md), and [Agent SDK Architecture](Agent%20SDK%20Architecture.md).
