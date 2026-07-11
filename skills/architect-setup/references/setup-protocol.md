# Architect Setup Protocol

## Purpose

Initialize or resume the durable Architect core context under `architect/`. Setup establishes product, guidelines, technology, code-style, workflow, and index context; it does not create proposal or track artifacts.

## Success Criteria

Setup succeeds when all core files exist, contain approved project context, and `architect/index.md` links to them:

- `architect/product.md`
- `architect/product-guidelines.md`
- `architect/tech-stack.md`
- At least one direct child `.md` file in `architect/code_styleguides/`
- `architect/workflow.md`
- `architect/index.md`

The completion message identifies whether the project is Greenfield or Brownfield, summarizes created or updated files, and recommends `/architect-discuss` next.

## Hard Boundaries

- Setup creates core context only. It must not create, repair, delete, or modify track artifacts, including `architect/tracks.md`, `architect/tracks/`, or files inside a track.
- Keep Architect-managed writes under `architect/`. Reject absolute paths and parent traversal (`..`).
- Use the runtime's safest reviewable edit mechanism, preferably patch-based. Do not write files with shell redirection.
- Validate every operation before continuing. Retry once only when the failure has a clear, recoverable path or command correction.
- Do not commit unless the user explicitly requests a commit in the current conversation.

These are invariants, not judgment calls. Stop rather than weakening them.

## State Model

Setup advances through the earliest incomplete state:

| State | Required evidence | Next state |
| --- | --- | --- |
| `uninitialized` | No Architect core artifacts | `product_ready` |
| `product_ready` | Complete `product.md` | `guidelines_ready` |
| `guidelines_ready` | Complete `product-guidelines.md` | `tech_ready` |
| `tech_ready` | Complete `tech-stack.md` | `guides_ready` |
| `guides_ready` | Non-empty `code_styleguides/` with a direct child `.md` file | `workflow_ready` |
| `workflow_ready` | Complete `workflow.md` | `core_ready` after `index.md` is generated |
| `core_ready` | Every success criterion is satisfied | Terminal; recommend discuss or propose |

A Markdown file is incomplete when empty or when it contains only an obvious interrupted-write placeholder. Always resume at the earliest missing or incomplete prerequisite, even if later files already exist.

## Decision Rules

### Project maturity

- Classify as Brownfield when a primary indicator exists: a dependency manifest (`package.json`, `pom.xml`, `requirements.txt`, `go.mod`, `Cargo.toml`) or application code under `src/`, `app/`, `lib/`, or `bin/`. Uncommitted non-Architect Git changes are supporting evidence.
- Classify as Greenfield only when no application source or dependency manifest exists, ignoring `architect/`, a new or clean `.git`, and `README.md`.
- Always classify maturity before resuming. When resuming after project inception, announce the classification and reason, read existing Architect files for context, and do not initialize Git, ask for a new project goal, or perform a broad Brownfield scan without permission.

### Resume routing

| Earliest missing state | Resume action |
| --- | --- |
| No Architect artifacts | Run project inception |
| `product.md` | Generate product guide |
| `product-guidelines.md` | Generate product guidelines |
| `tech-stack.md` | Define technology stack |
| `code_styleguides/` | Select code style guides |
| `workflow.md` | Select project workflow |
| `index.md` | Generate project index |
| None | Stop: project already initialized |

When already initialized, say: `The project is already initialized. Use /architect-discuss to explore the next direction, or /architect-propose when a track scope is already confirmed.`

### Interaction discipline

- Present full drafts, diffs, and explanations in normal assistant messages.
- Use the runtime's interaction mechanism only for concise questions and short choices. If structured interaction is unavailable, present the same choices in text and wait.
- Do not ask for information already established by repository evidence or approved Architect context.

## Approval Boundaries

| Action | Required approval |
| --- | --- |
| Brownfield repository scan | Explicit `Yes` after the read-only scan prompt |
| `git init` for Greenfield | Explicit user agreement |
| Write product guide | Product draft approval |
| Write product guidelines | Guidelines draft approval |
| Write or correct tech stack | Tech stack approval |
| Copy code style guides | User-approved selection |
| Generate a missing temporary style guide | Explicit approval for that guide |
| Write customized workflow | Confirmation of workflow choices |
| Commit setup files | User explicitly requests a commit in the current conversation |

Approval for one row does not authorize another.

## Workflow

### 1. Audit and announce

Inspect the six success-criteria locations, determine the earliest missing state, and classify project maturity. For a new setup, present this compact overview:

