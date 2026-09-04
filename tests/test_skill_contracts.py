import hashlib
import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

LIFECYCLE_SKILLS = (
    "systematic-debugging",
    "openspec-propose",
    "openspec-apply",
    "openspec-archive",
    "speckit-specify",
    "speckit-plan",
    "speckit-tasks",
    "speckit-converge",
)

CONTRACT_HEADINGS = (
    "Trigger",
    "Do not use for",
    "Consumes",
    "Produces",
    "Completion",
    "Next phase",
    "Supporting skills",
)


def read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def headings(markdown: str) -> set[str]:
    return set(re.findall(r"^## ([^\n]+)$", markdown, flags=re.MULTILINE))


def fenced_json(relative: str) -> dict[str, object]:
    content = read(relative)
    match = re.search(r"```json\n(.*?)\n```", content, flags=re.DOTALL)
    if match is None:
        raise AssertionError(f"{relative} must contain a fenced JSON contract")
    value = json.loads(match.group(1))
    if not isinstance(value, dict):
        raise AssertionError(f"{relative} JSON contract must be an object")
    return value


class LifecycleContractTests(unittest.TestCase):
    def test_every_lifecycle_skill_exposes_the_contract_headings(self) -> None:
        """Removing a lifecycle artifact boundary must make its contract incomplete."""
        for skill in LIFECYCLE_SKILLS:
            with self.subTest(skill=skill):
                actual = headings(read(f"skills/{skill}/SKILL.md"))
                self.assertEqual(set(CONTRACT_HEADINGS), set(CONTRACT_HEADINGS) & actual)

    def test_handoff_graph_is_acyclic_and_has_one_executor_per_lifecycle(self) -> None:
        """Adding a competing executor or cyclic handoff must invalidate the workflow."""
        graph = fenced_json("shared/policies/lifecycle-handoffs.md")
        nodes = graph["nodes"]
        edges = graph["edges"]
        executors = graph["executors"]
        self.assertIsInstance(nodes, list)
        self.assertIsInstance(edges, list)
        self.assertEqual(
            {
                "bugfix": "test-driven-development",
                "openspec": "openspec-apply",
                "speckit": "orchestrated-implementation",
            },
            executors,
        )

        adjacency = {node: [] for node in nodes}
        for edge in edges:
            adjacency[edge["from"]].append(edge["to"])

        visiting: set[str] = set()
        visited: set[str] = set()

        def visit(node: str) -> None:
            self.assertNotIn(node, visiting, f"cycle reaches {node}")
            if node in visited:
                return
            visiting.add(node)
            for successor in adjacency[node]:
                visit(successor)
            visiting.remove(node)
            visited.add(node)

        for node in nodes:
            visit(node)

    def test_openspec_to_speckit_requires_a_formal_escalation_artifact(self) -> None:
        """A direct cross-lifecycle handoff must not bypass the escalation record."""
        graph = fenced_json("shared/policies/lifecycle-handoffs.md")
        cross_edges = [
            edge
            for edge in graph["edges"]
            if edge["from"].startswith("openspec-") and edge["to"].startswith("speckit-")
        ]
        self.assertEqual(
            [
                {
                    "from": "openspec-propose",
                    "to": "speckit-specify",
                    "artifact": "openspec/changes/<change-id>/escalation.md",
                    "condition": "status: escalated",
                }
            ],
            cross_edges,
        )

    def test_templates_expose_required_engineering_decisions(self) -> None:
        """Deleting a required decision section must leave an unsafe artifact template."""
        expected = {
            "templates/spec-kit/spec.md": {
                "Stable work ID",
                "Acceptance criteria",
                "Compatibility boundaries",
                "Interface contracts",
            },
            "templates/spec-kit/plan.md": {
                "Stable work ID",
                "Compatibility boundaries",
                "Interface contracts",
                "Dependencies",
                "Tests",
                "Architecture findings",
            },
            "templates/spec-kit/tasks.md": {
                "Stable work ID",
                "Dependencies",
                "Tests",
                "Architecture findings",
            },
            "templates/openspec/proposal.md": {
                "Stable work ID",
                "Acceptance criteria",
                "Compatibility boundaries",
            },
            "templates/openspec/design.md": {
                "Interface contracts",
                "Dependencies",
                "Tests",
            },
            "templates/openspec/tasks.md": {
                "Stable work ID",
                "Dependencies",
                "Tests",
            },
        }
        for relative, required in expected.items():
            with self.subTest(template=relative):
                self.assertEqual(required, required & headings(read(relative)))

    def test_trigger_matrix_covers_the_required_boundaries(self) -> None:
        """Dropping a selection boundary must make collision coverage incomplete."""
        matrix = json.loads(read("tests/fixtures/trigger-cases/matrix.json"))
        self.assertEqual(
            {
                "trivial-edit",
                "reproducible-defect",
                "bounded-behavior-delta",
                "multi-component-feature",
                "architecture-migration",
                "existing-artifacts",
                "received-review",
                "independent-failures",
                "completion-without-evidence",
            },
            {case["id"] for case in matrix},
        )
        for case in matrix:
            with self.subTest(case=case["id"]):
                self.assertIsInstance(case["primary"], str)
                self.assertTrue(case["primary"])
                self.assertIsInstance(case["supporting"], list)
                self.assertIsInstance(case["prohibited"], list)


class ProvenanceContractTests(unittest.TestCase):
    def test_mapped_source_and_destination_hashes_match_disk(self) -> None:
        """Changing an adapted file without its source-lock hash must fail provenance."""
        lock = json.loads(read("third-party/sources.lock.json"))
        source_roots = {
            "github-spec-kit": Path("/tmp/engineering-method-spec-kit"),
            "openspec": Path("/tmp/engineering-method-openspec"),
            "superpowers": Path("/tmp/engineering-method-superpowers"),
        }
        for source in lock["sources"]:
            for mapping in source["files"]:
                if mapping["modification_status"] == "notice-only":
                    continue
                with self.subTest(source=source["id"], destination=mapping["destination_path"]):
                    source_path = source_roots[source["id"]] / mapping["source_path"]
                    destination_path = ROOT / mapping["destination_path"]
                    self.assertEqual(
                        mapping["source_sha256"], hashlib.sha256(source_path.read_bytes()).hexdigest()
                    )
                    self.assertEqual(
                        mapping["destination_sha256"],
                        hashlib.sha256(destination_path.read_bytes()).hexdigest(),
                    )


if __name__ == "__main__":
    unittest.main()
