---
name: architect-discuss
description: Use only when the user explicitly includes `architect-discuss` or directly asks to use the architect-discuss skill. Turns raw or ambiguous product and technical requirements into a product and architecture draft before tracked Architect proposal work.
---

# Architect Discuss

Use this skill to clarify early product or technical requirements and draft product/architecture direction before creating a tracked Architect proposal.

## Core Rules

- Follow the bundled resource `references/discuss-protocol.md` as the source of truth.
- Use Architect semantics consistently: `architect/`, `/architect-*`, `Architect methodology`, and `architect(...)` commit scopes.
- Use this skill only after explicit invocation. Do not use it for ordinary architecture discussion unless the user names `architect-discuss`.
- Inspect relevant project context when the topic touches existing product behavior, modules, APIs, data, or operations.
- Do not create or update tracked Architect artifacts during discussion: no `architect/tracks.md` edits and no `architect/tracks/<track_id>/` artifacts.
- If saving a standalone draft, recommend `architect/drafts/<initiative-name>.md` and use only a user-confirmed relative project path. Do not use absolute paths, `..`, tracked Architect artifact paths, or shell redirection, and do not overwrite existing files without explicit confirmation.
- Do not modify implementation code, scaffold modules, or run implementation validation as if work has been built.
- Ask the user through the active agent runtime's user-interaction mechanism. If structured choices are unavailable, present the options in text and wait for the user's reply.
- Do not commit unless the user explicitly asks for a commit in the current conversation.

## Execution

1. Read the bundled resource `references/discuss-protocol.md`.
2. Qualify the explicit `architect-discuss` trigger.
3. Build shallow project context from `architect/` docs and relevant code when needed.
4. Run progressive clarification loops with gates.
5. Generate the final product and architecture draft only after the readiness gate passes, or when the user explicitly asks for synthesis with unresolved gates.
6. Offer next paths: continue discussion, save standalone draft, split scope, or hand off to `architect-propose`.