1. Discover the project.
2. Define product context and technology.
3. Select style guides and workflow.
4. Finish with core context and hand off to `architect-discuss`.

For a resumed setup, announce the earliest missing artifact and the next action. Do not repeat completed stages.

### 2. Run project inception only for `uninitialized`

#### Brownfield

1. Announce the indicator that established Brownfield status.
2. Warn when Git has uncommitted changes outside `architect/`.
3. Ask:
   - Title: `Permission`
   - Prompt: `A brownfield (existing) project has been detected. May I perform a read-only scan to analyze the project?`
   - Choices: `Yes`, `No`
4. Halt if denied.
5. If approved, read `README.md` first when present; respect `.gitignore`; prioritize manifests, configs, package metadata, small docs, and top-level structure; sample rather than fully reading files over 1 MB.
6. Infer language, frameworks, persistence, architecture type, and project goal.

#### Greenfield

1. Announce that no application code or dependency manifest was found.
2. If `.git` is absent, ask before running `git init`.
3. Ask with Title `Project Goal` and Prompt `What do you want to build?` using free text.
4. Create or preserve the initial concept at the top of `architect/product.md`:

```markdown
# Initial Concept

<user response>
```

### 3. Create the product guide

Ask with Title `Product` and Prompt `How would you like to define the product details? Whether you prefer a quick start or a deep dive, both paths lead to a high-quality product guide.` Choices are `Interactive` and `Autogenerate`.

- Interactive: ask up to four batched questions about users, goals, capabilities, constraints, and success criteria. In Brownfield projects, skip facts already visible in the repository.
- Autogenerate: draft from the initial goal and approved Brownfield evidence.

Present the full draft, then ask `Approve` or `Suggest changes`. Revise until approved and write `architect/product.md`. Preserve an existing `# Initial Concept` above the guide.

Recommended sections: Vision, Users, Goals, Core Capabilities, Constraints, Success Criteria.

### 4. Create product guidelines

Ask for `Interactive` or `Autogenerate` mode. Interactive mode covers prose style, brand tone, UX principles, accessibility, and design priorities, with at most four batched questions. Brownfield suggestions should reflect existing UI and documentation.

Present the full draft, revise until approved, then write `architect/product-guidelines.md` with sections for Voice and Tone, UX Principles, Accessibility, Content Rules, Visual Direction, and Quality Bar.

### 5. Define the technology stack

- Greenfield: ask for `Interactive` or `Autogenerate`. Interactive mode may batch up to four questions covering language, frameworks, data, testing, and deployment.
- Brownfield: document the existing stack without proposing changes. State the inference and ask whether it is correct; if not, request the corrected stack in text.

Present and approve the complete draft before writing `architect/tech-stack.md`. Cover Runtime and Language, Frameworks, Data and Persistence, Testing, Tooling, Deployment, and Constraints and Decisions.

### 6. Select code style guides

Enumerate direct Markdown files in the bundled `references/code_styleguides/` directory at runtime so newly bundled guides remain discoverable.

- Greenfield: recommend guides from the approved tech stack, then let the user accept or select manually.
- Brownfield: recommend guides from the detected stack, then let the user proceed or add more.

Copy only approved guides into `architect/code_styleguides/`. When no bundled guide fits, generate a temporary guide only after user approval. Report every missing-guide decision.

### 7. Select workflow

Ask:

- Title: `Workflow`
- Prompt: `Use the default workflow (>80% coverage; commits only when authorized) or customize it?`
- Choices: `Default`, `Customize`

For Default, copy bundled `references/workflow.md`, changing only what path consistency requires. For Customize, ask for coverage target, commit frequency, and task-summary location. Present the resulting choices, accept further changes, then write `architect/workflow.md`.

Workflow text may describe later implementation commits; setup itself still requires explicit commit authorization.

### 8. Finalize core context

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
```

Report maturity, created or updated files, selected guides, and workflow mode. Recommend `/architect-discuss`; mention `/architect-propose` only when scope is already confirmed.

If the user explicitly requests a commit, use:

```text
architect(setup): add architect setup files
```

## Stop Conditions

Stop and report the blocker when:

- Brownfield scan permission is denied.
- A required path is unsafe or leaves `architect/`.
- An operation remains unsuccessful after one clear correction.
- Core context is already complete.
- The next requested action would create or repair proposal or track artifacts.

On a normal successful stop, do not create tracks and hand off to `/architect-discuss`.
