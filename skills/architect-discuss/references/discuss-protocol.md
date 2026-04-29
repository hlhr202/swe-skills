# Architect Discuss Protocol

## Purpose

Turn an early product or technical requirement into a comprehensive product and architecture draft that can be reviewed, refined, and optionally handed off to `architect-propose`.

This is a discussion and drafting step. It clarifies product intent, system context, architecture options, tradeoffs, risks, assumptions, and proposal readiness before any tracked implementation proposal is created.

`architect-discuss` is not a proposal, implementation, review, or status step. It may inspect repository context and produce draft text, but it must not create finalized Architect workflow artifacts or perform implementation work.

## Inputs

- Raw user requirement, product idea, bug context, refactor direction, or architecture question.
- Existing Architect docs and repository context relevant to the topic.
- Known product goals, users, workflows, constraints, and non-goals.
- Known technical constraints, modules, APIs, schemas, deployment, or operations requirements.

## Boundaries

`architect-discuss` may:

- Clarify product and technical requirements.
- Inspect relevant docs and code structure.
- Summarize current system context.
- Compare architecture options and tradeoffs.
- Recommend a direction with rationale.
- Produce a comprehensive product and architecture draft in the conversation.
- Update the draft through user feedback.
- Recommend handoff to `architect-propose` when the user wants tracked proposal artifacts.

`architect-discuss` must not:

- Create or update `architect/tracks.md`.
- Create track folders under `architect/tracks/`.
- Create finalized `metadata.json`, `spec.md`, `plan.md`, or `index.md`.
- Modify implementation code.
- Scaffold modules, packages, services, APIs, or UI.
- Run implementation validation as if work has been built.
- Automatically invoke `architect-propose`, `architect-implement`, `architect-review`, or `architect-status`.
- Create commits unless the user explicitly asks for a commit.

If the user has already confirmed the requirement and explicitly wants tracked proposal artifacts, use `architect-propose` instead. If the user asks to implement an existing track, use `architect-implement`. If the user asks for progress on tracked work, use `architect-status`.

## Operating Principle

Use progressive interactive loops with explicit gates, not a one-shot long report.

Each loop should clarify one category of decisions through short, focused questions. Ask one question at a time by default. A compact batch is allowed only when the questions are tightly related and low-cognitive-load.

Each loop must end with a gate before moving to the next loop. The gate confirms that the current category is clear enough to proceed, or records assumptions and deferred decisions explicitly.

A gate may be auto-passed when the required information is already clear from the user's prompt, prior discussion, repository context, or low-risk assumptions. Auto-passed gates must still be recorded with a reason and discussion state. Do not ask the user to reconfirm information they already provided.

Clarify ambiguities that affect product scope, architecture direction, delivery cost, operational risk, or proposal readiness. Do not try to resolve every implementation detail. When uncertainty remains, mark it honestly as an assumption, open question, or deferred detail.

The goal is a draft that is comprehensive enough to support product and technical review, not a final implementation contract.

The comprehensive product and architecture draft is the final synthesis artifact. Do not front-load it into the first response.

## Interaction Rules

### Interactive Prompt Boundary Rule

Interactive tools used for clarification, confirmation, or feedback may have limited rendering capabilities across coding agents. Do not rely on them to render Markdown, code blocks, tables, long lists, full drafts, architecture diagrams, detailed tradeoff analysis, or detailed reports.

When a human decision requires detailed context, present that context first in a normal assistant message. Then use the interactive confirmation tool only for a concise plain-text question and short plain-text choices.

Treat the interactive prompt as a decision boundary, not as the primary place to explain context.

When using an interactive question tool:

- Keep question text, option labels, and option descriptions short and plain text.
- Do not include Markdown formatting, code fences, tables, full product/architecture drafts, long tradeoff lists, diffs, or detailed context summaries in the tool payload.
- Put longer requirement summaries, scope decomposition, architecture options, tradeoff analysis, draft sections, and handoff rationale in the preceding assistant message.
- For draft review or handoff decisions, present the detailed draft or summary in a normal assistant message, then ask a short question such as `What should we do next?`.

### Discussion First

Start from the user's current requirement. If the request is unclear, summarize the current understanding and ask targeted questions before drafting.

Questioning rules:

- Ask only questions that can change product scope, architecture direction, delivery cost, or risk.
- Ask one focused question at a time by default.
- Group related questions into a compact batch only when they are tightly related and easy to answer together.
- Avoid asking about low-level implementation details unless they affect architecture.
- Offer explicit assumptions when the likely answer is clear enough to keep moving.
- Distinguish confirmed facts from assumptions and recommendations.

