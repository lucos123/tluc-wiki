---
title: Claude Code Hooks
date: 2026-07-28
tags:
  - source
  - documentation
  - agentic-design
  - claude-code
  - harness-engineering
source: "[[raw/cc-hooks.md]]"
---

# Claude Code Hooks

**Source File**: [[raw/cc-hooks.md]]

Official documentation for [[Claude Code]]'s lifecycle hooks system — user-defined shell commands that execute deterministically at specific points in the agent's workflow. Hooks are the primary mechanism for enforcing guaranteed behaviours outside the LLM's judgment.

## Key Concepts

- **Deterministic Control**: Unlike CLAUDE.md instructions (advisory), hooks are guaranteed to run. They enforce code formatting, security guardrails, notifications, and compliance logging regardless of what Claude chooses to do.

- **Full Lifecycle Event Table** (25+ events):
  | Event | When it fires |
  |-------|--------------|
  | `SessionStart` | Session begins or resumes |
  | `UserPromptSubmit` | Prompt submitted, before Claude processes |
  | `PreToolUse` | Before a tool executes — **can block** |
  | `PermissionRequest` | Permission dialog appears |
  | `PostToolUse` | After tool succeeds |
  | `Stop` | Claude finishes responding |
  | `CwdChanged` | Working directory changes (e.g., `cd`) |
  | `FileChanged` | Watched file changes on disk |
  | `ConfigChange` | A settings/skills file changes during session |
  | `PreCompact` / `PostCompact` | Before/after context compaction |
  | `SubagentStart` / `SubagentStop` | Subagent lifecycle |
  | `WorktreeCreate` / `WorktreeRemove` | Worktree lifecycle |
  | `Elicitation` | MCP server requests user input |
  | `SessionEnd`, `Setup`, `StopFailure`, ... | Additional events |

- **Four Hook Types**:
  - `command`: Runs a shell command (default). Communicates via stdin/stdout/stderr and exit codes.
  - `http`: POSTs event JSON to a URL — useful for shared audit services or cloud functions.
  - `prompt`: Single-turn LLM evaluation (Claude Haiku by default). Returns `{"ok": true/false, "reason": "..."}`.
  - `agent`: Multi-turn subagent with tool access — can read files and run commands before deciding. Experimental.

- **Input / Output Protocol**:
  - Input: JSON via stdin (common fields: `session_id`, `cwd`, `hook_event_name`, `tool_name`, `tool_input`).
  - Output: exit code `0` (no objection), exit code `2` (block — write reason to stderr), or structured JSON to stdout for decisions like `permissionDecision: "deny"/"allow"/"ask"`.

- **Matchers & `if` Field**: Matchers filter by event-specific field (e.g., tool name for `PreToolUse`, session source for `SessionStart`). The `if` field (v2.1.85+) adds argument-level filtering: `"Bash(git *)"` runs the hook only when Claude uses git commands. Fails open — runs if command can't be parsed.

- **PermissionRequest Hook**: Returns `{"hookSpecificOutput": {"hookEventName": "PermissionRequest", "decision": {"behavior": "allow"}}}` to auto-approve specific tools (e.g., `ExitPlanMode`) without user dialog.

- **Multiple Hooks Merging**: When multiple hooks match the same event, all run in parallel. For `PreToolUse` permission decisions, most-restrictive answer wins: `deny > defer > ask > allow`. `additionalContext` text is concatenated from all hooks.

- **Hook Scopes**: `~/.claude/settings.json` (global), `.claude/settings.json` (project, committable), `.claude/settings.local.json` (local, gitignored), managed policy settings (org-wide), or directly in skill/agent frontmatter (`hooks:` field).

## Common Use Cases

- **Auto-format after edits**: `PostToolUse` + `Edit|Write` matcher → `jq -r '.tool_input.file_path' | xargs npx prettier --write`
- **Block protected files**: `PreToolUse` + script that checks path and exits 2 for `.env`, `.git/`, etc.
- **Context re-injection after compaction**: `SessionStart` + `compact` matcher → echo project conventions back into Claude's context.
- **Environment variable reload**: `SessionStart` + `CwdChanged` → `direnv export bash > "$CLAUDE_ENV_FILE"` — Claude Code runs this as a shell preamble before each Bash command.
- **Audit configuration changes**: `ConfigChange` → append JSON to audit log.
- **Stop hook verification**: `Stop` hook that runs tests and returns `{"ok": false, "reason": "..."}` if they fail — Claude keeps working until tests pass (cap: 8 consecutive blocks).
- **Desktop notification**: `Notification` event → `osascript`/`notify-send`/PowerShell when Claude needs input.

## Synthesis Notes

Hooks are the "scaffolding" in `Agent = Model + Harness`. While [[Claude Code Skills]] give Claude modular capabilities it *can* invoke, hooks provide deterministic guarantees about what the system *must* do — regardless of the model's choices. This dual design allows high autonomy while remaining bounded by security policy.

The `prompt` and `agent` hook types are notable: they create a meta-layer where one Claude model (Haiku) reviews or verifies the actions of the primary Claude session. This is the programmatic form of the adversarial review pattern documented in [[Best practices for Claude Code]].

`PreToolUse` hooks enforce policy that users *cannot bypass* even in `bypassPermissions` mode — making hooks the ultimate security primitive in the Claude Code architecture.

The `CwdChanged` + `CLAUDE_ENV_FILE` pattern elegantly solves a subtle problem: Claude's Bash tool doesn't inherit shell environment changes mid-session, but hooks can inject environment state before each command.
