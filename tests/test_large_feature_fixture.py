"""End-to-end architecture and integration evidence for the checkout fixture."""

from __future__ import annotations

import ast
import json
import re
import subprocess
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import sys

from tests.large_feature_evidence import assert_large_feature, evidence_digest


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests/fixtures/large-feature"
PROJECT = FIXTURE / "project"


def read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def fixture_read(relative: str) -> str:
    return (FIXTURE / relative).read_text(encoding="utf-8")


def fenced_json(path: Path) -> dict[str, object]:
    match = re.search(r"```json\n(.*?)\n```", path.read_text(encoding="utf-8"), flags=re.DOTALL)
    if match is None:
        raise AssertionError(f"{path} must contain a fenced JSON contract")
    payload = json.loads(match.group(1))
    if not isinstance(payload, dict):
        raise AssertionError(f"{path} contract must be an object")
    return payload


def method_return(path: Path, class_name: str, method_name: str) -> str:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    for node in tree.body:
        if isinstance(node, ast.ClassDef) and node.name == class_name:
            for child in node.body:
                if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)) and child.name == method_name:
                    if child.returns is None:
                        raise AssertionError(f"{class_name}.{method_name} has no return annotation")
                    return ast.unparse(child.returns)
    raise AssertionError(f"missing {class_name}.{method_name} in {path}")


def called_attributes(path: Path, class_name: str, method_name: str) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    for node in tree.body:
        if isinstance(node, ast.ClassDef) and node.name == class_name:
            for child in node.body:
                if isinstance(child, ast.FunctionDef) and child.name == method_name:
                    return {
                        call.func.attr
                        for call in ast.walk(child)
                        if isinstance(call, ast.Call) and isinstance(call.func, ast.Attribute)
                    }
    raise AssertionError(f"missing {class_name}.{method_name} in {path}")


def architecture_defects(model: dict[str, object]) -> list[dict[str, object]]:
    defects: list[dict[str, object]] = []
    component = model["component"]
    expected = component["order_requires"]["reserve_returns"]
    actual = component["inventory_provides"]["reserve_returns"]
    if expected != actual:
        defects.append(
            {
                "id": "AF-001",
                "category": "interface_mismatch",
                "expected": expected,
                "actual": actual,
            }
        )
    recovery = model["sequence"]["payment_success_inventory_commit_failure"]
    missing = sorted(set(recovery["required_compensation"]) - set(recovery["messages"]))
    states = set(model["state"]["states"])
    if missing or "Compensating" not in states:
        defects.append(
            {
                "id": "AF-002",
                "category": "failure_or_rollback_gap",
                "missing": missing,
                "compensating_state_present": "Compensating" in states,
            }
        )
    return defects


class InitialArchitectureFindingTests(unittest.TestCase):
    def test_initial_component_sequence_and_state_expose_exact_required_defects(self) -> None:
        """The fixture must fail for the specified interface and compensation defects only."""
        model = json.loads(fixture_read("initial/architecture.json"))
        defects = architecture_defects(model)
        self.assertEqual(["AF-001", "AF-002"], [finding["id"] for finding in defects])
        self.assertEqual("Reservation", defects[0]["expected"])
        self.assertEqual("bool", defects[0]["actual"])
        self.assertEqual(
            ["inventory.release", "payment.reverse"], defects[1]["missing"]
        )
        self.assertFalse(defects[1]["compensating_state_present"])

        self.assertEqual(
            "Reservation",
            method_return(FIXTURE / "initial/contracts.py", "InventoryPort", "reserve"),
        )
        self.assertEqual(
            "Reservation",
            method_return(FIXTURE / "initial/order.py", "OrderService", "reserve"),
        )
        self.assertEqual(
            "bool",
            method_return(FIXTURE / "initial/inventory.py", "Inventory", "reserve"),
        )
        initial_calls = called_attributes(
            FIXTURE / "initial/checkout.py", "CheckoutService", "checkout"
        )
        self.assertNotIn("release", initial_calls)
        self.assertNotIn("reverse", initial_calls)

    def test_design_findings_become_normal_tasks_before_implementation(self) -> None:
        """An architecture finding omitted from tasks cannot influence implementation."""
        findings = fenced_json(FIXTURE / "docs/uml/findings.md")
        tasks = fenced_json(FIXTURE / "specs/F-001-checkout/tasks.md")
        self.assertEqual("design_time_before_tasks", findings["created_phase"])
        finding_ids = [item["id"] for item in findings["findings"]]
        self.assertEqual(["AF-001", "AF-002"], finding_ids)
        mapped = {item["finding_id"] for item in tasks["tasks"] if item["finding_id"]}
        self.assertEqual(set(finding_ids), mapped)
        self.assertEqual(["T001", "T002"], tasks["task_order"][:2])
        self.assertTrue(all(item["kind"] == "architecture_finding" for item in tasks["tasks"][:2]))


