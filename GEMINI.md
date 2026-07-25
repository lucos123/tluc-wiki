# LLM Wiki Schema

This document defines the rules, structure, and operations for maintaining this knowledge base. I (the LLM) must strictly adhere to these guidelines for all interactions within this workspace.

## 1. Directory Structure

```
tluc-wiki/
├── GEMINI.md              # This file — the schema and rules
├── index.md               # Content catalog of the wiki
├── raw/                   # 🔒 Immutable source of truth
│   ├── *.md               #    Curated source documents (articles, notes, papers)
│   └── assets/            #    Downloaded images and attachments
├── wiki/                  # 📝 LLM-maintained knowledge base (full read/write)
│   ├── log.md             #    Chronological, append-only record of operations
│   ├── analyses/          #    Cross-source syntheses and comparisons
│   ├── concepts/          #    Ideas, patterns, methodologies, frameworks
│   ├── entities/          #    Named tools, products, organizations, people
│   └── sources/           #    Summaries of ingested raw documents
└── .agents/skills/        # 🔧 Agent skills for wiki operations
    ├── wiki-ingest/       #    Skill for ingesting new source documents
    ├── wiki-query/        #    Skill for answering questions from the wiki
    └── wiki-lint/         #    Skill for health-checking the wiki
```

### Ownership Rules
- **`raw/`**: Immutable. I will NEVER modify files here.
- **`wiki/`**: I have full read/write ownership of this directory.
- **`index.md`**: I maintain this as the content catalog.

## 2. Page Conventions

All markdown pages in `wiki/` must follow these rules:
1. **Frontmatter**: Each page must begin with YAML frontmatter containing:
   - `title`: The title of the page
   - `date`: Date of creation/last update (YYYY-MM-DD)
   - `tags`: List of relevant tags
   - `source`: Links to raw sources if applicable
2. **Cross-referencing**: Actively use Obsidian-style wiki links (`[[Page Name]]`) to connect concepts, entities, and sources.
3. **Synthesis over duplication**: Synthesize information. Note contradictions or evolving claims clearly.

## 3. Operations

Each operation has a corresponding agent skill in `.agents/skills/` with detailed instructions. The skills are loaded on-demand when the operation is triggered.

### A. Ingest
When the user asks me to ingest a new source:
1. **Read**: Read the source document from `raw/` (or the provided file).
2. **Discuss (Optional)**: Discuss key takeaways with the user if they wish.
3. **Create/Update Wiki Pages**: 
   - Create a summary page in `wiki/sources/`.
   - Update existing entity or concept pages (in `wiki/entities/` or `wiki/concepts/`) with the new information.
4. **Update `index.md`**: Add or update entries for the touched wiki pages.
5. **Update `wiki/log.md`**: Append an entry: `## [YYYY-MM-DD] ingest | <Source Title>`

### B. Query
When the user asks a question:
1. **Search**: Read `index.md` to find relevant pages, then read those pages.
2. **Synthesize**: Answer the question using citations to the wiki.
3. **Compound**: If the answer is valuable (e.g., a new comparison, analysis), propose filing it back as a new page in `wiki/analyses/` or `wiki/concepts/`.
4. **Update `wiki/log.md`**: Append an entry: `## [YYYY-MM-DD] query | <Short description>`

### C. Lint
When the user asks for a health check:
1. **Analyze**: Scan `index.md` and `wiki/` pages for contradictions, stale claims, orphan pages, or missing cross-references.
2. **Report**: Suggest fixes, new questions to investigate, or missing sources.
3. **Update `wiki/log.md`**: Append an entry: `## [YYYY-MM-DD] lint | <Short description>`
