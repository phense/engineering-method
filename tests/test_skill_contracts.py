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


def frontmatter(markdown: str) -> dict[str, str]:
    self_contained = re.match(r"^---\n(.*?)\n---\n", markdown, flags=re.DOTALL)
    if self_contained is None:
        raise AssertionError("skill must start with YAML frontmatter")
    fields: dict[str, str] = {}
    for line in self_contained.group(1).splitlines():
        key, separator, value = line.partition(":")
        if not separator:
            raise AssertionError(f"invalid frontmatter line: {line}")
        fields[key] = value.strip().strip('"').strip("'")
    return fields


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


class SpecKitSkillContractTests(unittest.TestCase):
    SKILLS = ("speckit-specify", "speckit-plan", "speckit-tasks", "speckit-converge")

    def test_descriptions_define_positive_and_negative_selection_boundaries(self) -> None:
        """Weak discovery metadata must not let Spec Kit absorb defects or bounded deltas."""
        descriptions = {
            skill: frontmatter(read(f"skills/{skill}/SKILL.md"))["description"].lower()
            for skill in self.SKILLS
        }
        self.assertTrue(descriptions["speckit-specify"].startswith("use when "))
        for term in ("new capability", "cross-component", "architecture", "risky migration"):
            self.assertIn(term, descriptions["speckit-specify"])
        for term in ("not for", "defect", "bounded brownfield"):
            self.assertIn(term, descriptions["speckit-specify"])
        self.assertIn("existing spec", descriptions["speckit-plan"])
        self.assertIn("plan.md", descriptions["speckit-tasks"])
        self.assertIn("implemented", descriptions["speckit-converge"])

    def test_planning_phases_cannot_edit_application_code(self) -> None:
        """A planning request must not silently authorize implementation."""
        for skill in ("speckit-specify", "speckit-plan", "speckit-tasks"):
            with self.subTest(skill=skill):
                original = read(f"skills/{skill}/SKILL.md")
                content = original.lower()
                self.assertIn("Planning boundary", headings(original))
                self.assertIn("must not edit application code", content)

    def test_each_phase_names_exact_artifacts_and_next_phase(self) -> None:
        """Changing an artifact path or handoff must break lifecycle continuity."""
        contracts = {
            "speckit-specify": (
                "specs/<stable-feature-id>-<name>/spec.md",
                "speckit-plan",
            ),
            "speckit-plan": (
                "specs/<stable-feature-id>-<name>/plan.md",
                "architecture-modeling",
            ),
            "speckit-tasks": (
                "specs/<stable-feature-id>-<name>/tasks.md",
                "orchestrated-implementation",
            ),
            "speckit-converge": (
                "specs/<stable-feature-id>-<name>/tasks.md",
                "verification-before-completion",
            ),
        }
        for skill, expected in contracts.items():
            with self.subTest(skill=skill):
                content = read(f"skills/{skill}/SKILL.md")
                for value in expected:
                    self.assertIn(value, content)

    def test_stateful_phases_start_with_repository_validated_recovery(self) -> None:
        """Compaction recovery must not redispatch completed work from stale state."""
        required = (
            "state.json",
            "resume.md",
            "repository evidence wins",
            "never redispatch completed work",
        )
        for skill in self.SKILLS:
            with self.subTest(skill=skill):
                original = read(f"skills/{skill}/SKILL.md")
                content = original.lower()
                self.assertIn("Recovery preamble", headings(original))
                for phrase in required:
                    self.assertIn(phrase.lower(), content)

    def test_converge_is_read_only_except_append_only_tasks(self) -> None:
        """Convergence must report gaps instead of becoming a second executor."""
        content = read("skills/speckit-converge/SKILL.md").lower()
        for phrase in (
            "read-only for application code",
            "only allowed write",
            "append",
            "tasks.md",
            "actionable findings",
            "fresh verification",
        ):
            self.assertIn(phrase, content)

    def test_speckit_skills_are_free_of_removed_runtime_controllers(self) -> None:
        """A host command, hook, or omitted executor would make the shared core non-portable."""
        prohibited = (
            "/implement",
            "/analyze",
            "/clarify",
            "execute_command",
            ".specify/extensions",
            "__speckit_command_",
            "task-to-issue",
            "create-new-feature",
            "git checkout",
            "git branch",
        )
        for skill in self.SKILLS:
            with self.subTest(skill=skill):
                content = read(f"skills/{skill}/SKILL.md").lower()
                for token in prohibited:
                    self.assertNotIn(token, content)


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
