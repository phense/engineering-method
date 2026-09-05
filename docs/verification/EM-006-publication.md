# EM-006 public pre-release verification

## Scope

Publish `https://github.com/phense/engineering-method` and `v0.1.0-rc.1`
as an explicitly authorized **pre-release** of plugin `0.1.0`. No GitHub
Issues are created or migrated. The original EM-005 gate remains incomplete.

## Local evidence

Documentation and manifest revision `2508f3e` passed on 2026-09-05:

- All 301 Python unit/contract tests; no paid model evaluations.
- Portable plugin validator and Claude strict manifest validation.
- Python compileall, shell syntax checks and Git whitespace checks.
- Provenance audit against all three existing pinned upstream trees.
- Reproducible 186-file package and native Claude/Codex clean installation in
  disposable configuration homes, without credentials or model requests.
- Local Markdown links resolved. Documentation was checked against source,
  host CLI help and native installation behavior.
- The pre-publication history scan inspected 470 Git blobs and the 182-file
  original tracked inventory for credential patterns, private user paths and
  suspicious filenames, with no findings. New documentation was reviewed too.
  Pattern scanning is a bounded inspection, not a guarantee of secret absence.

Host versions: Python 3.14.6, Codex CLI 0.153.4, Claude Code 2.1.259, macOS.
The published package is rebuilt from its tagged commit; the release asset and
`SHA256SUMS` identify the final bytes. Local runtime state, full transcripts,
private logs and the external authoring skill are excluded from Git and packaging.

## Reused evidence and open limits

Implementation, skill policies, tests, templates, source locks and MIT notices
are unchanged from `03a979a`. Reuse the independent EM-004 reviews only within
[their recorded scope](EM-004-acceptance.md). Earlier native routing and Claude
architecture results retain the revision limits in
[EM-005](EM-005-completion-path.md). Current-package Codex architecture/reviewer
proof and the final independent release verdict remain missing. No failed gate
has been modified or marked passed. Mermaid rendering and live GitHub task
mutation acceptance remain outside this verification.

## Verified publication

- Public repository: https://github.com/phense/engineering-method.
- Pre-release: https://github.com/phense/engineering-method/releases/tag/v0.1.0-rc.1.
- Annotated tag `v0.1.0-rc.1` resolves to commit
  `9ff0bddeea13792de9d670337ea1c80c2987b72f`; no existing tag was overwritten.
- GitHub read-back confirmed public visibility, default branch `main`,
  `isPrerelease=true`, `isDraft=false`, and both uploaded assets.
- The final tagged package contains 187 files. Reproducible build and fresh native
  clean installation passed on both hosts. ZIP SHA-256:
  `21b27193dadafb939503c03db06659b2156affc190438c7f1fb45b0b35e5660f`.
- Both release assets were downloaded again; ZIP and checksum file matched the
  originals byte for byte, and `shasum -a 256 -c SHA256SUMS` passed.
- Documented GitHub installation, installed source bytes, update, disable and
  removal passed for both hosts in temporary configurations. No active plugin
  installation was changed and Superpowers was not reactivated.
- No GitHub Issues were created or migrated. BACKLOG.md remains canonical locally.

A subsequent documentation-only commit records these observed results and marks
EM-006 complete on `main`. The release tag and its verified package remain fixed
at the commit above. EM-005 and its outstanding technical evidence remain open.
