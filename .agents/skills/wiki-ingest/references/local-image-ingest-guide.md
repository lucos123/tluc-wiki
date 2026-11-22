# Local & Uploaded Image / Infographic Ingest Guide (v4.4)

Use this reference whenever the user uploads, pastes, or points to **local image files or visual infographics** (roadmaps, architecture diagrams, handwritten notes, cheat sheets) rather than a web/social URL.

---

## 3-Stage Local Image & Infographic Pipeline

### Stage 1 — Visual Inspection & Candidate Link Discovery
1. Call `read_file` directly on the uploaded/local image files in parallel batches of **5–7 images per turn**.
2. Extract:
   - Exact canonical title, clean kebab-case `<slug>`, and any source attribution visible on the image.
   - All layers, components, metrics, workflows, formulas, and tools shown visually.
3. Run keyword link discovery against `index.md` without redundant directory scans:
   ```powershell
   python .agents/skills/wiki-ingest/scripts/register_ingest.py --suggest-links "<core keywords>"
   ```

---

### Stage 2 — Immutable Archival & SHA-256 Deduplication (`--local-files`)
Archive the local/uploaded image(s) permanently inside `raw/` using `download_post_assets.py --local-files`:

```powershell
# Single or 1-3 standalone infographic(s) -> auto-routes to raw/assets/<slug>-01.<ext>
python .agents/skills/wiki-ingest/scripts/download_post_assets.py `
  --slug "<clean-kebab-case-slug>" `
  --mode auto `
  --local-files "<path-to-image-1>"

# Multi-slide local visual deck (>= 4 images) + optional raw summary stub -> raw/screenshots/<slug>/00.<ext>..NN.<ext>
python .agents/skills/wiki-ingest/scripts/download_post_assets.py `
  --slug "<clean-kebab-case-slug>" `
  --mode auto `
  --local-files "<path-1>" "<path-2>" "<path-3>" "<path-4>" `
  --init-raw --raw-subdir "ai-other" --raw-title "<Canonical Title>"
```

- **Auto Storage Routing (`--mode auto`)**: `1–3` images go to `raw/assets/<slug>-NN.<ext>` (`start_index=1`); `>= 4` images go to `raw/screenshots/<slug>/00.<ext>..NN.<ext>` (`start_index=0`).
- **SHA-256 Deduplication**: Each file's SHA-256 checksum is compared against existing images in `raw/assets/` and `raw/screenshots/`. If an identical file already exists, `duplicate_existing_path` is reported in stdout JSON so you can reuse or avoid re-ingesting duplicate visuals.
- **When to omit vs. include `--init-raw`**:
  - *Single standalone infographic (`1–2` images)*: Often sufficient to archive into `raw/assets/` and point `wiki/sources/<Title>.md` `source:` directly to `"raw/assets/<slug>-01.<ext>"` (matching `Memory Architecture Reference Notes.md`), OR pass `--init-raw` if accompanied by user notes/caption text.
  - *Multi-page deck (`>= 4` images)*: Pass `--init-raw --raw-subdir <topic> --raw-title "<Title>"` to generate `raw/articles/<topic>/<slug>.md` with `infographic` tags cleanly.

---

### Stage 3 — Synthesize, Compound & Register Atomically
1. Create `wiki/sources/<Safe Title>.md` (`source_type: infographic`, embedding `../../raw/...` and transcribing all visual layers/concepts systematically).
2. **Compound into existing `wiki/concepts/` or `wiki/topics/`** first; create a new `wiki/concepts/` page only if the graphic introduces a substantive new conceptual topic not yet covered. Flag outdated tools vs. newer vault standards with `> ⚠️ **Evolving tooling note**`.
3. Register atomically in 1 command via `register_ingest.py` (`--date YYYY-MM-DD --log-type ingest --source-title "<Title>" --entry "Sources|<Safe Title>|<summary>" ...`) and verify `"status": "ok"`, `"total_broken_links": 0`, and `"index_coverage_pct": 100.0`.
