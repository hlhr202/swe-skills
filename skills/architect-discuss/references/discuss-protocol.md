# Architect Discuss Protocol

## Purpose

Turn an early product or technical requirement into a reviewable product and architecture draft before tracked proposal work begins. Discussion clarifies intent, scope, system context, options, tradeoffs, risks, assumptions, and readiness for `architect-propose`.

## Success Criteria

Discussion succeeds when the resulting synthesis:

- Makes the problem, users, value, goals, and non-goals clear.
- Reflects relevant repository and Architect context.
- Separates confirmed decisions, assumptions, recommendations, deferred decisions, and open questions.
- Compares meaningful architecture options when the solution space is open.
- Explains the recommended direction and accepted tradeoffs.
- Identifies product, technical, and operational risks.
- States whether the initiative is ready for `architect-propose` and at what scope.

The synthesis is a draft for review, not an implementation contract.

## Hard Boundaries

- Use this protocol only when the user explicitly invokes `architect-discuss` or directly asks to use this skill.
- Discussion must not create or update tracked Architect artifacts: no `architect/tracks.md`, track directory, finalized `spec.md`, `plan.md`, `metadata.json`, or track `index.md`.
- Discussion must not modify implementation code, scaffold modules or services, or run validation as if the work had been implemented.
- Do not automatically invoke or execute `architect-propose`, `architect-implement`, `architect-review`, or `architect-status`.
- Do not commit unless the user explicitly requests a commit in the current conversation.
- Keep any saved standalone draft inside the project. Reject absolute paths, parent traversal (`..`), paths outside the workspace, and tracked-Architect artifact paths.

These boundaries remain in force even when the likely implementation is obvious.

## State Model

Discussion progresses through resumable gates:

```text
triggered
  -> background_ready
  -> requirements_ready
  -> scope_ready
  -> product_ready
  -> constraints_ready
  -> direction_ready
  -> tradeoffs_ready
  -> synthesis_ready
  -> synthesized
  -> handoff_or_stop
```

Each gate has one of three states:

- `Passed`: required decisions are sufficiently clear.
- `Needs input`: a user-owned or direction-changing decision is missing.
- `Deferred`: the unresolved item is explicit and does not invalidate later work.

Gate pass mode is `Explicit`, `Auto`, or `Deferred`. Auto-pass only when the answer is already established by the prompt, prior discussion, repository evidence, or a low-risk assumption.

At every gate, emit a compact recovery block:

```markdown
## Discussion State

- Current loop: <loop-name>
- Gate status: Passed / Needs input / Deferred
- Gate pass mode: Explicit / Auto / Deferred
- Confirmed decisions:
- Assumptions:
- Deferred questions:
- Next loop:
```

## Decision Rules

### Ask only material questions

Ask when the answer can change product scope, architecture direction, delivery cost, operational risk, or proposal readiness. Do not ask about implementation detail unless it changes architecture.

- Ask one focused question at a time by default.
- Batch only tightly related, low-cognitive-load questions.
- Do not ask the user to reconfirm information already supplied.
- Offer a low-risk likely answer as an assumption the user can correct.
- Distinguish facts, assumptions, recommendations, and user-owned decisions.

### Recommend before asking for a choice

When evidence supports a direction, state the recommendation and a short reason before asking the user to choose. Do not invent a recommendation for user-owned business priority, target audience, success criteria, policy, or organizational preference.

### Auto-pass versus ask

Auto-pass and explain why when a gate is already clear. Never auto-pass a missing decision that materially changes:

- Architecture or system boundaries.
- Security, privacy, compliance, or audit posture.
- Data ownership or consistency model.
- Public API or consumer contracts.
- Migration or rollout strategy.
- Scope decomposition or proposal readiness.

### Context depth

For an existing repository area, perform a shallow targeted scan before recommending architecture. Prefer `architect/product.md`, `architect/product-guidelines.md`, `architect/tech-stack.md`, `architect/workflow.md`, `architect/tracks.md`, relevant safe `architect/tracks/<track_id>/` artifacts, and directly related docs, code, APIs, schemas, and service boundaries. Do not over-explore implementation before product scope and architecture direction are stable.

### Scope decomposition

If the requirement contains separable initiatives, recommend either one focused draft, a high-level platform draft, or an explicit set of proposal candidates. When later proposal work is likely, prefer a focused initiative that maps to one track.

### Architecture options

When multiple directions are genuinely viable, present 2–3 compact options with best-fit condition and main tradeoff. Deepen only selected or contested options. Recommend one when evidence is sufficient; otherwise keep the unresolved choice explicit.

### Final synthesis

Do not front-load the full synthesis. Generate it only after `synthesis_ready`, or when the user explicitly requests synthesis with unresolved gates. In the latter case, label every unresolved item as an assumption, open question, or deferred decision.

## Approval Boundaries

| Action | Required approval |
| --- | --- |
| Advance past a material unresolved gate | Explicit decision or explicit deferral |
| Generate final synthesis | Readiness confirmation, unless user explicitly requests unresolved synthesis |
| Save a standalone draft | user-confirmed relative path |
| Overwrite an existing draft | Explicit confirmation of that exact path and overwrite |
| Commit a saved discussion artifact | Explicit commit request in the current conversation |
| Create tracked proposal artifacts | Not authorized here; hand off to `architect-propose` |

Approval to synthesize does not authorize saving. Approval to save does not authorize proposing, implementing, or committing.

## Workflow

### Interaction pattern

For each loop:

