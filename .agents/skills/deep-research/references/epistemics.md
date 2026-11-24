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

Run this checklist before reporting, citing, or acting on any measured speedup, regression, latency, throughput, cost delta, or eval score. Do not block prose discussions on this gate when no measurement is claimed; label unmeasured figures explicitly as `estimate` or `unmeasured`.

1. **Name the limiter**: State what constrains the metric before measuring (`CPU`, `lock contention`, `I/O`, `allocator`, `network`, `cold cache`, or the harness). Mark deltas lacking a plausible limiter as `unexplained` (likely noise).
2. **Measure the work claimed**: Match inputs, data shape, and scale to the stated claim. State `cold` vs `warm` cache state and confirm end-to-end coverage; microbenchmarks do not prove system-level speedup.
3. **Repeat and report variance**: Run `>= 5` repetitions (more in noisy environments) and report median plus spread instead of a single best run. If the delta sits inside run-to-run variance, report `"no measurable change"`.
4. **Rule out the observer**: Verify timers, profilers, and counters recorded real work (named function/span, moved counters, real exit codes, and non-truncated output).
5. **Report with inline provenance**: Keep value, provenance label (`measured`, `inferred`, or `estimate`), machine/build/scale context, and source citation in the same sentence; archive raw outputs in `raw/` or `output/` when decisions depend on them.

**Verdict Gate**: Only figures passing all five checks enter `output/reports/`, `wiki/analyses/`, or architecture decisions; otherwise downgrade the claim to what was actually established.

## 6. Pre-Send Audit

- Every `[Direct]` claim carries an adjacent citation or moves down to `Inferred` / `Speculative`.
- Zero certainty weasel words survive outside verbatim blockquotes.
- A concrete **What Remains Unknown** section lists every open gap explicitly.
