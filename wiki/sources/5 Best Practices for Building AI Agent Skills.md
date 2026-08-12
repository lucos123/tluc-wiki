---
title: "5 Best Practices for Building AI Agent Skills"
date: 2026-08-12
tags:
  - source
  - agent-skills
  - harness-engineering
  - best-practices
  - video-transcript
source: "[[raw/video-transcripts/5-best-practices-for-building-ai-agent-skills.md]]"
url: "https://www.youtube.com/watch?v=qYNs80FKIVc"
channel: "IBM Technology"
duration: "13m 22s"
---

# 5 Best Practices for Building AI Agent Skills

**URL**: https://www.youtube.com/watch?v=qYNs80FKIVc  
**Channel**: [[IBM Technology]]  
**Source File**: [[raw/video-transcripts/5-best-practices-for-building-ai-agent-skills.md]]  

---

## Executive Summary

In this 13-minute video by [[IBM Technology]], experts break down the **5 Best Practices for Building AI Agent Skills** based on the Open Agent Skills Standard (`agentskills.io`).

Agent skills deliver procedural domain knowledge to LLM agents via `SKILL.md` files. Because skills combine markdown guidance with executable code scripts and file system access, adhering to structural boundaries, progressive disclosure, deterministic scripting, and security auditing is critical to avoid generic output, context bloat, and malware vulnerabilities.

---

## The 5 Core Best Practices

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    5 Best Practices for AI Agent Skills                     │
├─────────────────────────────────────────────────────────────────────────────┤
│ 1. Description is the Trigger : Write pushy, specific YAML descriptions.     │
│ 2. Build from Real Expertise  : Use gotchas & artifacts; avoid LLM mush.   │
│ 3. Spend Context Wisely      : Keep SKILL.md <500 lines; use references/.   │
│ 4. Deterministic Scripts     : Use scripts/ for fragile steps (math, code). │
│ 5. Vet Skills Before Running : Audit 3rd-party skills for security/malware. │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 1. The Description is the Trigger (YAML Frontmatter)
- Startup behavior: Agents load **only** the `name` (max 64 chars) and `description` (max 1,024 chars) into initial context to save tokens.
- **Pushy Description Rule**: LLMs tend to under-trigger skills. Descriptions must explicitly state *what* the skill does and *when* the agent should execute it, leaning slightly "pushy" to ensure trigger reliability.

### 2. Build from Real Expertise (Avoid LLM-Generated Mush)
- Avoid generating skills via LLMs (produces generic filler like "validate inputs properly").
- Build content from real domain artifacts (runbooks, PR feedback, actual task walk-throughs).
- **Gotchas Section**: The highest value component of any `SKILL.md` is environment-specific gotchas that defy standard model assumptions.
- **Simon Willison's Axiom**: *"Bring the domain expertise, let the agent do the typing."*

### 3. Spend Context Wisely (Progressive Disclosure & 500-Line Rule)
- Limit `SKILL.md` body to **<500 lines (~5,000 tokens)**.
- Apply **Progressive Disclosure**: Offload detailed reference manuals, schemas, and long docs to a `references/` subdirectory. The agent reads `references/` files strictly on-demand.

### 4. Use Deterministic Scripts (Code for Fragile Steps)
- Match step fragility to execution mode:
  - **Loose steps**: Write markdown text instructions (allow LLM improvisation).
  - **Fragile steps**: Write deterministic code scripts in `scripts/` (e.g. math calculations, file transforms).
- Benefits: Running scripts in `scripts/` avoids LLM math/logic hallucinations AND saves context window tokens (script body isn't loaded into LLM context).

### 5. Vet Skills Before Execution (Security Auditing)
- Skills can execute code and access local files, environment variables, and API keys.
- **Security Statistic**: Audits of ~4,000 public skills revealed **>35% contained security flaws** and **13% contained critical vulnerabilities** (prompt injection, malware).
- Audit all third-party skills as untrusted software dependencies before installation.

---

## Related Knowledge Nodes

- **Concepts**: [[Agent Skills Best Practices]], [[Agent Skills Security Audit]], [[Agent Skills Architecture]], [[Progressive Disclosure]], [[Deterministic Lifecycle Hooks]].
- **Entities**: [[IBM Technology]], [[Simon Willison]], [[Claude Code]], [[Gemini CLI]].
