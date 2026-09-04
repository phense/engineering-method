"""Test doubles shared by Engineering Method state tests."""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from typing import Sequence

from engineering_method.gh import GhResult


@dataclass(frozen=True)
class ExpectedGhCall:
    args: tuple[str, ...]
    result: GhResult
    stdin: str | None = None


class FakeGhRunner:
    """An ordered gh boundary that rejects each unexpected command immediately."""

    def __init__(self, expected: Sequence[ExpectedGhCall]) -> None:
        self._expected = deque(expected)

    def run(self, args: Sequence[str], *, stdin: str | None = None) -> GhResult:
        if not self._expected:
            raise AssertionError(f"unexpected gh call: {list(args)!r}")
        expected = self._expected.popleft()
        if tuple(args) != expected.args or stdin != expected.stdin:
            raise AssertionError(f"expected {expected.args!r} with {expected.stdin!r}, got {list(args)!r} with {stdin!r}")
        return expected.result

    def assert_drained(self) -> None:
        if self._expected:
            raise AssertionError(f"unconsumed gh calls: {list(self._expected)!r}")
