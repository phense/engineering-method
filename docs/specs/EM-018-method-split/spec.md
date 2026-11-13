# Feature Specification: Shared core, engineering and writing methods

## Stable work ID

- Feature ID: `EM-018`
- Status: Accepted for implementation by the user's end-to-end request, 2026-11-13.
- Source request: Separate writing into `phense/writing-method`, share host adapters across both methods, and reassess genuinely shared responsibilities including playbooks.

## User scenarios

### US-001: Install a focused method (P1)

An author installs writing-method without engineering lifecycles. An engineer installs engineering-method without the writing lifecycle. Both get the common support needed to finish their work. Independent test: validate and exercise an extracted package with no sibling repositories present.

### US-002: Maintain shared behavior once (P1)

A maintainer updates adapters or shared state in method-core and synchronizes a pinned revision into each method. Independent test: both locks identify the same revision and all shared bytes and executable modes agree.

### US-003: Use playbooks in either method (P1)

An engineering migration or a writing publication/export can request a scenario-bound procedure, review and rehearsal evidence without starting a competing lifecycle. Independent test: each method bundles the playbook skills, templates and review support with no dependency on the other method.

## Acceptance criteria

- AC-001: Each method has matching Claude/Codex manifests, a local marketplace and a self-contained package whose skill-resource links resolve.
- AC-002: Engineering contains its engineering lifecycles; Writing contains all ten existing writing skills, policies, documentation/PDF templates and Humanizer attribution. No removed method remains an implicit mandatory dependency.
- AC-003: Core is the canonical source of genuinely shared support, including the two playbook skills. Consumer changes to core files are detected offline; synchronization refuses to overwrite local modifications or unowned files.
- AC-004: A synchronization failure leaves the old usable target intact; a subsequent valid synchronization and offline check work.
- AC-005: Existing project-state CLI commands, Python imports, work IDs, `.engineering-method/` data and backlog records remain compatible.
- AC-006: The methods can coexist. Shared skill names have byte-identical contracts; method-qualified invocation chooses an owner. OpenCode loaders do not overwrite each other.
- AC-007: Existing licenses, immutable upstream revisions and source hashes survive the split. Destination hashes reflect the actual delivered bytes.
- AC-008: Verification distinguishes structural/installation evidence from live model routing; no Claude live-evaluation claim is made during its outage.

## Functional requirements

- FR-001: Publish source boundaries as three independently versioned repositories under `phense`.
- FR-002: Keep host adapter implementations in the shared source; defer Gemini-specific behavior until separately verified.
- FR-003: Retain all existing authoring/planning/review/PDF behavior in the writing method.
- FR-004: Share backlog, continuity, verification, collaboration/review/isolation and generic playbook support; keep method-specific lifecycle graphs in their method.
- FR-005: Ship immutable, hashed shared copies so installation needs no sibling checkout, submodule or runtime network request.
- FR-006: Provide a safe repeatable sync/check command and independent source/target validation.
- FR-007: Document installation, update, rollback, coexistence and evidence limits for maintainers.

## Compatibility boundaries

Preserve `engineering_method` as the runtime Python import and all existing CLI wrapper names; ownership moves without renaming persisted data. Existing installation settings remain active until replacement packages are verified. Keep historical engineering specifications and release evidence as history. New package versions are engineering-method 0.3.0, writing-method 0.1.0 and method-core 0.1.0; no release tag or production installation is implicit in source publication.

## Interface contracts

| ID | Boundary | Contract |
|---|---|---|
| IC-001 | Core to consumer | A committed export inventory, immutable revision, relative paths, SHA256 and executable modes; exact copies in existing package-root paths. |
| IC-002 | Consumer to project | Existing `project-state`, `continuity-state`, `backlog-to-issues`, `refresh-issue-cache` and `engineering_method` imports; project cwd stays distinct from plugin root. |
| IC-003 | Host to method | Existing Claude/Codex manifests and OpenCode loader; no live credentials/configuration are copied. |
| IC-004 | Playbook to lifecycle | Authoring returns a draft, review returns a separate verdict, rehearsal remains separate authorized work; the invoking method owns acceptance. |

## Edge cases

Reject traversal, symlinked managed paths, malformed locks, missing blobs, duplicate exports, changed permissions and conflicting target ownership before mutation. A package moved to another directory remains usable. A source checkout with dirty export files must not silently supply uncommitted bytes. Shared dependencies must resolve even when only one method is installed.

## Assumptions and unresolved decisions

User-approved architecture is a third core repository vendored into both methods. Playbooks move to core following the user's later steering. Public visibility follows the existing public engineering repository. Shared support skills are namespaced by the method plugin when invoked; the core is a source repository, not a third plugin to install. Gemini remains a separately tracked follow-up. No unresolved implementation-blocking scope decision remains.

## Success measures

- SC-001: Both isolated packages pass validation and execute state/continuity commands against a fresh target project.
- SC-002: Common runtime characterization tests pass before and after the split; original baseline was 319 passing tests.
- SC-003: Lock tampering and interrupted synchronization tests fail safely, followed by successful recovery.
- SC-004: Independent review resolves all Critical/Important findings before integration handoff.

## Playbook obligations

No new system playbook is required: the delivered sync command must handle conflicts and rollback itself. Installation and source rollback instructions suffice for this reversible repository split; it changes no live service or user data. Existing playbook skills/templates are deliverables under FR-004, not a requirement to invent operational procedures.
