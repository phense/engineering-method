"""Compaction-boundary recovery tests for the orchestrated executor."""

from __future__ import annotations

import json
import re
import subprocess
import tempfile
import unittest
from pathlib import Path

from engineering_method import continuity
from engineering_method.backlog import BacklogDocument, render_backlog
from engineering_method.models import BacklogItem, Priority, TaskStatus


ROOT = Path(__file__).resolve().parents[1]
WORK_ID = "EM-004"
ARTIFACTS = (
    "specs/F-004/spec.md",
    "specs/F-004/plan.md",
    "specs/F-004/tasks.md",
    "docs/uml/component.mmd",
    "reports/slice.md",
    "artifacts/integration.txt",
)


def fenced_json(relative: str) -> dict[str, object]:
    content = (ROOT / relative).read_text(encoding="utf-8")
    match = re.search(r"```json\n(.*?)\n```", content, flags=re.DOTALL)
    if match is None:
        raise AssertionError(f"{relative} must contain a fenced JSON contract")
    payload = json.loads(match.group(1))
    if not isinstance(payload, dict):
        raise AssertionError(f"{relative} contract must be an object")
    return payload


class RecoveryFixture:
    def __init__(self, root: Path) -> None:
        self.root = root
        subprocess.run(("git", "init", "-q"), cwd=root, check=True)
        subprocess.run(("git", "config", "user.email", "test@example.com"), cwd=root, check=True)
        subprocess.run(("git", "config", "user.name", "Test User"), cwd=root, check=True)
        for relative in ARTIFACTS:
            path = root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(f"evidence for {relative}\n", encoding="utf-8")
        backlog = BacklogItem(
            WORK_ID,
            "Orchestration and architecture",
            TaskStatus.IN_PROGRESS,
            Priority.P1,
            None,
            (),
            "",
            "2026-09-04T12:00:00Z",
        )
        (root / "BACKLOG.md").write_text(
            render_backlog(BacklogDocument("EM", "local", (backlog,))),
            encoding="utf-8",
        )
        subprocess.run(("git", "add", "."), cwd=root, check=True)
        subprocess.run(("git", "commit", "-q", "-m", "base evidence"), cwd=root, check=True)
        self.base = self.head()
        marker = root / "artifacts/integration.txt"
        marker.write_text("current integration evidence\n", encoding="utf-8")
        subprocess.run(("git", "commit", "-qam", "current evidence"), cwd=root, check=True)
        self.current_head = self.head()

    def head(self) -> str:
        return subprocess.run(
            ("git", "rev-parse", "HEAD"),
            cwd=self.root,
            check=True,
            text=True,
            capture_output=True,
        ).stdout.strip()

    def state(self, **changes: object) -> continuity.RunState:
        values: dict[str, object] = {
            "work_id": WORK_ID,
            "backlog_id": WORK_ID,
            "feature_id": "F-004",
            "lifecycle": "orchestrated-implementation",
            "phase": "implementation",
            "current_slice": "S1",
            "spec_path": ARTIFACTS[0],
            "plan_path": ARTIFACTS[1],
            "tasks_path": ARTIFACTS[2],
            "uml_paths": (ARTIFACTS[3],),
            "report_paths": (ARTIFACTS[4],),
            "artifact_paths": (ARTIFACTS[5],),
            "worktree_path": str(self.root),
            "base_commit": self.base,
            "last_observed_head": self.base,
            "completed_work": (),
            "active_work": (),
            "pending_work": (),
            "active_agent_ids": (),
            "completed_agent_ids": (),
            "open_findings": (),
            "failing_checks": (),
            "next_action": "Continue implementation",
        }
        values.update(changes)
        return continuity.RunState(**values)

    def recover(
        self, saved: continuity.RunState, *, live_agent_ids: tuple[str, ...] = ()
    ) -> continuity.RecoveryResult:
        continuity.create_run(
            self.root,
            saved,
            f"Resume {saved.phase} at: {saved.next_action}\n",
        )
        return continuity.recover_run(
            self.root,
            WORK_ID,
            git_probe=continuity.SubprocessGitProbe(),
            canonical_probe=continuity.BacklogCanonicalProbe(),
            live_agent_ids=live_agent_ids,
        )


