"""Tests for compact-safe state and provider-neutral events."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from engineering_method.continuity import RunState, append_event, checkpoint, create_run, recover_run


def state() -> RunState:
    return RunState(work_id="EM-002", lifecycle="implementation", phase="task-6", next_action="run focused tests", completed_slices=("task-1",), active_agent_ids=("agent-a",), artifact_paths=("docs/plan.md",))


class ContinuityTests(unittest.TestCase):
    def test_creates_the_exact_run_tree_and_atomic_checkpoint(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            run = create_run(root, state(), "Resume here.", "Keep IDs stable.")
            self.assertEqual({path.name for path in run.iterdir()}, {"state.json", "resume.md", "decisions.md", "agent-reports", "events.jsonl"})
            checkpoint(root, "EM-002", state(), "New resume.")
            self.assertEqual(json.loads((run / "state.json").read_text())["schema_version"], 1)

    def test_accepts_all_allowed_events_and_rejects_sensitive_or_unsafe_events_before_write(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            create_run(root, state(), "Resume.")
            for kind in ("workflow_started", "phase_changed", "slice_started", "decision_recorded", "agent_dispatched", "agent_completed", "verification_failed", "verification_passed", "workflow_completed"):
                self.assertEqual(append_event(root, "EM-002", {"kind": kind, "artifact": "docs/plan.md"})["kind"], kind)
            events = root / ".engineering-method" / "runs" / "EM-002" / "events.jsonl"
            before = events.read_text()
            for event in ({"kind": "unknown"}, {"kind": "phase_changed", "artifact": "/tmp/x"}, {"kind": "phase_changed", "Token": "x"}):
                with self.subTest(event=event), self.assertRaises(ValueError):
                    append_event(root, "EM-002", event)
            self.assertEqual(events.read_text(), before)

    def test_recovery_preserves_completed_slices_and_redispatches_unavailable_agents(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            create_run(root, state(), "Resume.")
            result = recover_run(root, "EM-002", git_probe=lambda: "head", canonical_probe=lambda _: False, live_agent_ids=())
            self.assertEqual(result.completed_slices, ("task-1",))
            self.assertEqual(result.redispatchable_agent_ids, ("agent-a",))


if __name__ == "__main__":
    unittest.main()
