---
name: wiki-manage
description: >
  Manage personal memory, career goals, active projects, people, and user
  preferences in mem/. Triggers when the user asks to update project goals, log project
  decisions, record work preferences, update personal identity notes, or track
  people/tasks via /wiki-manage or natural language.
when_to_use: >
  Use whenever user identity, preferences, active project logs, career goals, or collaborator profiles
  need to be created, updated, or tracked in mem/.
argument-hint: "<project|goal|preference|person> <title>"
arguments:
  - name: category
    description: "The memory category: project, goal, preference, or person"
  - name: title
    description: "The title of the memory item"
allowed-tools:
  - run_command
  - read_file
  - write_file
  - edit_file
---

# Wiki Manage Skill

Target Category: `$1` (or `$category`)
Memory Title: `$2` (or `$title`)

You are operating the personal memory layer (`mem/`) of `tluc-wiki`. Your job is to capture, organize, and track personal projects, career goals, work preferences, and decision logs to personalize the Second Brain.

Refer to `examples/manage-project-example.md` for a complete execution walkthrough.

## 1. Memory Subdirectory Structure (`mem/`)

| Category | Path | Purpose | Template Reference |
|----------|------|---------|-------------------|
| **Identity** | `mem/gemini.md` | Core user identity, operating principles, AI persona preferences | `mem/gemini.md` |
| **Preferences** | `mem/preferences/` | Coding habits, workflow preferences, tool settings | `references/memory-management-guide.md` (#4) |
| **Goals** | `mem/goals/` | Short-term and long-term career, technical, and life goals | `references/memory-management-guide.md` (#2) |
| **Projects** | `mem/projects/` | Active personal, work, and engineering projects with decision logs | `references/memory-management-guide.md` (#1) |
| **People** | `mem/people/` | Key collaborators, contacts, team leads, or mentors | `references/memory-management-guide.md` (#3) |
| **History** | `mem/history/` | Historical milestones, project archives | Archival markdown format |

## 2. Manage Pipeline (Route $\rightarrow$ Gather Evidence $\rightarrow$ Confirm Diff $\rightarrow$ Track)

### Step 1 — Route & Classify Input
Verify the target item belongs in `mem/` (not `ctx/rules/`, `wiki/`, or transient chat) using the Memory Surface Routing Table in [memory-management-guide.md](references/memory-management-guide.md); read existing `mem/` files to flag duplicates or conflicts.

### Step 2 — Gather Evidence & Load Schema
Load the target schema from [memory-management-guide.md](references/memory-management-guide.md). For preferences, cite repeated transcript signals (optionally indexed via `python .agents/skills/reflect/scripts/summarize_transcript.py`) or explicit user instructions; keep one-off observations as **Unconfirmed Hypotheses** and exclude secrets or tokens.

### Step 3 — Confirm Diff Before Writing (Human-Gated)
Present proposed additions, updates, removals, and conflicting lines to the user before editing existing `mem/` files, and obtain explicit confirmation (skip waiting only when the user issued an exact scoped write command with zero conflicts).

### Step 4 — Write, Cross-Link, Register & Log
1. Format the page in `mem/<category>/<Name>.md` with YAML frontmatter (`title`, `date`, `tags`, and `status` when applicable).
2. Add Standard Relative Markdown Links to relevant pages in `wiki/concepts/` and `wiki/entities/`.
3. Update `index.md` under `## Personal Memory & Projects (mem/)` and append `## [YYYY-MM-DD] manage | <Memory Item Title>` to `wiki/log.md`.

### Step 5 — Embedded Verification Gate
Run memory hygiene and vault structure checks before finishing:
```powershell
python .agents/skills/wiki-manage/scripts/check_memory.py --strict
python .agents/skills/wiki-lint/scripts/lint_wiki.py
```
Confirm `check_memory.py --strict` reports `0` findings (`status: "ok"`) and `lint_wiki.py` reports `"total_broken_links": 0`.
