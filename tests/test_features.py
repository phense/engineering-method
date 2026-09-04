"""Tests for the non-duplicative capability inventory."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from engineering_method.features import (
    FeatureDocument,
    load_features,
    remove_feature,
    render_features,
    upsert_feature,
)
from engineering_method.models import Feature


def feature(
    identifier: str = "F-001",
    *,
    name: str = "Project-state storage",
    summary: str = "Keeps durable local workflow state.",
    status: str = "available",
    related_backlog_ids: tuple[str, ...] = ("EM-002",),
) -> Feature:
    """Build a literal capability fixture independent of renderer behavior."""
    return Feature(
        id=identifier,
        name=name,
        summary=summary,
        status=status,
        related_backlog_ids=related_backlog_ids,
        updated_at="2026-09-04T10:20:30Z",
    )


class FeatureInventoryTests(unittest.TestCase):
    def test_empty_inventory_keeps_the_honest_pre_release_statement(self) -> None:
        rendered = render_features(FeatureDocument(features=()))
        self.assertIn("currently pre-release. No plugin capability has been implemented or released yet.", rendered)

    def test_adds_a_capability_with_a_validated_hidden_marker(self) -> None:
        document = upsert_feature(FeatureDocument(features=()), feature())
        rendered = render_features(document)
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "FEATURES.md"
            path.write_text(rendered, encoding="utf-8")
            loaded = load_features(path)

        self.assertIn('<!-- engineering-method:feature {"schema_version":1,"id":"F-001"', rendered)
        self.assertEqual(loaded.features, (feature(),))

    def test_updates_a_capability_without_changing_its_id_or_losing_existing_backlog_links(self) -> None:
        initial = FeatureDocument(features=(feature(),))
        updated = upsert_feature(
            initial,
            feature(
                name="Project-state continuity",
                summary="Keeps durable state through compact recovery.",
                status="changed",
                related_backlog_ids=("EM-002.6",),
            ),
        )

        self.assertEqual(updated.features[0].id, "F-001")
        self.assertEqual(updated.features[0].status, "changed")
        self.assertEqual(updated.features[0].related_backlog_ids, ("EM-002", "EM-002.6"))

    def test_removes_a_capability_as_historical_inventory_entry_with_its_identity_and_links(self) -> None:
        removed = remove_feature(
            FeatureDocument(features=(feature(),)),
            "F-001",
            rationale="Superseded by a smaller local capability.",
        )
        rendered = render_features(removed)

        self.assertEqual(removed.features[0].id, "F-001")
        self.assertEqual(removed.features[0].status, "removed")
        self.assertEqual(removed.features[0].related_backlog_ids, ("EM-002",))
        self.assertIn("Superseded by a smaller local capability.", rendered)

    def test_rejects_backlog_only_fields_in_a_feature_marker(self) -> None:
        content = """# Features
<!-- engineering-method:feature {\"schema_version\":1,\"id\":\"F-001\",\"name\":\"Safe\",\"summary\":\"Safe capability.\",\"status\":\"available\",\"related_backlog_ids\":[],\"updated_at\":\"2026-09-04T10:20:30Z\",\"priority\":\"P0\"} -->
## `F-001` Safe
"""
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "FEATURES.md"
            path.write_text(content, encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "backlog-only"):
                load_features(path)

    def test_rejects_duplicate_feature_ids(self) -> None:
        with self.assertRaisesRegex(ValueError, "duplicate"):
            FeatureDocument(features=(feature(), feature()))

    def test_loads_the_current_pre_release_features_file(self) -> None:
        root = Path(__file__).resolve().parents[1]
        self.assertEqual(load_features(root / "FEATURES.md"), FeatureDocument(features=()))


if __name__ == "__main__":
    unittest.main()
