---
title: "SDK File Checkpointing"
date: 2026-08-10
tags:
  - concept
  - agent-sdk
  - state-management
  - harness-engineering
  - claude-code
source: "[[Rewind file changes with checkpointing]]"
---

# SDK File Checkpointing

**SDK File Checkpointing** is a programmatic file restoration mechanism in the [[Agent SDK Architecture|Claude Agent SDK]] (`enable_file_checkpointing=True`) that creates local backups of modified files before `Write`, `Edit`, or `NotebookEdit` execution.

---

## Architectural Topography

```mermaid
graph TD
    SDKPrompt["User Prompt (extraArgs: replay-user-messages)"] --> UUIDStream["Emit Checkpoint UUID (message.uuid)"]
    UUIDStream --> FileMod["Agent Executes Write/Edit Tools"]
    FileMod --> BackupStore["Local File Backup Snapshot"]
    BackupStore -- "rewind_files(checkpoint_id)" --> DiskRestore["Restore On-Disk Files (Deletes New Files / Restores Edits)"]
    DiskRestore --> Transcript["Conversation Context Stays Intact!"]
```

## Key Characteristics

1. **Context Preservation**: Unlike CLI `/rewind` (which can rewind both context and files), SDK `rewind_files()` restores disk files while leaving the conversation context completely intact for continuous debugging.
2. **Safety Exclusions**: Automatically skips symlinks, hard links, and non-regular paths, reporting skipped counts via `skippedLinks`.

See [[Rewind file changes with checkpointing]], [[Session Checkpoints]], and [[Agent SDK Architecture]].
