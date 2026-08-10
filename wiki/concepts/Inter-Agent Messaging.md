---
title: "Inter-Agent Messaging"
date: 2026-08-10
tags:
  - concept
  - harness-engineering
  - parallelism
  - claude-code
source: "[[Orchestrate teams of Claude Code sessions]]"
---

# Inter-Agent Messaging

**Inter-Agent Messaging** is the cross-session communications layer in [[Claude Code]] that allows peer agent instances (within [[Agent Teams Architecture|Agent Teams]] or via `SendMessage`) to exchange JSON messages and status updates directly.

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

See [[Orchestrate teams of Claude Code sessions]], [[Agent Teams Architecture]], and [[Parallel Agent Architecture]].
