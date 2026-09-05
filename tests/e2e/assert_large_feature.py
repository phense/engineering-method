#!/usr/bin/env python3
"""Host architecture evidence supplements the reusable checkout fixture oracle."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import re
import shlex
import sys
from datetime import datetime, timezone

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from scripts.run_host_evals import EvalFailure
from tests.large_feature_evidence import assert_large_feature, evidence_digest, supplied_test_digests, pre_review_large_feature

PHASES = ("specify", "plan", "findings", "tasks", "slices", "as-built",
          "integration", "converge", "review", "verification")
ARTIFACTS = {
    "specify": ["specs/F-001-checkout/spec.md"],
    "plan": ["specs/F-001-checkout/plan.md"],
    "findings": ["docs/uml/findings.md", "docs/uml/design-component.mmd",
                 "docs/uml/design-recovery-sequence.mmd", "docs/uml/design-state.mmd"],
    "tasks": ["specs/F-001-checkout/tasks.md"],
    "slices": ["reports/slices.json"],
    "as-built": ["docs/uml/reconciliation.md", "docs/uml/component.mmd",
                 "docs/uml/success-sequence.mmd", "docs/uml/recovery-sequence.mmd", "docs/uml/state.mmd"],
    "integration": ["evidence/integration-results.md", "docs/uml/integration-test-plan.md"],
    "converge": ["evidence/convergence.json"],
    "review": ["evidence/final-review.md"],
    "verification": ["evidence/integration-results.md"],
}
SKILLS = {"speckit-specify", "speckit-plan", "architecture-modeling", "speckit-tasks",
          "orchestrated-implementation", "speckit-converge", "requesting-code-review",
          "verification-before-completion"}

def need(condition, message):
    if not condition:
        raise EvalFailure(message)

def shell_arguments(command):
    try:
        words = shlex.split(command)
        if words and Path(words[0]).name in ("sh", "bash", "zsh") and len(words) == 3 and words[1] in ("-c", "-lc"):
            words = shlex.split(words[2])
        return words
    except ValueError:
        return []

def review_object(text):
    match = re.search(r"```json\s*\n(.*?)\n```", text, re.DOTALL)
    try:
        value = json.loads(match.group(1) if match else text)
        return value if isinstance(value, dict) else {}
    except ValueError:
        return {}

def history(project):
    path = project / "phase-evidence.jsonl"
    return [json.loads(line) for line in path.read_text().splitlines()] if path.exists() else []

def snapshot(project):
    paths = {}
    for prefix in ("initial", "checkout", "integration_tests", "specs", "docs/uml", "evidence", "reports"):
        for path in (project / prefix).rglob("*"):
            if path.is_file() and "__pycache__" not in path.parts:
                paths[str(path.relative_to(project))] = hashlib.sha256(path.read_bytes()).hexdigest()
    return paths

def checkpoint(project, phase):
    project = project.resolve()
    records = history(project)
    need(len(records) < len(PHASES) and PHASES[len(records)] == phase, "phase_order")
    if phase in ("specify", "plan", "findings", "tasks"):
        need(not any((project / "checkout").glob("*.py")), "implementation_before_findings_and_tasks")
    for relative in ARTIFACTS[phase]:
        path = project / relative
        need(path.is_file() and path.stat().st_size > 0, "missing_phase_artifact:" + relative)
    if phase == "findings":
        text = (project / "docs/uml/findings.md").read_text()
        need(all(term in text for term in ("AF-001", "AF-002", "Reservation", "bool")),
             "initial_interface_finding_missing")
        need("release" in text.lower() and ("reverse" in text.lower() or "reversal" in text.lower()),
             "initial_compensation_finding_missing")
    if phase == "tasks":
        text = (project / "specs/F-001-checkout/tasks.md").read_text()
        need(all(term in text for term in ("AF-001", "AF-002", "T001", "T002", "### Slice")),
             "stable_finding_tasks_missing")
    if phase == "verification":
        assert_large_feature(project)
    files = snapshot(project)
    need(all(files.get(relative) == digest for relative, digest in supplied_test_digests().items()),
         "modified_or_missing_supplied_integration_test")
    record = {"phase": phase, "recorded_at": datetime.now(timezone.utc).isoformat(), "files": files}
    with (project / "phase-evidence.jsonl").open("a") as stream:
        stream.write(json.dumps(record, sort_keys=True) + "\n")
    return record

def is_checkpoint_command(words, phase, project, assertion):
    if len(words) < 4 or not re.fullmatch(r"python(?:\d+(?:\.\d+)*)?", Path(words[0]).name):
        return False
    def resolved(value):
        path = Path(value)
        return (path if path.is_absolute() else project / path).resolve()
    if resolved(words[1]) != assertion.resolve():
        return False
    options = {}
    remaining = iter(words[2:])
    for word in remaining:
        key, separator, value = word.partition("=")
        if key not in ("--project", "--checkpoint") or key in options:
            return False
        options[key] = value if separator else next(remaining, None)
    return (options.get("--checkpoint") == phase and bool(options.get("--project"))
            and resolved(options["--project"]) == project.resolve())

def assert_host_run(project, transcript, *, assertion=None):
    assertion = Path(assertion) if assertion is not None else Path(__file__)
    records = history(project)
    need([row["phase"] for row in records] == list(PHASES), "incomplete_phase_history")
    command_positions = [i for i, tool in enumerate(transcript["tools"])
                         if tool["name"] in ("command", "Bash")]
    command_tools = [transcript["tools"][i] for i in command_positions]
    arguments = [shell_arguments(tool["input"] if isinstance(tool["input"], str)
                                 else tool["input"].get("command", "")) for tool in command_tools]
    checkpoint_positions = {}
    cursor = 0
    for phase in PHASES:
        matches = [i for i in range(cursor, len(arguments))
                   if is_checkpoint_command(arguments[i], phase, project, assertion)]
        need(matches, "missing_tool_checkpoint:" + phase)
        recorded = records[PHASES.index(phase)]
        need(json.dumps(recorded, sort_keys=True) in command_tools[matches[0]].get("output", ""),
             "checkpoint_lacks_observed_snapshot:" + phase)
        cursor = matches[0] + 1
        checkpoint_positions[phase] = command_positions[matches[0]]
    need(SKILLS.issubset(transcript["skills"]), "missing_workflow_skill_evidence")
    need(transcript.get("reviewers"), "missing_independent_reviewer_tool_evidence")
    findings_position = checkpoint_positions["findings"]
    initial_reads = [tool for tool in transcript["tools"][:findings_position]
                     if "initial/" in str(tool["input"]) and tool.get("output")
                     and (tool["name"] == "Read" or re.search(r"\b(cat|sed|read_text)\b", str(tool["input"])))]
    need(initial_reads, "initial_defects_not_inspected_before_findings")
    initial = Path(__file__).resolve().parents[1] / "fixtures/large-feature/initial"
    for path in initial.glob("*.py"):
        relative = "initial/" + path.name
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        need(all(row["files"].get(relative) == digest for row in records), "modified_initial_evidence")
    for phase in ("specify", "plan", "findings", "tasks"):
        row = records[PHASES.index(phase)]
        need(not any(path.startswith("checkout/") for path in row["files"]),
             "implementation_before_findings_and_tasks")
    for row in records:
        need(all(row["files"].get(relative) == digest for relative, digest in supplied_test_digests().items()),
             "modified_or_missing_supplied_integration_test")
        for relative in ARTIFACTS[row["phase"]]:
            need(relative in row["files"], "missing_snapshot_artifact")
    # Approved findings/tasks must survive implementation with stable identities.
    for phase in ("findings", "tasks"):
        relative = ARTIFACTS[phase][0]
        current = hashlib.sha256((project / relative).read_bytes()).hexdigest()
        need(records[PHASES.index(phase)]["files"][relative] == current, "rewritten_design_evidence")
    reports = json.loads((project / "reports/slices.json").read_text())
    need(isinstance(reports, list) and len(reports) >= 1, "missing_slice_reports")
    for report in reports:
        for key in ("slice_id", "owned_paths", "interfaces", "test_command", "test_output", "review_path", "root_cause"):
            need(report.get(key), "missing_slice_evidence:" + key)
        need(isinstance(report["owned_paths"], list) and isinstance(report["interfaces"], list),
             "malformed_slice_ownership")
        for relative in report["owned_paths"]:
            owned = (project / relative).resolve()
            need(owned.is_relative_to(project.resolve()) and owned.exists(), "invalid_slice_owned_path")
        review = (project / report["review_path"]).resolve()
        need(review.is_relative_to(project.resolve()) and review.is_file(), "missing_slice_review")
        verdict = review_object(review.read_text())
        need(verdict.get("status") == "clean" and verdict.get("actionable_findings") == [],
             "actionable_slice_review")
        reviewed_files = {relative: hashlib.sha256((project / relative).read_bytes()).hexdigest()
                          for relative in report["owned_paths"] if (project / relative).is_file()}
        need(verdict.get("reviewed_files") == reviewed_files and reviewed_files,
             "stale_slice_review")
        need(any(isinstance(reviewer, dict) and report["review_path"] in reviewer.get("prompt", "")
                 and review_object(reviewer.get("output", "")) == verdict
                 for reviewer in transcript["reviewers"]), "slice_review_lacks_completed_agent_evidence")
        test_runs = [tool for tool in transcript["tools"]
                     if shell_arguments(report["test_command"]) == shell_arguments(
                         tool["input"] if isinstance(tool["input"], str) else tool["input"].get("command", ""))]
        need(shell_arguments(report["test_command"])[:3] in (["python3", "-m", "unittest"], [sys.executable, "-m", "unittest"])
             and any(report["test_output"].strip() == tool.get("output", "").strip() for tool in test_runs),
             "slice_tests_lack_tool_evidence")
    final_path = project / "evidence/final-review.md"
    final = review_object(final_path.read_text())
    scope = {relative: digest for relative, digest in snapshot(project).items()
             if relative.startswith(("checkout/", "integration_tests/", "docs/uml/"))}
    need(final.get("review_kind") == "system-architect-final" and final.get("status") == "clean"
         and final.get("actionable_findings") == [] and final.get("reviewed_files") == scope
         and final.get("reviewed_sha256") == evidence_digest(project),
         "missing_or_stale_final_system_architect_verdict")
    review_position = checkpoint_positions["review"]
    integration_position = checkpoint_positions["integration"]
    need(any(isinstance(reviewer, dict) and "system-architect" in reviewer.get("prompt", "").lower()
             and "evidence/final-review.md" in reviewer.get("prompt", "")
             and review_object(reviewer.get("output", "")) == final
             and integration_position < reviewer.get("tool_position", -1) <= review_position
             for reviewer in transcript["reviewers"]),
         "missing_completed_final_system_architect_review")
    need(records[PHASES.index("review")]["files"]["evidence/final-review.md"]
         == hashlib.sha256(final_path.read_bytes()).hexdigest(), "final_review_changed_after_checkpoint")
    fresh = assert_large_feature(project)
    return {"status": "passed", "phases": list(PHASES), "verified_sha256": fresh["verified_sha256"],
            "tests_returncode": fresh["returncode"], "completed_at": fresh["completed_at"]}

def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", type=Path, required=True)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--checkpoint", choices=PHASES)
    mode.add_argument("--transcript", type=Path)
    mode.add_argument("--refresh-review-digest", action="store_true")
    mode.add_argument("--pre-review", action="store_true",
                      help="run fresh machine checks only; never grants final acceptance")
    args = parser.parse_args(argv)
    if args.refresh_review_digest:
        path = args.project / "evidence/final-review.md"
        text = path.read_text()
        text, count = re.subn(r'("reviewed_sha256": ")[a-f0-9]+',
                             lambda m: m[1] + evidence_digest(args.project), text)
        need(count == 1, "missing_review_digest_field")
        path.write_text(text)
        return 0
    if args.pre_review:
        print(json.dumps(pre_review_large_feature(args.project)))
    elif args.checkpoint:
        print(json.dumps(checkpoint(args.project, args.checkpoint), sort_keys=True))
    elif args.transcript:
        print(json.dumps(assert_host_run(args.project, json.loads(args.transcript.read_text()))))
    else:
        assert_large_feature(args.project)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
