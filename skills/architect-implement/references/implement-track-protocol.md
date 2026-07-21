# Architect Implement Track Protocol

## Purpose

Implement or resume one existing Architect track from its approved `plan.md`, follow `architect/workflow.md`, keep track and project context synchronized, verify the result, and finish with the authorized track-scoped terminal state.

## Success Criteria

Implementation succeeds when:

- One valid track is selected and its context is loaded.
- The user selects Manual or Auto Mode before work begins.
- Every status-managed task unit and phase verification gate reaches completion in order.
- Required tests, coverage, and manual or automated verification succeed or their accepted limitations are recorded.
- Registry, plan, metadata, and routine project documentation reflect the completed work.
- The final track-scoped commit is verified, unless the user explicitly opts out.
- Unrelated pre-existing changes remain preserved and unstaged.
- Cleanup occurs only when separately confirmed.

## Hard Boundaries

- Require initialized Architect core context and a valid existing track.
- Treat the selected `plan.md` as implementation scope and `architect/workflow.md` as task-lifecycle authority.
- Keep Architect-managed reads and writes under `architect/`. Reject absolute paths, parent traversal (`..`), invalid IDs, and links outside `architect/tracks/`.
- Capture the Git worktree before editing. Never modify, stage, or commit unrelated or ambiguous pre-existing changes.
- Never use broad staging such as `git add .` or `git add -A`.
- Do not skip pending or active status-managed units, phase protocol meta-tasks, or Manual Mode confirmation gates.
- Do not start a later phase while an earlier phase verification gate is incomplete.
- Do not make a significant technology-stack change without approval.
- Do not change sensitive product guidelines without approval in either mode.
- Do not archive or delete a track without explicit confirmation of that exact action.
- Use reviewable edits, preferably patch-based; do not write files with shell redirection.
- Validate every operation. Retry once only for a clear recoverable path or command issue; otherwise stop.

## State Model

### Track and metadata

```text
new -> in_progress -> completed
[ ] -> [~] -> [x]
```

Registry marker and metadata status move together. A completed track may return to `in_progress` only after explicit reopening confirmation.

### Task status granularity

Read the declaration near the top of `plan.md`:

```markdown
> Task status granularity: `<task|sub-task>`
```

An older plan without the declaration defaults to `sub-task` for backward compatibility. Any other declared value makes the plan malformed.

- **Task granularity:** parent tasks and phase protocol meta-tasks are the only state-managed units. Nested plain bullets are required implementation details of their parent, not separate state transitions.
- **Sub-task granularity:** parent tasks, actionable checkbox sub-tasks, and phase protocol meta-tasks follow the existing state workflow. Plain nested bullets remain contextual details.

### Tasks and sub-tasks

```text
[ ] -> [~] -> [x]
```

- `[ ]`: pending.
- `[~]`: active and must be resumed before later work.
- `[x]`: completed and recorded.

The state transition applies only to units managed by the selected Task status granularity. A phase is complete when every required status-managed checkbox is `[x]` and its phase protocol meta-task, when present, is `[x]`.

The generated phase protocol meta-task is exactly `Task: Architect - User Manual Verification '<Phase Name>' (Protocol in workflow.md)`. Treat Markdown headings beginning with `##` as phase boundaries.

### Workflow states

```text
selected
  -> mode_selected
  -> in_progress
  -> task_loop
  -> phase_verified (repeat per phase)
  -> completed
  -> docs_synchronized
  -> final_commit_verified | completed_without_commit
  -> cleanup_or_stop
```

## Decision Rules

### Setup and track validity

Core implementation context requires product, product guidelines, tech stack, workflow, index, registry, and tracks directory. Missing core context routes to `/architect-setup`; missing registry or tracks directory routes to `/architect-propose`.

A valid track registry entry has one marker, description, safe link, and ID matching `^[0-9]{8}_[a-z0-9_]+$`:

```markdown
- [ ] **Track: <description>**
  *Link: [./tracks/<track_id>/](./tracks/<track_id>/)*
```

