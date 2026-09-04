---
name: receiving-code-review
description: "Use when review feedback is received and must be understood, checked against the current repository, and resolved. Not for blindly implementing suggestions or accepting a verdict without evidence."
---

# Receiving Code Review

Treat feedback as a technical hypothesis. Understand it, verify against current
code and governing requirements, then act on evidence.

## Evaluate first

1. Read all findings and their claimed dependencies.
2. Restate each technical requirement in concrete terms. If any item is unclear
   and could affect another, clarify before implementing the set.
3. Verify against current code, tests, platform or version constraints, project
   decisions, and actual call sites.
4. Decide whether the finding is correct, already resolved, out of scope,
   incompatible, or based on incomplete context.
5. Give concise technical pushback with paths and evidence when a suggestion is
   unsound. Escalate a conflict with an approved architecture or user decision.

External review is not automatically authoritative. Current user instructions,
project gates, approved artifacts, and repository evidence retain their normal
authority.

## Resolve findings

Work one finding at a time in impact and dependency order:

1. Critical security, data, or broken-behavior issues.
2. Important requirement, architecture, interface, and test gaps.
3. Accepted Minor improvements within current scope.

For behavior changes, use `test-driven-development` and observe a meaningful
failure before the fix. Run the narrow affected checks after each correction,
then use `verification-before-completion` before claiming the finding resolved.
Re-review when a correction changes an interface or integration boundary.

## Completion

Feedback handling is complete when every finding has a technically evidenced
disposition, accepted changes are implemented and freshly verified, rejected
changes have a concise reason, and no Critical or Important finding remains open.

## Common mistakes

- Agreeing performatively before checking the code.
- Implementing understood items while a related item remains ambiguous.
- Adding an unused abstraction because it sounds more professional.
- Applying a reviewer suggestion that breaks compatibility or an approved
  decision.
- Batch-fixing several findings without isolating their tests and evidence.
