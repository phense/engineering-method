#!/usr/bin/env python3
"""Isolated, fail-closed CLI behavioral evaluations; expectations never enter prompts."""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import signal
import subprocess
import sys
import tempfile
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
AUTH_ERROR = re.compile(r"not logged in|authentication (?:required|failed)|please (?:log ?in|sign in)|oauth.*(?:expired|failed)|invalid api key", re.I)
SKILL_PATH = re.compile(r"(?:^|[/\\\s])skills[/\\]([a-z][a-z0-9-]+)[/\\]SKILL\.md")
DECISION_SCHEMA = {"type": "object", "properties": {"primary": {"type": "string"},
                   "supporting": {"type": "array", "items": {"type": "string"}}},
                   "required": ["primary", "supporting"], "additionalProperties": False}

def private_transcript(path, text):
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(descriptor, "w") as stream:
        stream.write(text)
    os.chmod(path, 0o600)

def normalize_skill(name):
    if isinstance(name, str) and name.startswith("engineering-method:"):
        return name[len("engineering-method:"):]
    if isinstance(name, str) and ":" in name:
        raise EvalFailure("unexpected_skill_namespace")
    return name

def model_policy(host, plugin=ROOT):
    text = (plugin / f"shared/platform/{host}.md").read_text()
    return json.loads(re.search(r"```json\n(.*?)\n```", text, re.DOTALL).group(1))

def model_effort(host, model, plugin=ROOT):
    for choices in model_policy(host, plugin)["roles"].values():
        for choice in choices:
            if choice["model"] == model:
                return choice["effort"]
    return None

class EvalFailure(RuntimeError):
    def __init__(self, message, transcript=""):
        super().__init__(message)
        self.transcript = transcript

def failure_category(text):
    """Allowlisted diagnostics keep native error context without copying secrets."""
    if AUTH_ERROR.search(text):
        return "authentication"
    patterns = (
        (r"unknown (?:option|argument)|unrecognized (?:option|argument)", "unsupported_cli_option"),
        (r"invalid.*mcp|mcp.*invalid|mcp.*parse", "invalid_mcp_configuration"),
        (r"permission.prompt|permission-prompts", "permission_prompt_configuration"),
        (r"stream-json.*verbose|verbose.*stream-json", "stream_json_requires_verbose"),
        (r"cannot be launched inside|nested.*session", "nested_host_session"),
        (r"operation not permitted|permission denied|eacces|sandbox", "host_permission_denied"),
        (r"keychain", "native_keychain_failure"),
        (r"enotfound|econnrefused|connection|network|fetch failed|dns", "network_failure"),
        (r"model.*(?:unavailable|not found|not supported|does not exist)", "model_unavailable"),
        (r"max.?budget|budget.*exceed", "budget_exceeded"),
    )
    for pattern, category in patterns:
        if re.search(pattern, text, re.I):
            return category
    return "uncategorized_native_error"

def diagnostic_events(text):
    """Keep event structure and skill names; never persist arbitrary host text."""
    records = []
    allowed = {path.name for path in (ROOT / "skills").iterdir() if path.is_dir()} | {"native-focused-edit"}
    for line in text.splitlines():
        try:
            event = json.loads(line)
            if not isinstance(event, dict):
                raise ValueError()
        except ValueError:
            records.append({"type": "malformed", "bytes": len(line.encode())})
            continue
        item = event.get("item", {})
        malformed_item = not isinstance(item, dict)
        if malformed_item:
            item = {}
        records.append({"type": event.get("type"), "subtype": event.get("subtype"),
                        "item_type": item.get("type"), "exit_code": item.get("exit_code"),
                        "is_error": event.get("is_error"), "malformed_item": malformed_item,
                        "skill_paths": sorted(set(SKILL_PATH.findall(json.dumps(event))))})
        final = item.get("text") if item.get("type") == "agent_message" else event.get("result")
        if isinstance(event.get("structured_output"), dict):
            final = json.dumps(event["structured_output"])
        if isinstance(final, str):
            try:
                decision = json.loads(re.sub(r"^\s*```(?:json)?\s*|\s*```\s*$", "", final))
                if isinstance(decision, dict):
                    primary = normalize_skill(decision.get("primary"))
                    supporting = decision.get("supporting", [])
                    if isinstance(supporting, list):
                        supporting = [normalize_skill(name) for name in supporting]
                    records[-1]["decision"] = {
                        "primary": primary if isinstance(primary, str) and primary in allowed else "unrecognized",
                        "supporting": [name if isinstance(name, str) and name in allowed else "unrecognized"
                                       for name in supporting] if isinstance(supporting, list) else ["malformed"],
                    }
            except (ValueError, TypeError, EvalFailure):
                pass
    return records

