

<!-- SpecAssay (append) — mandatory Carries field -->

## SpecAssay — Carries (required)

Every task MUST declare the registry ID(s) it implements:

- Format on each task line: `**Carries**: AC-…, FR-…` (one or more IDs from the PRD registry).
- Do not invent IDs in tasks. If an ID is missing from the registry, stop and fix the PRD first.
- Test tasks MUST name the exact proof before the code exists: the test's file path and its exact function/description name (e.g. `test_AC_SYNC_04_offline_edit_queues_locally` in `tests/test_sync.py`), not just "a test for this AC." The proof's name is decided at task creation, not audited afterward — write the task line as if the test already exists, then make it true.
- Implementation tasks that create or first touch a source file MUST carry the exact `@covers` line to paste, pre-written in the task itself: `# @covers ID-1, ID-2, …` (or the language's own comment syntax). Copy it in when the file is created; do not compose it from memory later. A task whose own line already states the mark removes the only step an author could forget (rule 6a's own "the honest path must be the shortest path").