Accept `[ ]`, `[~]`, or `[x]`. Resolve only `./tracks/<track_id>/` or equivalent `architect/tracks/<track_id>/` links. The selected track must contain `spec.md`, `plan.md`, `metadata.json`, and `index.md`. Setup cannot repair missing track artifacts; halt and report an incomplete track.

### Track selection

- User supplies an ID or name: match IDs case-insensitively first, then descriptions. For exactly one match, ask `I found track '<description>'. Is this correct?` with `Yes` or `No`.
- No target supplied: choose the first non-complete track and ask whether to proceed.
- No unique match: ask the user to choose from incomplete tracks or provide an exact ID.
- Duplicate selected ID or duplicate description after description matching: halt and require an exact ID or registry repair.
- Selected `[x]` track: ask `Reopen Track`; proceed only on explicit `Yes`.
- All tracks `[x]`: stop; no incomplete track exists.

Use these prompt contracts:

| Situation | Title | Prompt | Choices |
| --- | --- | --- | --- |
| Unique supplied match | `Confirm` | `I found track '<track_description>'. Is this correct?` | `Yes`, `No` |
| No supplied target | `Next Track` | `No track name was provided. Proceed with the next incomplete track: '<track_description>'?` | `Yes`, `No` |
| Completed target | `Reopen Track` | `Track '<track_description>' is already complete. Do you want to reopen it for implementation?` | `Yes`, `No` |

### Worktree ownership

Classify baseline changes against the track spec and plan as related, unrelated, or ambiguous.

- Preserve unrelated changes without staging or modification.
- Include pre-existing related work only after inspecting and verifying it in this workflow.
- If implementation must overlap an ambiguous file or hunk, ask once before editing or committing that overlap.
- If safe isolation is impossible, implementation may continue only where safe, but finalization must stop before a mixed commit.

### Task selection

- Before selecting normal work, scan phases in file order for an earlier phase whose non-meta work is complete but whose phase protocol meta-task is `[ ]` or `[~]`; select that meta-task first.
- Otherwise resume the first `[~]` parent task, then choose the next `[ ]` parent task.
- With `sub-task` granularity, within a parent resume the first `[~]` actionable sub-task, then choose the next `[ ]` sub-task.
- With `task` granularity, execute the parent as one unit and complete all nested plain-bullet details without separate status updates.
- Plain nested bullets are required task details in `task` granularity. In `sub-task` granularity, plain bullets, notes, summaries, and prose are contextual and not separately actionable.
- A `task` plan containing nested checkbox sub-tasks conflicts with its declaration and is malformed.
- If no recognized task remains but unfinished checkbox work exists in an unrecognized structure, halt as malformed.

### Implementation modes

- Manual Mode preserves every human confirmation in the workflow.
- Auto Mode bypasses phase-level human confirmation only; it performs or safely substitutes verification and creates required phase checkpoint commits.
- In Auto Mode, continue until finalization; task size and unfinished phases are not stop conditions.
- Both modes stop at safety boundaries and unrecoverable failures.

## Approval Boundaries

| Action | Authorization |
| --- | --- |
| Select exact matched track | Explicit `Yes` to track confirmation |
| Reopen completed track | Explicit `Yes` to `Reopen Track` |
| Start implementation | Manual or Auto Mode selection |
| one final, track-scoped implementation commit | The implementation request, unless the user opts out |
| Auto phase checkpoint commits | Auto Mode selection |
| Manual Mode checkpoint commits | Separate explicit commit authorization |
| Ordinary task or plan commits | Separate explicit commit authorization in either mode |
| Routine product/tech documentation sync | Auto Mode; Manual requires diff approval |
| Sensitive product-guideline change | Explicit approval in both modes |
| Significant tech-stack change | Explicit approval before implementation continues |
| Archive or delete | Explicit confirmation of the exact cleanup action |

Auto Mode additionally authorizes phase checkpoint commits. It does not authorize ordinary task commits, unrelated commits, cleanup, archive, or delete.

## Workflow

### 1. Verify Architect context

Check required core files, registry, and tracks directory. When the missing state is ambiguous, say:

```text
Architect has no implementable track. Run `/architect-setup` if core context is missing, or `/architect-propose` to create the first track after scope is confirmed.
```

