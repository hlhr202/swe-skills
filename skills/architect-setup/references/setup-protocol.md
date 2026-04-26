# Architect Setup Protocol

This protocol defines the Architect setup workflow for agent runtimes.

## 1. System Directive

You are setting up and managing a software project using the Architect methodology. Follow the steps sequentially unless the audit phase identifies a valid resume point.

Validate every operation result. If an operation fails because of a recoverable path or command issue, self-correct once. If it remains unrecoverable, stop, report the failure, and wait for the user.

Use relative project paths such as `architect/product.md` for generated project files. Architect-managed files must stay under `architect/`; never create or follow absolute paths, parent-directory paths (`..`), or track links outside `architect/tracks/`. Do not write files with shell redirection. Use the active agent runtime's safest reviewable file-editing mechanism, preferably patch-based, for file creation and edits.

Do not commit changes unless the user explicitly requests a commit in the current conversation.

## 2. Pre-Initialization Overview

Present this overview to the user before setup begins:

> Welcome to Architect. I will guide you through the following steps to set up your project:
> 1. **Project Discovery:** Analyze the current directory to determine if this is a new or existing project.
> 2. **Product Definition:** Collaboratively define the product's vision, design guidelines, and technology stack.
> 3. **Configuration:** Select appropriate code style guides and customize your development workflow.
> 4. **Track Generation:** Define the initial **track** (a high-level unit of work like a feature or bug fix) and automatically generate a detailed plan to start development.
>
> Let's get started.

## 3. Project Audit

Before setup, inspect existing artifacts under `architect/`:

- `product.md`
- `product-guidelines.md`
- `tech-stack.md`
- `code_styleguides/`
- `workflow.md`
- `index.md`
- `tracks/*/spec.md`
- `tracks/*/plan.md`
- `tracks/*/metadata.json`
- `tracks/*/index.md`

Determine the resume target by checking setup prerequisites in order. Do not jump to a later section just because a later artifact exists; if files were manually created out of order or setup was interrupted, resume at the earliest missing prerequisite.

| Earliest Missing or Incomplete State | Target | Announcement |
| --- | --- | --- |
| No Architect artifacts exist | Section 4 | No resume announcement |
| `architect/product.md` is missing or incomplete | Section 5 | "Resuming setup: Product guide is missing or incomplete. Next: create product guide." |
| `architect/product-guidelines.md` is missing or incomplete | Section 6 | "Resuming setup: Product guide is complete. Next: create product guidelines." |
| `architect/tech-stack.md` is missing or incomplete | Section 7 | "Resuming setup: Guidelines are complete. Next: define the technology stack." |
| `architect/code_styleguides/` is missing or empty | Section 8 | "Resuming setup: Tech stack is defined. Next: select code style guides." |
| `architect/workflow.md` is missing or incomplete | Section 9 | "Resuming setup: Guides and tech stack are configured. Next: define project workflow." |
| `architect/index.md` is missing or incomplete | Section 10 | "Resuming setup: Workflow is defined. Next: generate project index." |
| Any incomplete `architect/tracks/<track_id>/` exists | Section 11.1 | "Resuming setup: I found an incomplete track folder. I will inspect it and ask before changing it." |
| No complete track exists in `architect/tracks/` | Section 11.2 | "Resuming setup: Scaffolding is complete. Next: generate the first track." |
| `architect/index.md`, `architect/tracks.md`, and at least one complete `tracks/<track_id>/` containing `spec.md`, `plan.md`, `metadata.json`, and `index.md` exist after all prerequisites above are satisfied | Halt | "The project is already initialized. Use `/architect-propose` or `/architect-implement`." |

Treat a Markdown artifact as incomplete when it is empty or only contains an obvious placeholder from an interrupted write. Treat `architect/code_styleguides/` as complete only when it contains at least one direct child `.md` guide.

