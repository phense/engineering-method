"""Host process boundaries must fail closed and require observable skill use."""

import json
import os
from pathlib import Path
import signal
import shlex
import subprocess
import sys
import tempfile
import time
import unittest
from unittest.mock import patch

from scripts.run_host_evals import EvalFailure, execute, parse_transcript, check_routing, host_command, run_case, prepare_repo, ROUTING_INSTRUCTION, diagnostic_events


class HostRunnerTests(unittest.TestCase):
    def test_claude_shell_reads_allow_only_terminal_newline_removal(self):
        from scripts.run_host_evals import observed_read_skills
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / 'skills' / 'speckit-plan' / 'SKILL.md'
            path.parent.mkdir(parents=True)
            content = '# Complete skill\nRead every requirement.\n'
            path.write_text(content)
            command = 'cat .agents/skills/speckit-plan/SKILL.md'
            self.assertEqual({'speckit-plan'}, observed_read_skills(command, content[:-1], root))
            self.assertEqual(set(), observed_read_skills(command, content[:-2], root))
            self.assertEqual(set(), observed_read_skills(command, content.replace('every ', ''), root))

    def setUp(self):
        # Test defaults independently of the invoking live evaluation policy.
        override = patch.dict(os.environ, {f"EM_EVAL_{host}_{field}": ""
                             for host in ("CODEX", "CLAUDE") for field in ("MODEL", "EFFORT")})
        override.start()
        self.addCleanup(override.stop)

    def test_resolved_path_then_full_cat_is_observed_without_accepting_echo_or_partial_reads(self):
        from scripts.run_host_evals import observed_read_skills
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            skill = root / "skills/openspec-apply/SKILL.md"
            skill.parent.mkdir(parents=True)
            content = "---\nname: openspec-apply\n---\nComplete evaluated instructions.\n"
            skill.write_text(content)
            alias = ".agents/skills/openspec-apply/SKILL.md"
            output = str(skill) + "\n" + content + "other file listing\n"
            command = f"realpath {alias}; cat {alias}; rg --files"
            self.assertEqual({"openspec-apply"}, observed_read_skills(command, output, root))
            for bad_command, bad_output in (
                (f"realpath {alias}; echo {shlex.quote(content)}", output),
                (f"realpath {alias}; cat /dev/null; echo {shlex.quote(content)}", output),
                (command, str(skill) + "\n---\n"),
                (f"realpath {alias} && false && cat {alias}", output),
            ):
                with self.subTest(command=bad_command):
                    self.assertEqual(set(), observed_read_skills(bad_command, bad_output, root))

    def test_dynamic_batch_read_requires_actual_read_and_exact_evaluated_skill_content(self):
        with tempfile.TemporaryDirectory() as directory:
            plugin = Path(directory)
            skill = plugin / "skills/speckit-plan/SKILL.md"
            skill.parent.mkdir(parents=True)
            skill.write_text("---\nname: speckit-plan\n---\nUnique evaluated plugin planning contract.\n")
            read_command = "python3 - <<'PY'\nfrom pathlib import Path\nfor n in ['speckit-plan']:\n p=Path('.agents/skills')/n/'SKILL.md'\n print(p.resolve()); print(p.read_text())\nPY"
            output = str(skill) + "\n" + skill.read_text()
            def observed(command, content, code=0):
                events = [{"type": "item.completed", "item": {"type": "command_execution", "command": command,
                            "exit_code": code, "aggregated_output": content}},
                          {"type": "item.completed", "item": {"type": "agent_message", "text": '{"primary":"speckit-plan","supporting":[]}'}},
                          {"type": "turn.completed"}]
                return parse_transcript("codex", "\n".join(map(json.dumps, events)), plugin=plugin)
            self.assertEqual(["speckit-plan"], observed(read_command, output)["skills"])
            self.assertEqual([], observed(f"head -n 1 {skill}", "---\n")["skills"])
            self.assertEqual(["speckit-plan"], observed(f"cat {skill}", output)["skills"])
            for command, content, code in ((read_command, output, 1), (read_command, str(skill), 0),
                    (read_command, "Documentation mentions speckit-plan", 0),
                    ("echo " + shlex.quote(output + " read_text"), output, 0)):
                with self.subTest(command=command, content=content, code=code):
                    self.assertEqual([], observed(command, content, code)["skills"])
            skill.write_text("Updated evaluated content\n")
            self.assertEqual([], observed(read_command, output)["skills"])

    def test_successful_native_content_is_not_an_authentication_diagnostic(self):
        plugin = Path(__file__).resolve().parents[1]
        documentation = (plugin / "shared/platform/claude.md").read_text()
        events = [
            {"type": "user", "message": {"content": [{"type": "tool_result", "is_error": False,
                                                        "content": documentation}]}},
            {"type": "item.completed", "item": {"type": "command_execution", "exit_code": 0,
                                                  "aggregated_output": "Not logged in; OAuth failed describes a fixture"}},
            {"type": "assistant", "message": {"content": [{"type": "text", "text": "OAuth failed is documented"}]}},
            {"type": "result", "subtype": "success", "is_error": False,
             "result": "Documentation says not logged in", "structured_output": {"primary": "speckit-specify", "supporting": []}},
        ]
        raw = "\n".join(map(json.dumps, events))
        self.assertEqual(self.run_fake("print(" + repr(raw) + ")").strip(), raw)
        with self.assertRaisesRegex(EvalFailure, "host_exit:7:uncategorized_native_error"):
            self.run_fake("import sys; print(" + repr(raw) + "); sys.exit(7)")

    def test_native_authentication_failures_are_classified_without_scanning_tool_content(self):
        failures = ["Not logged in", json.dumps({"type": "result", "subtype": "error_during_execution",
                    "is_error": True, "errors": ["OAuth authentication failed"]}),
                    json.dumps({"type": "turn.failed", "error": {"message": "authentication required"}}),
                    json.dumps({"type": "error", "message": "invalid API key"})]
        for failure in failures:
            for code in (0, 1):
                with self.subTest(failure=failure, exit_code=code):
                    with self.assertRaisesRegex(EvalFailure, "^authentication$"):
                        self.run_fake("import sys; print(" + repr(failure) + "); sys.exit(" + str(code) + ")")
        with self.assertRaisesRegex(EvalFailure, "^authentication$"):
            self.run_fake("import sys; print('Please login: authentication required', file=sys.stderr)")

    def test_existing_openspec_fixture_contains_complete_approved_planning(self):
        plugin = Path(__file__).resolve().parents[1]
        case = json.loads((plugin / "evals/shared/triggers/existing-openspec.json").read_text())
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "repo"
            prepare_repo(root, case, plugin)
            change = root / "openspec/changes/export-semicolon"
            for relative in ("proposal.md", "design.md", "tasks.md", "specs/export/spec.md"):
                with self.subTest(artifact=relative):
                    self.assertTrue((change / relative).is_file(), "approved apply fixture lacks required planning input")
                    self.assertTrue((change / relative).read_text().strip())

    def test_default_evaluation_model_uses_host_routing_tier(self):
        for host, architectural, expected_model in (("codex", False, "gpt-5.6-luna"),
                                                    ("codex", True, "gpt-6-astra"),
                                                    ("claude", False, "sonnet"),
                                                    ("claude", True, "fable")):
            with self.subTest(host=host, architectural=architectural), tempfile.TemporaryDirectory() as directory:
                def inspect_invocation(command, cwd, env, timeout):
                    flag = "-m" if host == "codex" else "--model"
                    self.assertEqual(expected_model, command[command.index(flag) + 1])
                    raise EvalFailure("checked_default_model")
                with patch("scripts.run_host_evals.execute", inspect_invocation):
                    with self.assertRaisesRegex(EvalFailure, "checked_default_model"):
                        run_case(host, {"id": "default-tier", "prompt": "assess", "files": {}, "architectural": architectural},
                                 {"primary": "native-focused-edit", "supporting": [], "prohibited": [], "artifacts": []}, Path(directory), 1)

    def test_claude_grants_only_staged_plugin_and_preserves_safety_flags(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)
            def inspect_invocation(command, cwd, env, timeout):
                self.assertEqual("auto", command[command.index("--permission-mode") + 1])
                granted = Path(command[command.index("--add-dir") + 1])
                self.assertEqual(cwd.parent, granted.parent)
                self.assertEqual("plugin", granted.name)
                self.assertEqual(granted, Path(command[command.index("--plugin-dir") + 1]))
                self.assertTrue((cwd / ".agents/skills/openspec-propose/SKILL.md").resolve().is_relative_to(granted.resolve()))
                self.assertEqual("1", env["CLAUDE_CODE_SAFE_MODE"])
                self.assertEqual("1", env["CLAUDE_CODE_SIMPLE"])
                self.assertNotIn("bypassPermissions", command)
                raise EvalFailure("checked_invocation")
            with patch.dict(os.environ, {"CLAUDE_CODE_SAFE_MODE": "1", "CLAUDE_CODE_SIMPLE": "1"}), patch("scripts.run_host_evals.execute", inspect_invocation):
                with self.assertRaisesRegex(EvalFailure, "checked_invocation"):
                    run_case("claude", {"id": "permission-scope", "prompt": "assess", "files": {}},
                             {"primary": "native-focused-edit", "supporting": [], "prohibited": [], "artifacts": []}, output, 1)

    def test_informational_string_message_is_not_an_assistant_envelope(self):
        events = [{"type": "system", "subtype": "status", "message": "Connecting"},
                  {"type": "result", "subtype": "success", "structured_output": {"primary": "native-focused-edit", "supporting": []}}]
        parsed = parse_transcript("claude", "\n".join(map(json.dumps, events)))
        self.assertEqual("native-focused-edit", parsed["decision"]["primary"])
        self.assertEqual([], parsed["tools"])

    def test_malformed_evidence_envelopes_fail_explicitly(self):
        cases = [
            ("claude", {"type": "assistant", "message": "invalid"}),
            ("claude", {"type": "assistant", "message": {"content": None}}),
            ("claude", {"type": "assistant", "message": {"content": [{"type": "tool_use", "id": "t", "name": "Read", "input": "invalid"}]}}),
            ("codex", {"type": "item.completed", "item": "invalid"}),
            ("codex", {"type": "item.completed", "item": {"type": "command_execution", "exit_code": 0, "command": [], "aggregated_output": "invalid"}}),
        ]
        for host, event in cases:
            with self.subTest(event=event):
                with self.assertRaisesRegex(EvalFailure, "malformed"):
                    parse_transcript(host, json.dumps(event))
                self.assertIsInstance(diagnostic_events(json.dumps(event)), list)

    def test_parser_crash_retains_raw_and_project_before_diagnostics(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)
            raw = json.dumps({"type": "assistant", "message": "invalid"})
            def native_output(command, cwd, env, timeout):
                (cwd / "decision.md").write_text("Native generated assessment.")
                return raw
            with patch("scripts.run_host_evals.execute", native_output):
                with self.assertRaisesRegex(EvalFailure, "malformed"):
                    run_case("claude", {"id": "parser-shape", "prompt": "assess", "files": {}},
                             {"primary": "native-focused-edit", "supporting": [], "prohibited": [], "artifacts": []}, output, 1)
                with patch("scripts.run_host_evals._parse_transcript", side_effect=AttributeError("private native text")):
                    with self.assertRaisesRegex(EvalFailure, "^malformed_native_envelope:AttributeError$"):
                        run_case("claude", {"id": "parser-shape", "prompt": "assess", "files": {}},
                                 {"primary": "native-focused-edit", "supporting": [], "prohibited": [], "artifacts": []}, output, 1)
            self.assertEqual(raw, (output / "parser-shape-raw.jsonl").read_text())
            self.assertEqual(0o600, (output / "parser-shape-raw.jsonl").stat().st_mode & 0o777)
            self.assertEqual("Native generated assessment.", (output / "parser-shape/artifacts/decision.md").read_text())

    def test_prompt_discovery_command_follows_actual_skill_links(self):
        """A namespaced guess or non-following search must not hide installed skills."""
        import re
        command = re.search(r"`(rg --files[^`]+)`", ROUTING_INSTRUCTION)
        self.assertIsNotNone(command, "routing prompt needs executable filesystem discovery guidance")
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "repo"
            plugin = Path(__file__).resolve().parents[1]
            prepare_repo(root, {"files": {}}, plugin)
            result = subprocess.run(shlex.split(command.group(1)), cwd=root, capture_output=True, text=True, check=True)
            self.assertIn(".agents/skills/openspec-propose/SKILL.md", result.stdout.splitlines())
            for path in result.stdout.splitlines():
                self.assertTrue((root / path).is_file())
            backlog_skill = (root / ".agents/skills/project-backlog/SKILL.md").resolve()
            for name in ("project-state", "continuity-state"):
                self.assertTrue((backlog_skill.parent / "../../scripts" / name).resolve().is_file())
            apply_skill = (root / ".agents/skills/openspec-propose/SKILL.md").resolve()
            self.assertTrue((apply_skill.parent / "../../templates/openspec/design.md").resolve().is_file())

    def test_failed_run_retains_generated_artifacts_before_temp_cleanup(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)
            def failed_host(command, cwd, env, timeout):
                (cwd / "failure.md").write_text("Actual generated diagnostic artifact.")
                raise EvalFailure("timeout")
            with patch("scripts.run_host_evals.execute", failed_host):
                with self.assertRaisesRegex(EvalFailure, "timeout"):
                    run_case("codex", {"id": "retention", "prompt": "diagnose", "files": {}},
                             {"primary": "native-focused-edit", "supporting": [], "prohibited": [], "artifacts": []}, output, 1)
            self.assertEqual("Actual generated diagnostic artifact.", (output / "retention/artifacts/failure.md").read_text())

    def test_fallback_report_cannot_hide_prohibited_remote_or_agent_use(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            fallback = {"selected_role": "standard", "spawn_subagents": False, "use_github": False}
            (root / "fallback.json").write_text(json.dumps(fallback))
            expected = {"primary": "native-focused-edit", "supporting": [], "prohibited": [], "artifacts": ["fallback.json"], "fallback": fallback}
            transcript = {"decision": {"primary": "native-focused-edit", "supporting": []}, "skills": [], "tools": []}
            check_routing(transcript, expected, root)
            transcript["tools"] = [{"name": "command", "input": "gh issue create --title test"}]
            with self.assertRaisesRegex(EvalFailure, "unavailable_capability"):
                check_routing(transcript, expected, root)

    def test_explicit_evaluation_model_override_controls_roles_effort_and_native_prompt(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            plugin = Path(__file__).resolve().parents[1]
            for host, model in (("codex", "gpt-6-astra"), ("claude", "claude-fable-5-1")):
                with self.subTest(host=host), patch.dict(os.environ, {
                    "EM_EVAL_" + host.upper() + "_MODEL": model,
                    "EM_EVAL_" + host.upper() + "_EFFORT": "low",
                }):
                    from scripts.run_host_evals import model_policy, model_effort
                    policy = model_policy(host, plugin)
                    self.assertEqual({"model": model, "effort": "low"}, policy["coordinator"])
                    self.assertEqual("low", model_effort(host, model, plugin))
                    self.assertTrue(all(v == [{"model": model, "effort": "low"}] for v in policy["roles"].values()))
                    command, _ = host_command(host, root, plugin, root, model, prompt="Evaluate.")
                    self.assertIn("coordinator and all subagents", command[-1])
                    self.assertIn(model, command[-1])
                    self.assertIn("low", command[-1])

    def test_model_effort_comes_from_host_adapter(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for host, model, effort in (("codex", "gpt-6-astra", "medium"), ("codex", "gpt-5.6-sol", "high"),
                                        ("claude", "fable", "medium"), ("claude", "opus", "high")):
                with self.subTest(model=model):
                    command, env = host_command(host, root, Path(__file__).resolve().parents[1], root, model)
                    if host == "codex":
                        self.assertIn('model_reasoning_effort="' + effort + '"', command)
                    else:
                        self.assertEqual(effort, command[command.index("--effort") + 1])

    def test_wrapper_cancellation_stops_host_descendants(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            marker = root / "orphan.txt"
            ready = root / "ready.txt"
            child = f"import time; from pathlib import Path; time.sleep(0.6); Path({str(marker)!r}).write_text('orphan')"
            host = f"import subprocess,sys,time; from pathlib import Path; subprocess.Popen([sys.executable,'-c',{child!r}]); Path({str(ready)!r}).write_text('ready'); time.sleep(10)"
            wrapper = ("import sys; from pathlib import Path; from scripts.run_host_evals import execute; "
                       f"execute([sys.executable,'-c',{host!r}],Path({str(root)!r}),{{}},10)")
            process = subprocess.Popen([sys.executable, "-c", wrapper], stdout=subprocess.DEVNULL,
                                       stderr=subprocess.DEVNULL, start_new_session=True)
            try:
                deadline = time.monotonic() + 3
                while not ready.exists() and time.monotonic() < deadline:
                    time.sleep(0.01)
                self.assertTrue(ready.exists())
                process.send_signal(signal.SIGTERM)
                process.wait(timeout=2)
                time.sleep(0.7)
                self.assertFalse(marker.exists(), "cancelled host left an executing descendant")
            finally:
                if process.poll() is None:
                    os.killpg(process.pid, signal.SIGKILL)
                    process.wait()

    def test_claude_empty_mcp_configuration_has_native_schema(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            command, env = host_command("claude", root, Path(__file__).resolve().parents[1], root, "haiku")
            self.assertEqual({"mcpServers": {}}, json.loads(command[command.index("--mcp-config") + 1]))

    def run_fake(self, code, timeout=2):
        with tempfile.TemporaryDirectory() as directory:
            return execute([sys.executable, "-c", code], Path(directory), {}, timeout)

    def test_timeout_is_a_failure(self):
        with self.assertRaisesRegex(EvalFailure, "timeout"):
            self.run_fake("import time; time.sleep(10)", timeout=0.05)

    def test_missing_host_is_a_failure(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(EvalFailure, "missing_command"):
                execute(["/nonexistent/em-host"], Path(directory), {}, 1)

    def test_auth_failure_is_not_success_even_with_zero_exit(self):
        with self.assertRaisesRegex(EvalFailure, "authentication"):
            self.run_fake("print('Please login: authentication required')")

    def test_malformed_jsonl_is_a_failure(self):
        with self.assertRaisesRegex(EvalFailure, "malformed"):
            parse_transcript("codex", "not JSON\n")

    def test_claim_without_tool_evidence_cannot_pass(self):
        decision = {"primary": "systematic-debugging", "supporting": ["project-backlog"]}
        events = [{"type": "item.completed", "item": {"type": "agent_message", "text": json.dumps(decision)}}, {"type": "turn.completed"}]
        transcript = parse_transcript("codex", "\n".join(map(json.dumps, events)))
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(EvalFailure, "skill_evidence"):
                check_routing(transcript, {**decision, "prohibited": [], "artifacts": []}, Path(directory))

    def test_successful_read_evidence_and_real_artifacts_pass(self):
        decision = {"primary": "systematic-debugging", "supporting": ["project-backlog"]}
        plugin = Path(__file__).resolve().parents[1]
        contents = "\n".join((plugin / "skills" / name / "SKILL.md").read_text()
                             for name in ("systematic-debugging", "project-backlog"))
        events = [{"type": "item.completed", "item": {"type": "command_execution", "command": "cat skills/systematic-debugging/SKILL.md skills/project-backlog/SKILL.md", "exit_code": 0, "aggregated_output": contents}}, {"type": "item.completed", "item": {"type": "agent_message", "text": json.dumps(decision)}}, {"type": "turn.completed"}]
        transcript = parse_transcript("codex", "\n".join(map(json.dumps, events)))
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "decision.md").write_text("Diagnosis begins from the failure.")
            check_routing(transcript, {**decision, "prohibited": ["openspec-apply"], "artifacts": ["decision.md"]}, root)
            with self.assertRaisesRegex(EvalFailure, "selection"):
                check_routing(transcript, {**decision, "primary": "openspec-apply", "prohibited": [], "artifacts": []}, root)

    def test_collision_and_missing_terminal_are_failures(self):
        with self.assertRaisesRegex(EvalFailure, "incomplete"):
            parse_transcript("codex", json.dumps({"type": "thread.started"}))
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(EvalFailure, "selection"):
                check_routing({"decision": {"primary": ["openspec-apply", "speckit-plan"], "supporting": []}, "skills": []},
                              {"primary": "openspec-apply", "supporting": [], "prohibited": [], "artifacts": []}, Path(directory))

    def test_claude_requires_successful_tool_result(self):
        decision = {"primary": "openspec-apply", "supporting": []}
        events = [{"type": "assistant", "message": {"content": [{"type": "tool_use", "id": "r1", "name": "Read", "input": {"file_path": "/repo/skills/openspec-apply/SKILL.md"}}]}},
                  {"type": "user", "message": {"content": [{"type": "tool_result", "tool_use_id": "r1", "content": "skill text"}]}},
                  {"type": "result", "subtype": "success", "is_error": False, "result": json.dumps(decision)}]
        parsed = parse_transcript("claude", "\n".join(map(json.dumps, events)))
        self.assertEqual(["openspec-apply"], parsed["skills"])
        events[1]["message"]["content"][0]["is_error"] = True
        self.assertEqual([], parse_transcript("claude", "\n".join(map(json.dumps, events)))["skills"])

    def test_claude_native_structured_output_is_the_decision(self):
        decision = {"primary": "native-focused-edit", "supporting": []}
        transcript = json.dumps({"type": "result", "subtype": "success", "is_error": False,
                                 "result": "Assessment complete.", "structured_output": decision})
        self.assertEqual(decision, parse_transcript("claude", transcript)["decision"])

    def test_claude_plugin_prefix_normalizes_but_foreign_namespace_fails(self):
        event = {"type": "result", "subtype": "success", "is_error": False,
                 "structured_output": {"primary": "native-focused-edit", "supporting": ["engineering-method:verification-before-completion"]}}
        parsed = parse_transcript("claude", json.dumps(event))
        self.assertEqual(["verification-before-completion"], parsed["decision"]["supporting"])
        event["structured_output"]["supporting"] = ["other-plugin:verification-before-completion"]
        with self.assertRaisesRegex(EvalFailure, "namespace"):
            parse_transcript("claude", json.dumps(event))

    def test_explicit_prohibited_skill_invocation_overrides_denial_in_decision(self):
        events = [{"type": "assistant", "message": {"content": [{"type": "tool_use", "id": "s1", "name": "Skill", "input": {"skill": "engineering-method:openspec-apply"}}]}},
                  {"type": "user", "message": {"content": [{"type": "tool_result", "tool_use_id": "s1", "content": "loaded"}]}},
                  {"type": "result", "subtype": "success", "structured_output": {"primary": "native-focused-edit", "supporting": []}}]
        parsed = parse_transcript("claude", "\n".join(map(json.dumps, events)))
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(EvalFailure, "invoked"):
                check_routing(parsed, {"primary": "native-focused-edit", "supporting": [], "prohibited": ["openspec-apply"], "artifacts": []}, Path(directory))

    def test_codex_spawn_completion_is_not_reviewer_completion(self):
        events = [{"type": "item.completed", "item": {"type": "collab_agent_tool_call", "tool": "spawn_agent", "status": "completed", "prompt": "Read-only review of reports/S1.md", "receiver_thread_ids": ["reviewer-running"]}},
                  {"type": "item.completed", "item": {"type": "agent_message", "text": '{"primary":"orchestrated-implementation","supporting":[]}'}},
                  {"type": "turn.completed"}]
        self.assertEqual([], parse_transcript("codex", "\n".join(map(json.dumps, events)))["reviewers"])
        response = '{"review_kind":"system-architect-final","status":"clean","actionable_findings":[]}'
        events.insert(1, {"type": "item.completed", "item": {"type": "collab_agent_tool_call", "tool": "wait",
                         "status": "completed", "agents_states": {"reviewer-running": {"status": "completed", "message": response}}}})
        reviewers = parse_transcript("codex", "\n".join(map(json.dumps, events)))["reviewers"]
        self.assertEqual(1, len(reviewers))
        self.assertEqual(response, reviewers[0]["output"])
        self.assertEqual("reviewer-running", reviewers[0]["id"])
