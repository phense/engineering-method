---
name: empathic-troubleshooting
description: "Use when writing help for something that has gone wrong or may go wrong, in documentation or an ordinary reply: start from what the reader sees, name likely causes in order, give the first check, then the fix and its confirmation. Not for diagnosing a defect in code you own (use systematic-debugging), for normal procedures, or for reference lists of error codes."
---

# Empathic Troubleshooting

Apply the shared [proportionality rule](../../shared/policies/proportionality.md)
before adding work, delegating, or repeating verification.

The reader arrives with a symptom, not an error code, and often under time
pressure. Troubleshooting text meets them at the symptom, tells them the most
likely reason in plain words, and leads them through the cheapest check first.

## Trigger

Use for troubleshooting chunks, "if this does not work" paragraphs after a
procedure, FAQ entries about failures, support macros, and replies where the
user reports that something is not working for them.

## Do not use for

- Finding the root cause of a defect in a system you can inspect; that is
  `systematic-debugging`. This skill writes the reader-facing help once causes
  are known.
- Ordinary procedures where nothing has failed; use `writing-procedures`.
- Machine-readable error catalogs. A code table may exist as reference, but
  the troubleshooting text is organized by what the reader experiences.

## Entry pattern

Each troubleshooting entry follows this order:

1. **What you see.** The symptom in the reader's words and observable terms:
   "The screen stays black after you sign in", not "Authentication callback
   fails." Include the exact message text if the reader will see one.
2. **What it usually means.** The most common cause first, stated plainly,
   with a reassuring frame where honest: how common it is, whether data is
   at risk.
3. **Check this first.** The cheapest and most likely check, as one to three
   imperative steps with the result that tells the reader which cause applies.
4. **Fix.** Steps for each confirmed cause, using the `writing-procedures`
   rules. Order causes by probability and then by cost to check.
5. **Confirm it is resolved.** The observable result that shows the problem
   is gone.
6. **If it is still not working.** Where to get help and exactly what to
   include: version, the message, what was already tried.

## Tone rules

- Address the reader directly and never assign blame: "the password was
  entered differently" rather than "you typed it wrong".
- State uncertainty honestly and usefully: "most often", "in rare cases",
  never "should work".
- Use the glossary term and the exact interface label; the reader will search
  for what they see.
- Keep the whole entry scannable: a reader in trouble reads headings and the
  first line of each section.
- Do not hide the fix behind an explanation. A one-sentence cause is enough;
  link to a concept chunk for the rest.

## Organizing many entries

Group entries by the situation the reader is in, such as "signing in",
"during installation", "after an update", and order them by frequency. Give
each entry a stable ID and a symptom-based title. Apply the
[curse-of-knowledge filter](../../shared/writing/curse-of-knowledge-filter.md)
to each check and fix: the expert's mental shortcut is exactly what the
troubled reader lacks.

## Completion

An entry is complete when it opens with the reader's symptom, orders causes by
likelihood and cost, gives a first check with a decisive result, provides a
fix and a confirmation for each cause, and tells the reader how to escalate
with the right information. Where a cause was established by
`systematic-debugging`, link that evidence in the chunk metadata rather than
repeating internals in the reader's text.

## Common mistakes

- Titling entries by internal cause or error code instead of the symptom.
- Listing every possible cause with equal weight.
- Explaining the architecture before offering the first check.
- Ending with the fix and never telling the reader how to confirm it.
- Phrases that imply the reader is at fault or that the problem is trivial.
