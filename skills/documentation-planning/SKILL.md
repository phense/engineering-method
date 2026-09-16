---
name: documentation-planning
description: "Use when a documentation set is requested or discovered: a manual, handbook, course, knowledge base, or several documents that must share terms, structure, readers and images. Decides the writing scale, then produces the documentation plan, chunk manifest, glossary and asset manifest. Not for one standalone document (use documentation-authoring), a wording fix, or software specification."
---

# Documentation Planning

Apply the shared [proportionality rule](../../shared/policies/proportionality.md)
before adding work, delegating, or repeating verification.

Decide how large the writing project is before writing, record that decision,
and give the authors one plan they can follow chunk by chunk across many
sessions without losing consistency.

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

Use when the [writing-depth policy](../../shared/policies/writing-depth.md)
places the work at the large scale: several chapters or documents, more than
one reader group or reading path, shared terminology and images, or authoring
spread over several sessions or contributors. Also use when a standalone
document escalates to a set.

## Do not use for

- One self-contained document with one reader group; use
  `documentation-authoring` in standalone mode.
- A sentence, paragraph or section fix; use a native focused edit with the
  reader-oriented rules.
- Specifying, planning or documenting software behavior for engineers; that is
  the Spec Kit or OpenSpec lifecycle. This skill plans reader-facing text.
- Producing chapter text; that is `documentation-authoring`.

## Consumes

- The request: subject, readers, purpose, delivery format, language, deadline
  and constraints.
- Existing material: current documents, interface, product or code the text
  describes, style guides, glossaries, brand or legal requirements.
- Any existing `docs/writing/<doc-id>/` artifacts for the same stable
  documentation ID.

## Produces

Create one kebab-case `<doc-id>` directory containing:

- `docs/writing/<doc-id>/plan.md` from the installed
  [plan template](../../templates/documentation/plan.md): scale decision with
  evidence, readers, information architecture, chunk manifest, conventions,
  acceptance criteria and out-of-scope list.
- `docs/writing/<doc-id>/glossary.md` from the
  [glossary template](../../templates/documentation/glossary.md), seeded with
  every term the manifest titles and reader goals already use.
- `docs/writing/<doc-id>/assets.md` from the
  [asset manifest template](../../templates/documentation/assets.md), listing
  the images the plan already knows it needs.

The plan names the content root where chunk files will live; this skill does
not create the chunk files.

## Workflow

1. Resolve one stable documentation ID. If it exists, continue the recorded
   plan and phase rather than planning again.
2. Inspect the subject read-only: the interface, product version, code paths,
   existing documents and any glossary. Record what the text will describe
   and which version.
3. Decide the scale with the writing-depth table and record the evidence. If
   the evidence shows one document, hand over to `documentation-authoring` in
   standalone mode and stop.
4. Define the readers. Name the least experienced reader expected to succeed
   and what each reader wants to achieve. Reader goals drive the manifest.
5. Build the information architecture. Assign each planned chunk exactly one
   content type: concept, task, tutorial, reference or troubleshooting. Types
   classify chunks; they are not the navigation. Arrange sections by reader
   journey and keep each level internally consistent.
6. Write the chunk manifest. One row per Markdown file, stable IDs, type,
   readers, dependencies, assets and status. Each chunk must make sense on its
   own; chunks link to each other rather than repeating content.
7. Fix conventions: frontmatter fields, file naming, heading levels, step
   block rules, placeholder syntax, cross-reference style, documentation
   language. Invoke `terminology-guard` to seed the glossary and
   `visual-placeholders` to record known assets.
8. Define acceptance: which reader goals must have a complete path, which
   findings block acceptance, when set-wide review runs.
9. Verify the artifacts against the completion condition and hand over.

## Modular chunking

Large sets are written as one file per chunk, never as one growing document.
Each chunk carries the frontmatter from the
[chunk template](../../templates/documentation/chunk.md), so that any chunk can
be authored, reviewed, reordered, translated or regenerated independently,
and so that a new session can resume from the manifest without rereading the
whole set. Order lives in the manifest and in navigation files, not in file
names or IDs.

## Completion

The plan is ready when the scale decision and its evidence are recorded, every
reader has a goal and a path through the manifest, every manifest row has one
type and stable ID, conventions are complete enough that two authors would
produce interchangeable chunks, the glossary and asset manifest exist, and
acceptance criteria are observable.

## Next phase

`documentation-authoring`

## Supporting skills

- `project-backlog` for recovery, canonical task state, events, and checkpoints.
- `terminology-guard` for seeding and owning the glossary.
- `visual-placeholders` for the asset manifest conventions.
- `verification-before-completion` for fresh artifact checks.

## Planning boundary

This phase writes plan, glossary and manifest artifacts only. It must not
draft chapter text. After verifying the artifacts, return control to the
coordinator. When the original request authorizes end-to-end writing, the
coordinator continues with `documentation-authoring` without a new request
unless a material decision, blocker, or authority boundary requires user input.