1. Present short context.
2. Ask one focused question or a compact related choice set when needed.
3. Incorporate the answer into discussion state.
4. Continue only while unresolved information affects later loops.
5. Present the gate summary.
6. Proceed after the gate passes or is explicitly deferred.

Detailed drafts, Markdown, tables, diagrams, and tradeoff analysis belong in normal assistant messages. Interactive prompts are decision boundaries only: keep their question, labels, and descriptions short and plain text. If structured interaction is unavailable, present the same concise question in chat and wait.

### 1. Qualify trigger

Confirm explicit `architect-discuss` invocation. Decline this protocol for ordinary architecture conversation that does not name the skill, or when the user clearly requests setup, tracked proposal creation, implementation, review, or status.

### 2. Frame background

Build enough repository and domain context to identify relevant domains, modules, services, packages, docs, conventions, and initial architecture implications. Present a short background summary, not the final draft.

Gate: the discussion target, user intent, and necessary context are clear or explicitly deferred.

### 3. Clarify requirements

Stabilize the problem statement, users or consumers, motivation, desired behavior, success criteria, goals, non-goals, affected domains, and whether the request contains multiple initiatives.

Gate: requirement scope is stable enough to decompose.

### 4. Confirm draft scope

Split separable initiatives when needed. Record broader deferred work and identify the likely proposal-sized unit.

Gate: the target is one initiative, one high-level platform draft, or an explicit set of proposal candidates.

### 5. Clarify product behavior

Cover only behavior that can affect architecture: roles and permissions, primary journeys, functional requirements, business rules, state transitions, failures, admin or operational workflows, configuration, backward compatibility, MVP, and future scope.

Gate: core journeys, required behavior, business rules, failure behavior, MVP, and non-goals are clear or safely deferred.

### 6. Clarify constraints

Cover material latency, consistency, reliability, recovery, security, privacy, compliance, audit, observability, scale, cost, deployment, and rollout constraints.

Gate: remaining uncertainty cannot invalidate the architecture direction.

### 7. Select architecture direction

Present compact options when the solution space is open:

```markdown
## Architecture Direction Options

Option A: <name>
- Best for: <condition>
- Tradeoff: <main tradeoff>

Option B: <name>
- Best for: <condition>
- Tradeoff: <main tradeoff>

Recommended starting point:
- <option and rationale>
```

For a selected or contested option, expand product impact, technical impact, benefits, costs, risks, and best-fit conditions.

Gate: one direction is confirmed, or the user explicitly asks to retain multiple options; rejected options and major impacts are recorded.

### 8. Resolve direction-changing tradeoffs

Handle one major tradeoff at a time. Include system boundaries, data ownership, consistency, user-visible behavior, APIs, permissions, security/privacy/compliance, migration, operations, performance, cost, scale, and sequencing when relevant.

Record decision pressure, options, recommendation, rationale, and status (`Confirmed`, `Assumed`, `Needs decision`, or `Deferred`). Defer exact fields, functions, props, test-file layout, micro-interactions, and helper design unless they affect architecture.

Gate: direction-changing tradeoffs are confirmed, assumed, or safely deferred.

### 9. Confirm synthesis readiness

Present:

```markdown
## Readiness Check

Confirmed:
- <decision>

Assumptions:
- <assumption>

Deferred:
- <question>

Final synthesis scope:
- <scope>
```

Ask whether to synthesize, revise a prior loop, or continue tradeoff discussion.

### 10. Generate and self-review the synthesis

Write in the user's main language while preserving project terms and identifiers. Scale detail to the initiative. Use this structure unless the user requests another:

```markdown
# <Initiative Name> Product & Technical Architecture Draft

## 1. Executive Summary
## 2. Problem Statement
## 3. Goals
## 4. Non-Goals
## 5. Users And Use Cases
## 6. Functional Requirements
## 7. Non-Functional Requirements
## 8. Current System Context
## 9. Proposed Architecture
## 10. Architecture Options Considered
## 11. Recommended Approach
## 12. Product/Architecture Tradeoffs
## 13. Implementation Shape
## 14. Risks And Mitigations
## 15. Assumptions
## 16. Open Questions
## 17. Readiness For Proposal
```

Populate sections with the corresponding decisions already discussed. Options Considered must not introduce all options for the first time.

Before presenting, remove unresolved `TBD` or `TODO`, correct assumptions stated as facts, resolve contradictions, add missing major tradeoffs, remove implementation over-specification, verify repository references, and check whether scope is proposal-sized.

### 11. Review, save, or hand off

After presenting the synthesis, offer:

1. Continue or reopen a specific discussion loop.
2. Save a standalone draft.
3. Hand off the confirmed scope to `architect-propose`.
4. Split the synthesis into proposal candidates.
5. Stop.

For a standalone draft, recommend `architect/drafts/<initiative-name>.md`, using lowercase ASCII hyphenated words. Confirm the relative path, reject tracked-artifact targets, check for existing content, and use a reviewable edit mechanism. Do not overwrite without exact confirmation.

For proposal handoff, summarize confirmed scope and unresolved questions. Do not create the proposal in this protocol.

## Stop Conditions

Stop and report the current Discussion State when:

- Explicit invocation is absent.
- A material user-owned decision remains unresolved and cannot be deferred safely.
- A requested path is unsafe or targets tracked artifacts.
- Saving would overwrite a file without exact confirmation.
- The user requests implementation or tracked proposal creation instead of discussion.
- An operation remains unsuccessful after one clear correction.
- The user selects a next path or ends discussion.
