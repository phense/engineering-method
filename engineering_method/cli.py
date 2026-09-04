"""Command adapters; later task wiring owns the full user-facing command surface."""

from __future__ import annotations

import sys


def main(argv: list[str] | None = None) -> int:
    arguments = sys.argv[1:] if argv is None else argv
    if not arguments:
        print("project-state command required", file=sys.stderr)
        return 2
    print("project-state command wiring is completed by the acceptance command layer", file=sys.stderr)
    return 2
