# Documentation Plan: <documentation set name>

## Stable work ID

- Documentation ID: `<doc-id>`
- Artifact path: `docs/writing/<doc-id>/plan.md`
- Glossary: `docs/writing/<doc-id>/glossary.md`
- Asset manifest: `docs/writing/<doc-id>/assets.md`
- Content root: `<path where the chunk files live, for example docs/manual/>`
- Status: Planned

## Scale decision

- Scale: Large
- Evidence: <chapter count, audiences, expected length, shared terms, sessions>
- Documentation language: <language the readers read>
- Source-of-truth systems: <product version, UI build, API version, code paths>

## Readers

| Reader ID | Role and prior knowledge | Goal when reading | Interface and version |
|---|---|---|---|
| R1 | <role; what they already know and do not know> | <what they need to achieve> | <UI language, version, platform> |

Name the least experienced reader who is expected to succeed. Every chunk
declares which reader IDs it serves.

## Information architecture

Each chunk has exactly one content type. Do not mix a tutorial with reference
material or a procedure with a long explanation; link between them instead.
Types classify chunks; they are not the top-level navigation. Arrange sections
by the readers' journey and keep every level internally consistent.

| Type | Reader question | Shape |
|---|---|---|
| concept | Why and how does this work? | Analogy, mechanism, limits, related terms |
| task | How do I do X? | Goal, prerequisites, three-to-five-step blocks, validation |
| tutorial | Can you walk me through my first success? | Ordered lesson with a guaranteed visible result |
| reference | What exactly are the options, fields, limits? | Consistent tables and lists, no narrative |
| troubleshooting | Something is wrong; what now? | Symptom, likely causes in order, first check, fix, verification |

## Chunk manifest

One row per Markdown file. Rows define reading order; reorder rows without
renaming stable IDs.

| Chunk ID | File | Type | Title | Readers | Depends on | Assets | Status |
|---|---|---|---|---|---|---|---|
| C-001 | <content root>/<section>/<slug>.md | concept | <title> | R1 | none | none | planned |

Statuses: planned, drafted, reviewed, accepted, superseded.

## Conventions

- Frontmatter: every chunk uses the fields defined in the chunk template.
- File naming: `<section>/<kebab-case-slug>.md`; one chunk per file.
- Headings: one H1 equal to the title; H2 for the type's required sections.
- Procedures: imperative steps, one action per step, three to five steps per
  block, an observable result after each block.
- Terminology: the glossary is authoritative; add a term before using it.
- Prose: every chunk is drafted under the `human-prose-drafting` constraints;
  preserve source facts, technical terms and required structure while avoiding
  staged rhetoric and filler. There is no separate humanizing pass.
- Assets: use the placeholder callout syntax from `visual-placeholders` and
  register every placeholder in the asset manifest.
- Cross-references: link by relative file path and chunk ID; no bare "see above".

## Review and acceptance

- Set-wide review occurs when all chunks in a section reach drafted, and again
  before acceptance of the whole set.
- Acceptance criteria: <what makes the set complete, for example every reader
  goal has a path, every placeholder has capture instructions, no terminology
  findings remain>.

## PDF output (when requested)

- Export skill: `documentation-pdf`, after content acceptance.
- Quarto project root: <directory containing the chapters and _quarto.yml>
- PDF title, language and output name: <values>
- Design: <bundled em-manual template or named project template>
- Chapter list: accepted manifest rows in the same order, each included once.
- Verification: inspect contents links, page references, footer totals, assets
  and representative pages; record source revision and tool versions.

## Out of scope

- <documents, audiences, versions or platforms intentionally excluded>
