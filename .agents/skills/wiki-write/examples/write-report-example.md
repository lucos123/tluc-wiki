# Write Report Execution Example

This example demonstrates a complete end-to-end execution of the `wiki-write` skill.

---

## Input Command
```
/wiki-write report "GPT-5.6 Sol vs Claude 3.7 Sonnet Inference Benchmarks"
```

---

## Execution Output

Saved to `output/reports/GPT-5.6 Sol vs Claude 3.7 Sonnet Inference Benchmarks.md`:

```markdown
---
title: "GPT-5.6 Sol vs Claude 3.7 Sonnet Inference Benchmarks"
date: 2026-08-02
tags:
  - output
  - report
  - ai-models
type: report
---

# GPT-5.6 Sol vs Claude 3.7 Sonnet Inference Benchmarks

## Executive Summary

Comparison of [GPT-5.6 Sol](../../wiki/sources/GPT-5.6%20Sol%20Model%20API%20Reference.md) and [Claude Code](../../wiki/entities/Claude%20Code.md) models across token efficiency, context window (1.05M tokens), and multi-agent coordination (`ultra` subagent mode).

## Key Metric Comparison

| Dimension | GPT-5.6 Sol | Claude 3.7 Sonnet |
|-----------|-------------|-------------------|
| Uncached Input | $5.00 / 1M | $3.00 / 1M |
| Cached Input | $0.50 / 1M | $0.30 / 1M |
| Output | $30.00 / 1M | $15.00 / 1M |
```
