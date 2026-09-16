---
id: C-002
title: Configure the document
type: reference
doc_id: pdf-example
readers: [R1]
status: reviewed
version: Quarto 1.10.18
last_reviewed: 2026-09-16
---

# Configure the document {#sec-reference}

## Files and responsibilities

| File | What you change |
|---|---|
| `_quarto.yml` | Title, language, ordered chapter list and PDF filename |
| `_brand.yml` | Accent color, text color and font families |
| `chapters/*.md` | The text, tables, links and images readers will use |
| `_extensions/em-manual/typst-template.typ` | Heading layout, whitespace and footer |

## Chapter order

List files explicitly in `book.chapters`. Use the order in the accepted
documentation plan and include each selected chapter once. A filename does not
determine the reading order.

::: {.callout-warning icon=false}
Copy templates into a new directory. Do not replace an existing guide's
configuration or chapter files without inspecting them first.
:::

## Links and numbers

Give important headings a stable ID such as `{#sec-start}`. A reference such as
`@sec-start` produces a link and a chapter number in the PDF. The contents and
footer page numbers are recalculated when text changes.

## Language and fonts

Set `lang: de` for German labels, including the footer “Seite X von Y”. The
content remains in the language in which you wrote it. Changing this option
does not translate your Markdown files.

Font files are not bundled. Keep font names and installed versions consistent
on the machines that produce your PDFs.
