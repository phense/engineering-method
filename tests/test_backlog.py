"""Tests for the local canonical backlog and completed-work archive policy."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
import tempfile
import unittest
from pathlib import Path

from engineering_method.backlog import (
    BacklogDocument,
    archive_completed_groups,
    load_backlog,
    ordered_items,
    render_backlog,
)
from engineering_method.models import BacklogItem, Priority, TaskStatus


def item(
    identifier: str,
    *,
    status: TaskStatus = TaskStatus.OPEN,
    priority: Priority = Priority.P1,
    parent_id: str | None = None,
    depends_on: tuple[str, ...] = (),
    updated_at: str = "2026-09-04T10:20:30Z",
) -> BacklogItem:
    """Create a hand-specified task to exercise backlog behavior."""
    return BacklogItem(
        id=identifier,
        title=f"Task {identifier}",
        status=status,
        priority=priority,
        parent_id=parent_id,
        depends_on=depends_on,
        notes="Operator context",
        updated_at=updated_at,
    )


class BacklogRenderingTests(unittest.TestCase):
    def test_rendered_tasks_have_markers_and_all_status_presentations(self) -> None:
        document = BacklogDocument(
            project_key="EM",
            mode="local",
            items=(
                item("EM-001", status=TaskStatus.OPEN),
                item("EM-002", status=TaskStatus.IN_PROGRESS),
                item("EM-003", status=TaskStatus.COMPLETE),
                item("EM-004", status=TaskStatus.BLOCKED),
            ),
        )

        rendered = render_backlog(document)

        for emoji, identifier in (("⭕", "EM-001"), ("🔄", "EM-002"), ("✅", "EM-003"), ("❌", "EM-004")):
            marker = f'<!-- engineering-method:backlog {{"schema_version":1,"id":"{identifier}"'
            self.assertIn(marker, rendered)
            self.assertIn(f"- {emoji} `{identifier}` **P1** Task {identifier}", rendered)

    def test_round_trip_preserves_stable_ids_across_status_and_priority_changes(self) -> None:
        original = BacklogDocument(
            project_key="EM",
            mode="local",
            items=(
                item("EM-001", status=TaskStatus.IN_PROGRESS, priority=Priority.P0),
                item("EM-001.1", parent_id="EM-001", status=TaskStatus.COMPLETE),
            ),
        )
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "BACKLOG.md"
            path.write_text(render_backlog(original), encoding="utf-8")

            loaded = load_backlog(path)

        self.assertEqual([entry.id for entry in loaded.items], ["EM-001", "EM-001.1"])
        self.assertEqual(loaded.items[0].status, TaskStatus.IN_PROGRESS)
        self.assertEqual(loaded.items[0].priority, Priority.P0)
        self.assertEqual(loaded.items[1].parent_id, "EM-001")

    def test_loads_the_existing_backlog_without_changing_its_stable_ids_or_meanings(self) -> None:
        root = Path(__file__).resolve().parents[1]
        legacy = load_backlog(root / "BACKLOG.md")
        with tempfile.TemporaryDirectory() as temporary:
            rendered_path = Path(temporary) / "BACKLOG.md"
            rendered_path.write_text(render_backlog(legacy), encoding="utf-8")
            reparsed = load_backlog(rendered_path)

        original_meanings = {
            entry.id: (entry.title, entry.status, entry.priority, entry.parent_id, entry.depends_on)
            for entry in legacy.items
        }
        rendered_meanings = {
            entry.id: (entry.title, entry.status, entry.priority, entry.parent_id, entry.depends_on)
            for entry in reparsed.items
        }
        self.assertEqual(legacy.project_key, "EM")
        self.assertEqual(rendered_meanings, original_meanings)
        self.assertTrue(
            {
                "EM-000",
                "EM-001",
                "EM-001.1",
                "EM-002",
                "EM-002.1",
                "EM-002.7",
                "EM-003",
                "EM-003.1",
                "EM-003.6",
                "EM-004",
                "EM-005",
                "EM-005.6",
            }
            <= original_meanings.keys()
        )


class BacklogValidationTests(unittest.TestCase):
    def test_rejects_missing_dependencies(self) -> None:
        with self.assertRaisesRegex(ValueError, "dependency"):
            BacklogDocument(project_key="EM", mode="local", items=(item("EM-001", depends_on=("EM-999",)),))

    def test_rejects_dependency_cycles(self) -> None:
        document = BacklogDocument(
            project_key="EM",
            mode="local",
            items=(
                item("EM-001", depends_on=("EM-002",)),
                item("EM-002", depends_on=("EM-001",)),
            ),
        )
        with self.assertRaisesRegex(ValueError, "cycle"):
            ordered_items(document.items)

    def test_rejects_a_project_key_that_does_not_match_item_ids(self) -> None:
        with self.assertRaises(ValueError):
            BacklogDocument(project_key="OTHER", mode="local", items=(item("EM-001"),))


class BacklogOrderingTests(unittest.TestCase):
    def test_orders_top_level_groups_by_priority(self) -> None:
        items = (
            item("EM-001", priority=Priority.P3),
            item("EM-002", priority=Priority.P0),
            item("EM-003", priority=Priority.P1),
        )
        self.assertEqual([entry.id for entry in ordered_items(items)], ["EM-002", "EM-003", "EM-001"])

    def test_places_an_unblocker_before_its_blocked_work(self) -> None:
        items = (
            item("EM-001", priority=Priority.P0),
            item("EM-002", status=TaskStatus.BLOCKED, priority=Priority.P0, depends_on=("EM-003",)),
            item("EM-003", priority=Priority.P3),
        )
        self.assertEqual([entry.id for entry in ordered_items(items)], ["EM-003", "EM-002", "EM-001"])

    def test_keeps_children_next_to_their_parent_groups(self) -> None:
        items = (
            item("EM-001", priority=Priority.P1),
            item("EM-001.1", parent_id="EM-001", priority=Priority.P3),
            item("EM-002", priority=Priority.P0),
            item("EM-002.1", parent_id="EM-002", priority=Priority.P3),
        )
        self.assertEqual(
            [entry.id for entry in ordered_items(items)],
            ["EM-002", "EM-002.1", "EM-001", "EM-001.1"],
        )


class BacklogArchiveTests(unittest.TestCase):
    def test_archives_only_oldest_completed_top_level_groups_until_active_render_is_small(self) -> None:
        started = datetime(2020, 1, 1, tzinfo=timezone.utc)
        completed = tuple(
            item(
                f"EM-{number:03d}",
                status=TaskStatus.COMPLETE,
                updated_at=(started + timedelta(days=number)).strftime("%Y-%m-%dT%H:%M:%SZ"),
            )
            for number in range(1, 261)
        )
        protected = (
            item("EM-901", status=TaskStatus.OPEN),
            item("EM-902", status=TaskStatus.IN_PROGRESS),
            item("EM-903", status=TaskStatus.BLOCKED),
        )
        document = BacklogDocument(project_key="EM", mode="local", items=completed + protected)

        active, archived = archive_completed_groups(document)

        self.assertGreater(len(archived), 0)
        self.assertEqual([entry.id for entry in archived], sorted((entry.id for entry in archived)))
        self.assertTrue(all(entry.status is TaskStatus.COMPLETE for entry in archived))
        self.assertTrue({"EM-901", "EM-902", "EM-903"} <= {entry.id for entry in active.items})
        self.assertLessEqual(len(render_backlog(active).splitlines()), 350)
        self.assertGreater(len(render_backlog(document).splitlines()), 500)

    def test_refuses_to_archive_the_generated_github_cache(self) -> None:
        document = BacklogDocument(
            project_key="EM",
            mode="github-cache",
            items=(item("EM-001", status=TaskStatus.COMPLETE),),
        )
        with self.assertRaisesRegex(ValueError, "github-cache"):
            archive_completed_groups(document, active_line_limit=1, target_line_limit=1)


if __name__ == "__main__":
    unittest.main()