### 2. Parse and select a track

Parse registry sections separated by `---`, validate markers, descriptions, links, and IDs, then apply the selection rules. Do not proceed without a confirmed selection.

### 3. Load track and project context

Announce the track. Resolve only the validated registry link. Read track spec, plan, metadata, index, workflow, product, tech stack, and product guidelines.

### 4. Capture the worktree baseline

If Git is available, record `git status --short`, inspect existing diffs as needed, and classify ownership before editing.

### 5. Select implementation mode

Ask:

- Title: `Implementation Mode`
- Prompt: `How should Architect implement this track?`
- Choices:
  - `Manual`: preserve phase-level human verification; checkpoint and ordinary task commits need explicit authorization.
  - `Auto`: execute the full plan without phase-level human confirmation; verify automatically and create phase checkpoint commits.

Do not mark the track active until a mode is selected.

Auto Mode still stops when verification remains failing after allowed fixes, a significant tech change is needed, cleanup is destructive, product guidelines would materially change, a path or plan is unsafe, or an operation remains unrecoverable.

### 6. Mark Track In Progress

Change the selected registry marker to `[~]`, metadata status to `in_progress`, and refresh `updated_at`. Do not reopen `[x]` without prior confirmation.

### 7. Execute Plan Tasks

Loop sequentially:

1. Select work using the task rules.
2. Change a pending parent to `[~]` and save `plan.md` before application-code edits.
3. For a phase protocol meta-task, skip normal implementation and run Section 8.
4. With `sub-task` granularity, for each actionable sub-task persist `[ ] -> [~]`, perform the work, then persist `[~] -> [x]`.
5. With `task` granularity, perform all nested details as part of the active parent and do not add or update sub-task checkboxes.
6. Follow workflow tests, coverage, documentation, and verification requirements.
7. Manual Mode uses the runtime interaction mechanism for required human gates. Auto Mode handles only phase-level gates automatically.
8. Complete and record one parent task at a time; do not batch-complete parents.
9. Mark the parent `[x]` only after all work selected by its granularity is complete.
10. Record the workflow task summary and use `no-commit` when no commit exists.
11. Rescan the phase. Run the phase protocol before any later-phase work.

Make the smallest correct change and follow repository conventions. For persistent verification failure, stop after the workflow's allowed attempts.

### 8. Phase Completion Protocol

Run when a phase protocol meta-task is selected or a phase without one completes and the project workflow defines phase verification.

1. Announce phase verification.
2. Identify phase-changed code, verify corresponding tests, and add missing tests in project style.
3. Announce and run required tests or coverage. Allow at most two fix cycles before asking for guidance.
4. Generate manual verification from product, guidelines, and completed phase tasks.
5. Manual Mode: present steps and wait for explicit confirmation.
6. Auto Mode: execute feasible steps with tests, coverage, browser, CLI, API, or inspection; use the closest safe substitute and record limitations when direct execution is impossible.
7. Auto Mode: create `architect(checkpoint): complete phase <phase_name>`.
8. Manual Mode: create that checkpoint only when commits are explicitly authorized; otherwise report the skipped checkpoint and continue after verification approval.
9. Record a checkpoint hash only after its commit succeeds. The hash line remains for a later authorized or final commit because the hash cannot exist inside its own checkpoint.

For the generated phase protocol meta-task:

1. Mark it `[~]` before verification.
2. Run the entire phase protocol.
3. Manual: after confirmation, mark `[x]` with checkpoint SHA or `no-commit`.
4. Auto: after verification and successful checkpoint, mark `[x]` and append the SHA as a follow-up plan update.
5. A failed Auto checkpoint is a blocker; do not proceed without it.

### 9. Finalize Track

After every unit managed by the selected Task status granularity is `[x]`:

- Mark the registry `[x]`.
- Set metadata to `completed` and refresh `updated_at`.
- Summarize work and changed files.
- Keep completion bookkeeping uncommitted until after documentation sync so the final commit captures the terminal state.

### 10. Synchronize Project Documentation

