"""Test doubles shared by Engineering Method state tests."""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass
import json
import re
from typing import Sequence

from engineering_method.gh import GhResult


@dataclass(frozen=True)
class ExpectedGhCall:
    args: tuple[str, ...]
    result: GhResult
    stdin: str | None = None


class FakeGhRunner:
    """An ordered gh boundary that rejects each unexpected command immediately."""

    def __init__(self, expected: Sequence[ExpectedGhCall]) -> None:
        self._expected = deque(expected)

    def run(self, args: Sequence[str], *, stdin: str | None = None) -> GhResult:
        if not self._expected:
            raise AssertionError(f"unexpected gh call: {list(args)!r}")
        expected = self._expected.popleft()
        if tuple(args) != expected.args or stdin != expected.stdin:
            raise AssertionError(f"expected {expected.args!r} with {expected.stdin!r}, got {list(args)!r} with {stdin!r}")
        return expected.result

    def assert_drained(self) -> None:
        if self._expected:
            raise AssertionError(f"unconsumed gh calls: {list(self._expected)!r}")


class MutableGitHubRunner:
    """A persistent in-memory GitHub REST surface with no subprocess or network."""

    def __init__(
        self,
        *,
        repository: str = "peter/engineering-method",
        permission: str = "WRITE",
        issues: Sequence[dict[str, object]] = (),
        labels: Sequence[dict[str, str]] = (),
        page_size: int = 100,
    ) -> None:
        self.repository = repository
        self.permission = permission
        self.issues = [json.loads(json.dumps(issue)) for issue in issues]
        self.labels = {label["name"]: dict(label) for label in labels}
        self.page_size = page_size
        self.sub_issues: dict[int, set[int]] = {}
        self.blocked_by: dict[int, set[int]] = {}
        self.calls: list[tuple[tuple[str, ...], str | None]] = []
        self.mutation_count = 0
        self._failures: dict[str, int] = {}

    def fail_once(self, operation: str) -> None:
        self._failures[operation] = self._failures.get(operation, 0) + 1

    def _failure(self, operation: str) -> GhResult | None:
        remaining = self._failures.get(operation, 0)
        if not remaining:
            return None
        self._failures[operation] = remaining - 1
        return GhResult(1, "", f"injected {operation} failure")

    def _pages(self, values: list[object]) -> str:
        pages = [
            values[index : index + self.page_size]
            for index in range(0, len(values), self.page_size)
        ]
        return json.dumps(pages or [[]])

    def _issue_by_number(self, number: int) -> dict[str, object]:
        for issue in self.issues:
            if issue["number"] == number:
                return issue
        raise AssertionError(f"unknown issue number: {number}")

    def _issue_by_id(self, database_id: int) -> dict[str, object]:
        for issue in self.issues:
            if issue["id"] == database_id:
                return issue
        raise AssertionError(f"unknown issue database id: {database_id}")

    def run(self, args: Sequence[str], *, stdin: str | None = None) -> GhResult:
        command = tuple(args)
        self.calls.append((command, stdin))
        if command == ("repo", "view", "--json", "nameWithOwner,viewerPermission"):
            failure = self._failure("detect")
            if failure:
                return failure
            return GhResult(
                0,
                json.dumps(
                    {"nameWithOwner": self.repository, "viewerPermission": self.permission}
                ),
                "",
            )

        if command[:3] == ("api", "--paginate", "--slurp"):
            endpoint = command[3]
            if endpoint == f"repos/{self.repository}/issues?state=all&per_page=100":
                return GhResult(0, self._pages(self.issues), "")
            if endpoint == f"repos/{self.repository}/labels?per_page=100":
                return GhResult(0, self._pages(list(self.labels.values())), "")
            relation = re.fullmatch(
                rf"repos/{re.escape(self.repository)}/issues/(\d+)/(sub_issues|dependencies/blocked_by)\?per_page=100",
                endpoint,
            )
            if relation:
                number = int(relation.group(1))
                ids = (
                    self.sub_issues.get(number, set())
                    if relation.group(2) == "sub_issues"
                    else self.blocked_by.get(number, set())
                )
                related = [self._issue_by_id(database_id) for database_id in sorted(ids)]
                return GhResult(0, self._pages(related), "")

        if command[:2] == ("label", "create"):
            name = command[2]
            operation = "create-label"
            failure = self._failure(operation)
            if failure:
                return failure
            expected_prefix = ("label", "create", name, "--repo", self.repository)
            if command[:5] != expected_prefix:
                raise AssertionError(f"unexpected label command: {command!r}")
            color = command[command.index("--color") + 1]
            description = command[command.index("--description") + 1]
            self.labels[name] = {"name": name, "color": color, "description": description}
            self.mutation_count += 1
            return GhResult(0, "", "")

        if command[:3] == ("api", "--method", "POST") and command[3] == f"repos/{self.repository}/issues":
            failure = self._failure("create-issue")
            if failure:
                return failure
            if command[4:] != ("--input", "-") or stdin is None:
                raise AssertionError("issue creation must use JSON stdin")
            payload = json.loads(stdin)
            number = max((int(issue["number"]) for issue in self.issues), default=0) + 1
            database_id = max((int(issue["id"]) for issue in self.issues), default=1000) + 1
            issue = {
                "id": database_id,
                "number": number,
                "title": payload["title"],
                "body": payload["body"],
                "state": "open",
                "labels": [{"name": name} for name in payload["labels"]],
                "updated_at": "2026-09-04T12:00:00Z",
            }
            self.issues.append(issue)
            self.mutation_count += 1
            return GhResult(0, json.dumps(issue), "")

        issue_patch = re.fullmatch(
            rf"repos/{re.escape(self.repository)}/issues/(\d+)",
            command[3] if len(command) > 3 else "",
        )
        if command[:3] == ("api", "--method", "PATCH") and issue_patch:
            failure = self._failure("update-issue")
            if failure:
                return failure
            if command[4:] != ("--input", "-") or stdin is None:
                raise AssertionError("issue updates must use JSON stdin")
            issue = self._issue_by_number(int(issue_patch.group(1)))
            payload = json.loads(stdin)
            for field in ("title", "body", "state"):
                if field in payload:
                    issue[field] = payload[field]
            if "labels" in payload:
                issue["labels"] = [{"name": name} for name in payload["labels"]]
            issue["updated_at"] = "2026-09-04T12:30:00Z"
            self.mutation_count += 1
            return GhResult(0, json.dumps(issue), "")

        relation = re.fullmatch(
            rf"repos/{re.escape(self.repository)}/issues/(\d+)/(sub_issues|dependencies/blocked_by)",
            command[3] if len(command) > 3 else "",
        )
        if len(command) >= 6 and command[0] == "api" and relation:
            method = command[2]
            if command[1] != "--method" or command[4] != "-F":
                raise AssertionError("relationship mutations must use integer -F fields")
            field, raw_value = command[5].split("=", 1)
            if field not in {"sub_issue_id", "issue_id"} or not raw_value.isdigit():
                raise AssertionError("relationship mutation field must be an integer")
            database_id = int(raw_value)
            number = int(relation.group(1))
            target = (
                self.sub_issues.setdefault(number, set())
                if relation.group(2) == "sub_issues"
                else self.blocked_by.setdefault(number, set())
            )
            operation = {
                ("POST", "sub_issues"): "add-sub-issue",
                ("DELETE", "sub_issues"): "remove-sub-issue",
                ("POST", "dependencies/blocked_by"): "add-blocker",
                ("DELETE", "dependencies/blocked_by"): "remove-blocker",
            }.get((method, relation.group(2)))
            if operation is None:
                raise AssertionError(f"unexpected relation command: {command!r}")
            failure = self._failure(operation)
            if failure:
                return failure
            if method == "POST":
                if operation == "add-sub-issue" and any(
                    database_id in children
                    for parent, children in self.sub_issues.items()
                    if parent != number
                ):
                    return GhResult(1, "", "sub-issue already has a parent")
                target.add(database_id)
            else:
                target.discard(database_id)
            self.mutation_count += 1
            return GhResult(0, "", "")

        raise AssertionError(f"unexpected gh call: {command!r} with {stdin!r}")
