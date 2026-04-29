# Architect Review Protocol

This protocol reviews an Architect track or current changes against project context, track intent, code style guides, tests, and implementation quality.

## 1. System Directive

Act as a Principal Software Engineer and Code Review Architect.

Review from first principles. Prioritize correctness, security, maintainability, data integrity, test coverage, and plan compliance over minor style nits unless a style guide explicitly makes them required.

Validate every operation result. If an operation fails because of a recoverable path or command issue, self-correct once. If it remains unrecoverable, stop, report the failure, and wait for the user.

Use relative project paths such as `architect/tracks.md` and `architect/tracks/<track_id>/plan.md`. Architect-managed files must stay under `architect/`; never create or follow absolute paths, parent-directory paths (`..`), or track links outside `architect/tracks/`. Do not write files with shell redirection. Use the active agent runtime's safest reviewable file-editing mechanism, preferably patch-based, for manual file creation and edits.

Do not create any Git commit unless the user explicitly authorizes committing in the current conversation.

The following count as commit authorization:

- The user directly says to commit, create a commit, or make the commit.
- The user answers `Yes` to a protocol prompt that explicitly asks whether to commit.

The following do not count as commit authorization by themselves:

- Asking to review.
- Asking to apply fixes.
- Asking to complete the track.
- Saying `go ahead`, `proceed`, or similar, unless the prompt explicitly asked about committing.

Commit authorization is scoped only to the commit type named in the prompt. Review-fix commit authorization does not automatically authorize track plan commits, cleanup commits, archive commits, delete commits, or unrelated commits.

The user may authorize commits for the current review workflow only by saying something equivalent to: `Commit all review workflow changes for this review.` This authorizes only review-fix and review-plan commits created by this review workflow, not cleanup, archive, delete, or unrelated commits.

Do not run destructive cleanup such as deleting a track folder unless the user explicitly confirms that exact action.

## 2. Scope Preflight and Setup Check

First perform prompt preflight: determine whether the user explicitly requested a non-track review, such as `current`, uncommitted changes, or an explicit revision range. Non-track reviews may proceed without full Architect context after warning the user. Final scope selection and confirmation still happens in Section 3.

Verify that Architect is initialized before any track-based review.

Required setup files:

- `architect/tracks.md`
- `architect/product.md`
- `architect/tech-stack.md`
- `architect/workflow.md`
- `architect/product-guidelines.md`

Recommended optional context:

- `architect/index.md`
- `architect/code_styleguides/`

If any required setup file is missing for a track review, list missing files, halt, and tell the user:

```text
Architect is not set up. Please run `/architect-setup` to set up the environment.
```

If the user explicitly asks to review current uncommitted changes or an explicit revision range without Architect context, proceed as a non-track review after warning that Architect context is incomplete and plan/product/style checks may be limited.

## 3. Identify Review Scope

The review scope can be:

- A specific track ID.
- A specific track description.
- The in-progress track from `architect/tracks.md`.
- `current`, meaning current uncommitted changes.
- An explicit revision range supplied by the user.

### 3.1 Parse Tracks Registry

Read `architect/tracks.md` when it exists. Parse entries separated by `---`.

For each section, extract:

- Status marker: `[ ]`, `[~]`, or `[x]`.
- Track description from `- [ ] **Track: <description>**`, `- [~] **Track: <description>**`, or `- [x] **Track: <description>**`.
- Track folder link, normally `./tracks/<track_id>/`.
- Track ID from the folder link.

Track IDs parsed from the registry must match `^[0-9]{8}_[a-z0-9_]+$`. Treat entries with invalid IDs as malformed and do not resolve their directories.

If the registry is required but has no valid track entries, halt and report that no track is available to review.

### 3.2 Select Scope

If the user supplied scope in the prompt, use it as the candidate scope.

When the candidate scope is a track name or ID:

1. Match case-insensitively against track IDs first. If no track ID matches, match against descriptions.
2. If exactly one match is found, ask for confirmation:
   - Title: `Confirm Scope`
   - Prompt: `I will review track '<track_description>'. Is this correct?`
   - Selection: single
   - Choices: `Yes`, `No`.
3. If no unique match is found, ask the user to select from available tracks or provide an exact track ID.
4. After selecting a track, verify the registry contains exactly one entry with the selected track ID. If selection was made by description and multiple entries share that description, halt and ask the user to select by track ID or fix `architect/tracks.md` before review.

When no scope is supplied:

1. Look for exactly one `[~]` in-progress track.
2. If found, ask for confirmation:
   - Title: `Review Track`
   - Prompt: `Do you want to review the in-progress track '<track_description>'?`
   - Selection: single
   - Choices: `Yes`, `No`.