### Recommendation Before Choice Rule

When asking the user to choose among options, lead with a recommended option when enough context exists. Include a short reason tied to product scope, architecture direction, delivery cost, risk, or proposal readiness.

Do not invent a recommendation when the missing information is genuinely user-owned, such as business priority, target user, success criteria, policy decision, or organizational preference. In those cases, ask a direct clarification question.

If a likely answer is low-risk, present it as an assumption the user can accept or correct.

Preferred choice prompt shape:

```md
Recommendation:
- <recommended option>

Reason:
- <short reason>

Question:
- <concise decision question>
```

For interactive question tools, keep the tool payload short and put the recommendation and reason in the preceding assistant message.

### Cross-Agent State Rule

This skill may be used across different agent sessions. Do not rely on hidden memory. At each gate, output a compact discussion state block that another agent can use to resume the workflow.

Use this shape:

```md
## Discussion State

- Current loop: <loop-name>
- Gate status: Passed / Needs input / Deferred
- Gate pass mode: Explicit / Auto / Deferred
- Confirmed decisions:
- Assumptions:
- Deferred questions:
- Next loop:
```

Keep the state block concise. It is a recovery aid, not the final draft.

### Loop Gate Pattern

Every loop follows the same interaction pattern:

1. Present short context for the current loop.
2. Ask one focused question or one small set of tightly related choices.
3. Incorporate the user's answer into the discussion state.
4. Continue asking only if unresolved information would affect later loops.
5. Present a gate summary when the loop is clear enough.
6. Ask the user to proceed, revise, or defer unresolved points.
7. Move to the next loop only after the gate is passed or explicitly deferred.

If the answer is already clear, do not ask a redundant question. Instead, present an auto-pass gate summary with the reason it is safe to proceed.

At each gate, include the `Discussion State` block so another agent can resume the workflow.

Use this shape for auto-passed gates:

```md
## Gate: <Loop Name>

Auto-passed.

Reason:
- <why this loop is clear enough from prompt, context, prior discussion, or low-risk assumptions>

Confirmed:
- <confirmed decision>

Assumptions:
- <assumption>

Deferred:
- <deferred question>
```

Do not auto-pass when the missing decision would materially change architecture direction, security/privacy/compliance posture, data ownership, scope decomposition, public API exposure, consistency model, migration strategy, or proposal readiness.

### Context Before Architecture

When the request relates to an existing repository area, inspect enough context to avoid proposing architecture that conflicts with existing docs, modules, or workflow conventions.

Prefer a shallow targeted scan of:

- `architect/product.md`
- `architect/product-guidelines.md`
- `architect/tech-stack.md`
- `architect/workflow.md`
- `architect/tracks.md`
- Relevant `architect/tracks/<track_id>/` artifacts when discussing existing tracked work.
- Relevant local docs, code structure, API contracts, schemas, or service boundaries.

Do not over-explore implementation details before product scope and architecture direction are reasonably clear.

### No Premature Formalization

Do not write tracked proposal files during discussion. If the user wants the draft saved as a standalone document, recommend `architect/drafts/<initiative-name>.md` as the default target path and ask the user to confirm or change it unless they already provided a target path.

Build `<initiative-name>` from the final synthesis title or confirmed initiative name using lowercase ASCII words separated by hyphens, for example `architect/drafts/reporting-permissions-model.md`.

Standalone draft saves must follow these path and edit safety rules:

- Use a user-confirmed path relative to the project root.
- Prefer `architect/drafts/` for standalone discussion artifacts that are not tracked proposals.
- Reject absolute paths, parent-directory paths (`..`), and paths outside the project workspace.
- Do not target tracked Architect artifacts such as `architect/tracks.md` or files under `architect/tracks/<track_id>/`.
- Do not overwrite an existing file unless the user explicitly confirms that exact path and overwrite action.
- Use the active agent runtime's safest reviewable file-editing mechanism, preferably patch-based. Do not use shell redirection to write files.

If the user wants to convert the draft into a tracked Architect proposal, hand off to `architect-propose` after summarizing the confirmed scope and unresolved questions.

## Flow

Follow this progressive loop and gate sequence, adapting the depth to the request.

Do not skip directly to final synthesis unless the user explicitly asks for a synthesis with unresolved gates. If that happens, clearly label unresolved gates as assumptions, open questions, or deferred decisions.

### 1. Trigger Qualification

Use this skill only when the user explicitly includes the text `architect-discuss` or directly asks to use the `architect-discuss` skill.

