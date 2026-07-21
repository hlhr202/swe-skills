# Architect Status Protocol

## Purpose

Report the current Architect project state from core context, the track registry, plans, and metadata. Status supports both freshly initialized projects with no tracks and tracked projects with incomplete or inconsistent bookkeeping.

## Success Criteria

Produce a concise, evidence-based report that identifies:

- Overall project status and progress.
- Track totals and per-track progress.
- Current track, phase, and task.
- Next action.
- Active and possible blockers.
- Missing, malformed, duplicate, or inconsistent Architect artifacts.

## Hard Boundaries

- Status is strictly read-only. Never create, edit, move, delete, archive, or commit files.
- Keep Architect-managed reads under `architect/`. Reject absolute paths, parent traversal (`..`), invalid track IDs, and links outside `architect/tracks/`.
- Do not repair inconsistencies discovered during reporting.
- Validate reads and commands. Retry once only for a clear, recoverable path issue; otherwise stop and report the limitation.

## State Model

### Artifact state

| State | Evidence | Result |
| --- | --- | --- |
| `not_initialized` | Any required core file missing | Halt and recommend `/architect-setup` |
| `core_ready` | Core files exist; neither track artifact exists | Report setup-ready, no tracks |
| `partial_management` | Exactly one of `tracks.md` or `tracks/` exists | `Needs Attention`; parse only when possible |
| `tracked` | Both management artifacts exist | Parse registry, plans, and metadata |

Required core files are `product.md`, `product-guidelines.md`, `tech-stack.md`, `workflow.md`, and `index.md` under `architect/`.

### Project status precedence

Apply the first matching state:

1. `Needs Attention`: malformed or duplicate registry entries, invalid task-status declarations, missing plans, multiple `[~]` registry tracks, registry/plan active-track mismatches, missing index, invalid metadata, or metadata mismatches.
2. `Blocked`: an active blocker exists and no higher-priority condition applies.
3. `Complete`: every parsed track and counted task unit is complete.
4. `In Progress`: any track or counted unit is active, or completed and pending units coexist.
5. `Not Started`: no counted unit is active or complete.

## Decision Rules

### Registry parsing

Parse sections separated by `---` in this format:

```markdown
- [ ] **Track: <Track Description>**
  *Link: [./tracks/<track_id>/](./tracks/<track_id>/)*
```

Extract one marker (`[ ]`, `[~]`, `[x]`), description, folder link, and track ID. A valid ID matches `^[0-9]{8}_[a-z0-9_]+$`.

- Report duplicate IDs, missing fields, invalid IDs, and unsafe links in Notes.
- Resolve only `./tracks/<track_id>/` or equivalent `architect/tracks/<track_id>/` links.
- If no valid entries exist, report `No tracks found in architect/tracks.md.` and stop.

### Track reading

For each safe registered track, read `plan.md` and `metadata.json` when present. Missing or invalid track files affect that track and project status; they do not abort the remaining report.

Metadata alignment:

| Registry | Metadata |
| --- | --- |
| `[ ]` | `new` |
| `[~]` | `in_progress` |
| `[x]` | `completed` |

### Plan parsing and counting

- Read the `Task status granularity` declaration near the top of each plan; valid values are `task` and `sub-task`. A plan without this declaration defaults to `sub-task` for backward compatibility. Report any other value as malformed and parse it as `sub-task` best-effort.
- A phase is a Markdown heading beginning with `##`.
- A parent task is a non-indented checkbox task line such as `- [ ] Task: ...`, `- [~] Task: ...`, or `- [x] Task: ...`.
- An actionable sub-task is an indented checkbox line.
- With `task` granularity, count only parent tasks as progress units. Nested plain bullets are required implementation details but have no independent state.
- With `sub-task` granularity, if a parent has actionable sub-tasks, count only those sub-tasks as progress units. If it has none, count the parent as one unit.
- In either granularity, never count both a parent and its actionable sub-tasks in the percentage.
- Ignore summaries, notes, prose, and links. In `sub-task` granularity, also ignore plain nested bullets as contextual details.
- Report nested checkbox sub-tasks under an explicitly declared `task` plan as a granularity mismatch, but count only the parent tasks.
- Completion percentage is `completed / total * 100`; report `0%` and explain when total is zero.

