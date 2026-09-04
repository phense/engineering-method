"""Canonical local backlog parsing, rendering, ordering, and archiving."""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
import re
from typing import Iterable, Literal

from .models import (
    BacklogItem,
    PROJECT_KEY_PATTERN,
    Priority,
    TaskStatus,
    parse_task_id,
    validate_backlog_items,
)


SCHEMA_VERSION = 1
MARKER_PATTERN = re.compile(r"^\s*<!-- engineering-method:backlog (?P<payload>\{.*\}) -->\s*$")
DOCUMENT_MARKER_PATTERN = re.compile(
    r"^<!-- engineering-method:backlog-document (?P<payload>\{.*\}) -->$"
)
DISPLAY_PATTERN = re.compile(
    r"^(?P<indent>\s*)-\s+(?P<emoji>[⭕🔄✅❌])\s+`(?P<id>[^`]+)`\s+"
    r"(?:\*\*(?P<priority>P[0-3])\*\*\s+)?(?P<title>.+)$"
)
STATUS_EMOJI = {
    TaskStatus.OPEN: "⭕",
    TaskStatus.IN_PROGRESS: "🔄",
    TaskStatus.COMPLETE: "✅",
    TaskStatus.BLOCKED: "❌",
}
EMOJI_STATUS = {emoji: status for status, emoji in STATUS_EMOJI.items()}
PRIORITY_RANK = {Priority.P0: 0, Priority.P1: 1, Priority.P2: 2, Priority.P3: 3}
GITHUB_CACHE_NOTICE = "Generated GitHub Issues cache — do not edit"


@dataclass(frozen=True)
class BacklogDocument:
    """The local canonical backlog or generated GitHub cache."""

    project_key: str
    mode: Literal["local", "github-cache"]
    items: tuple[BacklogItem, ...]

    def __post_init__(self) -> None:
        if not PROJECT_KEY_PATTERN.fullmatch(self.project_key):
            raise ValueError("backlog project key must be uppercase alphanumeric")
        if self.mode not in {"local", "github-cache"}:
            raise ValueError("backlog mode must be local or github-cache")
        if not isinstance(self.items, tuple):
            raise ValueError("backlog items must be a tuple")
        validated = validate_backlog_items(self.items)
        for entry in validated:
            item_project_key, _ = parse_task_id(entry.id)
            if item_project_key != self.project_key:
                raise ValueError("all backlog IDs must use the document project key")


def _task_sort_key(identifier: str) -> tuple[tuple[int, ...], str]:
    _, components = parse_task_id(identifier)
    return components, identifier


def _root_id(entry: BacklogItem, by_id: dict[str, BacklogItem]) -> str:
    current = entry
    while current.parent_id is not None:
        current = by_id[current.parent_id]
    return current.id


def _render_order_for_group(root_id: str, by_id: dict[str, BacklogItem]) -> list[BacklogItem]:
    children: dict[str | None, list[BacklogItem]] = {}
    for entry in by_id.values():
        if _root_id(entry, by_id) == root_id:
            children.setdefault(entry.parent_id, []).append(entry)
    for siblings in children.values():
        siblings.sort(key=lambda entry: _task_sort_key(entry.id))

    ordered: list[BacklogItem] = []

    def visit(entry: BacklogItem) -> None:
        ordered.append(entry)
        for child in children.get(entry.id, []):
            visit(child)

    roots = children.get(None, [])
    if len(roots) != 1 or roots[0].id != root_id:
        raise ValueError("backlog hierarchy must have one top-level group root")
    visit(roots[0])
    return ordered


def ordered_items(items: Iterable[BacklogItem]) -> list[BacklogItem]:
    """Order top-level groups unblocker-first without separating children."""
    materialized = validate_backlog_items(items)
    by_id = {entry.id: entry for entry in materialized}
    if not by_id:
        return []
    group_ids = {_root_id(entry, by_id) for entry in by_id.values()}
    group_dependencies: dict[str, set[str]] = {identifier: set() for identifier in group_ids}
    blocked_groups: set[str] = set()
    unblocker_groups: set[str] = set()
    for entry in by_id.values():
        group_id = _root_id(entry, by_id)
        if entry.status is TaskStatus.BLOCKED:
            blocked_groups.add(group_id)
        for dependency in entry.depends_on:
            dependency_group = _root_id(by_id[dependency], by_id)
            if dependency_group != group_id:
                group_dependencies[group_id].add(dependency_group)
                if entry.status is TaskStatus.BLOCKED:
                    unblocker_groups.add(dependency_group)

    group_priorities = {
        group_id: min(
            PRIORITY_RANK[entry.priority]
            for entry in by_id.values()
            if _root_id(entry, by_id) == group_id
        )
        for group_id in group_ids
    }

    def group_sort_key(group_id: str) -> tuple[int, int, tuple[int, ...], str]:
        rank = 0 if group_id in unblocker_groups else 1 if group_id in blocked_groups else 2
        components, identifier = _task_sort_key(group_id)
        return rank, group_priorities[group_id], components, identifier

    pending = set(group_ids)
    placed: set[str] = set()
    group_order: list[str] = []
    while pending:
        ready = sorted(
            (group_id for group_id in pending if group_dependencies[group_id] <= placed),
            key=group_sort_key,
        )
        if not ready:
            raise ValueError("backlog dependency cycle detected")
        next_group = ready[0]
        pending.remove(next_group)
        placed.add(next_group)
        group_order.append(next_group)

    return [entry for group_id in group_order for entry in _render_order_for_group(group_id, by_id)]


