---
title: "Use Claude Code with Chrome"
date: 2026-08-10
tags:
  - source
  - chrome
  - browser-automation
  - harness-engineering
  - claude-code
source: "[[raw/articles/claude-code/hooks-tools-mcp-chrome/chrome.md]]"
url: "https://code.claude.com/docs/en/chrome.md"
---

# Use Claude Code with Chrome

**URL**: https://code.claude.com/docs/en/chrome.md  
**Source File**: [[raw/articles/claude-code/hooks-tools-mcp-chrome/chrome.md]]  

---

## Executive Summary

This official Anthropic guide details how **Claude Code** connects to Google Chrome and Chromium browsers via the **Claude in Chrome extension** (`claude-in-chrome`).

This integration enables direct browser automation from the CLI, inheriting active session authentication states to perform visual regression testing, live console debugging, automated form filling, file uploads (up to 10MB), GIF recording, and data extraction.

---

## Chrome Integration Capabilities

```
┌─────────────────────────────────────────────────────────────┐
│                   Claude Code CLI Session                   │
└──────────────────────────────┬──────────────────────────────┘
                               │ Native Messaging Host (MCP)
┌──────────────────────────────▼──────────────────────────────┐
│                  Chrome Browser Extension                   │
├─────────────────────────────────────────────────────────────┤
│ • Live Debugging (Console Logs & DOM State)                 │
│ • Local Web App Testing (http://localhost:3000)             │
│ • Authenticated Web App Access (Google Docs, Jira, Figma)   │
│ • Media Capture (GIF recording & screenshots saved to disk) │
└─────────────────────────────────────────────────────────────┘
```

---

## Launch & Configuration Commands

```bash
# Launch session with Chrome enabled
claude --chrome

# Manage status & default settings via interactive CLI menu
/chrome
```

---

## Related Knowledge Nodes

- **Concepts**: [[Chrome Integration Architecture]], [[Model Context Protocol]], [[Harness Engineering]].
- **Entities**: [[Chrome Extension]], [[Claude Code]], [[Anthropic]].
