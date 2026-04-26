# Architect Implement Track Protocol

This protocol implements an existing Architect track by executing its `plan.md`, following `architect/workflow.md`, and keeping Architect project documents synchronized.

## 1. System Directive

You are implementing an Architect track. Follow the selected track's `plan.md` and the project's `architect/workflow.md` precisely, while respecting user confirmations and the active agent runtime's safety rules.

Validate every operation result. If an operation fails because of a recoverable path or command issue, self-correct once. If it remains unrecoverable, stop, report the failure, and wait for the user.

Use relative project paths such as `architect/tracks.md` and `architect/tracks/<track_id>/plan.md`. Architect-managed files must stay under `architect/`; never create or follow absolute paths, parent-directory paths (`..`), or track links outside `architect/tracks/`. Do not write files with shell redirection. Use the active agent runtime's safest reviewable file-editing mechanism, preferably patch-based, for manual file creation and edits.

Do not commit unless the user explicitly asks for a commit in the current conversation or has explicitly authorized commits for the current implementation workflow.

Do not run destructive cleanup such as deleting a track folder unless the user explicitly confirms that exact action.

## 2. Setup Check

Verify that Architect is initialized before implementing a track.

Required setup files:

- `architect/product.md`
- `architect/product-guidelines.md`
- `architect/tech-stack.md`
- `architect/workflow.md`
- `architect/index.md`
- `architect/tracks.md`

Required tracks directory:

- `architect/tracks/`

If any required setup file or tracks directory is missing, halt and tell the user:

```text
Architect is not set up or has no track registry. Please run `/architect-setup` or `/architect-propose` first.
```

Do not proceed when setup or track registry state is incomplete.

## 3. Track Selection

### 3.1 Parse Tracks Registry

Read `architect/tracks.md` and parse track entries separated by `---`.

For each track section, extract:

- Status marker: `[ ]`, `[~]`, or `[x]`.
- Track description from the Architect registry item format: `- [ ] **Track: <description>**`, `- [~] **Track: <description>**`, or `- [x] **Track: <description>**`.
- Track folder link, normally `./tracks/<track_id>/`.
- Track ID from the folder link.

Track IDs parsed from the registry must match `^[0-9]{8}_[a-z0-9_]+$`. Treat entries with invalid IDs as malformed and do not resolve their directories.

If no valid track sections are found, halt and tell the user:

```text
The tracks file is empty or malformed. No tracks are available to implement.
```

### 3.2 Select Track

If the user provided a track name or track ID in the prompt:

1. Match it case-insensitively against track IDs first. If no track ID matches, match against descriptions.
2. If exactly one match is found, ask for confirmation:
   - Title: `Confirm`
   - Prompt: `I found track '<track_description>'. Is this correct?`
   - Selection: single
   - Choices: `Yes`, `No`.
3. If no unique match is found, ask the user to choose from the available incomplete tracks or provide an exact track name.

If no track name was provided:

1. Select the first track not marked `[x]`.
2. Ask for confirmation:
   - Title: `Next Track`
   - Prompt: `No track name was provided. Proceed with the next incomplete track: '<track_description>'?`
   - Selection: single
   - Choices: `Yes`, `No`.
3. If the user says no, ask them to choose from available incomplete tracks or provide an exact track name.

If all tracks are marked `[x]`, halt and tell the user:

```text
No incomplete tracks found in architect/tracks.md. All tracks are complete.
```

Do not proceed without a selected track.

After selecting a track, verify the registry contains exactly one entry with the selected track ID. If selection was made by description and multiple entries share that description, halt and ask the user to select by track ID or fix `architect/tracks.md` before implementation.

If the selected track is marked `[x]`, ask for explicit reopening confirmation before loading it:

- Title: `Reopen Track`
- Prompt: `Track '<track_description>' is already complete. Do you want to reopen it for implementation?`
- Selection: single
- Choices: `Yes`, `No`.

If the user does not confirm reopening, halt without changing the track.

## 4. Load Track Context

Announce which track you are beginning to implement.

Resolve the selected track directory from the registry link only when the parsed `track_id` matches `^[0-9]{8}_[a-z0-9_]+$` and the link is `./tracks/<track_id>/` or the equivalent `architect/tracks/<track_id>/`. If the link is absolute, contains `..`, has an invalid track ID, or points outside `architect/tracks/`, halt and ask the user to fix `architect/tracks.md` before continuing.

Required track files:

- `spec.md`
- `plan.md`
- `metadata.json`
- `index.md`

Read:

- Track specification: `architect/tracks/<track_id>/spec.md`
- Track implementation plan: `architect/tracks/<track_id>/plan.md`
- Track metadata: `architect/tracks/<track_id>/metadata.json`
- Project workflow: `architect/workflow.md`
- Product context: `architect/product.md`
- Tech stack: `architect/tech-stack.md`
- Product guidelines: `architect/product-guidelines.md`

