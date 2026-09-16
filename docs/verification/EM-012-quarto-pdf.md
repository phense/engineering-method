# EM-012 Local Quarto and Typst PDF export

Subsequent acceptance: [EM-013](EM-013-prepublication.md) records native
documentation/Humanizer/PDF routing checks and final package installation.
The results and limits below describe this change's original verification.

Date: 2026-09-16. Base: `13a372f` (Humanizer drafting integration).

## Scope

The `documentation-pdf` supporting skill and original template under
`templates/documentation/pdf/` export reviewed Markdown as one local PDF.
The existing authoring and review skills hand off to it only when the user
requests a PDF. Humanizer remains part of drafting. The template is a bounded
extension of the existing documentation workflow, with no deployment service,
new project-state engine or automatic remote publication.

An agent maps the accepted plan's manifest rows to `book.chapters` in their
recorded order. This mapping is explicit and reviewed; no automatic manifest
parser is claimed. The template provides A4 geometry, configurable brand colors
and fonts, numbered chapters, a linked table of contents and current/total page
numbers. All source chapter frontmatter and Markdown bytes are preserved.

## Dependencies and provenance

- Quarto 1.10.18 from the official macOS tarball, SHA-256
  `ddd6a71a9e0448ab15fb655bc589e11cb6589a248ec35ccd7f7f44137531688e`,
  verified before extraction. Installed at `~/.local/opt/quarto-1.10.18`, with
  `~/.local/bin/quarto` pointing to its launcher.
- Bundled Typst: `0.15.1 (9dfd3a08)`.
- Native verification uses Poppler `pdfinfo`/`pdftotext` and MuPDF `mutool`;
  no additional Python packages or model calls are required.
- The skill, Lua adapter, Typst layout and sample content are original work.
  Quarto's runtime and third-party packages remain external and are not
  distributed in the Engineering Method plugin. Fonts are not bundled.
- The supplied design reference was inspected locally. Its content and file
  are not included in the template or verification fixtures.

## Native evidence

Command from the checkout root:

```sh
python3 tests/e2e/test-documentation-pdf \
  --quarto "$HOME/.local/bin/quarto" \
  --output-dir dist/pdf-verification-final
```

The output directory must be new; the harness never overwrites earlier runs.
The JSON report and PDFs are local ignored artifacts in that directory.

| Case | Result |
|---|---|
| English, introduction and three metadata-bearing Markdown chapters | 4 pages; chapter starts 2, 3, 4 |
| German labels, same source content | 4 pages; German contents and `Seite X von Y` footer; no translation claimed |
| Changed chapter order and 120-row table | 7 pages; chapter starts 2, 6, 7; every row retained exactly once |
| Frontmatter `title` plus authored H1 | One chapter and contents entry per source, original `sec-*` IDs retained |
| Contents and internal links | PDF annotation destinations resolve to the expected chapter pages |
| Relative `.md` chapter link | Resolves inside the PDF |
| Page totals | Every page shows the correct current number and document total |
| Source preservation | Markdown SHA-256 values identical before and after rendering |
| Basic overflow check | Extracted words stay within page bounds |

Disabling the title-normalization filter in an isolated template copy produced
an explicit `Duplicate contents entry` failure. The enabled filter passes the
same native check. Quarto inserts a generated heading and a
`quarto-title-block` before the authored H1; the adapter removes only a matching
synthetic heading before cross-reference numbering. A plain authored H1 and
its stable ID remain unchanged. Footer text is composed separately from the
numeric counters so Typst does not interpret letters in “Page” as numbering
patterns.

All four English baseline pages were visually inspected, plus the German
contents/footer and a continuation page of the long table. The final table
styling was inspected after its last change. Titles, body text, code, callouts,
contents and footer fit the pages; no visible clipping was found in those views.
This is bounded sample evidence, not a guarantee for every future document.

## Repository verification and review

- Full local Python suite: 317 tests passed.
- `python3 scripts/validate-plugin`: exit 0.
- `claude plugin validate --strict .`: passed.
- `python3 -m compileall -q engineering_method scripts tests`: exit 0.
- `git diff --check`: exit 0.
- Independent read-only review and independent native harness run: Ready,
  no actionable findings. The reviewer verified English/German output,
  reordered long-table output, authored IDs, destinations, totals, ordering,
  source preservation, provenance coverage and package inclusion rules.

## Limits

- Native evidence is from this macOS installation with Helvetica Neue and
  Menlo. Other operating systems and font substitutions need a fresh render.
- The sample supports a flat chapter list. Parts, independently numbered
  appendices, complex figures and custom diagram pipelines were not accepted
  by this change and are not claimed as tested.
- Tagged output is not a PDF/UA compliance claim; no accessibility conformance
  validator was run.
- Native host skill selection and installed-plugin refresh are not claimed.
  The source checkout and the native PDF build are verified locally.
- No GitHub state check, migration, issue creation, push or release was run.

Official references: [Quarto book output](https://quarto.org/docs/books/book-output.html),
[custom Typst formats](https://quarto.org/docs/output-formats/typst-custom.html),
[brand configuration](https://quarto.org/docs/authoring/brand.html),
[Typst page layout](https://typst.app/docs/guides/page-setup/).
