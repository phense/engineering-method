---
name: human-prose-drafting
description: "Use within documentation-authoring for medium and large texts to apply Humanizer prose guidance from the first sentence, with a brief per-chunk check. Not a separate rewrite phase or a reason to change facts, code, quotations or required document structure."
---

# Human Prose Drafting

Apply the shared [proportionality rule](../../shared/policies/proportionality.md)
before adding work, delegating, or repeating verification.

Write for the defined reader and subject from the first sentence. Apply the
patterns below while choosing words and organizing each paragraph. The writing
lifecycle includes a short check of each chunk, with no separate humanizing phase.

Adapted from blader/humanizer (MIT); patterns trace to Wikipedia's "Signs of AI
writing" maintained by WikiProject AI Cleanup. See the third-party notices.

## Trigger

Use inside `documentation-authoring` for every chunk or standalone document at
the medium or large scale, and inside `documentation-review` as one check.
The didactic skills decide what to say and in what order; this skill decides
how the sentences may not be built.

## Do not use for

- Code blocks, inline code, commands, paths, YAML frontmatter, data tables,
  link targets and quoted material: leave them unchanged.
- Changing claims. A name, number, date, quote, citation or fact comes from
  verified source material, never from this skill; when a sentence needs a
  missing detail, write a simpler sentence or record the gap.
- Small-scale edits inside existing text that keep the surrounding voice.

## Two rules while drafting

1. Give each sentence a purpose for the reader. Omit sentences that only
   signal importance, echo a heading or repeat a conclusion. Keep useful
   teaching recaps and required warnings.
2. Choose for the defined reader. Vary sentence length as speech does; name
   the actor; use the number of items the meaning has; pick the plain word.

## Constraints by strength

Use these patterns as contextual writing guidance, not a string blacklist.
The staged rhetoric in group A warrants attention on one occurrence. Weak
signals such as a dash or a three-item list need context before changing them.
User instructions, required templates, glossary terms, source fidelity and
project style take precedence over stylistic preferences here.

### A. State instead of staging

- **No "not X but Y".** Also not "not just X, it's Y", "X rather than Y" as a
  reveal, or the split form "This does not mean X. It means Y." State the
  point. Keep a contrast only when the negative half corrects a belief the
  reader actually holds.
- **No one-line closers or fragment rows.** No "That is the real win.", no
  sentence-long paragraph that restates the one before, no "No prior. No
  nostalgia." Merge fragments into one sentence with a specific claim.
- **No sayings dressed as depth.** Not "at its core", "the real question is",
  "what really matters", "X is the language of Y". Write the specific claim.
- **No run-up before the point.** Not "Let's dive in", "Here's what you need
  to know", "Honestly?", "Here's the thing". Begin with the point.
- **No arguing with no one.** Not "This isn't about", "To be clear", "A
  tempting approach would be", "You might think". Keep an objection only
  when the text attributes it or the reader would actually weigh it.

### B. Rhythm follows meaning

- **No forced triads.** Three items only when the meaning has three; three
  parallel examples plus a lesson is the same tell at paragraph scale.
- **No repeated sentence openings** in a row unless deliberate for rhythm.
- **Avoid dash chains.** Use periods, commas, colons or parentheses when they
  make the sentence easier to read. Keep meaningful ranges, names and dashes
  required by the project's style. *Weak alone.*
- **No stacked qualifiers.** "could potentially possibly" becomes "may". Keep
  scope statements, safety notices and honest uncertainty. *Weak alone.*
- **Hyphenate only where grammar needs it**: "a high-quality report", "the
  report is high quality". *Weak alone.*
- **Name the actor.** "You do not need a configuration file", not "No
  configuration file needed". Procedures already require this. *Weak alone.*

### C. Facts without inflation

- **Avoid the stock words**: actually, additionally, align with, bolstered,
  crucial, deep dive, delve, emphasizing, enduring, enhance, fostering,
  garner, highlight (verb), interplay, intricate, key (adjective), landscape
  (abstract), meticulous, pivotal, quietly, robust (figurative), showcase,
  tapestry, testament, underscore (verb), valuable, vibrant. Keep precise
  technical senses, glossary terms and interface names. This is a watch list,
  not a ban on words that accurately describe the subject.
- **No inflated significance.** Not "marks a pivotal moment", "plays a key
  role", "the future looks bright", and no closing send-off paragraph. End on
  the last concrete fact.
- **No vague association.** Not "associated with", "in connection with" when
  the subject shows the actual relationship; when it does not, keep the vague
  wording rather than inventing a role.
- **No shallow -ing riders**: "highlighting", "ensuring", "reflecting",
  "showcasing" bolted onto a fact. Keep the fact.
- **No sales language**: boasts, vibrant, rich (figurative), nestled,
  renowned, breathtaking, seamless, powerful. State what the thing is.
- **No borrowed authority.** Not "experts believe", not a list of outlets.
  Name the source and what it said, or leave the claim out.
- **Use is, are and has.** Not "serves as", "features", "boasts", "offers".

### D. Formatting carries information

- **Bold only for interface labels** as `writing-procedures` requires, and
  for the first words of a list item when the reader scans by them. No bold
  for emphasis, no list where every item is a bold label with a colon and a
  sentence that repeats the label.
- **Prefer sentence-case headings** and avoid decorative emojis, arrows and
  rules. Preserve required headings, anchors and template title structure.
- **Straight quotation marks** unless the project's style guide says
  otherwise. *Weak alone.*

### E. Nothing left over from the chat

- **No chatbot residue**: "Great question", "I hope this helps", "Let me
  know", "Would you like", "Here is a". Documentation stands on its own.
- **No knowledge-limit disclaimers or guesses.** Not "details are limited in
  available sources, it appears". State what the subject shows or leave it
  out; never present a guess as a fact.
- **No heading repeated in the first sentence.**
- **No writing about the previous version** except in release notes,
  changelogs and migration guides. Describe current behavior.

## Voice for documentation

Concept, task, reference and troubleshooting text stays neutral and plain,
addresses the reader as "you", and keeps the project's glossary terms. The
plan or project contract decides the language of the text; the tells above have
equivalents in every language and are treated the same. Do not add opinions,
humor or asides to documentation; those belong to personal writing.

## Chunk check

Before marking a chunk drafted, read it once for the five tells that most
often survive drafting: a not-X-but-Y contrast, a one-line closer, a dash, a
triad, a bold label. Assess each in context, including the exceptions below.
Correct unnecessary rhetoric within the chunk; retain useful structure. Confirm the fix dropped no fact, step, warning or
claim. This check is part of authoring the chunk and adds no separate
humanizing stage or extra output artifact.

## When not to act

Leave a watched phrase alone inside a quotation, a title, a product or
interface name, or a passage that discusses the phrase rather than uses it.
Keep scope statements, legal and safety notices, and real corrections. A
specific unusual detail, a stated limit or an honest "we do not know" is not a
tell; it is what a person would write.

## Completion

A chunk is complete when the contextual check finds no unresolved prose
problem and preserves facts, steps, uncertainty, warnings, glossary terms and
required structure. Record the check in the existing self-review or review
report; update `last_reviewed` only when the full chunk review is complete.
A literal word match alone is not a failure.
