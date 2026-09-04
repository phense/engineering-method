---
name: project-backlog
description: "Use when engineering work needs durable backlog state, a capability inventory, GitHub Issue synchronization, offline mutation handling, or compact-continuity recovery. Do not use it to select or control an implementation methodology."
---

# Project Backlog

## Overview

Keep one canonical task history with stable IDs. `BACKLOG.md` is canonical in local mode; GitHub Issues are canonical after migration, and the generated local cache is read-only. GitHub-authored content is English.

This skill never selects or controls an implementation methodology. Resolve `<plugin-root>` as the directory two levels above this `SKILL.md`. Invoke bundled scripts from `<plugin-root>/scripts/` and set the process cwd to the target repository root for every command.

## State and local work

Run commands from the project root. Initialize only when state is absent:

```sh
<plugin-root>/scripts/project-state backlog init --project-key EM
<plugin-root>/scripts/project-state backlog state-check
```

Initialization is non-destructive. `--replace` is an explicit destructive reset. Add and update work with `backlog add|start|block|complete|priority|dependencies`; use `--depends-on ID[,ID]` for dependencies. Normal writes enforce blocker-first ordering and the archive threshold.

Persist an eligible archive explicitly when checking policy or after a bulk import:

```sh
<plugin-root>/scripts/project-state backlog archive
```

Record implemented capabilities with `feature add|change|remove`. Removal requires `--rationale`; planned work stays only in the backlog.

## GitHub mode and outage recovery

Migrate once, refresh without remote writes, and replay pending offline changes in order:

```sh
<plugin-root>/scripts/backlog-to-issues migrate
<plugin-root>/scripts/refresh-issue-cache
<plugin-root>/scripts/backlog-to-issues reconcile
```

In GitHub-cache mode, backlog mutation commands append idempotent queue records and do not alter the cache. Reconcile after connectivity returns; never edit the cache or queue by hand.

## Compact continuity

Supply state and events as repository-relative JSON files or stdin. Keep the recovery brief separate:

```sh
<plugin-root>/scripts/continuity-state init EM-002 --file state.json --resume-file resume.md
<plugin-root>/scripts/continuity-state checkpoint EM-002 --file state.json
<plugin-root>/scripts/continuity-state event EM-002 --file event.json
<plugin-root>/scripts/continuity-state status EM-002
<plugin-root>/scripts/continuity-state recover EM-002
```

Checkpoint without `--resume-file` preserves the existing brief. Recovery validates git, artifacts, canonical status, and live-agent evidence before choosing the next action. Persist concise facts only—never credentials, full prompts, environment dumps, or verbose command output.

## Common mistakes

- Renumbering work after priority changes: update priority, never identity.
- Re-running `init` to repair state: use the specific update or recovery command.
- Treating no remote or no authentication as a workflow blocker: report the factual detection reason and remain local.
- Marking a feature available before integration: capability inventory follows verified implementation.
