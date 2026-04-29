---
name: architect-implement
description: Implement or resume an existing Architect track by executing its approved plan and updating track status. Use when the user asks to implement, continue, resume, or complete a planned Architect track.
---

# Architect Implement

Use this skill to implement a track that already exists in an initialized Architect project. It executes the selected track's `plan.md` while keeping `architect/tracks.md`, track metadata, and project context synchronized.

## Core Rules

- Follow the bundled resource `references/implement-track-protocol.md` as the source of truth.
- Use Architect semantics consistently: `architect/`, `/architect-*`, `Architect methodology`, and `architect(...)` commit scopes.
- Require an initialized Architect context and a valid track before implementation.
- Use relative paths rooted in the user's project when editing Architect files. Architect-managed files must stay under `architect/`; do not use absolute paths, `..`, or track links outside `architect/tracks/`.
- Ask the user through the active agent runtime's user-interaction mechanism for decisions and workflow confirmations. If structured choices are unavailable, present the options in text and wait for the user's reply. Manual Mode preserves all human confirmations; Auto Mode bypasses phase-level human confirmations after the user selects it.
- Present detailed Markdown, drafts, diffs, reports, verification summaries, or risk analysis in a normal assistant message before asking for a decision. Use interactive prompts only for concise plain-text questions and short plain-text choices.
- Use the active agent runtime's safest reviewable file-editing mechanism, preferably patch-based, for manual file creation and edits. Do not use shell redirection to write files.
- Validate each operation result before continuing. If a step fails, correct it once when the error is clear; otherwise stop and report the blocker.
- Do not commit unless the user explicitly asks for a commit in the current conversation, has explicitly authorized commits for the current implementation workflow, or selected Auto Mode for phase checkpoint commits.
- Do not archive or delete track folders unless the user explicitly confirms that cleanup action.

## Execution

1. Read the bundled resource `references/implement-track-protocol.md`.
2. Verify required Architect context files exist.
3. Parse `architect/tracks.md` and select the target track.
4. Load the track's `spec.md`, `plan.md`, `metadata.json`, and `architect/workflow.md`.
5. Ask whether to run Manual Mode or Auto Mode.
6. Execute plan tasks according to the workflow.
7. Update task, track, registry, and metadata status.
8. Synchronize project documentation when the track is complete.
9. Offer review/archive/delete/skip cleanup choices safely.
