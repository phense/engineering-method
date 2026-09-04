"""Tests for the injected, network-free GitHub Issues boundary."""

from __future__ import annotations

import json
import unittest

from engineering_method.gh import GhResult, GitHubIssuesGateway, RepositoryRef
from tests.fakes import ExpectedGhCall, FakeGhRunner


def result(payload: object, *, returncode: int = 0, stderr: str = "") -> GhResult:
    return GhResult(returncode=returncode, stdout=json.dumps(payload), stderr=stderr)


class GitHubDetectionTests(unittest.TestCase):
    def test_detects_a_writable_authenticated_repository_for_each_allowed_permission(self) -> None:
        for permission in ("WRITE", "MAINTAIN", "ADMIN"):
            with self.subTest(permission=permission):
                runner = FakeGhRunner((ExpectedGhCall(
                    ("repo", "view", "--json", "nameWithOwner,viewerPermission"),
                    result({"nameWithOwner": "peter/engineering-method", "viewerPermission": permission}),
                ),))
                repository = GitHubIssuesGateway(runner).detect_writable_repository()
                self.assertEqual(repository, RepositoryRef("peter", "engineering-method"))
                runner.assert_drained()

    def test_no_remote_authentication_or_read_only_access_is_not_a_workflow_error(self) -> None:
        for response in (
            GhResult(1, "", "no git remotes configured"),
            GhResult(1, "", "authentication required"),
            result({"nameWithOwner": "peter/engineering-method", "viewerPermission": "READ"}),
        ):
            with self.subTest(response=response):
                runner = FakeGhRunner((ExpectedGhCall(
                    ("repo", "view", "--json", "nameWithOwner,viewerPermission"), response
                ),))
                self.assertIsNone(GitHubIssuesGateway(runner).detect_writable_repository())
                runner.assert_drained()

    def test_malformed_detection_json_is_not_treated_as_a_repository(self) -> None:
        runner = FakeGhRunner((ExpectedGhCall(
            ("repo", "view", "--json", "nameWithOwner,viewerPermission"), GhResult(0, "[", "")
        ),))
        self.assertIsNone(GitHubIssuesGateway(runner).detect_writable_repository())


class GitHubIssueOperationsTests(unittest.TestCase):
    def setUp(self) -> None:
        self.repository = RepositoryRef("peter", "engineering-method")

    def test_lists_complete_remote_issues_and_rejects_partial_responses(self) -> None:
        complete = [{
            "number": 12, "title": "EM-002 State", "body": "marker", "state": "OPEN",
            "labels": [{"name": "engineering-method"}],
        }]
        runner = FakeGhRunner((ExpectedGhCall(
            ("issue", "list", "--repo", "peter/engineering-method", "--state", "all", "--label", "engineering-method", "--json", "number,title,body,state,labels", "--limit", "100"),
            result(complete),
        ),))
        issues = GitHubIssuesGateway(runner).list_method_issues(self.repository)
        self.assertEqual(issues[0].number, 12)
        self.assertEqual(issues[0].labels, ("engineering-method",))
        runner.assert_drained()

        partial_runner = FakeGhRunner((ExpectedGhCall(
            ("issue", "list", "--repo", "peter/engineering-method", "--state", "all", "--label", "engineering-method", "--json", "number,title,body,state,labels", "--limit", "100"),
            result([{"number": 12, "title": "missing fields"}]),
        ),))
        with self.assertRaisesRegex(ValueError, "partial"):
            GitHubIssuesGateway(partial_runner).list_method_issues(self.repository)

    def test_nonzero_issue_command_raises_without_claiming_success(self) -> None:
        runner = FakeGhRunner((ExpectedGhCall(
            ("issue", "list", "--repo", "peter/engineering-method", "--state", "all", "--label", "engineering-method", "--json", "number,title,body,state,labels", "--limit", "100"),
            GhResult(1, "", "connection refused"),
        ),))
        with self.assertRaisesRegex(RuntimeError, "connection refused"):
            GitHubIssuesGateway(runner).list_method_issues(self.repository)

    def test_creates_an_issue_with_argument_list_and_explicit_stdin_body(self) -> None:
        body = "<!-- engineering-method:issue {\"schema_version\":1} -->"
        runner = FakeGhRunner((ExpectedGhCall(
            ("api", "--method", "POST", "repos/peter/engineering-method/issues", "--input", "-"),
            result({"number": 13, "title": "EM-002 State", "body": body, "state": "OPEN", "labels": [{"name": "engineering-method"}]}),
            stdin='{"title":"EM-002 State","body":"<!-- engineering-method:issue {\\"schema_version\\":1} -->","labels":["engineering-method"]}',
        ),))
        created = GitHubIssuesGateway(runner).create_issue(
            self.repository, title="EM-002 State", body=body, labels=("engineering-method",)
        )
        self.assertEqual(created.number, 13)
        runner.assert_drained()

    def test_relationship_calls_use_explicit_argument_lists(self) -> None:
        runner = FakeGhRunner((
            ExpectedGhCall(("api", "--method", "POST", "repos/peter/engineering-method/issues/10/sub_issues", "-f", "sub_issue_id=11"), GhResult(0, "", "")),
            ExpectedGhCall(("api", "--method", "POST", "repos/peter/engineering-method/issues/11/dependencies/blocked_by", "-f", "issue_id=10"), GhResult(0, "", "")),
        ))
        gateway = GitHubIssuesGateway(runner)
        gateway.ensure_sub_issue(self.repository, parent=10, child=11)
        gateway.ensure_blocked_by(self.repository, blocked=11, blocker=10)
        runner.assert_drained()


if __name__ == "__main__":
    unittest.main()
