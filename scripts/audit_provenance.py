"""Audit locked upstream and destination bytes from explicitly supplied roots."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def audit_repository(root: Path, source_roots: dict[str, Path]) -> list[str]:
    """Return provenance errors using only caller-provisioned upstream roots."""
    root = root.resolve()
    lock_path = root / "third-party/sources.lock.json"
    try:
        lock = json.loads(lock_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError):
        return ["third-party/sources.lock.json is missing or invalid"]

    errors: list[str] = []
    for source in lock.get("sources", []):
        source_id = source.get("id")
        if not isinstance(source_id, str):
            errors.append("source entry has no valid id")
            continue
        source_root = source_roots.get(source_id)
        if source_root is None:
            errors.append(f"source root for {source_id} was not provisioned")
            continue
        source_root = source_root.resolve()
        if not source_root.is_dir():
            errors.append(f"source root for {source_id} is not a directory: {source_root}")
            continue
        for mapping in source.get("files", []):
            source_relative = mapping.get("source_path")
            if not isinstance(source_relative, str):
                errors.append(f"source path missing for {source_id}")
                continue
            source_path = (source_root / source_relative).resolve()
            try:
                source_path.relative_to(source_root)
            except ValueError:
                errors.append(f"source path escapes root for {source_id}:{source_relative}")
                continue
            if not source_path.is_file():
                errors.append(f"source file missing for {source_id}:{source_relative}")
                continue
            source_hash = hashlib.sha256(source_path.read_bytes()).hexdigest()
            if source_hash != mapping.get("source_sha256"):
                errors.append(f"source hash mismatch for {source_id}:{source_relative}")

            if mapping.get("modification_status") != "adapted":
                continue
            destination_relative = mapping.get("destination_path")
            if not isinstance(destination_relative, str):
                errors.append(f"destination path missing for {source_id}:{source_relative}")
                continue
            destination_path = (root / destination_relative).resolve()
            try:
                destination_path.relative_to(root)
            except ValueError:
                errors.append(f"destination path escapes root: {destination_relative}")
                continue
            if not destination_path.is_file():
                errors.append(f"destination file missing: {destination_relative}")
                continue
            destination_hash = hashlib.sha256(destination_path.read_bytes()).hexdigest()
            if destination_hash != mapping.get("destination_sha256"):
                errors.append(f"destination hash mismatch: {destination_relative}")
    return sorted(errors)


def _source_root(value: str) -> tuple[str, Path]:
    source_id, separator, path = value.partition("=")
    if not separator or not source_id or not path:
        raise argparse.ArgumentTypeError("source roots use ID=PATH")
    return source_id, Path(path)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Verify source-lock bytes using explicitly provisioned upstream roots."
    )
    parser.add_argument("root", nargs="?", default=".", type=Path)
    parser.add_argument(
        "--source-root",
        action="append",
        default=[],
        type=_source_root,
        metavar="ID=PATH",
        help="Pinned upstream checkout root; repeat once per source id.",
    )
    arguments = parser.parse_args()
    roots: dict[str, Path] = {}
    for source_id, path in arguments.source_root:
        if source_id in roots:
            parser.error(f"duplicate source root for {source_id}")
        roots[source_id] = path
    errors = audit_repository(arguments.root, roots)
    for error in errors:
        print(f"ERROR {error}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