Markers mean pending `[ ]`, in progress `[~]`, and complete `[x]`.

### Current work and next action

- Current track: the only registry `[~]` track; otherwise the first track whose plan contains `[~]` work.
- Current phase and task: the phase and first `[~]` counted unit; if none exists under `sub-task` granularity, use an active parent whose actionable sub-tasks are all complete.
- If multiple registry tracks are `[~]`, list all and mark `Needs Attention`.
- Resolve the current track before choosing its next action, then apply that track's declared granularity. If no track is active, scan incomplete tracks in registry order and apply each track's own granularity.
- Next action for `task` granularity: the first active parent task, otherwise the first pending parent task.
- Next action for `sub-task` granularity: the first `[~]` actionable sub-task; otherwise the first pending sub-task under the active parent; otherwise complete an active parent whose actionable sub-tasks are all `[x]`; otherwise resume the first active counted parent with no actionable sub-tasks; otherwise the first pending counted unit in registry order.
- If neither rule finds work, report `No pending tasks`.

### Blockers

- Active blockers are explicit markers such as `[BLOCKED] ...`, `Blocked: <reason>`, `Blocker: <reason>`, or an active task explicitly marked blocked.
- General prose containing `blocker`, `blocked`, or `blocking` is only a possible blocker and belongs in Notes.

## Approval Boundaries

Status has no approval-gated mutation because it has no mutation capability.

- Do not ask for permission to perform ordinary safe reads required by the report.
- Do not turn a status request into cleanup or repair.
- If the user later requests repairs, that is a separate workflow and authorization decision.

## Workflow

1. Verify core setup files.
2. Inspect presence of `architect/tracks.md` and `architect/tracks/`.
3. When neither exists, report setup-ready status and recommend `/architect-discuss`, followed by `/architect-propose` after scope confirmation.
4. When only `tracks/` exists, report `Needs Attention`, recommend inspecting the directory or using `/architect-propose` only when safe recovery is intended, and stop because no registry can be parsed.
5. When only `tracks.md` exists, report `Needs Attention` and parse it best-effort without resolving missing directories.
6. When both exist, parse and validate registry entries.
7. Read each safe track's plan and metadata.
8. Compute track, phase, task, blocker, and percentage results.
9. Apply project-status precedence.
10. Return the report without modifying files.

Use this output shape:

```markdown
# Architect Status

## Summary
- **Timestamp**: <current timestamp>
- **Project Status**: <Needs Attention|Blocked|Complete|In Progress|Not Started>
- **Progress**: <completed>/<total> tasks (<percentage>%)
- **Tracks**: <completed>/<total> completed, <in-progress> in progress, <pending> pending
- **Phases**: <total phases>
- **Task Status Granularity**: <task|sub-task|mixed>
- **Task Units**: <units>; <parent count> parent tasks, <sub-task count> actionable sub-tasks

## Current Work
- **Current Track**: <track, active list, or none>
- **Current Phase**: <phase or none>
- **Current Task**: <task or none>

## Next Action
- <next action>

## Blockers
- <active blockers or `None detected`>

## Track Details
- `<marker>` <track_id or unknown>: <description> — <completed>/<total> task units (<percentage>%); granularity: <task|sub-task>

## Notes
- <integrity issues, possible blockers, or limitations>
```

## Stop Conditions

Stop after reporting when:

- Core setup is incomplete.
- No track management artifacts exist.
- `tracks/` exists without a registry.
- The registry contains no valid tracks.
- A read remains unavailable after one clear correction.
- The report is complete.

Never convert a stop condition into a write or repair action.