def execute(command, cwd, env, timeout):
    try:
        process = subprocess.Popen(command, cwd=cwd, env=env, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE, text=True, start_new_session=True)
    except FileNotFoundError as exc:
        raise EvalFailure("missing_command") from exc
    def cancel(signum, frame):
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        process.wait()
        # Termination must exit the wrapper, never advance a both-host loop.
        raise SystemExit(128 + signum)
    previous_term = signal.signal(signal.SIGTERM, cancel)
    try:
        try:
            stdout, stderr = process.communicate(timeout=timeout)
        except subprocess.TimeoutExpired as exc:
            os.killpg(process.pid, signal.SIGKILL)
            stdout, stderr = process.communicate()
            raise EvalFailure("timeout", stdout) from exc
    finally:
        signal.signal(signal.SIGTERM, previous_term)
    if AUTH_ERROR.search(stdout + stderr):
        raise EvalFailure("authentication", stdout)
    if process.returncode:
        raise EvalFailure(f"host_exit:{process.returncode}:" + failure_category(stdout + stderr), stdout)
    return stdout

def parse_transcript(host, text):
    try:
        return _parse_transcript(host, text)
    except EvalFailure:
        raise
    except Exception as exc:
        # An unanticipated native shape is a failed evaluation, never evidence.
        raise EvalFailure("malformed_native_envelope:" + type(exc).__name__, text) from exc

def typed(value, expected, label):
    if not isinstance(value, expected):
        raise EvalFailure("malformed_" + label)
    return value

