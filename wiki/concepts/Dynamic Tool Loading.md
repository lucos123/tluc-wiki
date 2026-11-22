---
title: Dynamic Tool Loading
date: 2026-08-01
tags:
  - concept
  - agentic-design
  - tool
---

# Dynamic Tool Loading

An API pattern supported by [Moonshot AI](../entities/Moonshot%20AI.md) models ([Kimi K3](../entities/Kimi%20K3.md), [Kimi K2.7 Code](../entities/Kimi%20K2.7%20Code.md)) where tool definitions are loaded dynamically mid-conversation by placing a complete JSON tool definition inside a `system` role message without a `content` string.

## How it Works

1. **Inline Declaration**: Instead of declaring all tools globally at the start of a session, a client inserts a `system` message containing a `tools` array at any point in the `messages` array.
2. **On-Demand Scope**: The tool becomes available to the model from that message position onward.
3. **Context Control**: Reduces initial prompt token overhead by only introducing specialized tool schemas (e.g. calculator, specific database queries) when the agent workflow reaches the specific sub-task requiring them.

See [Kimi K3 Model Guide](../sources/Kimi%20K3%20Model%20Guide.md) and [Kimi API Quickstart & Integration](../sources/Kimi%20API%20Quickstart%20%26%20Integration.md).