Run only after the registry reaches `[x]`. Compare the completed spec with product, tech stack, and product guidelines.

- Product definition: update only for significant user-facing behavior, goals, or capabilities. Manual Mode requires proposed-diff approval; Auto Mode may apply routine already-implemented updates and must report them.
- Tech stack: update only for significant technology, infrastructure, persistence, testing, or deployment decisions. Manual Mode requires approval. Auto Mode may document decisions already made within the track, but a significant new stack decision still requires approval before implementation.
- Product guidelines: change only when the spec explicitly changes branding, voice, accessibility, UX principles, or product identity. Present a warning and diff; require approval in both modes.

For Manual Mode approvals, and for guidelines in either mode, use:

| Document | Title | Prompt | Choices |
| --- | --- | --- | --- |
| Product definition | `Product` | `Approve the proposed Product Definition updates?` | `Approve`, `Reject` |
| Technology stack | `Tech Stack` | `Approve the proposed Tech Stack updates?` | `Approve`, `Reject` |
| Product guidelines | `Guidelines` | `Approve these Product Guidelines changes?` | `Approve`, `Reject` |

Report changed and unchanged documents. Keep routine sync in the final commit unless the user explicitly requested another commit structure.

### 11. Final Implementation Commit

Run only after implementation, bookkeeping, required verification, and documentation synchronization succeed.

Unless the user opts out:

1. Compare the current worktree with the captured baseline.
2. Build a candidate from inspected track-owned implementation, registry, plan, metadata, last checkpoint-hash update, and approved routine docs.
3. Exclude unrelated or ambiguous files and hunks. Never use broad staging.
4. Inspect staged files and diff; run `git diff --cached --check`; correct unsafe staging before continuing.
5. Commit:

```text
architect(implement): complete track <track_id>
```

6. Verify the commit and `git status --short`.
7. If selected-track changes remain, include them in a safe follow-up track-scoped commit or stop and explain why isolation is impossible.
8. Do not create an empty commit; if `HEAD` already contains the complete terminal state, verify and report it.

Unsafe staging or commit failure is a finalization blocker. Do not report full workflow success until the scoped commit is verified. If the user opts out, list remaining track changes and report completion without a final commit.

### 12. Track Cleanup

After finalization, ask:

- Title: `Track Cleanup`
- Prompt: `Track '<track_id>' is complete. What would you like to do?`
- Choices: `Review`, `Archive`, `Delete`, `Skip`

#### Review

Tell the user to run `/architect-review`; do not clean up in this run.

#### Archive

Before explicit confirmation, warn that the full track directory will move, report unexpected files and uncommitted changes, and halt on an existing archive destination. Ask with Title `Confirm Archive`, Prompt `Archive architect/tracks/<track_id>/ to architect/archive/<track_id>/ and remove it from architect/tracks.md?`, and Choices `Yes`, `No`. On `Yes`, perform and verify the move. Commit `architect(cleanup): archive track <track_id>` only when separately authorized.

#### Delete

Before explicit confirmation, report unexpected or uncommitted contents. Ask with Title `Confirm`, Prompt `WARNING: This permanently deletes architect/tracks/<track_id>/, including spec.md, plan.md, metadata.json, index.md, and any user notes or extra files. This cannot be undone. Type or choose Yes only if you are sure.`, and Choices `Yes`, `No`. On `Yes`, delete it and remove the registry section. Commit `architect(cleanup): delete track <track_id>` only when separately authorized.

#### Skip

Leave the completed track registered.

## Stop Conditions

Stop and report the exact state when:

- Required Architect or track context is missing, malformed, or unsafe.
- No track is selected or reopening is declined.
- No implementation mode is selected.
- Worktree ownership is ambiguous where editing or committing is required.
- A task or phase structure is malformed.
- Verification remains failing after allowed fix attempts.
- A significant tech-stack or sensitive-guideline change lacks approval.
- An Auto Mode checkpoint fails.
- The final commit cannot be isolated or verified.
- Cleanup lacks exact confirmation or collides with existing data.
- An operation remains unsuccessful after one clear correction.
- The authorized workflow is complete.
