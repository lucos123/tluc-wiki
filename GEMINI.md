# Second Brain Architecture & LLM Wiki Schema

This document defines the rules, structure, and operational pipelines for maintaining `tluc-wiki` as a persistent **Personal & Engineering Second Brain System**. I (the LLM) must strictly adhere to these guidelines across all interactions.

---

## 1. Directory Structure & Architecture

```
tluc-wiki/
├── GEMINI.md              # This file — schema, rules, and architecture specs
├── index.md               # Master content catalog of the Second Brain
├── raw/                   # 🔒 Immutable source of truth (Ground truth inputs)
│   ├── articles/          #    Web articles, clippings, and text sources
│   ├── pdfs/              #    PDF books, whitepapers, and documentation
│   ├── screenshots/       #    Visual diagrams and image assets
│   ├── video-transcripts/ #    Auto-extracted YouTube & media transcripts
│   ├── notes/             #    User drafts, scratch notes, and voice transcripts
│   └── assets/            #    Embedded attachments and media files
├── wiki/                  # 📝 LLM-maintained evergreen knowledge base
│   ├── log.md             #    Chronological append-only record of all operations
│   ├── analyses/          #    Cross-source syntheses, comparisons, and evaluations
│   ├── concepts/          #    Core ideas, patterns, frameworks, and methodologies
│   ├── entities/          #    Tools, platforms, organizations, products, people
│   └── sources/           #    Summaries of ingested raw source documents
├── output/                # 📤 Generated shareable artifacts & deliverables
│   ├── reports/           #    In-depth research reports and technical analyses
│   ├── documents/         #    Markdown documents, specifications, and whitepapers
│   ├── summaries/         #    Executive summaries and digest notes
│   ├── posts/             #    Blog posts, articles, and presentations
│   └── visuals/           #    Mermaid diagrams, mockups, and exported media
├── ctx/                   # ⚙️ Context & interaction primitives
│   ├── templates/         #    Standardized document templates
│   ├── prompts/           #    Re-usable system prompts and workflows
│   ├── rules/             #    Domain-specific guidelines and constraints
│   └── snippets/          #    Code snippets and helper routines
├── mem/                   # 🧠 Identity, preferences, and personal memory
│   ├── gemini.md          #    User identity, work style, preferences, and AI persona
│   ├── preferences/       #    Detailed workflow & coding preferences
│   ├── goals/             #    Career, technical, and life goals
│   ├── projects/          #    Active personal & engineering projects
│   └── history/           #    Historical milestones and project decision logs
└── .agents/skills/        # 🔧 Agent skills for Second Brain operations
    ├── wiki-ingest/       #    Skill for ingesting raw sources into structured knowledge
    ├── wiki-write/        #    Skill for synthesizing and producing deliverables in output/
    ├── wiki-manage/       #    Skill for tracking projects, goals, and identity in mem/
    ├── wiki-query/        #    Skill for searching, synthesizing, and compounding answers
    ├── wiki-lint/         #    Skill for health-checking link integrity & index coverage
    └── dental-consult-ops/#    Skill for dental consultation operations & TVV training (Nha Khoa 3C)
```

---

## 2. Ownership Rules

- **`raw/`**: Immutable ground truth. I will NEVER modify or edit original files here once saved.
- **`wiki/`**: Full read/write ownership. Evergreen, connected knowledge base.
- **`output/`**: Full read/write ownership. Shareable outputs generated for the user.
- **`ctx/`**: Read/write. Reusable prompt templates, rules, and workflow snippets.
- **`mem/`**: Read/write (collaborative). Stores user identity, career/project goals, and preferences.
- **`index.md`**: Maintained continuously as the catalog for `wiki/`, `mem/`, and `output/`.

### Subdirectory Boundary & Separation Rules
- **`wiki/entities/` vs `mem/people/`**: `wiki/entities/` contains objective public technical entities, tools, platforms, and public figures. `mem/people/` is reserved strictly for personal network contacts and private team members.
- **`wiki/references/` vs `mem/preferences/` vs `ctx/rules/`**: `wiki/references/` contains objective technical cheatsheets and syntax references. `ctx/rules/` contains AI operational constraints. `mem/preferences/` contains user AI interaction style and workflow preferences.

---

## 3. Page Conventions

All markdown pages across `wiki/`, `output/`, and `mem/` must follow these rules:
1. **YAML Frontmatter**: Each page must begin with YAML frontmatter containing:
   - `title`: Descriptive title of the page
   - `date`: YYYY-MM-DD
   - `tags`: Relevant tags (e.g. `concept`, `entity`, `source`, `project`, `goal`, `output`)
   - `source`: Links to raw sources or parent notes if applicable
2. **Cross-Referencing**: Actively use Obsidian-style wiki links (`[[Page Name]]`) to connect concepts, entities, projects, and sources.
3. **Synthesis & Compounding**: Synthesize information over mere duplication. Preserve contradictions, trade-offs, and evolving insights clearly.

---

## 4. Operational Pipelines

```
Source ──> Knowledge (Wiki) ──> Context (Ctx) ──> Output ──> Memory (Mem) ──> Re-compounds
```

### A. Ingest Pipeline (Capture $\rightarrow$ Extract $\rightarrow$ Add to Wiki)
- Read raw input from `raw/<category>/`.
- Extract key concepts, entities, and takeaways.
- Create source summary in `wiki/sources/` and create/update entity & concept pages in `wiki/entities/` and `wiki/concepts/`.
- Update `index.md` and append log to `wiki/log.md`.

### B. Write Pipeline (Retrieve $\rightarrow$ Draft $\rightarrow$ Refine $\rightarrow$ Output)
- Search `index.md` and `wiki/` for relevant context.
- Synthesize comprehensive deliverables (reports, guides, code artifacts).
- Save completed deliverables to `output/<category>/`.
- Link deliverables in `index.md` and `wiki/log.md`.

### C. Manage Pipeline (Decisions $\rightarrow$ Link Context $\rightarrow$ Track)
- Track active projects and goals in `mem/projects/` and `mem/goals/`.
- Cross-reference technical wiki concepts with personal project goals.

### D. Review & Compound Pipeline (Summarize $\rightarrow$ Reflect $\rightarrow$ Update)
- Periodically review past outputs and project logs.
- Compound valuable insights into permanent wiki pages.

### E. Maintain Pipeline (Prune $\rightarrow$ Dedupe $\rightarrow$ Improve Links)
- Execute `wiki-lint` health check to audit broken links, orphan pages, tag typos, and index coverage.