class AsBuiltArchitectureTests(unittest.TestCase):
    def test_component_and_flow_models_match_implemented_contracts(self) -> None:
        """A stale as-built interface or recovery edge must fail before integration review."""
        model = json.loads(fixture_read("project/docs/uml/as-built-model.json"))
        contract_return = method_return(
            PROJECT / "checkout/ports.py", "InventoryPort", "reserve"
        )
        implementation_return = method_return(
            PROJECT / "checkout/inventory.py", "Inventory", "reserve"
        )
        self.assertEqual("Reservation", contract_return)
        self.assertEqual(contract_return, implementation_return)
        self.assertEqual(contract_return, model["component"]["reserve_returns"])

        checkout_calls = called_attributes(
            PROJECT / "checkout/service.py", "CheckoutService", "checkout"
        )
        self.assertEqual(
            {"release", "reverse"},
            {"release", "reverse"} & checkout_calls,
        )
        self.assertEqual(
            ["inventory.release", "payment.reverse"],
            model["recovery_sequence"]["compensation"],
        )
        self.assertIn("Compensating", model["state"]["states"])

        diagrams = {
            "component": "flowchart LR",
            "success-sequence": "sequenceDiagram",
            "recovery-sequence": "sequenceDiagram",
            "state": "stateDiagram-v2",
        }
        for name, directive in diagrams.items():
            with self.subTest(diagram=name):
                content = fixture_read(f"project/docs/uml/{name}.mmd")
                self.assertRegex(content, r"%% Verified on: \d{4}-\d{2}-\d{2}")
                self.assertIn(directive, content)

        reconciliation = fenced_json(PROJECT / "docs/uml/reconciliation.md")
        self.assertEqual(
            {"AF-001": "code_corrected", "AF-002": "code_corrected"},
            {item["finding_id"]: item["disposition"] for item in reconciliation["differences"]},
        )

    def test_system_architect_derived_success_and_recovery_tests_pass(self) -> None:
        """Unit evidence cannot replace the two diagram-derived cross-component paths."""
        result = subprocess.run(
            ("python3", "-m", "unittest", "discover", "-s", "integration_tests", "-v"),
            cwd=PROJECT,
            text=True,
            capture_output=True,
        )
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        output = result.stdout + result.stderr
        self.assertIn("test_checkout_success_matches_success_sequence", output)
        self.assertIn("test_commit_failure_releases_inventory_and_reverses_payment", output)
        self.assertIn("OK", output)


