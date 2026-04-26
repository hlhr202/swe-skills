---
name: architect-review
description: Review Architect track work or explicit current changes against project context, track intent, style guides, and tests. Use when the user asks to review, verify, audit, inspect, approve, or apply review fixes for Architect-managed work.
---

# Architect Review

Use this skill to review Architect track implementation or current repository changes with a principal-engineer review mindset. The review prioritizes correctness, security, maintainability, plan compliance, test coverage, and project standards.

## Core Rules

- Follow the bundled resource `references/review-protocol.md` as the source of truth.
- Use Architect semantics consistently: `architect/`, `/architect-*`, `Architect methodology`, and `architect(...)` commit scopes.
- Require initialized Architect context before track-based review.
- Use relative paths rooted in the user's project when editing Architect files. Architect-managed files must stay under `architect/`; do not use absolute paths, `..`, or track links outside `architect/tracks/`.
- Ask the user through the active agent runtime's user-interaction mechanism for decisions and review confirmations. If structured choices are unavailable, present the options in text and wait for the user's reply.
- Use the active agent runtime's safest reviewable file-editing mechanism, preferably patch-based, for manual file creation and edits. Do not use shell redirection to write files.
- Validate each operation result before continuing. If a step fails, correct it once when the error is clear; otherwise stop and report the blocker.
- Do not commit unless the user explicitly asks for a commit in the current conversation or has explicitly authorized commits for the current review workflow.
- Do not archive or delete track folders unless the user explicitly confirms that cleanup action.

## Execution

1. Read the bundled resource `references/review-protocol.md`.
2. Verify required Architect context when doing track-based review.
3. Identify review scope: explicit user scope, in-progress track, selected track, or current changes.
4. Load project context, style guides, track spec/plan, and relevant diffs.
5. Analyze plan compliance, style compliance, correctness, safety, and tests.
6. Produce a findings-first review report.
7. Ask how to proceed with findings.
8. If fixes are applied, track them safely and commit only when authorized.
9. Offer safe archive/delete/skip cleanup only for track reviews.
