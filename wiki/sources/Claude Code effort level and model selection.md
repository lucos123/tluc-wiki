---
title: Claude Code effort level and model selection
date: 2026-07-28
tags:
  - source
  - claude-code
  - model-selection
  - cost-optimization
source: "[[raw/articles/claude-code/claude-code-effort-level-and-model-selection.md]]"
---

# Claude Code effort level and model selection

**Source File**: `raw/articles/claude-code/claude-code-effort-level-and-model-selection.md`
**Original URL**: https://claude.com/blog/claude-model-and-effort-level-in-claude-code
**Author**: Lydia Hallie, Member of Technical Staff, Claude Code team

A technical deep-dive into how [[Claude Code]]'s two primary performance dials — **model selection** and **effort level** — actually work under the hood, and a practical decision framework for when to change each.

## Key Takeaways (verbatim from source)

- Model selection chooses the *set of frozen weights* — the overall capability range. Context can steer, but not change the weights.
- **Effort means more than "thinking time."** It controls how many files Claude reads, how many tools it uses, how many steps it takes before checking back in.
- Choose smaller models for routine tasks; larger for complex or ambiguous ones. Start with default effort and tune as a *general preference* (by domain/work type), not task-by-task.
- Wrong answer with good context? → pick a more capable **model**. Wrong answer by skipping files or bailing mid-refactor? → pick higher **effort**.

## How Model Selection Works (Technical)

When you submit a prompt, Claude Code assembles: message + system prompt + tool definitions + CLAUDE.md + conversation history + any files in context → packed into one API request.

On the server:
1. **Tokenization**: Text split into pieces, each mapped to an integer from a fixed vocabulary trained with the model (`const` → 1978, `await` → 4293, etc.).
2. **Weight-based prediction**: The model runs the token array through billions of numbers organized as matrices (the *weights*). Output is a probability distribution over every token in the vocabulary. Top probability wins. One token at a time.
3. **Autoregressive loop**: A 200-token response = 200 separate passes through the weights. This loop = most wait time and output cost.

**Weights are frozen at inference time.** Nothing in your prompt, CLAUDE.md, or context changes them. Context *steers* predictions for that request — it doesn't *teach* the model. Hallucinations happen when weights produce plausible-looking token sequences from training patterns, not from failed lookups.

**Changing the model = swapping which set of frozen weights handles your request.**

## How Effort Level Works (Technical)

Effort level is sent to the model as part of the request — right alongside the prompt. The model was *trained* to understand how to behave at each effort level. This behavior is baked into the frozen weights. Effort is one more input the model responds to.

**Output token categories — all billed at the same rate:**
| Category | Description |
|----------|-------------|
| **Thinking** | Reasoning streamed before/between actions. Stays in context as input for subsequent steps. |
| **Tool calls** | Structured blocks naming tool + arguments (e.g., `Read`, `Edit`, `Bash`). Claude Code parses and executes these. |
| **Text to you** | Plan, progress updates, summary. |

