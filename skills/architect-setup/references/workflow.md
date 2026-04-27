# Project Workflow

## Guiding Principles

1. **The Plan is the Source of Truth:** All work must be tracked in `plan.md`.
2. **The Tech Stack is Deliberate:** Changes to the tech stack must be documented in `tech-stack.md` before implementation.
3. **Test-Driven Development:** Write unit tests before implementing functionality.
4. **High Code Coverage:** Aim for >80% code coverage for all modules.
5. **User Experience First:** Every decision should prioritize user experience.
6. **Non-Interactive and CI-Aware:** Prefer non-interactive commands. Use `CI=true` for watch-mode tools so tests and linters run once.

## Task Workflow

All tasks follow a strict lifecycle.

### Implementation Modes

`/architect-implement` asks for an implementation mode after loading track context and before marking the track in progress.

- **Manual Mode:** Preserve all human confirmation steps. Phase completion waits for user feedback before proceeding, and commits are created only when the user has explicitly authorized commits for the current implementation workflow.
- **Auto Mode:** Run the full `plan.md` without phase-level human confirmation. The agent must perform phase verification itself using tests, coverage, browser automation, command-line checks, API checks, or code inspection where appropriate. Auto Mode authorizes phase checkpoint commits for the current implementation workflow, but does not authorize final track completion, documentation sync, cleanup, archive, delete, or unrelated commits.

Auto Mode still stops for unrecoverable blockers, failed verification after the allowed fix attempts, significant technology stack changes, destructive cleanup, or sensitive product guideline changes.

### Standard Task Workflow

1. **Select Task:** Choose the next available task from `plan.md` in sequential order.
2. **Mark In Progress:** Before beginning work, edit `plan.md` and change the task from `[ ]` to `[~]`.
3. **Write Failing Tests (Red Phase):** Create tests that define the expected behavior and confirm they fail before implementation.
4. **Implement to Pass Tests (Green Phase):** Write the minimum application code required to pass the failing tests.
5. **Refactor:** Improve clarity, remove duplication, and rerun tests without changing behavior.
6. **Verify Coverage:** Run the project's coverage command and target >80% coverage for new code.
7. **Document Deviations:** If implementation requires a significant tech stack change, stop and get user approval before updating `tech-stack.md`. After approval, add a dated note and resume.
8. **Commit Code Changes:** Stage task-related changes and commit with a clear message only when the user has explicitly authorized commits for the current implementation workflow. Auto Mode only authorizes phase checkpoint commits, not ordinary task commits.
9. **Attach Task Summary:** Record a task summary using the configured summary mechanism. If no commit is created, add an indented sub-item beneath the completed task in `plan.md` using `    - Summary: <summary>`.
10. **Record Task Completion:** Update `plan.md` from `[~]` to `[x]`. Append the short commit hash when a commit exists; otherwise append `no-commit`.
11. **Commit Plan Update:** Commit the `plan.md` update only when the user has explicitly authorized commits for the current implementation workflow. Auto Mode only authorizes phase checkpoint commits, not ordinary plan update commits.

### Phase Completion Verification and Checkpointing Protocol

This protocol runs immediately after a task completes a phase in `plan.md`.

1. **Announce Protocol Start:** Inform the user that the phase is complete and verification has begun.
2. **Ensure Test Coverage for Phase Changes:** Identify changed code files for the phase, verify corresponding tests exist, and create missing tests using the repository's existing testing style.
3. **Execute Automated Tests:** Announce the exact command, run it, and debug failures. Attempt at most two fix cycles before asking the user for guidance.
4. **Generate Manual Verification:** Generate step-by-step manual verification instructions based on `product.md`, `product-guidelines.md`, and `plan.md`.
5. **Manual Mode Feedback:** In Manual Mode, ask the user to confirm whether the manual verification meets expectations before proceeding.
6. **Auto Mode Verification:** In Auto Mode, do not wait for phase-level human feedback. Execute the generated verification steps directly when feasible. If a step cannot be executed directly, perform the closest safe automated substitute and record the limitation in the task summary.
7. **Create Checkpoint Commit:** In Auto Mode, stage phase-related changes and create a phase checkpoint commit. In Manual Mode, create the checkpoint commit only when the user has explicitly authorized commits for the current implementation workflow. Use commit message format `architect(checkpoint): complete phase <phase_name>`.
8. **Record Checkpoint Hash:** When a checkpoint commit is created, record its hash in `plan.md` only after the commit succeeds. The `plan.md` line that records the checkpoint hash cannot be included in the same checkpoint commit because the hash does not exist until after that commit is created; it remains a follow-up Architect status update for the next authorized commit or final track update.

## Manual Verification Examples

For a frontend change:

```markdown
The automated tests have passed. For manual verification, please follow these steps:

1. Start the development server with `npm run dev`.
2. Open your browser to `http://localhost:3000`.
3. Confirm that the new user-facing behavior appears as expected.
```

For a backend change:

```markdown
The automated tests have passed. For manual verification, please follow these steps:

1. Ensure the server is running.
2. Execute the documented API request.
3. Confirm that the response status and body match the acceptance criteria.
```
