# Query Workflow Execution Example

This example demonstrates a complete end-to-end execution of the `wiki-query` skill.

---

## Input Command
```
/wiki-query "So sánh Loop Engineering và Harness Engineering"
```

---

## Execution Steps

1. **Fast Search Script Execution**:
   ```powershell
   python .agents/skills/wiki-query/scripts/query_wiki.py "Harness Engineering"
   python .agents/skills/wiki-query/scripts/query_wiki.py "Loop Engineering"
   ```
2. **Targeted Page Reads**: Read `wiki/concepts/Harness Engineering.md` and `wiki/concepts/Loop Engineering.md`.
3. **Synthesis & Answer Delivery**:
   - Classification: Comparative Query.
   - Output structured comparison table & analytical trade-offs with citations `[Harness Engineering](../../wiki/concepts/Harness%20Engineering.md)` and `[Loop Engineering](../../wiki/concepts/Loop%20Engineering.md)`.
4. **Compounding Evaluation**: Proposal accepted to file back as `wiki/analyses/Loop Engineering vs Harness Engineering.md`.
5. **Log & Self-Verification**: Appended `wiki/log.md` and ran `lint_wiki.py` to confirm 0 broken links.