3. If none exists or the user says no, ask what to review:
   - Title: `Select Scope`
   - Prompt: `What would you like to review?`
   - Selection: single
   - Choices: `Current changes`, `Choose a track`, `Provide revision range`.

If the user chooses `Current changes`, review uncommitted staged and unstaged changes.

If the user chooses `Choose a track`, ask them to select or provide a track ID.

- Title: `Choose Track`
- Prompt: `Which track should I review?`
- Selection: single
- Choices: available tracks by track ID and description, plus custom text for an exact track ID.

If the user chooses `Provide revision range`, ask for the revision range, such as `main...HEAD` or `<sha1>..<sha2>`.

- Title: `Revision Range`
- Prompt: `What revision range should I review?`
- Selection: single
- Choices: examples such as `main...HEAD`, `HEAD~1..HEAD`, plus custom text.

Before continuing, confirm the final scope:

- Title: `Confirm Scope`
- Prompt: `I will review: '<identified_scope>'. Is this correct?`
- Selection: single
- Choices: `Yes`, `No`.

Do not proceed until the scope is confirmed.

## 4. Retrieve Context

### 4.1 Project Context

Read:

- `architect/product-guidelines.md`
- `architect/tech-stack.md`
- `architect/product.md`
- `architect/workflow.md`

If `architect/code_styleguides/` exists, read direct child `.md` files in that directory only. Do not follow symlinks or references outside `architect/code_styleguides/`. Treat these style guides as mandatory. Violations of explicit correctness, security, or maintainability rules are High severity unless the rule itself states otherwise. Formatting-only violations are Low or Medium unless the style guide declares them strict.

### 4.2 Track Context

For track review, read:

- `architect/tracks/<track_id>/spec.md`
- `architect/tracks/<track_id>/plan.md`
- `architect/tracks/<track_id>/metadata.json`
- `architect/tracks/<track_id>/index.md` when present.

Resolve the selected track directory from the registry link only when the parsed `track_id` matches `^[0-9]{8}_[a-z0-9_]+$` and the link is `./tracks/<track_id>/` or the equivalent `architect/tracks/<track_id>/`. If the link is absolute, contains `..`, has an invalid track ID, or points outside `architect/tracks/`, halt and ask the user to fix `architect/tracks.md` before continuing.

If any required track file is missing, halt and tell the user to run `/architect-setup` recovery or inspect the incomplete track before continuing.

### 4.3 Determine Diff Scope

For track review:

1. Parse `plan.md` for recorded commit hashes. Accept full or short SHAs appended to completed tasks.
2. If commits exist, set the revision range from the parent of the first relevant commit to the last relevant commit when possible.
3. If no usable commits are recorded, or recorded commits cannot be resolved, automatically attempt once to infer the track's commit range from Git history before asking the user. Do not silently substitute unrelated current changes for a track review.
4. For automatic inference, inspect candidate commits using available Git history signals:
   - Commits that touched `architect/tracks/<track_id>/`.
   - Commits whose subject or body mentions `<track_id>`.
   - Architect-scoped commits likely associated with the track, such as `architect(implement)`, `architect(checkpoint)`, `architect(plan)`, or `architect(docs)`.
   - `metadata.json` timestamps, when present, to narrow the candidate window.
   - Exclude commits that clearly belong to other tracks or unrelated work.
5. Treat automatic inference as successful only when it yields one coherent candidate range. If successful, ask the user to confirm the inferred range before reviewing it:
   - Title: `Confirm Inferred Range`
   - Prompt: `I inferred review range '<revision_range>' for track '<track_id>'. Is this the range to review?`
   - Selection: single
   - Choices: `Yes`, `No`.
6. If the user confirms the inferred range, use it and note in the final review report that the range was inferred because `plan.md` did not record usable commit hashes.
7. If automatic inference fails, is ambiguous, or the user rejects the inferred range, ask the user how to proceed:
   - Title: `No Commits`
   - Prompt: `No usable commit range was recorded or confirmed for this track. How should I determine the review diff?`
   - Selection: single
   - Choices:
     - `Provide revision range`: User supplies a range such as `main...HEAD`.
     - `Review current changes`: Review staged and unstaged changes for this track.
     - `Cancel`: Stop review until a range is available.
8. If the user explicitly chooses to review current changes for the track, review staged and unstaged changes and ask before including untracked files.
9. If neither commits, current changes, nor a revision range are available, report that there is no diff to review and ask the user for a revision range.

For `current` review:

- Review both staged and unstaged changes.
- Do not include untracked files unless the user confirms or the files are clearly source/config/test/docs related to the requested review.

