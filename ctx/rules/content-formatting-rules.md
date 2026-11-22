# Content & Markdown Formatting Rules

1. **Standard Relative Markdown Link Syntax**: Always use relative Markdown links (`[Page Name](../concepts/Page%20Name.md)`), RFC 3986 percent-encoded via `quote(rel_path, safe="/-._~")`, so links work natively in IDE Preview, GitHub, and Obsidian. Keep frontmatter `source:` as clean repo-relative plain paths (`"raw/..."` or `"wiki/sources/..."`) without `[[ ]]`.
2. **YAML Frontmatter**: Required fields: `title`, `date` (YYYY-MM-DD), `tags` (multiline YAML list).
3. **Clean Related Pages Layout**: Format `## Related Pages` groups with `>= 3` links as nested sub-bullets instead of single comma-separated lines.
4. **Alphabetical Indexing**: Keep `index.md` sorted alphabetically in each section.
