# Worked Examples: Sharpening & Quick Playback

Concrete before/after examples adapted for `tluc-wiki` (`output/`, `mem/projects/`, `dental-consult-ops`, and code edits).

---

## Example 1 — Mode B: `output/reports/` Brief (English)

> Vague request: "Write a report on agent memory."

**Sharpened Brief (`86` words)**:
- **Consumer**: Engineer designing persistent memory for multi-session CLI agents; gains a clear architecture decision table comparing working, semantic, episodic, and procedural tiers.
- **Goal & Expert Lens**: Synthesize primary `raw/` articles and existing `wiki/concepts/` pages (`[AI Agent Memory Types](../../wiki/concepts/AI%20Agent%20Memory%20Types.md)`, `[Memory Architecture](../../wiki/concepts/Memory%20Architecture.md)`) into `output/reports/Agent Memory Architecture Trade-offs.md`, surfacing conflicting storage vs. retrieval cost benchmarks rather than repeating summaries.
- **Done-Check**: `check_prose.py`, `check_research.py`, and `lint_wiki.py` all return `0` errors and `100.0%` index coverage.
- **Non-Goals**: No database provisioning scripts, no runtime benchmarks, no edits to `raw/`.

---

## Example 2 — Mode B: `dental-consult-ops` SOP Brief (Vietnamese)

> Yêu cầu mơ hồ: "Cải thiện kịch bản tư vấn Implant cho đội TVV."

**Sharpened Brief (`78` words)**:
- **Consumer / Đối tượng hưởng lợi**: Đội ngũ TVV Nha khoa 3C tiếp nhận khách hỏi giá Implant qua inbox; có khung phản hồi 3 bước kèm mốc chuyển ca lên bác sĩ.
- **Goal / Mục tiêu**: Cập nhật `references/` trong `dental-consult-ops` dựa trên log khiếu nại và bảng giá hiện hành, tách rõ tình huống khách so sánh giá vs. lo ngại đau/biến chứng.
- **Done-Check / Tiêu chí hoàn thành**: 3 kịch bản mẫu có đầy đủ lời thoại, ngưỡng escalation và checklist kiểm tra bởi quản lý TVV trong `< 5` phút.
- **Non-Goals / Ngoài phạm vi**: Không sửa bảng giá y khoa và không viết lại quy trình chỉnh nha.

---

## Example 3 — Mode A: Quick Playback Stop-vs-Proceed Decision

| Situation | Example Playback Closure | Action |
| :--- | :--- | :--- |
| **Irreversible / High Risk** (schema change, bulk vault migration, deletion) | *"Goal: convert all 3,700 wikilinks to percent-encoded relative Markdown links. Assumptions: skip `raw/` and keep `wiki/log.md` intact. Success check: `lint_wiki.py` exits `0` with `0` broken links. Right? Correct me where I drifted."* | **Pause** for user go-ahead before editing files. |
| **Clearly Reversible** (drafting 1 new note, running read-only audit script) | *"Interpreted as a read-only audit across `wiki/concepts/` rather than modifying pages; proceeding now and reporting counts."* | **Proceed** immediately and surface the interpretation inline.

### Paraphrase vs. Echo Test

- **Bad (Echo)**: `"Goal: analyze OMC repo skills to see what we can copy to tluc-wiki."` (repeats user words blindly; adds zero clarity).
- **Good (Playback)**: `"Goal: produce a dependency audit of all 84 OMC skills, split them into copyable discipline skills vs. OMC-locked runtime skills, and test each ported skill under .agents/skills/ with lint_wiki.py staying at 0 errors."`
