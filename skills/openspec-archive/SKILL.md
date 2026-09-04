---
name: openspec-archive
description: "Use when an implemented OpenSpec change has all tasks complete and fresh verification passing and its accepted requirement delta must be synchronized and archived. Not for incomplete, failing, or escalated changes."
---

# OpenSpec Archive

Synchronize an accepted delta into the main capability specifications and move
the completed change to its dated archive. Archival is an evidence gate, not a
waiver mechanism.

## Recovery preamble

Before synchronization or movement:

1. Look for a relevant `.engineering-method/runs/<work-id>/state.json` and
   `resume.md`.
2. Compare recorded commits, worktree, artifacts, and canonical task state with
   the repository.
3. Repository evidence wins over stale checkpoint or memory data.
4. Preserve validated completed work and never redispatch completed work after
   compaction or resumption.
5. Continue the recorded next action when it still matches current evidence;
   otherwise reconstruct the phase from git and canonical artifacts.

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

- The complete active directory at `openspec/changes/<change-id>/`.
- Each delta spec under `specs/<capability>/spec.md` within that change.
- The corresponding main `openspec/specs/<capability>/spec.md` files.
- Completed task state, resolved review state, and fresh verification output.

## Produces

- Main capability specs updated with accepted added, modified, removed, or
  renamed requirements while preserving unaffected requirements and scenarios.
- The completed directory moved to
  `openspec/changes/archive/yyyy-mm-dd-<change-id>/` without adding a second date
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
