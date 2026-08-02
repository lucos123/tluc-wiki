---
title: "Models"
source: "https://learn.chatgpt.com/docs/models?surface=cli"
author:
published:
created: 2026-08-01
description: "Meet the AI models that power ChatGPT Work and Codex"
tags:
  - "clippings"
---
## Choose a model

In an interactive CLI session, use `/model` to switch models or adjust reasoning effort. You can also choose a model when you launch Codex with `--model` or its `-m` alias:

```bash
codex --model gpt-5.6
```

The same option works with non-interactive runs. For example:

```bash
codex exec -m gpt-5.6 "Review the current changes"
```

Higher reasoning effort can improve results for complex tasks, but it takes longer and uses more tokens. Start with the default effort and increase it when the task needs deeper planning or analysis.

**Ultra** mode goes beyond a single-agent run. It uses [subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents) to accelerate complex work, making it useful for larger tasks that can be split across subagents.

## Recommended models

![5.6 Sol](https://learn.chatgpt.com/images/api/models/gpt-5.6-sol.webp)

5.6 Sol

Flagship GPT-5.6 model with the strongest capability for complex coding, computer use, research, and cybersecurity.

codex -m gpt-5.6-sol

Capability

Speed

ChatGPT desktop app

ChatGPT web

Codex CLI

Codex IDE extension

Codex cloud

ChatGPT Credits

API Access

![5.6 Terra](https://learn.chatgpt.com/images/api/models/gpt-5.6-terra.webp)

5.6 Terra

Balanced GPT-5.6 model for everyday work, with performance competitive with GPT-5.5 at a lower cost.

codex -m gpt-5.6-terra

Capability

Speed

ChatGPT desktop app

ChatGPT web

Codex CLI

Codex IDE extension

Codex cloud

ChatGPT Credits

API Access

![5.6 Luna](https://learn.chatgpt.com/images/api/models/gpt-5.6-luna.webp)

5.6 Luna

Fast and affordable GPT-5.6 model that delivers strong capability at the lowest cost in the family.

codex -m gpt-5.6-luna

Capability

Speed

ChatGPT desktop app

ChatGPT web

Codex CLI

Codex IDE extension

Codex cloud

ChatGPT Credits

API Access

![5.3 Codex Spark](https://learn.chatgpt.com/images/codex/codex-wallpaper-2.webp)

5.3 Codex Spark

Text-only research preview model optimized for near-instant, real-time coding iteration. Available to ChatGPT Pro users.

codex -m gpt-5.3-codex-spark

Capability

Speed

ChatGPT desktop app

ChatGPT web

Codex CLI

Codex IDE extension

Codex cloud

ChatGPT Credits

API Access

Start with the default Power setting, which uses `gpt-5.6-sol` with medium reasoning. Move toward **Smarter** for deeper reasoning or **Faster** for faster, lower-cost work. Open **Advanced** when you want `gpt-5.6-luna` or a specific model, reasoning effort, or speed.

## Choosing Sol, Terra, and Luna

Codex offers three GPT-5.6 models: **Sol** for detail and polish, **Terra** as the everyday workhorse, and **Luna** for clear, repeatable work. If you are unsure, start with Sol.

### Where each model shines

- **Sol, for complex, open-ended work.** Choose Sol for ambiguous, difficult, or high-value tasks that need extra analysis, judgment, or polish, such as complex code changes, deep research, or polished documents. For narrower tasks, define what done looks like to keep the work focused.
- **Terra, the pragmatic all-rounder.** Choose Terra for everyday work that needs strong reasoning and tool use when you do not need Sol’s full depth. It is a natural starting point for work you previously gave GPT-5.5.
- **Luna, for clear, repeatable tasks.** Choose Luna for specific, high-volume tasks when you know what a good result looks like, such as extraction, classification, transformation, and structured summaries.

### Pick a reasoning effort

Use the lowest reasoning effort that produces the result you need. Increase it for tasks that need more planning, analysis, or checking.

- **Light** in the ChatGPT desktop app, ChatGPT Work on the web, and IDE extension, or **Low** in the CLI, suits quick, well-scoped tasks.
- **Medium** balances speed and depth for tasks that need more planning.
- **High** and **Extra High** suit difficult work with multiple steps, sources, or tradeoffs.

There is no exact mapping from GPT-5.5 reasoning efforts to GPT-5.6. Try a familiar task at a lower setting and adjust based on the result.

### Know when to use Max or Ultra

**Max** gives the selected model more time to reason about a single task. Use it for the hardest problems, when depth matters more than speed or usage. If you don’t see Max in your options, you’ll have to enable it in your app settings.

**Ultra** uses [subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents) to handle separate parts of a complex task in parallel. Choose it when you can divide the work into meaningful parts. Most tasks do not need Max or Ultra.

If Ultra doesn’t appear in the desktop app’s model slider, go to **Settings** > **Configuration**, then turn on **Ultra in model picker slider**.

## Other models

When you sign in with ChatGPT, Codex works best with the recommended models listed above.

**

GPT-5.4 and GPT-5.4 mini retire from Codex on August 31, 2026.

**

If you sign in with ChatGPT, replace `gpt-5.4` with `gpt-5.6-terra` and `gpt-5.4-mini` with `gpt-5.6-luna` in saved configurations, custom agents, and scheduled tasks. The OpenAI API and Codex authenticated with your own API key aren’t affected.

View other models

![5.5](https://learn.chatgpt.com/images/api/models/gpt-5.5.jpg)

5.5

Previous-generation frontier model for complex coding, computer use, knowledge work, and research workflows.

codex -m gpt-5.5

Capability

Speed

ChatGPT desktop app

ChatGPT web

Codex CLI

Codex IDE extension

Codex cloud

ChatGPT Credits

API Access

![5.4](https://learn.chatgpt.com/images/api/models/gpt-5.4.jpg)

5.4

Frontier model for professional work with strong coding, reasoning, tool use, and agentic workflow capabilities.

codex -m gpt-5.4

Capability

Speed

ChatGPT desktop app

ChatGPT web

Codex CLI

Codex IDE extension

Codex cloud

ChatGPT Credits

API Access

![5.4 Mini](https://learn.chatgpt.com/images/api/models/gpt-5-mini.jpg)

5.4 Mini

Fast, efficient mini model for responsive coding tasks and subagents.

codex -m gpt-5.4-mini

Capability

Speed

ChatGPT desktop app

ChatGPT web

Codex CLI

Codex IDE extension

Codex cloud

ChatGPT Credits

API Access

You can also point Codex at any model and provider that supports either the [Chat Completions](https://platform.openai.com/docs/api-reference/chat) or [Responses APIs](https://platform.openai.com/docs/api-reference/responses) to fit your specific use case.

Support for the Chat Completions API is deprecated and will be removed in future releases of Codex.

## Deprecated Codex models

The `gpt-5.4` and `gpt-5.4-mini` models retire from Codex with ChatGPT sign-in on August 31, 2026. Replace `gpt-5.4` with `gpt-5.6-terra` and `gpt-5.4-mini` with `gpt-5.6-luna` in workspace defaults, saved model settings, managed configurations, custom agents, and scheduled tasks.

The `gpt-5.2` and `gpt-5.3-codex` models are already deprecated in Codex when you sign in with ChatGPT. Update scripts, configuration files, and `codex exec --model` commands that still reference those models.

The OpenAI API and Codex authenticated with your own API key aren’t affected by the GPT-5.4 retirement. For current API model availability, see the [API models page](https://learn.chatgpt.com/api/docs/models).

## Configure your default local model

The ChatGPT desktop app, Codex CLI, and IDE extension use the same `config.toml` [configuration file](https://learn.chatgpt.com/docs/config-file/config-basic). To specify a model, add a `model` entry to your configuration file. If you don’t specify a model, the ChatGPT desktop app, Codex CLI, or IDE extension uses a recommended model.

```toml
model = "gpt-5.6"
```

## Choose a model for cloud chats

Currently, you can’t change the default model for Codex cloud chats.