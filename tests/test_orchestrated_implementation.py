"""Behavior and provenance contracts for cohesive-slice orchestration."""

from __future__ import annotations

import json
import re
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TASK_BRIEF = ROOT / "scripts/task-brief"
REVIEW_PACKAGE = ROOT / "scripts/review-package"


def read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def fenced_json(relative: str) -> dict[str, object]:
    match = re.search(r"```json\n(.*?)\n```", read(relative), flags=re.DOTALL)
    if match is None:
        raise AssertionError(f"{relative} must contain a fenced JSON contract")
    payload = json.loads(match.group(1))
    if not isinstance(payload, dict):
        raise AssertionError(f"{relative} contract must be an object")
    return payload


def normalized(relative: str) -> str:
    return " ".join(read(relative).lower().split())


class OrchestratedImplementationSkillTests(unittest.TestCase):
    def test_skill_has_exclusive_large_feature_inputs_and_handoff(self) -> None:
        """The executor must not absorb small edits or the OpenSpec apply lifecycle."""
        contract = fenced_json("skills/orchestrated-implementation/SKILL.md")
        self.assertEqual(
            {"spec_kit_tasks", "architecture_findings", "work_id", "project_gates"},
            set(contract["inputs"]),
        )
        self.assertEqual(".engineering-method/runs/<work-id>/", contract["run_root"])
        self.assertEqual("speckit-converge", contract["next_phase"])
        description = normalized("skills/orchestrated-implementation/SKILL.md")
        for phrase in ("spec kit", "tasks.md", "not for small", "openspec apply"):
            self.assertIn(phrase, description)

    def test_slice_and_review_rules_preserve_interfaces_and_proportionate_risk(self) -> None:
        """Shared interfaces cannot be parallelized and risky slices cannot self-review."""
        contract = fenced_json("skills/orchestrated-implementation/SKILL.md")
        rules = contract["slice_rules"]
        self.assertEqual("batch", rules["adjacent_tiny_same_shape"])
        self.assertEqual("serialize", rules["shared_interface"])
        self.assertEqual(
            ["disjoint_paths", "disjoint_interfaces", "safe_isolation", "integration_order"],
            rules["parallel_requires"],
        )
        review = contract["review"]
        self.assertEqual("coordinator_allowed", review["mechanical"])
        self.assertEqual(
            {"security", "migration", "interface", "concurrency", "cross_component"},
            set(review["independent_required"]),
        )

    def test_skill_brackets_every_recovery_boundary_with_em002_checkpoints(self) -> None:
        """A compacted coordinator needs durable state at every externally visible edge."""
        contract = fenced_json("skills/orchestrated-implementation/SKILL.md")
        self.assertEqual(
            {
                "before_dispatch",
                "after_dispatch",
                "after_implementation",
                "after_test",
                "after_review",
                "after_fix",
                "before_long_wait",
                "handoff",
            },
            set(contract["checkpoint_boundaries"]),
        )
        content = normalized("skills/orchestrated-implementation/SKILL.md")
        self.assertIn("existing em-002", content)
        self.assertIn("sole writer of state.json", content)
        self.assertIn("only their named report file", content)

    def test_defect_loop_escalates_after_two_ineffective_attempts(self) -> None:
        """Repeated local retries must change perspective before more code churn."""
        policy = fenced_json("shared/policies/defect-convergence.md")
        self.assertEqual(
            [
                "precise_finding_to_original_implementer",
                "root_cause_and_covering_test",
                "after_two_ineffective_attempts_use_fresh_or_stronger_agent",
                "repeated_local_failure_run_interface_or_architecture_analysis",
            ],
            policy["escalation_sequence"],
        )
        self.assertEqual(2, policy["fresh_perspective_after_ineffective_attempts"])
        self.assertTrue(policy["reject_identical_retry_brief"])
        skill = fenced_json("skills/orchestrated-implementation/SKILL.md")
        self.assertEqual("shared/policies/defect-convergence.md", skill["defect_convergence"])

    def test_every_retry_adds_evidence_and_terminal_conditions_are_exhaustive(self) -> None:
        """A retry without progress or an invented exit can silently discard a real defect."""
        policy = fenced_json("shared/policies/defect-convergence.md")
        self.assertEqual(
            {"new_evidence", "new_hypothesis", "changed_approach", "model_or_perspective_escalation"},
            set(policy["retry_progress_requires_one"]),
        )
        self.assertEqual(
            {
                "all_actionable_findings_resolved",
                "external_blocker",
                "missing_authorization",
                "unsafe_irreversible_operation",
                "specification_contradiction",
            },
            set(policy["terminal_conditions"]),
        )
        self.assertEqual("narrowest_meaningful_covering_tests", policy["after_each_fix"])
        self.assertEqual(
            ["integration_affecting_fix", "integration_boundary"],
            policy["broaden_tests_only_for"],
        )

    def test_agent_roles_carry_finding_and_fix_evidence_across_retries(self) -> None:
        """Escalation loses value if the next perspective cannot see prior evidence."""
        implementer = normalized("shared/agent-roles/implementer.md")
        debugger = normalized("shared/agent-roles/debugger.md")
        reviewer = normalized("shared/agent-roles/reviewer.md")
        for phrase in ("precise finding", "root-cause", "covering test", "prior attempts"):
            self.assertIn(phrase, implementer)
        for phrase in ("new evidence", "new hypothesis", "changed approach", "perspective escalation"):
            self.assertIn(phrase, debugger)
        for phrase in ("identical retry brief", "actionable", "resolution condition"):
            self.assertIn(phrase, reviewer)


