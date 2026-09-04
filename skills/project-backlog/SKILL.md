---
name: project-backlog
description: "Use as a supporting skill when engineering work needs durable backlog state, capability inventory updates, GitHub Issue synchronization, offline mutation handling, or compact-continuity recovery. Never use it to select or control an implementation methodology."
---

# Project Backlog

## Overview

Keep one canonical task history with stable IDs. `BACKLOG.md` is canonical in
local mode; GitHub Issues are canonical after migration, and the generated
local cache is read-only. GitHub-authored content is English.

## Responsibilities

- State initialization only when absent.
- Stable-ID status, priority, dependency, and blocker updates.
- Blocker-first ordering without renumbering work.
- FEATURES.md handoff after a user-visible or architectural capability is
  verified as added, changed, or removed.
- Automatic GitHub-mode detection and ordered offline reconciliation.
- Cache refresh without turning the cache into canonical state.
- Continuity pointers to run state, resume briefs, decisions, reports, and
  events.

## Methodology boundary

This is a supporting state skill. Never classify a request, choose a primary
lifecycle, or control implementation methodology. The active lifecycle or
coordinator supplies the stable work ID, phase, status change, and next action;
this skill persists those facts without reinterpreting them.

## Bundled script resolution

The bundled entry points are:

- [`project-state`](../../scripts/project-state)
- [`backlog-to-issues`](../../scripts/backlog-to-issues)
- [`refresh-issue-cache`](../../scripts/refresh-issue-cache)
- [`continuity-state`](../../scripts/continuity-state)

Resolve each link relative to the directory containing this `SKILL.md`, then
convert it to an absolute path before invocation. Set the process cwd to the
target repository root for every command. Never treat `scripts/...` as relative
to the target repository. In the examples below, the uppercase variables refer
to those resolved absolute paths.

## Recovery gate

1. Obtain the host-observed live agent IDs through the platform capability seam.
   If the host cannot observe agent state, stop before mutation.
2. Discover an active run for the stable work ID. For every existing run, pass
   the observation explicitly to `continuity-state recover --live-agents`. Use
   an explicit empty observation only when the host confirms none are live;
   never omit the option. If no run exists, verify and record that absence.
3. Complete recovery, or the verified no-run result, before any canonical or
   backlog mutation, including state check, migration, refresh, queue replay,
   status changes, dependency changes, and feature updates.
4. Read `state.json` and `resume.md`, then reconcile commits, worktree,
   artifacts, canonical backlog or issue state, and saved agent identities.
5. Preserve completed work, keep observed live agents active, and expose only
   unavailable saved agents as redispatchable.

Repository and remote evidence wins over stale checkpoint or memory data.

## State and local work

Run commands from the project root. Initialize only when state is absent:

```sh
"$PROJECT_STATE" backlog init --project-key EM
"$PROJECT_STATE" backlog state-check
```

Initialization is non-destructive. `--replace` is an explicit destructive reset. Add and update work with `backlog add|start|block|complete|priority|dependencies`; use `--depends-on ID[,ID]` for dependencies. Normal writes enforce blocker-first ordering and the archive threshold.

Persist an eligible archive explicitly when checking policy or after a bulk import:

```sh
"$PROJECT_STATE" backlog archive
```

Record implemented capabilities with `feature add|change|remove`. Removal requires `--rationale`; planned work stays only in the backlog.

## GitHub mode and outage recovery

Migrate once, refresh without remote writes, and replay pending offline changes in order:

```sh
"$BACKLOG_TO_ISSUES" migrate
"$REFRESH_ISSUE_CACHE"
"$BACKLOG_TO_ISSUES" reconcile
```

In GitHub-cache mode, backlog mutation commands append idempotent queue records and do not alter the cache. Reconcile after connectivity returns; never edit the cache or queue by hand.

## Compact continuity

Supply state and events as repository-relative JSON files or stdin. Keep the recovery brief separate:

```sh
"$CONTINUITY_STATE" init EM-002 --file state.json --resume-file resume.md
"$CONTINUITY_STATE" checkpoint EM-002 --file state.json
"$CONTINUITY_STATE" event EM-002 --file event.json
"$CONTINUITY_STATE" status EM-002
"$CONTINUITY_STATE" recover EM-002 --live-agents "$LIVE_AGENT_IDS"
```

Checkpoint without `--resume-file` preserves the existing brief. Recovery validates git, artifacts, canonical status, and live-agent evidence before choosing the next action. Persist concise facts only—never credentials, full prompts, environment dumps, or verbose command output.

## Transition-to-event ordering

The machine-readable contract is:

```json
{
  "event_order": [
    "workflow_started",
    "phase_changed",
    "slice_started",
    "decision_recorded",
    "agent_dispatched",
    "agent_completed",
    "verification_failed",
    "verification_passed",
    "workflow_completed"
  ],
  "transition_write_order": [
    "recover",
    "durable_transition",
    "event",
    "checkpoint"
  ],
  "agent_dispatch_order": [
    "recover",
    "checkpoint_before_dispatch",
    "host_dispatch",
    "agent_dispatched",
    "checkpoint_after_dispatch"
  ],
  "workflow_completion_order": [
    "verification_passed",
    "checkpoint",
    "canonical_completion",
    "workflow_completed",
    "checkpoint"
  ]
}
```

`event_order` defines causal order for applicable events. Emit
`workflow_started` once and first. Emit `phase_changed` before the first
`slice_started` in that phase. Persist a decision before `decision_recorded` and
before work that depends on it. Emit each `agent_dispatched` after the host
returns its agent ID and before the matching `agent_completed`. Emit
`verification_failed` or `verification_passed` only after reading the check's
exit status and complete output. A failed verification may return to another
phase or slice loop; a final `verification_passed` precedes canonical completion.
Emit `workflow_completed` once and last.

For an ordinary transition, recover first, make the durable artifact or
canonical transition, explicitly write one JSON event file and call
`"$CONTINUITY_STATE" event <work-id> --file <event.json>`, then write the new
state/resume input and call `"$CONTINUITY_STATE" checkpoint <work-id> --file
<state.json>`. Agent dispatch uses both checkpoints in
`agent_dispatch_order`. Workflow completion uses the exact five operations in
`workflow_completion_order`.

Event emission is never automatic. Do not claim an event was recorded unless
the explicit `event` call succeeds, and do not claim a checkpoint unless the
explicit `checkpoint` call succeeds.

## Operational handoffs

- At work start, complete the Recovery gate first. After a verified no-run
  result, initialize missing state from the supplied stable work ID. Only then
  run the automatic state check and mark the stable backlog ID in progress.
- At scope change, recover first, update the same stable backlog ID, emit the
  applicable event, and checkpoint revised artifacts, pending work, and next
  action.
- At blocker discovery, recover first, record the blocker and dependencies so
  blocker-first ordering exposes the unblocker, emit the applicable event, and
  checkpoint the failing evidence.
- At each completed slice, recover first, update canonical backlog state, emit
  the applicable event, and checkpoint completed and pending work without
  duplicating completion.
- At every phase or final handoff, recover first, emit the applicable event, and
  checkpoint the new phase, artifact pointers, verification evidence, and next
  action before transferring control.

## Common mistakes

- Renumbering work after priority changes: update priority, never identity.
- Re-running `init` to repair state: use the specific update or recovery command.
- Treating no remote or no authentication as a workflow blocker: report the factual detection reason and remain local.
- Marking a feature available before integration: capability inventory follows verified implementation.
