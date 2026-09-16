# Glossary: <documentation set name>

- Documentation ID: `<doc-id>`
- Artifact path: `docs/writing/<doc-id>/glossary.md`
- Rule: one term per concept, one concept per term. Add a term here before it
  appears in a chunk. Deprecated variants are listed so a check can find them.

```json
{
  "schema_version": 1,
  "doc_id": "<doc-id>",
  "language": "<documentation language>",
  "terms": [
    {
      "term": "<preferred term exactly as written in the text>",
      "definition": "<one or two sentences a reader of the least experienced reader ID understands>",
      "avoid": ["<synonym or spelling that must not appear>"],
      "first_use": "<chunk ID where the term is first introduced>",
      "ui_label": "<exact label in the interface if it differs>",
      "notes": "<capitalization, plural, translation notes>"
    }
  ]
}
```

| Term | Definition | Avoid | First use | UI label |
|---|---|---|---|---|
| <term> | <definition> | <variants> | C-001 | <label> |

Keep the table and the JSON block in agreement; the JSON block is the
machine-checkable list, the table is what readers and reviewers read.