After explicit invocation, this skill is appropriate when the user wants exploration, architecture discussion, product clarification, option comparison, or a draft before formal proposal work.

Do not use it for ordinary architecture discussion, brainstorming, feature exploration, or general product planning if the user does not explicitly name `architect-discuss`.

Do not use it when the user clearly wants implementation, review, status, setup, or already-confirmed tracked proposal creation.

### 2. Background Framing Loop

Build enough repository and domain context to frame the discussion intelligently.

When the request relates to an existing repository area, perform a shallow targeted context scan. Then present a short background summary, not a full draft.

The short background summary should include:

- Relevant domains, modules, services, packages, or apps.
- Relevant docs or code references.
- Known constraints and conventions.
- Initial architecture implications.

Ask only if the problem frame or discussion goal is unclear.

Gate objective: problem frame confirmed.

Gate passes when:

- The discussion target is clear.
- The user intent is clear enough, such as exploration, draft creation, or later proposal preparation.
- Required repository context is known or explicitly deferred.

### 3. Requirement Clarification Loop

Clarify the problem before proposing architecture.

Each loop should:

1. Summarize the current understanding.
2. Identify the missing or unstable information.
3. Ask one focused question or state one explicit assumption.
4. Update the understanding from the user's response.

Focus on:

- Problem statement.
- User or consumer groups.
- Business or product motivation.
- Desired behavior.
- Success criteria.
- Goals and non-goals.
- Affected domains or modules.
- Whether the request is one initiative or several independent initiatives.

Exit this loop when:

- The problem statement is stable.
- Primary users or consumers are known or explicitly assumed.
- Goals and non-goals are clear enough.
- Success criteria are known or explicitly assumed.
- No obvious scope explosion remains unresolved.

Gate objective: requirement scope confirmed.

At the gate, summarize confirmed requirement decisions, assumptions, and deferred questions. Ask whether to proceed to scope decomposition or revise the requirement framing.

### 4. Scope Decomposition Loop

Before deep architecture discussion, decide whether the request is too broad for one coherent draft or proposal.

If the request contains multiple separable initiatives, present a decomposition such as:

```md
## Scope Decomposition

This request appears to contain multiple separable initiatives:

1. <initiative-a>
2. <initiative-b>
3. <initiative-c>

Recommended first discussion target:
- <target>

Reason:
- <why this should be discussed first>
```

Ask whether the user wants a high-level platform draft or a focused draft for the recommended first target.

If the user intends to proceed to `architect-propose`, prefer a focused initiative that can become one tracked proposal.

Gate objective: draft scope confirmed.

Gate passes when:

- The draft target is a single initiative, a high-level platform draft, or an explicitly split set of proposal candidates.
- The recommended proposal scope is clear if later `architect-propose` work is likely.
- Any broader out-of-scope initiatives are recorded as deferred.

### 5. Product Design Loop

Clarify product behavior that can affect architecture.

Focus on:

- User roles and permissions.
- Primary user journeys.
- Functional requirements.
- Business rules.
- State transitions.
- Failure states.
- Operational or admin workflows.
- Configuration needs.
- Historical data or backward compatibility needs.
- MVP boundary and future scope.

Do not over-focus on low-level UI or implementation details unless they change architecture direction.

Exit this loop when:

- Core user journeys are clear.
- Required behaviors are known.
- Business rules are known or explicitly assumed.
- MVP scope and non-goals are clear.
- Remaining product details can be deferred without invalidating architecture.

Gate objective: product behavior confirmed.

At the gate, summarize user journeys, required behaviors, failure behavior, permissions, MVP boundary, and non-goals. Ask whether to proceed to constraints or revise product behavior.

### 6. Constraints And Non-Functional Requirements Loop

Clarify only constraints that can affect architecture.

Focus on:

- Latency and real-time expectations.
- Consistency expectations.
- Reliability and recovery expectations.
- Security, privacy, compliance, and auditability.
- Observability and operational needs.
- Scalability and cost constraints.
- Deployment or rollout constraints.

Ask one constraint question at a time when the answer can change the architecture direction. If the likely constraint is obvious and low-risk, state it as an assumption instead of asking.

Exit this loop when:

- Latency and consistency requirements are known or explicitly assumed.
- Security, privacy, compliance, or audit needs are known or explicitly assumed.
- Reliability and observability expectations are known or explicitly assumed.
- Remaining constraints can be deferred without invalidating architecture.

Gate objective: architecture constraints confirmed.

