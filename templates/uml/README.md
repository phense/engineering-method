# UML Templates

Use a template only after naming a design or verification question. Copy the
smallest useful source to the feature's `docs/uml/` directory, replace its
example participants with evidence-backed system facts, and delete irrelevant
examples. A feature is not expected to use every template.

## Selection

| Template | Use only when the question concerns |
|---|---|
| `component.mmd` | ownership, dependencies, interfaces, or trust boundaries |
| `sequence.mmd` | ordered end-to-end, failure, rollback, or concurrent messages |
| `state.mmd` | valid, invalid, unreachable, terminal, or recovery states |
| `activity.mmd` | branching, parallel work, or migration workflow |
| `deployment.mmd` | runtime topology, processes, stores, zones, or network trust |

Place the five metadata comments from `diagram-metadata.md` at the start of
every Mermaid file. A source-evidence entry names repository-relative paths and
stable requirement IDs; it is not a conversational assertion.

## Verification

Prefer a current Mermaid renderer when one is already available. Otherwise
review the text source for the correct diagram directive, unique identifiers,
valid relationships, paired blocks, and quoted labels. Record the method and
date without claiming a rendered result.
