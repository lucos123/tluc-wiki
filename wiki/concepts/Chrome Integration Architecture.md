---
title: "Chrome Integration Architecture"
date: 2026-08-10
tags:
  - concept
  - browser-automation
  - harness-engineering
  - claude-code
source: "[[Use Claude Code with Chrome]]"
---

# Chrome Integration Architecture

**Chrome Integration Architecture** is the browser automation subsystem in [[Claude Code]] that connects the CLI to Chromium browsers via a local Native Messaging Host and the `claude-in-chrome` [[Model Context Protocol|MCP server]].

---

## Technical Mechanism

1. **Native Messaging Protocol**: Claude Code registers a Native Messaging Host (`com.anthropic.claude_code_browser_extension`) in OS app support directories to communicate with the browser extension via stdio streams.
2. **Inherited Session Cookies**: Reuses the user's active browser cookies and authentication tokens for seamless interaction with authenticated web apps (Jira, Notion, Google Docs).
3. **Interactive Manual Pause**: Automatically pauses automation and prompts the developer when encountering CAPTCHAs or 2FA login screens.

See [[Use Claude Code with Chrome]], [[Model Context Protocol]], and [[Harness Engineering]].
