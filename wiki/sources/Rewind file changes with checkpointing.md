---
title: "Rewind file changes with checkpointing"
date: 2026-08-10
tags:
  - source
  - file-checkpointing
  - agent-sdk
  - harness-engineering
  - claude-code
source: "raw/articles/claude-code/costs-models-checkpoints/file-checkpointing.md"
url: "https://code.claude.com/docs/en/file-checkpointing.md"
---

# Rewind file changes with checkpointing

**URL**: https://code.claude.com/docs/en/file-checkpointing.md  
**Source File**: [raw/articles/claude-code/costs-models-checkpoints/file-checkpointing.md](../../raw/articles/claude-code/costs-models-checkpoints/file-checkpointing.md)  

---

## Executive Summary

This official Anthropic guide details how to implement programmatic **File Checkpointing** using the **Claude Agent SDK** (Python & TypeScript).

File checkpointing tracks all file modifications made by editing tools (`Write`, `Edit`, `NotebookEdit`), attaching a unique checkpoint UUID to each user message stream. Programmers can invoke `rewind_files(checkpoint_id)` / `rewindFiles(checkpoint_id)` to restore files on disk to any previous snapshot without losing conversation history.

---

## SDK Implementation Pattern

```typescript
import { query } from "@anthropic-ai/claude-agent-sdk";

// Step 1: Enable file checkpointing in SDK options
const options = {
  enableFileCheckpointing: true,
  permissionMode: "acceptEdits" as const,
  extraArgs: { "replay-user-messages": null } // Emits checkpoint UUIDs
};

// Step 2: Capture checkpoint UUID from stream
for await (const message of query({ prompt: "Refactor auth", options })) {
  if (message.type === "user" && message.uuid) {
    const checkpointId = message.uuid;
  }
}

// Step 3: Rewind files on disk to captured checkpoint
await rewindQuery.rewindFiles(checkpointId);
```

---

## Tracked vs Untracked Operations

| Operation Type | Checkpoint Tracking Status |
| --- | --- |
| `Write` / `Edit` / `NotebookEdit` | ✅ Tracked & Rewound |
| Shell Modifications (`rm`, `mv`, `sed`) | ❌ Untracked (Bypassed) |
| Symlinks & Hard-linked Paths | ❌ Skipped for safety (`skippedLinks`) |
| Conversation History | ℹ️ Preserved (rewinds files ONLY, not transcript) |

---

## Related Knowledge Nodes

- **Concepts**:
  - [SDK File Checkpointing](../concepts/SDK%20File%20Checkpointing.md)
  - [Session Checkpoints](../concepts/Session%20Checkpoints.md)
  - [Agent SDK Architecture](../concepts/Agent%20SDK%20Architecture.md)
  - [Harness Engineering](../concepts/Harness%20Engineering.md)
- **Entities**: [Claude Code](../entities/Claude%20Code.md), [Anthropic](../entities/Anthropic.md).
