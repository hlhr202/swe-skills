# Architect Propose Track Protocol

## Purpose

Turn a confirmed initiative into a new Architect track with an approved specification, approved implementation plan, metadata, index, and registry entry.

## Success Criteria

A proposal succeeds when:

- Required Architect core context exists.
- The user has approved `spec.md` and then `plan.md`.
- A safe, collision-free track ID is used consistently.
- `spec.md`, `plan.md`, `metadata.json`, and `index.md` exist under one track directory.
- `architect/tracks.md` contains exactly one matching registry entry.
- `architect/index.md` links to track management artifacts.
- The completion message lists created or updated files and the next action.

## Hard Boundaries

- Require initialized Architect core context before proposal work.
- Do not create track artifacts before both the specification and plan are approved.
- Keep Architect-managed writes under `architect/`. Reject absolute paths, parent traversal (`..`), and track links outside `architect/tracks/`.
- Do not inspect unrelated tracks for completeness or block a new independent proposal because another track is unfinished. Only ID or short-name collision may block creation.
- Use a reviewable edit mechanism, preferably patch-based. Do not write files with shell redirection.
- Validate every operation. Retry once only for a clear, recoverable error; otherwise stop.
- Do not commit unless the user explicitly requests a commit in the current conversation.

## State Model

The proposal state machine is:

```text
context_ready -> spec_draft -> spec_approved -> plan_draft -> plan_approved -> track_created -> registered
```

- `spec_approved` is reached only after the `Confirm Spec` approval.
- `plan_approved` is reached only after the `Confirm Plan` approval.
- `track_created` may occur only after `plan_approved` and a successful collision check.
- `registered` is the terminal proposal state.

Track metadata begins in state `new`; the registry marker begins as `[ ]`.

## Decision Rules

### Setup

Required core files:

- `architect/product.md`
- `architect/product-guidelines.md`
- `architect/tech-stack.md`
- `architect/workflow.md`
- `architect/index.md`

Missing `architect/tracks.md` or `architect/tracks/` is recoverable during artifact creation. Missing core context is not: halt and recommend `/architect-setup`.

### Description and type

- Use a description already supplied by the user.
- Otherwise ask with Title `Description` and Prompt `Please provide a brief description of the track you want to start.`, offering 2–3 examples and custom text.
- If the user selects a generic example, ask one follow-up for specifics.
- Infer type without asking unless type materially changes the plan.
- Supported types: `feature`, `bug`, `chore`, `refactor`, `docs`, `test`. Default to `feature` when unclear.

### Questions

- Ask only questions that change scope, behavior, constraints, validation, or definition of done.
- Use additive multi-select for combinable scope, users, requirements, surfaces, and acceptance criteria.
- Use single choice for mutually exclusive decisions.
- Use free text for reproduction steps or constraints that do not fit predefined choices.
- Do not ask for facts already established by Architect context.

### Track ID

Generate `YYYYMMDD_shortname` from the approved description. Lowercase the short name, keep ASCII letters and numbers, replace spaces with underscores, strip punctuation, and retain at most four meaningful words. The result must match `^[0-9]{8}_[a-z0-9_]+$`.

Before writing track artifacts, check both `architect/tracks/` and `architect/tracks.md` for:

- The same full track ID.
- The same short name after the date prefix.
- A registry mention of the same ID or short name.

Any collision halts creation and suggests a different description or resuming the existing track.

## Approval Boundaries

| Action | Required approval |
| --- | --- |
| Use specification for planning | `Confirm Spec` → `Approve` |
| Create artifacts from plan | `Confirm Plan` → `Approve` |
| Commit proposal artifacts | User explicitly requests a commit in the current conversation |

Approval of the spec does not approve the plan. Approval of both documents authorizes creating the listed proposal artifacts, not implementation, cleanup, or unrelated changes.

## Workflow

### 1. Verify and load context

Verify core files, then read product, product guidelines, tech stack, workflow, and the registry when present.

### 2. Establish the track

Gather the description and infer its supported type using the decision rules above.

### 3. Draft and approve `spec.md`

Ask context-aware questions. Feature tracks normally cover behavior, users, inputs and outputs, affected UI or APIs, and success criteria. Bug tracks cover reproduction, actual and expected behavior, environment, and severity. Other types cover scope, constraints, affected modules, validation, and definition of done.

Briefly summarize the stable understanding, then present the full draft. Use this default structure:

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

For bugs, replace Goals, Requirements, and Non-Functional Requirements with Reproduction, Actual Behavior, and Expected Behavior when that is clearer.

Ask:

- Title: `Confirm Spec`
- Prompt: `Is this specification ready to use for planning?`
- Choices: `Approve`, `Revise`

On `Revise`, gather changes, update the full draft, and repeat. Do not add another approval gate before this loop.

### 4. Draft and approve `plan.md`

After `spec_approved`, derive the plan from the approved spec and `architect/workflow.md`.

- Use phases, parent tasks, and sub-tasks.
- Mark every actionable line `[ ]`.
- Format parents as `- [ ] Task: ...` and sub-tasks as `    - [ ] ...`.
- Follow workflow ordering, including tests before implementation when TDD is configured.
- When the workflow defines Phase Completion Verification and Checkpointing, end every phase with:

```markdown
- [ ] Task: Architect - User Manual Verification '<Phase Name>' (Protocol in workflow.md)
```

Present the complete plan, then ask:

- Title: `Confirm Plan`
- Prompt: `Is this implementation plan ready to create track artifacts?`
- Choices: `Approve`, `Revise`

On `Revise`, update the plan and repeat.

### 5. Recover management paths and check collision

After `plan_approved`:

1. Create `architect/tracks/` if missing.
2. If `architect/tracks.md` is missing, create:

```markdown
# Project Tracks

This file tracks all major tracks for the project. Each track has its own detailed plan in its respective folder.
```

3. Ensure `architect/index.md` contains a `## Management` section linking to `./tracks.md` and `./tracks/`.
4. Generate and validate one track ID.
5. Run the complete collision check.

### 6. Create artifacts

Create `architect/tracks/<track_id>/` with the approved `spec.md`, approved `plan.md`, and:

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

Use the current timestamp for both initial timestamp fields.

Create `index.md`:

```markdown
# Track <track_id> Context

- [Specification](./spec.md)
- [Implementation Plan](./plan.md)
- [Metadata](./metadata.json)
```

### 7. Register and finish

Append only after collision checks pass:

```markdown

---

- [ ] **Track: <Track Description>**
  *Link: [./tracks/<track_id>/](./tracks/<track_id>/)*
```

Announce that the track was created and can be implemented with `/architect-implement`. List created or updated files.

If the user explicitly requests a commit, use:

```text
architect(propose): add track <track_id>
```

Otherwise state that the proposal artifacts were not committed because commit authorization was not given, and mention the optional commit message.

## Stop Conditions

Stop without partial track creation when:

- Required core context is missing.
- A required decision prevents a stable specification or plan.
- The user does not approve the specification or plan.
- The generated path or registry link is unsafe.
- A track ID or short-name collision exists.
- An operation remains unsuccessful after one clear correction.

Do not proceed from proposal into implementation automatically.
