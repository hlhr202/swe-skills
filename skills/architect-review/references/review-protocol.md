# Architect Review Protocol

## Purpose

Review an Architect track or explicit current changes with a principal-engineer standard. Prioritize correctness, security, data integrity, maintainability, plan compliance, project standards, and tests over incidental style preferences.

## Success Criteria

A review succeeds when it:

- Uses an explicit, uniquely identified, or user-confirmed scope.
- Records how the diff was derived and why its confidence is sufficient.
- Checks project context, track intent, style rules, correctness, safety, maintainability, and tests.
- Returns findings first, ordered by severity, with precise evidence and actionable guidance.
- Reports verification performed, limitations, and residual risk.
- Applies, records, commits, or cleans up only within the authorization granted by the user.

## Hard Boundaries

- Track-based review requires initialized Architect context. Explicit current-change or revision-range review may proceed without it only after warning that plan, product, and style checks may be limited.
- Keep Architect-managed reads and writes under `architect/`. Reject absolute paths, parent traversal (`..`), invalid track IDs, and links outside `architect/tracks/`.
- Review scope does not authorize fixes. `Apply Fixes` authorizes only changes directly supported by reported findings.
- Never broaden a review fix into unrelated refactoring or behavior changes without separate approval.
- Never create a Git commit unless the user has explicitly authorized that commit type in the current conversation.
- Never archive or delete a track without explicit confirmation of that exact cleanup action.
- Use reviewable edits, preferably patch-based; do not use shell redirection for file writes.
- Validate every operation. Retry once only for a clear recoverable issue; otherwise stop.

## State Model

```text
requested
  -> scope_adopted
  -> context_loaded
  -> diff_adopted
  -> analyzed
  -> reported
  -> decision
  -> fixes_applied?
  -> fixes_recorded?
  -> cleanup_or_stop
```

Scope confidence is either `high` or `user-confirmed`. Diff provenance is `explicit`, `recorded`, `inferred`, or `current`.

Review findings do not change track status by themselves. Review-fix plan entries use `[~]` while work is active and `[x]` when recorded complete.

## Decision Rules

### Scope preflight

Supported scopes are an exact track ID, track description, the sole in-progress track, `current`, or an explicit Git revision range.

- Exact valid track ID or exact normalized full-description matching one safe registry entry: high confidence; adopt it without confirmation and announce it.
- One plausible partial or fuzzy match: ask once. The answer is final.
- No unique match or conflicting evidence: ask for an exact ID or selection.
- Explicit `current`: adopt staged and unstaged changes without confirmation.
- Valid explicit revision range: adopt without redundant confirmation; ask once only if Git cannot resolve it.
- No supplied scope and exactly one `[~]` registry track: adopt it without confirmation.
- No supplied scope with zero or multiple active tracks: ask the user to choose current changes, a track, or a revision range.

Do not ask a second final-scope question after a scope is selected or confirmed. Always announce the adopted scope and evidence before loading changes.

### Registry and path validation

Parse registry sections separated by `---`, extracting marker, description, folder link, and track ID from entries such as:

```markdown
- [ ] **Track: <description>**
  *Link: [./tracks/<track_id>/](./tracks/<track_id>/)*
```

Accept `[ ]`, `[~]`, or `[x]`. IDs must match `^[0-9]{8}_[a-z0-9_]+$`. Resolve only `./tracks/<track_id>/` or equivalent `architect/tracks/<track_id>/` links. Duplicate, ambiguous, malformed, or unsafe entries cannot be reviewed as a track.

### Diff confidence

For a track review, first parse full or short commit SHAs recorded in `plan.md`. A recorded or inferred range is high confidence only when:

- Every boundary and recorded SHA resolves to a commit.
- The first relevant commit is an ancestor of the last relevant commit.
- The range is non-empty.
- Boundaries are anchored by a recorded SHA, a change under the track directory, or a subject/body mentioning the track ID.
- Commits form one coherent implementation sequence supported by messages, files, and plan tasks.
- There is no unexplained commit or conflicting evidence for another track.
- The aggregate diff footprint matches `spec.md` and `plan.md` without silently including unrelated work.

Routing:

- Recorded commits pass every check: use parent-of-first through last, announce evidence, proceed.
- Recorded commits fail or are absent: infer once from commits touching the track directory, mentioning the track ID, using related scopes such as `architect(implement)`, `architect(checkpoint)`, `architect(plan)`, or `architect(docs)`, or falling inside metadata timestamps; exclude other-track work.
- Exactly one inferred range passes every check: adopt and record provenance without confirmation.
- Exactly one plausible range has a named uncertainty: ask once whether to use it.
- Multiple or no plausible ranges: ask for an explicit range, current changes, or cancellation.
- Never silently substitute unrelated current changes for a track review.

