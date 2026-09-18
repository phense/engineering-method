---
name: documentation-pdf
description: "Use when existing Markdown documentation must become one local PDF with a reusable design, table of contents and page numbers. Supports a standalone document or an accepted documentation set. Not for drafting prose, reviewing content, deploying a website or publishing remotely."
---

# Documentation PDF

Apply the shared [proportionality rule](../../shared/policies/proportionality.md).
Render the reviewed Markdown with Quarto and its bundled Typst engine. Keep
Humanizer guidance in authoring; PDF export does not rewrite the text.

## Inputs and template

- A reviewed document or the accepted chunk manifest in `docs/writing/<doc-id>/plan.md`.
- Documentation language, title, output path and any brand requirements.
- The bundled [book configuration](../../templates/documentation/pdf/_quarto.yml),
  [brand](../../templates/documentation/pdf/_brand.yml) and
  [design guide](../../templates/documentation/pdf/DESIGN.md).

Resolve template resources relative to this skill, never the invoking cwd.
Read the design guide before configuring the output. Use Quarto 1.10.18 for the
verified baseline; inspect `quarto --version` and `quarto typst --version`.
Quarto is an external export dependency, not bundled in the plugin. Install
from the official release only when needed and verify its published checksum.
Rendering is local; no online Typst account or document upload is needed.

## Prepare the book

1. For an existing project, preserve its configuration and make the smallest
   change. For a new one, copy the complete template directory into the chosen
   documentation root. Omit `_book/`, `.quarto/` and generated top-level `.typ`
   files if copying from a checkout that has already been rendered; retain the
   extension's `.typ` sources. Never overwrite existing files when copying.
2. Set title, subtitle, language and output name in `_quarto.yml`. Configure
   colors and fonts in `_brand.yml`; the Typst layout lives in the extension.
3. Replace the example chapter list with the accepted manifest files in their
   recorded row order. Include each selected chunk exactly once, omit
   superseded rows and do not sort by filename. Reconcile missing or duplicate
   files before rendering. Record the manifest revision in the export evidence.
   For a standalone text, list that text after the book's `index.md` introduction.
4. Paths in `book.chapters` are relative to the Quarto project root. Keep the
   Markdown sources and local images in that tree, retaining their relative
   relationships. Preserve chunk frontmatter; rendering options belong in the
   project configuration. Give chapters stable heading IDs and use Quarto
   cross-references for links that must work inside the PDF.
5. Replace sample title and chapter content before delivering a real document.
   Resolve image placeholders before calling the PDF final; a requested preview
   may retain them only when clearly labeled as a draft. Do not enable code
   execution, remote images or remote includes as a side effect of export.

## Render and verify

From the book directory run `quarto render --to em-manual-typst`. The default
output is `_book/manual.pdf`; a different `book.output-file` changes that name.
Keep generated output and `.quarto/` out of the source repository.

Check the actual PDF, not only the renderer's exit code:

- Every selected chapter appears once, in manifest order.
- The cover is visually separate from the contents and has no running footer.
- The table of contents is clickable and its page references match the chapters.
- Page numbers and the total in the footer are correct, including the final page.
- Cross-references and images resolve; long tables and code fit within margins.
- Inspect representative rendered pages for clipping, isolated headings, broken
  callouts, missing glyphs, excessive line length and usable contrast. Confirm
  that chapter rules use the configured dark accent. Check each page in a short
  book.
- Compare the source files before and after rendering; export must not change
  prose, facts or chunk metadata.

Use `pdfinfo`, `pdftotext` and page images when available. Record tool versions,
command, source revision, output path, checks and remaining limitations in the
existing review or verification record. Return a clickable local PDF link.

## Boundaries

Rendering does not grant content acceptance or deployment approval. Return
content defects to `documentation-authoring`; fix layout in the template.
Do not run GitHub migration, `backlog state-check`, remote publication or a
second prose-humanizing phase during PDF export. Finish with
`verification-before-completion` after inspecting the rendered artifact.
