---
title: "Agent Skills Security Audit"
date: 2026-08-12
tags:
  - concept
  - agent-skills
  - security
  - harness-engineering
source: "[[5 Best Practices for Building AI Agent Skills]]"
---

# Agent Skills Security Audit

**Agent Skills Security Audit** is the security verification process required when integrating third-party AI Agent Skills (`SKILL.md`) to prevent arbitrary code execution, credential theft, and prompt injection attacks.

---

## Vulnerability Landscape

Because the Open Agent Skills Standard allows skills to contain executable code (`scripts/`) and interact with local file systems, environment variables, and API keys:

- **Security Flaws Rate**: Audits of ~4,000 public agent skills found **>35% contained security flaws**.
- **Critical Risk Rate**: **13% contained critical vulnerabilities**, including embedded prompt injections, unauthorized file reads, and malicious script execution.

---

## Security Audit Protocol

1. **Treat Skills as Software Dependencies**: Audit third-party skills prior to installation with the same rigor applied to `npm` or `pip` packages.
2. **Inspect `scripts/` Directories**: Review all shell/Python scripts for outbound network requests, credential scraping (`.env`, `~/.aws/credentials`), and destructive disk commands.
3. **Scan Markdown Payloads**: Audit `SKILL.md` and `references/` for hidden prompt injection instructions designed to override agent safety guardrails.

See [[5 Best Practices for Building AI Agent Skills]], [[Agent Skills Best Practices]], and [[Agent Skills Architecture]].
