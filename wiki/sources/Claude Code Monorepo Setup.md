---
title: Claude Code Monorepo Setup
date: 2026-07-28
tags:
  - source
  - documentation
  - agentic-design
  - claude-code
  - context-engineering
source: "[[raw/cc-mono-and-large-repo.md]]"
---

# Claude Code Monorepo Setup

**Source File**: [[raw/cc-mono-and-large-repo.md]]

Official guide for configuring [[Claude Code]] in monorepos and large single-tree codebases. All techniques address one problem: a large codebase fills the context window with irrelevant content, degrading performance. The solution is to scope Claude to only the code relevant to the current task.

## Key Concepts

- **Starting Directory Determines Scope**: Where you run `claude` controls which files Claude can access, which CLAUDE.md files load at startup, and which `.claude/settings.json` applies.
  | Start from | File access | CLAUDE.md loaded | Use when |
  |------------|------------|-----------------|---------|
  | Repo root | Everything | Root only; subdirs on demand | Tasks span packages |
  | A subdirectory | That subtree | That dir + all ancestors | Work scoped to one package |

- **Hierarchical CLAUDE.md Layering**: Root `CLAUDE.md` holds repo-wide rules (commit conventions, repo layout). Per-package `CLAUDE.md` holds stack-specific rules (test runner, port, migration command). Claude loads both on startup when launched from a subdirectory. Commit all CLAUDE.md files — each directory owner maintains theirs.

- **`claudeMdExcludes` Setting**: Prevents specified CLAUDE.md files from ever loading (even when Claude reads files in that directory). Uses glob patterns against absolute paths. Use `**/` prefix to match anywhere. Best placed in `settings.local.json` for personal exclusions or committed `settings.json` for team-wide. Managed policy CLAUDE.md files cannot be excluded.

- **`Read` Deny Rules**: Block Claude from reading build output, generated code, and vendored dependencies. Add to `permissions.deny`. Committed to `.claude/settings.json` for team-wide enforcement or `.claude/settings.local.json` for personal. Note: gitignored paths (like `node_modules/`, `dist/`) are already excluded from content searches by default.

- **Code Intelligence Plugins**: Install LSP plugins (TypeScript, Python, Go, Rust) via `/plugin install typescript-lsp@claude-plugins-official`. Lets Claude jump to definitions and find references without scanning files. Add to `enabledPlugins` in project settings for team-wide installation.

- **Sparse Worktrees** (`worktree.sparsePaths`): When `--worktree` creates an isolated git worktree, sparse-checkout writes only the listed directories to disk. Faster startup, less disk usage. Lists merge across scopes (local can add paths, not remove). Use `worktree.symlinkDirectories` to symlink `node_modules` instead of duplicating.

- **`additionalDirectories` Setting**: Grants Claude file access to directories outside the working directory (e.g., sibling packages). Relative paths resolve from the starting directory. Does NOT load CLAUDE.md, rules, or skills from added dirs. Use `--add-dir` flag at runtime (which DOES load skills) for one-off access.

- **Per-Directory Skills**: Place `.claude/skills/` inside any package directory. Skills load on demand only when Claude works in that directory. Commit alongside the package code. A `paths:` frontmatter field provides an alternative: one skill in the repo root's `.claude/skills/` activating only for files matching a glob pattern (e.g., `**/migrations/**`).

- **Path-Scoped Rules** (`.claude/rules/*.md`): Alternative to per-directory CLAUDE.md. Rules live centrally in one `.claude/rules/` folder with `paths:` glob to control when they activate. Use when conventions apply to scattered paths or you prefer centralised management.

- **Cross-Package Change Strategy**: For changes spanning multiple packages, keep the entire edit in one session (consistent decisions) and save the plan to a markdown file before editing — compaction summarises conversation history but a saved plan survives.

- **Scaling with Plugins**: When per-directory CLAUDE.md files become hard to govern (drift, staleness, no clear owner), move conventions into plugins. Platform team owns and versions them centrally; per-repo settings reference plugin name. Use `SessionStart` hook to recommend the right plugin when Claude launches in an unfamiliar area.

## Synthesis Notes

This document is the applied implementation of [[Context Engineering]] at the codebase-organisation level. The principle throughout: access to *everything* paradoxically *degrades* performance. The entire configuration system is a series of knobs for reducing what Claude sees.

The distinction between `additionalDirectories` (file access only) and `--add-dir`/`/add-dir` (file access + skills) is subtle but consequential: teams that want consistent skill availability across sibling packages must use `--add-dir`, not the static setting.

The `sparsePaths` + `symlinkDirectories` combination for worktrees is directly relevant to the subagent fan-out patterns in [[Best practices for Claude Code]]: subagents each get a lightweight sparse checkout instead of duplicating the full repo.

Cross-references: [[Claude Code Skills]] for per-directory skills details, [[Claude Code Hooks]] for the `SessionStart` plugin-recommendation hook, [[Persistent Instruction File]] for CLAUDE.md hierarchy, [[Context Engineering]] for the theoretical frame.
