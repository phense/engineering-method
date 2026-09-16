---
name: explaining-concepts
description: "Use when a technical concept, mechanism, or design must be explained to a reader who lacks the writer's expertise, in documentation or an ordinary reply. Introduces each concept with an everyday analogy before the mechanism and removes undefined jargon. Not for step-by-step instructions, reference tables, or error diagnosis."
---

# Explaining Concepts

Apply the shared [proportionality rule](../../shared/policies/proportionality.md)
before adding work, delegating, or repeating verification.

Explain so that the defined reader could restate the idea in their own words.
This is the Feynman technique applied to writing: if the explanation needs
jargon to stand up, the writer has not understood it well enough yet.

## Trigger

Use for concept sections in documentation, the "why" paragraph before a
procedure, architecture or design explanations for non-specialists, onboarding
material, and any reply where the reader asked how or why something works.
The [reader-oriented output policy](../../shared/policies/reader-oriented-output.md)
applies this skill to ordinary replies as well as to documents.

## Do not use for

- Procedures and instructions; use `writing-procedures`.
- Symptom-driven help for something that is failing; use `empathic-troubleshooting`.
- Reference material whose value is exactness and completeness, not
  understanding. Reference text may link to a concept chunk instead.
- Readers who demonstrably share the vocabulary and asked for the short
  expert version.

## Explanation pattern

Write each concept in this order. Keep the sections short; a concept chunk is
usually under 600 words.

1. **One sentence of purpose.** What the concept does for the reader, in the
   reader's terms.
2. **Everyday analogy.** One concrete image from ordinary life that shares the
   concept's structure. Choose it for structural fit, not for charm. State in
   one sentence where the analogy stops being true.
3. **Mechanism.** How it actually works, in the same order the reader would
   observe it. Use only glossary terms and terms defined in the previous
   sentences. Prefer a small concrete example over a general statement.
4. **Consequence.** What changes for the reader because this is how it works:
   what they can rely on, what they must avoid, what to do next.
5. **Related terms.** Link the glossary terms and the neighboring concept,
   task or reference chunks.

## Jargon rule

Every term in the explanation is one of: a word the defined reader already
uses in this sense, a glossary term introduced before this point, or a term
defined in the sentence where it first appears. Anything else is rewritten or
removed. Abbreviations are expanded at first use. Do not introduce a second
name for something already named.

Run the [curse-of-knowledge filter](../../shared/writing/curse-of-knowledge-filter.md)
after drafting: the expert's skipped intermediate idea is the most common gap.

## Self-check

Before handing over, answer with evidence from the text:

- Could the reader restate the idea without the analogy? If the analogy is the
  only explanation, the mechanism section is missing.
- Does any sentence carry more than one new idea? Split it.
- Is the analogy's limit stated? An unbounded analogy misleads later.
- Would the mechanism paragraph still be true for an expert? Simplification
  must not become falsehood; mark deliberate omissions with "for now" or a
  link to the reference.

## Completion

The explanation is complete when the pattern is present, every term passes the
jargon rule, the analogy's limit is stated, and the text was read once as the
defined reader. In a documentation set, record `last_reviewed` in the chunk
frontmatter only after `documentation-review` confirms it.

## Common mistakes

- Starting with history, internals or a definition instead of the reader's
  purpose.
- Stacking several analogies; one that fits beats three that half fit.
- Using the analogy in the procedure that follows; procedures use the exact
  interface terms.
- Explaining what the writer finds interesting rather than what the reader
  needs for their next action.
