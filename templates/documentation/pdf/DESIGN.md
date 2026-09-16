# Manual PDF design

Use this template to turn a reviewed Markdown document set into one local PDF.
It follows the supplied marketing guide's visual direction: white A4 pages,
petrol accents, a clear sans-serif hierarchy, quiet callouts and a running footer.
The layout and sample text are original; the reference PDF and its content are
not distributed with the template.

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
| Page | A4, 18 mm side margins, 20 mm top, 22 mm bottom | `_quarto.yml` |
| Accent | Petrol `#007D8A` | `_brand.yml`, `color.palette.petrol` |
| Text | Dark ink `#20262B`, 11 pt | `_brand.yml`, foreground and base typography |
| Heading hierarchy | 28 pt title, 20 pt chapter, 14 pt section | `typst-template.typ` |
| Chapter marker | White number on a petrol badge | `typst-template.typ` |
| Contents | Linked headings, two levels, automatic page references | `_quarto.yml`, `toc-depth` |
| Footer | Document title and current/total page count | `typst-template.typ` |
| Code | 9 pt monospace, shaded blocks | `_brand.yml` and Typst layout |
| Notes and warnings | Quarto callouts with icons disabled in the sample | Markdown callout attributes |

The two `.typ` files live in `_extensions/em-manual/`. Change design rules there
instead of adding layout instructions to chapter prose. Keep required headings,
content order, facts and warnings intact when adapting the appearance. For a
long document, use a short title in the footer or adapt the footer layout before
letting it wrap across several lines.

## Language and numbering

`lang: en` selects English labels. `lang: de` selects German labels and the
footer `Seite X von Y`. This setting does not translate the content. The title
and contents count as page 1, so printed numbers and PDF viewer page numbers
agree. Chapters begin on a new page; this template uses single-sided layout
without blank recto/verso pages. It supports a flat ordered chapter list;
parts and separately numbered appendices need their own layout work.

Keep headings with the following paragraph. Split very long commands or table
cells at meaningful points rather than shrinking text until it is unreadable.
Check long tables, figures and callouts for overflow. A renderer's successful
exit status does not prove a usable layout or PDF accessibility conformance.

## Verification

Run `python3 tests/e2e/test-documentation-pdf --quarto /path/to/quarto` from the
Engineering Method checkout for the native sample check. It requires Poppler's
`pdfinfo` and `pdftotext` and MuPDF's `mutool`. These tools are verification
utilities; the render itself only needs Quarto and the configured fonts.

Check the rendered title, contents, chapter openings, code, tables, callouts and
last page visually. For delivery, confirm manifest order, working PDF links,
correct contents page references, every footer total and unchanged Markdown
sources. Keep `_book/`, `.quarto/` and generated `.typ` files out of version
control; the sample `.gitignore` does this without hiding the extension sources.

Sources: [Quarto book output](https://quarto.org/docs/books/book-output.html),
[custom Typst formats](https://quarto.org/docs/output-formats/typst-custom.html),
[central branding](https://quarto.org/docs/authoring/brand.html), and
[Typst page layout](https://typst.app/docs/guides/page-setup/).