def _parse_transcript(host, text):
    events, skills, tools, pending, reviewers = [], set(), [], {}, []
    invoked, review_assignments = set(), {}
    final, terminal = None, False
    try:
        for line in text.splitlines():
            if line.strip():
                event = json.loads(line)
                if not isinstance(event, dict):
                    raise ValueError("event must be object")
                events.append(event)
    except (ValueError, TypeError) as exc:
        raise EvalFailure("malformed_jsonl") from exc
    for event in events:
        typed(event.get("type"), str, "event_type")
        if host == "codex":
            if event.get("type") in ("error", "turn.failed"):
                raise EvalFailure("host_error")
            terminal |= event.get("type") == "turn.completed"
            item = event.get("item", {})
            if event.get("type") == "item.completed":
                typed(item, dict, "codex_item")
                typed(item.get("type"), str, "codex_item_type")
                if item.get("type") in ("collab_agent_tool_call", "collab_tool_call") and item.get("status") == "completed":
                    prompt = typed(item.get("prompt") or "", str, "collaboration_prompt")
                    operation = typed(item.get("tool", "unknown"), str, "collaboration_tool")
                    states = typed(item.get("agents_states", item.get("agent_states", {})) or {}, dict, "agent_states")
                    identities = typed(item.get("receiver_thread_ids") or [], list, "agent_identities")
                    tools.append({"name": "collaboration:" + operation, "input": prompt, "output": json.dumps(states)})
                    if "review" in prompt.lower() and re.search(r"read[- ]only", prompt, re.I):
                        for identity in identities:
                            typed(identity, str, "agent_identity")
                            review_assignments[identity] = prompt
                    for identity, state in states.items():
                        if identity in review_assignments and isinstance(state, dict) and state.get("status") == "completed" and state.get("message"):
                            typed(state["message"], str, "reviewer_response")
                            reviewers.append({"id": identity, "prompt": review_assignments[identity], "output": state["message"], "tool_position": len(tools)})
                if item.get("type") == "agent_message":
                    final = item.get("text")
                if item.get("type") == "mcp_tool_call" and item.get("status") == "completed":
                    tools.append({"name": "mcp:" + item.get("server", "unknown") + ":" + item.get("tool", "unknown"),
                                  "input": item.get("arguments", {}), "output": "completed"})
                if item.get("type") == "command_execution" and item.get("exit_code") == 0:
                    command = typed(item.get("command"), str, "command_input")
                    output = typed(item.get("aggregated_output", ""), str, "command_output")
                    tools.append({"name": "command", "input": command, "output": output})
                    # A cat/sed/read command must complete and actually return content.
                    if item.get("aggregated_output") and re.search(r"\b(cat|sed|head|read_text)\b", command):
                        skills.update(SKILL_PATH.findall(command))
        else:
            # Status/system events may carry plain message strings. Only the
            # assistant/user envelopes contain tool evidence.
            blocks = []
            if event["type"] in ("assistant", "user"):
                message = typed(event.get("message"), dict, "claude_message")
                content = message.get("content")
                if event["type"] == "user" and isinstance(content, str):
                    content = []  # Valid user text cannot prove a tool result.
                blocks = typed(content, list, "claude_content")
            for block in blocks:
                typed(block, dict, "claude_content_block")
                typed(block.get("type"), str, "claude_block_type")
                if block.get("type") == "tool_use":
                    identity = typed(block.get("id"), str, "tool_identity")
                    typed(block.get("name"), str, "tool_name")
                    arguments = typed(block.get("input"), dict, "tool_input")
                    for field in ("prompt", "file_path", "skill", "command"):
                        if field in arguments:
                            typed(arguments[field], str, "tool_input_" + field)
                    pending[identity] = block
                if block.get("type") == "tool_result" and not block.get("is_error"):
                    identity = typed(block.get("tool_use_id"), str, "tool_result_identity")
                    if identity not in pending:
                        raise EvalFailure("malformed_unmatched_tool_result")
                    call = pending[identity]
                    name, arguments = call.get("name", ""), call.get("input", {})
                    result_content = block.get("content", "")
                    if isinstance(result_content, list):
                        text_parts = []
                        for part in result_content:
                            typed(part, dict, "tool_result_block")
                            if "text" in part:
                                text_parts.append(typed(part["text"], str, "tool_result_text"))
                        result_content = "\n".join(text_parts)
                    typed(result_content, str, "tool_result_content")
                    tools.append({"name": name, "input": arguments, "output": result_content})
                    if name in ("Agent", "Task") and "review" in arguments.get("prompt", "").lower() and re.search(r"read[- ]only", arguments.get("prompt", ""), re.I):
                        reviewers.append({"id": block.get("tool_use_id"), "prompt": arguments["prompt"], "output": result_content, "tool_position": len(tools)})
                    if name == "Read" and block.get("content"):
                        skills.update(SKILL_PATH.findall(arguments.get("file_path", "")))
                    if name == "Skill" and block.get("content"):
                        selected_skill = normalize_skill(arguments.get("skill", ""))
                        skills.add(selected_skill)
                        invoked.add(selected_skill)
                    if name == "Bash" and block.get("content"):
                        command = arguments.get("command", "")
                        if re.search(r"\b(cat|sed|head|read_text)\b", command):
                            skills.update(SKILL_PATH.findall(command))
            if event.get("type") == "result":
                if event.get("is_error") or event.get("subtype") != "success":
                    raise EvalFailure("host_error")
                terminal, final = True, event.get("result")
                if isinstance(event.get("structured_output"), dict):
                    final = json.dumps(event["structured_output"])
    if not terminal or final is None:
        raise EvalFailure("incomplete_transcript")
    try:
        clean = re.sub(r"^\s*```(?:json)?\s*|\s*```\s*$", "", final)
        decision = json.loads(clean)
        if not isinstance(decision, dict):
            raise ValueError("decision must be object")
    except (ValueError, TypeError) as exc:
        raise EvalFailure("malformed_decision") from exc
    decision["primary"] = normalize_skill(decision.get("primary"))
    if isinstance(decision.get("supporting"), list):
        decision["supporting"] = [normalize_skill(name) for name in decision["supporting"]]
    return {"decision": decision, "skills": sorted(skills), "invoked_skills": sorted(invoked), "tools": tools, "reviewers": reviewers, "event_count": len(events)}

