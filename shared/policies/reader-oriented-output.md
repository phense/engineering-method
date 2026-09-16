# Reader-Oriented Output

The didactic writing skills are not limited to documentation projects. They
govern how any explanation, instruction or troubleshooting help is written for
a reader who lacks the writer's context, including ordinary replies, commit
and pull-request descriptions, review comments, handoff notes and error
reports. Apply them by default; skip them only when the reader has explicitly
asked for terse expert output or the text is machine-consumed.

## Which rules apply to which reply

| The reply is mainly | Apply | Not |
|---|---|---|
| Explaining why or how something works to someone who does not already know it | `explaining-concepts`: an everyday analogy before the mechanism, no undefined jargon, one idea per sentence, the analogy's limits stated | A textbook-length detour; an analogy for a term the reader already uses correctly |
| Telling the reader what to do next: install, configure, run, click, review | `writing-procedures`: numbered imperative steps, one action each, exact locations named, three to five steps per block, a visible result to confirm success | Passive descriptions of where something happens; a wall of twelve unnumbered steps |
| Helping with something that went wrong or might go wrong | `empathic-troubleshooting`: start from what the reader sees, name the likely cause, give the first check, then the fix, in order of probability and cost | A table of error codes without the reader's symptom; blame or hedging language |
| A pass, fix, or completion claim | `verification-before-completion` | Reader-oriented tone replacing evidence |

The curse-of-knowledge filter in
[shared/writing/curse-of-knowledge-filter.md](../writing/curse-of-knowledge-filter.md)
applies to all three: write out the step the expert would skip, name the place
where the reader has to look, and define or avoid every term the reader might
not share.

## Boundaries

- These rules shape wording and order. They never replace the evidence a claim
  needs, remove required detail, or add filler. A shorter, exact reply is still
  the goal.
- Terminology follows the project's glossary when one exists. In a project
  without a glossary, keep one term per concept within the reply and reuse the
  term the reader used.
- The reader's language decides the reply language; repository artifacts stay
  in the project's documented language.
- Host adapters may point to this policy; they do not add host syntax to it.
