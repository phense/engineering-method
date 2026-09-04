import hashlib
import json
import re
import unittest
from copy import deepcopy
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


def normalized(markdown: str) -> str:
    return " ".join(markdown.lower().split())


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

    def test_conditional_handoffs_deactivate_prior_lifecycle_and_preserve_traceability(self) -> None:
        """Reclassification and escalation must not leave two active lifecycle owners."""
        graph = fenced_json("shared/policies/lifecycle-handoffs.md")
        conditional_edges = [
            edge
            for edge in graph["edges"]
            if "condition" in edge
        ]
        self.assertEqual(
            {
                ("systematic-debugging", "openspec-propose"),
                ("systematic-debugging", "speckit-specify"),
                ("openspec-propose", "speckit-specify"),
                ("openspec-apply", "speckit-specify"),
            },
            {(edge["from"], edge["to"]) for edge in conditional_edges},
        )
        for edge in conditional_edges:
            with self.subTest(edge=edge):
                self.assertEqual(edge["from"], edge["deactivates"])
                self.assertTrue(edge["artifact"])
                self.assertTrue(edge["traceability"])

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

    def test_trigger_matrix_has_exact_roles_consistent_with_skills_and_handoffs(self) -> None:
        """Changing a role assignment must expose a collision or missing support boundary."""
        matrix = json.loads(read("tests/fixtures/trigger-cases/matrix.json"))
        expected = {
            "trivial-edit": (
                "native-focused-edit",
                ["verification-before-completion"],
                ["speckit-specify", "openspec-propose", "systematic-debugging"],
            ),
            "reproducible-defect": (
                "systematic-debugging",
                ["test-driven-development", "verification-before-completion"],
                ["speckit-specify", "openspec-propose"],
            ),
            "bounded-behavior-delta": (
                "openspec-propose",
                ["test-driven-development", "verification-before-completion"],
                ["speckit-specify", "systematic-debugging"],
            ),
            "multi-component-feature": (
                "speckit-specify",
                ["architecture-modeling", "verification-before-completion"],
                ["openspec-propose", "systematic-debugging"],
            ),
            "architecture-migration": (
                "speckit-specify",
                ["architecture-modeling", "verification-before-completion"],
                ["openspec-propose", "systematic-debugging"],
            ),
            "existing-artifacts": (
                "speckit-plan",
                [],
                ["speckit-specify", "openspec-propose"],
            ),
            "received-review": (
                "native-focused-edit",
                ["receiving-code-review", "verification-before-completion"],
                ["speckit-specify", "openspec-propose"],
            ),
            "independent-failures": (
                "systematic-debugging",
                ["dispatching-parallel-agents", "verification-before-completion"],
                ["speckit-specify", "openspec-propose"],
            ),
            "completion-without-evidence": (
                "native-focused-edit",
                ["verification-before-completion"],
                ["speckit-specify", "openspec-propose"],
            ),
        }
        actual = {
            case["id"]: (case["primary"], case["supporting"], case["prohibited"])
            for case in matrix
        }
        self.assertEqual(expected, actual)

        graph = fenced_json("shared/policies/lifecycle-handoffs.md")
        known = set(graph["nodes"]) | {"native-focused-edit"}
        known.update(path.parent.name for path in (ROOT / "skills").glob("*/SKILL.md"))
        for case in matrix:
            with self.subTest(case=case["id"]):
                roles = [case["primary"], *case["supporting"], *case["prohibited"]]
                self.assertEqual([], sorted(set(roles) - known))
                self.assertNotIn(case["primary"], case["supporting"])
                self.assertNotIn(case["primary"], case["prohibited"])
                self.assertEqual([], sorted(set(case["supporting"]) & set(case["prohibited"])))

        mutated = deepcopy(matrix)
        mutated[1]["primary"] = "openspec-propose"
        mutated_actual = {
            case["id"]: (case["primary"], case["supporting"], case["prohibited"])
            for case in mutated
        }
        self.assertNotEqual(expected, mutated_actual)

    def test_installed_resource_links_are_skill_relative_and_resolve(self) -> None:
        """An installed skill must not depend on the invoking working directory."""
        expected = {
            "skills/speckit-specify/SKILL.md": {"../../templates/spec-kit/spec.md"},
            "skills/speckit-plan/SKILL.md": {"../../templates/spec-kit/plan.md"},
            "skills/speckit-tasks/SKILL.md": {"../../templates/spec-kit/tasks.md"},
            "skills/openspec-propose/SKILL.md": {
                "../../templates/openspec/proposal.md",
                "../../templates/openspec/design.md",
                "../../templates/openspec/tasks.md",
                "../../templates/openspec/spec.md",
                "../../templates/openspec/escalation.md",
            },
            "skills/test-driven-development/SKILL.md": {"writing-good-tests.md"},
            "skills/requesting-code-review/SKILL.md": {"code-reviewer.md"},
        }
        link_pattern = re.compile(r"\[[^\]]+\]\(([^)#]+)(?:#[^)]+)?\)")
        for relative, required in expected.items():
            with self.subTest(skill=relative):
                links = set(link_pattern.findall(read(relative)))
                self.assertEqual(required, required & links)
                for link in links:
                    target = ((ROOT / relative).parent / link).resolve()
                    target.relative_to(ROOT.resolve())
                    self.assertTrue(target.exists(), f"missing bundled resource {link}")

    def test_stateful_checkpoint_operations_disclose_pending_integration(self) -> None:
        """Tasks 1-5 must not claim operational checkpoint writes before integration."""
        for skill in LIFECYCLE_SKILLS:
            with self.subTest(skill=skill):
                content = normalized(read(f"skills/{skill}/SKILL.md"))
                for phrase in (
                    "checkpoint initialization and writes",
                    "em-002 and task 6 integration",
                    "do not claim checkpoint continuity is operational",
                ):
                    self.assertIn(phrase, content)


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

    def test_planning_phases_return_to_coordinator_for_authorized_continuation(self) -> None:
        """Planning-only scope must not discard end-to-end authority at its handoff."""
        for skill in ("speckit-specify", "speckit-plan", "speckit-tasks"):
            with self.subTest(skill=skill):
                content = normalized(read(f"skills/{skill}/SKILL.md"))
                for phrase in (
                    "return control to the coordinator",
                    "original request authorizes end-to-end",
                    "continue the declared next phase",
                ):
                    self.assertIn(phrase, content)

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


