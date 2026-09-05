import hashlib
import json
import re
import subprocess
import tempfile
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

ENTRY_CONTROLLERS = frozenset(
    {
        "native-focused-edit",
        "systematic-debugging",
        "openspec-propose",
        "speckit-specify",
    }
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


def section(markdown: str, heading: str) -> str:
    match = re.search(
        rf"^## {re.escape(heading)}\n(.*?)(?=^## |\Z)",
        markdown,
        flags=re.MULTILINE | re.DOTALL,
    )
    if match is None:
        raise AssertionError(f"missing section: {heading}")
    return match.group(1).strip()


def markdown_links(markdown: str) -> set[str]:
    return set(re.findall(r"\[[^\]]+\]\(([^)#]+)(?:#[^)]+)?\)", markdown))


def numbered_items(markdown: str) -> list[str]:
    return [
        normalized(match.group(1))
        for match in re.finditer(
            r"^\d+\. (.*?)(?=^\d+\. |\Z)",
            markdown,
            flags=re.MULTILINE | re.DOTALL,
        )
    ]


def section_json(markdown: str, heading: str) -> dict[str, object]:
    match = re.search(r"```json\n(.*?)\n```", section(markdown, heading), flags=re.DOTALL)
    if match is None:
        raise AssertionError(f"{heading} must contain a fenced JSON contract")
    value = json.loads(match.group(1))
    if not isinstance(value, dict):
        raise AssertionError(f"{heading} JSON contract must be an object")
    return value


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
    def test_convergence_retry_and_as_built_gate_are_explicit(self) -> None:
        """Open convergence findings must return to the sole executor, never verification."""
        graph = fenced_json("shared/policies/lifecycle-handoffs.md")
        retry = graph.get("retry_transitions", [])
        self.assertEqual(1, len(retry))
        self.assertEqual("speckit-converge", retry[0]["from"])
        self.assertEqual("orchestrated-implementation", retry[0]["to"])
        self.assertEqual("actionable findings appended as new slices", retry[0]["condition"])
        execution = next(edge for edge in graph["edges"] if edge["from"] == "orchestrated-implementation")
        self.assertEqual("architecture-modeling:as-built", execution.get("required_gate"))
        completion = next(edge for edge in graph["edges"] if edge["from"] == "speckit-converge")
        self.assertEqual("no actionable findings and all evidence current", completion.get("completion_guard"))

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
                ["project-backlog", "verification-before-completion"],
                ["speckit-specify", "openspec-propose", "systematic-debugging"],
            ),
            "reproducible-defect": (
                "systematic-debugging",
                ["project-backlog", "test-driven-development", "verification-before-completion"],
                ["native-focused-edit", "openspec-propose", "speckit-specify"],
            ),
            "bounded-behavior-delta": (
                "openspec-propose",
                ["project-backlog", "test-driven-development", "verification-before-completion"],
                ["native-focused-edit", "systematic-debugging", "speckit-specify"],
            ),
            "multi-component-feature": (
                "speckit-specify",
                ["project-backlog", "architecture-modeling", "verification-before-completion"],
                ["native-focused-edit", "systematic-debugging", "openspec-propose"],
            ),
            "architecture-migration": (
                "speckit-specify",
                ["project-backlog", "architecture-modeling", "verification-before-completion"],
                ["native-focused-edit", "systematic-debugging", "openspec-propose"],
            ),
            "existing-artifacts": (
                "speckit-plan",
                ["project-backlog"],
                sorted(ENTRY_CONTROLLERS),
            ),
            "received-review": (
                "native-focused-edit",
                ["project-backlog", "receiving-code-review", "verification-before-completion"],
                ["speckit-specify", "openspec-propose", "systematic-debugging"],
            ),
            "independent-failures": (
                "systematic-debugging",
                ["project-backlog", "dispatching-parallel-agents", "verification-before-completion"],
                ["native-focused-edit", "openspec-propose", "speckit-specify"],
            ),
            "completion-without-evidence": (
                "native-focused-edit",
                ["project-backlog", "verification-before-completion"],
                ["speckit-specify", "openspec-propose", "systematic-debugging"],
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
                self.assertIn("project-backlog", case["supporting"])
                competing_entries = ENTRY_CONTROLLERS - {case["primary"]}
                self.assertEqual(set(competing_entries), set(case["prohibited"]) & ENTRY_CONTROLLERS)

        mutated = deepcopy(matrix)
        mutated[1]["primary"] = "openspec-propose"
        mutated_actual = {
            case["id"]: (case["primary"], case["supporting"], case["prohibited"])
            for case in mutated
        }
        self.assertNotEqual(expected, mutated_actual)

    def test_trigger_matrix_structurally_declares_artifact_state_handoffs(self) -> None:
        """A case without explicit artifact state cannot prove lifecycle continuity."""
        matrix = json.loads(read("tests/fixtures/trigger-cases/matrix.json"))
        for case in matrix:
            with self.subTest(case=case["id"]):
                self.assertEqual(
                    {"id", "request", "primary", "supporting", "prohibited", "handoff"},
                    set(case),
                )
                handoff = case["handoff"]
                self.assertEqual({"consumes", "produces", "next"}, set(handoff))
                for field in ("consumes", "produces"):
                    self.assertIsInstance(handoff[field], list)
                    self.assertTrue(handoff[field])
                    self.assertTrue(all(isinstance(value, str) and value for value in handoff[field]))
                self.assertIsInstance(handoff["next"], str)
                self.assertTrue(handoff["next"])

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
        for relative, required in expected.items():
            with self.subTest(skill=relative):
                links = markdown_links(read(relative))
                self.assertEqual(required, required & links)
                for link in links:
                    target = ((ROOT / relative).parent / link).resolve()
                    target.relative_to(ROOT.resolve())
                    self.assertTrue(target.is_file(), f"missing bundled resource file {link}")

    def test_stateful_lifecycles_recover_and_persist_operational_handoffs(self) -> None:
        """Stateful work must recover first and persist every meaningful transition."""
        for skill in LIFECYCLE_SKILLS:
            with self.subTest(skill=skill):
                markdown = read(f"skills/{skill}/SKILL.md")
                recovery = normalized(section(markdown, "Recovery preamble"))
                handoffs = normalized(section(markdown, "Operational state handoffs"))
                for phrase in (
                    "discover an active run",
                    "state.json",
                    "resume.md",
                    "canonical backlog or issue state",
                    "reconcile saved agent identities",
                    "repository evidence wins",
                    "never silently restart or reclassify",
                ):
                    self.assertIn(phrase, recovery)
                for phrase in (
                    "project-backlog",
                    "work start",
                    "scope change",
                    "blocker",
                    "completed slice",
                    "handoff",
                    "backlog state",
                    "run checkpoint",
                ):
                    self.assertIn(phrase, handoffs)
                self.assertNotIn("pending integration", normalized(markdown))
                self.assertNotIn("do not claim checkpoint continuity is operational", normalized(markdown))

    def test_recovery_precedes_canonical_mutation_with_explicit_host_observation(self) -> None:
        """Omitted or guessed live-agent state can duplicate active work."""
        for skill in LIFECYCLE_SKILLS:
            with self.subTest(skill=skill):
                items = numbered_items(section(read(f"skills/{skill}/SKILL.md"), "Recovery preamble"))
                self.assertGreaterEqual(len(items), 3)
                self.assertIn("read-only", items[0])
                self.assertIn("discover an active run", items[0])
                self.assertIn("verified absent", items[0])
                self.assertIn("platform capability seam", items[1])
                self.assertIn("host-observed live agent ids", items[1])
                self.assertIn("continuity-state recover", items[1])
                self.assertIn("--live-agents", items[1])
                self.assertIn("explicit empty observation", items[1])
                self.assertIn("host confirms none are live", items[1])
                self.assertIn("before any canonical or backlog mutation", items[2])

    def test_stateful_lifecycles_declare_backlog_support_and_event_protocol(self) -> None:
        """Implicit support or automatic event claims leave lifecycle state unauditable."""
        contract_link = "../project-backlog/SKILL.md#transition-to-event-ordering"
        for skill in LIFECYCLE_SKILLS:
            with self.subTest(skill=skill):
                markdown = read(f"skills/{skill}/SKILL.md")
                support = section(markdown, "Supporting skills")
                handoffs = section(markdown, "Operational state handoffs")
                self.assertRegex(support, r"(?m)^- `project-backlog`(?:\s|$)")
                self.assertIn(f"]({contract_link})", handoffs)
                ordered = numbered_items(handoffs)
                self.assertGreaterEqual(len(ordered), 3)
                self.assertIn("continuity-state event", ordered[0])
                self.assertIn("applicable event", ordered[0])
                self.assertIn("continuity-state checkpoint", ordered[1])
                self.assertIn("event call succeeds", ordered[2])
                self.assertIn("never automatic", ordered[2])


class ProjectBacklogSkillContractTests(unittest.TestCase):
    def test_project_backlog_recovers_before_mutation_from_explicit_host_state(self) -> None:
        """The state service must not mutate canonical truth from an unverified run."""
        items = numbered_items(
            section(read("skills/project-backlog/SKILL.md"), "Recovery gate")
        )
        self.assertGreaterEqual(len(items), 3)
        self.assertIn("read-only", items[0])
        self.assertIn("verified absent", items[0])
        self.assertIn("platform capability seam", items[1])
        self.assertIn("host-observed live agent ids", items[1])
        self.assertIn("continuity-state recover", items[1])
        self.assertIn("--live-agents", items[1])
        self.assertIn("explicit empty observation", items[1])
        self.assertIn("host confirms none are live", items[1])
        self.assertIn("before any canonical or backlog mutation", items[2])

    def test_absent_run_exception_is_shared_and_cannot_recover_saved_agents(self):
        for skill in (*LIFECYCLE_SKILLS, "architecture-modeling", "orchestrated-implementation"):
            with self.subTest(skill=skill):
                recovery = normalized(section(read(f"skills/{skill}/SKILL.md"), "Recovery preamble"))
                self.assertIn("read-only", recovery)
                self.assertIn("verified absent", recovery)
                self.assertIn("new-run-only", recovery)
                self.assertIn("saved", recovery)
        policy = normalized(section(read("skills/project-backlog/SKILL.md"), "Recovery gate"))
        for required in ("symlink", "unreadable", "partial", "no delegation", "never fabricate", "new-run-only"):
            self.assertIn(required, policy)

    def test_project_backlog_owns_state_services_but_never_methodology(self) -> None:
        """A state helper must not become a second lifecycle controller."""
        markdown = read("skills/project-backlog/SKILL.md")
        description = frontmatter(markdown)["description"].lower()
        responsibilities_section = section(markdown, "Responsibilities")
        responsibilities = normalized(responsibilities_section)
        boundary = normalized(section(markdown, "Methodology boundary"))
        self.assertEqual(7, len(re.findall(r"^- ", responsibilities_section, re.MULTILINE)))
        for phrase in (
            "state initialization only when absent",
            "stable-id status, priority, dependency, and blocker updates",
            "blocker-first ordering",
            "features.md handoff",
            "automatic github-mode detection",
            "cache refresh",
            "continuity pointers",
        ):
            self.assertIn(phrase, responsibilities)
        self.assertIn("supporting skill", description)
        for phrase in (
            "never classify a request",
            "choose a primary lifecycle",
            "control implementation methodology",
        ):
            self.assertIn(phrase, boundary)

    def test_bundled_scripts_resolve_from_the_skill_and_run_in_a_target_project(self) -> None:
        """Changing cwd must not turn bundled script paths into target-relative paths."""
        markdown = read("skills/project-backlog/SKILL.md")
        required = {
            "../../scripts/project-state",
            "../../scripts/backlog-to-issues",
            "../../scripts/refresh-issue-cache",
            "../../scripts/continuity-state",
        }
        links = markdown_links(section(markdown, "Bundled script resolution"))
        self.assertEqual(required, links)
        skill_dir = ROOT / "skills/project-backlog"
        for link in links:
            with self.subTest(link=link):
                resolved = (skill_dir / link).resolve()
                resolved.relative_to(ROOT.resolve())
                self.assertTrue(resolved.is_file())

        project_state = (skill_dir / "../../scripts/project-state").resolve()
        with tempfile.TemporaryDirectory() as directory:
            completed = subprocess.run(
                [str(project_state), "backlog", "init", "--project-key", "TP"],
                cwd=directory,
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(0, completed.returncode, completed.stderr)
            self.assertTrue((Path(directory) / "BACKLOG.md").is_file())
            self.assertTrue((Path(directory) / "FEATURES.md").is_file())

    def test_transition_event_contract_has_exact_order_and_write_protocols(self) -> None:
        """A transition log needs machine-checkable ordering, not an unordered vocabulary."""
        contract = section_json(
            read("skills/project-backlog/SKILL.md"), "Transition-to-event ordering"
        )
        self.assertEqual(
            [
                "workflow_started",
                "phase_changed",
                "slice_started",
                "decision_recorded",
                "agent_dispatched",
                "agent_completed",
                "verification_failed",
                "verification_passed",
                "workflow_completed",
            ],
            contract["event_order"],
        )
        self.assertEqual(
            ["recover", "durable_transition", "event", "checkpoint"],
            contract["transition_write_order"],
        )
        self.assertEqual(
            [
                "recover",
                "checkpoint_before_dispatch",
                "host_dispatch",
                "agent_dispatched",
                "checkpoint_after_dispatch",
            ],
            contract["agent_dispatch_order"],
        )
        self.assertEqual(
            [
                "verification_passed",
                "checkpoint",
                "canonical_completion",
                "workflow_completed",
                "checkpoint",
            ],
            contract["workflow_completion_order"],
        )

    def test_installed_continuity_wrapper_recovers_agents_and_preserves_event_order(self) -> None:
        """The installed wrapper must preserve live work and expose only missing agents."""
        markdown = read("skills/project-backlog/SKILL.md")
        skill_dir = ROOT / "skills/project-backlog"
        links = markdown_links(section(markdown, "Bundled script resolution"))
        scripts = {
            Path(link).name: (skill_dir / link).resolve()
            for link in links
        }
        event_order = section_json(markdown, "Transition-to-event ordering")["event_order"]

        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)

            def run(script: str, *arguments: str, input_text: str | None = None):
                return subprocess.run(
                    [str(scripts[script]), *arguments],
                    cwd=target,
                    input=input_text,
                    check=False,
                    capture_output=True,
                    text=True,
                    timeout=10,
                )

            for command in (
                ("backlog", "init", "--project-key", "EM"),
                ("backlog", "add", "--id", "EM-900", "--title", "External continuity", "--priority", "P1"),
                ("backlog", "start", "EM-900"),
            ):
                result = run("project-state", *command)
                self.assertEqual(0, result.returncode, result.stderr)

            for command in (
                ("init", "-q"),
                ("config", "user.email", "test@example.com"),
                ("config", "user.name", "Test User"),
                ("add", "BACKLOG.md", "FEATURES.md"),
                ("commit", "-q", "-m", "state"),
            ):
                subprocess.run(("git", *command), cwd=target, check=True, timeout=10)
            head = subprocess.run(
                ("git", "rev-parse", "HEAD"),
                cwd=target,
                check=True,
                capture_output=True,
                text=True,
                timeout=10,
            ).stdout.strip()
            resume = target / "resume.md"
            resume.write_text("Resume external continuity.\n", encoding="utf-8")
            state_payload = {
                "backlog_id": "EM-900",
                "lifecycle": "openspec",
                "phase": "apply",
                "current_slice": "slice-1",
                "active_work": ["slice-1"],
                "active_agent_ids": ["agent-live", "agent-gone"],
                "worktree_path": str(target),
                "base_commit": head,
                "last_observed_head": head,
                "next_action": "continue slice-1",
            }
            initialized = run(
                "continuity-state",
                "init",
                "EM-900",
                "--file",
                "-",
                "--resume-file",
                "resume.md",
                input_text=json.dumps(state_payload),
            )
            self.assertEqual(0, initialized.returncode, initialized.stderr)

            applicable_events = [
                "workflow_started",
                "phase_changed",
                "slice_started",
                "decision_recorded",
                "agent_dispatched",
                "verification_failed",
            ]
            for kind in applicable_events:
                emitted = run(
                    "continuity-state",
                    "event",
                    "EM-900",
                    "--file",
                    "-",
                    input_text=json.dumps({"kind": kind}),
                )
                self.assertEqual(0, emitted.returncode, emitted.stderr)
                checkpointed = run(
                    "continuity-state",
                    "checkpoint",
                    "EM-900",
                    "--file",
                    "-",
                    input_text=json.dumps(state_payload),
                )
                self.assertEqual(0, checkpointed.returncode, checkpointed.stderr)
            recovered = run(
                "continuity-state",
                "recover",
                "EM-900",
                "--live-agents",
                "agent-live",
            )
            self.assertEqual(0, recovered.returncode, recovered.stderr)
            self.assertIn("agent-gone", recovered.stdout)
            self.assertNotIn("agent-live", recovered.stdout)

            run_root = target / ".engineering-method/runs/EM-900"
            recovered_state = json.loads((run_root / "state.json").read_text(encoding="utf-8"))
            self.assertEqual(["agent-live"], recovered_state["active_agent_ids"])
            records = [
                json.loads(line)
                for line in (run_root / "events.jsonl").read_text(encoding="utf-8").splitlines()
            ]
            actual_kinds = [record["kind"] for record in records]
            self.assertEqual(applicable_events, actual_kinds)
            self.assertEqual(
                applicable_events,
                [kind for kind in event_order if kind in applicable_events],
            )


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
        for phrase in ("confirm archive", "confirmation to waive", "ask for confirmation"):
            self.assertNotIn(phrase, archive)

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

    def test_tdd_starting_evidence_is_consistent_for_every_work_mode(self) -> None:
        """No global red-test wording may contradict green-green refactor evidence."""
        markdown = read("skills/test-driven-development/SKILL.md")
        mode_rows = {
            cells[0]: cells[1]
            for line in markdown.splitlines()
            if line.startswith("|")
            and len(cells := [cell.strip() for cell in line.strip("|").split("|")]) == 2
            and cells[0] not in {"Work mode", "---"}
        }
        self.assertEqual(
            {
                "New or changed behavior": "Verified red then green",
                "Confirmed defect": "Verified regression red then green",
                "Behavior-preserving refactor": "Passing characterization tests before and after",
            },
            mode_rows,
        )

        sentences = re.split(r"(?<=[.!?])(?:\s+|\n+-\s+)", normalized(markdown))
        red_phrases = ("watch it fail", "test passed before implementation")
        red_qualifiers = ("new or changed behavior", "confirmed defect", "red-green mode")
        for sentence in sentences:
            if any(phrase in sentence for phrase in red_phrases):
                with self.subTest(sentence=sentence):
                    self.assertTrue(
                        any(qualifier in sentence for qualifier in red_qualifiers),
                        f"unqualified red-test rule contradicts refactor mode: {sentence}",
                    )

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

    def test_unverified_review_feedback_has_exclusive_entry_boundary(self) -> None:
        """A review allegation must not become a confirmed bug merely by being reported."""
        receiving = read("skills/receiving-code-review/SKILL.md")
        debugging = read("skills/systematic-debugging/SKILL.md")
        receiving_description = frontmatter(receiving)["description"].lower()
        debugging_description = frontmatter(debugging)["description"].lower()
        self.assertIn("unverified review feedback", receiving_description)
        self.assertIn("not for unverified review feedback", debugging_description)
        self.assertIn("receiving-code-review", debugging_description)
        self.assertIn("confirmed failure", normalized(receiving))
        self.assertIn("remains primary", normalized(receiving))

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

    def test_plan_pins_the_delta_template_source_declared_by_the_lock(self) -> None:
        """The approved source list must cover every newly selected OpenSpec input."""
        plan = read("docs/plans/EM-003-curated-workflow-skills.md")
        lock = json.loads(read("third-party/sources.lock.json"))
        delta_mapping = next(
            mapping
            for source in lock["sources"]
            if source["id"] == "openspec"
            for mapping in source["files"]
            if mapping.get("destination_path") == "templates/openspec/spec.md"
        )
        self.assertEqual("schemas/spec-driven/templates/spec.md", delta_mapping["source_path"])
        openspec_row = next(
            line for line in plan.splitlines() if line.startswith("| OpenSpec |")
        )
        self.assertIn(f"`{delta_mapping['source_path']}`", openspec_row)


if __name__ == "__main__":
    unittest.main()
