"""Small dependency-free command adapters for project-state workflows."""

from __future__ import annotations

from dataclasses import replace
import json
from pathlib import Path
import sys

from .backlog import BacklogDocument, load_backlog, render_backlog
from .continuity import RunState, append_event, checkpoint, create_run, recover_run
from .features import FeatureDocument, load_features, remove_feature, render_features, upsert_feature
from .files import atomic_write_text
from .gh import GitHubIssuesGateway
from .issues import workflow_state_check
from .models import BacklogItem, Feature, Priority, TaskStatus, derive_project_key, utc_timestamp


def _error(message: str) -> int:
    print(message, file=sys.stderr)
    return 2


def _option(arguments: list[str], name: str, *, required: bool = False, default: str | None = None) -> str | None:
    try:
        index = arguments.index(name)
    except ValueError:
        if required:
            raise ValueError(f"{name} is required")
        return default
    if index + 1 >= len(arguments):
        raise ValueError(f"{name} requires a value")
    return arguments[index + 1]


def _write_backlog(document: BacklogDocument) -> None:
    atomic_write_text(Path("BACKLOG.md"), render_backlog(document))


def _local_backlog() -> BacklogDocument:
    document = load_backlog(Path("BACKLOG.md"))
    if document.mode != "local":
        raise ValueError("local backlog mutation is unavailable in github-cache mode")
    return document


def _backlog_command(arguments: list[str]) -> int:
    if not arguments:
        return _error("backlog action required")
    action = arguments[0]
    if action == "init":
        try:
            key = _option(arguments, "--project-key") or derive_project_key(Path.cwd().name)
            _write_backlog(BacklogDocument(key, "local", ()))
            atomic_write_text(Path("FEATURES.md"), render_features(FeatureDocument(features=())))
        except ValueError as error:
            return _error(str(error))
        print("BACKLOG.md")
        return 0
    try:
        document = _local_backlog()
        if action == "add":
            identifier = _option(arguments, "--id", required=True)
            title = _option(arguments, "--title", required=True)
            priority = Priority(_option(arguments, "--priority", required=True))
            parent = _option(arguments, "--parent")
            item = BacklogItem(identifier, title, TaskStatus.OPEN, priority, parent, (), _option(arguments, "--notes", default="") or "", utc_timestamp())
            document = BacklogDocument(document.project_key, "local", document.items + (item,))
        elif action in {"start", "block", "complete"}:
            if len(arguments) < 2:
                raise ValueError("backlog ID is required")
            identifier = arguments[1]
            statuses = {"start": TaskStatus.IN_PROGRESS, "block": TaskStatus.BLOCKED, "complete": TaskStatus.COMPLETE}
            found = False
            items = []
            for item in document.items:
                if item.id == identifier:
                    found = True
                    items.append(replace(item, status=statuses[action], notes=_option(arguments, "--notes", default=item.notes) or "", updated_at=utc_timestamp()))
                else:
                    items.append(item)
            if not found:
                raise ValueError("backlog ID does not exist")
            document = BacklogDocument(document.project_key, "local", tuple(items))
        else:
            raise ValueError("unsupported backlog action")
        _write_backlog(document)
    except (ValueError, OSError) as error:
        return _error(str(error))
    print("BACKLOG.md")
    return 0


def _feature_command(arguments: list[str]) -> int:
    if not arguments:
        return _error("feature action required")
    try:
        document = load_features(Path("FEATURES.md"))
        action = arguments[0]
        if action in {"add", "change"}:
            identifier = _option(arguments, "--id", required=True)
            existing = next((entry for entry in document.features if entry.id == identifier), None)
            if action == "change" and existing is None:
                raise ValueError("feature ID does not exist")
            name = _option(arguments, "--name", default=existing.name if existing else None)
            summary = _option(arguments, "--summary", default=existing.summary if existing else None)
            status = _option(arguments, "--status", default=existing.status if existing else "available")
            related = _option(arguments, "--related")
            links = tuple(related.split(",")) if related else (existing.related_backlog_ids if existing else ())
            document = upsert_feature(document, Feature(identifier, name, summary, status, links, utc_timestamp()))
        elif action == "remove":
            document = remove_feature(document, _option(arguments, "--id", required=True), rationale=_option(arguments, "--rationale", required=True))
        else:
            raise ValueError("unsupported feature action")
        atomic_write_text(Path("FEATURES.md"), render_features(document))
    except (ValueError, OSError) as error:
        return _error(str(error))
    print("FEATURES.md")
    return 0


def _continuity_command(arguments: list[str]) -> int:
    if not arguments:
        return _error("continuity action required")
    try:
        action = arguments[0]
        if action == "event":
            if len(arguments) != 3:
                raise ValueError("event requires work ID and JSON")
            append_event(Path.cwd(), arguments[1], json.loads(arguments[2]))
        elif action in {"init", "checkpoint"}:
            if len(arguments) != 3:
                raise ValueError(f"{action} requires work ID and JSON state")
            payload = json.loads(arguments[2])
            payload["work_id"] = arguments[1]
            state = RunState(**payload)
            if action == "init":
                create_run(Path.cwd(), state, "")
            else:
                checkpoint(Path.cwd(), arguments[1], state, "")
        elif action == "status":
            if len(arguments) != 2:
                raise ValueError("status requires work ID")
            print((Path(".engineering-method") / "runs" / arguments[1] / "state.json").as_posix())
            return 0
        elif action == "recover":
            if len(arguments) != 2:
                raise ValueError("recover requires work ID")
            print(recover_run(Path.cwd(), arguments[1], git_probe=lambda: "", canonical_probe=lambda _: False, live_agent_ids=()).next_action)
            return 0
        else:
            raise ValueError("unsupported continuity action")
    except (ValueError, OSError, json.JSONDecodeError, TypeError) as error:
        return _error(str(error))
    print(".engineering-method/runs")
    return 0


def main(argv: list[str] | None = None) -> int:
    arguments = list(sys.argv[1:] if argv is None else argv)
    if not arguments:
        return _error("project-state command required")
    command, remaining = arguments[0], arguments[1:]
    if command == "backlog":
        return _backlog_command(remaining)
    if command == "feature":
        return _feature_command(remaining)
    if command == "continuity-state":
        return _continuity_command(remaining)
    if command in {"backlog-to-issues", "refresh-issue-cache"}:
        try:
            outcome = workflow_state_check(Path("BACKLOG.md"), GitHubIssuesGateway())
        except (ValueError, OSError, RuntimeError) as error:
            return _error(str(error))
        print(outcome.reason)
        return 0
    return _error("unsupported project-state command")