### Current and untracked changes

Review staged and unstaged changes for `current`. Include untracked files only when confirmed or when they are clearly source, config, test, or documentation files within the requested review.

### Diff volume

Run a shortstat first. Review a diff under 300 changed lines in full. For larger diffs, announce iterative review mode and proceed automatically; chunking is a read-only strategy, not a scope change. List files, skip irrelevant generated or binary artifacts, review source/config/test/doc chunks, and aggregate findings.

### Tests

Infer and announce the most relevant non-interactive test command. Run it automatically when feasible and use CI-safe flags such as `CI=true` when appropriate. Ask before commands that appear destructive, long-running, integration-dependent, or likely to require external services. If no reliable command exists, say why tests were not run.

## Approval Boundaries

### Commit authorization

The following count as commit authorization:

- A direct request to commit, create a commit, or make the commit.
- `Yes` to a prompt that explicitly asks whether to commit.
- An explicit statement equivalent to `Commit all review workflow changes for this review`, limited to review-fix and review-plan commits.

The following do not count as commit authorization:

- Asking to review.
- Asking to apply fixes.
- Asking to complete the track.
- `Go ahead`, `proceed`, or similar unless the active prompt explicitly asked about committing.

Authorization is scoped to the named commit type. Review-fix authorization does not authorize plan, cleanup, archive, delete, or unrelated commits.

### Action matrix

| Action | Required approval |
| --- | --- |
| Adopt exact/high-confidence scope | None; announce evidence |
| Adopt one uncertain scope or range | One user confirmation |
| Apply clear localized findings | `Apply Fixes` |
| Apply broad or subjective Medium/Low change | Separate confirmation |
| Commit non-track review fixes | Explicit `Yes` to commit prompt |
| Record track fixes in plan | Explicit `Yes` to record prompt |
| Commit track review fixes or plan update | Existing or newly explicit commit authorization |
| Archive or permanently delete | Explicit confirmation of the exact action |

## Workflow

### 1. Preflight and setup

Determine whether the request is track-based or an explicit non-track review. Track review requires:

- `architect/tracks.md`
- `architect/product.md`
- `architect/tech-stack.md`
- `architect/workflow.md`
- `architect/product-guidelines.md`

`architect/index.md` and direct child Markdown files under `architect/code_styleguides/` are recommended context. For a missing track file, halt and report the incomplete track; setup cannot repair track artifacts.

### 2. Select and announce scope

Apply the scope rules above. When user input is needed, use concise choices:

- Title: `Select Scope`
- Prompt: `What would you like to review?`
- Choices: `Current changes`, `Choose a track`, `Provide revision range`

For `Choose a track`, ask with Title `Choose Track`, Prompt `Which track should I review?`, and choices listing available IDs and descriptions plus custom text. For `Provide revision range`, ask with Title `Revision Range`, Prompt `What revision range should I review?`, and examples such as `main...HEAD` and `HEAD~1..HEAD` plus custom text.

A chosen scope is already confirmed. Do not ask again.

### 3. Load context and determine diff

For track review, read project context plus the selected track's `spec.md`, `plan.md`, `metadata.json`, and `index.md` when present. Read only direct child style guides and do not follow external symlinks or references.

Treat explicit correctness, security, and maintainability style rules as High unless the guide says otherwise. Formatting-only violations are Low or Medium unless declared strict.

Derive the diff using the confidence rules. If no high-confidence range exists, ask:

- Title: `No Commits`
- Prompt: `I could not determine one high-confidence commit range for this track. How should I determine the review diff?`
- Choices: `Provide revision range`, `Review current changes`, `Cancel`

### 4. Analyze and verify

Check:

- Plan and specification compliance.
- Product and guideline fit.
- Tech-stack and style compliance.
- Correctness, edge cases, state transitions, races, nullability, error handling, and data loss.
- Secrets, unsafe input, injection, PII, authentication, authorization, and insecure defaults.
- Complexity, boundaries, duplication, and fragile abstractions.
- Test coverage for new or changed behavior.

Run feasible tests according to the decision rules.

### 5. Report findings first

Order findings Critical, High, Medium, Low. Use precise file and line evidence, explain impact, and provide a concrete suggestion or compact diff when useful.