def check_routing(transcript, expected, repo):
    if set(transcript.get("invoked_skills", [])) & set(expected["prohibited"]):
        raise EvalFailure("prohibited_skill_invoked")
    decision = transcript["decision"]
    supporting = decision.get("supporting")
    if decision.get("primary") != expected["primary"] or not isinstance(supporting, list):
        raise EvalFailure("unexpected_selection")
    selected = [decision["primary"], *supporting]
    if any(not isinstance(item, str) for item in selected) or len(selected) != len(set(selected)):
        raise EvalFailure("duplicate_controller")
    if not set(expected["supporting"]).issubset(supporting) or set(selected) & set(expected["prohibited"]):
        raise EvalFailure("unexpected_selection")
    required_reads = set(selected) - {"native-focused-edit"}
    if not required_reads.issubset(transcript["skills"]):
        raise EvalFailure("missing_skill_evidence")
    for relative in expected["artifacts"]:
        artifact = (repo / relative).resolve()
        if not artifact.is_relative_to(repo.resolve()) or not artifact.is_file() or not artifact.stat().st_size:
            raise EvalFailure("missing_artifact:" + relative)
    if "fallback" in expected:
        observed = json.loads((repo / "fallback.json").read_text())
        if any(observed.get(key) != value for key, value in expected["fallback"].items()):
            raise EvalFailure("incorrect_capability_fallback")
        for tool in transcript["tools"]:
            command = tool["input"] if isinstance(tool["input"], str) else tool["input"].get("command", "")
            if tool["name"] in ("Agent", "Task") or tool["name"].startswith(("collaboration:", "mcp:", "mcp__")) or re.search(r"\b(?:gh\s|git\s+push\b|git\s+worktree\s+(?:add|remove)\b)", command):
                raise EvalFailure("unavailable_capability_invoked")

def fingerprint(root):
    paths = [p for p in root.rglob("*") if p.is_file() and
             not any(part in {".git", ".engineering-method", ".superpowers", ".worktrees", "__pycache__"} for part in p.relative_to(root).parts)]
    data = {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(paths)}
    return hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()

def retain_project(repo, destination):
    """Retain bounded generated artifacts for replay, including failed runs."""
    destination.mkdir(parents=True, exist_ok=True)
    total, count = 0, 0
    for path in sorted(repo.rglob("*")):
        relative = path.relative_to(repo)
        if any(part in {".git", ".agents", "__pycache__"} for part in relative.parts) or path.is_symlink() or not path.is_file():
            continue
        total += path.stat().st_size
        count += 1
        if total > 20_000_000 or count > 1000:
            raise EvalFailure("artifact_retention_limit")
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(path, target)
        target.chmod(0o600)

def prepare_repo(repo, case, plugin):
    repo.mkdir()
    subprocess.run(["git", "init", "-q", str(repo)], check=True, capture_output=True)
    for relative, content in case.get("files", {}).items():
        path = (repo / relative).resolve()
        if not path.is_relative_to(repo.resolve()):
            raise EvalFailure("fixture_path_escape")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
    skills = repo / ".agents/skills"
    skills.mkdir(parents=True)
    for path in (plugin / "skills").iterdir():
        if path.is_dir():
            (skills / path.name).symlink_to(path.resolve(), target_is_directory=True)

