---
name: diagram
description: >
  Create load-bearing visual explanations (pseudocode, call trees, file/component trees,
  Mermaid diagrams, structural diffs, or generative UI escalations) in chat, wiki/concepts/,
  or output/visuals/. Triggers when the user asks to draw a diagram, visualize an architecture,
  workflow, sequence, or state machine, or explain complex structural relationships clearly.
argument-hint: "<concept | architecture | flow | path-to-file>"
allowed-tools:
  - read_file
  - write_file
  - edit_file
  - run_command
metadata:
  credits:
    diagram-skill: pstack
    adapted-from: oh-my-claudecode (diagram)
---

# Diagram

**Diagrams are load-bearing, not decoration.** Add a visual only when prose forces the reader to hold a topology, flow, or boundary in working memory at once — then choose the smallest view that carries the shape. If one sentence answers honestly, write the sentence instead.

## 1. View Selection Matrix

Pick **one** view (two at most); more creates decoding noise. Copyable templates for every view live in [visual-vocabulary.md](./references/visual-vocabulary.md).

| Question Shape | Smallest View | When to Prefer |
| :--- | :--- | :--- |
| Branching conditions or locking logic | **Pseudocode** | Control flow without language boilerplate |
| Runtime execution or script pipeline | **Call tree** | Call depth and failure edges matter |
| Module boundaries or skill ownership | **Component / File tree** | Folder layout or UI hierarchy needs 1-line roles |
| Multi-party protocol, dataflow, states, metrics | **Mermaid** | Interactions, pipelines, or state transitions |
| Structural edit on existing layout or flow | **Structural Diff** | Before/after shape is clearer than full repetition |
| Atomic non-elidable unit | **Complete block** | Summarizing would hide ownership or execution order |

## 2. Antigravity & `tluc-wiki` Mermaid Rules

1. **Allowed diagram headers only**: `flowchart` (`TD`/`LR`/`BT`/`RL`), `graph` (`TD`/`LR`/`BT`/`RL`), `sequenceDiagram`, `stateDiagram-v2`, `stateDiagram`, `classDiagram`, `erDiagram`, `xychart-beta`. For timelines, roadmaps, or schedules, use `flowchart LR` / `flowchart TD` or a Markdown table — never `gantt`, `mindmap`, `timeline`, or `pie`.
2. **Quote special-character labels**: Quote `flowchart` and `graph` node labels containing parentheses, brackets, or colons as `id["Label (Extra Info)"]`, never unquoted `id[Label (Extra Info)]`.
3. **No HTML tags inside labels**: Avoid `<br>`, `<b>`, or `<span>` tags inside Mermaid text so Obsidian, GitHub, and IDE previews render consistently.
4. **Stay lean**: Keep each Mermaid block at `<= 45` content lines; split larger topologies into focused sub-diagrams or escalate.

## 3. Escalation & Storage Paths

- **3D Biomolecular Structures**: Follow Science Visualization Priority Rules and load interactive 3D viewers via the `biomolecular-structure-viewer` sidecar rather than static diagrams.
- **Dense UI, Interactive Charts, Side-by-Side Explorers**: Escalate to Antigravity's built-in `generative_ui` skill (HTML artifact with Tailwind CSS + `--foreground`/`--card` semantic tokens; `<agent-embed>` inline when `<= 450px` tall or standalone artifact when taller).
- **Persistent Diagrams in `tluc-wiki`**: Embed directly in `wiki/concepts/<Concept>.md` or save standalone artifacts to `output/visuals/<Title>.md` (with YAML `tags: [output, visual, ...]` and `type: visual`, registered in `index.md` and `wiki/log.md`).
- **Inline Discipline**: Place each visual right beside the 2–3 sentences it explains and prune every node that does not directly answer the question.

## 4. Deterministic Verification Gate

Validate authored Mermaid blocks against Antigravity & `tluc-wiki` syntax rules with [check_diagrams.py](./scripts/check_diagrams.py):

```powershell
python .agents/skills/diagram/scripts/check_diagrams.py "<target-file>" --strict
```

To audit every Mermaid block across `wiki/`, `mem/`, and `output/` at once:

```powershell
python .agents/skills/diagram/scripts/check_diagrams.py --vault --strict
```
