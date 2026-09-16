---
name: writing-procedures
description: "Use when a reader must perform actions: installation, configuration, operation, or any how-to steps in documentation or an ordinary reply. Produces numbered imperative steps, one action each, exact locations named, three to five steps per block, and a check that it worked. Not for conceptual explanation, reference tables, or diagnosing a failure."
---

# Writing Procedures

Apply the shared [proportionality rule](../../shared/policies/proportionality.md)
before adding work, delegating, or repeating verification.

Write for the reader's hands. A procedure tells one defined reader exactly what
to do, where, in what order, and how to see that it worked. Passive descriptions
of where something happens are not instructions.

## Trigger

Use for task and tutorial chunks, README installation and usage sections,
runbooks, handoff notes that ask someone to act, and replies that tell the
user what to do next. The [reader-oriented output
policy](../../shared/policies/reader-oriented-output.md) applies it to
ordinary replies.

## Do not use for

- Explaining why something works; use `explaining-concepts` before or beside
  the procedure, not inside it.
- Symptom-first help when something has gone wrong; use
  `empathic-troubleshooting`.
- Reference tables of options, fields or commands; link to them from a step.

## Chapter pattern

Every task chunk and every procedure section uses these four parts in this
order. In a short reply the headings may be implied, but the parts remain.

1. **Goal.** One sentence: what the reader will have achieved.
2. **Before you start.** Prerequisites the reader can verify: access, installed
   software with versions, state of the system, data they need, expected time.
3. **Steps.** Blocks of three to five numbered steps. Each block has a short
   heading naming its sub-goal and ends with what the reader now sees. Split a
   longer sequence into more blocks; never let a block grow past five steps.
4. **Check that it worked.** The observable result that proves success, and
   the first thing to do if it is absent, with a link to the matching
   troubleshooting chunk when one exists.

## Step rules

- Imperative mood, reader as the actor: "Select **Save**", not "The settings
  are saved here" and not "You can now save".
- One action per step. A condition or a location may accompany it: "In the
  top-right corner, select the gear icon."
- Name locations and labels exactly as the reader sees them, in the reader's
  interface language, in bold for interface labels and in code for commands,
  paths and values.
- Put the purpose before the action when it helps the reader decide: "To keep
  the old key, select **Skip**."
- Write out the step an expert would skip. Apply the
  [curse-of-knowledge filter](../../shared/writing/curse-of-knowledge-filter.md)
  for skipped steps, unlocated objects and assumed state.
- Put warnings before the step they concern, not after it.
- Give the full path first; keyboard shortcuts and aliases are optional
  extras in parentheses.
- Use the glossary term for every object; do not vary wording for style.
- Show the exact command or value in a fenced block when the reader must type
  it; do not paraphrase it in prose.

## Result statements

After each block, state what the reader now sees: a dialog, a status, an
output line, a file. Where the result can vary, name the acceptable range.
Use a `visual-placeholders` callout when a screenshot would confirm the state
faster than words.

## Completion

A procedure is complete when the four parts are present, every block has three
to five imperative single-action steps, every location and label is exact,
prerequisites are verifiable, and the validation names an observable result.
Where possible, run or replay the procedure against the current system and
record the revision or version it was checked against.

## Common mistakes

- Numbering explanations, options or warnings as if they were steps.
- Describing the interface instead of instructing the reader.
- Hiding two or three actions in one step joined by "and".
- Ending a block without telling the reader what they should now see.
- Leaving "simply", "just" or "obviously" in the text; they signal a skipped
  step.
