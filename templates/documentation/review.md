# Documentation Review: <documentation set name>

## Stable work ID

- Documentation ID: `<doc-id>`
- Plan: `docs/writing/<doc-id>/plan.md`
- Artifact path: `docs/writing/<doc-id>/review.md`
- Reviewed revision: `<full commit>`
- Scope: <section IDs or whole set>

## Checks

| Check | Method | Result |
|---|---|---|
| Frontmatter complete and matches the manifest | Read every chunk header against the manifest | pass / findings |
| One content type per chunk | Read headings against the type skeleton | pass / findings |
| Task chunks: goal, prerequisites, step blocks of three to five, validation | Count steps per block; confirm each block ends with a result | pass / findings |
| Terminology | Search for every `avoid` variant and undefined capitalized terms | pass / findings |
| Curse-of-knowledge filter | Sample read as the least experienced reader; locations, skipped steps, assumed state | pass / findings |
| Placeholders and assets | Every callout has a manifest row and capture instructions | pass / findings |
| Cross-references | Every relative link resolves; no dangling chunk IDs | pass / findings |
| Troubleshooting chunks | Symptom first, causes ordered, fix, confirmation | pass / findings |
| Prose tells | Assess passages in context per `human-prose-drafting`; preserve facts, terms, warnings and required structure; no word-blacklist failures | pass / findings |

## Findings

| Finding ID | Chunk | Severity | Evidence | Required change | Status |
|---|---|---|---|---|---|
| DR-001 | C-003 | Important | <quoted passage or missing item> | <what the author must do> | open |

Severities: Critical (reader cannot succeed or is misled), Important (reader
succeeds with friction or inconsistency), Minor (style within conventions).

## Verdict

- Open Critical or Important findings: <count>
- Result: Ready / Return to `documentation-authoring` with the findings above
