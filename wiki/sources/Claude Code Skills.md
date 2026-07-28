---
title: Claude Code Skills
date: 2026-07-28
tags:
  - source
  - documentation
  - agentic-design
  - claude-code
  - harness-engineering
source: "[[raw/cc-skills.md]]"
---

# Claude Code Skills

**Source File**: [[raw/cc-skills.md]]

Official documentation for [[Claude Code]]'s skills system — the mechanism for extending Claude with modular, on-demand capabilities. Skills implement the open [Agent Skills standard](https://agentskills.io) and replace the older `.claude/commands/` approach.

## Key Concepts

- **Skill vs. CLAUDE.md**: CLAUDE.md is always loaded (every token, every session). A skill's body only loads when the skill is invoked — making skills the correct place for long reference docs, multi-step procedures, or task-specific instructions that would otherwise bloat the context window.

- **Structure**: Each skill is a directory with a required `SKILL.md` and optional supporting files (`examples/`, `scripts/`, `references/`, templates). The directory name becomes the `/command` name.

- **Bundled Skills**: Claude Code ships built-in skills available in every session (unless `disableBundledSkills` is set):
  - `/run`: Launch & drive the app to see a change working.
  - `/verify`: Build & run to confirm a change, without falling back to tests.
  - `/run-skill-generator`: Records the project's build/launch recipe as a skill for `/run` and `/verify` to follow.
  - `/code-review`, `/batch`, `/debug`, `/loop`, `/claude-api`.

- **Full Frontmatter Reference**:
  | Field | Purpose |
  |-------|---------|
  | `description` | (Recommended) When Claude auto-invokes the skill. Truncated at 1,536 chars in listing. |
  | `when_to_use` | Additional trigger context. Appended to `description`. |
  | `disable-model-invocation: true` | Only the user can invoke (manual workflows with side effects). |
  | `user-invocable: false` | Only Claude can invoke (background reference knowledge). |
  | `allowed-tools` | Pre-approved tools while skill is active (no per-use prompt). |
  | `disallowed-tools` | Tools removed from Claude's pool while skill is active. Cleared after next prompt. |
  | `context: fork` | Run in an isolated subagent context. |
  | `agent` | Which agent type to use when `context: fork` (e.g., `Explore`, `Plan`, custom). |
  | `paths` | Glob patterns — skill auto-activates only when working on matching files. |
  | `hooks` | Hooks scoped to this skill's lifecycle. |
  | `model` | Override the model for this skill's duration. |
  | `effort` | Override effort level (`low`, `medium`, `high`, `xhigh`, `max`). |
  | `shell` | `bash` (default) or `powershell` for `!`command`` injection. |
  | `argument-hint` | Hint shown in autocomplete. |
  | `arguments` | Named positional arguments for `$name` substitution. |

- **Dynamic Context Injection**: `` !`command` `` at line start runs shell commands before Claude sees the prompt. Output replaces the placeholder. Also supports fenced ` ```! ``` ` blocks for multi-line commands. Runs once at invocation — output is plain text, not re-processed.

- **String Substitutions**: `$ARGUMENTS`, `$ARGUMENTS[N]`/`$N`, `$name` (from `arguments` list), `${CLAUDE_SESSION_ID}`, `${CLAUDE_EFFORT}`, `${CLAUDE_SKILL_DIR}`.

- **Subagent Execution** (`context: fork`): Skill content becomes the subagent's prompt. The forked agent runs in isolation (no conversation history access). Built-in agents: `Explore` (read-only, no CLAUDE.md), `Plan`, `general-purpose`.

- **Skill Scopes and Precedence**: Enterprise > Personal (`~/.claude/skills/`) > Project (`.claude/skills/`) > Bundled. Plugin skills use `plugin-name:skill-name` namespace to avoid collisions.

- **Live Change Detection**: Editing a SKILL.md takes effect in the current session without restart. Creating a new top-level skills directory requires restart.

- **Invocation Control Table**:
  | Frontmatter | User invoke | Claude invoke | Context loading |
  |-------------|------------|--------------|----------------|
  | (default) | Yes | Yes | Description always in context |
  | `disable-model-invocation: true` | Yes | No | Description NOT in context |
  | `user-invocable: false` | No | Yes | Description always in context |

- **`skillOverrides` Setting**: Control skill visibility from settings (without editing SKILL.md). States: `on`, `name-only`, `user-invocable-only`, `off`. The `/skills` menu writes this interactively.

- **Skill Content Lifecycle**: Invoked skill content enters conversation as one message and stays for the session. Auto-compaction carries forward the most recent invocation of each skill (up to first 5,000 tokens, shared 25,000-token budget across all skills). Re-invoke after compaction if a skill stops influencing behavior.

## Synthesis Notes

The shift from `.claude/commands/` (flat files) to `.claude/skills/` (directories with supporting assets) mirrors the evolution from CLAUDE.md monoliths to modular harnesses described in [[Harness Engineering]]. The addition of `paths:` activation (file-glob-based auto-loading) and `context: fork` (subagent execution) makes skills a complete unit of encapsulation: they carry their own knowledge, their own tool permissions, their own execution context, and their own activation criteria.

The `disable-model-invocation: true` pattern is particularly important: it draws a sharp line between *automation* (Claude-driven) and *control* (user-driven), ensuring that high-impact workflows like `/deploy` require explicit human intent.

The `disallowed-tools` field enables safe background loops (e.g., prevent `AskUserQuestion` so the agent doesn't block on input mid-automation).

Cross-references: [[Claude Code Hooks]] for the deterministic complement to skills, [[Best practices for Claude Code]] for when to use skills vs. CLAUDE.md, [[Claude Code Monorepo Setup]] for per-directory scoping.
