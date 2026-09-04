import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from scripts.audit_provenance import audit_repository


class AuditProvenanceTests(unittest.TestCase):
    def test_accepts_explicit_source_root_with_matching_bytes(self) -> None:
        """A provisioned upstream root proves the locked source hash against real bytes."""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "plugin"
            upstream = Path(directory) / "upstream"
            (root / "third-party").mkdir(parents=True)
            upstream.mkdir()
            source = upstream / "source.md"
            destination = root / "destination.md"
            source.write_text("source\n", encoding="utf-8")
            destination.write_text("adapted\n", encoding="utf-8")
            (root / "third-party/sources.lock.json").write_text(
                json.dumps(
                    {
                        "schema_version": 1,
                        "sources": [
                            {
                                "id": "upstream",
                                "revision": "a" * 40,
                                "files": [
                                    {
                                        "source_path": "source.md",
                                        "destination_path": "destination.md",
                                        "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
                                        "destination_sha256": hashlib.sha256(destination.read_bytes()).hexdigest(),
                                        "modification_status": "adapted",
                                    }
                                ],
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )

            errors = audit_repository(root, {"upstream": upstream})

        self.assertEqual([], errors)

    def test_rejects_unprovisioned_source_and_source_hash_mismatch(self) -> None:
        """Live auditing must fail closed when a root is absent or bytes differ."""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "plugin"
            upstream = Path(directory) / "upstream"
            (root / "third-party").mkdir(parents=True)
            upstream.mkdir()
            (upstream / "source.md").write_text("actual\n", encoding="utf-8")
            (root / "destination.md").write_text("adapted\n", encoding="utf-8")
            (root / "third-party/sources.lock.json").write_text(
                json.dumps(
                    {
                        "schema_version": 1,
                        "sources": [
                            {
                                "id": "upstream",
                                "revision": "a" * 40,
                                "files": [
                                    {
                                        "source_path": "source.md",
                                        "destination_path": "destination.md",
                                        "source_sha256": "0" * 64,
                                        "destination_sha256": hashlib.sha256(
                                            (root / "destination.md").read_bytes()
                                        ).hexdigest(),
                                        "modification_status": "adapted",
                                    }
                                ],
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )

            missing = audit_repository(root, {})
            mismatch = audit_repository(root, {"upstream": upstream})

        self.assertIn("source root for upstream was not provisioned", missing)
        self.assertIn("source hash mismatch for upstream:source.md", mismatch)


if __name__ == "__main__":
    unittest.main()
