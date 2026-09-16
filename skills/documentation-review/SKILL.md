---
name: documentation-review
description: "Use when drafted chunks of a documentation set under docs/writing must be checked for set-wide consistency before acceptance: frontmatter against the manifest, one content type per chunk, step-block and validation rules, terminology, curse-of-knowledge gaps, placeholders and cross-references. Not for code review, for reviewing a single standalone document, or for writing corrections."
---

# Documentation Review

Apply the shared [proportionality rule](../../shared/policies/proportionality.md)
before adding work, delegating, or repeating verification.

Read the set as its least experienced reader and as its glossary owner. Record
findings with evidence, and return actionable findings to the author with the
text they must change, not with a verdict alone.

## Recovery preamble

Before creating or updating an artifact:

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

Use when all manifest rows of a section, or of the whole set, are drafted, and
before any chunk is marked accepted. Also use after a glossary or interface
change that affects already drafted chunks.

## Do not use for

- Code or engineering artifacts; use `requesting-code-review`.
- A standalone document; `documentation-authoring` performs a recorded
  self-review with the same checks.
- Making the corrections; findings return to `documentation-authoring`.

## Consumes

- `docs/writing/<doc-id>/plan.md`, `glossary.md`, `assets.md`.
- Every chunk file in the review scope at a named revision.
- Prior `docs/writing/<doc-id>/review.md` findings and their dispositions.

## Produces

- `docs/writing/<doc-id>/review.md` from the installed
  [review template](../../templates/documentation/review.md), with the reviewed
  revision, each check's method and result, findings with stable IDs, chunk,
  severity, quoted evidence and required change, and a verdict.
- Manifest status updates: reviewed for chunks without open Critical or
  Important findings, otherwise unchanged with the finding IDs noted.

## Checks

Run every row of the review template against the actual files, using search
on the text rather than recollection:

1. Frontmatter fields present and consistent with the manifest row.
2. One content type per chunk; headings match the type skeleton.
3. Task and tutorial chunks: goal, prerequisites, step blocks of three to
   five imperative single-action steps, an observable result per block, a
   validation section.
4. Terminology through the `terminology-guard` consistency check across the
   whole scope, not chunk by chunk in isolation.
5. Curse-of-knowledge sample: read at least one chunk per type as the defined
   least experienced reader and record skipped steps, unlocated objects,
   unshared terms and assumed state.
6. Placeholders: every callout registered in the asset manifest with capture
   instructions; every manifest row referenced from a chunk.
7. Cross-references: every relative link and chunk ID resolves; no "see above".
8. Troubleshooting chunks: symptom first, causes ordered, first check, fix,
   confirmation, escalation.
9. Read [human-prose-drafting](../human-prose-drafting/SKILL.md) and assess
   passages for staged contrasts, empty closers, dash chains, inflated wording
   and chatbot residue. Apply its context and preservation exceptions; a
   word match alone is not a finding. Return specific prose findings to the
   author within the existing review cycle; add no separate rewrite phase.

Independence: a set-wide acceptance review is performed by a reviewer who did
not draft the reviewed chunks when the host can provide one; otherwise record
that the review was a coordinator self-review and its limits.

## Completion

The review is complete when every check has a recorded method and result at
the named revision, every finding has evidence and a required change, and the
verdict states the count of open Critical and Important findings. Acceptance
of the scope requires zero open Critical or Important findings.

## Next phase

`verification-before-completion` when the verdict is Ready. Otherwise return
the findings to `documentation-authoring` as new work for the affected chunks;
that return preserves accepted chunks and stable IDs and is not a new plan.

If the requested deliverable includes a PDF, invoke
[documentation-pdf](../documentation-pdf/SKILL.md) after the content review is
accepted and before final artifact verification. Export is optional for other
deliverables and does not introduce a new prose-editing phase.

## Supporting skills

- `project-backlog` for recovery, canonical task state, events, and checkpoints.
- `terminology-guard` for the set-wide term check.
- `human-prose-drafting` for the prose-tell check.
- `receiving-code-review` for evaluating disputed findings against the text.
- `verification-before-completion` for the final fresh check.

## Common mistakes

- Reviewing chunk by chunk and never reading a reader's whole path.
- Reporting "inconsistent terminology" without the term, the chunk and the
  replacement.
- Accepting a set with placeholders that no one could capture from the
  instructions.
- Treating a rendered page without errors as proof that the reader can succeed.