Always run Section 4.1 first to establish Greenfield or Brownfield context before jumping to a later target. Run the Greenfield or Brownfield inception flow only when the audit target is Section 4.

## 4. Project Inception

### 4.1 Detect Project Maturity

Classify the project as Brownfield when any primary indicator exists:

- Dependency manifests: `package.json`, `pom.xml`, `requirements.txt`, `go.mod`, `Cargo.toml`.
- Source directories containing code: `src/`, `app/`, `lib/`, `bin/`.
- A Git repository with uncommitted changes outside `architect/` may be treated as additional Brownfield evidence.

Classify as Greenfield only when no application source code or dependency manifests exist, ignoring `architect/`, a clean or newly initialized `.git`, and `README.md`.

If the audit target is later than Section 4, announce the maturity and the reason, then jump to that target. Do not initialize Git, ask for a project goal, or run the Brownfield read-only scan. For resume context, read existing Architect files only; ask the user before any broader project scan.

### 4.2 Brownfield Inception

Run this subsection only when the audit target is Section 4 and Brownfield is detected:

1. Announce the specific indicator, such as `package.json`.
2. If Git has uncommitted changes outside `architect/`, warn the user that setup will modify files.
3. Ask permission for a read-only scan:
   - Title: `Permission`
   - Prompt: `A brownfield (existing) project has been detected. May I perform a read-only scan to analyze the project?`
   - Choices: `Yes`, `No`
4. If denied, halt.
5. If approved, analyze the project:
   - Read `README.md` first when present.
   - Respect `.gitignore` when scanning.
   - Prefer high-value files: manifests, configs, package metadata, small docs, and top-level directory structure.
   - Do not read large files fully. For files over 1 MB, inspect only enough context to infer purpose.
6. Infer and retain:
   - Programming language.
   - Frontend and backend frameworks.
   - Database drivers or persistence layer.
   - Architecture type, such as monorepo, service, MVC, SPA, or library.
   - Project goal from `README.md` or manifest description.
7. Proceed to Section 5.

### 4.3 Greenfield Inception

Run this subsection only when the audit target is Section 4 and Greenfield is detected:

1. Announce that no existing application code or dependency manifests were found.
2. If `.git` does not exist, ask before initializing Git. If the user agrees, run `git init`.
3. Ask the user:
   - Title: `Project Goal`
   - Prompt: `What do you want to build?`
   - Free-text answer.
4. Create `architect/product.md` with:

```markdown
# Initial Concept

<user response>
```

5. Proceed to Section 5.

## 5. Generate Product Guide

Create or complete `architect/product.md`.

1. Announce that you will help create the product guide.
2. Ask the user to choose a workflow:
   - Title: `Product`
   - Prompt: `How would you like to define the product details? Whether you prefer a quick start or a deep dive, both paths lead to a high-quality product guide.`
   - Choices:
     - `Interactive`: Guide the user through questions.
     - `Autogenerate`: Draft from the initial project goal and brownfield analysis when available.
3. If Interactive, ask up to four batched questions. Use choices with useful suggested answers. Ask about target users, primary goals, key features, and constraints. In Brownfield projects, do not ask for information already present in the codebase.
4. Draft a polished product guide. Use only the user's selected answers plus already-audited project facts as source material.
5. Ask for approval with the full draft embedded in the question:
   - Choices: `Approve`, `Suggest changes`.
6. If the user suggests changes, revise and repeat approval.
7. Once approved, write the result to `architect/product.md`. If `# Initial Concept` exists, keep it at the top and append the approved Product Guide below it rather than replacing the initial concept.

Suggested structure:

```markdown
# Product Guide

## Vision
## Users
## Goals
## Core Capabilities
## Constraints
## Success Criteria
```

## 6. Generate Product Guidelines

Create `architect/product-guidelines.md`.

1. Announce the section.
2. Ask the user to choose:
   - `Interactive`: Ask about prose style, brand tone, UX principles, accessibility, and design priorities.
   - `Autogenerate`: Draft standard guidelines from the product guide.
