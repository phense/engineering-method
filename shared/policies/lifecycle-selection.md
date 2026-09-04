# Lifecycle Selection

Select exactly one primary lifecycle from the request and current artifact
state. Supporting skills may compose with it but never take ownership from it.

| Observable condition | Primary entry | Closest negative boundary |
|---|---|---|
| Observed failure, regression, or unexplained behavior | `systematic-debugging` | Not a deliberate behavior change without a defect |
| Bounded intentional change to an existing capability | `openspec-propose` | Not defect repair, a new subsystem, architecture, a risky migration, or tightly coupled cross-component work |
| New capability, cross-component feature, architecture, risky migration, or material unresolved design | `speckit-specify` | Not a localized Brownfield delta or ordinary defect |
| Existing lifecycle artifact awaiting its next phase | The phase named by that artifact state | Do not start a second lifecycle for the same work |
| Small reversible edit with no behavior-contract impact | Native focused edit | No specification, plan, architecture model, or implementation orchestrator |

An active OpenSpec change stays in OpenSpec unless its proposal records a formal
escalation. An active Spec Kit feature stays in Spec Kit. When the request is
ambiguous at the nearest boundary, inspect the affected code and artifacts
read-only; ask only if the answer would materially change scope or ownership.
