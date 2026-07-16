import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(relative_path: str) -> str:
    return (ROOT / relative_path).read_text(encoding="utf-8")


class ArchitectImplementContractTests(unittest.TestCase):
    def test_auto_mode_does_not_stop_for_task_size_or_unfinished_phases(self) -> None:
        paths = (
            "skills/architect-implement/SKILL.md",
            "skills/architect-implement/references/implement-track-protocol.md",
        )

        for path in paths:
            with self.subTest(path=path):
                content = read(path)
                self.assertIn("continue until finalization", content)
                self.assertIn("task size and unfinished phases", content)

    def test_final_commit_is_required_in_skill_protocol_and_project_template(self) -> None:
        paths = (
            "skills/architect-implement/SKILL.md",
            "skills/architect-implement/references/implement-track-protocol.md",
            "skills/architect-setup/references/workflow.md",
        )

        for path in paths:
            with self.subTest(path=path):
                content = read(path).lower()
                self.assertIn("final", content)
                self.assertIn("track-scoped", content)
                self.assertIn("commit", content)
                self.assertIn("opts out", content)

    def test_final_commit_runs_after_documentation_sync_and_before_cleanup(self) -> None:
        protocol = read(
            "skills/architect-implement/references/implement-track-protocol.md"
        )

        self.assertLess(
            protocol.index("## 10. Synchronize Project Documentation"),
            protocol.index("## 11. Final Implementation Commit"),
        )
        self.assertLess(
            protocol.index("## 11. Final Implementation Commit"),
            protocol.index("## 12. Track Cleanup"),
        )

    def test_final_commit_safety_excludes_broad_staging(self) -> None:
        protocol = read(
            "skills/architect-implement/references/implement-track-protocol.md"
        )

        self.assertIn("Never use broad staging", protocol)
        self.assertIn("git add .", protocol)
        self.assertIn("git add -A", protocol)
        self.assertIn("git diff --cached --check", protocol)
        self.assertIn("finalization blocker", protocol)

    def test_implement_flow_reaches_final_commit_after_docs(self) -> None:
        flow = read("misc/architect/flow-charts/architect-implement-flow.md")

        self.assertIn("DocsReport --> FinalOptOut", flow)
        self.assertIn("SafeFinal -->|Yes| CommitFinal", flow)
        self.assertNotIn("CompletionCommit", flow)
        self.assertNotIn("DocsCommit", flow)


class ArchitectReviewContractTests(unittest.TestCase):
    def test_high_confidence_scope_and_range_do_not_require_confirmation(self) -> None:
        protocol = read("skills/architect-review/references/review-protocol.md")

        self.assertIn("high confidence", protocol)
        self.assertIn("adopt it without confirmation", protocol)
        self.assertIn("Do not ask a second final-scope question", protocol)
        self.assertNotIn("Confirm Inferred Range", protocol)
        self.assertNotIn("Before continuing, confirm the final scope", protocol)

    def test_range_confidence_requires_coherent_git_evidence(self) -> None:
        protocol = read("skills/architect-review/references/review-protocol.md")

        for evidence in (
            "resolves to a commit",
            "ancestor of the last relevant commit",
            "one coherent implementation sequence",
            "no unexplained commit",
            "aggregate diff footprint",
        ):
            with self.subTest(evidence=evidence):
                self.assertIn(evidence, protocol)

    def test_large_diff_uses_iterative_review_without_confirmation(self) -> None:
        protocol = read("skills/architect-review/references/review-protocol.md")
        flow = read("misc/architect/flow-charts/architect-review-flow.md")

        self.assertIn("proceed automatically", protocol)
        self.assertNotIn("Title: `Large Review`", protocol)
        self.assertNotIn("ConfirmInferredRange", flow)
        self.assertNotIn("ConfirmScope", flow)
        self.assertNotIn("Diff --> Volume", flow)


if __name__ == "__main__":
    unittest.main()
