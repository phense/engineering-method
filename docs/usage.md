# Usage examples

Start the host in the project you want to change. Describe the outcome and
constraints; the host uses skill descriptions and current artifacts to choose
the workflow. The following are example requests, not guaranteed transcripts.

## Make a small edit

> Fix the broken installation link in README.md and verify the affected links.

A reversible documentation edit uses a focused edit and verification. It should
not create a specification, architecture diagrams or a delegation cycle.

## Repair a reproducible failure

> The checkout test fails when payment succeeds but inventory reservation fails.
> Reproduce it, find the cause and fix it without changing the API contract.

`systematic-debugging` establishes the cause; a meaningful regression test
supports the fix. Review and fresh verification apply according to risk. An
unverified review allegation enters `receiving-code-review` first.

## Change an existing capability

> Add a configurable timeout to this existing export command. Keep its output
> format and the other commands unchanged.

A bounded Brownfield change uses OpenSpec: `openspec-propose` records the delta
requirements, design and tasks under `docs/openspec/changes/<change>/`;
`openspec-apply` implements an approved complete change; `openspec-archive`
synchronizes and archives its verified requirements. If inspection exposes a
new system boundary or risky migration, record the escalation before handing
over to Spec Kit. Do not silently grow the original proposal.

## Build a large feature

> Add a checkout flow spanning inventory, payment and order persistence, with
> recovery after partial failure. Inspect the existing system before specifying it.

Spec Kit proceeds through `speckit-specify`, `speckit-plan`, the architecture
gate, `speckit-tasks`, `orchestrated-implementation` and `speckit-converge`.
Specification artifacts live under `docs/specs/<feature>/`. Relevant diagrams and
findings live under `docs/uml/` in the target project. Each diagram answers a
named question; diagram count is not an acceptance criterion.

Design findings become tasks. After implementation, reconcile diagrams with
code, derive success and relevant failure/recovery integration checks, and
resolve review findings before convergence. The shared policies favor cohesive
slices and reuse unchanged evidence. Additional expensive runs or reviews need
a concrete unresolved question and must respect user effort limits.

## Include playbooks in engineering work

> Build a new import service. Operators must recover interrupted imports and
> restore backups before launch. The rollout also includes a staged cutover.

`speckit-specify` records recovery playbooks as system deliverables even before
an incident has occurred. `speckit-plan` separately assesses the cutover's
need for a development playbook. The plan names owners, paths, dependencies and
required validation. The existing executor invokes `playbook-authoring` and
`playbook-review`; it arranges authorized rehearsal at the agreed level.
The cutover waits for its playbook readiness, and delivery waits for the required
system playbooks. OpenSpec applies the same decisions to a bounded change.

> Review the cutover playbook. It claims validation on its creation date, but
> has no rehearsal evidence and retries a non-idempotent import after a timeout.

`playbook-review` reports the missing proof and unsafe retry assumptions without
executing the procedure. It records content-review and rehearsal status
separately. Corrections return to the owning executor; convergence and archival
remain blocked while required evidence is missing or stale.

A direct request to author a scenario-bound onboarding or recovery playbook
uses `playbook-authoring`; a general tutorial or manual keeps its documentation
route. A typo fix or simple reversible refactor does not require a playbook.

## Write one document

> Write a how-to guide that shows an administrator how to rotate an API key.
> One reader group; no other documentation exists yet.

The writing-depth policy places this at the medium scale. `documentation-authoring`
runs in standalone mode: it defines the reader and version, uses the task
skeleton from the chunk template, and applies `writing-procedures` (goal,
prerequisites, blocks of three to five imperative steps, a check that it
worked). The draft is written under `human-prose-drafting` from the first
sentence, so no humanizing pass follows. A recorded self-review and fresh link
check close the work. No plan directory is created.

## Build a documentation set

> Create the complete user manual: about twelve chapters for administrators,
> end users and support staff, with shared terminology and screenshots.

Several readers, shared terms and images and many sessions place this at the
large scale. `documentation-planning` records the scale decision and writes
`docs/writing/<doc-id>/plan.md` with readers, information architecture and a
chunk manifest, plus `glossary.md` and `assets.md`. `documentation-authoring`
then writes one Markdown file per chunk with frontmatter, using
`explaining-concepts`, `writing-procedures` and `empathic-troubleshooting`
per content type, `human-prose-drafting` for sentence-level constraints while
writing, `terminology-guard` for terms and `visual-placeholders` for image
callouts. `documentation-review` checks the set at a named revision
and returns findings to authoring; acceptance needs zero open Critical or
Important findings and fresh verification.

## Explain, instruct or troubleshoot in a reply

> Why does the retry queue drop messages after a restart, and what should I
> check first?

Outside documentation projects, the reader-oriented output policy applies the
same skills to ordinary replies: the explanation opens with an everyday
analogy and avoids undefined jargon, the next steps are numbered imperative
actions with exact locations and a visible result, and help with a failure
starts from the symptom the user sees. Evidence and verification rules do not
change.

## Resume work

> Resume work item APP-014 from its repository checkpoint. Reconcile Git,
> artifacts, task status and current agents before continuing.

Stateful workflows save `.engineering-method/runs/APP-014/` with `state.json`,
`resume.md`, decisions, reports and events. Checkpoints must actually be written;
a compact or a new session cannot recover unsaved work. Repository evidence
wins over remembered state. agentic-rag may recall a work ID and artifact links,
but is optional and never the canonical state writer.

## Maintain task state

> Update APP-014 in the local backlog and record its verified capability in
> FEATURES.md. Do not migrate or create GitHub Issues.

`project-backlog` preserves stable IDs, blocker-first ordering and dependencies.
`FEATURES.md` describes working capabilities, not proposed work. With separate
permission, GitHub migration maps hierarchy to Sub-Issues and dependencies to
native dependency edges. After migration, Issues become canonical and the local
backlog is a marked cache; offline changes queue for reconciliation. Publishing
a repository alone does not authorize migrating its tasks.

## Export reviewed Markdown to PDF

> Build one PDF from these accepted chapters, in plan order, with the manual
> design, table of contents and page numbers.

`documentation-pdf` uses Quarto and its bundled Typst engine after content
review. Copy the [manual template](../templates/documentation/pdf/DESIGN.md)
to a new documentation root, map the accepted manifest rows to `book.chapters`
in `_quarto.yml`, and set title, language, output name and `_brand.yml`.
From that directory, run `quarto render --to em-manual-typst`. The default
result is `_book/manual.pdf`. Inspect the actual contents links, page totals
and page layout before delivery. This export preserves Markdown sources and
does not publish remotely or re-run Humanizer over the finished text.
