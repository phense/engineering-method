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
"$CONTINUITY_STATE" recover EM-002
```

Checkpoint without `--resume-file` preserves the existing brief. Recovery validates git, artifacts, canonical status, and live-agent evidence before choosing the next action. Persist concise facts only—never credentials, full prompts, environment dumps, or verbose command output.

## Operational handoffs

- At work start, run the automatic state check, initialize absent state, mark
  the stable backlog ID in progress, and initialize or recover its run.
- At scope change, update the same stable backlog ID and checkpoint the revised
  artifacts, pending work, and exact next action.
- At blocker discovery, record the blocker and dependencies so blocker-first
  ordering exposes the unblocker, then checkpoint the failing evidence.
- At each completed slice, update canonical backlog state and checkpoint the
  completed and pending work without duplicating completion.
- At every phase or final handoff, checkpoint the new active phase, artifact
  pointers, verification evidence, and next action before transferring control.

## Common mistakes

- Renumbering work after priority changes: update priority, never identity.
- Re-running `init` to repair state: use the specific update or recovery command.
- Treating no remote or no authentication as a workflow blocker: report the factual detection reason and remain local.
- Marking a feature available before integration: capability inventory follows verified implementation.