def _marker_payload(entry: BacklogItem) -> str:
    payload = {
        "schema_version": SCHEMA_VERSION,
        "id": entry.id,
        "title": entry.title,
        "status": entry.status.value,
        "priority": entry.priority.value,
        "parent_id": entry.parent_id,
        "depends_on": list(entry.depends_on),
        "notes": entry.notes,
        "updated_at": entry.updated_at,
    }
    return json.dumps(payload, ensure_ascii=False, separators=(",", ":"))


def _document_marker(document: BacklogDocument) -> str:
    payload = {
        "schema_version": SCHEMA_VERSION,
        "project_key": document.project_key,
        "mode": document.mode,
    }
    return json.dumps(payload, separators=(",", ":"))


def render_backlog(document: BacklogDocument) -> str:
    """Render a readable, marker-backed canonical local document or cache."""
    header = [
        "# Backlog",
        f"<!-- engineering-method:backlog-document {_document_marker(document)} -->",
    ]
    if document.mode == "github-cache":
        header.extend(
            [
                "",
                GITHUB_CACHE_NOTICE,
                "GitHub Issues are canonical. Refresh this cache; do not make local canonical mutations.",
            ]
        )
    else:
        header.extend(
            [
                "",
                "This is the canonical local task register until GitHub Issues become writable and canonical.",
                "Keep stable IDs unchanged. Order groups unblocker-first, then priority and dependency order.",
            ]
        )
    header.extend(
        [
            "",
            "## Status legend",
            "",
            "- `⭕` Open",
            "- `🔄` In progress",
            "- `✅` Complete",
            "- `❌` Blocked",
            "",
            "## Tasks",
            "",
        ]
    )
    lines = header
    for entry in ordered_items(document.items):
        _, components = parse_task_id(entry.id)
        indent = "  " * (len(components) - 1)
        lines.append(f"{indent}<!-- engineering-method:backlog {_marker_payload(entry)} -->")
        lines.append(
            f"{indent}- {STATUS_EMOJI[entry.status]} `{entry.id}` **{entry.priority.value}** {entry.title}"
        )
        if entry.depends_on:
            dependencies = ", ".join(f"`{identifier}`" for identifier in entry.depends_on)
            lines.append(f"{indent}  - Depends on: {dependencies}")
        if entry.notes:
            lines.append(f"{indent}  - Notes: {entry.notes}")
    return "\n".join(lines).rstrip() + "\n"


def _parse_marker_item(payload: object, display: re.Match[str]) -> BacklogItem:
    if not isinstance(payload, dict) or payload.get("schema_version") != SCHEMA_VERSION:
        raise ValueError("backlog marker must use schema_version 1")
    required = {"id", "title", "status", "priority", "parent_id", "depends_on", "notes", "updated_at"}
    if not required <= payload.keys() or not isinstance(payload["depends_on"], list):
        raise ValueError("backlog marker is incomplete")
    try:
        entry = BacklogItem(
            id=payload["id"],
            title=payload["title"],
            status=TaskStatus(payload["status"]),
            priority=Priority(payload["priority"]),
            parent_id=payload["parent_id"],
            depends_on=tuple(payload["depends_on"]),
            notes=payload["notes"],
            updated_at=payload["updated_at"],
        )
    except (TypeError, ValueError) as error:
        raise ValueError("backlog marker contains invalid task data") from error
    if (
        display.group("id") != entry.id
        or display.group("title") != entry.title
        or display.group("priority") != entry.priority.value
        or EMOJI_STATUS[display.group("emoji")] is not entry.status
    ):
        raise ValueError("backlog marker and visible task disagree")
    return entry


def _load_marked_items(lines: list[str]) -> list[BacklogItem]:
    items: list[BacklogItem] = []
    for index, line in enumerate(lines):
        marker = MARKER_PATTERN.fullmatch(line)
        if marker is None:
            continue
        if index + 1 >= len(lines):
            raise ValueError("backlog marker must precede a visible task")
        display = DISPLAY_PATTERN.fullmatch(lines[index + 1])
        if display is None:
            raise ValueError("backlog marker must immediately precede a visible task")
        try:
            payload = json.loads(marker.group("payload"))
        except json.JSONDecodeError as error:
            raise ValueError("backlog marker contains invalid JSON") from error
        items.append(_parse_marker_item(payload, display))
    return items


