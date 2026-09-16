---
id: C-003
title: Check the finished PDF
type: task
doc_id: pdf-example
readers: [R1]
status: reviewed
version: Quarto 1.10.18
last_reviewed: 2026-09-16
---

# Check the finished PDF {#sec-check}

## Verify the reading path

1. Compare the PDF chapter order with the documentation plan.
2. Click an entry in the contents and check its destination page.
3. Follow the link back to @sec-start and verify that it reaches the first chapter.

The links should stay inside the PDF, and their printed numbers should match
the destination headings. This [relative chapter link](01-start.md) should also
open the first chapter.

## Inspect the pages

Look at every page in a short guide. For a long manual, inspect the title,
contents, chapter openings, tables, figures, code and final page. Check that
nothing is clipped and that headings stay with their following text.

> Keep the content review separate from the layout check. A successful render
> confirms that the document can be built; it does not confirm the instructions
> are correct for the reader.

## Record the result

Record the source revision, tool versions, output path and any unresolved
layout defects. On this final page, the current page and the total in the footer
should be equal. The Markdown source files must remain unchanged after rendering.