3. If Interactive, ask up to four batched questions with high-quality suggestions. For Brownfield projects, align suggestions with existing documentation and UI style.
4. Draft the guidelines.
5. Ask for approval with the full draft embedded.
6. Revise until approved.
7. Write `architect/product-guidelines.md`.

Suggested structure:

```markdown
# Product Guidelines

## Voice and Tone
## UX Principles
## Accessibility
## Content Rules
## Visual Direction
## Quality Bar
```

## 7. Generate Tech Stack

Create `architect/tech-stack.md`.

### 7.1 Greenfield

Ask the user to choose:

- `Interactive`: Pick language, frameworks, data layer, testing, and deployment.
- `Autogenerate`: Recommend a proven stack for the product goal.

If Interactive, batch up to four questions. Allow multi-select when combinations are useful.

### 7.2 Brownfield

Document the existing stack, do not propose changes.

1. State the inferred stack.
2. Ask: `Is the inferred tech stack correct?`
3. If the user says no, ask them to provide the corrected stack in text.

### 7.3 Draft and Write

Draft `architect/tech-stack.md`, ask for approval with the full content embedded, revise if needed, then write the file.

Suggested structure:

```markdown
# Technology Stack

## Runtime and Language
## Frameworks
## Data and Persistence
## Testing
## Tooling
## Deployment
## Constraints and Decisions
```

## 8. Select Code Style Guides

Create `architect/code_styleguides/`, copy selected bundled guides, and optionally generate temporary guides after user approval.

Available bundled guides are the Markdown files in the skill bundled resource directory `references/code_styleguides/`. Enumerate that bundled resource directory at setup time and present matching guide names to the user so newly added guides are automatically available.

For Greenfield projects:

1. Recommend guide(s) based on `architect/tech-stack.md`.
2. Ask whether to use recommended guides or select manually.
3. If manual, present available guides in batches with multi-select.

For Brownfield projects:

1. Recommend guide(s) based on the inferred stack.
2. Ask whether to proceed or add more.

Write approved guides under `architect/code_styleguides/` and include missing guide decisions in the setup summary.

## 9. Select Workflow

Create `architect/workflow.md` from the bundled resource template `references/workflow.md`.

1. Ask the user:
   - Title: `Workflow`
   - Prompt: `Use the default workflow (>80% coverage; commits only when authorized) or customize it?`
   - Choices: `Default`, `Customize`.
2. If Default, write the bundled workflow unchanged except for any needed Architect path consistency.
3. If Customize, ask for:
   - Desired coverage percentage.
   - Commit frequency.
   - Where task summaries should be recorded.
4. Show the resulting workflow choices and ask whether anything else should change.
5. Write `architect/workflow.md`.

Remember: the skill should not perform commits unless the user explicitly requests them, even if the workflow template describes commit behavior for implementation phases.

## 10. Finalize Project Context

Create `architect/index.md`:

```markdown
# Project Context

## Definition
- [Product Definition](./product.md)
- [Product Guidelines](./product-guidelines.md)
- [Tech Stack](./tech-stack.md)

## Workflow
- [Workflow](./workflow.md)
- [Code Style Guides](./code_styleguides/)

## Management
- [Tracks Registry](./tracks.md)
- [Tracks Directory](./tracks/)
```

Then summarize:

- Files created or updated.
- Code style guides selected.
- Workflow mode selected.
- Whether the setup was Greenfield or Brownfield.

Announce that setup is ready to generate the first track.

## 11. Initial Plan and Track Generation

Interactively define the first track and create track artifacts.

### 11.1 Cleanup Incomplete Track State

If `architect/tracks/` exists but contains incomplete setup-generated track folders, ask the user before deleting or replacing them. A track folder is incomplete when it is missing any of `spec.md`, `plan.md`, `metadata.json`, or `index.md`. If an incomplete folder contains unexpected files, assume it may include user work and ask before changing it. Do not delete user-created work silently.