class OrchestrationScriptTests(unittest.TestCase):
    def test_helpers_preserve_canonical_run_files(self) -> None:
        """Custom artifact outputs must not destroy continuity state or reports."""
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._repo(root)
            head = self._commit(root, "tasks.md", "### Slice S1: work\n- [ ] T001 work\n", "base")
            run = root / ".engineering-method/runs/EM-004"
            for relative in ("state.json", "resume.md", "decisions.md", "events.jsonl", "agent-reports/worker.md",
                             "STATE.JSON", "RESUME.MD", "DECISIONS.MD", "EVENTS.JSONL", "AGENT-REPORTS/worker.md"):
                target = run / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text("preserve this evidence\n", encoding="utf-8")
                for command in ((str(TASK_BRIEF), "tasks.md", "EM-004", "S1"),
                                (str(REVIEW_PACKAGE), "EM-004", head, head)):
                    with self.subTest(helper=command[0], target=relative):
                        result = subprocess.run((*command, str(target)), cwd=root, capture_output=True, text=True)
                        self.assertNotEqual(0, result.returncode)
                        self.assertEqual("preserve this evidence\n", target.read_text())

    def test_helpers_reject_run_symlinks_outside_repository(self) -> None:
        """A linked run must not redirect generated artifacts into another repository."""
        with tempfile.TemporaryDirectory() as temporary, tempfile.TemporaryDirectory() as outside:
            root = Path(temporary)
            self._repo(root)
            head = self._commit(root, "tasks.md", "### Slice S1: work\n- [ ] T001 work\n", "base")
            run = root / ".engineering-method/runs/EM-004"
            (run / "state.json").unlink()
            run.rmdir()
            run.symlink_to(outside, target_is_directory=True)
            (Path(outside) / "state.json").write_text("{}\n", encoding="utf-8")
            for command in ((str(TASK_BRIEF), "tasks.md", "EM-004", "S1"),
                            (str(REVIEW_PACKAGE), "EM-004", head, head)):
                with self.subTest(helper=command[0]):
                    result = subprocess.run(command, cwd=root, capture_output=True, text=True)
                    self.assertNotEqual(0, result.returncode)
                    self.assertEqual(["state.json"], sorted(path.name for path in Path(outside).iterdir()))

    def test_every_template_task_is_extractable_exactly_once(self) -> None:
        """Prerequisite and final tasks must not disappear at the slice boundary."""
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._repo(root)
            tasks = read("templates/spec-kit/tasks.md")
            (root / "tasks.md").write_text(tasks, encoding="utf-8")
            extracted = []
            slice_tasks = {}
            for slice_id in re.findall(r"^### Slice ([^: ]+):", tasks, flags=re.MULTILINE):
                result = subprocess.run((str(TASK_BRIEF), "tasks.md", "EM-004", slice_id),
                                        cwd=root, capture_output=True, text=True, check=True)
                slice_tasks[slice_id] = re.findall(r"^- \[ \] (T\d+)", Path(result.stdout.strip()).read_text(), flags=re.MULTILINE)
                extracted.extend(slice_tasks[slice_id])
            self.assertEqual(["T001", "T002", "T003", "T004", "T005", "T006", "T007"], extracted)
            self.assertEqual(["T001", "T002", "T003", "T004"], slice_tasks["S1"])

    def _repo(self, root: Path) -> None:
        subprocess.run(("git", "init", "-q"), cwd=root, check=True)
        subprocess.run(("git", "config", "user.email", "test@example.com"), cwd=root, check=True)
        subprocess.run(("git", "config", "user.name", "Test User"), cwd=root, check=True)
        run = root / ".engineering-method/runs/EM-004"
        run.mkdir(parents=True)
        (run / "state.json").write_text("{}\n", encoding="utf-8")

    def _commit(self, root: Path, relative: str, content: str, subject: str) -> str:
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        subprocess.run(("git", "add", relative), cwd=root, check=True)
        subprocess.run(("git", "commit", "-q", "-m", subject), cwd=root, check=True)
        return subprocess.run(
            ("git", "rev-parse", "HEAD"), cwd=root, check=True, text=True, capture_output=True
        ).stdout.strip()

    def test_task_brief_extracts_one_complete_slice_into_existing_run(self) -> None:
        """Selecting S1 must not leak adjacent S2 work into an implementer brief."""
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._repo(root)
            tasks = root / "docs/specs/F-001-checkout/tasks.md"
            tasks.parent.mkdir(parents=True)
            tasks.write_text(
                "# Tasks\n\n### Slice S1: inventory contract\n\n"
                "- [ ] T001 fix reserve\n- [ ] T002 test reserve\n\n"
                "### Slice S2: checkout recovery\n\n- [ ] T003 compensate\n\n"
                "## Dependencies\n\nT003 depends on T001.\n",
                encoding="utf-8",
            )
            result = subprocess.run(
                (str(TASK_BRIEF), str(tasks), "EM-004", "S1"),
                cwd=root,
                text=True,
                capture_output=True,
                check=True,
            )
            output = root / ".engineering-method/runs/EM-004/slice-S1-brief.md"
            self.assertEqual(output.resolve(), Path(result.stdout.strip()).resolve())
            brief = output.read_text(encoding="utf-8")
            self.assertIn("Work ID: EM-004", brief)
            self.assertIn("Slice ID: S1", brief)
            self.assertIn("T001 fix reserve", brief)
            self.assertIn("T002 test reserve", brief)
            self.assertNotIn("T003 compensate", brief)

            second = subprocess.run(
                (str(TASK_BRIEF), str(tasks), "EM-004", "S2"),
                cwd=root,
                text=True,
                capture_output=True,
                check=True,
            )
            second_brief = Path(second.stdout.strip()).read_text(encoding="utf-8")
            self.assertIn("T003 compensate", second_brief)
            self.assertNotIn("T003 depends on T001", second_brief)

    def test_review_package_contains_the_complete_requested_commit_range(self) -> None:
        """Using only the latest commit would hide earlier files in a multi-commit slice."""
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._repo(root)
            base = self._commit(root, "base.txt", "base\n", "base")
            self._commit(root, "first.txt", "first slice change\n", "first slice commit")
            head = self._commit(root, "second.txt", "second slice change\n", "second slice commit")
            result = subprocess.run(
                (str(REVIEW_PACKAGE), "EM-004", base, head),
                cwd=root,
                text=True,
                capture_output=True,
                check=True,
            )
            package = Path(result.stdout.strip()).resolve()
            self.assertEqual(
                (
                    root
                    / f".engineering-method/runs/EM-004/review-{base[:7]}..{head[:7]}.diff"
                ).resolve(),
                package,
            )
            content = package.read_text(encoding="utf-8")
            for evidence in (
                "first slice commit",
                "second slice commit",
                "first.txt",
                "second.txt",
                "first slice change",
                "second slice change",
            ):
                self.assertIn(evidence, content)