At higher effort, Claude generates more of all three before reporting done — roughly **7x more tokens** to reach higher confidence answers (per Anthropic's example). The plan created at the start of a high-effort run is not frozen — Claude updates it as it receives results. If step 1 of a 3-hypothesis plan finds the answer, Claude skips steps 2 and 3 explicitly.

**Important**: Claude is trained against "overthinking" — it won't artificially inflate token usage on simple tasks at higher effort settings. Effort = how far Claude is *willing* to travel along the capability curve, not how far it *will* travel.

**Token limits**:
- `max_tokens`: hard cap that truncates mid-stream — blunt instrument, mostly for API developers.
- **Task budgets** and in-prompt guidance ("keep it brief"): softer, advisory controls. Trained behaviour — Claude looks to conclude near the limit rather than hitting a wall.

## The Specialist / Expert / Generalist Framework

| Model | Metaphor | Strength | When to use |
|-------|---------|---------|------------|
| **Claude Fable 5** | Specialist | Rare pattern recognition: "I've seen exactly this before." Finishes jobs Opus/Sonnet cannot reach at any effort level. | Genuinely hard tasks: subtle bugs, unfamiliar domains, architecture. Save it. |
| **Claude Opus 4.8** | Expert | Deep experience; handles ambiguity well. Better than Opus 4.7 at same token count. | Hard-to-ambiguous tasks where you need expertise without Fable's cost. |
| **Claude Sonnet** | Great generalist | Thorough, reads everything, understands *your specific code*. Less "I've seen this" recognition. | Routine, well-scoped, precisely described work. |

**The effort analogy**: Effort decides how much *time* any of these specialists gets with your problem.
- **Opus at low effort** = five minutes with an expert: pattern recognition + quick read, not a careful one.
- **Sonnet at high effort** = afternoon with a generalist: reads everything, runs things, deep familiarity with your specific code.
- **Fable at low effort** = specialist glancing at the problem everyone's stuck on and still spotting the thing no one else would.

## The Diagnostic Heuristic

First check: is context clear? (Prompt quality, right tools, right skills, CLAUDE.md scope.) If increasing effort on a task that *shouldn't* need it, the fix is usually upstream.

If context is clear and Claude still gets it wrong, ask: **did it not *try* hard enough, or did it not *know* enough?**

| Failure mode | Signal | Fix |
|-------------|--------|-----|
| **Didn't know enough** | Right context, clearly tried, still wrong. Confidently wrong. | Upgrade **model** |
| **Didn't try hard enough** | Skipped a file, didn't run tests, bailed mid-refactor | Raise **effort level** |

If on a larger model and work has been routine → drop down (increases speed, reduces cost, no quality loss).

## Model × Effort Cost Interaction

| Task type | Recommendation |
|-----------|---------------|
| Routine, same effort | Use smaller model. Larger model burns extra verification tokens at higher per-token cost for no quality gain. |
| Hard, multi-step | Consider larger model. Smaller model grinds toward its capability limit burning iterations; larger model reaches same quality bar in fewer steps → total cost per task can be *lower* despite higher per-token cost. |
| Genuinely Fable-required | Only Fable can complete it at any effort level. Cost justified. |

The critical insight: effort and model are not substitutes on hard tasks. A smaller model at maximum effort may still fail at what a larger model completes at default effort. The capability ceiling is in the weights.

## Practical Guidance

- **Start with defaults.** Default effort = level where Claude scales token usage to what most people would want to spend on a task.
- **Treat effort as a general preference**, not a task-by-task dial. Set it per domain or per type of work you do.
- **Reach for dials only when something misses**, after checking context quality first.

## Synthesis Notes

This source fills a critical gap in the wiki's [[Claude Code]] coverage: the mechanics of why model and effort behave as they do (weights are frozen; effort is trained-in behavior; tokens are the universal unit). Understanding this directly informs:

- **[[AI Code Migration]]**: The tiered model pattern (Fable for rule-writers/reviewers, Sonnet for implementation fan-out) now has a principled basis. Sonnet at high effort covers your specific codebase thoroughly; Fable is saved for the cross-file pattern recognition that determines whether entire batches get regenerated.
- **[[Verification Loop]]**: Higher effort = more verification steps before reporting done. The Stop hook (one of the 4 gate strengths) interacts with this — Claude at low effort might not self-verify; a Stop hook enforces it regardless.
- **[[Context Engineering]]**: Context steers predictions but doesn't teach the model. CLAUDE.md and skills don't add to weights — they are steering inputs. This reframes the entire [[Persistent Instruction File]] concept: it's pure steering, not training.
- **[[Harness Engineering]]**: The effort system shows that "harness" now includes the model itself as a configurable component — not just the scaffolding around it.

Cross-references: [[Effort Level and Model Selection]], [[Claude Code]], [[Context Engineering]], [[AI Code Migration]], [[Verification Loop]], [[Harness Engineering]].
