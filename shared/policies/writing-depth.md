# Writing Depth

Prose deliverables follow the same rule as code: match the workflow to the
observable size, audience risk and lifetime of the text. Decide the scale first,
record it, and select the writing lifecycle from that decision. Do not adopt
documentation-set machinery for a paragraph, and do not write a manual one
chapter at a time without a plan.

Apply [proportionality](proportionality.md) at every scale. Depth describes the
evidence and structure a reader needs, not an unlimited writing budget.

## Scale decision

Estimate from the request and existing material, then confirm by inspecting the
target repository or document tree read-only. Record the chosen scale and its
evidence in the owning artifact or, for small work, in the reply.

| Observable conditions (any one moves the work to that scale) | Scale | Writing lifecycle |
|---|---|---|
| One sentence, paragraph, or section inside an existing text; wording, correctness or a single explanation; no new document structure; no new terms that other pages must share | Small | Native focused edit; the reader-oriented rules apply inline |
| One self-contained document: a README section set, guide, tutorial, article, report, release note or reference page; one primary audience; expected length up to roughly 3,000 words or 40 procedure steps; no shared glossary or asset plan needed beyond the document | Medium | `documentation-authoring` in standalone mode, with the didactic and structural supporting skills its content type requires |
| Several chapters or documents that must agree on terms, structure and images; more than one audience or reading path; a manual, handbook, course, knowledge base or product documentation set; expected length above roughly 3,000 words, more than five chapters, or contributors and reviews spread over multiple sessions | Large | `documentation-planning` → `documentation-authoring` (per chunk) → `documentation-review` → `verification-before-completion` |

The word and chapter figures are thresholds for the decision, not targets. When
two conditions disagree, the higher scale wins if the text must stay consistent
over its lifetime; the lower scale wins if the request is reversible and local.
When existing writing artifacts exist under `docs/writing/<doc-id>/`, continue
that recorded scale and phase instead of deciding again.

## Required depth per scale

| Scale | Required depth |
|---|---|
| Small | Reader-oriented wording, terminology consistent with the surrounding text, focused check of the changed passage and its links; preserve the surrounding voice without loading an additional supporting skill |
| Medium | Content type chosen from the information architecture, one template-based document with frontmatter, explicit reader, prerequisites and validation for procedures, local glossary check, drafting under the `human-prose-drafting` constraints, self-review against the didactic rules, fresh link and rendering check |
| Large | Documentation plan with audience, architecture map, chunk manifest and conventions; shared glossary; asset manifest with placeholders; per-chunk authoring under the `human-prose-drafting` constraints with checkpoints; set-wide consistency review including prose tells; convergence of findings; fresh verification |

## Escalation between scales

If a medium document reveals shared terminology, several audiences or a chapter
structure that other documents must mirror, stop extending it. Create the
documentation plan through `documentation-planning`, register the existing
document as its first chunk, and continue at the large scale. Preserve the
written text and its stable identifiers. Never grow a standalone document into
an unplanned manual.

If a large plan turns out to cover one document, reduce it to standalone mode
explicitly in the plan, keep the glossary if other text uses it, and record the
reason. The scale decision is a checkpoint fact, not a silent assumption.