class EvidenceMutationTests(unittest.TestCase):
    def test_weakened_supplied_test_is_rejected_even_after_fresh_review(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory) / "project"
            shutil.copytree(PROJECT, project)
            path = project / "integration_tests/test_checkout.py"
            tree = ast.parse(path.read_text())
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef) and node.name.startswith("test_"):
                    node.body = [ast.Pass()]
            path.write_text(ast.unparse(tree) + "\n")
            self.refresh_review_digest(project)
            with self.assertRaisesRegex(AssertionError, "supplied integration test"):
                assert_large_feature(project)

    def test_additional_real_integration_test_is_allowed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory) / "project"
            shutil.copytree(PROJECT, project)
            (project / "integration_tests/test_additional.py").write_text(
                "import unittest\n"
                "from checkout import CheckoutService, Inventory, OrderService, Payment\n"
                "class AdditionalCheckoutTest(unittest.TestCase):\n"
                "    def test_two_orders_have_distinct_reservations(self):\n"
                "        events = []\n"
                "        service = CheckoutService(OrderService(Inventory(events), events), Payment(events))\n"
                "        first = service.checkout('first')\n"
                "        second = service.checkout('second')\n"
                "        self.assertNotEqual(first.reservation_id, second.reservation_id)\n")
            self.refresh_review_digest(project)
            result = assert_large_feature(project)
            self.assertEqual(0, result["returncode"])
            self.assertIn("test_two_orders_have_distinct_reservations", result["output"])

    @staticmethod
    def refresh_review_digest(project):
        path = project / "evidence/final-review.md"
        path.write_text(re.sub(r'("reviewed_sha256": ")[a-f0-9]+',
                               lambda match: match.group(1) + evidence_digest(project),
                               path.read_text()))

    def check_rejected(self, mutate) -> None:
        with tempfile.TemporaryDirectory(prefix="large-feature-evidence-") as directory:
            fixture = Path(directory) / "fixture"
            shutil.copytree(FIXTURE, fixture)
            project = fixture / "project"
            mutate(project)
            with patch.object(sys.modules[__name__], "FIXTURE", fixture), patch.object(
                sys.modules[__name__], "PROJECT", project
            ):
                with self.assertRaises(AssertionError):
                    ConvergenceGateTests().test_converge_requires_every_architecture_integration_and_review_gate()

    def test_missing_artifact_rejects_convergence_despite_true_flags(self) -> None:
        for relative in (
            "docs/uml/reconciliation.md", "docs/uml/integration-test-plan.md",
            "evidence/final-review.md", "evidence/integration-results.md",
        ):
            with self.subTest(artifact=relative):
                self.check_rejected(lambda project: (project / relative).unlink())

    def test_empty_diagram_rejects_convergence_despite_valid_header(self) -> None:
        for name in ("component", "success-sequence", "recovery-sequence", "state"):
            def strip(project):
                path = project / f"docs/uml/{name}.mmd"
                path.write_text("\n".join(line for line in path.read_text().splitlines()
                    if line.startswith(("%%", "flowchart", "sequenceDiagram", "stateDiagram"))))
                self.refresh_review_digest(project)
            with self.subTest(diagram=name):
                self.check_rejected(strip)

    def test_actionable_review_rejects_convergence_despite_true_flags(self) -> None:
        def mutate(project):
            path = project / "evidence/final-review.md"
            path.write_text(path.read_text().replace("Status: clean", "Status: actionable"))
        self.check_rejected(mutate)

    def test_changed_code_invalidates_old_review(self) -> None:
        def mutate(project):
            path = project / "checkout/service.py"
            path.write_text(path.read_text() + "\n# Changed after review.\n")
        self.check_rejected(mutate)

    def test_semantic_drift_rejected_even_with_refreshed_review_digest(self) -> None:
        mutations = (
            ("docs/uml/success-sequence.mmd", "capture(order_id)", "reverse(order_id)"),
            ("docs/uml/recovery-sequence.mmd", "release(reservation)", "commit(reservation)"),
            ("docs/uml/state.mmd", "Paid --> Complete", "Reserved --> Complete"),
            ("docs/uml/component.mmd", "returns Reservation", "returns bool"),
        )
        for relative, before, after in mutations:
            def mutate(project):
                path = project / relative
                path.write_text(path.read_text().replace(before, after))
                self.refresh_review_digest(project)
            with self.subTest(artifact=relative):
                self.check_rejected(mutate)

    def test_fresh_integration_failure_rejected_despite_recorded_success(self) -> None:
        def mutate(project):
            path = project / "checkout/service.py"
            path.write_text(path.read_text().replace("self.payment.reverse(receipt)", "pass"))
            self.refresh_review_digest(project)
        self.check_rejected(mutate)

    def test_each_missing_gate_claim_rejects_real_evidence_validation(self) -> None:
        for field in ("as_built_reconciliation", "derived_success_test_passed",
                      "derived_recovery_test_passed", "clean_final_review", "fresh_verification"):
            for missing in (False, True):
                def mutate(project):
                    path = project / "evidence/convergence.json"
                    evidence = json.loads(path.read_text())
                    if missing:
                        del evidence[field]
                    else:
                        evidence[field] = False
                    path.write_text(json.dumps(evidence))
                with self.subTest(gate=field, missing=missing):
                    self.check_rejected(mutate)


class ConvergenceGateTests(unittest.TestCase):
    def test_converge_requires_every_architecture_integration_and_review_gate(self) -> None:
        """Removing any single gate must make convergence ineligible."""
        template = fenced_json(ROOT / "templates/uml/integration-test-plan.md")
        role = fenced_json(ROOT / "shared/agent-roles/system-architect.md")
        skill = fenced_json(ROOT / "skills/architecture-modeling/SKILL.md")
        required = {
            "as_built_reconciliation",
            "derived_success_test_passed",
            "derived_recovery_test_passed",
            "clean_final_review",
            "fresh_verification",
        }
        self.assertEqual(required, set(template["completion_requires"]))
        self.assertEqual(required, set(role["completion_requires"]))
        self.assertEqual(required, set(skill["system_integration_gate"]))
        self.assertEqual({"success": 1, "recovery": 1}, template["minimum_derived_tests"])

        evidence = json.loads(fixture_read("project/evidence/convergence.json"))
        fresh = assert_large_feature(PROJECT)
        self.assertEqual(0, fresh["returncode"])
        self.assertLessEqual(fresh["started_at"], fresh["completed_at"])
        self.assertTrue(all(evidence[field] is True for field in required))
        converge = " ".join(
            read("skills/speckit-converge/SKILL.md").lower().split()
        )
        for required_evidence in (
            "as-built architecture agrees",
            "integration flows pass",
            "review findings are resolved",
            "fresh verification passes",
        ):
            self.assertIn(required_evidence, converge)


if __name__ == "__main__":
    unittest.main()
