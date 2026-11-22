---
title: "Chrome Extension"
date: 2026-08-10
tags:
  - entity
  - tool
  - browser-extension
  - claude-code
source: "wiki/sources/Use Claude Code with Chrome.md"
---

# Chrome Extension

**Chrome Extension** (`Claude in Chrome`) is the official Chromium extension developed by [Anthropic](Anthropic.md) to enable deep browser automation, DOM inspection, live console log reading, and visual verification for [Claude Code](Claude%20Code.md).

---

## Technical Specifications

- **Extension ID**: `fcoeoabgfenejglbffodgkkbkcdhcgfn`
- **Supported Browsers**: Google Chrome, Microsoft Edge, Brave, Arc, Vivaldi, Opera.
- **Protocol**: Exposes browser control actions as native [MCP tools](../concepts/Model%20Context%20Protocol.md) (`read_page`, `get_page_text`, `find`, `browser_batch`).

See [Use Claude Code with Chrome](../sources/Use%20Claude%20Code%20with%20Chrome.md), [Chrome Integration Architecture](../concepts/Chrome%20Integration%20Architecture.md), and [Anthropic](Anthropic.md).
