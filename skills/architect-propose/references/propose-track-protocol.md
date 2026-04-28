# Architect Propose Track Protocol

This protocol creates a new Architect track for a project that has already run Architect setup.

## 1. System Directive

You are creating a new Architect track. Guide the user from a short track description to confirmed `spec.md` and `plan.md`, then create the track artifacts under `architect/tracks/<track_id>/` and update `architect/tracks.md`.

Validate every operation result. If an operation fails because of a recoverable path or command issue, self-correct once. If it remains unrecoverable, stop, report the failure, and wait for the user.

Use relative project paths such as `architect/tracks.md` and `architect/tracks/<track_id>/spec.md`. Architect-managed files must stay under `architect/`; never create or follow absolute paths, parent-directory paths (`..`), or track links outside `architect/tracks/`. Do not write files with shell redirection. Use the active agent runtime's safest reviewable file-editing mechanism, preferably patch-based, for manual file creation and edits.

Do not commit changes unless the user explicitly requests a commit in the current conversation.

## 2. Setup Check

Verify that Architect is initialized before creating a track.

Required setup files:

- `architect/product.md`
- `architect/product-guidelines.md`
- `architect/tech-stack.md`
- `architect/workflow.md`
- `architect/index.md`

Recoverable management artifacts:

- `architect/tracks.md`
- `architect/tracks/`

If any required setup file is missing, halt and tell the user:

```text
Architect is not set up. Please run `/architect-setup` to set up the environment.
```

Do not proceed to track creation when setup is incomplete.

If recoverable management artifacts are missing but required setup files exist, recreate them during Section 7.1.

Before proposing a new track, inspect `architect/tracks/` when it exists. If any incomplete `architect/tracks/<track_id>/` folder exists, halt and tell the user to resume or clean up that incomplete track before creating a new one. Suggest running `/architect-setup` to resume setup recovery if the incomplete track came from interrupted setup. A track folder is incomplete when it is missing any of `spec.md`, `plan.md`, `metadata.json`, or `index.md`.

## 3. Load Project Context

Read and use the existing Architect context:

- Product definition: `architect/product.md`
- Product guidelines: `architect/product-guidelines.md`
- Tech stack: `architect/tech-stack.md`
- Workflow: `architect/workflow.md`
- Tracks registry when present: `architect/tracks.md`

Use this context to ask relevant questions and avoid asking for information already documented.

## 4. Get Track Description and Infer Type

If the user already supplied a track description in the prompt, use it.

If no description was supplied, ask the user for it through the active agent runtime's user-interaction mechanism. Provide 2-3 common examples as inspiration, but prefer the user's custom answer as the actual description:

- Title: `Description`
- Prompt: `Please provide a brief description of the track you want to start.`
- Choices such as `Implement user authentication`, `Fix a production bug`, and `Refactor a core module`.

If the user chooses an example rather than a custom answer, ask one follow-up question for specifics before inferring type or drafting the spec.

Infer the track type from the description. Do not ask the user to classify it unless the description is ambiguous and the type changes planning materially.

Supported types:

- `feature`
- `bug`
- `chore`
- `refactor`
- `docs`
- `test`

Default to `feature` when the type is unclear.

## 5. Generate `spec.md`

Announce that you will gather details for the track specification.

Ask context-aware questions through the active agent runtime's user-interaction mechanism. Batch up to four related questions when structured interaction is available. Prefer choice questions with 2-4 strong options and allow custom input when useful.

Questioning rules:

- Use additive multi-select questions for scope, user groups, requirements, affected surfaces, and acceptance criteria.
- Use single-choice questions for mutually exclusive decisions.
- Allow custom text for reproduction steps, constraints, and custom acceptance criteria when predefined choices would be too restrictive.
- For feature tracks, ask about intended behavior, users, inputs/outputs, impacted UI or APIs, and success criteria.
- For bug tracks, ask about reproduction steps, actual behavior, expected behavior, affected environment, and severity.
- For chores/refactors/docs/tests, ask about scope, constraints, affected files or modules, validation, and definition of done.

Before drafting, summarize your understanding briefly, then draft. Do not add a separate approval step before the specification approval loop unless a required decision is missing.

Draft `spec.md` with this structure:

```markdown
# Specification: <Track Description>

## Overview
## Goals
## Requirements
## Non-Functional Requirements
## Acceptance Criteria
## Out of Scope
## Risks and Assumptions
```

For bug tracks, include these sections instead when more appropriate:

```markdown
# Specification: <Track Description>

## Overview
## Reproduction
## Actual Behavior
## Expected Behavior
## Acceptance Criteria
## Out of Scope
## Risks and Assumptions
```

Ask for approval with the full draft embedded in the question:

