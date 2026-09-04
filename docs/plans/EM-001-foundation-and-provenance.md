# EM-001 Foundation and Provenance Implementation Plan

> **For agentic workers:** Use `superpowers:subagent-driven-development` to bootstrap this plan. Keep one strong coordinator, apply TDD to validator behavior, and update `BACKLOG.md` after every completed task.

**Goal:** Establish a dependency-free, host-neutral plugin foundation with valid Codex and Claude manifests, portable validation, MIT licensing, and immutable provenance for the approved upstream snapshots.

**Architecture:** Both hosts consume one root `skills/` tree through separate manifests. A Python 3.11+ standard-library validator owns portable structural checks; native host validators remain additional evidence. No upstream CLI or plugin is installed at runtime.

**Tech Stack:** Python 3.11+ standard library, `unittest`, JSON, Markdown, Git.

**Spec:** `docs/specs/2026-09-04-engineering-method-design.md`

## Global Constraints

- Plugin ID: `engineering-method`; display name: `Peter's Engineering Method`; initial version: `0.1.0`.
- Public files and skill instructions are English.
- No PyYAML, pytest, upstream CLI, hooks, MCP server, app, or asset is added in this block.
- The Codex manifest must not declare `hooks`, `apps`, or `mcpServers` without corresponding supported components.
- Record these immutable source revisions:
  - Spec Kit: `df6b3187022ce986759bd854467e8a4bb56bb0f4`
  - OpenSpec: `e062b9572be933564ba3899d059377dfa1393e32`
  - Superpowers: `b36e0829c6d0140e93cfef2ca599b1b07d4a7797`
- `/.engineering-method/` is local recovery state and must be ignored.

## File Map

| File | Responsibility |
|---|---|
| `.gitignore` | Ignore recovery state and Python by-products. |
| `.codex-plugin/plugin.json` | Codex package identity and common skill root. |
| `.claude-plugin/plugin.json` | Claude package identity; root skills use default discovery. |
| `skills/.gitkeep` | Preserve the common skill root before lifecycle skills exist. |
| `scripts/validate_plugin.py` | Portable validation API and CLI implementation. |
| `scripts/validate-plugin` | Executable wrapper. |
| `tests/test_validate_plugin.py` | Fixture-based validator tests. |
| `LICENSE` | Peter Hense's MIT license. |
| `THIRD_PARTY_NOTICES.md` | Complete upstream MIT notices and immutable revisions. |
| `third-party/sources.lock.json` | Machine-readable provenance ledger. |
| `README.md` | Truthful pre-release scope and validation instructions. |

### Task 1: EM-001.1 Add the portable validator contract

**Files:**

- Create: `scripts/__init__.py`
- Create: `scripts/validate_plugin.py`
- Create: `scripts/validate-plugin`
- Create: `tests/__init__.py`
- Create: `tests/test_validate_plugin.py`

**Interfaces:**

```python
def validate_repository(root: pathlib.Path) -> list[str]:
    """Return sorted validation errors, or an empty list."""

def main(argv: collections.abc.Sequence[str] | None = None) -> int:
    """Validate argv[0] or the current directory and return a process code."""
```

- [ ] Write tests using `tempfile.TemporaryDirectory()` for missing manifests, invalid JSON, manifest-name mismatch, missing common files, unfinished markers, invalid skill frontmatter, and a complete fixture.
- [ ] Assert the exact missing-file diagnostic `ERROR .codex-plugin/plugin.json: file is required`.
- [ ] Run `python3 -m unittest tests.test_validate_plugin -v`. Expected red result: `ModuleNotFoundError: No module named 'scripts.validate_plugin'`.
- [ ] Implement JSON parsing, repository-relative diagnostics, strict semver, common manifest identity checks, required Codex interface fields, component-path existence, skill frontmatter checks, and unfinished-marker detection without a YAML dependency.
- [ ] The unfinished scan rejects bracketed task placeholders and the banned scaffold phrases defined by the validator tests, excluding `.git/`, Python caches, fixtures explicitly testing those strings, and generated recovery state.
- [ ] Create `scripts/validate-plugin` as:

  ```python
  #!/usr/bin/env python3
  from validate_plugin import main

  raise SystemExit(main())
  ```

- [ ] Run `python3 -m unittest tests.test_validate_plugin -v`. Expected: all fixture tests pass.
- [ ] Commit with `git commit -m "test: add dependency-free plugin validator"`.

### Task 2: EM-001.2 Create dual-host manifests

**Files:**

- Create: `.codex-plugin/plugin.json`
- Create: `.claude-plugin/plugin.json`
- Create: `.gitignore`
- Create: `skills/.gitkeep`
- Modify: `tests/test_validate_plugin.py`

**Shared manifest identity:**

```json
{
  "name": "engineering-method",
  "version": "0.1.0",
  "description": "Risk-proportionate engineering workflows for Codex and Claude.",
  "author": {"name": "Peter Hense"},
  "license": "MIT",
  "keywords": ["engineering", "workflow", "specification", "testing", "review"]
}
```