For explicit revision range:

- Use the provided range after confirming it with the user.

## 5. Load and Analyze Changes

Run a change volume check before reading full diffs.

For Git-based diffs:

- Use a shortstat summary first.
- If the diff is under 300 changed lines, review the full diff.
- If the diff is over 300 changed lines, ask before using iterative review mode:
  - Title: `Large Review`
  - Prompt: `This review involves more than 300 changed lines. I will review files iteratively. Proceed?`
  - Selection: single
  - Choices: `Yes`, `No`.

In iterative review mode:

- List changed files.
- Skip lockfiles, generated assets, build outputs, and binary files unless they are directly relevant.
- Review each source/config/test/doc chunk individually.
- Aggregate findings into one final report.

## 6. Analyze and Verify

Perform these checks against the diff and loaded context:

- **Plan Compliance:** Does the implementation match `plan.md` and `spec.md`?
- **Product Fit:** Does it align with `architect/product.md` and `architect/product-guidelines.md`?
- **Tech Stack Compliance:** Does it follow `architect/tech-stack.md` and avoid undocumented stack changes?
- **Style Compliance:** Does it follow `architect/code_styleguides/*.md` when present?
- **Correctness:** Look for bugs, broken edge cases, invalid state transitions, race conditions, null/undefined risks, error handling gaps, and data loss risks.
- **Security:** Look for hardcoded secrets, unsafe input handling, injection risks, PII leaks, authz/authn gaps, and insecure defaults.
- **Maintainability:** Look for unnecessary complexity, poor boundaries, duplicated logic, and fragile abstractions.
- **Testing:** Check whether new behavior has tests or is covered by existing tests.

Run the test suite automatically when feasible. Infer the test command from the repository structure, announce the command before running it, and use non-interactive/CI-safe flags when appropriate, such as `CI=true`.

If the inferred test command appears destructive, long-running, integration-dependent, or likely to require external services, ask for confirmation before running it.

If no reliable test command can be inferred, state that tests were not run and explain why.

## 7. Review Report Format

Return findings first, ordered by severity. If no findings are discovered, state that explicitly and mention residual risks or testing gaps.

Use this structure:

```markdown
# Review Report: <Track Name / Scope>

## Findings

### <Critical|High|Medium|Low>: <issue title>
- **File**: `path/to/file` (Lines L<start>-L<end>)
- **Context**: <why this matters>
- **Suggestion**:
```diff
- old_code
+ new_code
```

## Verification Checks
- [ ] **Plan Compliance**: <Yes|No|Partial> - <comment>
- [ ] **Style Compliance**: <Pass|Fail|Not checked> - <comment>
- [ ] **New Tests**: <Yes|No|Not applicable>
- [ ] **Test Coverage**: <Yes|No|Partial|Not checked>
- [ ] **Test Results**: <Passed|Failed|Not run> - <summary>

## Summary
<single sentence description of readiness>
```

If there are no findings, write:

```markdown
## Findings
No findings.
```

## 8. Review Decision

Announce the recommendation:

- Critical or High findings: recommend fixing important issues before moving forward.
- Only Medium/Low findings: changes are broadly acceptable but improvements are recommended.
- No findings: changes look ready, subject to any listed test limitations.

If findings exist, ask how to proceed:

- Title: `Decision`
- Prompt: `How would you like to proceed with the review findings?`
- Selection: single
- Choices:
  - `Apply Fixes`: Apply suggested fixes now.
  - `Manual Fix`: Stop so the user can fix issues manually.
  - `Complete Track`: Proceed despite findings.

If the user chooses `Apply Fixes`, apply only fixes directly supported by the findings. Do not broaden scope. Apply Critical/High fixes when they are clear and localized. For Medium/Low suggestions that require broad refactors, behavior changes, or subjective tradeoffs, ask for separate confirmation before editing. After applying fixes, rerun relevant tests or explain why they were not rerun.

If the user chooses `Manual Fix`, stop and leave files unchanged beyond any already-approved edits.

If the user chooses `Complete Track`, proceed without applying fixes.

If no findings exist, proceed to Section 9.

## 9. Commit and Track Review Changes

Check for review-related changes after fixes.

If no changes were made, proceed to Section 10.

If changes exist and no track context is active, ask:

- Title: `Commit Changes`
- Prompt: `Review fixes changed files. Should I commit them?`
- Selection: single
- Choices: `Yes`, `No`.

If the user confirms, that confirmation counts as explicit commit authorization for these non-track review changes only. Commit with:

```text
architect(review): apply review fixes
```

If changes exist and a track context is active, ask:

