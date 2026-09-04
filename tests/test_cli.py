"""Temporary-repository acceptance tests for the project-state command surface."""

from __future__ import annotations

import contextlib
import io
import os
import tempfile
import unittest
from pathlib import Path

from engineering_method.backlog import load_backlog, render_backlog
from engineering_method.cli import main
from engineering_method.continuity import RunState, create_run, recover_run
from engineering_method.features import load_features
from engineering_method.gh import RemoteIssue, RepositoryRef
from engineering_method.issues import migrate_backlog, reconcile_queue


@contextlib.contextmanager
def in_directory(path: Path):
    previous = Path.cwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(previous)


class FakeMigrationGateway:
    def __init__(self) -> None:
        self.issues: list[RemoteIssue] = []

    def list_method_issues(self, repository: RepositoryRef) -> list[RemoteIssue]:
        return list(self.issues)

    def create_issue(self, repository: RepositoryRef, *, title: str, body: str, labels: tuple[str, ...], language: str = "en") -> RemoteIssue:
        issue = RemoteIssue(len(self.issues) + 1, title, body, "OPEN", labels)
        self.issues.append(issue)
        return issue

    def close_issue(self, repository: RepositoryRef, number: int) -> None:
        return None

    def ensure_sub_issue(self, repository: RepositoryRef, parent: int, child: int) -> None:
        return None

    def ensure_blocked_by(self, repository: RepositoryRef, blocked: int, blocker: int) -> None:
        return None


class ProjectStateAcceptanceTests(unittest.TestCase):
    def test_local_lifecycle_feature_migration_queue_and_recovery(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            with in_directory(root):
                self.assertEqual(main(["backlog", "init", "--project-key", "EM"]), 0)
                self.assertEqual(main(["backlog", "add", "--id", "EM-001", "--title", "State", "--priority", "P1"]), 0)
                self.assertEqual(main(["backlog", "start", "EM-001"]), 0)
                self.assertEqual(main(["backlog", "complete", "EM-001"]), 0)
                self.assertEqual(main(["feature", "add", "--id", "F-001", "--name", "State", "--summary", "Durable state.", "--related", "EM-001"]), 0)
            document = load_backlog(root / "BACKLOG.md")
            self.assertEqual(document.items[0].id, "EM-001")
            self.assertEqual(document.items[0].status.value, "complete")
            self.assertEqual(load_features(root / "FEATURES.md").features[0].related_backlog_ids, ("EM-001",))
            migrated = migrate_backlog(document, FakeMigrationGateway(), RepositoryRef("peter", "method"), language="en")
            self.assertEqual(migrated.mode, "github-cache")
            sent: list[str] = []
            reconcile_queue(root, {"id": "offline-complete", "kind": "complete"}, send=lambda event: sent.append(str(event["id"])))
            self.assertEqual(sent, ["offline-complete"])
            create_run(root, RunState("EM-001", "implementation", "verify", "continue", completed_slices=("slice-1",), active_agent_ids=("gone",)), "resume")
            recovered = recover_run(root, "EM-001", git_probe=lambda: "head", canonical_probe=lambda _: False, live_agent_ids=())
            self.assertEqual(recovered.completed_slices, ("slice-1",))
            self.assertEqual(recovered.redispatchable_agent_ids, ("gone",))

    def test_concise_nonzero_command_errors(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            errors = io.StringIO()
            with in_directory(root), contextlib.redirect_stderr(errors):
                main(["backlog", "init", "--project-key", "EM"])
                self.assertEqual(main(["backlog", "add", "--id", "EM-001", "--title", "State", "--priority", "bad"]), 2)
                self.assertEqual(main(["backlog", "add", "--id", "EM-001", "--title", "State", "--priority", "P1"]), 0)
                self.assertEqual(main(["backlog", "add", "--id", "EM-001", "--title", "Duplicate", "--priority", "P1"]), 2)
                cache = load_backlog(root / "BACKLOG.md")
                (root / "BACKLOG.md").write_text(render_backlog(type(cache)(cache.project_key, "github-cache", cache.items)), encoding="utf-8")
                self.assertEqual(main(["backlog", "start", "EM-001"]), 2)
                self.assertEqual(main(["continuity-state", "event", "EM-001", "{"]), 2)
            self.assertLessEqual(max(len(line) for line in errors.getvalue().splitlines()), 120)


if __name__ == "__main__":
    unittest.main()
