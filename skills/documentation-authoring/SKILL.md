---
name: documentation-authoring
description: "Use when reader-facing documentation must be written or revised: one standalone document, or chunks of a planned documentation set with a plan under docs/writing. Applies the content-type skeletons, chunk frontmatter, didactic writing skills, glossary and placeholder conventions. Not for a wording fix inside existing text, for planning a multi-document set (use documentation-planning), or for software specifications."
---

# Documentation Authoring

Apply the shared [proportionality rule](../../shared/policies/proportionality.md)
before adding work, delegating, or repeating verification.

Write the text readers will use. In a documentation set, author chunks
according to the plan; for a standalone document, apply the same content-type
discipline without the set-level machinery.

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

In standalone mode the run is optional. When the project backlog does not track
the document under a stable work ID, record the verified-absent discovery
result in the reply, do not initialize a run, and treat the committed document
as the checkpoint. A documentation set always has a run.

## Trigger

Use when the [writing-depth policy](../../shared/policies/writing-depth.md)
places the work at the medium scale (one self-contained document), or when a
documentation plan exists and manifest rows are planned or returned with review
findings.

## Do not use for

- Changing a sentence, paragraph or section of existing text without new
  structure or shared terms; use a native focused edit.
- A documentation set without a plan; invoke `documentation-planning` first.
- Specifications, plans or architecture documents that belong to an
  engineering lifecycle.
- Set-wide consistency review; that is `documentation-review`.

## Consumes

- Standalone mode: the request, the defined reader, the subject and version
  to describe, any existing style guide or glossary.
- Set mode: `docs/writing/<doc-id>/plan.md`, `glossary.md`, `assets.md`, the
  manifest rows assigned to this session, and any open findings in
  `docs/writing/<doc-id>/review.md`.
- The current subject: interface, product, code or process the text describes,
  inspected directly rather than remembered.

## Produces

- One Markdown file per chunk under the content root named in the plan, or one
  standalone document at the requested path, each starting with the frontmatter
  of the installed [chunk template](../../templates/documentation/chunk.md).
- Manifest status updates in `plan.md`, new glossary entries through
  `terminology-guard`, and new asset rows through `visual-placeholders`.
- For a standalone document with more than a handful of recurring terms, a
  glossary section or definition list inside the document.

## Workflow

1. Read the plan or, in standalone mode, define the reader, the content type
   and the version described at the top of the document.
2. Take one chunk at a time in manifest order. Re-read its dependencies from
   disk before writing; do not write from memory of an earlier session.
3. Draft with the type skeleton from the chunk template and the matching
   skill: `explaining-concepts` for concept chunks and for the purpose
   paragraph of any other type; `writing-procedures` for task and tutorial
   chunks, with blocks of three to five steps and a validation section;
   `empathic-troubleshooting` for troubleshooting chunks; consistent tables
   for reference chunks. Before writing the first sentence, read
   [human-prose-drafting](../human-prose-drafting/SKILL.md) and apply its
   guidance while drafting: direct statements, concrete facts, natural
   rhythm and useful formatting. Preserve its exceptions for source fidelity,
   required structure and technical terms. These constraints apply while writing; a
   separate humanizing pass afterwards is not part of this lifecycle.
4. Keep one content type per chunk. When a procedure needs explanation, link
   the concept chunk; when a concept needs steps, link the task chunk.
5. Check facts against the subject: run or replay commands, open the interface,
   read the code. Record the version or revision in the frontmatter.
6. Run the [curse-of-knowledge filter](../../shared/writing/curse-of-knowledge-filter.md),
   the `human-prose-drafting` chunk check and the `terminology-guard`
   consistency check on the chunk; insert `visual-placeholders` callouts
   where an image confirms a state.
7. Mark the manifest row drafted, checkpoint, and continue with the next
   chunk. Stop at a section boundary when the plan calls for a section review.

Write in the documentation language recorded in the plan. Reader-facing text
follows the reader; repository artifacts such as the plan follow the project's
documented language.

## Completion

A chunk is complete when its frontmatter is filled, its body follows the type
skeleton, task blocks have three to five imperative steps and an observable
validation, every term passes the glossary check, the prose passes the
`human-prose-drafting` chunk check, every image has a registered placeholder,
cross-references resolve, and the described facts were checked against the
current subject. Standalone documents are complete when the same
holds for the single file and its links render.

## Next phase

`documentation-review`

For a standalone document, the review is a self-review against the review
template's checks recorded in the reply, followed by
`verification-before-completion`.

If the requested deliverable includes a PDF, invoke
[documentation-pdf](../documentation-pdf/SKILL.md) after the content review is
accepted and before final artifact verification. Export is optional for other
deliverables and does not introduce a new prose-editing phase.

## Supporting skills

- `project-backlog` for recovery, canonical task state, events, and checkpoints.
- `explaining-concepts`, `writing-procedures` and `empathic-troubleshooting`
  for the text of each content type.
- `human-prose-drafting` for the sentence-level constraints of every draft.
- `terminology-guard` and `visual-placeholders` for glossary and assets.
- `dispatching-parallel-agents` only for chunks with disjoint files, a stable
  glossary and no cross-dependency; the coordinator owns the manifest.
- `verification-before-completion` for fresh rendering and link checks.

## Escalation

If a standalone document reveals several readers, shared terminology with
other documents or a chapter structure others must mirror, stop extending it.
Record the finding, invoke `documentation-planning`, register the document as
the first manifest row, and continue in set mode. Preserve the written text
and its IDs.