def stage_plugin(plugin, destination):
    """Native tool grants cover a disposable copy, never the caller's sources."""
    shutil.copytree(plugin, destination, ignore=shutil.ignore_patterns(
        ".git", ".engineering-method", ".superpowers", ".worktrees", "__pycache__"))
    return destination

def host_command(host, repo, plugin, config, model, auth_home=None, prompt="", budget=2):
    env = os.environ.copy()
    for key in ("ANTHROPIC_API_KEY", "OPENAI_API_KEY", "CLAUDECODE", "ANTHROPIC_AUTH_TOKEN"):
        env.pop(key, None)
    effort = model_effort(host, model, plugin)
    if host == "codex":
        env["CODEX_HOME"] = str(auth_home or config)
        schema = config / "decision-schema.json"
        schema.write_text(json.dumps(DECISION_SCHEMA))
        command = ["codex", "exec", "--json", "--ephemeral", "--ignore-user-config",
                   "--sandbox", "workspace-write", "-C", str(repo),
                   "-m", model, "--output-schema", str(schema)]
        if effort is not None:
            command.extend(["-c", f'model_reasoning_effort="{effort}"'])
        command.append(prompt)
    else:
        env["CLAUDE_CONFIG_DIR"] = str(auth_home or config)
        settings = config / "settings.json"
        settings.write_text(json.dumps({"disableAllHooks": True, "enableAllProjectMcpServers": False}))
        command = ["claude", "-p", "--verbose", "--output-format", "stream-json",
                   "--no-session-persistence", "--setting-sources", "", "--settings", str(settings),
                   "--strict-mcp-config", "--mcp-config", '{"mcpServers":{}}', "--plugin-dir", str(plugin),
                   "--add-dir", str(plugin), "--model", model, "--permission-mode", "auto",
                   "--permission-prompts", "none", "--max-budget-usd", str(budget), "--no-chrome",
                   "--json-schema", json.dumps(DECISION_SCHEMA)]
        if effort is not None:
            command.extend(["--effort", effort])
        command.append(prompt)
    return command, env

SKILL_DISCOVERY_INSTRUCTION = """
The shared skill files are linked directly at
.agents/skills/<skill-name>/SKILL.md in this repository. The engineering-method:
invocation namespace is not an extra filesystem directory. Discover actual paths
with `rg --files --hidden --follow .agents/skills -g SKILL.md`, then read the
selected files. Ordinary searches without symlink following may miss these files;
an invented path or empty non-following search is not evidence of a missing skill.
"""

