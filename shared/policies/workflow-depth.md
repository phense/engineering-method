# Workflow Depth

Depth follows reversibility, ambiguity, architectural reach, data or security
risk, and integration surface.

Apply [proportionality](proportionality.md) at every depth, including reviews
and verification. Depth describes needed evidence, not an unlimited work budget.

| Work shape | Required depth |
|---|---|
| Small reversible edit | Project gates, focused edit, targeted verification |
| Observed defect | Reproduction, root-cause debugging, meaningful regression test when possible, focused fix, targeted verification |
| Bounded Brownfield delta | OpenSpec proposal, TDD where behavior is testable, apply, verification, archive |
| New or architecture-bearing feature | Spec Kit specification and plan, architecture analysis, dependency-ordered tasks, isolated implementation, as-built reconciliation, integration testing, convergence, review, verification |

Do not add lifecycle artifacts merely because tools are available. Add depth
when current evidence crosses a boundary above, and record the reason in the
owning artifact.

Reader-facing documentation has its own scale table in
[writing-depth](writing-depth.md); the [reader-oriented output
policy](reader-oriented-output.md) governs explanations, instructions and
troubleshooting help in ordinary replies.
