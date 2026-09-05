"""Release policy is strict about missing live evidence and ordered gates."""
from pathlib import Path
from datetime import datetime, timezone
import contextlib
import hashlib
import io
import json
import subprocess
import sys
import tempfile
import time
import unittest
from unittest.mock import patch

from scripts.release_check import assert_live_evidence, gate_commands, main, package_fingerprint, run_gate, validate_mode


class ReleaseCheckTests(unittest.TestCase):
    def test_routing_results_must_match_requested_host(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "package"
            cases = source / "evals/shared/triggers"
            cases.mkdir(parents=True)
            (cases / "case.json").write_text('{"id":"case"}')
            output = root / "codex-routing"
            output.mkdir()
            payload = {"status": "passed", "completed_at": datetime.now(timezone.utc).isoformat(),
                       "source_sha256": package_fingerprint(source), "host": "codex", "requested_cases": 1,
                       "results": [{"case_id": "case", "host": "claude", "status": "passed"}]}
            (output / "summary.json").write_text(json.dumps(payload))
            with self.assertRaisesRegex(ValueError, "host"):
                assert_live_evidence("codex-routing", root, source, "2000-01-01T00:00:00+00:00")

    def test_release_timeout_terminates_grandchild_before_return(self):
        with tempfile.TemporaryDirectory() as directory:
            marker = Path(directory) / "orphan"
            child = f"import time; from pathlib import Path; time.sleep(0.5); Path({str(marker)!r}).touch()"
            parent = f"import subprocess,sys,time; subprocess.Popen([sys.executable,'-c',{child!r}]); time.sleep(5)"
            result = run_gate("probe", [sys.executable, "-c", parent], Path(directory), 0.1)
            self.assertEqual("failed", result["status"])
            time.sleep(0.6)
            self.assertFalse(marker.exists(), "release timeout left an active grandchild")

    def test_release_timeout_is_forwarded_to_separate_eval_host_group(self):
        with tempfile.TemporaryDirectory() as directory:
            marker = Path(directory) / "detached-host-orphan"
            child = f"import time; from pathlib import Path; time.sleep(0.7); Path({str(marker)!r}).touch()"
            host = f"import subprocess,sys,time; subprocess.Popen([sys.executable,'-c',{child!r}]); time.sleep(5)"
            wrapper = ("import os,sys; from pathlib import Path; from scripts.run_host_evals import execute; "
                       f"execute([sys.executable,'-c',{host!r}],Path({directory!r}),dict(os.environ),5)")
            result = run_gate("nested-probe", [sys.executable, "-c", wrapper], Path(__file__).resolve().parents[1], 0.2)
            self.assertEqual("failed", result["status"])
            time.sleep(0.8)
            self.assertFalse(marker.exists(), "release timeout was not forwarded to the live host group")

    def test_zero_exit_without_fresh_live_summary_is_not_release_evidence(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            with self.assertRaises(ValueError):
                assert_live_evidence("codex-routing", root, root, "2026-09-05T00:00:00+00:00")
            output = root / "codex-routing"
            output.mkdir()
            (output / "summary.json").write_text(json.dumps({"status": "passed", "completed_at": "2026-09-04T00:00:00+00:00"}))
            with self.assertRaisesRegex(ValueError, "stale"):
                assert_live_evidence("codex-routing", root, root, "2026-09-05T00:00:00+00:00")

    def test_release_cannot_skip_live_evaluations(self):
        with self.assertRaises(ValueError):
            validate_mode(release=True, skip_live=True)
        validate_mode(release=False, skip_live=True)

    def test_gate_order_matches_approved_plan(self):
        gates = gate_commands(Path("/package"), Path("/evidence"), Path("/repo"), Path("/artifact.zip"))
        self.assertEqual([
            "portable-validation", "claude-strict-validation", "python-tests", "codex-routing",
            "claude-routing", "large-feature-both-hosts", "clean-install", "reproducible-package", "clean-working-tree",
        ], [name for name, command, cwd in gates])
        self.assertIn("--strict", gates[1][1])
        self.assertIn("both", gates[5][1])

    def test_failure_timeout_and_missing_tool_fail_gate_without_raw_output(self):
        with patch("scripts.release_check.run_bounded", return_value=subprocess.CompletedProcess(["host"], 1, "secret", "auth failed")):
            result = run_gate("live", ["host"], Path("/tmp"), 1)
            self.assertEqual("failed", result["status"])
            self.assertNotIn("secret", str(result))
        for error in (FileNotFoundError("missing"), subprocess.TimeoutExpired("host", 1)):
            with patch("scripts.release_check.run_bounded", side_effect=error):
                self.assertEqual("failed", run_gate("live", ["host"], Path("/tmp"), 1)["status"])

    def test_live_failure_stops_release_and_records_commit_package_binding(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "package"
            source.mkdir()
            def package(source, archive):
                archive.write_bytes(b"immutable-package")
                return {"source_commit": "a" * 40, "sha256": hashlib.sha256(archive.read_bytes()).hexdigest()}
            seen = []
            def gate(name, *args, **kwargs):
                seen.append(name)
                return {"name": name, "status": "failed" if name == "codex-routing" else "passed"}
            with patch("scripts.release_check.build_package", side_effect=package), \
                 patch("scripts.release_check.extract_package", return_value=source), \
                 patch("scripts.release_check.source_commit", return_value="a" * 40), \
                 patch("scripts.release_check.run_gate", side_effect=gate), contextlib.redirect_stdout(io.StringIO()):
                result = main(["--release", "--root", str(root), "--output-dir", str(root / "evidence")])
            self.assertEqual(1, result)
            self.assertEqual("codex-routing", seen[-1])
            report = json.loads((root / "evidence/release.json").read_text())
            self.assertFalse(report["release_eligible"])
            self.assertEqual("failed", report["status"])
            self.assertEqual("a" * 40, report["source_commit"])
            self.assertIn("sha256", report)

    def test_any_gate_mutating_extracted_source_fails_before_next_gate(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "package"
            source.mkdir()
            (source / "source.py").write_text("original")
            def package(repo, archive):
                archive.write_bytes(b"immutable-package")
                return {"source_commit": "a" * 40, "sha256": hashlib.sha256(archive.read_bytes()).hexdigest()}
            def gate(name, *args, **kwargs):
                (source / "source.py").write_text("mutated during validation")
                return {"name": name, "status": "passed"}
            with patch("scripts.release_check.build_package", side_effect=package), \
                 patch("scripts.release_check.extract_package", return_value=source), \
                 patch("scripts.release_check.source_commit", return_value="a" * 40), \
                 patch("scripts.release_check.run_gate", side_effect=gate), contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(1, main(["--skip-live", "--root", str(root), "--output-dir", str(root / "evidence")]))
            report = json.loads((root / "evidence/release.json").read_text())
            self.assertEqual(1, len(report["gates"]))
            self.assertEqual("failed", report["gates"][0]["status"])
