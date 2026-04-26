---
name: architect-propose
description: Propose and create a new Architect track for an initialized project, including its spec, plan, metadata, and registry entry. Use when the user asks to add, plan, or propose a new feature, bug fix, chore, refactor, docs, or test track.
---

# Architect Propose

Use this skill to create a new Architect track for an already initialized Architect project. A track is a focused unit of work, such as a feature, bug fix, chore, refactor, or setup milestone.

## Core Rules

- Follow the bundled resource `references/propose-track-protocol.md` as the source of truth.
- Use Architect semantics consistently: `architect/`, `/architect-*`, `Architect methodology`, and `architect(...)` commit scopes.
- Require an initialized Architect context before creating a track.
- Use relative paths rooted in the user's project when creating Architect files. Architect-managed files must stay under `architect/`; do not use absolute paths, `..`, or track links outside `architect/tracks/`.
- Ask the user through the active agent runtime's user-interaction mechanism. If structured choices are unavailable, present the options in text and wait for the user's reply.
- Use the active agent runtime's safest reviewable file-editing mechanism, preferably patch-based, for manual file creation and edits. Do not use shell redirection to write files.
- Validate each operation result before continuing. If a step fails, correct it once when the error is clear; otherwise stop and report the blocker.
- Do not commit unless the user explicitly asks for a commit in the current conversation.

## Execution

1. Read the bundled resource `references/propose-track-protocol.md`.
2. Verify required Architect context files exist.
3. Gather or use the track description.
4. Generate and confirm `spec.md`.
5. Generate and confirm `plan.md` from `architect/workflow.md`.
6. Create the track directory and artifacts.
7. Update `architect/tracks.md`.
8. Summarize created files and next steps.
