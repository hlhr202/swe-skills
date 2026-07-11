import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(relative_path: str) -> str:
    return (ROOT / relative_path).read_text(encoding="utf-8")


PROTOCOLS = {
    "setup": "skills/architect-setup/references/setup-protocol.md",
    "discuss": "skills/architect-discuss/references/discuss-protocol.md",
    "propose": "skills/architect-propose/references/propose-track-protocol.md",
    "implement": "skills/architect-implement/references/implement-track-protocol.md",
    "review": "skills/architect-review/references/review-protocol.md",
    "status": "skills/architect-status/references/status-protocol.md",
}


class ArchitectProtocolShapeTests(unittest.TestCase):
    def test_every_protocol_names_the_behavior_layers(self) -> None:
        required_sections = (
            "## Purpose",
            "## Success Criteria",
            "## Hard Boundaries",
            "## State Model",
            "## Decision Rules",
            "## Approval Boundaries",
            "## Workflow",
            "## Stop Conditions",
        )

        for name, path in PROTOCOLS.items():
            content = read(path)
            for section in required_sections:
                with self.subTest(protocol=name, section=section):
                    self.assertIn(section, content)

    def test_every_skill_keeps_its_protocol_as_source_of_truth(self) -> None:
        for name in PROTOCOLS:
            skill = read(f"skills/architect-{name}/SKILL.md")
            with self.subTest(skill=name):
                self.assertIn("source of truth", skill)


class ArchitectBoundaryTests(unittest.TestCase):
    def test_setup_creates_core_context_only(self) -> None:
        content = read(PROTOCOLS["setup"])
        self.assertIn("core context", content)
        self.assertIn("must not create, repair, delete, or modify track artifacts", content)
        self.assertIn("earliest missing", content)
        self.assertIn("explicitly requests a commit", content)

    def test_discuss_requires_explicit_invocation_and_stays_pre_proposal(self) -> None:
        content = read(PROTOCOLS["discuss"])
        self.assertIn("explicitly invokes `architect-discuss`", content)
        self.assertIn("must not create or update tracked Architect artifacts", content)
        self.assertIn("must not modify implementation code", content)
        self.assertIn("user-confirmed", content)
        self.assertIn("architect/drafts/", content)

    def test_propose_requires_both_approvals_before_writing(self) -> None:
        content = read(PROTOCOLS["propose"])
        spec = content.index("spec_approved")
        plan = content.index("plan_approved")
        created = content.index("track_created")
        self.assertLess(spec, plan)
        self.assertLess(plan, created)
        self.assertIn('"status": "new"', content)
        self.assertIn("collision", content.lower())
        self.assertIn("explicitly requests a commit", content)

    def test_status_is_strictly_read_only(self) -> None:
        content = read(PROTOCOLS["status"])
        self.assertIn("strictly read-only", content)
        for action in ("create", "edit", "move", "delete", "archive", "commit"):
            with self.subTest(action=action):
                self.assertIn(action, content)


class ArchitectStateMachineTests(unittest.TestCase):
    def test_implement_preserves_track_task_and_phase_state(self) -> None:
        content = read(PROTOCOLS["implement"])
        for transition in (
            "new -> in_progress -> completed",
            "[ ] -> [~] -> [x]",
            "Manual Mode",
            "Auto Mode",
            "phase protocol meta-task",
        ):
            with self.subTest(transition=transition):
                self.assertIn(transition, content)

    def test_review_preserves_confidence_routing(self) -> None:
        content = read(PROTOCOLS["review"])
        self.assertIn("adopt it without confirmation", content)
        self.assertIn("ask once", content)
        self.assertIn("Do not ask a second", content)
        self.assertIn("findings first", content.lower())

    def test_status_preserves_precedence_and_counting(self) -> None:
        content = read(PROTOCOLS["status"])
        for state in (
            "Needs Attention",
            "Blocked",
            "Complete",
            "In Progress",
            "Not Started",
        ):
            with self.subTest(state=state):
                self.assertIn(state, content)
        self.assertIn("count only those sub-tasks", content)
        self.assertIn("completed / total * 100", content)


class ArchitectApprovalTests(unittest.TestCase):
    def test_implement_commit_authority_is_narrow(self) -> None:
        content = read(PROTOCOLS["implement"])
        self.assertIn("one final, track-scoped implementation commit", content)
        self.assertIn("Auto Mode additionally authorizes phase checkpoint commits", content)
        self.assertIn("Manual Mode checkpoint commits", content)
        self.assertIn("Never use broad staging", content)
        self.assertIn("git add .", content)
        self.assertIn("git add -A", content)

    def test_review_does_not_infer_commit_authority(self) -> None:
        content = read(PROTOCOLS["review"])
        for phrase in (
            "Asking to review",
            "Asking to apply fixes",
            "Asking to complete the track",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, content)
        self.assertIn("do not count as commit authorization", content)

    def test_cleanup_always_requires_exact_confirmation(self) -> None:
        for name in ("implement", "review"):
            content = read(PROTOCOLS[name])
            with self.subTest(protocol=name):
                self.assertIn("explicit confirmation", content)
                self.assertIn("Confirm Archive", content)
                self.assertIn("permanently delete", content)


class ArchitectDocumentationSyncTests(unittest.TestCase):
    def test_propose_flow_defers_management_writes_until_plan_approval(self) -> None:
        flow = read("misc/architect/flow-charts/architect-propose-flow.md")
        self.assertLess(flow.index("ConfirmPlan -->|Approve| RecoverMgmt"), flow.index("RecoverMgmt --> TrackID"))
        self.assertNotIn("PlanQuestions", flow)

    def test_implement_flow_preserves_track_confirmation_and_reopen_gate(self) -> None:
        flow = read("misc/architect/flow-charts/architect-implement-flow.md")
        self.assertIn("ConfirmTrack{User confirms matched track?}", flow)
        self.assertIn("ReopenConfirm{User explicitly confirms reopening?}", flow)

    def test_setup_flow_generates_missing_index_after_workflow(self) -> None:
        flow = read("misc/architect/flow-charts/architect-setup-flow.md")
        self.assertIn("IndexReady{Index complete?}", flow)
        self.assertIn("IndexReady -->|No| WriteIndex", flow)

    def test_prompt_contracts_keep_side_effecting_decisions_explicit(self) -> None:
        implement = read(PROTOCOLS["implement"])
        review = read(PROTOCOLS["review"])
        for prompt in (
            "I found track '<track_description>'. Is this correct?",
            "Approve these Product Guidelines changes?",
            "Track '<track_id>' is complete. What would you like to do?",
        ):
            with self.subTest(protocol="implement", prompt=prompt):
                self.assertIn(prompt, implement)
        for prompt in (
            "What would you like to review?",
            "How would you like to proceed with the review findings?",
            "Review fixes changed files. Should I commit them?",
        ):
            with self.subTest(protocol="review", prompt=prompt):
                self.assertIn(prompt, review)


if __name__ == "__main__":
    unittest.main()
