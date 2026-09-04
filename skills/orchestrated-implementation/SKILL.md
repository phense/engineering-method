---
name: orchestrated-implementation
description: "Use when approved Spec Kit tasks.md and architecture findings are ready for cohesive-slice implementation of a large feature. Not for small changes, bug diagnosis, or OpenSpec apply."
---

# Orchestrated Implementation

Execute one approved large-feature plan as cohesive, independently verifiable
slices. The coordinator remains responsible for architecture, interfaces,
cross-slice state, integration, and acceptance.

```json
{
  "inputs": ["spec_kit_tasks", "architecture_findings", "work_id", "project_gates"],
  "run_root": ".engineering-method/runs/<work-id>/",
  "next_phase": "speckit-converge",
  "slice_rules": {
    "adjacent_tiny_same_shape": "batch",
    "shared_interface": "serialize",
    "parallel_requires": ["disjoint_paths", "disjoint_interfaces", "safe_isolation", "integration_order"]
  },
  "review": {
    "mechanical": "coordinator_allowed",
    "independent_required": ["security", "migration", "interface", "concurrency", "cross_component"]
  },
  "checkpoint_boundaries": ["before_dispatch", "after_dispatch", "after_implementation", "after_test", "after_review", "after_fix", "before_long_wait", "handoff"]
}
```

## Recovery preamble

Before implementation or any canonical mutation:

1. Obtain host-observed live agent identities through the platform capability
   seam. If observation is unavailable, stop before mutation; an empty set is
   valid only when the host confirms no agents are live.
2. Invoke `project-backlog` and its existing EM-002 `continuity-state recover`
   interface for the supplied work ID, passing the explicit observation.
3. Read `state.json` and `resume.md`, then validate the worktree, base and head
   commits, task and architecture artifacts, reports, and canonical backlog or
   issue state against current repository evidence.
4. Preserve completed slices, retain observed active agents, make only missing
   active agents redispatchable, and resume exactly the validated next action.

Repository evidence wins over stale checkpoints and recalled memory. Never
silently restart, reclassify, or redispatch completed work.

## Operational state handoffs

Use the [EM-002 transition and event
protocol](../project-backlog/SKILL.md#transition-to-event-ordering) and the
[continuity contract](../../shared/policies/continuity-contract.md). The
coordinator is the sole writer of state.json, resume.md, decisions, and events.
Subagents write only their named report file.

- Checkpoint immediately before host dispatch and again after the host returns
  an identity; emit `agent_dispatched` between those durable states.
- After implementation, test, review, and every fix transition, emit the
  applicable event and checkpoint the evidence plus exact next action.
- Checkpoint before a long wait, after each completed slice, at every phase
  transition, and at final handoff.
- Never claim an event, checkpoint, or agent completion until its operation has
  succeeded and its result has been read.

These calls consume the existing EM-002 service. Do not create a second ledger,
state schema, event vocabulary, or recovery implementation.

## Trigger

Use only when an approved Spec Kit `tasks.md`, completed design-time
architecture findings, stable work ID, and current project gates exist for a
large feature or architecture-bearing change awaiting implementation.

## Do not use for

- Small, reversible, or mechanical changes that do not need a large-feature
  executor.
- Defect diagnosis before root cause is known.
- OpenSpec apply or any other active primary lifecycle.
- Task generation, architecture design, or convergence.

## Consumes

- `specs/<stable-feature-id>-<name>/tasks.md` with cohesive slices and stable
  requirement/finding references.
- `docs/uml/findings.md` and the relevant design-time diagrams.
- The stable work ID and current EM-002 run state.
- Applicable project gates, specification, plan, interfaces, and test commands.

## Produces

- File-backed slice briefs derived with [`task-brief`](../../scripts/task-brief).
- One agent report per assigned agent using the [report
  contract](../../templates/orchestration/agent-report.md).
- Complete-range review artifacts derived with
  [`review-package`](../../scripts/review-package).
- Tested slice commits, resolved finding evidence, integrated implementation,
  and the durable state needed by architecture reconciliation and convergence.

## Completion

Every task is implemented or has a recorded terminal blocker; all actionable
findings are resolved; slice and integrated tests pass; reports and complete
diffs are reconciled; as-built architecture and system integration evidence
exist; and the coordinator records a fresh handoff checkpoint.

## Next phase

`architecture-modeling` performs as-built reconciliation and the
system-architect integration gate, then hands the complete evidence to
`speckit-converge`.

## Supporting skills

- `project-backlog` for the existing continuity API, events, checkpoints, and
  canonical work status.
- `test-driven-development` for new behavior and
  characterization-green refactoring where behavior must be preserved.
- `using-git-worktrees` and `dispatching-parallel-agents` when the isolation and
  independence gates pass.
- `requesting-code-review` and `receiving-code-review` for risk-proportionate
  review and evidence-based feedback handling.
- `verification-before-completion` for fresh evidence.

## Coordinator setup

1. Re-read the approved tasks, findings, specification, plan, and project
   gates from disk after recovery.
2. Build a dependency and ownership table. Record interfaces shared across
   tasks and the integration order before grouping slices.
3. Resolve the capability role through the [host-neutral routing
   policy](../../shared/policies/model-routing.md). The later platform adapter
   inspects actual availability and performs any fallback.
4. Record the base commit for each slice before dispatch or local execution.

## Slice formation

Batch adjacent tiny tasks only when they have the same change shape, ownership,
dependencies, and one targeted verification outcome. Never split a tightly
coupled interface change across concurrent writers. Tasks that produce and
consume one interface remain serial until the coordinator verifies it stable.

Parallel writes are optional. They require disjoint paths, disjoint interfaces,
safe host-owned isolation, separate mutable resources, a declared integration
order, and acceptance evidence. If any fact is unknown, serialize writes while
allowing independent read-only investigation or review.

## Slice loop

For each slice:

1. Create a brief from the exact task section and fill the [slice
   contract](../../templates/orchestration/slice-brief.md) with ownership,
   interfaces, dependencies, base commit, tests, and report path.
2. Select `fast` only for fully specified mechanical work, `standard` for
   normal multi-file work, or `strong` for design judgment, difficult
   debugging, and integration. Optimize completed-task turns.
3. Perform the dispatch checkpoint protocol. If subagents are unavailable,
   execute the slice sequentially in the coordinator without claiming a model
   or agent change.
4. Implement through test-first red/green or characterization-green refactoring
   as appropriate. The assigned agent changes only owned paths and writes only
   its named report.
5. Validate the report's identity, commits/files, exact test commands/results,
   root-cause or fix findings, concerns, and next dependency facts against the
   repository.
6. Build a review package from the recorded base to the current head. A
   coordinator may review mechanical work; security, migration, interface,
   concurrency, data-integrity, and cross-component work requires an
   independent reviewer.
7. Route actionable findings through the [defect convergence
   policy](../../shared/policies/defect-convergence.md), package every fix range,
   and re-review it.
8. Integrate only after the slice is clean, then checkpoint completed and
   pending work without duplicating completion.

## Review and integration

A report is not proof. Inspect the full base-to-head diff and compare it with
the approved requirements, owned paths, and stable interfaces. Review every
fix range. Before accepting combined work, verify integration order and rerun
the narrowest cross-slice checks capable of catching an interface break; use a
broader suite at the final integration boundary.

Do not silently park actionable findings. Do not impose a fixed retry count.
Progress is bounded by new evidence and by the terminal conditions in the
defect-convergence policy.