- [ ] Add a real-repository test and run it. Expected red result: missing `.codex-plugin/plugin.json`.
- [ ] Create the Codex manifest with `"skills": "./skills/"` and this interface:

  ```json
  {
    "displayName": "Peter's Engineering Method",
    "shortDescription": "Risk-proportionate workflows for engineering agents",
    "longDescription": "A shared workflow skill set that selects lightweight or rigorous engineering practices according to the requested work and its risk.",
    "developerName": "Peter Hense",
    "category": "Developer Tools",
    "capabilities": ["Interactive", "Read", "Write"],
    "defaultPrompt": [
      "Plan a new multi-component feature.",
      "Diagnose and fix this reproducible regression.",
      "Propose a bounded change to existing behavior."
    ],
    "brandColor": "#0B7285",
    "screenshots": []
  }
  ```

- [ ] Create the Claude manifest with the shared identity, `"$schema": "https://json.schemastore.org/claude-code-plugin-manifest.json"`, and `"displayName": "Peter's Engineering Method"`. Omit a `skills` field because Claude discovers root `skills/` automatically.
- [ ] Add `/.engineering-method/`, `.venv/`, `__pycache__/`, `*.py[cod]`, `.coverage`, and `htmlcov/` to `.gitignore`.
- [ ] Run `python3 scripts/validate-plugin`. Expected: only `README.md`, `LICENSE`, `THIRD_PARTY_NOTICES.md`, and the source lock remain missing.
- [ ] Commit with `git commit -m "feat: add Codex and Claude plugin manifests"`.

### Task 3: EM-001.3 Add licensing and pinned provenance

**Files:**

- Create: `LICENSE`
- Create: `THIRD_PARTY_NOTICES.md`
- Create: `third-party/sources.lock.json`
- Modify: `tests/test_validate_plugin.py`

**Lock-file root:**

```json
{"schema_version": 1, "sources": []}
```

Each source entry contains `id`, `project`, `repository`, full `revision`, `license.spdx`, `license.source_path`, `license.sha256`, and `files`. Each file mapping contains `source_path`, `destination_path`, `source_sha256`, and `modification_status` from `notice-only`, `copied`, `adapted`, or `reference-only`.

- [ ] Add failing tests requiring exactly the source IDs `github-spec-kit`, `openspec`, and `superpowers`, 40-character revisions, lock/notice agreement, and these license hashes:
  - Spec Kit: `2510b446bc1f0cf9702453075d20cd88631e20e5642658edb7325d9c1eb534f7`
  - OpenSpec: `c3c7235bea1214ab62df643473975c2e8b8848f528901a976693f7d069713e64`
  - Superpowers: `a37e0e9697144819e1d965176ac4ae5bc3fa02d11e7812036bbcadf6dafe2400`
- [ ] Run the validator tests. Expected red result: missing lock and notices.
- [ ] Create `LICENSE` with the complete MIT text and `Copyright (c) 2026 Peter Hense`.
- [ ] Create one complete MIT-notice section per upstream. Record repository, revision, license hash, copyright holder, and `LICENSE -> THIRD_PARTY_NOTICES.md` as `notice-only`. State accurately that EM-001 contains no copied workflow text.
- [ ] Create all three source-lock entries in the same order as the tests.
- [ ] Run `python3 -m unittest tests.test_validate_plugin -v`. Expected: only the real-root README requirement remains red.
- [ ] Commit with `git commit -m "docs: add MIT license and source provenance"`.

### Task 4: EM-001.4 Add truthful foundation documentation and host checks

**Files:**

- Create: `README.md`
- Modify: `tests/test_validate_plugin.py`

- [ ] Add a README contract test requiring project purpose, `0.1.0` pre-release status, design-spec link, both host names, test/validation commands, MIT link, third-party notice link, and non-endorsement wording. It must reject claims that lifecycle skills or marketplace installation already work.
- [ ] Run the README test. Expected red result: `README.md` missing.
- [ ] Write the foundation README in English with only functionality present after EM-001.
- [ ] Run:

  ```bash
  python3 -m unittest discover -s tests -t . -v
  python3 scripts/validate-plugin
  claude plugin validate --strict .
  ```

  Expected: unit and portable validation pass; Claude reports a valid plugin. If the installed Claude CLI uses a different flag order, record the verified invocation in the README and add a deterministic regression test for any manifest change it requires.
- [ ] Run `codex plugin --help` and record only capabilities actually shown. Do not invent a local Codex validation command or modify a global marketplace in this task.
- [ ] Run `git diff --check`.
- [ ] Update `BACKLOG.md`: mark `EM-001` and its children complete; leave dependent items unchanged.
- [ ] Commit with `git commit -m "docs: document validated plugin foundation"`.

## EM-001 Acceptance Evidence

- `python3 -m unittest discover -s tests -t . -v` passes.
- `python3 scripts/validate-plugin` passes.
- `claude plugin validate --strict .` passes using the installed CLI's verified syntax.
- Both manifests share identity and expose one `skills/` tree.
- License hashes match the pinned upstream revisions.
- `THIRD_PARTY_NOTICES.md` and `sources.lock.json` agree.
- `BACKLOG.md` records the completed block without renumbering IDs.
