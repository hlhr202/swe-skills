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

### Standard Task Workflow

1. **Select Task:** Choose the next available task from `plan.md` in sequential order.
2. **Mark In Progress:** Before beginning work, edit `plan.md` and change the task from `[ ]` to `[~]`.
3. **Write Failing Tests (Red Phase):** Create tests that define the expected behavior and confirm they fail before implementation.
4. **Implement to Pass Tests (Green Phase):** Write the minimum application code required to pass the failing tests.
5. **Refactor:** Improve clarity, remove duplication, and rerun tests without changing behavior.
6. **Verify Coverage:** Run the project's coverage command and target >80% coverage for new code.
7. **Document Deviations:** If implementation requires a tech stack change, stop, update `tech-stack.md`, add a dated note, and resume.
8. **Commit Code Changes:** Stage task-related changes and commit with a clear message only when the user has explicitly authorized commits for the current implementation workflow.
9. **Attach Task Summary:** Record a task summary using the configured summary mechanism. If no commit is created, add an indented sub-item beneath the completed task in `plan.md` using `    - Summary: <summary>`.
10. **Record Task Completion:** Update `plan.md` from `[~]` to `[x]`. Append the short commit hash when a commit exists; otherwise append `no-commit`.
11. **Commit Plan Update:** Commit the `plan.md` update only when the user has explicitly authorized commits for the current implementation workflow.

### Phase Completion Verification and Checkpointing Protocol

This protocol runs immediately after a task completes a phase in `plan.md`.

1. **Announce Protocol Start:** Inform the user that the phase is complete and verification has begun.
2. **Ensure Test Coverage for Phase Changes:** Identify changed code files for the phase, verify corresponding tests exist, and create missing tests using the repository's existing testing style.
3. **Execute Automated Tests:** Announce the exact command, run it, and debug failures. Attempt at most two fix cycles before asking the user for guidance.
4. **Propose Manual Verification:** Generate step-by-step manual verification instructions based on `product.md`, `product-guidelines.md`, and `plan.md`.
5. **Await User Feedback:** Ask the user to confirm whether the manual verification meets expectations before proceeding.
6. **Create Checkpoint Commit:** Stage changes and create a phase checkpoint commit only when the user has explicitly authorized commits for the current implementation workflow. Use commit message format `architect(checkpoint): complete phase <phase_name>`.

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