```markdown
# Review Report: <Track Name / Scope>

## Findings

### <Critical|High|Medium|Low>: <issue title>
- **File**: `path/to/file` (Lines L<start>-L<end>)
- **Context**: <why this matters>
- **Suggestion**: <specific fix or compact diff>

## Verification Checks
- [ ] **Review Scope**: <scope> — <provenance>, <confidence>; <evidence>
- [ ] **Plan Compliance**: <Yes|No|Partial> — <comment>
- [ ] **Style Compliance**: <Pass|Fail|Not checked> — <comment>
- [ ] **New Tests**: <Yes|No|Not applicable>
- [ ] **Test Coverage**: <Yes|No|Partial|Not checked>
- [ ] **Test Results**: <Passed|Failed|Not run> — <summary>

## Summary
<one-sentence readiness assessment>
```

When no findings exist, write `No findings.` and identify residual risk or testing gaps.

### 6. Resolve findings

Recommendation:

- Critical/High: fix before proceeding.
- Medium/Low only: broadly acceptable, with improvements recommended.
- No findings: ready subject to stated limitations.

When findings exist, ask:

- Title: `Decision`
- Prompt: `How would you like to proceed with the review findings?`
- Choices: `Apply Fixes`, `Manual Fix`, `Complete Track`

`Apply Fixes` applies only supported findings and reruns relevant tests. `Manual Fix` stops. `Complete Track` accepts the findings without applying fixes. With no findings, continue directly.

### 7. Commit and record review changes

If no files changed, skip this stage.

For non-track fixes, ask with Title `Commit Changes`, Prompt `Review fixes changed files. Should I commit them?`, and Choices `Yes`, `No`. If authorized, use:

```text
architect(review): apply review fixes
```

For track fixes, ask:

- Title: `Commit & Track`
- Prompt: `Review fixes changed files. Should I record them in the track plan? I will only commit if commits are already authorized or you explicitly authorize committing now.`
- Choices: `Yes`, `No`

On `Yes`:

1. Append or reuse `## Phase: Review Fixes`.
2. Reuse an active `Apply review suggestions` task; after a completed task, create `Apply review suggestions 2` or ask for a label when several exist.
3. Mark the task `[~]`, preserve approved fixes, and save the plan.
4. If authorized, commit code with `architect(review): apply fixes for track <track_id>`.
5. Mark the task `[x]` with the short SHA or `no-commit`.
6. If authorized, commit the plan update with `architect(plan): record review fixes for track <track_id>`.
7. Report every changed but uncommitted file.

### 8. Cleanup

Skip cleanup without track context. Offer it only after review completes, the user did not choose Manual Fix, and the track is `[x]` or cleanup was explicitly requested.

Ask with Title `Track Cleanup`, Prompt `Review complete for track '<track_id>'. What would you like to do?`, and Choices `Archive`, `Delete`, `Skip`.

#### Archive

Before concise explicit confirmation:

1. Warn that the entire track directory, including expected and extra files, will move.
2. Report unexpected files and uncommitted changes.
3. Halt if `architect/archive/<track_id>/` already exists.
4. Ask with Title `Confirm Archive`, Prompt `Archive architect/tracks/<track_id>/ to architect/archive/<track_id>/ and remove it from architect/tracks.md?`, and Choices `Yes`, `No`.

On `Yes`, move the entire directory, verify destination exists and source does not, remove an empty residual source directory only after inspection, stop on non-empty residual contents, then remove the registry section. Commit `architect(cleanup): archive track <track_id>` only when separately authorized.

#### Delete

Report unexpected or uncommitted contents. Ask with Title `Confirm`, Prompt `WARNING: This permanently deletes architect/tracks/<track_id>/, including spec.md, plan.md, metadata.json, index.md, and any user notes or extra files. This cannot be undone. Type or choose Yes only if you are sure.`, and Choices `Yes`, `No`. Delete and remove the registry section only after explicit confirmation. Commit `architect(cleanup): delete track <track_id>` only when separately authorized.

#### Skip

Leave the track registered and unchanged.

## Stop Conditions

Stop and report the current evidence when:

- Required track context is missing or unsafe.
- Scope remains ambiguous after the allowed question.
- No reviewable diff exists.
- A requested test requires confirmation and approval is not given.
- The user chooses Manual Fix or Cancel.
- A fix would exceed reported findings or granted authorization.
- A commit cannot be safely isolated.
- Cleanup is unconfirmed, collides with an archive, or leaves unexpected source contents.
- An operation remains unsuccessful after one clear correction.
- Review and any authorized follow-up are complete.
