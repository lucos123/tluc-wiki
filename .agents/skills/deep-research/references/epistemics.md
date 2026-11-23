# Epistemics & Evidence Vetting Reference

Standards for reasoning under fragmentary, historical, or conflicting evidence without flattening uncertainty into false certainty.

---

## 1. Claims About Human Decisions

- Locate the person's original attributable words whenever a human ruling sets scope (commit message, issue thread, design doc, raw transcript, or chat log).
- Quote the original words verbatim with a source pointer; label any summary or interpretation as an **Inferred** interpretation.
- Never extrapolate a scoped instruction (e.g., `"avoid endpoint X during migration"`) into a permanent blanket ban unless the original source states it.

## 2. Five Confidence Tiers

Every substantive claim belongs to one tier, and its phrasing must match that tier:

| Tier | Criteria | Required Phrasing & Citation |
| :--- | :--- | :--- |
| **Direct** | Explicit textual statement in a primary source (`raw/`, official doc, code, log) directly proves the claim | Confident, directly cited in the same sentence (`[Source](...)` or `` `file:line` ``) |
| **Supported** | Multiple independent pieces of indirect evidence converge on one conclusion | Confident derivation citing each converging source |
| **Inferred** | Logical deduction or reading beyond what sources explicitly state | Hedged with explicit chain (`"Given A and B, C appears likely because D."`) |
| **Speculative** | Plausible hypothesis on thin evidence where other explanations fit equally well | Explicit hypothesis marker (`"One possibility is X, though direct evidence is missing."`) |
| **Unknown** | Investigated concrete sources and found no answer | Concrete gap statement naming every source and search run |

## 3. Phrasing Discipline

- **Citation Words** (`"because"`, `"was designed to"`, `"the team decided"`): valid **only** for `Direct` or `Supported` claims with an adjacent source.
- **Inference Hedges** (`"appears to"`, `"suggests"`, `"is consistent with"`, `"likely"`): required for `Inferred` and `Speculative` claims.
- **Avoid Certainty Weasels**: Never write `"obviously"`, `"clearly"`, `"of course"`, `"undoubtedly"`, `"I think"`, `"I believe"`, `"hiển nhiên là"`, `"rõ ràng là"`, `"tất nhiên là"`, `"tôi nghĩ rằng"`, or `"tôi tin rằng"`.

## 4. Anti-Rationalization & The Sycophancy Trap

- **Do not retrofit clean rationales** onto messy history — existing patterns may be legacy accidents or copy-paste.
- **Do not confirm user-embedded hypotheses** automatically (e.g., *"Is X slow because of locking?"*). Test locking alongside competing explanations independently.
- **Surface contradictions directly**: Present conflicting sources side-by-side instead of smoothing them into a single tidy story.

## 5. Benchmark & Number Vetting

Before quoting a speedup, latency, throughput, or eval metric in a research brief:
1. Identify the limiting bottleneck claimed (CPU, I/O, network, memory bandwidth, cache state).
2. Confirm end-to-end workload equivalence (avoid extrapolating microbenchmarks to full pipelines).
3. Prefer median and spread across repeated runs over single best-case numbers.
4. Label every figure inline with its provenance (`measured` + source, `inferred`, or `estimate`).

## 6. Pre-Send Audit

- Every `[Direct]` claim carries an adjacent citation or moves down to `Inferred` / `Speculative`.
- Zero certainty weasel words survive outside verbatim blockquotes.
- A concrete **What Remains Unknown** section lists every open gap explicitly.