### 11.2 Propose One Initial Track

1. Explain that a track is a high-level unit of work such as a feature, bug fix, or setup milestone.
2. Generate one concise track title:
   - Greenfield: focus on the MVP core.
   - Brownfield: focus on maintenance or a targeted enhancement.
3. Ask for confirmation:
   - Choices: `Yes`, `Suggest changes`.
4. If the user suggests changes, ask for the desired track description.

### 11.3 Create Track Artifacts

Create `architect/tracks.md` with the first track:

```markdown
# Project Tracks

This file tracks all major tracks for the project. Each track has its own detailed plan in its respective folder.

---

- [ ] **Track: <Track Description>**
  *Link: [./tracks/<track_id>/](./tracks/<track_id>/)*
```

Generate one track ID from the description with format `YYYYMMDD_shortname`, and use the exact same ID everywhere. Build `shortname` by lowercasing the description, keeping ASCII letters and numbers, replacing spaces with underscores, stripping punctuation, and using at most four meaningful words. The final `track_id` must match `^[0-9]{8}_[a-z0-9_]+$`.

Before creating any track artifacts, run a collision check against both `architect/tracks/` and `architect/tracks.md` when they exist:

- Existing track directories must not contain the same track ID.
- Existing track directories must not contain the same short name after the date prefix.
- The tracks registry must not already mention the same track ID or short name.

If any collision exists, halt and explain that a matching track already exists. Suggest resuming the existing track, cleaning up the interrupted setup state, or choosing a different initial track description.

Create `architect/tracks/<track_id>/` containing:

- `metadata.json`
- `spec.md`
- `plan.md`
- `index.md`

`metadata.json` structure:

```json
{
  "track_id": "<track_id>",
  "type": "feature",
  "status": "new",
  "created_at": "YYYY-MM-DDTHH:MM:SSZ",
  "updated_at": "YYYY-MM-DDTHH:MM:SSZ",
  "description": "<Track Description>"
}
```

Use `type: "feature"` by default, or `type: "bug"` when the approved track is clearly a bug fix.

`index.md` structure:

```markdown
# Track <track_id> Context

- [Specification](./spec.md)
- [Implementation Plan](./plan.md)
- [Metadata](./metadata.json)
```

### 11.4 Generate `spec.md`

The spec should include:

- Track summary.
- User or system goals.
- Functional requirements.
- Non-functional requirements.
- Acceptance criteria.
- Out of scope.
- Risks and assumptions.

### 11.5 Generate `plan.md`

The plan must follow `architect/workflow.md`.

Rules:

- Include status markers `[ ]` for every parent task and sub-task.
- Parent task format: `- [ ] Task: ...`
- Sub-task format: `    - [ ] ...`
- If `architect/workflow.md` defines a Phase Completion Verification and Checkpointing Protocol, append a final meta-task to every phase:
  - `- [ ] Task: Architect - User Manual Verification '<Phase Name>' (Protocol in workflow.md)`
- If the workflow uses TDD, split implementation work into test-writing and implementation subtasks.

Recommended structure:

```markdown
# Implementation Plan: <Track Description>

## Phase 1: Foundation
- [ ] Task: ...
    - [ ] Write tests for ...
    - [ ] Implement ...
- [ ] Task: Architect - User Manual Verification 'Foundation' (Protocol in workflow.md)

## Phase 2: Core Behavior
- [ ] Task: ...
    - [ ] Write tests for ...
    - [ ] Implement ...
- [ ] Task: Architect - User Manual Verification 'Core Behavior' (Protocol in workflow.md)
```

### 11.6 Completion

Announce that Architect setup and initial track generation are complete.

If the user explicitly requested a commit, commit all Architect files with:

```text
architect(setup): add architect setup files
```

Otherwise, tell the user the files are ready and that they can begin with `/architect-implement`.
