# Project Workflow

## Outcome

Complete each approved track through traceable task states, test-first implementation, phase verification, project-context synchronization, and a verified track-scoped terminal commit.

## Engineering Principles

- `plan.md` is the source of truth for implementation scope and progress.
- Document significant technology decisions in `tech-stack.md` before implementing them.
- Use TDD: establish failing tests, implement the minimum passing behavior, then refactor safely.
- Target more than 80% coverage for new code.
- Prioritize user experience and project conventions.
- Prefer non-interactive, CI-safe commands; use `CI=true` for watch-mode tools.

## Hard Boundaries

- Preserve state order: `[ ] -> [~] -> [x]`.
- Do not skip phase verification or start a later phase while an earlier phase gate is incomplete.
- Do not make significant stack changes without approval.
- Never stage or commit unrelated or ambiguous changes. Never use `git add .` or `git add -A`.
- Cleanup, archive, delete, and unrelated commits are outside implementation authorization.

## Implementation Modes

Select a mode after loading track context and before marking the track active.

| Mode | Phase confirmation | Checkpoint commits | Final commit |
| --- | --- | --- | --- |
| Manual | Wait for user feedback | Require separate authorization | Authorized by implementation request unless user opts out |
| Auto | Agent performs or substitutes verification | Authorized by Auto Mode | Authorized by implementation request unless user opts out |

Auto Mode still stops for unrecoverable blockers, persistent verification failure, significant stack changes, destructive cleanup, or sensitive product-guideline changes.

## Standard Task Workflow

For one parent task at a time:

1. Select the first `[~]` task, otherwise the next `[ ]` task in plan order.
2. Persist `[ ] -> [~]` before implementation changes.
3. Write tests that define expected behavior and confirm the Red phase when feasible.
4. Implement the minimum Green-phase change.
5. Refactor without changing behavior and rerun tests.
6. Run relevant coverage and target more than 80% for new code.
7. Stop for approval before a significant tech-stack change; after approval, update `tech-stack.md` with a dated decision.
8. Create an ordinary task commit only when explicitly authorized for this workflow. Auto Mode does not authorize ordinary task commits.
9. Record the configured task summary. Without a commit, add `    - Summary: <summary>` beneath the task.
10. Persist `[~] -> [x]`; append the short commit SHA or `no-commit`.
11. Commit the plan update only when explicitly authorized. Auto Mode does not authorize ordinary plan commits.

## Phase Completion Verification and Checkpointing Protocol

Run immediately when the last non-meta task in a phase completes:

1. Announce verification start.
2. Identify phase-changed code and ensure corresponding tests exist in project style.
3. Announce and run automated tests or coverage. Attempt at most two fix cycles before requesting guidance.
4. Generate manual verification steps from `product.md`, `product-guidelines.md`, and the phase tasks.
5. Manual Mode: present the steps and wait for explicit confirmation.
6. Auto Mode: execute feasible steps directly; use the closest safe automated substitute and record any limitation.
7. Create `architect(checkpoint): complete phase <phase_name>` in Auto Mode, or in Manual Mode when checkpoint commits are explicitly authorized.
8. Record the checkpoint SHA only after the commit succeeds. The hash line belongs to a later authorized or final commit because the hash cannot exist inside its own checkpoint.

## Final Track Commit

After all tasks, verification, bookkeeping, and routine documentation synchronization succeed, create one final track-scoped commit unless the user explicitly opts out.

1. Compare the final worktree with the implementation baseline.
2. Stage only inspected files or hunks owned by the track and workflow.
3. Inspect the staged diff and run `git diff --cached --check`.
4. Commit `architect(implement): complete track <track_id>`.
5. Verify the commit and confirm no selected-track changes remain uncommitted.

Unsafe staging or commit failure is a finalization blocker. The implementation request authorizes this final commit in Manual and Auto modes, but never unrelated changes or cleanup commits. If the user opts out, report the remaining selected-track changes.

## Manual Verification Shape

Use concrete steps appropriate to the affected surface. Name the command or entry point, the action to perform, and the expected result. For example:

```markdown
1. Start the relevant application or service with `<command>`.
2. Exercise `<changed behavior>` through `<UI, API, or workflow>`.
3. Confirm `<observable result>` matches the acceptance criteria.
```