class OpenSpecSkillContractTests(unittest.TestCase):
    SKILLS = ("openspec-propose", "openspec-apply", "openspec-archive")

    def test_descriptions_bound_brownfield_ownership(self) -> None:
        """OpenSpec discovery must route defects and architecture-bearing work elsewhere."""
        descriptions = {
            skill: frontmatter(read(f"skills/{skill}/SKILL.md"))["description"].lower()
            for skill in self.SKILLS
        }
        proposal = descriptions["openspec-propose"]
        for term in ("bounded", "existing capability", "not for", "defect", "architecture"):
            self.assertIn(term, proposal)
        self.assertIn("existing change", descriptions["openspec-apply"])
        self.assertIn("all tasks complete", descriptions["openspec-archive"])

    def test_propose_is_planning_only_and_apply_is_the_only_executor(self) -> None:
        """A proposal or archive phase must not become another Brownfield executor."""
        propose = normalized(read("skills/openspec-propose/SKILL.md"))
        apply = normalized(read("skills/openspec-apply/SKILL.md"))
        archive = normalized(read("skills/openspec-archive/SKILL.md"))
        self.assertIn("must not edit application code", propose)
        self.assertIn("planning boundary", propose)
        self.assertIn("sole brownfield executor", apply)
        self.assertIn("edits application code", apply)
        self.assertIn("must not edit application code", archive)

    def test_propose_returns_to_coordinator_for_authorized_continuation(self) -> None:
        """A planning-only proposal must preserve end-to-end change authority."""
        content = normalized(read("skills/openspec-propose/SKILL.md"))
        for phrase in (
            "return control to the coordinator",
            "original request authorizes end-to-end",
            "continue the declared next phase",
        ):
            self.assertIn(phrase, content)

    def test_delta_spec_template_defines_deterministic_operations_and_merge(self) -> None:
        """A delta must preserve stable requirement and scenario semantics at archive."""
        relative = "templates/openspec/spec.md"
        template = read(relative)
        required_headings = {
            "Purpose",
            "ADDED Requirements",
            "MODIFIED Requirements",
            "REMOVED Requirements",
            "RENAMED Requirements",
        }
        self.assertEqual(required_headings, required_headings & headings(template))
        content = normalized(template)
        for phrase in (
            "stable requirement identity",
            "exactly four hash marks",
            "complete replacement block",
            "every surviving scenario",
            "reason and migration",
            "renamed then removed then modified then added",
            "conflict",
            "main spec does not exist",
            "only added requirements",
        ):
            self.assertIn(phrase, content)

        archive = normalized(read("skills/openspec-archive/SKILL.md"))
        for phrase in (
            "renamed then removed then modified then added",
            "complete replacement block",
            "main spec does not exist",
            "stop on conflict",
        ):
            self.assertIn(phrase, archive)

    def test_change_artifact_layout_and_formal_escalation_are_explicit(self) -> None:
        """A Brownfield delta must remain traceable when escalation changes lifecycle."""
        propose = read("skills/openspec-propose/SKILL.md")
        for relative in (
            "openspec/changes/<change-id>/proposal.md",
            "openspec/changes/<change-id>/design.md",
            "openspec/changes/<change-id>/tasks.md",
            "openspec/changes/<change-id>/specs/<capability>/spec.md",
        ):
            self.assertIn(relative, propose)

        escalation = headings(read("templates/openspec/escalation.md"))
        self.assertEqual(
            {"Status", "Reason", "Preserved change", "Spec Kit handoff"},
            {"Status", "Reason", "Preserved change", "Spec Kit handoff"} & escalation,
        )
        escalation_content = read("templates/openspec/escalation.md")
        for phrase in (
            "status: escalated",
            "openspec/changes/<change-id>/",
            "<stable-feature-id>",
            "specs/<stable-feature-id>-<name>/spec.md",
        ):
            self.assertIn(phrase, escalation_content)

        apply = normalized(read("skills/openspec-apply/SKILL.md"))
        self.assertIn("status: escalated", apply)
        self.assertIn("executor is inactive", apply)

    def test_archive_requires_complete_tasks_and_fresh_verification(self) -> None:
        """Archive must refuse rather than waive incomplete or failing change evidence."""
        archive = normalized(read("skills/openspec-archive/SKILL.md"))
        for phrase in (
            "refuse to archive",
            "incomplete task",
            "fresh verification",
            "openspec/specs/<capability>/spec.md",
            "openspec/changes/archive/yyyy-mm-dd-<change-id>/",
        ):
            self.assertIn(phrase, archive)
        self.assertNotIn("confirm", archive)

    def test_openspec_skills_remove_cli_store_schema_and_dynamic_runtime_inputs(self) -> None:
        """The shared lifecycle must work without an OpenSpec runtime controller."""
        prohibited = (
            "allowed-tools",
            "requires openspec cli",
            "store selection",
            "profile",
            "schema selection",
            "instructions json",
            "dynamic instruction",
            "openspec status",
            "openspec list",
            "openspec archive ",
        )
        for skill in self.SKILLS:
            with self.subTest(skill=skill):
                content = read(f"skills/{skill}/SKILL.md").lower()
                for token in prohibited:
                    self.assertNotIn(token, content)
                self.assertNotRegex(content, r"(?m)^\s*(?:\$ )?openspec\s")


