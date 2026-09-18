# Manual PDF design

Use this template to turn a reviewed Markdown document set into one local PDF.
It uses white A4 pages, dark-navy rules, a restrained sans-serif hierarchy,
quiet callouts and a running footer. The layout and sample text are original.

The design is deliberately editorial rather than application-like. The cover
has one focal point, the contents begin on their own page, chapter numbers are
typography rather than badges, and colour supports the hierarchy instead of
carrying it alone.

## Build

Copy this directory's source files into a new documentation directory. Exclude
`_book/`, `.quarto/` and generated top-level `.typ` files when copying an already
rendered checkout; keep `.typ` sources inside `_extensions/`. Run from that copy:

```sh
quarto --version
quarto render --to em-manual-typst
```

Open `_book/manual.pdf`. The verified baseline is Quarto 1.10.18 with bundled
Typst 0.15.1. No R, Python, LaTeX or online Typst account is needed to render
these Markdown chapters. The plugin does not bundle Quarto or install it
implicitly. Get it from the [official release](https://github.com/quarto-dev/quarto-cli/releases/tag/v1.10.18)
and check the release's SHA-256 checksum before installing.

The sample uses Helvetica Neue and Menlo, available on the verified Mac. On
other systems, select installed font families in `_brand.yml`, for example
locally installed Noto Sans and Noto Sans Mono. Do not ignore missing-font
warnings. Fonts are not downloaded or redistributed by this template.

## Source and order

Replace the sample files with your accepted chapters. Set their explicit order
in `book.chapters` in `_quarto.yml`, with paths relative to that file. The first
file is `index.md`, containing introductory material. Compare the list with the
accepted chunk manifest, in row order; include each selected chunk exactly once.
No manifest parser or filename sorting runs implicitly.

Each chapter has one H1. Existing Engineering Method chunk frontmatter can stay:
when Quarto adds a matching title heading from that metadata, the bundled filter
removes only the generated duplicate in the render tree. It preserves the
original Markdown files and the authored heading ID. Use stable IDs such as
`{#sec-start}` and references such as `@sec-start` for links across chapters.

Keep image paths relative to the chapter that contains them. Inspect images,
links and callouts in the actual PDF. The sample configuration disables code
execution. Use local assets; remote includes and external image downloads are
not part of this workflow.

## Design settings

| Element | Default | Where to change it |
|---|---|---|
| Page | A4, 28 mm side margins, 22 mm top, 24 mm bottom | `_quarto.yml` |
| Accent | Dark navy `#173A5E` | `_brand.yml`, `color.palette.navy` |
| Text | Dark ink `#232A31`, 12 pt | `_brand.yml`, foreground and base typography |
| Heading hierarchy | 36 pt cover, 25 pt chapter, 15 pt section | `typst-template.typ` |
| Chapter marker | Navy number, dark title and a 1 pt navy rule | `typst-template.typ` |
| Contents | Linked headings, two levels, automatic page references | `_quarto.yml`, `toc-depth` |
| Footer | No cover footer; then document title and current/total page count | `typst-template.typ` |
| Code | 9.5 pt monospace, shaded blocks | `_brand.yml` and Typst layout |
| Notes and warnings | Quarto callouts with icons disabled in the sample | Markdown callout attributes |

The two `.typ` files live in `_extensions/em-manual/`. Change design rules there
instead of adding layout instructions to chapter prose. Keep required headings,
content order, facts and warnings intact when adapting the appearance. For a
long document, use a short title in the footer or adapt the footer layout before
letting it wrap across several lines.

## Typographic rationale

Treat the defaults as a coherent starting system, not isolated numbers:

- The 28 mm side margins move ordinary A4 prose toward the established 45–75
  character reading range instead of filling almost the entire sheet. Actual
  characters per line still vary with the font and the text.
- The 12 pt body and open leading favour sustained reading. Left-aligned,
  non-justified text avoids the uneven word spaces produced by narrow justified
  columns.
- Space, size and weight establish hierarchy before colour. The navy accent is
  reserved for headings, links and rules; paragraphs remain dark neutral ink.
- Heading space is asymmetric: more separation before a new section, less
  between its heading and first paragraph. Chapter rules sit close enough to
  read as part of the heading.
- The default ink, navy and muted text have contrast ratios of 14.51:1,
  11.65:1 and 5.87:1 against white. These exceed the WCAG 2.1 AA threshold for
  ordinary text, although contrast alone is not a PDF accessibility claim.

Do not reduce margins merely to fit one more paragraph. First shorten or split
content, simplify tables, or give a wide figure its own layout. A successful
render is not evidence that a dense page is comfortable to read.

## Typst and LaTeX

The layout principles above are engine-independent. Quarto's LaTeX route uses
KOMA-Script by default and is a strong choice when a publisher requires `.tex`,
specialist TeX packages, or print-binding controls. This template retains Typst
because its custom format is already local, fast and self-contained in Quarto;
it does not require a separate TeX distribution. Changing engines would not by
itself repair weak margins, spacing or hierarchy.

Keep one accepted layout implementation rather than maintaining visually
divergent Typst and LaTeX templates. Add a LaTeX variant only for a concrete
delivery requirement and verify it as a separate output contract.

## Language and numbering

`lang: en` selects English labels. `lang: de` selects German labels and the
footer `Seite X von Y`. This setting does not translate the content. The title
page is PDF page 1 but intentionally has no running footer. The contents begin
on page 2, and printed footer numbers then agree with PDF viewer page numbers.
Chapters begin on a new page; this template uses single-sided layout without
blank recto/verso pages. It supports a flat ordered chapter list; parts and
separately numbered appendices need their own layout work.

Keep headings with the following paragraph. Split very long commands or table
cells at meaningful points rather than shrinking text until it is unreadable.
Check long tables, figures and callouts for overflow. A renderer's successful
exit status does not prove a usable layout or PDF accessibility conformance.

## Verification

Run `python3 tests/e2e/test-documentation-pdf --quarto /path/to/quarto` from the
Engineering Method checkout for the native sample check. It requires Poppler's
`pdfinfo` and `pdftotext` and MuPDF's `mutool`. These tools are verification
utilities; the render itself only needs Quarto and the configured fonts.

Check the rendered cover, contents, chapter openings, code, tables, callouts and
last page visually. Confirm that the cover is uncluttered and has no footer,
the chapter rule is dark navy, and prose uses the intended narrower measure.
For delivery, confirm manifest order, working PDF links, correct contents page
references, every footer total and unchanged Markdown sources. Keep `_book/`,
`.quarto/` and generated `.typ` files out of version control; the sample
`.gitignore` does this without hiding the extension sources.

Sources: [Quarto book output](https://quarto.org/docs/books/book-output.html),
[custom Typst formats](https://quarto.org/docs/output-formats/typst-custom.html),
[central branding](https://quarto.org/docs/authoring/brand.html), and
[Typst page layout](https://typst.app/docs/guides/page-setup/). The design
rationale also draws on the [ONS accessible text guidance](https://service-manual.ons.gov.uk/brand-guidelines/typography/accessible-text-formatting),
the [Eurostat A4 publication grid and heading styles](https://ec.europa.eu/eurostat/documents/4187653/7192088/STYLE_GUIDE_2016.pdf),
the [W3C minimum-contrast explanation](https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum),
and Quarto's [LaTeX/KOMA-Script PDF documentation](https://quarto.org/docs/output-formats/pdf-basics).
