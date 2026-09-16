---
name: terminology-guard
description: "Use as a supporting skill when a document or documentation set must use one term per concept: create or extend the glossary before new terms appear, check drafts for banned variants and undefined terms, and align wording with interface labels. Not for choosing content structure, writing the text itself, or code identifiers."
---

# Terminology Guard

Apply the shared [proportionality rule](../../shared/policies/proportionality.md)
before adding work, delegating, or repeating verification.

Over hundreds of pages, readers lose trust when the same thing has three names.
The glossary is the single authority for terms; text follows it, and checks
are run against it rather than against memory.

## Trigger

Use when a documentation plan is created, before a chunk introduces a new
term, during set-wide review, and when an interface label, product name or
translation changes. In standalone documents, keep a local glossary section or
an inline definition list when more than a handful of terms recur.

## Do not use for

- Deciding chunk types or structure; that is `documentation-planning`.
- Writing the explanatory or procedural text; the didactic skills do that
  using the terms this skill fixes.
- Code identifiers, API names and command syntax, which stay exactly as
  implemented and are quoted in code formatting.

## Glossary authority

The glossary lives at `docs/writing/<doc-id>/glossary.md` from the installed
[glossary template](../../templates/documentation/glossary.md). It contains a
machine-checkable JSON list and a readable table that must agree. Each entry
has the preferred term, a reader-level definition, the variants to avoid, the
chunk of first use and, when different, the exact interface label.

Rules:

- One term per concept and one concept per term. Introduce a synonym only as
  an `avoid` entry that points to the preferred term.
- Add the term before the chunk that uses it is drafted. A term found in a
  draft but not in the glossary is a finding, not a style choice.
- Interface labels are quoted exactly as the reader sees them, in the reader's
  interface language, even when the glossary term differs; record both.
- Capitalization, plural and hyphenation are fixed per entry and followed
  everywhere, including headings and captions.
- Deprecated terms remain listed with their replacement so old text can be
  found and corrected.

## Consistency check

Run before a chunk is marked drafted and during `documentation-review`:

1. Search the text for every `avoid` variant in the glossary; each hit is a
   finding with the chunk, line and replacement.
2. List capitalized nouns, abbreviations and product names in the text that
   are not glossary terms and not code; classify each as define, add to
   glossary, or replace.
3. Confirm every abbreviation is expanded at first use in the chunk or linked
   to its glossary entry.
4. Confirm interface labels in steps match the recorded `ui_label`.
5. Record the check in the chunk's `last_reviewed` field or the review report
   with the glossary revision used.

Use exact search on the actual files; do not rely on recollection of what a
chunk says. When a prose linter that reads term lists is available, generate
its lists from the glossary JSON rather than maintaining a second list by
hand: preferred terms with fixed casing become the accepted list, `avoid`
variants become the rejected list or a substitution rule mapping each variant
to its preferred term. The glossary remains the source; generated lists are
derived artifacts.

## Completion

The guard is satisfied for a scope when the glossary contains every recurring
term with a definition and avoid-list, no avoid variant appears in the scope,
no undefined abbreviation or unlisted term remains, interface labels match,
and the check is recorded with the revision it ran against.

## Common mistakes

- Treating the glossary as an appendix written last instead of a contract
  written first.
- Allowing "the app", "the application" and the product name to alternate for
  variety.
- Translating interface labels that the reader sees untranslated.
- Fixing a term in one chunk and not searching the rest of the set.
