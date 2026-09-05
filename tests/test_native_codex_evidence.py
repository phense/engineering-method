"""Native reviewer evidence must not be replaced by coordinator assertions."""
import copy
import json
from pathlib import Path
import tempfile
import unittest

from scripts import run_host_evals as runner

THREAD = '01a071b3-5bcb-7f32-9208-64bc1787d4d9'
CHILD = '01a071b3-8d7f-7ee1-a471-f4a9850857b9'


def records(project):
    def item(value):
        return {'type': 'event_msg', 'payload': {'type': 'item_completed', 'thread_id': THREAD, 'item': value}}
    answer = {'review_assignment': 'Read-only system-architect review evidence/final-review.md',
              'status': 'clean', 'actionable_findings': [], 'reviewed_files': {'checkout/service.py': 'a' * 64}}
    response = '```json\n' + json.dumps(answer) + '\n```'
    return [
        {'type': 'session_meta', 'payload': {'id': THREAD, 'cwd': str(project), 'source': 'exec'}},
        item({'type': 'CommandExecution', 'command': ['python3', 'check.py'], 'exit_code': 0, 'aggregated_output': 'before'}),
        item({'type': 'SubAgentActivity', 'kind': 'started', 'agent_thread_id': CHILD, 'agent_path': '/root/reviewer'}),
        item({'type': 'SubAgentActivity', 'kind': 'completed', 'agent_thread_id': CHILD, 'agent_path': '/root/reviewer'}),
        {'type': 'response_item', 'payload': {'type': 'agent_message', 'author': '/root/reviewer', 'recipient': '/root',
          'content': [{'type': 'input_text', 'text': 'Message Type: FINAL_ANSWER\nTask name: /root\nSender: /root/reviewer\nPayload:\n' + response}]}},
        item({'type': 'CommandExecution', 'command': ['python3', 'check.py'], 'exit_code': 0, 'aggregated_output': 'after'}),
        item({'type': 'AgentMessage', 'phase': 'final_answer', 'content': [{'type': 'Text', 'text': '{"primary":"orchestrated-implementation","supporting":[]}'}]}),
        {'type': 'event_msg', 'payload': {'type': 'task_complete'}},
    ], response


class NativeCodexEvidenceTests(unittest.TestCase):
    def parse(self, rows, project):
        parser = getattr(runner, 'parse_codex_rollout', None)
        self.assertIsNotNone(parser, 'Native completed reviewer responses must be captured')
        return parser('\n'.join(map(json.dumps, rows)), thread_id=THREAD, project=project)

    def test_preserves_native_response_and_its_position_without_decrypting_assignment(self):
        with tempfile.TemporaryDirectory() as d:
            rows, response = records(Path(d))
            parsed = self.parse(rows, Path(d))
            self.assertEqual(1, len(parsed['reviewers']))
            review = parsed['reviewers'][0]
            self.assertEqual(CHILD, review['id'])
            self.assertEqual(response, review['output'])
            self.assertEqual(1, review['tool_position'])
            self.assertEqual('native-reviewer-response', review['assignment_source'])
            self.assertEqual(['before', 'after'], [tool['output'] for tool in parsed['tools']])

    def test_rejects_wrong_session_project_and_incomplete_capture(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            rows, _ = records(root)
            for mutation in ('thread', 'project', 'terminal', 'malformed'):
                bad = copy.deepcopy(rows)
                if mutation == 'thread': bad[0]['payload']['id'] = CHILD
                if mutation == 'project': bad[0]['payload']['cwd'] = str(root / 'other')
                if mutation == 'terminal': bad.pop()
                if mutation == 'malformed': bad[3]['payload']['item']['agent_thread_id'] = 'bad'
                with self.subTest(mutation=mutation), self.assertRaises(runner.EvalFailure):
                    self.parse(bad, root)

    def test_capture_reads_only_the_stdout_thread_and_writes_private_evidence(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            sessions = root / 'sessions'
            sessions.mkdir()
            rows, response = records(root)
            native = sessions / ('rollout-date-' + THREAD + '.jsonl')
            native.write_text('\n'.join(map(json.dumps, rows)))
            output = root / 'capture.jsonl'
            stdout = json.dumps({'type': 'thread.started', 'thread_id': THREAD})
            capture = getattr(runner, 'capture_codex_rollout', None)
            self.assertIsNotNone(capture)
            parsed = capture(stdout, auth_home=root, project=root, output=output)
            self.assertEqual(response, parsed['reviewers'][0]['output'])
            self.assertEqual(0o600, output.stat().st_mode & 0o777)
            for identity in (CHILD, '../outside', THREAD + '/bad'):
                with self.subTest(identity=identity), self.assertRaises(runner.EvalFailure):
                    capture(json.dumps({'type': 'thread.started', 'thread_id': identity}),
                            auth_home=root, project=root, output=output)

    def test_coordinator_unfinished_foreign_and_unconfirmed_responses_cannot_qualify(self):
        with tempfile.TemporaryDirectory() as d:
            rows, _ = records(Path(d))
            for mutation in ('coordinator', 'unfinished', 'foreign', 'not-final', 'no-assignment'):
                bad = copy.deepcopy(rows)
                if mutation == 'coordinator': bad[4]['payload']['author'] = '/root'
                if mutation == 'unfinished': bad[3]['payload']['item']['kind'] = 'started'
                if mutation == 'foreign': bad[4]['payload']['recipient'] = '/other'
                if mutation == 'not-final': bad[4]['payload']['content'][0]['text'] = 'Message Type: MESSAGE\nPayload:\n{}'
                if mutation == 'no-assignment':
                    bad[4]['payload']['content'][0]['text'] = 'Message Type: FINAL_ANSWER\nTask name: /root\nSender: /root/reviewer\nPayload:\n{"status":"clean"}'
                with self.subTest(mutation=mutation):
                    try: parsed = self.parse(bad, Path(d))
                    except runner.EvalFailure: continue
                    self.assertFalse(any(r.get('prompt') for r in parsed['reviewers']))


if __name__ == '__main__':
    unittest.main()