ROUTING_INSTRUCTION = SKILL_DISCOVERY_INSTRUCTION + """
Assess the request and current repository using the available engineering-method
skills. Perform the first safe assessment step only; do not implement the entire
feature or launch subagents in this routing evaluation. Open the selected skill
instructions through tools before applying them. The assessment includes that
skill's required prerequisite and recovery preamble checks: follow its supporting
skill handoffs far enough to establish the current state before stopping. Do not
stop merely after choosing or reading the primary skill. This does not authorize
full lifecycle implementation or generating later-phase artifacts.
Write decision.md explaining the
one primary workflow and necessary supporting skills, using repository evidence.
Finish with ONLY a JSON object {"primary": "<skill-name or native-focused-edit>",
"supporting": ["<selected supporting skill names>"]}. Report the skills actually
applied, not every skill considered. Do not invent artifacts, live agents, or tests.
"""
def run_case(host, case, expected, output, timeout, auth_home=None, model=None, plugin=ROOT):
    source_sha256 = fingerprint(plugin)
    with tempfile.TemporaryDirectory(prefix="engineering-method-eval-") as directory:
        temporary = Path(directory)
        repo, config = temporary / "repo", temporary / "config"
        config.mkdir()
        staged_plugin = stage_plugin(plugin, temporary / "plugin")
        staged_sha256 = fingerprint(staged_plugin)
        prepare_repo(repo, case, staged_plugin)
        policy = model_policy(host, plugin)
        evaluation_kind = "architectural" if case.get("architectural") else "routing"
        evaluation_role = policy["evaluation_roles"][evaluation_kind]
        model = model or policy["roles"][evaluation_role][0]["model"]
        command, env = host_command(host, repo, staged_plugin, config, model, auth_home,
                                    case["prompt"] + "\n" + ROUTING_INSTRUCTION)
        stdout = ""
        try:
            stdout = execute(command, repo, env, timeout)
            private_transcript(output / f'{case["id"]}-raw.jsonl', stdout)
            retain_project(repo, output / case["id"] / "artifacts")
            transcript = parse_transcript(host, stdout)
            check_routing(transcript, expected, repo)
            if fingerprint(plugin) != source_sha256 or fingerprint(staged_plugin) != staged_sha256:
                raise EvalFailure("plugin_changed_during_evaluation")
        except EvalFailure as exc:
            private_transcript(output / f'{case["id"]}-raw.jsonl', exc.transcript or stdout)
            retain_project(repo, output / case["id"] / "artifacts")
            (output / f'{case["id"]}-events.json').write_text(json.dumps(diagnostic_events(exc.transcript or stdout), indent=2) + "\n")
            raise
        retain_project(repo, output / case["id"] / "artifacts")
        private_transcript(output / f'{case["id"]}-raw.jsonl', stdout)
        (output / f'{case["id"]}-events.json').write_text(json.dumps(diagnostic_events(stdout), indent=2) + "\n")
        return {"case_id": case["id"], "status": "passed", "host": host, "model": model,
                "effort": model_effort(host, model, plugin), "source_sha256": source_sha256,
                "primary": transcript["decision"]["primary"], "skills": transcript["skills"],
                "tool_count": len(transcript["tools"]), "event_count": transcript["event_count"],
                "artifacts": {p: hashlib.sha256((repo / p).read_bytes()).hexdigest()
                              for p in expected["artifacts"]},
                "transcript_sha256": hashlib.sha256(stdout.encode()).hexdigest()}

def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", required=True, choices=["codex", "claude"])
    parser.add_argument("--case")
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--timeout", type=float, default=120)
    parser.add_argument("--auth-home", type=Path)
    parser.add_argument("--model")
    parser.add_argument("--plugin-root", type=Path, default=ROOT)
    args = parser.parse_args(argv)
    output = args.output_dir.resolve()
    fixture = (ROOT / "tests/fixtures").resolve()
    if output.is_relative_to(ROOT.resolve()):
        parser.error("output must not overwrite fixture or plugin sources")
    output.mkdir(parents=True, exist_ok=True)
    os.chmod(output, 0o700)
    expected = json.loads((ROOT / f"evals/{args.host}/expected.json").read_text())
    cases = [json.loads(path.read_text()) for path in sorted((ROOT / "evals/shared/triggers").glob("*.json"))]
    if args.case:
        cases = [case for case in cases if case["id"] == args.case]
    if not cases:
        parser.error("no evaluation cases selected")
    results = []
    for case in cases:
        try:
            result = run_case(args.host, case, expected[case["id"]], output, args.timeout,
                              args.auth_home, args.model, args.plugin_root)
        except (EvalFailure, OSError, ValueError) as exc:
            result = {"case_id": case["id"], "host": args.host, "status": "failed",
                      "failure": str(exc) if isinstance(exc, EvalFailure) else type(exc).__name__}
        results.append(result)
        (output / f'{case["id"]}.json').write_text(json.dumps(result, indent=2) + "\n")
        print(json.dumps(result), flush=True)
        if result["status"] != "passed":
            break
    commit = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True)
    summary = {"status": "passed" if len(results) == len(cases) and all(r["status"] == "passed" for r in results) else "failed",
               "host": args.host, "source_commit": commit.stdout.strip(),
               "source_sha256": fingerprint(args.plugin_root), "completed_at": datetime.now(timezone.utc).isoformat(),
               "requested_cases": len(cases), "results": results}
    (output / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    return 0 if summary["status"] == "passed" else 1

if __name__ == "__main__":
    raise SystemExit(main())