class QualitySkillContractTests(unittest.TestCase):
    SKILLS = (
        "systematic-debugging",
        "test-driven-development",
        "verification-before-completion",
    )

    def test_debugging_requires_observed_failure_and_root_cause(self) -> None:
        """A deliberate behavior request must not be misclassified as a defect."""
        content = normalized(read("skills/systematic-debugging/SKILL.md"))
        description = frontmatter(read("skills/systematic-debugging/SKILL.md"))["description"].lower()
        for phrase in ("observed failure", "test regression", "unexplained behavior", "not for"):
            self.assertIn(phrase, description)
        for phrase in (
            "reproduce",
            "root cause",
            "one hypothesis",
            "smallest test",
            "do not propose a fix",
        ):
            self.assertIn(phrase, content)

    def test_debugging_handoff_requires_evidence_of_intent_change(self) -> None:
        """An unsuccessful repair attempt must not manufacture a feature lifecycle."""
        content = normalized(read("skills/systematic-debugging/SKILL.md"))
        for phrase in (
            "intentional contract change",
            "architecture change",
            "evidence establishes",
            "openspec-propose",
            "speckit-specify",
        ):
            self.assertIn(phrase, content)

    def test_tdd_applies_only_to_meaningful_testable_behavior(self) -> None:
        """TDD must not create implementation-mirroring tests for prose or mechanics."""
        content = normalized(read("skills/test-driven-development/SKILL.md"))
        description = frontmatter(read("skills/test-driven-development/SKILL.md"))["description"].lower()
        for phrase in ("testable behavior", "before implementation", "not for documentation"):
            self.assertIn(phrase, description)
        for phrase in (
            "watch it fail",
            "expected reason",
            "minimal implementation",
            "implementation-mirroring",
            "writing-good-tests.md",
        ):
            self.assertIn(phrase, content)

    def test_tdd_distinguishes_new_behavior_from_existing_code_and_refactors(self) -> None:
        """Test-first discipline must not delete baseline code or invent a refactor failure."""
        content = normalized(read("skills/test-driven-development/SKILL.md"))
        for phrase in (
            "do not delete pre-existing code",
            "own uncommitted and safely recoverable production diff",
            "new behavior and confirmed defects",
            "verified red-green",
            "behavior-preserving refactor",
            "passing characterization tests before and after",
            "do not invent a failing behavior",
        ):
            self.assertIn(phrase, content)

    def test_verification_requires_fresh_output_before_every_success_claim(self) -> None:
        """Prior or partial output must not support a pass, fix, or completion claim."""
        content = normalized(read("skills/verification-before-completion/SKILL.md"))
        description = frontmatter(read("skills/verification-before-completion/SKILL.md"))["description"].lower()
        for phrase in ("pass", "fix", "completion claim", "fresh output"):
            self.assertIn(phrase, description)
        for phrase in (
            "identify the command",
            "run the full command",
            "read the complete output",
            "exit status",
            "prior output",
        ):
            self.assertIn(phrase, content)

    def test_quality_skills_are_host_and_provider_neutral(self) -> None:
        """A shared quality skill must not depend on omitted controllers or host syntax."""
        prohibited = (
            "superpowers:",
            "using-superpowers",
            "finishing-a-development-branch",
            "gpt-",
            "claude-",
            "spawn_agent",
            "task(",
        )
        for skill in self.SKILLS:
            with self.subTest(skill=skill):
                content = read(f"skills/{skill}/SKILL.md").lower()
                for token in prohibited:
                    self.assertNotIn(token, content)


