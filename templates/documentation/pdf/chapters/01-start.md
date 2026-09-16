---
id: C-001
title: Create your first PDF
type: task
doc_id: pdf-example
readers: [R1]
status: reviewed
version: Quarto 1.10.18
last_reviewed: 2026-09-16
---

# Create your first PDF {#sec-start}

## Goal

Create one PDF from the introduction and three Markdown chapter files.

## Before you start

Install Quarto 1.10.18 and confirm that the fonts listed in `_brand.yml` are
available. This template uses Helvetica Neue and Menlo on macOS. Change those
names to installed fonts when rendering on another operating system.

::: {.callout-note icon=false}
The PDF is built locally. You do not need a Typst account or a browser session.
:::

## Build the document

1. Open a terminal in the copied template directory.
2. Run `quarto render --to em-manual-typst`.
3. Open `_book/manual.pdf` in your PDF viewer.

You should see a title, contents with page references, and the chapter headings
listed in `_quarto.yml`. Each page has a footer with its number and the total.

```sh
quarto --version
quarto render --to em-manual-typst
```

## Check that it worked

Use the contents to open @sec-reference. Confirm that the footer shows the same
page as the contents entry. Follow the final checklist in @sec-check before
sharing a real document.
