---
name: architect-setup
description: Initialize or resume Architect project setup by creating the core architect/ context and first track. Use when the user asks to set up Architect, scaffold Architect context, or recover an interrupted setup.
---

# Architect Setup

Use this skill to initialize or resume an Architect project setup. Architect is a project-planning workflow that stores durable project context in an `architect/` directory and organizes implementation work as tracks under `architect/tracks/`.

## Core Rules

- Follow the bundled resource `references/setup-protocol.md` as the source of truth for the setup sequence.
- Use Architect semantics consistently: `architect/`, `/architect-*`, `Architect methodology`, and `architect(...)` commit scopes.
- Use relative paths rooted in the user's project when creating Architect files. Architect-managed files must stay under `architect/`; do not use absolute paths, `..`, or track links outside `architect/tracks/`.
- Ask the user through the active agent runtime's user-interaction mechanism. If structured choices are unavailable, present the options in text and wait for the user's reply.
- Present detailed Markdown, drafts, diffs, reports, or risk analysis in a normal assistant message before asking for a decision. Use interactive prompts only for concise plain-text questions and short plain-text choices.
- Use the active agent runtime's safest reviewable file-editing mechanism, preferably patch-based, for manual file creation and edits. Do not use shell redirection to write files.
- Validate each operation result before continuing. If a step fails, correct it once when the error is clear; otherwise stop and report the blocker.
- Do not commit unless the user explicitly asks for a commit in the current conversation.

## Bundled Templates

- Bundled resource `references/workflow.md` is the default Architect workflow template.
- Bundled resources under `references/code_styleguides/*.md` are code style guides. Enumerate this bundled resource directory at setup time so newly added guides are automatically available.

## Execution

1. Read the bundled resource `references/setup-protocol.md`.
2. Audit the target project for existing `architect/` artifacts.
3. Resume from the correct setup stage or initialize from scratch.
4. Generate the first track and its artifacts when setup reaches track creation.
5. Summarize created files and next steps.