class CollaborationSkillContractTests(unittest.TestCase):
    SKILLS = (
        "requesting-code-review",
        "receiving-code-review",
        "using-git-worktrees",
        "dispatching-parallel-agents",
    )

    def test_review_depth_is_risk_proportionate(self) -> None:
        """Mechanical work may avoid extra cost while risky work gets independence."""
        content = normalized(read("skills/requesting-code-review/SKILL.md"))
        for phrase in (
            "mechanical slices",
            "coordinator review",
            "risky or integration-bearing",
            "independent reviewer",
            "critical",
            "important",
        ):
            self.assertIn(phrase, content)

        template = headings(read("skills/requesting-code-review/code-reviewer.md"))
        self.assertEqual(
            {"Requirements", "Review scope", "Findings", "Verdict"},
            {"Requirements", "Review scope", "Findings", "Verdict"} & template,
        )

    def test_received_feedback_is_verified_before_implementation(self) -> None:
        """A plausible review suggestion must not bypass current repository evidence."""
        content = normalized(read("skills/receiving-code-review/SKILL.md"))
        for phrase in (
            "verify against current code",
            "clarify",
            "technical pushback",
            "one finding at a time",
            "test-driven-development",
            "verification-before-completion",
        ):
            self.assertIn(phrase, content)

    def test_worktree_isolation_prefers_native_capabilities_and_guards_fallback(self) -> None:
        """Fallback isolation must not create phantom state or target broad paths."""
        content = normalized(read("skills/using-git-worktrees/SKILL.md"))
        for phrase in (
            "resolved git directory",
            "common git directory",
            "submodule",
            "detached head",
            "native worktree",
            "fallback",
            "ignored",
            "repository root",
            "broad path",
            "baseline tests",
        ):
            self.assertIn(phrase, content)
        for command in ("git worktree add", "git checkout -b", "git branch"):
            self.assertNotIn(command, content)

    def test_parallel_dispatch_requires_proven_independence_and_safe_writes(self) -> None:
        """Shared state or overlapping ownership must force serialized writes."""
        content = normalized(read("skills/dispatching-parallel-agents/SKILL.md"))
        for phrase in (
            "independence is established",
            "read-only investigation",
            "parallel",
            "disjoint ownership",
            "safe isolation",
            "serialize writes",
            "full test suite",
        ):
            self.assertIn(phrase, content)

    def test_collaboration_skills_do_not_call_omitted_or_host_specific_controllers(self) -> None:
        """Shared collaboration semantics must be resolved only by platform adapters."""
        prohibited = (
            "finishing-a-development-branch",
            "using-superpowers",
            "superpowers:",
            "spawn_agent",
            "enterworktree",
            "/worktree",
            "gpt-",
            "claude-",
        )
        for skill in self.SKILLS:
            with self.subTest(skill=skill):
                content = read(f"skills/{skill}/SKILL.md").lower()
                for token in prohibited:
                    self.assertNotIn(token, content)


