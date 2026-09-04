"""Tests for the injected, network-free GitHub Issues boundary."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from engineering_method.gh import GhResult, GitHubIssuesGateway, RemoteIssue, RepositoryRef
from engineering_method.backlog import BacklogDocument, load_backlog
from engineering_method.issues import migrate_backlog, reconcile_queue, workflow_state_check
from engineering_method.models import BacklogItem, Priority, TaskStatus
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


class MigrationGateway:
    def __init__(self, remote: list[RemoteIssue] | None = None, *, writable: bool = True) -> None:
        self.remote = list(remote or [])
        self.writable = writable
        self.calls: list[tuple[object, ...]] = []

    def detect_writable_repository(self) -> RepositoryRef | None:
        return RepositoryRef("peter", "engineering-method") if self.writable else None

    def list_method_issues(self, repository: RepositoryRef) -> list[RemoteIssue]:
        self.calls.append(("list", repository))
        return list(self.remote)

    def create_issue(self, repository: RepositoryRef, *, title: str, body: str, labels: tuple[str, ...], language: str = "en") -> RemoteIssue:
        self.calls.append(("create", title, body, labels, language))
        issue = RemoteIssue(len(self.remote) + 1, title, body, "OPEN", labels)
        self.remote.append(issue)
        return issue

    def close_issue(self, repository: RepositoryRef, number: int) -> None:
        self.calls.append(("close", number))

    def ensure_sub_issue(self, repository: RepositoryRef, parent: int, child: int) -> None:
        self.calls.append(("sub", parent, child))

    def ensure_blocked_by(self, repository: RepositoryRef, blocked: int, blocker: int) -> None:
        self.calls.append(("blocked", blocked, blocker))


def backlog_item(identifier: str, status: TaskStatus, *, parent_id: str | None = None, depends_on: tuple[str, ...] = ()) -> BacklogItem:
    return BacklogItem(identifier, f"English {identifier}", status, Priority.P1, parent_id, depends_on, "", "2026-09-04T10:20:30Z")


class IssueMigrationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.repository = RepositoryRef("peter", "engineering-method")

    def test_migrates_before_relationships_closes_completed_and_is_idempotent(self) -> None:
        document = BacklogDocument("EM", "local", (
            backlog_item("EM-001", TaskStatus.OPEN),
            backlog_item("EM-001.1", TaskStatus.BLOCKED, parent_id="EM-001", depends_on=("EM-002",)),
            backlog_item("EM-002", TaskStatus.COMPLETE),
        ))
        gateway = MigrationGateway()
        migrated = migrate_backlog(document, gateway, RepositoryRef("peter", "engineering-method"), language="en")
        self.assertEqual(migrated.mode, "github-cache")
        create_positions = [index for index, call in enumerate(gateway.calls) if call[0] == "create"]
        relationship_positions = [index for index, call in enumerate(gateway.calls) if call[0] in {"sub", "blocked"}]
        self.assertLess(max(create_positions), min(relationship_positions))
        self.assertIn(("close", 3), gateway.calls)
        first_count = len(gateway.calls)
        migrate_backlog(migrated, gateway, RepositoryRef("peter", "engineering-method"), language="en")
        self.assertEqual(len(gateway.calls), first_count + 1)

    def test_rejects_non_english_outbound_operations_and_duplicate_markers(self) -> None:
        document = BacklogDocument("EM", "local", (backlog_item("EM-001", TaskStatus.OPEN),))
        marker = '<!-- engineering-method:issue {"schema_version":1,"backlog_id":"EM-001"} -->'
        duplicate = [RemoteIssue(1, "EM-001", marker, "OPEN", ()), RemoteIssue(2, "other", marker, "OPEN", ())]
        with self.assertRaisesRegex(ValueError, "English"):
            migrate_backlog(document, MigrationGateway(), RepositoryRef("peter", "engineering-method"), language="de")
        with self.assertRaisesRegex(ValueError, "duplicate"):
            migrate_backlog(document, MigrationGateway(duplicate), RepositoryRef("peter", "engineering-method"), language="en")

    def test_workflow_state_check_keeps_local_mode_without_writable_remote(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "BACKLOG.md"
            path.write_text("# Backlog\n\n- ⭕ `EM-001` **P1** Local\n", encoding="utf-8")
            outcome = workflow_state_check(path, MigrationGateway(writable=False))
            self.assertEqual(outcome.reason, "no writable authenticated GitHub repository")
            self.assertEqual(load_backlog(path).mode, "local")

    def test_reconciliation_appends_acknowledgements_in_causal_order(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            sent: list[str] = []
            reconcile_queue(root, {"id": "one", "kind": "change"}, send=lambda event: sent.append(event["id"]))
            reconcile_queue(root, {"id": "two", "kind": "change"}, send=lambda event: sent.append(event["id"]))
            self.assertEqual(sent, ["one", "two"])

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
