"""Idempotent local-backlog migration and offline GitHub mutation reconciliation."""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Callable, Mapping, Protocol

from .backlog import BacklogDocument, render_backlog
from .files import append_jsonl, atomic_write_text
from .gh import RemoteIssue, RepositoryRef
from .models import BacklogItem, TaskStatus


ISSUE_PREFIX = "<!-- engineering-method:issue "


class IssueGateway(Protocol):
    def detect_writable_repository(self) -> RepositoryRef | None: ...
    def list_method_issues(self, repository: RepositoryRef) -> list[RemoteIssue]: ...
    def create_issue(self, repository: RepositoryRef, *, title: str, body: str, labels: tuple[str, ...], language: str = "en") -> RemoteIssue: ...
    def close_issue(self, repository: RepositoryRef, number: int) -> None: ...
    def ensure_sub_issue(self, repository: RepositoryRef, parent: int, child: int) -> None: ...
    def ensure_blocked_by(self, repository: RepositoryRef, blocked: int, blocker: int) -> None: ...


@dataclass(frozen=True)
class StateCheckResult:
    document: BacklogDocument
    reason: str


def _marker(backlog_id: str) -> str:
    return f'{ISSUE_PREFIX}{{"schema_version":1,"backlog_id":"{backlog_id}"}} -->'


def _remote_map(items: tuple[BacklogItem, ...], remote: list[RemoteIssue]) -> dict[str, RemoteIssue]:
    known = {item.id for item in items}
    mapped: dict[str, RemoteIssue] = {}
    for issue in remote:
        matches = [item_id for item_id in known if _marker(item_id) in issue.body]
        if len(matches) > 1:
            raise ValueError("remote issue has ambiguous method markers")
        if not matches:
            if ISSUE_PREFIX in issue.body:
                raise ValueError("remote issue has an unknown method marker")
            continue
        item_id = matches[0]
        if item_id in mapped:
            raise ValueError("duplicate remote marker")
        mapped[item_id] = issue
    return mapped


def _labels(item: BacklogItem) -> tuple[str, ...]:
    labels = ["engineering-method", f"priority:{item.priority.value.lower()}"]
    if item.status is not TaskStatus.COMPLETE:
        labels.append(f"status:{item.status.value.replace('_', '-')}")
    return tuple(labels)


def migrate_backlog(document: BacklogDocument, gateway: IssueGateway, repository: RepositoryRef, *, language: str) -> BacklogDocument:
    """Create missing issues before relationships, then commit cache mode in memory."""
    if language != "en":
        raise ValueError("GitHub-authored content must declare English")
    mapping = _remote_map(document.items, gateway.list_method_issues(repository))
    created: set[str] = set()
    for item in document.items:
        if item.id not in mapping:
            mapping[item.id] = gateway.create_issue(
                repository, title=f"{item.id}: {item.title}", body=_marker(item.id), labels=_labels(item), language=language
            )
            created.add(item.id)
    for item in document.items:
        if item.status is TaskStatus.COMPLETE and item.id in created:
            gateway.close_issue(repository, mapping[item.id].number)
    for item in document.items:
        if item.parent_id is not None and (item.id in created or item.parent_id in created):
            gateway.ensure_sub_issue(repository, mapping[item.parent_id].number, mapping[item.id].number)
        for dependency in item.depends_on:
            if item.id in created or dependency in created:
                gateway.ensure_blocked_by(repository, mapping[item.id].number, mapping[dependency].number)
    return BacklogDocument(document.project_key, "github-cache", document.items)


def workflow_state_check(path: Path, gateway: IssueGateway) -> StateCheckResult:
    """Migrate automatically only when a reachable authenticated writable remote exists."""
    from .backlog import load_backlog
    document = load_backlog(path)
    repository = gateway.detect_writable_repository()
    if repository is None:
        return StateCheckResult(document, "no writable authenticated GitHub repository")
    if document.mode == "github-cache":
        return StateCheckResult(document, "GitHub Issues cache already canonical")
    migrated = migrate_backlog(document, gateway, repository, language="en")
    atomic_write_text(path, render_backlog(migrated))
    return StateCheckResult(migrated, "migrated local backlog to canonical GitHub Issues")


def reconcile_queue(root: Path, mutation: Mapping[str, object], *, send: Callable[[dict[str, object]], None]) -> None:
    """Append a mutation then acknowledgement only after causal successful delivery."""
    if not isinstance(mutation.get("id"), str) or not mutation["id"]:
        raise ValueError("queued GitHub mutation requires a non-empty id")
    queue = root / ".engineering-method" / "github-queue.jsonl"
    event = dict(mutation)
    event["schema_version"] = 1
    event["state"] = "pending"
    append_jsonl(queue, event)
    send(event)
    append_jsonl(queue, {"schema_version": 1, "id": event["id"], "state": "acknowledged"})