- Title: `Confirm Spec`
- Selection: single
- Choices:
  - `Approve`: The specification is correct; proceed to planning.
  - `Revise`: The specification needs changes.

If the user chooses `Revise`, ask for the requested changes, update the draft, and repeat approval.

## 6. Generate `plan.md`

After `spec.md` is approved, generate an implementation plan from the approved spec and `architect/workflow.md`.

Plan rules:

- Use phases, tasks, and sub-tasks.
- Include status markers `[ ]` for every task and sub-task.
- Parent task format: `- [ ] Task: ...`
- Sub-task format: `    - [ ] ...`
- Follow the workflow. If it uses TDD, include test-writing before implementation work.
- If `architect/workflow.md` defines a Phase Completion Verification and Checkpointing Protocol, append this meta-task to every phase:
  - `- [ ] Task: Architect - User Manual Verification '<Phase Name>' (Protocol in workflow.md)`

Recommended structure:

```markdown
# Implementation Plan: <Track Description>

## Phase 1: <Phase Name>
- [ ] Task: <task>
    - [ ] <sub-task>
    - [ ] <sub-task>
- [ ] Task: Architect - User Manual Verification '<Phase Name>' (Protocol in workflow.md)
```

Ask for approval with the full draft embedded in the question:

- Title: `Confirm Plan`
- Selection: single
- Choices:
  - `Approve`: The plan is correct; create the track artifacts.
  - `Revise`: The plan needs changes.

If the user chooses `Revise`, ask for the requested changes, update the draft, and repeat approval.

## 7. Create Track Artifacts

### 7.1 Resolve Track Paths

Use these fixed Architect management paths:

- Tracks registry: `architect/tracks.md`
- Tracks directory: `architect/tracks/`

Create `architect/tracks/` if it does not exist and the setup context is otherwise valid.

If `architect/tracks.md` is missing but setup context is otherwise valid, create it with:

```markdown
# Project Tracks

This file tracks all major tracks for the project. Each track has its own detailed plan in its respective folder.
```

After creating or recovering `architect/tracks.md`, ensure `architect/index.md` links to it under `## Management`. If `## Management` is missing, create that section before adding the links:

```markdown
- [Tracks Registry](./tracks.md)
- [Tracks Directory](./tracks/)
```

### 7.2 Generate Track ID

Generate one track ID from the approved description with format `YYYYMMDD_shortname`.

Build `shortname` by lowercasing the description, keeping ASCII letters and numbers, replacing spaces with underscores, stripping punctuation, and using at most four meaningful words. The final `track_id` must match `^[0-9]{8}_[a-z0-9_]+$`.

Before creating any track artifacts, run a collision check against both `architect/tracks/` and `architect/tracks.md`:

- Existing track directories must not contain the same track ID.
- Existing track directories must not contain the same short name after the date prefix.
- The tracks registry must not already mention the same track ID or short name.

If any collision exists, halt and explain that a matching track already exists. Suggest choosing a different description or resuming the existing track.

Use the exact same track ID for every artifact.

### 7.3 Metadata

Create `architect/tracks/<track_id>/metadata.json`:

```json
{
  "track_id": "<track_id>",
  "type": "<type>",
  "status": "new",
  "created_at": "YYYY-MM-DDTHH:MM:SSZ",
  "updated_at": "YYYY-MM-DDTHH:MM:SSZ",
  "description": "<Track Description>"
}
```

Use the current timestamp for `created_at` and `updated_at`.
Use the inferred supported type from Section 4 for `type`.

### 7.4 Files

Create these files in `architect/tracks/<track_id>/`:

- `spec.md`: confirmed specification.
- `plan.md`: confirmed implementation plan.
- `metadata.json`: track metadata.
- `index.md`: track index.

`index.md` content:

```markdown
# Track <track_id> Context

- [Specification](./spec.md)
- [Implementation Plan](./plan.md)
- [Metadata](./metadata.json)
```

## 8. Update Tracks Registry

Append the new track to `architect/tracks.md`:

```markdown

---

- [ ] **Track: <Track Description>**
  *Link: [./tracks/<track_id>/](./tracks/<track_id>/)*
```

Do not append unless the Section 7.2 collision check passed.

## 9. Completion

Announce completion:

```text
New track '<track_id>' has been created and added to architect/tracks.md. You can now start implementation by running `/architect-implement`.
```

Summarize created or updated files.

If the user explicitly requested a commit, commit Architect files with:

```text
architect(propose): add track <track_id>
```

Otherwise, do not commit. In the completion summary, explicitly state that the track files were created but not committed because commit authorization was not given in the current conversation. Offer that the user can request a commit with `architect(propose): add track <track_id>` if they want the planning artifacts recorded in Git.
