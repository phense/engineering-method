"""Filesystem primitives that keep project-state writes safe and portable."""

from __future__ import annotations

import json
import os
from pathlib import Path, PurePosixPath
import tempfile
from typing import Any, Mapping


def require_repo_relative(path: str) -> str:
    """Return a normalized repository-relative POSIX path or reject unsafe input."""
    if (
        not isinstance(path, str)
        or not path
        or "\\" in path
        or (len(path) >= 3 and path[0].isalpha() and path[1:3] == ":/")
    ):
        raise ValueError("path must be a non-empty repository-relative POSIX path")
    candidate = PurePosixPath(path)
    if candidate.is_absolute() or any(part == ".." for part in candidate.parts):
        raise ValueError("path must remain within the repository")
    normalized = str(candidate)
    if normalized in {"", "."}:
        raise ValueError("path must name a repository artifact")
    return normalized


def _json_bytes(payload: Mapping[str, Any]) -> bytes:
    return (json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")


def atomic_write_json(path: Path, payload: Mapping[str, Any]) -> None:
    """Atomically replace JSON using a flushed sibling temporary file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    data = _json_bytes(payload)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.", suffix=".tmp", dir=path.parent
    )
    temporary_path = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary_path, path)
    finally:
        if temporary_path.exists():
            temporary_path.unlink()


def append_jsonl(path: Path, record: Mapping[str, Any]) -> None:
    """Append exactly one fsynced JSON object and newline per call."""
    path.parent.mkdir(parents=True, exist_ok=True)
    line = json.dumps(record, ensure_ascii=False, separators=(",", ":"), sort_keys=True) + "\n"
    with path.open("a", encoding="utf-8") as handle:
        handle.write(line)
        handle.flush()
        os.fsync(handle.fileno())
