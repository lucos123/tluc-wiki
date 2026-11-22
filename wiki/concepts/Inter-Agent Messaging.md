---
title: "Inter-Agent Messaging"
date: 2026-08-10
tags:
  - concept
  - harness-engineering
  - parallelism
  - claude-code
source: "wiki/sources/Orchestrate teams of Claude Code sessions.md"
---

# Inter-Agent Messaging

**Inter-Agent Messaging** is the cross-session communications layer in [Claude Code](../entities/Claude%20Code.md) that allows peer agent instances (within [Agent Teams](Agent%20Teams%20Architecture.md) or via `SendMessage`) to exchange JSON messages and status updates directly.

---

## Inbox Topography

Each agent possesses a dedicated filesystem inbox at:
`~/.claude/teams/{team-name}/inboxes/{agent-name}.json`

```json
{
  "sender": "frontend-dev",
  "recipient": "backend-dev",
  "content": "API endpoint for auth is deployed; ready for integration tests.",
  "timestamp": "2026-08-10T16:30:00Z"
}
```

## Protocol Features

1. **Self-Healing Inbox Validation**: Corrupted or malformed inbox messages are automatically stripped and reported without blocking valid message delivery.
2. **Asynchronous Polling**: Agents read inboxes at turn boundaries to update their working state.

See [Orchestrate teams of Claude Code sessions](../sources/Orchestrate%20teams%20of%20Claude%20Code%20sessions.md), [Agent Teams Architecture](Agent%20Teams%20Architecture.md), and [Parallel Agent Architecture](Parallel%20Agent%20Architecture.md).
