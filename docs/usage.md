# Usage examples

Start the host in the project you want to change. Describe the outcome and
constraints; the host uses skill descriptions and current artifacts to choose
the workflow. The following are example requests, not guaranteed transcripts.

## Make a small edit

> Fix the broken installation link in README.md and verify the affected links.

A reversible documentation edit uses a focused edit and verification. It should
not create a specification, architecture diagrams or a delegation cycle.

## Repair a reproducible failure

> The checkout test fails when payment succeeds but inventory reservation fails.
> Reproduce it, find the cause and fix it without changing the API contract.

`systematic-debugging` establishes the cause; a meaningful regression test
supports the fix. Review and fresh verification apply according to risk. An
unverified review allegation enters `receiving-code-review` first.

## Change an existing capability

> Add a configurable timeout to this existing export command. Keep its output
> format and the other commands unchanged.

A bounded Brownfield change uses OpenSpec: `openspec-propose` records the delta
requirements, design and tasks under `openspec/changes/<change>/`;
`openspec-apply` implements an approved complete change; `openspec-archive`
synchronizes and archives its verified requirements. If inspection exposes a
new system boundary or risky migration, record the escalation before handing
over to Spec Kit. Do not silently grow the original proposal.

## Build a large feature

> Add a checkout flow spanning inventory, payment and order persistence, with
> recovery after partial failure. Inspect the existing system before specifying it.

Spec Kit proceeds through `speckit-specify`, `speckit-plan`, the architecture
gate, `speckit-tasks`, `orchestrated-implementation` and `speckit-converge`.
Specification artifacts live under `specs/<feature>/`. Relevant diagrams and
findings live under `docs/uml/` in the target project. Each diagram answers a
named question; diagram count is not an acceptance criterion.

Design findings become tasks. After implementation, reconcile diagrams with
code, derive success and relevant failure/recovery integration checks, and
resolve review findings before convergence. The shared policies favor cohesive
slices and reuse unchanged evidence. Additional expensive runs or reviews need
a concrete unresolved question and must respect user effort limits.

## Resume work

> Resume work item APP-014 from its repository checkpoint. Reconcile Git,
> artifacts, task status and current agents before continuing.

Stateful workflows save `.engineering-method/runs/APP-014/` with `state.json`,
`resume.md`, decisions, reports and events. Checkpoints must actually be written;
a compact or a new session cannot recover unsaved work. Repository evidence
wins over remembered state. agentic-rag may recall a work ID and artifact links,
but is optional and never the canonical state writer.

## Maintain task state

> Update APP-014 in the local backlog and record its verified capability in
> FEATURES.md. Do not migrate or create GitHub Issues.

`project-backlog` preserves stable IDs, blocker-first ordering and dependencies.
`FEATURES.md` describes working capabilities, not proposed work. With separate
permission, GitHub migration maps hierarchy to Sub-Issues and dependencies to
native dependency edges. After migration, Issues become canonical and the local
backlog is a marked cache; offline changes queue for reconciliation. Publishing
a repository alone does not authorize migrating its tasks.