class OrchestrationProvenanceTests(unittest.TestCase):
    def test_all_pinned_superpowers_inputs_have_adapted_destination_mappings(self) -> None:
        """An adapted orchestration mechanism without its source mapping is unauditable."""
        lock = json.loads(read("third-party/sources.lock.json"))
        source = next(item for item in lock["sources"] if item["id"] == "superpowers")
        mappings = [
            mapping for mapping in source["files"] if mapping["modification_status"] == "adapted"
        ]
        expected_sources = {
            "skills/subagent-driven-development/SKILL.md",
            "skills/subagent-driven-development/implementer-prompt.md",
            "skills/subagent-driven-development/task-reviewer-prompt.md",
            "skills/subagent-driven-development/re-review-prompt.md",
            "skills/subagent-driven-development/scripts/task-brief",
            "skills/subagent-driven-development/scripts/review-package",
            "skills/subagent-driven-development/scripts/sdd-workspace",
        }
        self.assertEqual(expected_sources, expected_sources & {item["source_path"] for item in mappings})
        expected_destinations = {
            "skills/orchestrated-implementation/SKILL.md",
            "scripts/task-brief",
            "scripts/review-package",
            "shared/agent-roles/implementer.md",
            "shared/agent-roles/reviewer.md",
            "shared/policies/continuity-contract.md",
            "templates/orchestration/agent-report.md",
            "templates/orchestration/resume.md",
            "templates/orchestration/review-report.md",
            "templates/orchestration/slice-brief.md",
        }
        self.assertEqual(
            expected_destinations,
            expected_destinations & {item["destination_path"] for item in mappings},
        )
        notices = read("THIRD_PARTY_NOTICES.md")
        for destination in expected_destinations:
            self.assertIn(f"`{destination}`", notices)


if __name__ == "__main__":
    unittest.main()
