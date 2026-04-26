# Architect Status Protocol

This protocol provides a read-only status overview of an Architect project by parsing `architect/tracks.md` and each registered track's `plan.md`.

## 1. System Directive

You are reporting Architect project status. Read project files, parse progress, and present a concise status report. Do not modify files, move files, delete files, archive tracks, or commit changes.

Validate every operation result. If a read or command fails because of a recoverable path issue, self-correct once. If it remains unrecoverable, stop, report the failure, and wait for the user.

Use relative project paths such as `architect/tracks.md` and `architect/tracks/<track_id>/plan.md`. Architect-managed reads must stay under `architect/`; never follow absolute paths, parent-directory paths (`..`), or track links outside `architect/tracks/`.

## 2. Setup Check

Verify that Architect is initialized before reporting project status.

Required setup files. If any of these are missing, status cannot run:

- `architect/tracks.md`
- `architect/product.md`
- `architect/tech-stack.md`
- `architect/workflow.md`

Expected setup context. Missing expected context should be reported in Notes and may contribute to `Needs Attention`, but it should not halt status reporting:

- `architect/index.md`

Optional enrichment context. Missing enrichment context should not affect project status unless another Architect file references it as required:

- `architect/product-guidelines.md`

If any required setup file is missing, halt and tell the user:

```text
Architect is not set up. Please run `/architect-setup` to set up the environment.
```

## 3. Read Tracks Registry

Read `architect/tracks.md` and parse entries separated by `---`.

For each track section, support the Architect registry format:

```markdown
- [ ] **Track: <Track Description>**
  *Link: [./tracks/<track_id>/](./tracks/<track_id>/)*
```

For each track, extract:

- Status marker: `[ ]`, `[~]`, or `[x]`.
- Track description.
- Track folder link when present.
- Track ID from the folder link when present.

Track IDs parsed from the registry must match `^[0-9]{8}_[a-z0-9_]+$`. Treat entries with invalid IDs as malformed and do not resolve their directories.

Validate registry structure:

- A valid track should have one status marker, one track description, one folder link, and one track ID.
- Duplicate track IDs are status issues.
- Track sections missing a folder link or track ID, or using an invalid track ID, are malformed and should be reported in Notes.

If no valid track entries are found, report:

```text
No tracks found in architect/tracks.md.
```

Then stop.

## 4. Read Track Plans

For each registered track with a folder link:

1. Resolve the track directory only when the parsed `track_id` matches `^[0-9]{8}_[a-z0-9_]+$` and the registry link is `./tracks/<track_id>/` or the equivalent `architect/tracks/<track_id>/`. If the link is absolute, contains `..`, has an invalid track ID, or points outside `architect/tracks/`, report the track as malformed and do not read it.
2. Read `plan.md` when present.
3. Read `metadata.json` when present.
4. If `plan.md` is missing, include the track in the report with `plan missing` status instead of failing the entire status report.
5. If `metadata.json` is missing, invalid, or inconsistent with the registry marker, include that in Notes.

Do not require every track to be complete or well-formed. Status should be best-effort and should call out missing or malformed track files.

Metadata consistency rules:

- Registry `[ ]` should match metadata status `new`.
- Registry `[~]` should match metadata status `in_progress`.
- Registry `[x]` should match metadata status `completed`.
- Missing, invalid, or mismatched metadata is a status issue and should be reported in Notes.

## 5. Parse Track Plans

For each `plan.md`, parse:

- Phases: markdown headings beginning with `##`.
- Parent tasks: non-indented checkbox task lines such as `- [ ] Task: ...`, `- [~] Task: ...`, and `- [x] Task: ...`.
- Actionable sub-tasks: indented checkbox lines using `[ ]`, `[~]`, or `[x]`.
- Active blockers: lines that clearly indicate blocked work, such as `[BLOCKED] ...`, `Blocked: <reason>`, `Blocker: <reason>`, or an unchecked/current task explicitly marked blocked.
- Possible blockers: weak matches such as general prose containing `blocker`, `blocked`, or `blocking` that do not clearly identify active blocked work.
- Summaries: non-actionable summary lines should not count as tasks.

