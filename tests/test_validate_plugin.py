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

PROVENANCE_SOURCES = (
    {
        "id": "github-spec-kit",
        "project": "Spec Kit",
        "repository": "https://github.com/github/spec-kit.git",
        "revision": "df6b3187022ce986759bd854467e8a4bb56bb0f4",
        "license_sha256": "2510b446bc1f0cf9702453075d20cd88631e20e5642658edb7325d9c1eb534f7",
    },
    {
        "id": "openspec",
        "project": "OpenSpec",
        "repository": "https://github.com/Fission-AI/OpenSpec.git",
        "revision": "e062b9572be933564ba3899d059377dfa1393e32",
        "license_sha256": "c3c7235bea1214ab62df643473975c2e8b8848f528901a976693f7d069713e64",
    },
    {
        "id": "superpowers",
        "project": "Superpowers",
        "repository": "https://github.com/obra/superpowers.git",
        "revision": "b36e0829c6d0140e93cfef2ca599b1b07d4a7797",
        "license_sha256": "a37e0e9697144819e1d965176ac4ae5bc3fa02d11e7812036bbcadf6dafe2400",
    },
)


class ValidatePluginTests(unittest.TestCase):
    def make_repository(self, root: Path) -> None:
        codex = {
            **IDENTITY,
            "skills": "./skills/",
            "interface": {
                "displayName": "Peter's Engineering Method",
                "shortDescription": "Risk-proportionate workflows for engineering agents",
                "longDescription": "A shared workflow skill set that selects lightweight or rigorous engineering practices according to the requested work and its risk.",
                "developerName": "Peter Hense",
                "category": "Developer Tools",
                "capabilities": ["Interactive", "Read", "Write"],
                "defaultPrompt": ["Plan a new multi-component feature."],
                "brandColor": "#0B7285",
                "screenshots": [],
            },
        }
        claude = {
            **IDENTITY,
            "$schema": "https://json.schemastore.org/claude-code-plugin-manifest.json",
            "displayName": "Peter's Engineering Method",
        }
        self.write_json(root / ".codex-plugin/plugin.json", codex)
        self.write_json(root / ".claude-plugin/plugin.json", claude)
        self.write_json(root / ".agents/plugins/marketplace.json", {
            "name": "engineering-method", "plugins": [{
                "name": "engineering-method", "source": {"source": "local", "path": "./"},
                "policy": {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
                "category": "Developer Tools",
            }],
        })
        self.write_json(root / ".claude-plugin/marketplace.json", {
            "name": "engineering-method", "owner": {"name": "Peter Hense"},
            "plugins": [{"name": "engineering-method", "source": "./"}],
        })
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

    def test_marketplaces_reject_wrong_identity_source_and_policy(self) -> None:
        for host_path in (".agents/plugins/marketplace.json", ".claude-plugin/marketplace.json"):
            for mutation in ("identity", "source", "missing", "duplicate"):
                with self.subTest(host=host_path, mutation=mutation), tempfile.TemporaryDirectory() as directory:
                    root = Path(directory)
                    self.make_repository(root)
                    path = root / host_path
                    data = json.loads(path.read_text())
                    if mutation == "identity":
                        data["plugins"][0]["name"] = "another-plugin"
                    elif mutation == "source":
                        data["plugins"][0]["source"] = "../outside"
                    elif mutation == "duplicate":
                        data["plugins"].append(data["plugins"][0].copy())
                    else:
                        path.unlink()
                    if mutation != "missing":
                        self.write_json(path, data)
                    self.assertTrue(any(host_path in error for error in validate_repository(root)))
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.make_repository(root)
            path = root / ".agents/plugins/marketplace.json"
            data = json.loads(path.read_text())
            del data["plugins"][0]["policy"]
            self.write_json(path, data)
            self.assertTrue(any("policy" in error for error in validate_repository(root)))

    def test_reports_missing_codex_manifest_with_exact_diagnostic(self) -> None:
        """Removing the primary manifest must be reported at its repository path."""
        with tempfile.TemporaryDirectory() as directory:
            errors = validate_repository(Path(directory))

        self.assertIn("ERROR .codex-plugin/plugin.json: file is required", errors)

    def test_real_repository_is_valid_after_the_foundation_artifacts_exist(self) -> None:
        """The foundation checkout must satisfy the portable repository validator."""
        root = Path(__file__).resolve().parents[1]

        errors = validate_repository(root)

        self.assertEqual([], errors)

    def test_readme_identifies_candidate_and_verification_commands(self) -> None:
        """The public README must distinguish candidate scope from release evidence."""
        root = Path(__file__).resolve().parents[1]
        readme_path = root / "README.md"

        self.assertTrue(readme_path.is_file(), "README.md must exist")
        if not readme_path.is_file():
            return
        readme = readme_path.read_text(encoding="utf-8")

        for expected in (
            "Risk-proportionate engineering workflows",
            "0.1.0",
            "pre-release",
            "docs/specs/2026-09-04-engineering-method-design.md",
            "Codex",
            "Claude",
            "python3 -m unittest discover -s tests -t . -v",
            "python3 scripts/validate-plugin",
            "claude plugin validate --strict .",
            "[MIT License](LICENSE)",
            "[third-party notices](THIRD_PARTY_NOTICES.md)",
        ):
            self.assertIn(expected, readme)

        self.assertRegex(readme, r"do not imply affiliation with\s+or endorsement by")
        self.assert_readme_avoids_unavailable_capabilities(readme)

    def assert_readme_avoids_unavailable_capabilities(self, readme: str) -> None:
        """Reject claims for functionality intentionally absent from EM-001."""
        self.assertNotRegex(
            readme.lower(),
            r"\blifecycle skills?\s+(?:(?:are|is)\s+(?:currently )?(?:available|implemented|working|supported|enabled|functional)|works?|function)\b",
        )
        self.assertNotRegex(
            readme.lower(),
            r"\bmarketplace installation\s+(?:(?:is|are)\s+(?:currently )?(?:available|implemented|working|supported|enabled|functional)|works?|function)\b",
        )

    def test_readme_contract_rejects_direct_lifecycle_skill_claim(self) -> None:
        """The terse sentence 'Lifecycle skills work.' must be rejected."""
        with self.assertRaises(AssertionError):
            self.assert_readme_avoids_unavailable_capabilities("Lifecycle skills work.")

    def test_readme_contract_rejects_direct_marketplace_claim(self) -> None:
        """The terse sentence 'Marketplace installation works.' must be rejected."""
        with self.assertRaises(AssertionError):
            self.assert_readme_avoids_unavailable_capabilities("Marketplace installation works.")

    def test_readme_contract_rejects_affirmative_capability_synonyms(self) -> None:
        """Affirmative lifecycle and marketplace claims must be rejected regardless of synonym."""
        for claim in (
            "Lifecycle skills are supported.",
            "Marketplace installation is supported.",
        ):
            with self.subTest(claim=claim), self.assertRaises(AssertionError):
                self.assert_readme_avoids_unavailable_capabilities(claim)

    def test_real_repository_pins_the_required_upstream_provenance(self) -> None:
        """Changing a source ID, revision, license digest, or mapping must fail."""
        root = Path(__file__).resolve().parents[1]
        lock_path = root / "third-party/sources.lock.json"

        self.assertTrue(lock_path.is_file(), "third-party/sources.lock.json must exist")
        if not lock_path.is_file():
            return
        lock = json.loads(lock_path.read_text(encoding="utf-8"))

        self.assertEqual(1, lock["schema_version"])
        sources = lock["sources"]
        self.assertEqual([source["id"] for source in PROVENANCE_SOURCES], [source["id"] for source in sources])
        for expected, actual in zip(PROVENANCE_SOURCES, sources, strict=True):
            self.assertEqual(expected["project"], actual["project"])
            self.assertEqual(expected["repository"], actual["repository"])
            self.assertEqual(expected["revision"], actual["revision"])
            self.assertRegex(actual["revision"], r"^[0-9a-f]{40}$")
            self.assertEqual("MIT", actual["license"]["spdx"])
            self.assertEqual("LICENSE", actual["license"]["source_path"])
            self.assertEqual(expected["license_sha256"], actual["license"]["sha256"])
            self.assertEqual(
                {
                    "source_path": "LICENSE",
                    "destination_path": "THIRD_PARTY_NOTICES.md",
                    "source_sha256": expected["license_sha256"],
                    "modification_status": "notice-only",
                },
                actual["files"][0],
            )
            for mapping in actual["files"][1:]:
                self.assertEqual("adapted", mapping["modification_status"])
                self.assertRegex(mapping["source_sha256"], r"^[0-9a-f]{64}$")
                self.assertRegex(mapping["destination_sha256"], r"^[0-9a-f]{64}$")

    def test_real_repository_notices_agree_with_the_source_lock(self) -> None:
        """Every locked MIT license must be recorded as a notice-only source."""
        root = Path(__file__).resolve().parents[1]
        notice_path = root / "THIRD_PARTY_NOTICES.md"

        self.assertTrue(notice_path.is_file(), "THIRD_PARTY_NOTICES.md must exist")
        if not notice_path.is_file():
            return
        notices = notice_path.read_text(encoding="utf-8")

        self.assertIn("This plugin adapts only the files listed below", notices)
        self.assertIn("## Original implementation", notices)
        for source in PROVENANCE_SOURCES:
            for value in (
                source["project"],
                source["repository"],
                source["revision"],
                source["license_sha256"],
                "LICENSE -> THIRD_PARTY_NOTICES.md: notice-only",
            ):
                self.assertIn(value, notices)

    def test_reports_invalid_manifest_json(self) -> None:
        """A malformed manifest must not be treated as an empty manifest."""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.make_repository(root)
            (root / ".codex-plugin/plugin.json").write_text("{not json", encoding="utf-8")

            errors = validate_repository(root)

        self.assertIn("ERROR .codex-plugin/plugin.json: invalid JSON", errors)

    def test_accepts_required_codex_fields_in_nested_interface(self) -> None:
        """Moving Codex interface fields back to the top level must fail validation."""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.make_repository(root)

            errors = validate_repository(root)

        self.assertEqual([], errors)

    def test_rejects_noncanonical_codex_skills_paths(self) -> None:
        """Accepting a directory other than the shared skills root must fail validation."""
        for skills in (".",):
            with self.subTest(skills=skills), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                self.make_repository(root)
                manifest_path = root / ".codex-plugin/plugin.json"
                manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
                manifest["skills"] = skills
                self.write_json(manifest_path, manifest)

                errors = validate_repository(root)

            self.assertIn(
                "ERROR .codex-plugin/plugin.json: skills must be exactly ./skills/",
                errors,
            )

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.make_repository(root)
            manifest_path = root / ".codex-plugin/plugin.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest["skills"] = str(root / "skills")
            self.write_json(manifest_path, manifest)

            errors = validate_repository(root)

        self.assertIn(
            "ERROR .codex-plugin/plugin.json: skills must be exactly ./skills/",
            errors,
        )

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

    def test_accepts_host_specific_author_metadata(self) -> None:
        """Comparing complete author objects must reject harmless host metadata."""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.make_repository(root)
            claude_path = root / ".claude-plugin/plugin.json"
            claude = json.loads(claude_path.read_text(encoding="utf-8"))
            claude["author"] = {"name": "Peter Hense", "email": "peter@example.com"}
            self.write_json(claude_path, claude)

            errors = validate_repository(root)

        self.assertEqual([], errors)

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

    def test_project_backlog_requires_negative_boundary_and_plugin_root_commands(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.make_repository(root)
            skill = root / "skills" / "project-backlog" / "SKILL.md"
            skill.parent.mkdir(parents=True)
            skill.write_text(
                "---\n"
                "name: project-backlog\n"
                "description: Use when durable task state is needed.\n"
                "---\n\n"
                "# Project Backlog\n\n"
                "```sh\n"
                "scripts/project-state backlog state-check\n"
                "```\n",
                encoding="utf-8",
            )

            errors = validate_repository(root)

        self.assertIn(
            "ERROR skills/project-backlog/SKILL.md: description must exclude implementation methodology selection",
            errors,
        )
        self.assertIn(
            "ERROR skills/project-backlog/SKILL.md: bundled script links must resolve from the skill directory and run with the target repository cwd",
            errors,
        )

    def test_reports_missing_and_escaping_bundled_skill_resources(self) -> None:
        """A local skill link must resolve to an existing path inside the plugin root."""
        cases = (
            (
                "[missing resource](missing.md)",
                "ERROR skills/example/SKILL.md: bundled resource missing.md is required",
            ),
            (
                "[escaping resource](../../../outside.md)",
                "ERROR skills/example/SKILL.md: bundled resource ../../../outside.md must stay within the repository",
            ),
        )
        for reference, expected in cases:
            with self.subTest(reference=reference), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                self.make_repository(root)
                skill_path = root / "skills/example/SKILL.md"
                skill_path.write_text(skill_path.read_text(encoding="utf-8") + reference + "\n", encoding="utf-8")

                errors = validate_repository(root)

            self.assertIn(expected, errors)

    def test_accepts_existing_bundled_skill_resource(self) -> None:
        """A valid skill-relative link must resolve from the document directory."""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.make_repository(root)
            skill_path = root / "skills/example/SKILL.md"
            resource = root / "templates/example.md"
            resource.parent.mkdir(parents=True)
            resource.write_text("example\n", encoding="utf-8")
            skill_path.write_text(
                skill_path.read_text(encoding="utf-8")
                + "[resource](../../templates/example.md)\n",
                encoding="utf-8",
            )

            errors = validate_repository(root)

        self.assertEqual([], errors)

    def test_rejects_a_directory_as_a_bundled_skill_resource(self) -> None:
        """A Markdown resource link must resolve to a file, not merely an existing path."""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.make_repository(root)
            skill_path = root / "skills/example/SKILL.md"
            resource = root / "templates/example"
            resource.mkdir(parents=True)
            skill_path.write_text(
                skill_path.read_text(encoding="utf-8")
                + "[resource](../../templates/example)\n",
                encoding="utf-8",
            )

            errors = validate_repository(root)

        self.assertIn(
            "ERROR skills/example/SKILL.md: bundled resource ../../templates/example is required",
            errors,
        )

    def test_reports_stale_locked_destination_hash(self) -> None:
        """An adapted destination changed without a lock update must fail validation."""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.make_repository(root)
            lock_path = root / "third-party/sources.lock.json"
            self.write_json(
                lock_path,
                {
                    "schema_version": 1,
                    "sources": [
                        {
                            "id": "example-upstream",
                            "files": [
                                {
                                    "source_path": "source.md",
                                    "destination_path": "skills/example/SKILL.md",
                                    "source_sha256": "1" * 64,
                                    "destination_sha256": "0" * 64,
                                    "modification_status": "adapted",
                                }
                            ],
                        }
                    ],
                },
            )

            errors = validate_repository(root)

        self.assertIn(
            "ERROR third-party/sources.lock.json: destination hash mismatch for skills/example/SKILL.md",
            errors,
        )

    def test_enforces_safe_skill_frontmatter_scalars(self) -> None:
        """Only non-empty plain or balanced quoted name and description scalars are valid."""
        valid_frontmatter = (
            "---\nname: example-workflow\ndescription: An example workflow.\n---\n\n# Example\n",
            "---\nname: \"example-workflow\"\ndescription: 'An example workflow.'\n---\n\n# Example\n",
            "---\nname: 'example-workflow'\ndescription: \"true\"\n---\n\n# Example\n",
            "---\nname: example-workflow\ndescription: \"A workflow: test and review!\"\n---\n\n# Example\n",
        )
        for content in valid_frontmatter:
            with self.subTest(valid=content), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                self.make_repository(root)
                (root / "skills/example/SKILL.md").write_text(content, encoding="utf-8")

                errors = validate_repository(root)

            self.assertEqual([], errors)

        invalid_scalars = (
            ("name", "[unterminated"),
            ("description", "{workflow: example}"),
            ("description", "|"),
            ("description", "!workflow example"),
            ("description", "&workflow example"),
            ("description", "*workflow"),
            ("name", "\"unterminated"),
            ("description", "'unterminated"),
        )
        for field, value in invalid_scalars:
            with self.subTest(field=field, value=value), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                self.make_repository(root)
                (root / "skills/example/SKILL.md").write_text(
                    "---\n"
                    f"name: {'example' if field != 'name' else value}\n"
                    f"description: {'An example workflow.' if field != 'description' else value}\n"
                    "---\n\n# Example\n",
                    encoding="utf-8",
                )

                errors = validate_repository(root)

            self.assertIn(
                f"ERROR skills/example/SKILL.md: frontmatter {field} must be a supported scalar",
                errors,
            )

    def test_rejects_ambiguous_and_structural_frontmatter_scalars(self) -> None:
        """Implicit YAML values and syntax outside the safe string grammar must fail."""
        invalid_scalars = (
            ("name", "null", "frontmatter name must be a supported scalar"),
            ("description", "true", "frontmatter description must be a supported scalar"),
            ("name", "example:", "frontmatter name must be a supported scalar"),
            ("description", "42", "frontmatter description must be a supported scalar"),
            ("description", "1:20", "frontmatter description must be a supported scalar"),
            ("description", ".inf", "frontmatter description must be a supported scalar"),
            ("description", ".nan", "frontmatter description must be a supported scalar"),
            ("description", "0xFF", "frontmatter description must be a supported scalar"),
            ("description", "0o77", "frontmatter description must be a supported scalar"),
            ("description", "+42", "frontmatter description must be a supported scalar"),
            ("description", "-42", "frontmatter description must be a supported scalar"),
            ("description", "2026-09-04", "frontmatter description must be a supported scalar"),
            ("description", "A:workflow", "frontmatter description must be a supported scalar"),
            ("description", "A [workflow]", "frontmatter description must be a supported scalar"),
            ("description", "A & workflow", "frontmatter description must be a supported scalar"),
            ("description", "An example # comment", "frontmatter description must be a supported scalar"),
            ("description", "An example\t# comment", "frontmatter description must be a supported scalar"),
            ("description", "key: value", "frontmatter description must be a supported scalar"),
            ("description", "key:\tvalue", "frontmatter description must be a supported scalar"),
            ("name", "Example_Workflow", "frontmatter name must be lowercase hyphen-case"),
        )
        for field, value, message in invalid_scalars:
            with self.subTest(field=field, value=value):
                with tempfile.TemporaryDirectory() as directory:
                    root = Path(directory)
                    self.make_repository(root)
                    (root / "skills/example/SKILL.md").write_text(
                        "---\n"
                        f"name: {'example-workflow' if field != 'name' else value}\n"
                        f"description: {'An example workflow.' if field != 'description' else value}\n"
                        "---\n\n# Example\n",
                        encoding="utf-8",
                    )

                    errors = validate_repository(root)

                self.assertIn(f"ERROR skills/example/SKILL.md: {message}", errors)

    def test_accepts_complete_repository(self) -> None:
        """Removing required files or validation fields from this fixture must fail validation."""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.make_repository(root)

            errors = validate_repository(root)

        self.assertEqual([], errors)


if __name__ == "__main__":
    unittest.main()
