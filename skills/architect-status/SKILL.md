---
name: architect-status
description: Report read-only Architect project status from core context and, when available, the tracks registry and plans. Use when the user asks for setup status, progress, current task, next action, blockers, completion percentage, or pending work.
---

# Architect Status

Use this skill to report the current status of an initialized Architect project. It can report projects with core context but no tracks yet, or read `architect/tracks.md` and track plans when proposal artifacts exist. It never modifies files.

## Core Rules

- Follow the bundled resource `references/status-protocol.md` as the source of truth.
- Use Architect terminology consistently: `architect/`, `/architect-*`, and `Architect methodology`.
- This skill is read-only. Do not create, edit, move, delete, archive, or commit files.
- Architect-managed reads must stay under `architect/`; do not follow absolute paths, `..`, or track links outside `architect/tracks/`.
- Validate each operation result before continuing. If a read or command fails, correct it once when the error is clear; otherwise stop and report the blocker.
- Parse registry and plan formats produced by `architect-propose` and `architect-implement`.

## Execution

1. Read the bundled resource `references/status-protocol.md`.
2. Verify required Architect context files exist.
3. If no track management artifacts exist, report setup-ready status and recommend `/architect-discuss`.
4. Otherwise parse `architect/tracks.md`.
5. Read each track's `plan.md` and `metadata.json` when available.
6. Compute track and project progress.
7. Report current work, next action, blockers, and completion percentage.
