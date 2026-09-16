"""Public documentation and attribution acceptance, alongside portable validation."""

import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]


class PublicReleaseContracts(unittest.TestCase):
    def test_readme_documents_installation_boundaries_and_evidence_limits(self):
        """Dropping an installation or authority boundary must fail public documentation."""
        text = (ROOT / "README.md").read_text()
        headings = set(re.findall(r"^## (.+)$", text, re.MULTILINE))
        self.assertTrue({"Installation", "Automatic workflow selection", "Architecture and review",
                         "Backlog and GitHub Issues", "Continuity", "Models and host adapters",
                         "Development and verification", "Validation scope", "License and attribution"}
                        <= headings)
        for term in ("codex plugin marketplace add", "codex plugin add", "--plugin-dir",
                     "BACKLOG.md", "FEATURES.md", "sub-issues", "native dependencies",
                     "English", "offline", "agentic-rag", "docs/uml", "Mermaid",
                     "Spec Kit", "OpenSpec", "Superpowers", "no central router"):
            self.assertIn(term, text)
        self.assertNotIn("an empty shared", text)
        self.assertNotIn("No lifecycle skills", text)
        self.assertNotRegex(text, r"https://github.com/(?:OWNER|YOUR|your)[^\s)]*")

    def test_every_distributed_skill_is_attributed_or_explicitly_original(self):
        """Adding a derived skill without a mapping must not silently claim provenance."""
        lock = json.loads((ROOT / "third-party/sources.lock.json").read_text())
        derived = {m["destination_path"] for s in lock["sources"] for m in s["files"]
                   if m["modification_status"] == "adapted"}
        original = lock.get("original", {})
        self.assertEqual("MIT", original.get("license"))
        self.assertEqual("Copyright (c) 2026 Peter Hense", original.get("copyright"))
        explicit = set(original.get("paths", []))
        for path in (ROOT / "skills").rglob("*.md"):
            relative = path.relative_to(ROOT).as_posix()
            self.assertTrue(relative in derived or relative in explicit, relative)
        self.assertTrue({"engineering_method/**", "shared/platform/**", "templates/uml/**",
                         "tests/**", "evals/**"} <= explicit)

    def test_notices_cover_every_pinned_mapping_and_full_mit_permissions(self):
        """Removing a source notice, copyright or modification disclosure must fail."""
        notices = (ROOT / "THIRD_PARTY_NOTICES.md").read_text()
        lock = json.loads((ROOT / "third-party/sources.lock.json").read_text())
        for source in lock["sources"]:
            self.assertIn(source["repository"], notices)
            self.assertIn(source["revision"], notices)
            self.assertTrue(source.get("copyright"), source["id"])
            self.assertIn(source["copyright"], notices)
            self.assertTrue(source.get("modification_summary"), source["id"])
            for mapping in source["files"]:
                if mapping["modification_status"] == "adapted":
                    self.assertIn('`' + mapping["destination_path"] + '`', notices)
        permission = (ROOT / "LICENSE").read_text().split("Permission is hereby granted", 1)[1]
        normalized = " ".join(notices.split())
        self.assertEqual(4, normalized.count(" ".join(("Permission is hereby granted" + permission).split())))
        self.assertIn("Original implementation", notices)


if __name__ == "__main__":
    unittest.main()
