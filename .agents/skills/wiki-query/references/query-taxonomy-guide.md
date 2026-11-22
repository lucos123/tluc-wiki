# Query Taxonomy & Formatting Guide

This guide details the 5 Question Types and their respective synthesis strategies, output formats, and citation protocols.

---

## 1. Factual Lookup Query

- **Objective**: Retrieve direct facts, parameters, or specifications for a specific entity or concept.
- **Search Scope**: Search `index.md` $\rightarrow$ Read targeted page in `wiki/entities/` or `wiki/concepts/`.
- **Output Format**:
  - Direct 1-2 sentence answer.
  - Bulleted list of specifications.
  - Citation format: `According to [Page Name](wiki/concepts/Page%20Name.md), ...`

---

## 2. Comparative Query

- **Objective**: Compare two or more models, frameworks, architectures, or tools.
- **Search Scope**: Read all pages being compared $\rightarrow$ Extract side-by-side metrics.
- **Output Format**:
  - Structured Comparison Table (Metrics / Features / Trade-offs).
  - Analytical breakdown of key differentiators.
  - Side-by-side citations: `[Entity A](wiki/entities/Entity%20A.md) features X, while [Entity B](wiki/entities/Entity%20B.md) features Y.`

---

## 3. Analytical & Architectural Query

- **Objective**: Provide deep synthesis across multiple domain topics, trade-off evaluation, or system design decisions.
- **Search Scope**: Multi-page scan across `wiki/concepts/`, `wiki/entities/`, and `raw/`.
- **Output Format**:
  - Executive Thesis / Core Takeaways.
  - Deep-dive sections with clear headers.
  - Mermaid Architecture or Flow Diagram (if applicable).
  - Explicit trade-off matrix.

---

## 4. Gap-Finding Query

- **Objective**: Identify what information is covered versus what is missing from the Second Brain.
- **Search Scope**: Broad `index.md` and `grep_search` across `wiki/`.
- **Output Format**:
  - Summary of covered aspects (with citations).
  - List of missing topics / undocumented areas.
  - Recommended next ingests (URL/Paper suggestions).

---

## 5. Exploratory Query

- **Objective**: Map relationships, dependencies, and connections across concepts.
- **Search Scope**: Trace Markdown cross-links (`[...](...)`) across multiple pages.
- **Output Format**:
  - Concept Graph Overview.
  - Section-by-section breakdown of linked nodes.
