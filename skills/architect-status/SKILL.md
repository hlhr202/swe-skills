---
name: architect-status
description: Report read-only Architect project progress from the tracks registry and plans. Use when the user asks for status, progress, current task, next action, blockers, completion percentage, or pending work.
---

# Architect Status

Use this skill to report the current status of an initialized Architect project. It reads `architect/tracks.md` and track plans, then summarizes progress without modifying files.

## Core Rules

- Follow the bundled resource `references/status-protocol.md` as the source of truth.
- Use Architect terminology consistently: `architect/`, `/architect-*`, and `Architect methodology`.
- This skill is read-only. Do not create, edit, move, delete, archive, or commit files.
- Architect-managed reads must stay under `architect/`; do not follow absolute paths, `..`, or track links outside `architect/tracks/`.
- Validate each operation result before continuing. If a read or command fails, correct it once when the error is clear; otherwise stop and report the blocker.
- Parse registry and plan formats produced by `architect-setup`, `architect-propose`, and `architect-implement`.

## Execution

1. Read the bundled resource `references/status-protocol.md`.
2. Verify required Architect context files exist.
3. Parse `architect/tracks.md`.
4. Read each track's `plan.md` and `metadata.json` when available.
5. Compute track and project progress.
6. Report current work, next action, blockers, and completion percentage.
