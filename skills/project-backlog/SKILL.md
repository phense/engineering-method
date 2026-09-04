---
name: project-backlog
description: "Use when engineering work needs durable backlog state, a capability inventory, GitHub Issue synchronization, offline mutation handling, or compact-continuity recovery."
---

# Project Backlog

## Overview

Keep one canonical task history with stable IDs. `BACKLOG.md` is canonical in local mode; GitHub Issues are canonical after migration, and the generated local cache is read-only. GitHub-authored content is English.

## State and local work

Run commands from the project root. Initialize only when state is absent:

```sh
scripts/project-state backlog init --project-key EM
scripts/project-state backlog state-check
```

Initialization is non-destructive. `--replace` is an explicit destructive reset. Add and update work with `backlog add|start|block|complete|priority|dependencies`; use `--depends-on ID[,ID]` for dependencies. Normal writes enforce blocker-first ordering and the archive threshold.

Persist an eligible archive explicitly when checking policy or after a bulk import:

```sh
scripts/project-state backlog archive
```

Record implemented capabilities with `feature add|change|remove`. Removal requires `--rationale`; planned work stays only in the backlog.

## GitHub mode and outage recovery

Migrate once, refresh without remote writes, and replay pending offline changes in order:

```sh
scripts/backlog-to-issues migrate
scripts/refresh-issue-cache
scripts/backlog-to-issues reconcile
```

In GitHub-cache mode, backlog mutation commands append idempotent queue records and do not alter the cache. Reconcile after connectivity returns; never edit the cache or queue by hand.

## Compact continuity

Supply state and events as repository-relative JSON files or stdin. Keep the recovery brief separate:

```sh
scripts/continuity-state init EM-002 --file state.json --resume-file resume.md
scripts/continuity-state checkpoint EM-002 --file state.json
scripts/continuity-state event EM-002 --file event.json
scripts/continuity-state status EM-002
scripts/continuity-state recover EM-002
```

Checkpoint without `--resume-file` preserves the existing brief. Recovery validates git, artifacts, canonical status, and live-agent evidence before choosing the next action. Persist concise facts only—never credentials, full prompts, environment dumps, or verbose command output.

## Common mistakes

- Renumbering work after priority changes: update priority, never identity.
- Re-running `init` to repair state: use the specific update or recovery command.
- Treating no remote or no authentication as a workflow blocker: report the factual detection reason and remain local.
- Marking a feature available before integration: capability inventory follows verified implementation.
