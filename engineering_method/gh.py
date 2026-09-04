"""Injected GitHub CLI boundary; ordinary tests never invoke a real subprocess."""

from __future__ import annotations

from dataclasses import dataclass
import json
import subprocess
from typing import Protocol, Sequence


@dataclass(frozen=True)
class GhResult:
    returncode: int
    stdout: str
    stderr: str


class GhRunner(Protocol):
    def run(self, args: Sequence[str], *, stdin: str | None = None) -> GhResult: ...


@dataclass(frozen=True)
class RepositoryRef:
    owner: str
    name: str

    @property
    def full_name(self) -> str:
        return f"{self.owner}/{self.name}"


@dataclass(frozen=True)
class RemoteIssue:
    number: int
    title: str
    body: str
    state: str
    labels: tuple[str, ...]


class SubprocessGhRunner:
    """The sole live-process adapter, deliberately using a fixed argument list."""

    def run(self, args: Sequence[str], *, stdin: str | None = None) -> GhResult:
        completed = subprocess.run(
            ["gh", *args], input=stdin, text=True, capture_output=True, check=False
        )
        return GhResult(completed.returncode, completed.stdout, completed.stderr)


def _json_result(result: GhResult, *, operation: str) -> object:
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or f"gh {operation} failed")
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError as error:
        raise ValueError(f"gh {operation} returned malformed JSON") from error


def _remote_issue(payload: object) -> RemoteIssue:
    if not isinstance(payload, dict):
        raise ValueError("gh issue response is partial")
    required = {"number", "title", "body", "state", "labels"}
    if not required <= payload.keys() or not isinstance(payload["labels"], list):
        raise ValueError("gh issue response is partial")
    labels: list[str] = []
    for label in payload["labels"]:
        if not isinstance(label, dict) or not isinstance(label.get("name"), str):
            raise ValueError("gh issue response is partial")
        labels.append(label["name"])
    if not all(isinstance(payload[field], expected) for field, expected in (("number", int), ("title", str), ("body", str), ("state", str))):
        raise ValueError("gh issue response is partial")
    return RemoteIssue(payload["number"], payload["title"], payload["body"], payload["state"], tuple(labels))


class GitHubIssuesGateway:
    """All current GitHub Issue transport shapes behind an injectable runner."""

    def __init__(self, runner: GhRunner | None = None) -> None:
        self._runner = runner or SubprocessGhRunner()

    def detect_writable_repository(self) -> RepositoryRef | None:
        result = self._runner.run(("repo", "view", "--json", "nameWithOwner,viewerPermission"))
        if result.returncode != 0:
            return None
        try:
            payload = json.loads(result.stdout)
        except json.JSONDecodeError:
            return None
        if not isinstance(payload, dict) or payload.get("viewerPermission") not in {"WRITE", "MAINTAIN", "ADMIN"}:
            return None
        name_with_owner = payload.get("nameWithOwner")
        if not isinstance(name_with_owner, str) or name_with_owner.count("/") != 1:
            return None
        owner, name = name_with_owner.split("/", 1)
        return RepositoryRef(owner, name) if owner and name else None

    def list_method_issues(self, repository: RepositoryRef) -> list[RemoteIssue]:
        payload = _json_result(self._runner.run((
            "issue", "list", "--repo", repository.full_name, "--state", "all", "--label",
            "engineering-method", "--json", "number,title,body,state,labels", "--limit", "100",
        )), operation="issue list")
        if not isinstance(payload, list):
            raise ValueError("gh issue list response is partial")
        return [_remote_issue(entry) for entry in payload]

    def create_issue(self, repository: RepositoryRef, *, title: str, body: str, labels: Sequence[str], language: str = "en") -> RemoteIssue:
        if language != "en":
            raise ValueError("GitHub-authored content must declare English")
        request = json.dumps({"title": title, "body": body, "labels": list(labels)}, separators=(",", ":"))
        payload = _json_result(self._runner.run((
            "api", "--method", "POST", f"repos/{repository.full_name}/issues", "--input", "-"
        ), stdin=request), operation="issue create")
        return _remote_issue(payload)

    def close_issue(self, repository: RepositoryRef, number: int) -> None:
        result = self._runner.run(("api", "--method", "PATCH", f"repos/{repository.full_name}/issues/{number}", "-f", "state=closed"))
        if result.returncode != 0:
            raise RuntimeError(result.stderr.strip() or "gh issue close failed")

    def ensure_sub_issue(self, repository: RepositoryRef, parent: int, child: int) -> None:
        result = self._runner.run((
            "api", "--method", "POST", f"repos/{repository.full_name}/issues/{parent}/sub_issues",
            "-f", f"sub_issue_id={child}",
        ))
        if result.returncode != 0:
            raise RuntimeError(result.stderr.strip() or "gh sub-issue relationship failed")

    def ensure_blocked_by(self, repository: RepositoryRef, blocked: int, blocker: int) -> None:
        result = self._runner.run((
            "api", "--method", "POST", f"repos/{repository.full_name}/issues/{blocked}/dependencies/blocked_by",
            "-f", f"issue_id={blocker}",
        ))
        if result.returncode != 0:
            raise RuntimeError(result.stderr.strip() or "gh dependency relationship failed")