Status marker meanings:

- `[ ]`: pending.
- `[~]`: in progress.
- `[x]`: completed.

Ignore plain bullets, notes, summaries, explanatory text, and links when counting tasks.

## 6. Compute Status

Compute per-track and overall totals:

- Track count by registry status: pending, in progress, completed.
- Phase count.
- Parent task count.
- Actionable sub-task count.
- Completed tasks.
- In-progress tasks.
- Pending tasks.
- Completion percentage: `completed / total * 100` using counted task units. If `total` is `0`, report `0%` and note that no counted task units were found.

Count task progress with these rules:

- If a parent task has actionable sub-tasks, count only those sub-tasks as progress units.
- If a parent task has no actionable sub-tasks, count the parent task as one progress unit.
- Do not count both a parent task and its actionable sub-tasks in the completion percentage.
- Parent task count and actionable sub-task count may still be reported as separate supporting metrics.

Determine current work:

- Current track: the only `[~]` registry track when exactly one exists, otherwise the first track whose plan has `[~]` tasks.
- Current phase: phase containing the first `[~]` parent task or actionable sub-task.
- Current task: first `[~]` parent task or actionable sub-task.

If multiple registry tracks are `[~]`, list all active tracks in Current Work and report the condition in Notes. Do not silently ignore additional active tracks.

If multiple track plans contain `[~]` parent tasks or actionable sub-tasks while the registry does not show the same active tracks as `[~]`, report the registry/plan mismatch in Notes and treat it as `Needs Attention`.

Determine next action:

- First `[~]` actionable sub-task in registry order, if any.
- Otherwise, first `[ ]` actionable sub-task under the current `[~]` parent task, if any.
- Otherwise, first `[ ]` counted task unit in registry order.
- If no pending work exists, report `No pending tasks`.

Determine project status with this precedence:

1. `Needs Attention`: missing plans, malformed registry entries, duplicate track IDs, multiple `[~]` registry tracks, registry/plan active-track mismatches, missing `architect/index.md`, invalid metadata, or metadata mismatches are detected.
2. `Blocked`: active blockers exist and no `Needs Attention` condition is present.
3. `Complete`: all parsed tracks are `[x]`, all counted task units are `[x]`, and no higher-priority condition is present.
4. `In Progress`: any track, parent task, or counted task unit is `[~]`, or completed counted task units coexist with pending counted task units, and no higher-priority condition is present.
5. `Not Started`: no completed or in-progress counted task units exist and no higher-priority condition is present.

Report possible blockers in Notes unless they also meet the active blocker rules.

## 7. Present Status Overview

Report status in this format:

```markdown
# Architect Status

## Summary
- **Timestamp**: <current timestamp>
- **Project Status**: <Blocked|In Progress|Complete|Not Started|Needs Attention>
- **Progress**: <completed>/<total> tasks (<percentage>%)
- **Tracks**: <completed>/<total> completed, <in-progress> in progress, <pending> pending
- **Phases**: <total phases>
- **Task Units**: <counted task units>; <parent task count> parent tasks, <actionable sub-task count> actionable sub-tasks

## Current Work
- **Current Track**: <track description, active track list, or none>
- **Current Phase**: <phase or none>
- **Current Task**: <task or none>

## Next Action
- <next pending task or no pending tasks>

## Blockers
- <blocker lines or `None detected`>

## Track Details
- `<marker>` <track_id or unknown>: <description> — <completed>/<total> task units (<percentage>%)

## Notes
- <missing plans, malformed entries, duplicate track IDs, multiple active tracks, registry/plan mismatches, inconsistent metadata, possible blockers, or status limitations>
```

Keep the report concise. Include details only when they help the user decide the next action.
