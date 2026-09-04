"""Contracts for host-neutral orchestration roles, briefs, and reports."""

from __future__ import annotations

import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ROLE_NAMES = {"strong", "standard", "fast"}
ROLE_FILES = ("implementer", "debugger", "reviewer", "system-architect")


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


class ModelRoutingContractTests(unittest.TestCase):
    def test_common_policy_defines_exactly_three_semantic_roles(self) -> None:
        """Adding a provider role or omitting a capability tier breaks portable routing."""
        contract = fenced_json("shared/policies/model-routing.md")
        self.assertEqual(ROLE_NAMES, set(contract["roles"]))
        for role in ROLE_NAMES:
            with self.subTest(role=role):
                definition = contract["roles"][role]
                self.assertEqual({"use_for", "do_not_use_for"}, set(definition))
                self.assertTrue(definition["use_for"])
                self.assertTrue(definition["do_not_use_for"])

    def test_common_skills_contain_no_provider_model_identifiers(self) -> None:
        """A concrete provider ID in a shared skill bypasses the EM-005 adapter seam."""
        provider_id = re.compile(
            r"(?i)\b(?:gpt-[0-9]|claude-(?:opus|sonnet|haiku|fable)(?:-[0-9]|\b))"
        )
        offenders = [
            path.relative_to(ROOT).as_posix()
            for path in sorted((ROOT / "skills").rglob("*"))
            if path.is_file() and provider_id.search(path.read_text(encoding="utf-8"))
        ]
        self.assertEqual([], offenders)

    def test_runtime_selection_falls_back_by_semantic_tier_and_records_it(self) -> None:
        """Unavailable preferred tiers must degrade honestly through the adapter."""
        policy = normalized("shared/policies/model-routing.md")
        for phrase in (
            "platform adapter",
            "actual available",
            "next lower available tier",
            "record the fallback",
            "cannot change the main model",
            "must not claim",
            "completed-task turns",
        ):
            self.assertIn(phrase, policy)


class AgentContractTests(unittest.TestCase):
    def test_four_agent_roles_publish_explicit_input_and_output_contracts(self) -> None:
        """A worker without bounded inputs or outputs cannot be integrated safely."""
        required_inputs = {"work_id", "slice_id", "requirements", "owned_paths", "interfaces"}
        for role in ROLE_FILES:
            with self.subTest(role=role):
                relative = f"shared/agent-roles/{role}.md"
                contract = fenced_json(relative)
                self.assertEqual(required_inputs, required_inputs & set(contract["inputs"]))
                self.assertEqual("templates/orchestration/agent-report.md", contract["output"])
                self.assertIn(contract["preferred_role"], ROLE_NAMES)

    def test_agent_report_schema_contains_integration_evidence(self) -> None:
        """A report missing identity, changes, tests, or findings is not actionable."""
        contract = fenced_json("templates/orchestration/agent-report.md")
        self.assertEqual(
            {
                "status",
                "work_id",
                "slice_id",
                "commits",
                "files",
                "tests",
                "root_cause",
                "fix_findings",
                "concerns",
                "next_dependency_facts",
            },
            set(contract["required"]),
        )
        self.assertEqual({"command", "result"}, set(contract["tests_required"]))
        self.assertEqual(
            {"DONE", "DONE_WITH_CONCERNS", "BLOCKED", "NEEDS_CONTEXT"},
            set(contract["statuses"]),
        )

    def test_orchestration_templates_are_distinct_file_backed_handoffs(self) -> None:
        """Dispatch, review, and recovery need durable artifacts with non-overlapping jobs."""
        contracts = {
            name: fenced_json(f"templates/orchestration/{name}.md")
            for name in ("slice-brief", "review-report", "resume")
        }
        self.assertEqual("dispatch", contracts["slice-brief"]["purpose"])
        self.assertEqual("review", contracts["review-report"]["purpose"])
        self.assertEqual("recovery", contracts["resume"]["purpose"])
        self.assertEqual(
            {"work_id", "slice_id"},
            {"work_id", "slice_id"} & set(contracts["slice-brief"]["required"]),
        )


if __name__ == "__main__":
    unittest.main()
