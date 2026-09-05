"""Architecture host acceptance must reject fabricated or incomplete histories."""
from pathlib import Path
import json
import hashlib
from copy import deepcopy
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from scripts.run_host_evals import EvalFailure
from tests.e2e.assert_large_feature import checkpoint, assert_host_run, PHASES, SKILLS
from tests.large_feature_evidence import evidence_digest


class ArchitectureHostTests(unittest.TestCase):
    def test_completed_fixture_requires_observed_snapshots_and_review(self):
        """Real checkpoint output binds phase history; deleting it must fail acceptance."""
        repository = Path(__file__).resolve().parents[1]
        fixture = repository / "tests/fixtures/large-feature"
        script = repository / "tests/e2e/assert_large_feature.py"
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            shutil.copytree(fixture / "initial", project / "initial")
            shutil.copytree(fixture / "project/integration_tests", project / "integration_tests")
            specs = project / "specs/F-001-checkout"
            specs.mkdir(parents=True)
            (specs / "spec.md").write_text("Approved checkout behavior and recovery requirements.")
            (specs / "plan.md").write_text("Order, Inventory, Payment, Checkout ownership and contracts.")
            shutil.copytree(fixture / "docs/uml", project / "docs/uml")
            shutil.copy2(fixture / "specs/F-001-checkout/tasks.md", specs / "tasks.md")
            transcript = {"tools": [{"name": "command", "input": "cat initial/inventory.py", "output": (project / "initial/inventory.py").read_text()}],
                          "skills": list(SKILLS), "reviewers": []}
            for phase in PHASES:
                if phase == "slices":
                    shutil.copytree(fixture / "project", project, dirs_exist_ok=True)
                    (project / "reports").mkdir()
                    verdict = {"status": "clean", "actionable_findings": [], "reviewed_files": {
                        "checkout/service.py": hashlib.sha256((project / "checkout/service.py").read_bytes()).hexdigest()}}
                    (project / "reports/review.md").write_text(json.dumps(verdict))
                    transcript["reviewers"].append({"id": "independent-review", "prompt": "Read-only review reports/review.md", "output": json.dumps(verdict)})
                    reports = [{"slice_id": "S1", "owned_paths": ["checkout/service.py"],
                                "interfaces": ["InventoryPort"], "test_command": "python3 -m unittest discover -s integration_tests -v",
                                "test_output": "Ran 2 tests", "review_path": "reports/review.md",
                                "root_cause": "Mismatch and absent compensation corrected."}]
                    (project / "reports/slices.json").write_text(json.dumps(reports))
                    test = subprocess.run([sys.executable, "-B", "-m", "unittest", "discover", "-s", "integration_tests", "-v"], cwd=project, capture_output=True, text=True, check=True)
                    reports[0]["test_output"] = test.stdout + test.stderr
                    (project / "reports/slices.json").write_text(json.dumps(reports))
                    transcript["tools"].append({"name": "command", "input": reports[0]["test_command"], "output": test.stdout + test.stderr})
                    review = project / "evidence/final-review.md"
                    review.write_text(re.sub(r'("reviewed_sha256": ")[a-f0-9]+',
                                            lambda m: m[1] + evidence_digest(project), review.read_text()))
                if phase == "review":
                    reviewed_files = {}
                    for prefix in ("checkout", "integration_tests", "docs/uml"):
                        for path in (project / prefix).rglob("*"):
                            if path.is_file() and "__pycache__" not in path.parts:
                                reviewed_files[str(path.relative_to(project))] = hashlib.sha256(path.read_bytes()).hexdigest()
                    final = {"review_kind": "system-architect-final", "status": "clean", "actionable_findings": [],
                             "reviewed_files": reviewed_files, "reviewed_sha256": evidence_digest(project)}
                    response = "```json\n" + json.dumps(final) + "\n```"
                    (project / "evidence/final-review.md").write_text("Status: clean\n\n" + response)
                    transcript["reviewers"].append({"id": "final-architect", "prompt": "Read-only system-architect review; write evidence/final-review.md",
                                                  "output": response, "tool_position": len(transcript["tools"])})
                command = [sys.executable, str(script), "--project", str(project), "--checkpoint", phase]
                result = subprocess.run(command, capture_output=True, text=True, check=True)
                transcript["tools"].append({"name": "command", "input": " ".join(command), "output": result.stdout})
            without_final_review = deepcopy(transcript)
            without_final_review["reviewers"] = [reviewer for reviewer in transcript["reviewers"]
                                                if "system-architect" not in reviewer["prompt"]]
            with self.assertRaisesRegex(EvalFailure, "final_system_architect"):
                assert_host_run(project, without_final_review)
            self.assertEqual("passed", assert_host_run(project, transcript)["status"])
            broken = deepcopy(transcript)
            test_tool = next(tool for tool in broken["tools"] if tool["input"].startswith("python3 -m unittest"))
            test_tool["input"] = "echo " + test_tool["input"]
            with self.assertRaisesRegex(EvalFailure, "slice_tests"):
                assert_host_run(project, broken)
            broken = deepcopy(transcript)
            broken["tools"].append(broken["tools"].pop(0))
            with self.assertRaisesRegex(EvalFailure, "before_findings"):
                assert_host_run(project, broken)
            review = project / "reports/review.md"
            original = review.read_text()
            review.write_text("NOT CLEAN: Critical defect\n")
            with self.assertRaisesRegex(EvalFailure, "slice_review"):
                assert_host_run(project, transcript)
            review.write_text(original)
            transcript["tools"][-1]["output"] = "claimed checkpoint success"
            with self.assertRaisesRegex(EvalFailure, "observed_snapshot"):
                assert_host_run(project, transcript)

    def test_incomplete_recorded_run_is_not_accepted(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            with self.assertRaisesRegex(EvalFailure, "phase"):
                assert_host_run(root, {"tools": [], "skills": []})

    def test_implementation_cannot_precede_findings(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "checkout").mkdir()
            (root / "checkout/service.py").write_text("# premature implementation\n")
            with self.assertRaisesRegex(EvalFailure, "before_findings"):
                checkpoint(root, "specify")

    def test_checkpoint_order_is_enforced(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            with self.assertRaisesRegex(EvalFailure, "phase_order"):
                checkpoint(root, "tasks")

    def test_missing_phase_artifact_cannot_be_recorded(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            with self.assertRaisesRegex(EvalFailure, "artifact"):
                checkpoint(root, "specify")
