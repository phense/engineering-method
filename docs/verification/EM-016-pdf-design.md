# EM-016 Professional A4 PDF design revision

Date: 2026-09-18. Base: `f45b1a8` on `main`.

## Scope

This revision improves the existing Quarto/Typst documentation template without
changing its Markdown composition contract. It replaces the wide petrol layout
with a restrained dark-navy A4 system: separate cover and contents pages, a
narrower text measure, 12 pt body text, typographic chapter numbers, controlled
heading spacing, dark-blue chapter rules and a cover without a running footer.

The design work does not add a LaTeX implementation. Publication was not part
of the initial design scope; the maintainer subsequently authorized a 0.2.1
version bump and GitHub publication. A separate state-tracking incident is
recorded below.

## Design evidence

The design decisions were checked against primary or institutional guidance:

- Typst recommends using margins or columns to keep lines near 45–75 characters.
- ONS guidance for general A4 material recommends a 12 pt starting minimum,
  left-aligned non-justified text, consistent hierarchy, useful white space and
  approximately 120–145% line spacing.
- Eurostat's publication grid uses explicit A4 geometry, deliberate white space,
  differentiated heading sizes and coloured chapter rules.
- W3C guidance requires at least 4.5:1 contrast for ordinary text. Against white,
  the template's ink, navy and muted colours measure 14.51:1, 11.65:1 and 5.87:1.
- Quarto supports both Typst custom formats and LaTeX/KOMA-Script. Typst remains
  the accepted engine here because the existing local format meets the need
  without a separate TeX distribution; switching engines is not a substitute
  for correcting the page geometry and rhythm.

The exact rationale and source links are recorded in
`templates/documentation/pdf/DESIGN.md`.

## TDD and native PDF evidence

A native end-to-end regression was added before the template change. It failed
because the old output placed the contents on the cover. The completed check now
also verifies a footer-free cover, contents on page 2, a rendered `#173A5E`
chapter rule and a body measure beginning at or inside the revised margin.

The Quarto 1.10.18 / Typst 0.15.1 sample check passes for:

| Case | Result |
|---|---|
| English sample | 5 pages; chapters begin on pages 3, 4 and 5 |
| German labels | 5 pages; German contents and footer labels pass |
| Reordered 120-row table | 9 pages; chapters begin on pages 3, 8 and 9 |
| PDF navigation | Contents, internal destinations and relative links pass |
| Source preservation | Markdown hashes are unchanged after rendering |

All five English sample pages were visually inspected after the final heading
spacing change. The cover, contents, chapter openings, table, callouts, code,
footer and final page show no visible clipping. This remains bounded sample
evidence, not a claim that arbitrary future content will fit without review.

## Repository verification and review

- `python3 -m unittest discover -s tests -t . -v`: 319 tests passed.
- Native PDF check: English and German samples plus the reordered 120-row table
  passed with Quarto 1.10.18 and Typst 0.15.1.
- `python3 scripts/validate-plugin`: passed.
- `claude plugin validate --strict .`: passed.
- Python compilation, shell syntax and `git diff --check`: passed.
- Coordinator review of the bounded template, documentation and regression-test
  diff found no unresolved template finding.

## Remaining limits

- The fonts remain Helvetica Neue and Menlo on the verified Mac. Other systems
  require selected installed fonts and a fresh visual check.
- The template does not claim PDF/UA conformance, complex book parts, separately
  numbered appendices, print bleed or imposed spreads.
- A LaTeX/KOMA-Script variant was researched but not added because no delivery
  requirement justifies a second template contract.

## State-tracking incident

An installed 0.1.1 backlog wrapper was used after the template checks. That
stale wrapper predates the repository's read-only state-check correction and
unexpectedly migrated the local backlog despite the absence of publication or
Issue-creation authorization. Read-only audit found 53 newly created GitHub
Issues, `#82` through `#134`, on 2026-09-18. All 53 issues are closed. The
stale wrapper process was stopped, and no further remote mutation was performed
afterward.

The local `BACKLOG.md` was restored to canonical local mode and the generated
queue removed. Deleting or otherwise mutating the unintended remote Issues is
outside the publication authorization; they remain closed and were not deleted.

## Published release

The maintainer subsequently authorized the version bump and GitHub publication.
Release `v0.2.1` was published from `49aa3c6aa7d57dbabea2e3edfe7d9cb083ea8dd6`
as a stable, non-draft, non-prerelease Latest release. Its reproducible 256-file
package has SHA-256
`2a0d0b6d520d509276c7d04d80b83a43a5aada78132d1ae48461c03fe3c21693`.
The downloaded release asset passed `shasum -a 256 -c SHA256SUMS`, and the tag,
asset digest and remote commit were verified after publication.
