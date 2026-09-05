"""Ordered release gates over a committed package, with explicit live failures."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile

try:
    from .clean_install import extract_package, isolated_environment
    from .package_plugin import build_package, source_commit
    from .process_control import run_bounded
except ImportError:
    from clean_install import extract_package, isolated_environment
    from package_plugin import build_package, source_commit
    from process_control import run_bounded


LIVE_GATES = {"codex-routing", "claude-routing", "large-feature-both-hosts"}


def package_fingerprint(root: Path) -> str:
    excluded = {".git", ".engineering-method", ".superpowers", ".worktrees", "__pycache__"}
    data = {str(path.relative_to(root)): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in sorted(root.rglob("*")) if path.is_file()
            and not excluded.intersection(path.relative_to(root).parts)}
    return hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()


def assert_live_evidence(name: str, evidence: Path, package_root: Path, started_at: str,
                         expected_source_sha256: str | None = None) -> dict:
    output = evidence / ("large-feature" if name == "large-feature-both-hosts" else name)
    path = output / "summary.json"
    try:
        payload = json.loads(path.read_text())
        if payload.get("status") != "passed":
            raise ValueError("live summary does not report success")
        completed = datetime.fromisoformat(payload["completed_at"])
        if completed < datetime.fromisoformat(started_at) or completed > datetime.now(timezone.utc):
            raise ValueError("live summary is stale or future dated")
        if payload.get("source_sha256") != (expected_source_sha256 or package_fingerprint(package_root)):
            raise ValueError("live summary does not match package source")
        results = payload["results"]
        if not results or any(result.get("status") != "passed" for result in results):
            raise ValueError("live summary contains missing or failing results")
        if name == "large-feature-both-hosts":
            if len(results) != 2 or {result.get("host") for result in results} != {"codex", "claude"}:
                raise ValueError("large-feature evidence must cover both hosts")
        else:
            host = name.split("-")[0]
            expected = {json.loads(case.read_text())["id"]
                        for case in (package_root / "evals/shared/triggers").glob("*.json")}
            if not expected or payload.get("host") != host or any(result.get("host") != host for result in results) \
                    or payload.get("requested_cases") != len(expected) \
                    or len(results) != len(expected) or {result.get("case_id") for result in results} != expected:
                raise ValueError("routing evidence must cover the complete host trigger matrix")
    except (OSError, KeyError, TypeError, json.JSONDecodeError) as error:
        raise ValueError("live gate did not produce valid complete summary evidence") from error
    return {"summary": str(path), "summary_sha256": hashlib.sha256(path.read_bytes()).hexdigest()}


def validate_mode(*, release: bool, skip_live: bool) -> None:
    if release and skip_live:
        raise ValueError("release mode requires successful live evaluations on both hosts; --skip-live is forbidden")


def gate_commands(package_root: Path, evidence: Path, source_root: Path, archive: Path):
    python = sys.executable
    return [
        ("portable-validation", [python, str(package_root / "scripts/validate-plugin")], package_root),
        ("claude-strict-validation", ["claude", "plugin", "validate", "--strict", str(package_root)], evidence),
        ("python-tests", [python, "-m", "unittest", "discover", "-s", "tests", "-v"], package_root),
        ("codex-routing", [python, str(package_root / "tests/e2e/run-codex-evals"), "--output-dir", str(evidence / "codex-routing")], package_root),
        ("claude-routing", [python, str(package_root / "tests/e2e/run-claude-evals"), "--output-dir", str(evidence / "claude-routing")], package_root),
        ("large-feature-both-hosts", [python, str(package_root / "tests/e2e/run-large-feature-eval"), "--host", "both", "--output-dir", str(evidence / "large-feature")], package_root),
        ("clean-install", [python, str(package_root / "tests/e2e/test-clean-install"), "--package", str(archive), "--output", str(evidence / "clean-install.json")], package_root),
        ("reproducible-package", [python, str(package_root / "scripts/package-plugin"), "--root", str(source_root), "--check", "--output", str(archive)], package_root),
        ("clean-working-tree", [python, str(package_root / "scripts/release-check"), "--assert-clean", "--root", str(source_root)], source_root),
    ]


def run_gate(name, command, cwd, timeout, *, env=None) -> dict:
    started = datetime.now(timezone.utc).isoformat()
    evidence = {"name": name, "command": command, "cwd": str(cwd), "started_at": started}
    try:
        result = run_bounded(command, cwd=cwd, env=env, timeout=timeout)
        output = result.stdout + result.stderr
        if isinstance(output, str):
            output = output.encode()
        evidence.update(status="passed" if result.returncode == 0 else "failed",
                        returncode=result.returncode, output_sha256=hashlib.sha256(output).hexdigest(),
                        output_bytes=len(output))
    except (OSError, subprocess.TimeoutExpired) as error:
        evidence.update(status="failed", error=type(error).__name__)
    evidence["completed_at"] = datetime.now(timezone.utc).isoformat()
    return evidence


def assert_clean(root: Path) -> None:
    for args in (("diff", "--check"), ("diff", "--cached", "--check"),
                 ("status", "--porcelain=v1", "--untracked-files=all")):
        result = subprocess.run(["git", "-C", str(root), *args], capture_output=True, timeout=30)
        if result.returncode or result.stdout:
            raise ValueError("Git working tree/index is not clean or contains whitespace errors")


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--release", action="store_true")
    parser.add_argument("--skip-live", action="store_true")
    parser.add_argument("--assert-clean", action="store_true", help=argparse.SUPPRESS)
    parser.add_argument("--timeout", type=int, default=1800, help="maximum seconds per release gate")
    parser.add_argument("--codex-auth-home", type=Path)
    parser.add_argument("--claude-auth-home", type=Path)
    args = parser.parse_args(argv)
    try:
        validate_mode(release=args.release, skip_live=args.skip_live)
        if args.assert_clean:
            assert_clean(args.root)
            return 0
        if args.timeout <= 0:
            raise ValueError("timeout must be positive")
        directory = (args.output_dir or Path(tempfile.mkdtemp(prefix="em-release-evidence-"))).resolve()
        directory.mkdir(parents=True, exist_ok=True)
        if (directory / "release.json").exists():
            raise ValueError("output directory already contains release evidence; select a fresh directory")
        root = args.root.resolve()
        archive = directory / "engineering-method.zip"
        package = build_package(root, archive)
        report = {"status": "running", "release_mode": args.release, "release_eligible": False,
                  "started_at": datetime.now(timezone.utc).isoformat(), **package, "gates": []}
        with tempfile.TemporaryDirectory(prefix="em-release-package-") as temporary:
            package_root = extract_package(archive, Path(temporary) / "extracted")
            report["source_sha256"] = package_fingerprint(package_root)
            native_env = isolated_environment(Path(temporary) / "native-home")
            for name, command, cwd in gate_commands(package_root, directory, root, archive):
                if name in LIVE_GATES and args.skip_live:
                    report["gates"].append({"name": name, "status": "skipped", "reason": "development --skip-live"})
                    continue
                if name in {"codex-routing", "claude-routing"}:
                    home = args.codex_auth_home if name == "codex-routing" else args.claude_auth_home
                    if home:
                        command.extend(["--auth-home", str(home.resolve())])
                if name == "large-feature-both-hosts":
                    for host in ("codex", "claude"):
                        home = getattr(args, host + "_auth_home")
                        if home:
                            command.extend([f"--{host}-auth-home", str(home.resolve())])
                result = run_gate(name, command, cwd, args.timeout,
                                  env=native_env if name == "claude-strict-validation" else None)
                if package_fingerprint(package_root) != report["source_sha256"]:
                    result.update(status="failed", error="gate mutated extracted package source")
                if result["status"] == "passed" and name in LIVE_GATES:
                    try:
                        result.update(assert_live_evidence(name, directory, package_root, result["started_at"],
                                                           report["source_sha256"]))
                    except ValueError as error:
                        result.update(status="failed", error=str(error))
                report["gates"].append(result)
                (directory / "release.json").write_text(json.dumps(report, indent=2) + "\n")
                print(f"{name}: {result['status']}", flush=True)
                if result["status"] != "passed":
                    break
        complete = len(report["gates"]) == 9 and all(
            gate["status"] == "passed" or (args.skip_live and gate["status"] == "skipped")
            for gate in report["gates"])
        if source_commit(root) != package["source_commit"] or hashlib.sha256(archive.read_bytes()).hexdigest() != package["sha256"]:
            complete = False
            report["error"] = "source commit/package changed during gates"
        report["release_eligible"] = complete and not args.skip_live
        report["status"] = "passed" if report["release_eligible"] else "development-only" if complete else "failed"
        report["completed_at"] = datetime.now(timezone.utc).isoformat()
        (directory / "release.json").write_text(json.dumps(report, indent=2) + "\n")
        print(json.dumps({"status": report["status"], "release_eligible": report["release_eligible"],
                          "evidence": str(directory / "release.json")}))
        return 0 if complete else 1
    except (ValueError, OSError, subprocess.TimeoutExpired) as error:
        print(json.dumps({"status": "failed", "error": str(error)}))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