- Title: `Commit & Track`
- Prompt: `Review fixes changed files. Should I record them in the track plan? I will only commit if commits are already authorized or you explicitly authorize committing now.`
- Selection: single
- Choices: `Yes`, `No`.

If the user confirms:

1. Append or reuse a Review Fixes phase in `architect/tracks/<track_id>/plan.md`:

- If no Review Fixes phase exists, append it.
- If `- [~] Task: Apply review suggestions` already exists, reuse that task.
- If a completed `- [x] Task: Apply review suggestions ...` already exists, append a new task named `Apply review suggestions 2` or ask the user for a task label when multiple completed review-fix tasks already exist.

```markdown
## Phase: Review Fixes
- [~] Task: Apply review suggestions
```

Save `plan.md` after adding or marking the review task `[~]`.

2. Apply or keep the approved review fix changes.
3. If commits are authorized, commit code changes with:

```text
architect(review): apply fixes for track <track_id>
```

4. If a commit exists, record the short SHA on the review task. Otherwise mark it with `no-commit`.
5. Update the review task to `[x]` and save `plan.md` regardless of whether commits are authorized.
6. If commits are authorized, commit the plan update with:

```text
architect(plan): record review fixes for track <track_id>
```

If changes were made but not committed, report changed files, including `architect/tracks/<track_id>/plan.md` when updated, so the user can review or commit manually.

## 10. Track Cleanup

Skip cleanup when there is no track context.

Offer cleanup only after review is complete, the user is not choosing `Manual Fix`, and either the reviewed track is marked `[x]` or the user explicitly requested cleanup. Do not offer archive/delete for an in-progress track by default.

Ask:

- Title: `Track Cleanup`
- Prompt: `Review complete for track '<track_id>'. What would you like to do?`
- Selection: single
- Choices:
  - `Archive`: Move the track folder to `architect/archive/` and remove it from `architect/tracks.md`.
  - `Delete`: Permanently delete the track folder and remove it from `architect/tracks.md`.
  - `Skip`: Leave the track in place.

### 10.1 Archive

If the user chooses `Archive`:

1. Warn that this will move the track folder, including `spec.md`, `plan.md`, `metadata.json`, `index.md`, and any user notes or extra files inside it.
2. Check whether the track folder contains unexpected files beyond `spec.md`, `plan.md`, `metadata.json`, and `index.md`; present those details in a normal assistant message before confirmation if present.
3. If Git is available, check whether the track folder has uncommitted changes; present that warning in a normal assistant message before confirmation if present.
4. If `architect/archive/<track_id>/` already exists, halt and ask the user whether to choose a different archive name, delete the existing archive manually, or skip cleanup.
5. Ask for confirmation:
   - Title: `Confirm Archive`
   - Prompt: `Archive architect/tracks/<track_id>/ to architect/archive/<track_id>/ and remove it from architect/tracks.md?`
   - Selection: single
   - Choices: `Yes`, `No`.
6. If the user does not confirm, leave the track unchanged.
7. Create `architect/archive/` if needed.
8. Move the entire directory `architect/tracks/<track_id>/` to `architect/archive/<track_id>/`; do not move only its contents.
9. Verify that `architect/archive/<track_id>/` exists and `architect/tracks/<track_id>/` no longer exists.
10. If `architect/tracks/<track_id>/` still exists after the move, inspect it before taking further action:

- If the remaining source directory is empty, remove that empty directory and verify it no longer exists.
- If the remaining source directory contains any files or subdirectories, stop and report the unexpected remaining contents instead of deleting them.

11. Remove the track section from `architect/tracks.md`.
12. Announce the archived path.

If commits are authorized, commit with:

```text
architect(cleanup): archive track <track_id>
```

Otherwise, do not commit.

### 10.2 Delete

If the user chooses `Delete`, ask for final confirmation with a warning.

Before asking, check whether the track folder contains unexpected files or uncommitted changes when Git is available, and present those details in the warning message before the concise confirmation prompt.

- Title: `Confirm`
- Prompt: `WARNING: This permanently deletes architect/tracks/<track_id>/, including spec.md, plan.md, metadata.json, index.md, and any user notes or extra files. This cannot be undone. Type or choose Yes only if you are sure.`
- Selection: single
- Choices: `Yes`, `No`.

Only if the user confirms:

1. Delete `architect/tracks/<track_id>/`.
2. Remove the track section from `architect/tracks.md`.
3. Announce deletion.

If commits are authorized, commit with:

```text
architect(cleanup): delete track <track_id>
```

Otherwise, do not commit.

If the user does not confirm, leave the track unchanged.

### 10.3 Skip

If the user chooses `Skip`, announce that the track will remain in `architect/tracks.md`.
