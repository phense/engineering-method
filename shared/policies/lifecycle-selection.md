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
| Documentation set: several chapters or documents sharing readers, terms, structure or images | `documentation-planning` | Not one standalone document, a wording fix, or software specification |
| One standalone reader-facing document | `documentation-authoring` | Not a sentence-level fix, a multi-document set, or an engineering artifact |

Prose work decides its scale first with the [writing-depth
policy](writing-depth.md); existing `docs/writing/<doc-id>/` artifacts fix the
scale and phase. An active OpenSpec change stays in OpenSpec unless its proposal records a formal
escalation. An active Spec Kit feature stays in Spec Kit. When the request is
ambiguous at the nearest boundary, inspect the affected code and artifacts
read-only; ask only if the answer would materially change scope or ownership.

## Engineering playbooks

Scenario-bound development and system-deliverable playbooks use
`playbook-authoring` and `playbook-review` under the
[playbook policy](playbooks.md). They are engineering artifacts, including when
their audience is an end user, and retain the owning engineering work ID.
Direct requests enter the supporting skill without starting a new lifecycle.
Generic manuals and tutorials retain the documentation routes above. A request
for new system behavior still enters the appropriate engineering phase first.