def _load_legacy_items(lines: list[str]) -> list[BacklogItem]:
    items: list[BacklogItem] = []
    ancestry: list[tuple[int, BacklogItem]] = []
    for line in lines:
        display = DISPLAY_PATTERN.fullmatch(line)
        if display is None:
            continue
        indent = len(display.group("indent"))
        tail = display.group("title")
        title, separator, dependency_text = tail.partition(". Depends on ")
        dependencies = tuple(re.findall(r"`([^`]+)`", dependency_text)) if separator else ()
        while ancestry and ancestry[-1][0] >= indent:
            ancestry.pop()
        parent = ancestry[-1][1] if ancestry else None
        priority_value = display.group("priority")
        if priority_value is None and parent is None:
            raise ValueError("a top-level legacy backlog item requires a priority")
        entry = BacklogItem(
            id=display.group("id"),
            title=title,
            status=EMOJI_STATUS[display.group("emoji")],
            priority=Priority(priority_value) if priority_value is not None else parent.priority,
            parent_id=parent.id if parent is not None else None,
            depends_on=dependencies,
            notes="",
            updated_at="1970-01-01T00:00:00Z",
        )
        items.append(entry)
        ancestry.append((indent, entry))
    return items


def _load_document_metadata(lines: list[str]) -> tuple[str | None, str | None]:
    for line in lines:
        marker = DOCUMENT_MARKER_PATTERN.fullmatch(line)
        if marker is None:
            continue
        try:
            payload = json.loads(marker.group("payload"))
        except json.JSONDecodeError as error:
            raise ValueError("backlog document marker contains invalid JSON") from error
        if (
            not isinstance(payload, dict)
            or payload.get("schema_version") != SCHEMA_VERSION
            or not isinstance(payload.get("project_key"), str)
            or payload.get("mode") not in {"local", "github-cache"}
        ):
            raise ValueError("backlog document marker is invalid")
        return payload["project_key"], payload["mode"]
    return None, None


def load_backlog(path: Path) -> BacklogDocument:
    """Load a marker-backed document or migrate compatible legacy task lines in memory."""
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError as error:
        raise ValueError(f"cannot read backlog: {path}") from error
    project_key, metadata_mode = _load_document_metadata(lines)
    items = _load_marked_items(lines)
    if not items:
        items = _load_legacy_items(lines)
    if project_key is None:
        if not items:
            raise ValueError("backlog has no task IDs from which to derive a project key")
        project_key, _ = parse_task_id(items[0].id)
    mode = metadata_mode or ("github-cache" if GITHUB_CACHE_NOTICE in lines else "local")
    return BacklogDocument(project_key=project_key, mode=mode, items=tuple(items))


def archive_completed_groups(
    document: BacklogDocument,
    *,
    active_line_limit: int = 500,
    target_line_limit: int = 350,
) -> tuple[BacklogDocument, tuple[BacklogItem, ...]]:
    """Move oldest fully-complete top-level groups out of an oversized local backlog."""
    if document.mode == "github-cache":
        raise ValueError("cannot archive a github-cache backlog")
    if not 0 < target_line_limit <= active_line_limit:
        raise ValueError("archive line limits must be positive and target no greater than active")
    if len(render_backlog(document).splitlines()) <= active_line_limit:
        return document, ()

    by_id = {entry.id: entry for entry in document.items}
    groups = {
        root_id: _render_order_for_group(root_id, by_id)
        for root_id in {_root_id(entry, by_id) for entry in document.items}
    }
    eligible = sorted(
        (
            (min(entry.updated_at for entry in entries), root_id)
            for root_id, entries in groups.items()
            if all(entry.status is TaskStatus.COMPLETE for entry in entries)
        ),
        key=lambda pair: (pair[0], _task_sort_key(pair[1])),
    )
    remaining_ids = set(by_id)
    archived: list[BacklogItem] = []
    for _, root_id in eligible:
        if len(render_backlog(BacklogDocument(
            project_key=document.project_key,
            mode=document.mode,
            items=tuple(entry for entry in document.items if entry.id in remaining_ids),
        )).splitlines()) <= target_line_limit:
            break
        archived.extend(groups[root_id])
        remaining_ids.difference_update(entry.id for entry in groups[root_id])
    active = BacklogDocument(
        project_key=document.project_key,
        mode=document.mode,
        items=tuple(entry for entry in document.items if entry.id in remaining_ids),
    )
    if len(render_backlog(active).splitlines()) > target_line_limit:
        raise ValueError("cannot reduce backlog to archive target without archiving active work")
    return active, tuple(archived)
