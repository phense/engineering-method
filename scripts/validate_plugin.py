"""Dependency-free validation for an Engineering Method plugin checkout."""

from __future__ import annotations

import collections.abc
import json
import re
import sys
from pathlib import Path


COMMON_IDENTITY_FIELDS = ("name", "version", "description", "author", "license", "keywords")
COMMON_REQUIRED_FILES = (
    "README.md",
    "LICENSE",
    "THIRD_PARTY_NOTICES.md",
    "third-party/sources.lock.json",
)
CODEX_REQUIRED_INTERFACE_FIELDS = {
    "displayName": str,
    "shortDescription": str,
    "longDescription": str,
    "developerName": str,
    "category": str,
    "capabilities": list,
    "defaultPrompt": list,
    "brandColor": str,
    "screenshots": list,
}
SEMVER = re.compile(
    r"^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)"
    r"(?:-(?:0|[0-9A-Za-z-]*[A-Za-z-][0-9A-Za-z-]*|[1-9][0-9]*)(?:\.(?:0|[0-9A-Za-z-]*[A-Za-z-][0-9A-Za-z-]*|[1-9][0-9]*))*)?"
    r"(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?$"
)
BRACKETED_PLACEHOLDER = re.compile(r"\[(?:TODO|TBD|TASK|FIXME)(?::[^\]]*)?\]", re.IGNORECASE)
SCAFFOLD_PHRASES = tuple(
    re.compile(pattern, re.IGNORECASE)
    for pattern in (
        "TODO" + r":\s*replace this placeholder",
        "TODO" + r":\s*add implementation",
    )
)
EXCLUDED_SCAN_PARTS = {".git", "__pycache__", ".engineering-method"}
SKILL_FRONTMATTER_FIELDS = frozenset({"name", "description"})
PLAIN_SCALAR_START_INDICATORS = frozenset("-?:,[]{}#&*!|>@`")
DOUBLE_QUOTED_SCALAR = re.compile(
    r'^"(?:[^"\\\r\n]|\\(?:["\\/bfnrt]|u[0-9A-Fa-f]{4}))*"$'
)
SINGLE_QUOTED_SCALAR = re.compile(r"^'(?:[^'\r\n]|'')*'$")


def _relative(root: Path, path: Path) -> str:
    return path.relative_to(root).as_posix()


def _error(path: str, message: str) -> str:
    return f"ERROR {path}: {message}"


def _load_json(root: Path, relative: str, errors: list[str]) -> dict[str, object] | None:
    path = root / relative
    if not path.is_file():
        errors.append(_error(relative, "file is required"))
        return None
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError):
        errors.append(_error(relative, "invalid JSON"))
        return None
    if not isinstance(value, dict):
        errors.append(_error(relative, "must contain a JSON object"))
        return None
    return value


def _validate_identity(
    relative: str, manifest: dict[str, object], errors: list[str]
) -> None:
    for field in COMMON_IDENTITY_FIELDS:
        if field not in manifest:
            errors.append(_error(relative, f"{field} is required"))
    name = manifest.get("name")
    if "name" in manifest and (not isinstance(name, str) or not name):
        errors.append(_error(relative, "name must be a non-empty string"))
    version = manifest.get("version")
    if "version" in manifest and (not isinstance(version, str) or not SEMVER.fullmatch(version)):
        errors.append(_error(relative, "version must be strict semver"))
    if "description" in manifest and (
        not isinstance(manifest["description"], str) or not manifest["description"]
    ):
        errors.append(_error(relative, "description must be a non-empty string"))
    author = manifest.get("author")
    if "author" in manifest and (
        not isinstance(author, dict)
        or not isinstance(author.get("name"), str)
        or not author["name"]
    ):
        errors.append(_error(relative, "author.name must be a non-empty string"))
    if "license" in manifest and (not isinstance(manifest["license"], str) or not manifest["license"]):
        errors.append(_error(relative, "license must be a non-empty string"))
    if "keywords" in manifest and (
        not isinstance(manifest["keywords"], list)
        or not all(isinstance(keyword, str) and keyword for keyword in manifest["keywords"])
    ):
        errors.append(_error(relative, "keywords must be a list of non-empty strings"))


def _validate_codex_manifest(
    root: Path, relative: str, manifest: dict[str, object], errors: list[str]
) -> None:
    interface = manifest.get("interface")
    if not isinstance(interface, dict):
        errors.append(_error(relative, "interface must be an object"))
        interface = {}
    skills = manifest.get("skills")
    if "skills" not in manifest:
        errors.append(_error(relative, "skills is required"))
    elif not isinstance(skills, str) or not skills:
        errors.append(_error(relative, "skills must be a non-empty string"))
    elif skills != "./skills/":
        errors.append(_error(relative, "skills must be exactly ./skills/"))
    for field, expected_type in CODEX_REQUIRED_INTERFACE_FIELDS.items():
        value = interface.get(field)
        if field not in interface:
            errors.append(_error(relative, f"{field} is required"))
        elif not isinstance(value, expected_type) or (isinstance(value, str) and not value):
            errors.append(_error(relative, f"{field} must be a non-empty {expected_type.__name__}"))

    for field in ("capabilities", "defaultPrompt"):
        value = interface.get(field)
        if isinstance(value, list) and not all(isinstance(item, str) and item for item in value):
            errors.append(_error(relative, f"{field} must be a list of non-empty strings"))
    brand_color = interface.get("brandColor")
    if isinstance(brand_color, str) and not re.fullmatch(r"#[0-9A-Fa-f]{6}", brand_color):
        errors.append(_error(relative, "brandColor must be a six-digit hex color"))

    for field in ("hooks", "apps", "mcpServers"):
        if field in manifest:
            errors.append(_error(relative, f"{field} is not supported without a component"))

    for field in ("skills", "agents", "commands"):
        if field not in manifest:
            continue
        component = manifest[field]
        if not isinstance(component, str) or not component:
            continue
        component_path = (root / component).resolve()
        try:
            component_path.relative_to(root.resolve())
        except ValueError:
            errors.append(_error(relative, f"{field} must stay within the repository"))
            continue
        if not component_path.is_dir():
            errors.append(_error(relative, f"{field} path {_relative(root, component_path)} is required"))


