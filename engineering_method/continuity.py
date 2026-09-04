"""Versioned compact-continuity state with append-only safe events."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Collection, Mapping

from .files import append_jsonl, atomic_write_json, atomic_write_text, require_repo_relative
from .models import utc_timestamp


EVENT_KINDS = frozenset({"workflow_started", "phase_changed", "slice_started", "decision_recorded", "agent_dispatched", "agent_completed", "verification_failed", "verification_passed", "workflow_completed"})
SENSITIVE = frozenset({"token", "password", "secret", "authorization", "cookie"})


@dataclass(frozen=True)
class RunState:
    work_id: str
    lifecycle: str
    phase: str
    next_action: str
    completed_slices: tuple[str, ...] = ()
    active_agent_ids: tuple[str, ...] = ()
    artifact_paths: tuple[str, ...] = ()
    schema_version: int = 1

    def __post_init__(self) -> None:
        if self.schema_version != 1 or not self.work_id or "/" in self.work_id or ".." in self.work_id:
            raise ValueError("invalid run state")
        for path in self.artifact_paths:
            require_repo_relative(path)


@dataclass(frozen=True)
class RecoveryResult:
    completed_slices: tuple[str, ...]
    redispatchable_agent_ids: tuple[str, ...]
    next_action: str


def _run(root: Path, work_id: str) -> Path:
    if not work_id or "/" in work_id or ".." in work_id:
        raise ValueError("invalid work id")
    return root / ".engineering-method" / "runs" / work_id


def _state_payload(state: RunState) -> dict[str, object]:
    return asdict(state)


def create_run(root: Path, state: RunState, resume_markdown: str, decisions_markdown: str = "") -> Path:
    run = _run(root, state.work_id)
    run.mkdir(parents=True, exist_ok=True)
    (run / "agent-reports").mkdir(exist_ok=True)
    atomic_write_json(run / "state.json", _state_payload(state))
    atomic_write_text(run / "resume.md", resume_markdown)
    atomic_write_text(run / "decisions.md", decisions_markdown)
    (run / "events.jsonl").touch(exist_ok=True)
    return run


def checkpoint(root: Path, work_id: str, state: RunState, resume_markdown: str) -> None:
    if work_id != state.work_id:
        raise ValueError("checkpoint work id does not match state")
    run = _run(root, work_id)
    if not run.is_dir():
        raise ValueError("run does not exist")
    atomic_write_json(run / "state.json", _state_payload(state))
    atomic_write_text(run / "resume.md", resume_markdown)


def _unsafe(value: object) -> bool:
    if isinstance(value, Mapping):
        return any(str(key).lower() in SENSITIVE or _unsafe(item) for key, item in value.items())
    if isinstance(value, (tuple, list)):
        return any(_unsafe(item) for item in value)
    return False


def append_event(root: Path, work_id: str, event: Mapping[str, object]) -> dict[str, object]:
    kind = event.get("kind")
    if kind not in EVENT_KINDS or _unsafe(event):
        raise ValueError("event kind is invalid or contains sensitive data")
    artifact = event.get("artifact")
    if artifact is not None:
        require_repo_relative(str(artifact))
    payload = {"schema_version": 1, "timestamp": utc_timestamp(), **event}
    append_jsonl(_run(root, work_id) / "events.jsonl", payload)
    return payload


def recover_run(root: Path, work_id: str, *, git_probe, canonical_probe, live_agent_ids: Collection[str]) -> RecoveryResult:
    import json
    payload = json.loads((_run(root, work_id) / "state.json").read_text(encoding="utf-8"))
    version = payload.get("schema_version", 0)
    if version > 1:
        raise ValueError("future run schema is unsupported")
    if version == 0:
        payload["schema_version"] = 1
    for field in ("completed_slices", "active_agent_ids", "artifact_paths"):
        if field in payload:
            payload[field] = tuple(payload[field])
    state = RunState(**payload)
    git_probe()
    canonical_probe(work_id)
    return RecoveryResult(state.completed_slices, tuple(agent for agent in state.active_agent_ids if agent not in live_agent_ids), state.next_action)
