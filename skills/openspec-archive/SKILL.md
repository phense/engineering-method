---
name: openspec-archive
description: "Use when an implemented OpenSpec change has all tasks complete and fresh verification passing and its accepted requirement delta must be synchronized and archived. Not for incomplete, failing, or escalated changes."
---

# OpenSpec Archive

Apply the shared [proportionality rule](../../shared/policies/proportionality.md)
before adding work, delegating, or repeating verification.

Synchronize an accepted delta into the main capability specifications and move
the completed change to its dated archive. Archival is an evidence gate, not a
waiver mechanism.

## Recovery preamble

Before synchronization or movement:

1. Invoke `project-backlog` for read-only discovery: discover an active run
   for the stable work ID before requesting agent status. Only a verified absent
   run may enroll in the new-run-only coordinator-only mode described there.
2. For an existing ordinary run, obtain host-observed live agent IDs through
   the platform capability seam and call `continuity-state recover --live-agents`.
   Use an explicit empty observation only when the host confirms none are live.
   With no observation, only verified coordinator-only provenance permits
   `continuity-state recover --coordinator-only`; saved or uncertain agent
   activity remains blocked. Never fabricate observed IDs.
3. Complete recovery, or verified absent-run initialization, before any canonical
   or backlog mutation. The coordinator-only mode permits sequential continuity
   across phase handoffs, not delegation or bypass of independent-review gates.
4. Read the run's `state.json` and `resume.md` when a run exists.
5. Check recorded commits, worktree, artifacts, and canonical backlog or issue
   state against current reality.
6. Reconcile saved agent identities with agents still available from the host;
   coordinator-only recovery must verify that no saved agent history exists.
7. Preserve validated completed work and never redispatch completed work after
   compaction or resumption.
8. Reconstruct stale state from git and canonical artifacts when they disagree.
9. Continue from the validated next action.

Repository evidence wins over stale checkpoint or memory data. Never silently
restart or reclassify an active workflow.

## Operational state handoffs

Follow the [transition-to-event ordering
contract](../project-backlog/SKILL.md#transition-to-event-ordering):

1. After each durable transition, invoke `project-backlog` to call
   `continuity-state event` with the applicable event and its concise facts.
2. Then call `continuity-state checkpoint` with current state and the exact next
   action, except where the dispatch or completion protocol requires two
   checkpoints.
3. Event emission is never automatic. Claim it only after the event call
   succeeds, and likewise verify every checkpoint call.

Apply this protocol while updating backlog state and the run checkpoint at work
start, scope change, blocker discovery, each completed slice, and every phase or
final handoff.

## Trigger

Use only when one active OpenSpec change is fully implemented, every task is
checked, all accepted delta requirements are present, and fresh targeted
verification passes.

## Do not use for

- Any incomplete task, failed or stale verification, unresolved review finding,
  missing delta artifact, or merge conflict.
- A change with `status: escalated`.
- Implementing or repairing application behavior.

## Consumes

- The complete active directory at `docs/openspec/changes/<change-id>/`.
- Each delta spec under `docs/specs/<capability>/spec.md` within that change.
- The corresponding main `docs/openspec/specs/<capability>/spec.md` files.
- Completed task state, resolved review state, and fresh verification output.

## Produces

- Main capability specs updated with accepted added, modified, removed, or
  renamed requirements while preserving unaffected requirements and scenarios.
- The completed directory moved to
  `docs/openspec/changes/archive/yyyy-mm-dd-<change-id>/` without adding a second date
  when the change ID is already date-prefixed.
- A concise archive summary naming synchronized capabilities and evidence.

## Completion

Refuse to archive when there is an incomplete task, missing artifact, unresolved
finding, failed verification, or sync mismatch. Completion requires a
byte-for-byte preserved change directory at the unique archive destination, all
delta requirements reflected in main specs, and no active source directory.

## Next phase

None. This is the terminal OpenSpec lifecycle phase.

## Supporting skills

- `project-backlog` for recovery, canonical task state, events, and checkpoints.
- `verification-before-completion` for fresh task, sync, and movement evidence.

## No implementation boundary

This phase must not edit application code. It may update main capability specs
and move the completed change directory only after every gate passes.

## Workflow

1. Re-read all artifacts and count checked and unchecked tasks.
2. Require fresh verification that covers the accepted delta and compatibility
   boundary.
3. Compare every delta requirement with its main capability spec and prepare a
   deterministic merge preserving unaffected content.
4. Stop on ambiguity, collision, or any incomplete evidence before changing a
   main spec or moving the directory.
5. Apply the merge, then re-read every affected main spec and verify exact delta
   semantics.
6. Ensure the archive destination does not exist, move the entire change, and
   verify the source is absent and destination complete.

## Delta merge contract

Before any main-spec write, validate stable requirement identities and reject
duplicates or cross-operation conflicts. Stop on conflict and leave both the
main spec and active change in place.

If the main spec does not exist, only ADDED requirements are valid and Purpose
must seed the new capability. MODIFIED or RENAMED is an error; REMOVED has no
target and cannot justify creating an empty capability.

For an existing main spec, apply operations in this deterministic order:
RENAMED then REMOVED then MODIFIED then ADDED.

1. RENAMED changes only the exact requirement heading from FROM to TO. The FROM
   identity must exist and TO must not collide.
2. REMOVED deletes the exact requirement block and requires the authored Reason
   and Migration. Never leave an empty Requirements section or delete unrelated
   prose.
3. MODIFIED is a complete replacement block. Its stable requirement identity
   must match the current block or the new TO identity from a rename, and it must
   contain every surviving scenario. Missing scenarios are a hard error, not
   permission to merge partial content.
4. ADDED requires a new stable identity. An identical already-present block is
   an already-synchronized no-op; differing content is a conflict.

Recompose the main spec under one `## Requirements` section without delta
operation headers, then re-read it and prove every operation before moving the
change directory.