class CompactionBoundaryTests(unittest.TestCase):
    def test_recovery_resumes_exactly_after_all_eight_checkpoint_boundaries(self) -> None:
        """Compaction at a meaningful boundary must neither rewind nor skip its next action."""
        boundaries = (
            {
                "id": "before_dispatch",
                "phase": "dispatch",
                "next_action": "Dispatch the prepared S1 brief",
            },
            {
                "id": "active_agent",
                "phase": "implementation",
                "next_action": "Wait for the current agent report",
                "active_work": ("implementation:S1",),
                "active_agent_ids": ("agent-live",),
                "live": ("agent-live",),
            },
            {
                "id": "completed_agent_before_integration",
                "phase": "integration",
                "next_action": "Integrate the verified report range",
                "completed_work": ("implementation:S1",),
                "completed_agent_ids": ("agent-done",),
            },
            {
                "id": "failed_verification",
                "phase": "verification",
                "next_action": "Diagnose the recorded failing check",
                "failing_checks": ("python3 -m unittest focused",),
            },
            {
                "id": "mid_fix",
                "phase": "fix",
                "next_action": "Run the covering test for AF-002",
                "open_findings": ("AF-002 compensation ordering",),
                "active_work": ("fix:AF-002",),
            },
            {
                "id": "post_slice",
                "phase": "implementation",
                "current_slice": "S2",
                "next_action": "Start the pending S2 slice",
                "completed_work": ("implementation:S1",),
                "pending_work": ("implementation:S2",),
            },
            {
                "id": "pre_converge",
                "phase": "as-built-reconciliation",
                "current_slice": None,
                "next_action": "Run Spec Kit convergence",
                "completed_work": ("implementation:S1", "implementation:S2"),
            },
            {
                "id": "final_handoff",
                "phase": "final-handoff",
                "current_slice": None,
                "next_action": "Hand off the verified EM-004 evidence",
                "completed_work": ("implementation:S1", "implementation:S2", "integration"),
            },
        )
        for boundary in boundaries:
            with self.subTest(boundary=boundary["id"]), tempfile.TemporaryDirectory() as temporary:
                fixture = RecoveryFixture(Path(temporary))
                changes = {key: value for key, value in boundary.items() if key not in {"id", "live"}}
                saved = fixture.state(**changes)
                recovered = fixture.recover(saved, live_agent_ids=boundary.get("live", ()))
                self.assertEqual(boundary["next_action"], recovered.next_action)
                self.assertEqual(fixture.current_head, recovered.state.last_observed_head)
                self.assertEqual(TaskStatus.IN_PROGRESS, recovered.canonical_status)
                self.assertEqual(saved.completed_work, recovered.completed_work)
                self.assertEqual((), recovered.redispatchable_agent_ids)

    def test_unavailable_agent_is_redispatchable_without_repeating_completed_slice(self) -> None:
        """Agent eviction may reopen active work but never completed work."""
        with tempfile.TemporaryDirectory() as temporary:
            fixture = RecoveryFixture(Path(temporary))
            saved = fixture.state(
                current_slice="S2",
                completed_work=("implementation:S1",),
                active_work=("implementation:S2",),
                active_agent_ids=("agent-live", "agent-gone"),
                pending_work=("integration",),
                next_action="Wait for active S2 agents",
            )
            recovered = fixture.recover(saved, live_agent_ids=("agent-live",))

            self.assertEqual(("agent-gone",), recovered.redispatchable_agent_ids)
            self.assertEqual(("agent-live",), recovered.state.active_agent_ids)
            self.assertEqual(("implementation:S1",), recovered.completed_work)
            self.assertNotIn("S1", recovered.next_action)
            self.assertEqual("Redispatch unavailable agents: agent-gone", recovered.next_action)

    def test_missing_artifact_fails_recovery_before_a_resume_decision(self) -> None:
        """A checkpoint pointer cannot be trusted after its repository artifact disappears."""
        with tempfile.TemporaryDirectory() as temporary:
            fixture = RecoveryFixture(Path(temporary))
            saved = fixture.state(next_action="Dispatch S1")
            continuity.create_run(fixture.root, saved, "Resume dispatch.\n")
            (fixture.root / ARTIFACTS[2]).unlink()
            with self.assertRaisesRegex(ValueError, "artifact does not exist"):
                continuity.recover_run(
                    fixture.root,
                    WORK_ID,
                    git_probe=continuity.SubprocessGitProbe(),
                    canonical_probe=continuity.BacklogCanonicalProbe(),
                    live_agent_ids=(),
                )


class RecallBoundaryTests(unittest.TestCase):
    def test_recalled_state_supplies_only_identity_and_pointers_not_authority(self) -> None:
        """Stale recalled completion and next-action values must lose to repository evidence."""
        contract = fenced_json("shared/policies/continuity-contract.md")
        self.assertEqual(
            {"work_id", "artifact_pointers"}, set(contract["downstream_recall_allowed"])
        )
        self.assertEqual("repository_evidence", contract["authority_on_conflict"])

        with tempfile.TemporaryDirectory() as temporary:
            fixture = RecoveryFixture(Path(temporary))
            saved = fixture.state(
                current_slice="S2",
                completed_work=("implementation:S1",),
                pending_work=("implementation:S2",),
                next_action="Start the pending S2 slice",
            )
            continuity.create_run(fixture.root, saved, "Resume S2 from repository state.\n")
            recalled = {
                "work_id": WORK_ID,
                "artifact_pointers": [".engineering-method/runs/EM-004/state.json"],
                "canonical_status": "complete",
                "last_observed_head": "0" * 40,
                "completed_work": [],
                "next_action": "Redispatch implementation:S1",
            }
            allowed = {
                key: recalled[key]
                for key in contract["downstream_recall_allowed"]
                if key in recalled
            }
            self.assertEqual({"work_id", "artifact_pointers"}, set(allowed))

            recovered = continuity.recover_run(
                fixture.root,
                allowed["work_id"],
                git_probe=continuity.SubprocessGitProbe(),
                canonical_probe=continuity.BacklogCanonicalProbe(),
                live_agent_ids=(),
            )

            self.assertEqual(TaskStatus.IN_PROGRESS, recovered.canonical_status)
            self.assertEqual(fixture.current_head, recovered.state.last_observed_head)
            self.assertEqual(("implementation:S1",), recovered.completed_work)
            self.assertEqual("Start the pending S2 slice", recovered.next_action)

    def test_contract_names_all_modeled_compaction_boundaries(self) -> None:
        """An unnamed checkpoint boundary is an untested restart path."""
        policy = fenced_json("shared/policies/continuity-contract.md")
        skill = fenced_json("skills/orchestrated-implementation/SKILL.md")
        expected = {
            "before_dispatch",
            "active_agent",
            "completed_agent_before_integration",
            "failed_verification",
            "mid_fix",
            "post_slice",
            "pre_converge",
            "final_handoff",
        }
        self.assertEqual(expected, set(policy["compaction_boundaries"]))
        self.assertEqual(expected, set(skill["compaction_boundaries"]))


if __name__ == "__main__":
    unittest.main()