If any required track file is missing, halt and tell the user to run `/architect-setup` recovery or inspect the incomplete track before continuing.

## 5. Mark Track In Progress

Before implementation work starts:

- Update the selected track entry in `architect/tracks.md` from `[ ]` to `[~]` unless already `[~]`.
- Update `metadata.json` status to `in_progress` and refresh `updated_at`.
- Do not change `[x]` tracks back to in progress unless the user explicitly confirms reopening the completed track.

## 6. Execute Plan Tasks

The track's `plan.md` is the source of truth for implementation scope. `architect/workflow.md` is the source of truth for task lifecycle.

An actionable sub-task is an indented checkbox line using `[ ]`, `[~]`, or `[x]`. Plain bullets, notes, summaries, and explanatory lines are not actionable sub-tasks and do not participate in status progression.

Loop through tasks in `plan.md` sequentially.

For each task:

1. Resume the first parent task marked `[~]`. If no parent task is `[~]`, select the next parent task marked `[ ]`. If no parent task is `[~]` or `[ ]`, run a final scan of `plan.md`; if no parent task or actionable sub-task remains `[ ]` or `[~]`, stop the task loop and proceed to Section 8. If unfinished actionable work remains in an unrecognized structure, halt and report the malformed plan.
2. If the selected parent task was `[ ]`, mark it `[~]` in `plan.md` and save the file before changing application code.
3. Execute sub-tasks in order. Resume the first actionable sub-task marked `[~]`; otherwise select the next actionable sub-task marked `[ ]`. When a sub-task is `[ ]`, mark it `[~]`, save `plan.md`, complete the work, then mark it `[x]` and save `plan.md` again. Do not skip `[~]` sub-tasks.
4. Execute subtasks according to `architect/workflow.md`.
5. Use tests, verification, and documentation rules from the workflow.
6. Conduct every human-in-the-loop workflow step through the active agent runtime's user-interaction mechanism.
7. Do not mark multiple parent tasks complete in one batch; complete and record one parent task at a time.
8. When all sub-tasks for the parent task are complete, update the parent task from `[~]` to `[x]` and save `plan.md`. If the parent task has no actionable sub-tasks, complete the parent task itself according to `architect/workflow.md` before marking it `[x]`.
9. Record a task summary in the format required by the workflow. If no commit exists, use the workflow's `no-commit` convention.
10. After each parent task, check whether the completed task concludes a phase and whether Section 7 must run.

Implementation rules:

- Make the smallest correct code changes.
- Respect existing project conventions before adding new patterns.
- If implementation requires a tech stack change, stop implementation, propose the `architect/tech-stack.md` change, and get user approval before continuing.
- Do not skip manual verification steps required by the workflow.
- If tests fail, debug according to the workflow. If failures persist beyond the workflow's allowed attempts, stop and ask the user for guidance.

## 7. Phase Completion Protocol

When a completed task concludes a phase and `architect/workflow.md` defines a Phase Completion Verification and Checkpointing Protocol:

1. Execute that protocol immediately.
2. Present manual verification steps to the user through the active agent runtime's user-interaction mechanism.
3. Wait for explicit user confirmation before proceeding.
4. Create checkpoint commits only when commits are explicitly authorized for the current implementation workflow.

## 8. Finalize Track

After all parent tasks and actionable sub-tasks in the selected track's `plan.md` are marked `[x]`:

- Update the selected track entry in `architect/tracks.md` from `[~]` or `[ ]` to `[x]`.
- Update `metadata.json` status to `completed` and refresh `updated_at`.
- Summarize completed work and changed files.

If commits are explicitly authorized, commit the track completion update with:

```text
architect(implement): complete track <track_id>
```

Otherwise, do not commit.

If the track completion updates were not committed, report the changed Architect files, including `architect/tracks.md`, `architect/tracks/<track_id>/metadata.json`, and `architect/tracks/<track_id>/plan.md` when they changed.

## 9. Synchronize Project Documentation

Run this section only after the selected track reaches `[x]` in `architect/tracks.md`.

Announce that you are synchronizing project documentation with the completed track.

Read:

- Track specification: `architect/tracks/<track_id>/spec.md`
- Product definition: `architect/product.md`
- Tech stack: `architect/tech-stack.md`
- Product guidelines: `architect/product-guidelines.md`

Analyze the completed track specification for product behavior changes, technology changes, or product guideline impacts.

### 9.1 Product Definition

Update `architect/product.md` only when the completed track significantly changes the product's user-facing behavior, goals, or capabilities.