class ProvenanceContractTests(unittest.TestCase):
    def test_normal_contracts_use_only_repository_contained_provenance_facts(self) -> None:
        """Normal tests must not require a machine-local upstream checkout."""
        machine_local_root = "/" + "tmp"
        self.assertNotIn(machine_local_root, read("tests/test_skill_contracts.py"))

    def test_locked_destination_hashes_and_source_metadata_are_complete(self) -> None:
        """Changing an adapted file without its lock metadata must fail provenance."""
        lock = json.loads(read("third-party/sources.lock.json"))
        destinations: set[str] = set()
        for source in lock["sources"]:
            for mapping in source["files"]:
                if mapping["modification_status"] == "notice-only":
                    continue
                with self.subTest(source=source["id"], destination=mapping["destination_path"]):
                    destination_path = ROOT / mapping["destination_path"]
                    self.assertRegex(mapping["source_sha256"], r"^[0-9a-f]{64}$")
                    self.assertNotIn(mapping["destination_path"], destinations)
                    destinations.add(mapping["destination_path"])
                    self.assertEqual(
                        mapping["destination_sha256"],
                        hashlib.sha256(destination_path.read_bytes()).hexdigest(),
                    )

    def test_delta_spec_uses_real_pinned_template_and_escalation_is_original(self) -> None:
        """Original escalation text must not be misattributed as an upstream adaptation."""
        lock = json.loads(read("third-party/sources.lock.json"))
        mappings = {
            mapping["destination_path"]: (source["id"], mapping)
            for source in lock["sources"]
            for mapping in source["files"]
            if mapping["modification_status"] == "adapted"
        }
        source_id, delta = mappings["templates/openspec/spec.md"]
        self.assertEqual("openspec", source_id)
        self.assertEqual("schemas/spec-driven/templates/spec.md", delta["source_path"])
        self.assertEqual(
            "1f370642f106589d901c0568e81b5f7741e9289da48df41b70dd21ad99592a0c",
            delta["source_sha256"],
        )
        self.assertNotIn("templates/openspec/escalation.md", mappings)
        self.assertIn(
            "`templates/openspec/escalation.md`: original",
            read("THIRD_PARTY_NOTICES.md"),
        )


if __name__ == "__main__":
    unittest.main()
