# SWE Skills

SWE Skills is a collection of agent-usable software engineering workflows. The first skill set in this repository is the Architect workflow, a structured planning and execution system for managing software projects through durable project context and track-based implementation.

## Installation

```sh
npx skills add https://github.com/hlhr202/swe-skills
```

## Architect Skills

Architect stores project context in `architect/` and organizes implementation work as tracks under `architect/tracks/`. The workflow is designed to be runtime-neutral so it can be used across different coding agents, not only one specific agent runtime.

| Skill | Capability | When to Use |
| --- | --- | --- |
| `architect-setup` | Initializes or resumes the core Architect project context, including product definition, product guidelines, tech stack, workflow, style guides, and project index. It does not create tracks. | Use when starting Architect in a project or recovering an interrupted setup before discussion or proposal work. |
| `architect-discuss` | Clarifies raw or ambiguous requirements and drafts product/architecture direction before tracked proposal work. | Use only when explicitly invoking `architect-discuss` for exploration, option comparison, or proposal readiness discussion. |
| `architect-propose` | Creates a new track with a confirmed specification, implementation plan, metadata, track index, and registry entry. | Use when planning a new feature, bug fix, chore, refactor, docs update, or test track. |
| `architect-implement` | Executes an existing track plan, updates task status, syncs track metadata, and keeps project context aligned with completed work. | Use when implementing, continuing, resuming, or completing a planned track. |
| `architect-review` | Reviews track work or explicit current changes against project context, track intent, style guides, correctness, safety, and tests. | Use when verifying implementation quality, applying review fixes, or checking cleanup readiness. |
| `architect-status` | Reports read-only project status from core context and, when available, the track registry and plans. | Use when checking setup status, project progress, or deciding what to work on next. |

## Acknowledgements

The Architect skills are intended as a workflow that can be shared across multiple coding agents. The design is strongly inspired by, and intentionally models many ideas from, Google's Conductor extension for Gemini CLI: https://github.com/gemini-cli-extensions/conductor.