If an update is needed, ask for approval with the proposed diff embedded in the question:

- Title: `Product`
- Prompt: `Please review the proposed updates to Product Definition below. Do you approve?` Include the diff directly in the prompt body.
- Selection: single
- Choices: `Approve`, `Reject`.

Only edit the file after explicit approval.

### 9.2 Tech Stack

Update `architect/tech-stack.md` only when the completed track introduced or removed significant technology, framework, infrastructure, persistence, testing, or deployment decisions.

If an update is needed, ask for approval with the proposed diff embedded in the question:

- Title: `Tech Stack`
- Prompt: `Please review the proposed updates to Tech Stack below. Do you approve?` Include the diff directly in the prompt body.
- Selection: single
- Choices: `Approve`, `Reject`.

Only edit the file after explicit approval.

### 9.3 Product Guidelines

Treat `architect/product-guidelines.md` as sensitive. Routine features and bug fixes should not update it.

Propose changes only when the track specification explicitly changes branding, voice, tone, accessibility principles, UX principles, or core product identity.

If an update is needed, ask for approval with a clear warning and the proposed diff embedded in the question:

- Title: `Guidelines`
- Prompt: `WARNING: This affects core product guidelines. Please review the proposed changes below. Do you approve?` Include the diff directly in the prompt body.
- Selection: single
- Choices: `Approve`, `Reject`.

Only edit the file after explicit approval.

### 9.4 Documentation Sync Report

Report which files changed and which did not need updates.

If documentation files changed and commits are explicitly authorized, commit them with:

```text
architect(docs): sync docs for track <track_id>
```

Otherwise, do not commit.

If documentation files changed but were not committed, report the changed files so the user can review or commit them manually.

## 10. Track Cleanup

Run cleanup only after implementation and documentation synchronization are complete.

Ask the user what to do with the completed track:

- Title: `Track Cleanup`
- Prompt: `Track '<track_id>' is complete. What would you like to do?`
- Selection: single
- Choices:
  - `Review`: Run review before cleanup.
  - `Archive`: Move the track folder to `architect/archive/` and remove it from `architect/tracks.md`.
  - `Delete`: Permanently delete the track folder and remove it from `architect/tracks.md`.
  - `Skip`: Leave the completed track in place.

### 10.1 Review

If the user chooses `Review`, tell them:

```text
Please run `/architect-review` to verify changes. You can archive or delete the track after review.
```

Do not archive or delete the track during this run after the user chooses `Review`.

### 10.2 Archive

If the user chooses `Archive`:

1. Warn that this will move the track folder, including `spec.md`, `plan.md`, `metadata.json`, `index.md`, and any user notes or extra files inside it.
2. Check whether the track folder contains unexpected files beyond `spec.md`, `plan.md`, `metadata.json`, and `index.md`; include them in the confirmation prompt if present.
3. If Git is available, check whether the track folder has uncommitted changes; include that warning in the confirmation prompt if present.
4. If `architect/archive/<track_id>/` already exists, halt and ask the user whether to choose a different archive name, delete the existing archive manually, or skip cleanup.
5. Ask for confirmation before moving files:
   - Title: `Confirm Archive`
   - Prompt: `Archive architect/tracks/<track_id>/ to architect/archive/<track_id>/ and remove it from architect/tracks.md?`
   - Selection: single
   - Choices: `Yes`, `No`.
6. If the user does not confirm, leave the track unchanged.
7. Create `architect/archive/` if needed.
8. Move `architect/tracks/<track_id>/` to `architect/archive/<track_id>/`.
9. Remove the completed track section from `architect/tracks.md`.
10. Announce the archived path.

If commits are explicitly authorized, commit with:

```text
architect(cleanup): archive track <track_id>
```

Otherwise, do not commit.

### 10.3 Delete

If the user chooses `Delete`, ask for final confirmation with a warning:

Before asking, check whether the track folder contains unexpected files or uncommitted changes when Git is available, and include those details in the warning.

- Title: `Confirm`
- Prompt: `WARNING: This permanently deletes architect/tracks/<track_id>/, including spec.md, plan.md, metadata.json, index.md, and any user notes or extra files. This cannot be undone. Type or choose Yes only if you are sure.`
- Selection: single
- Choices: `Yes`, `No`.

Only if the user confirms:

1. Delete `architect/tracks/<track_id>/`.
2. Remove the completed track section from `architect/tracks.md`.
3. Announce deletion.

If commits are explicitly authorized, commit with:

```text
architect(cleanup): delete track <track_id>
```

Otherwise, do not commit.

If the user does not confirm, leave the track unchanged.

### 10.4 Skip

If the user chooses `Skip`, announce that the completed track will remain in `architect/tracks.md`.