At the gate, summarize confirmed constraints, assumptions, and deferred constraint questions. Ask whether to proceed to architecture options or revise constraints.

### 7. Architecture Options Selection Loop

When the solution space is meaningfully open, present 2 to 3 architecture options.

Present compact options first. Do not present the full comprehensive draft during option exploration. Deepen only selected or contested options.

Compact option format:

```md
## Architecture Direction Options

Option A: <name>
- Best for: <short condition>
- Tradeoff: <main tradeoff>

Option B: <name>
- Best for: <short condition>
- Tradeoff: <main tradeoff>

Option C: <name, if relevant>
- Best for: <short condition>
- Tradeoff: <main tradeoff>

Recommended starting point:
- <option and short rationale>
```

Ask the user which direction to use as the basis for the draft, whether to compare options further, or whether to keep multiple options open.

When the user asks to explore an option more deeply, use this format for that option only:

```md
### Option <A/B/C>: <name>

Description:
- <what this architecture does>

Product impact:
- <how it affects behavior, UX, scope, or capability>

Technical impact:
- <modules, services, data, APIs, or operations affected>

Pros:
- <benefits>

Cons:
- <costs or limitations>

Risks:
- <failure modes or unknowns>

Best when:
- <conditions where this option is appropriate>
```

Then recommend one option when enough context exists. Explain the rationale and accepted tradeoffs.

Exit this loop when:

- At least one recommended architecture direction exists.
- Major alternatives have been considered.
- The recommendation has clear rationale.
- No unresolved unknown would invalidate the recommendation.

Gate objective: architecture direction confirmed.

Gate passes when:

- One architecture direction is confirmed, or the user explicitly asks the final synthesis to keep multiple options open.
- Rejected options have concise rationale.
- Major architecture impacts are recorded.

### 8. Tradeoff Decision Loop

Clarify tradeoffs that can change the recommended architecture.

Direction-changing tradeoffs include:

- System boundaries.
- Data ownership.
- Consistency model.
- User-visible behavior.
- API exposure and consumer contracts.
- Permissions, security, privacy, compliance, or auditability.
- Migration and rollout strategy.
- Operational complexity and observability.
- Performance, cost, and scalability constraints.
- Delivery sequencing.

Defer implementation-detail tradeoffs unless the user asks or they affect architecture. Examples of usually-deferred details include exact field names, function boundaries, component props, test file layout, non-critical UI micro-interactions, and local helper design.

Handle one major tradeoff at a time. Present short context, state the recommendation, then ask whether to confirm, revise, or defer the decision.

Record each major tradeoff in this shape:

```md
### <Tradeoff Name>

Decision pressure:
- <why this matters>

Options:
- <option-a>
- <option-b>

Recommendation:
- <recommended choice>

Rationale:
- <why this is preferred>

Decision status:
- Confirmed / Assumed / Needs decision / Deferred
```

Exit this loop when direction-changing tradeoffs are confirmed, explicitly assumed, or listed as open questions.

Gate objective: key tradeoffs confirmed or explicitly deferred.

Gate passes when:

- Direction-changing tradeoffs are confirmed, assumed, or deferred.
- Deferred tradeoffs are not likely to invalidate the final synthesis.
- Implementation-detail tradeoffs have not been over-discussed.

### 9. Readiness Check Loop

Before final synthesis, present a compact readiness summary.

Use this shape:

```md
## Readiness Check

Confirmed:
- <confirmed decision>

Assumptions:
- <assumption>

Deferred:
- <deferred question>

Final synthesis scope:
- <scope>
```

Ask whether to generate the final synthesis, revise a previous loop, or continue tradeoff discussion.

Gate objective: ready for final synthesis.

Gate passes when:

- The user confirms final synthesis should be generated.
- All prior loop gates are passed or explicitly deferred.
- Final synthesis scope is clear.

### 10. Final Synthesis Generation

Generate a comprehensive product and architecture draft only after the readiness gate passes, or after the user explicitly asks for a synthesis with unresolved gates.

Write the final synthesis in the same language as the user's prompt by default. If the user uses mixed languages, prefer the language used for the main requirement or ask briefly when unclear. Preserve established project terminology and code identifiers in their original language.

In the final synthesis, `Architecture Options Considered` should summarize options already discussed or explicitly assumed. It should not be the first time the user sees all option details.

Use this template unless the user asks for a different shape:

