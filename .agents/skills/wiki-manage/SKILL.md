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
  - view_file
  - write_to_file
  - replace_file_content
  - grep_search
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
| **Preferences** | `mem/preferences/` | Coding habits, workflow preferences, tool settings | `references/memory-management-guide.md` |
| **Goals** | `mem/goals/` | Short-term and long-term career, technical, and life goals | `references/memory-management-guide.md` (#2) |
| **Projects** | `mem/projects/` | Active personal, work, and engineering projects with decision logs | `references/memory-management-guide.md` (#1) |
| **People** | `mem/people/` | Key collaborators, contacts, team leads, or mentors | `references/memory-management-guide.md` (#3) |
| **History** | `mem/history/` | Historical milestones, project archives | Archival markdown format |

## 2. Manage Pipeline (Decisions $\rightarrow$ Link Context $\rightarrow$ Track)

### Step 1 — Capture Input
Read the user's project update, decision log, goal adjustment, or preference change.

### Step 2 — Create or Update Memory Page
1. Load schema from `references/memory-management-guide.md`.
2. Format page in `mem/<category>/<Name>.md` with frontmatter (`title`, `date`, `tags`, `status`).
3. **Automated Cross-Linking**: Search `wiki/concepts/` and `wiki/entities/` to cross-reference relevant technical concepts using Standard Relative Markdown Links (`[Concept Name](../../wiki/concepts/Concept%20Name.md)` or `[Entity Name](../../wiki/entities/Entity%20Name.md)`).

### Step 3 — Register & Log
1. Update `index.md` under `## Personal Memory & Projects (mem/)`.
2. Append log entry to `wiki/log.md`: `## [YYYY-MM-DD] manage | <Memory Item Title>`

### Step 4 — Embedded Verification Gate
Run structural health check to confirm memory items are correctly indexed and cross-linked:
```powershell
python .agents/skills/wiki-lint/scripts/lint_wiki.py
```
Confirm `"total_broken_links": 0` before finishing.
