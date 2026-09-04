import json
import tempfile
import unittest
from pathlib import Path

from scripts.validate_plugin import validate_repository


IDENTITY = {
    "name": "engineering-method",
    "version": "0.1.0",
    "description": "Risk-proportionate engineering workflows for Codex and Claude.",
    "author": {"name": "Peter Hense"},
    "license": "MIT",
    "keywords": ["engineering", "workflow", "specification", "testing", "review"],
}


class ValidatePluginTests(unittest.TestCase):
    def make_repository(self, root: Path) -> None:
        codex = {
            **IDENTITY,
            "displayName": "Peter's Engineering Method",
            "shortDescription": "Risk-proportionate workflows for engineering agents",
            "longDescription": "A shared workflow skill set that selects lightweight or rigorous engineering practices according to the requested work and its risk.",
            "developerName": "Peter Hense",
            "category": "Developer Tools",
            "capabilities": ["Interactive", "Read", "Write"],
            "defaultPrompt": ["Plan a new multi-component feature."],
            "brandColor": "#0B7285",
            "screenshots": [],
            "skills": "./skills/",
        }
        claude = {
            **IDENTITY,
            "$schema": "https://json.schemastore.org/claude-code-plugin-manifest.json",
            "displayName": "Peter's Engineering Method",
        }
        self.write_json(root / ".codex-plugin/plugin.json", codex)
        self.write_json(root / ".claude-plugin/plugin.json", claude)
        (root / "skills/example").mkdir(parents=True)
        (root / "skills/example/SKILL.md").write_text(
            "---\nname: example\ndescription: An example workflow.\n---\n\n# Example\n",
            encoding="utf-8",
        )
        for relative in ("README.md", "LICENSE", "THIRD_PARTY_NOTICES.md"):
            (root / relative).write_text("present\n", encoding="utf-8")
        self.write_json(root / "third-party/sources.lock.json", {"schema_version": 1, "sources": []})

    def write_json(self, path: Path, value: object) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(value), encoding="utf-8")

    def test_reports_missing_codex_manifest_with_exact_diagnostic(self) -> None:
        """Removing the primary manifest must be reported at its repository path."""
        with tempfile.TemporaryDirectory() as directory:
            errors = validate_repository(Path(directory))

        self.assertIn("ERROR .codex-plugin/plugin.json: file is required", errors)

    def test_reports_invalid_manifest_json(self) -> None:
        """A malformed manifest must not be treated as an empty manifest."""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.make_repository(root)
            (root / ".codex-plugin/plugin.json").write_text("{not json", encoding="utf-8")

            errors = validate_repository(root)

        self.assertIn("ERROR .codex-plugin/plugin.json: invalid JSON", errors)

    def test_reports_manifest_identity_mismatch(self) -> None:
        """Changing one host's package identity must invalidate the shared plugin."""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.make_repository(root)
            claude_path = root / ".claude-plugin/plugin.json"
            claude = json.loads(claude_path.read_text(encoding="utf-8"))
            claude["name"] = "different-plugin"
            self.write_json(claude_path, claude)

            errors = validate_repository(root)

        self.assertIn(
            "ERROR .claude-plugin/plugin.json: name must match .codex-plugin/plugin.json",
            errors,
        )

    def test_reports_missing_common_files(self) -> None:
        """Removing a public foundation artifact must make the repository incomplete."""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.make_repository(root)
            (root / "LICENSE").unlink()

            errors = validate_repository(root)

        self.assertIn("ERROR LICENSE: file is required", errors)

    def test_reports_unfinished_scaffolding_outside_excluded_paths(self) -> None:
        """A TODO placeholder in tracked content must block a release-ready repository."""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.make_repository(root)
            marker = "[" + "TODO: finish this]"
            (root / "notes.md").write_text(marker + "\n", encoding="utf-8")
            (root / ".git").mkdir()
            (root / ".git/ignored.md").write_text("TODO: ignored\n", encoding="utf-8")

            errors = validate_repository(root)

        self.assertIn("ERROR notes.md: unfinished marker '" + marker + "'", errors)
        self.assertFalse(any("ignored.md" in error for error in errors))

    def test_reports_banned_scaffold_phrase(self) -> None:
        """A scaffold phrase left in ordinary content must be rejected."""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.make_repository(root)
            marker = "TODO" + ": replace this placeholder"
            (root / "notes.md").write_text(marker + "\n", encoding="utf-8")

            errors = validate_repository(root)

        self.assertIn("ERROR notes.md: unfinished marker '" + marker + "'", errors)

    def test_reports_invalid_skill_frontmatter(self) -> None:
        """A skill without required frontmatter fields cannot be discovered reliably."""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.make_repository(root)
            (root / "skills/example/SKILL.md").write_text("# No frontmatter\n", encoding="utf-8")

            errors = validate_repository(root)

        self.assertIn("ERROR skills/example/SKILL.md: YAML frontmatter is required", errors)

    def test_accepts_complete_repository(self) -> None:
        """Removing required files or validation fields from this fixture must fail validation."""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.make_repository(root)

            errors = validate_repository(root)

        self.assertEqual([], errors)


if __name__ == "__main__":
    unittest.main()