```md
# <Initiative Name> Product & Technical Architecture Draft

## 1. Executive Summary
- What this is
- Why it matters
- Recommended direction

## 2. Problem Statement
- Current problem
- User/business impact
- Existing limitations

## 3. Goals
- Product goals
- Technical goals
- Operational goals

## 4. Non-Goals
- Explicitly out of scope
- Deferred capabilities

## 5. Users And Use Cases
- Primary users
- Secondary users
- Main user journeys
- Edge cases

## 6. Functional Requirements
- Required behaviors
- Business rules
- Permissions and roles
- Failure states

## 7. Non-Functional Requirements
- Performance
- Reliability
- Security
- Privacy/compliance
- Observability
- Scalability
- Cost constraints

## 8. Current System Context
- Relevant modules/services
- Existing APIs/data models
- Relevant docs/code references
- Current constraints

## 9. Proposed Architecture
- High-level architecture
- Component responsibilities
- Data flow
- API boundaries
- Storage/schema implications
- Integration points

## 10. Architecture Options Considered
- Option A
- Option B
- Option C, if relevant
- Tradeoffs

## 11. Recommended Approach
- Recommendation
- Rationale
- Accepted tradeoffs
- Rejected alternatives

## 12. Product/Architecture Tradeoffs
- Direction-changing tradeoffs
- Decision status
- Deferred details

## 13. Implementation Shape
- Major workstreams
- Suggested sequencing
- Migration strategy
- Rollout strategy
- Backward compatibility needs

## 14. Risks And Mitigations
- Product risks
- Technical risks
- Operational risks
- Mitigations

## 15. Assumptions
- Product assumptions
- Technical assumptions
- Operational assumptions

## 16. Open Questions
- Questions requiring product decision
- Questions requiring technical decision
- Questions safe to defer

## 17. Readiness For Proposal
- Ready / Not ready
- What must be resolved before architect-propose
- Suggested proposal scope
```

Scale the draft to the request. A simple initiative can have compact sections. A broad platform initiative should be detailed enough to support review and decomposition.

### 11. Final Synthesis Self-Review

Before presenting the final synthesis, check it with fresh eyes.

Review for:

- Unresolved `TBD` or `TODO` placeholders.
- Assumptions presented as facts.
- Contradictions between product goals and architecture.
- Missing major tradeoffs.
- Over-specified implementation details.
- Unclear proposal readiness.
- Inaccurate repository references.
- Scope that is too broad for a single tracked proposal.

Fix issues inline before presenting the final synthesis.

### 12. Final Synthesis Review Loop

After presenting the final synthesis, ask whether the user wants to revise it, return to a specific earlier loop, save it as standalone documentation, split the work, or convert it into a tracked proposal.

When the user requests revisions:

1. Identify the sections affected.
2. Identify which loop should be reopened, if any.
3. Update the final synthesis or return to the relevant loop.
4. Re-mark assumptions, open questions, and proposal readiness.
5. Ask for the next decision only if needed.

### 13. Handoff Decision

End with clear next paths:

```md
## Next Step

This synthesis is suitable for one of these paths:

1. Continue discussion
   Use this if product scope or architecture direction still feels unsettled.

2. Convert to tracked Architect proposal
   Use `architect-propose` to create finalized `spec.md`, `plan.md`, `metadata.json`, `index.md`, and register the work in `architect/tracks.md`.

3. Save as standalone architecture draft
   Use this if the team wants a discussion artifact but is not ready to create a tracked proposal.

4. Split into multiple proposals
   Use this if the synthesis contains several independent initiatives.
```

Do not automatically choose one of these paths for the user.

## Final Synthesis Quality Bar

A good `architect-discuss` final synthesis should:

- Make the product problem and user value clear.
- Describe the current system context when available.
- Separate confirmed decisions, assumptions, recommendations, and open questions.
- Compare meaningful architecture options when alternatives exist.
- Explain why the recommended approach is appropriate.
- Identify risks and mitigations.
- Avoid pretending that unresolved details are finalized.
- Avoid implementation-level over-specification.
- Make clear whether the topic is ready for `architect-propose`.

## Relationship To Other Architect Skills

- `architect-setup` initializes or normalizes repository workflow structure.
- `architect-discuss` explores requirements and drafts product/architecture direction before tracked proposal work.
- `architect-propose` turns a confirmed requirement into finalized `spec.md`, `plan.md`, `metadata.json`, `index.md`, and `architect/tracks.md` registration.
- `architect-implement` implements an existing track from finalized proposal artifacts.
- `architect-review` reviews implemented work against the Architect workflow.
- `architect-status` summarizes tracked Architect work.

`architect-discuss` should improve the quality of later `architect-propose` work, not replace it.
