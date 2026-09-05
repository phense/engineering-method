"""Contracts for focused, original, Mermaid-first architecture modeling."""

from __future__ import annotations

import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


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


class ArchitectureActivationTests(unittest.TestCase):
    def test_discovery_requires_phase_artifacts_before_architecture_analysis(self):
        """A new migration request must reach specification before the architecture gate."""
        description = (ROOT / "skills/architecture-modeling/SKILL.md").read_text().splitlines()[2]
        self.assertIn("approved Spec Kit plan", description)
        self.assertIn("implemented slices", description)
        self.assertIn("Not for initial feature requests", description)

    def test_gate_activates_for_exactly_the_five_approved_risk_categories(self) -> None:
        """Expanding or shrinking activation makes architecture depth disproportionate."""
        contract = fenced_json("shared/policies/architecture-gate.md")
        self.assertEqual(
            {
                "large_cross_component_feature",
                "new_or_materially_changed_system_boundary",
                "architectural_refactor",
                "substantial_migration",
                "cross_component_concurrency_security_or_data_integrity",
            },
            set(contract["activate_for"]),
        )

    def test_gate_excludes_small_local_documentation_and_mechanical_work(self) -> None:
        """A local edit must not acquire a UML lifecycle merely because templates exist."""
        contract = fenced_json("shared/policies/architecture-gate.md")
        self.assertEqual(
            {"small_fix", "localized_brownfield_change", "documentation", "mechanical_refactor"},
            set(contract["exclude_for"]),
        )
        self.assertEqual(set(), set(contract["activate_for"]) & set(contract["exclude_for"]))


class ArchitectureArtifactTests(unittest.TestCase):
    def test_each_diagram_must_answer_a_named_question_and_carry_metadata(self) -> None:
        """A diagram without purpose or evidence cannot govern design or verification."""
        policy = fenced_json("shared/policies/architecture-gate.md")
        self.assertTrue(policy["named_question_required"])
        self.assertTrue(policy["omit_irrelevant_diagrams"])
        metadata = fenced_json("templates/uml/diagram-metadata.md")
        self.assertEqual(
            {"purpose", "source_evidence", "requirement_ids", "notation", "verified_on"},
            set(metadata["required"]),
        )
        self.assertEqual("YYYY-MM-DD", metadata["verified_on_format"])

    def test_mermaid_templates_have_metadata_and_valid_diagram_openers(self) -> None:
        """A copied filename or malformed opener must not masquerade as renderable source."""
        expected = {
            "component": "flowchart LR",
            "sequence": "sequenceDiagram",
            "state": "stateDiagram-v2",
            "activity": "flowchart TD",
            "deployment": "flowchart TB",
        }
        for name, opener in expected.items():
            with self.subTest(diagram=name):
                content = read(f"templates/uml/{name}.mmd")
                for label in (
                    "%% Purpose:",
                    "%% Source evidence:",
                    "%% Requirement IDs:",
                    "%% Notation: Mermaid",
                    "%% Verified on:",
                ):
                    self.assertIn(label, content)
                code = [line for line in content.splitlines() if line and not line.startswith("%%")]
                self.assertEqual(opener, code[0])

    def test_mermaid_is_default_and_plantuml_requires_value_and_validation(self) -> None:
        """A renderer dependency must never be introduced without a material modeling gain."""
        skill = normalized("skills/architecture-modeling/SKILL.md")
        self.assertIn("mermaid is the dependency-free default", skill)
        self.assertIn("material modeling value", skill)
        self.assertIn("validator is available", skill)
        self.assertIn("self-contained", skill)
        self.assertNotIn("docs-management", skill)


class ArchitectureAnalysisTests(unittest.TestCase):
    def test_design_analysis_checks_every_required_architecture_failure_class(self) -> None:
        """Omitting one analysis class lets a diagram go green while its hazard remains."""
        contract = fenced_json("shared/policies/architecture-gate.md")
        self.assertEqual(
            {
                "ownership",
                "interface_mismatch",
                "dependency_cycles",
                "invalid_or_unreachable_states",
                "failure_or_rollback_gaps",
                "ordering_or_races",
                "trust_boundaries",
                "migration_consistency",
            },
            set(contract["analysis_checks"]),
        )

    def test_findings_precede_tasks_and_as_built_reconciliation_precedes_integration(self) -> None:
        """Late findings cannot shape tasks and stale diagrams cannot derive valid tests."""
        contract = fenced_json("shared/policies/architecture-gate.md")
        self.assertEqual(
            [
                "analyze_plan_and_repository",
                "create_relevant_diagrams",
                "write_docs/uml/findings.md",
                "speckit-tasks",
            ],
            contract["design_time_order"],
        )
        self.assertEqual(
            [
                "reconcile_diagrams_against_code",
                "classify_every_difference",
                "system_architect_integration_tests",
            ],
            contract["as_built_order"],
        )
        self.assertEqual(
            {"code_corrected", "diagram_corrected_with_rationale", "unresolved_defect"},
            set(contract["difference_dispositions"]),
        )

    def test_architecture_assets_are_original_not_upstream_mappings(self) -> None:
        """Original architecture guidance must not be falsely attributed as copied work."""
        lock = json.loads(read("third-party/sources.lock.json"))
        mapped = {
            item["destination_path"]
            for source in lock["sources"]
            for item in source["files"]
            if item["modification_status"] == "adapted"
        }
        originals = {
            "skills/architecture-modeling/SKILL.md",
            "shared/policies/architecture-gate.md",
            "templates/uml/README.md",
            "templates/uml/diagram-metadata.md",
            "templates/uml/component.mmd",
            "templates/uml/sequence.mmd",
            "templates/uml/state.mmd",
            "templates/uml/activity.mmd",
            "templates/uml/deployment.mmd",
        }
        self.assertEqual(set(), originals & mapped)


if __name__ == "__main__":
    unittest.main()
