---
title: "Chrome Integration Architecture"
date: 2026-08-10
tags:
  - concept
  - browser-automation
  - harness-engineering
  - claude-code
source: "wiki/sources/Use Claude Code with Chrome.md"
---

# Chrome Integration Architecture

**Chrome Integration Architecture** is the browser automation subsystem in [Claude Code](../entities/Claude%20Code.md) that connects the CLI to Chromium browsers via a local Native Messaging Host and the `claude-in-chrome` [MCP server](Model%20Context%20Protocol.md).

---

## Technical Mechanism

1. **Native Messaging Protocol**: Claude Code registers a Native Messaging Host (`com.anthropic.claude_code_browser_extension`) in OS app support directories to communicate with the browser extension via stdio streams.
2. **Inherited Session Cookies**: Reuses the user's active browser cookies and authentication tokens for seamless interaction with authenticated web apps (Jira, Notion, Google Docs).
3. **Interactive Manual Pause**: Automatically pauses automation and prompts the developer when encountering CAPTCHAs or 2FA login screens.

See [Use Claude Code with Chrome](../sources/Use%20Claude%20Code%20with%20Chrome.md), [Model Context Protocol](Model%20Context%20Protocol.md), and [Harness Engineering](Harness%20Engineering.md).
