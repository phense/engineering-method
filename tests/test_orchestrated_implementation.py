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


class OrchestrationScriptTests(unittest.TestCase):
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
            tasks = root / "specs/F-001-checkout/tasks.md"
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
