---
name: test-driven-development
description: "Use when testable behavior that is new or a confirmed defect needs verified tests before implementation, or when a behavior-preserving refactor needs characterization. Not for documentation, generated artifacts, or implementation-mirroring tests."
---

# Test-Driven Development

Write one behavior test, watch it fail for the expected reason, then write the
minimal implementation that makes it pass.

## Trigger

Use before implementing a feature, behavior change, defect repair, or refactor
whose consumer-visible contract can be exercised by a meaningful automated test.

## Do not use for

- Human documentation, planning prose, or generated artifacts.
- Trivial declarations with no behavior.
- Implementation-mirroring or source-text tests that cannot catch a realistic
  bug.

## The rule

New behavior and confirmed defects require verified red-green: run a meaningful
test and observe the expected failure before writing the implementation change.
Do not delete pre-existing code to manufacture a red state. Deletion applies
only to your own uncommitted and safely recoverable production diff written
before a required red test; restore that diff and begin from the behavior
contract.

A behavior-preserving refactor uses passing characterization tests before and
after every step to cover the preserved contract. Do not invent a failing
behavior when no behavior change is intended.

## Red green refactor

1. **Red:** Name the realistic production break the test catches. Derive the
   expected result independently, exercise real behavior, and write one focused
   test.
2. **Verify red:** Run the narrow test. It must fail, not crash, for the expected
   reason. A passing test covers existing behavior; an unrelated error needs
   correction before continuing.
3. **Green:** Write the minimal implementation needed for this behavior only.
4. **Verify green:** Run the narrow test and relevant affected tests. Read the
   output and ensure there are no new errors or warnings.
5. **Refactor:** Improve structure only while characterization and affected
   tests remain green. Start a new red cycle only for new or changed behavior.

## Test quality gate

Read [writing-good-tests.md](writing-good-tests.md) before writing or changing
tests. In particular:

- name the bug-producing mutation the test would catch;
- assert the consumer-visible result rather than a mock or private structure;
- use literal, hand-checked expectations instead of the implementation's helper;
- mock only the slow or external boundary after understanding the real side
  effects;
- include malformed, empty, unauthorized, and boundary cases when they are part
  of the contract.

## Completion

New or changed behavior is complete when the red failure and its reason were
observed, the minimal implementation passes the new test, affected tests pass,
and a realistic mutation would make at least one test fail. A behavior-preserving
refactor is complete when the characterization suite passed before and after the
change and the externally visible contract is unchanged.

## Handoff

Use `verification-before-completion` before reporting the behavior fixed or
passing. An unexpected failure during the cycle returns to
`systematic-debugging`; do not stack speculative changes on a failing green step.

## Warning signs

- The test passed before implementation.
- Setup and assertion compute the same value.
- The assertion proves a mock exists rather than behavior works.
- The test checks prose or source text instead of executing an artifact.
- Multiple behaviors or fixes are combined before the red result is understood.