def _is_supported_frontmatter_scalar(value: str) -> bool:
    """Accept the narrow, dependency-free scalar subset used by skill metadata.

    A scalar is non-empty plain text without YAML control syntax, a JSON-style
    double-quoted string, or a YAML single-quoted string. Collections, blocks,
    tags, anchors, aliases, and nested mappings are intentionally unsupported.
    """
    if not value:
        return False
    if value.startswith('"'):
        return bool(DOUBLE_QUOTED_SCALAR.fullmatch(value) and value[1:-1].strip())
    if value.startswith("'"):
        return bool(SINGLE_QUOTED_SCALAR.fullmatch(value) and value[1:-1].strip())
    return (
        value[0] not in PLAIN_SCALAR_START_INDICATORS
        and ": " not in value
        and " #" not in value
    )


def _validate_skill_frontmatter(root: Path, errors: list[str]) -> None:
    skills_root = root / "skills"
    if not skills_root.is_dir():
        return
    for path in sorted(skills_root.rglob("SKILL.md")):
        relative = _relative(root, path)
        try:
            content = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            errors.append(_error(relative, "must be valid UTF-8 text"))
            continue
        if not content.startswith("---\n"):
            errors.append(_error(relative, "YAML frontmatter is required"))
            continue
        closing = content.find("\n---\n", 4)
        if closing == -1:
            errors.append(_error(relative, "YAML frontmatter must be closed"))
            continue
        fields: set[str] = set()
        for line in content[4:closing].splitlines():
            if not line.strip():
                continue
            key, separator, value = line.partition(":")
            if not separator or key not in SKILL_FRONTMATTER_FIELDS or key in fields:
                errors.append(
                    _error(relative, "frontmatter supports only unique name and description scalars")
                )
                continue
            fields.add(key)
            if not _is_supported_frontmatter_scalar(value.strip()):
                errors.append(_error(relative, f"frontmatter {key} must be a supported scalar"))
        for field in SKILL_FRONTMATTER_FIELDS:
            if field not in fields:
                errors.append(_error(relative, f"frontmatter {field} is required"))


def _is_excluded_scan_path(relative: Path) -> bool:
    return any(part in EXCLUDED_SCAN_PARTS for part in relative.parts) or relative.parts[:2] == (
        "tests",
        "fixtures",
    )


def _validate_unfinished_markers(root: Path, errors: list[str]) -> None:
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        relative_path = path.relative_to(root)
        if _is_excluded_scan_path(relative_path):
            continue
        try:
            content = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        marker = BRACKETED_PLACEHOLDER.search(content)
        if marker is None:
            marker = next(
                (phrase.search(content) for phrase in SCAFFOLD_PHRASES if phrase.search(content)), None
            )
        if marker is not None:
            errors.append(
                _error(_relative(root, path), f"unfinished marker '{marker.group(0)}'")
            )


def validate_repository(root: Path) -> list[str]:
    """Return sorted validation errors, or an empty list."""
    root = root.resolve()
    errors: list[str] = []
    codex_relative = ".codex-plugin/plugin.json"
    claude_relative = ".claude-plugin/plugin.json"
    codex = _load_json(root, codex_relative, errors)
    claude = _load_json(root, claude_relative, errors)
    for relative in COMMON_REQUIRED_FILES:
        if not (root / relative).is_file():
            errors.append(_error(relative, "file is required"))
    if codex is not None:
        _validate_identity(codex_relative, codex, errors)
        _validate_codex_manifest(root, codex_relative, codex, errors)
    if claude is not None:
        _validate_identity(claude_relative, claude, errors)
    if codex is not None and claude is not None:
        for field in (field for field in COMMON_IDENTITY_FIELDS if field != "author"):
            if field in codex and field in claude and codex[field] != claude[field]:
                errors.append(_error(claude_relative, f"{field} must match .codex-plugin/plugin.json"))
        codex_author = codex.get("author")
        claude_author = claude.get("author")
        if (
            isinstance(codex_author, dict)
            and isinstance(claude_author, dict)
            and codex_author.get("name") != claude_author.get("name")
        ):
            errors.append(_error(claude_relative, "author.name must match .codex-plugin/plugin.json"))
    _validate_skill_frontmatter(root, errors)
    _validate_unfinished_markers(root, errors)
    return sorted(errors)


def main(argv: collections.abc.Sequence[str] | None = None) -> int:
    """Validate argv[0] or the current directory and return a process code."""
    arguments = list(sys.argv[1:] if argv is None else argv)
    root = Path(arguments[0]) if arguments else Path.cwd()
    errors = validate_repository(root)
    for error in errors:
        print(error)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
