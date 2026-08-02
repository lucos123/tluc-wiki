# Wiki Index

A catalog of everything in the knowledge base.

## Entities
- [[AI LABS]]: Technical content creator channel producing deep-dive analysis on AI agent engineering, graph topologies, and verification loops.
- [[Addy Osmani]]: Engineering leader and advocate for "AI-assisted engineering".
- [[Andre Karpathy]]: AI researcher and founding team member at OpenAI; framed the "smarter vs. faster" model trade-off.
- [[Caleb Writes Code]]: Tech content creator focusing on AI agent engineering architecture.
- [[Cerebras Systems]]: Wafer-scale AI chip manufacturer providing 750 t/s ultra-fast inference for OpenAI.
- [[Claude Code]]: Agentic coding environment developed by Anthropic.
- [[Codex]]: OpenAI's coding agent platform.
- [[DeepCent]]: Fictional state-backed Chinese AI collective from the AI 2027 scenario.
- [[GPT-5.6]]: OpenAI's frontier model family (Sol, Terra, Luna) emphasizing token efficiency and parallel reasoning.
- [[GPT-5.6 Luna]]: Fast, cost-sensitive model tier ($0.20/$1.20) in the GPT-5.6 family for high-volume subagents.
- [[GPT-5.6 Terra]]: Balanced model tier ($2.00/$12.00) in the GPT-5.6 family, replacing GPT-5.4/5.5 at lower cost.
- [[Gemini CLI]]: Open-source terminal AI assistant by Google.
- [[Goon Nguyen]]: AI Engineer and author who coined Harness Engineering.
- [[Greta]]: Context-aware AI development partner tool.
- [[HumanLayer]]: Tooling platform focused on human-in-the-loop agentic workflows and production control loops.
- [[Jarred Sumner]]: Bun co-founder and Anthropic MTS; ran the Zig→Rust 1M-line migration with Claude Code.
- [[Kimi K2.7 Code]]: Dedicated long-horizon coding and agentic model by Moonshot AI with 256K context and HighSpeed variant.
- [[Kimi K3]]: Open-weights frontier AI model by Moonshot AI featuring 896 experts, 1.8% activation, and KDA.
- [[Kyle Mistele]]: Co-founder/engineer at HumanLayer; introduced Control-Loop Engineering.
- [[LangChain Engine]]: Background agent in LangSmith that powers the Hill-Climbing Loop by optimizing traces.
- [[Leonhard Euler]]: Swiss mathematician (1707–1783) who founded Graph Theory, the theoretical basis for Graph Engineering.
- [[Mike Krieger]]: Anthropic Labs co-lead; ran the Python→TypeScript 165K-line weekend migration with Claude Code.
- [[Moonshot AI]]: AI research lab behind the Kimi model series.
- [[OpenAI]]: AI research and deployment company developing the GPT model series, Codex, and Responses API.
- [[OpenBrain]]: Fictional leading US AGI company from the AI 2027 scenario.
- [[OpenBrain Agents]]: The series of increasingly capable AI models (Agent 1-4) developed by OpenBrain.
- [[Sean's AI Stories]]: Educational content creator focusing on AI agent systems, memory architectures, and LLMOps.
- [[Uber]]: Global mobility and food delivery enterprise using closed-loop evals for multimodal agent orchestration.

## Concepts
- [[AI Code Migration]]: Six-step methodology for AI-assisted language/framework migrations at industrial scale.
- [[Agentic Engineering]]: Topic overview page covering Prompt, Context, Harness, Loop, and Graph Engineering pillars.
- [[Closed-Loop Evals]]: Automated architecture for continuous evaluation, reflection, prompt optimization, and auto-deployment without human intervention.
- [[Conductor vs Orchestrator]]: Modes of developer interaction with AI.
- [[Context Engineering]]: The practice of explicitly managing and structuring what the AI "sees".
- [[Control-Loop Engineering]]: Application of Classical Control Theory to agentic loops (Set Point, Sensors, Actuator, Adaptive Flow Control, FEEDBACK.md).
- [[Dynamic Tool Loading]]: Pattern for declaring tool schemas on-demand inside system messages during chat completions.
- [[Effort Level and Model Selection]]: The 2D decision framework for model × effort tuning in Claude Code — includes diagnostic heuristic ("didn't try" vs "didn't know") and cost-interaction curves.
- [[Graph Engineering]]: Orchestration paradigm structuring reliable agent nodes into directed graphs (DAGs or cyclic graphs).
- [[Harness Engineering]]: The design of the environment (tools, sandboxes, memory) that wraps the model.
- [[Hill-Climbing Loop]]: The highest level of LangChain's loop taxonomy, where an agent autonomously self-improves its own harness via trace analysis.
- [[Inference Speed vs Intelligence Trade-off]]: 3D decision framework balancing model intelligence, token speed, and token efficiency in model serving.
- [[LLMOps & Inference]]: Topic overview page covering model serving architectures, token economics, and inference trade-offs.
- [[Loop Engineering]]: The 4-type taxonomy (turn-based, goal-based, time-based, proactive) for designing agent loops with explicit triggers, stop conditions, and quality gates.
- [[Iterated Distillation and Amplification (IDA)]]: Training methodology to amplify and distill model capabilities.
- [[Memory Architecture]]: Reference architecture for persistent context management outside the model context window.
- [[Model Context Protocol]]: Open standard enabling AI models and agent harnesses to connect to external systems.
- [[Model Specification (Spec)]]: Document outlining desired AI behavior and alignment rules.
- [[Neuralese]]: High-dimensional vector memory that replaces text-based chain-of-thought.
- [[Obsidian Syntax Cheat Sheet]]: Quick reference guide for Obsidian wiki links, callouts, and frontmatter syntax.
- [[Orchestrator Skill Pattern]]: Multi-agent pattern where a top-level skill coordinates parallel specialized subagent review skills and merges findings.
- [[Persistent Instruction File]]: Durable guidance for agents (e.g., AGENTS.md, CLAUDE.md).
- [[Preserved Thinking]]: Pattern of retaining historical reasoning_content across multi-turn messages to preserve continuous chain-of-thought.
- [[Programmatic Tool Calling]]: Model capability to write and execute code for filtering data and dynamically orchestrating tool calls.
- [[Reasoning Effort]]: Top-level model parameter for dynamically tuning reasoning depth (low, high, max).
- [[Responses API]]: OpenAI's v1/responses endpoint succeeding Chat Completions, built for native tool use, hosted shell, and multi-agent coordination.
- [[Second Opinion Pattern]]: Verification pattern using fresh-context background subagents (e.g., claude -p) with model overrides (Opus over Haiku) to eliminate worker self-review bias.
- [[Stable Latent MoE]]: Ultra-sparse MoE architecture with latent token compression and quantile balancing.
- [[Superhuman AI]]: AI systems capable of recursively improving themselves.
- [[Superhuman Coder]]: Milestone where AI can perform coding tasks faster and cheaper than top humans.
- [[The Factory Model (SDLC)]]: Building systems that build software.
- [[Vibe Coding vs Agentic Engineering]]: The spectrum of AI-assisted development.
- [[Verification Loop]]: The repeating check-and-fix cycle where an AI agent verifies its own work before reporting completion. Covers gate strengths and 4 deployment modes (Standalone, Embedded, Chained, PR).
- [[llm-wiki]]: A pattern for building personal knowledge bases using LLMs.

## Sources
- [[12 Agentic Harness Patterns from Claude Code]]: Design patterns from a leaked production agent's source code.
- [[7 AI Coding Trends to Watch This Year in 2026]]: Shifts in software development as AI integration matures, such as AI-native systems and context-aware tools.
- [[AI 2027]]: Scenario forecasting the rapid development of superhuman AI and geopolitical tensions between 2025-2027.
- [[Agent Harness explained in 8min]]: Caleb Writes Code's concise breakdown of the 3-stage evolution (Prompt → Context → Harness Engineering) and fresh-context loops.
- [[Anthropic Just Fixed Graph Engineering's Greatest Flaw]]: AI LABS breakdown of DAG error cascading, the Second Opinion Pattern, Chrome Headless Shell verification, and the Orchestrator Skill Pattern.
- [[Best practices for Claude Code]]: Guide to managing context, verification, and autonomous workflows.
- [[Building Closed-Loop Evals for a Multimodal Agent at Scale]]: Uber's presentation on multimodal agent orchestration, closed-loop auto-tuning, and Pass at K metrics.
- [[Building verification loops in Claude Code with skills]]: How to encode manual checks as skills and deploy them standalone, embedded, chained, or as PR-level team gates.
- [[Loop Engineering explained in 8min]]: Caleb Writes Code's technical breakdown of multi-loop stacking and Addy Osmani's 6 components of loop engineering.
- [[Loop Engineering from First Principles]]: Kyle Mistele's talk on applying Control Theory and production patterns (Adaptive Flow Control, FEEDBACK.md) to agentic loops.
- [[Loop engineering Getting started with loops]]: Official Claude Code loop taxonomy — turn-based, goal-based, time-based, proactive — with decision framework and the full proactive loop composition.
- [[Best practices – Codex]]: Habits and configurations to scale agentic usage with AGENTS.md and MCP.
- [[Claude Code Hooks]]: Documentation on lifecycle hooks for deterministic agent control and workflow automation.
- [[Claude Code effort level and model selection]]: Deep-dive on frozen weights, effort as trained behavior, 7x token multiplier, specialist/expert/generalist model framework, and diagnostic heuristic.
- [[Claude Code Monorepo Setup]]: Strategies for configuring Claude Code in large, multi-package repositories using sparse worktrees and hierarchical context.
- [[Claude Code Skills]]: Documentation on extending Claude Code with modular skills via SKILL.md.
- [[Codex Skills]]: Documentation on how Codex implements the open Agent Skills standard using progressive disclosure.
- [[Creating Agent Skills]]: Detailed guide on automated and manual creation of Gemini Agent Skills.
- [[GPT-5.6 Frontier Intelligence]]: OpenAI launch announcement for GPT-5.6 (Sol, Terra, Luna) focusing on efficiency and parallel agent reasoning.
- [[GPT-5.6 Luna Model API Reference]]: Official OpenAI API documentation, pricing, and limits for gpt-5.6-luna.
- [[GPT-5.6 Sol Model API Reference]]: Official OpenAI API documentation, pricing, and limits for gpt-5.6-sol.
- [[GPT-5.6 Terra Model API Reference]]: Official OpenAI API documentation, pricing, and limits for gpt-5.6-terra.
- [[Gemini CLI Skills]]: Documentation on the Gemini CLI's implementation of Agent Skills, emphasizing progressive disclosure and explicit consent models.
- [[Graph Engineering explained in 8min]]: Caleb Writes Code's technical breakdown of multi-agent graph topologies, node capability evolution, and prompt caching economics.
- [[Gemini CLI Tips & Tricks]]: Dozens of pro-tips for Google's agentic command-line tool.
- [[Get started with Agent Skills]]: Tutorial on creating an API Auditor skill for the Gemini CLI.
- [[Harness Engineering]]: Goon Nguyen's breakdown of why the ecosystem around the model matters more than the model itself.
- [[How Anthropic runs large-scale code migrations with Claude Code]]: Anthropic's six-step AI migration methodology; Bun Zig→Rust (1M lines, $165K) and Python→TypeScript (165K lines, 1 weekend).
- [[Kimi API Model List & Deprecations]]: Official model IDs, context lengths, and sunset schedule for Moonshot AI APIs.
- [[Kimi API Quickstart & Integration]]: Integration guide for Kimi models via OpenAI-compatible endpoints, streaming, and multimodal inputs.
- [[Kimi K2.7 Code Guide]]: Moonshot AI documentation for Kimi K2.7 Code and HighSpeed variants.
- [[Kimi K3 Model Guide]]: Technical documentation for Kimi K3, Moonshot AI's 2.8T open-source flagship model.
- [[Kimi K3 explained in 13min]]: Caleb Writes Code's technical deep-dive into Kimi K3's architecture, Stable Latent MoE, and KDA.
- [[Kimi Multi-turn Context Management Guide]]: Best practices for managing stateless conversation payloads, message truncation, and system prompt pinning.
- [[Kimi Reasoning Effort Guide]]: Guidance for configuring top-level reasoning_effort in Kimi K3.
- [[Kimi Thinking Models & Preserved Thinking Guide]]: Detailed breakdown of reasoning tokens, preserved thinking, and multi-step tool configurations across Kimi models.
- [[Managing Agent Skills]]: Guide to slash commands, terminal utilities, and discovery tiers for Gemini Agent Skills.
- [[Memory Architecture Reference Notes]]: Reference diagram (2nd-brain.jpg) detailing 5-tier directory structure and compounding feedback loop.
- [[My LLM coding workflow going into 2026]]: Addy Osmani's structured "AI-assisted engineering" approach.
- [[OpenAI Models & Codex Integration Guide]]: Developer guide for model selection, config.toml, and reasoning effort in Codex.
- [[OpenAI's $10B Bet on their biggest model yet]]: Caleb Writes Code's financial and architectural analysis of OpenAI's $10B Cerebras deal and GPT-5.6 2-tier serving.
- [[The Art of Loop Engineering]]: LangChain's 4-level loop taxonomy culminating in autonomous self-improvement via trace evaluation.
- [[The New SDLC With Vibe Coding]]: Whitepaper detailing the transition to intent-driven software development.
- [[Vault Welcome]]: Summary of the default Obsidian onboarding note.
- [[You Can Learn AI Agent Harness & Loop Engineering In 19 Min]]: Sean's AI Stories breakdown of horse-and-harness analogy, 4 memory tiers, and LLMOps.

## Personal Memory & Projects (mem/)
- [[2026-Q3-Milestones]]: Historical milestone log for 2nd Brain architecture and AI engineering progress.
- [[AI Engineering Mastery 2026]]: Personal career goal for mastering agentic software engineering and Second Brain systems.
- [[AI Pair Programming Preferences]]: Work preferences and collaboration rules for Gemini AI.
- [[gemini]]: Second Brain identity, user profile, operating preferences, career focus, and active goals.
- [[tluc-wiki 2nd Brain Architecture]]: Engineering project upgrading tluc-wiki into a 5-tier persistent context system.

## Analyses
