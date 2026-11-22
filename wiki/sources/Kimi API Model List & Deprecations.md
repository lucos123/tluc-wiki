---
title: "Kimi API Model List & Deprecations"
date: 2026-08-01
tags:
  - source
  - ai-models
  - moonshot-ai
source: "raw/articles/kimi/model-list.md"
---

# Kimi API Model List & Deprecations

**Source File**: [raw/articles/kimi/model-list.md](../../raw/articles/kimi/model-list.md)

Catalog of official model IDs, context windows, and deprecation timelines across the [Moonshot AI](../entities/Moonshot%20AI.md) platform.

## Key Concepts

- **Active Model Lineup**:
  - `kimi-k3`: 2.8T parameters, 1M context, flagship multimodal reasoning model.
  - `kimi-k2.7-code`: 256K context, dedicated long-horizon coding model.
  - `kimi-k2.7-code-highspeed`: 256K context, 180–260 t/s high-speed coding variant.
  - `kimi-k2.6`: 256K context, multimodal text/image/video reasoning model.
  - `kimi-k2.5`: 256K context, multimodal agent & general intelligence model.
- **Deprecation & Sunset Schedule**:
  - `moonshot-v1` series (8k, 32k, 128k text & vision) and `kimi-k2.5`: Closed to new users following K3 launch, with full platform sunset on **August 31, 2026**.
  - `kimi-k2` series (`kimi-k2-0905-preview`, `kimi-k2-thinking`, etc.): Discontinued on **May 25, 2026**.
  - `kimi-latest`: Discontinued on **January 28, 2026**.
  - `kimi-thinking-preview`: Discontinued on **November 11, 2025**.

## Synthesis Notes

This document provides a clear snapshot of the model lifecycle at [Moonshot AI](../entities/Moonshot%20AI.md). The rapid retirement of `moonshot-v1` and legacy `kimi-k2` models highlights the speed of transition toward MoE-backed thinking architectures ([Kimi K3](../entities/Kimi%20K3.md), [Kimi K2.7 Code](../entities/Kimi%20K2.7%20Code.md)).
