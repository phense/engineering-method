# Engineering Method

Risk-proportionate engineering workflows for Codex, Claude and OpenCode. One shared plugin
combines selected Spec Kit, OpenSpec and Superpowers practices with durable
project state, cohesive implementation slices and architecture verification.
Small edits stay small; complex changes receive the evidence they need.

Every skill follows a shared [proportionality rule](shared/policies/proportionality.md):
local checks first, reuse unaffected evidence, focused review of fixes, and an
effort brake before testing or delegation grows beyond the task. Subscription
limits and model-effort permissions remain binding across quota resets.

**[Version 0.1.1](https://github.com/phense/engineering-method/releases/tag/v0.1.1)
adds native OpenCode integration.** See the [release notes](docs/releases/0.1.1.md)
for its bounded acceptance. The historical 0.1.0 baseline has independently accepted
[complete original gate coverage](docs/verification/EM-005-acceptance.md), with
documented evidence reuse and corrections. Read the acceptance limits before
relying on it for unattended work. The
[approved design](docs/specs/2026-09-04-engineering-method-design.md) records the
intended scope.

The earlier `v0.1.0-rc.1` pre-release remains available with its original, reduced
acceptance scope.

## Installation

Requires Python 3.11+, Git, and Codex CLI, Claude Code or OpenCode.
OpenCode uses the separate source-linked installation described below.
GitHub task synchronization additionally requires authenticated `gh` and repository
permissions. No upstream Spec Kit, OpenSpec or Superpowers installation is needed.
Native installation was checked with Codex CLI 0.153.4 and Claude Code 2.1.259;
other host versions and operating systems are not covered by that evidence.

Install from [phense/engineering-method](https://github.com/phense/engineering-method):

```sh
# Codex
codex plugin marketplace add phense/engineering-method
codex plugin add engineering-method@engineering-method

# Claude Code
claude plugin marketplace add phense/engineering-method
claude plugin install engineering-method@engineering-method
```

Start a new host session in your target project, then describe the change you
want. These commands follow the repository's default branch. For the fixed
release, local packages, updates, disabling and removal, see
[Installation and maintenance](docs/installation.md). Disable overlapping
lifecycle plugins, including Superpowers, before using Engineering Method.
Claude also supports session-only loading with `claude --plugin-dir` and an
absolute plugin directory; see the installation guide.

OpenCode can load the same shared skills through a source-linked native adapter;
its recorded discovery evidence covers the 17 skills of version 0.1.1.
See [OpenCode installation](docs/opencode.md) for setup, verification and the
bounded OpenCode 1.18.30 / DeepSeek acceptance scope. This addition is separate
from the historical v0.1.0 dual-host release evidence.

## Automatic workflow selection

Describe the engineering outcome. The host selects skills from exclusive
descriptions, existing artifacts and explicit handoffs; there is **no central router**
and no methodology-selection question. Quality skills support one primary
lifecycle rather than start competing plans.

| Work and current artifacts | Selected workflow |
|---|---|
| Small reversible docs/configuration or mechanical edit without behavior-contract impact | Focused edit and targeted verification; no spec, plan or UML cycle |
| Reproducible failure or unexplained regression | Systematic debugging, meaningful regression test, fix and verification |
| Bounded intentional change to existing behavior | OpenSpec `propose` → `apply` → `archive` |
| New subsystem, multi-component feature, architecture change or risky migration | Spec Kit `specify` → `plan` → architecture gate → `tasks` → orchestrated implementation → `converge` |
| Existing Spec Kit or OpenSpec artifacts | Continue the recorded phase; preserve completed work |
| One standalone reader-facing document | `documentation-authoring` in standalone mode with the didactic writing skills |
| Documentation set: several chapters or readers sharing terms, structure and images | `documentation-planning` → `documentation-authoring` per chunk → `documentation-review` |

Review, TDD, worktrees and parallel dispatch activate only when their own
conditions apply. If a bounded change reveals architectural scope, its formal
escalation artifact preserves the original work and transfers ownership.

## Documentation and reader-oriented writing

Prose deliverables decide their scale first with the
[writing-depth policy](shared/policies/writing-depth.md): a wording fix stays a
focused edit, one document uses `documentation-authoring` directly, and a
manual or handbook runs through planning, per-chunk authoring and set-wide
review with checkpoints across sessions. Plans, glossaries, asset manifests and
review reports live under `docs/writing/<doc-id>/`; chapters are one Markdown
file per chunk with uniform frontmatter.

Three didactic skills shape the text and, through the
[reader-oriented output policy](shared/policies/reader-oriented-output.md),
ordinary replies as well: `explaining-concepts` introduces each concept with
an everyday analogy before the mechanism and removes undefined jargon;
`writing-procedures` writes imperative single-action steps in blocks of three
to five with exact locations, prerequisites and a check that it worked;
`empathic-troubleshooting` starts from the symptom the reader sees. All three
apply the shared curse-of-knowledge filter that writes out the steps and
locations an expert would skip. Medium and large texts are drafted under
`human-prose-drafting`, an adaptation of Humanizer's AI-writing patterns
applied while writing, so finished documentation needs no separate
humanizing pass. `terminology-guard` keeps one term per concept
across hundreds of pages, and `visual-placeholders` inserts standardized
screenshot and diagram callouts with alt text and capture instructions.

For a requested PDF, `documentation-pdf` uses a reusable Quarto/Typst
[manual template](templates/documentation/pdf/DESIGN.md). It combines Markdown
chapters in the accepted order with central branding, a linked contents page
and current/total page numbers. Quarto is an optional local export dependency;
see the [native verification scope](docs/verification/EM-012-quarto-pdf.md).

## Architecture and review

Large features and architecture changes use relevant Mermaid sources under
`docs/uml`. Each diagram answers a named question and identifies its requirements,
source evidence and verification date. Small changes do not acquire an
architecture gate merely because diagrams exist.

Design findings become ordinary tasks before implementation. After cohesive
slices complete, a system architect reconciles the as-built diagrams with code
and derives cross-component success and relevant failure, rollback or recovery
tests. Convergence requires current reconciliation, integration results, resolved
review findings and fresh verification. Remaining findings return to the same
executor as new slices, preserving completed work.

Independent reviews cover risky or integration-bearing slices. Mechanical work
can use coordinator review. Failed fixes require new evidence or a changed
approach; repeated ineffective attempts escalate perspective rather than repeat
the same prompt. Parallel writes require disjoint ownership and safe isolation.

These are agent instructions supported by contract tests and executable fixtures,
not a mechanism that makes arbitrary host/model behavior infallible. Mermaid
sources can be semantically checked without a renderer; rendered validation is
reported separately when available.

## Backlog and GitHub Issues

`BACKLOG.md` is the canonical local task register. Stable IDs never change when
priorities change. Unblocking work comes first; status is open, in progress,
complete or blocked. `FEATURES.md` records working capabilities, not another
task list. Large local backlogs archive eligible completed groups while retaining
active dependencies.

With a reachable authorized GitHub repository and suitable CLI permissions,
migration preserves IDs and completed history in Issues. Hierarchy becomes
sub-issues and dependency edges become native dependencies. All agent-authored
GitHub titles, bodies, labels and comments are **English**. User communication
can remain in the user's language.

After migration, Issues are canonical and `BACKLOG.md` is a marked cache.
An offline outage queues changes for reconciliation rather than creating a
second source of truth. Migration and refresh use embedded identity markers to
avoid duplicate issues. Current project restrictions on remote mutations still
apply. Publishing this repository does not migrate its backlog. Its task register remains
local until a separate migration is explicitly authorized.

## Continuity

Stateful workflows persist checkpoints, concise recovery notes, artifact pointers
and events in `.engineering-method/runs/<work-id>/`. The coordinator owns run
state; agents own their assigned reports. Dispatch, review, fixes, verification
and phase transitions form recovery boundaries.

After `/compact` or a new session, skills validate saved work against Git,
artifacts, canonical task state and host-observed agents before continuing.
Completed work is retained; stale memory cannot override repository evidence.
This is explicit workflow checkpoint/recovery behavior, not a universal host
hook that intercepts every possible compaction.

The plugin works without agentic-rag. A separate downstream integration may
index events and recall a work ID plus artifact pointers; it never becomes the
canonical state writer. Project instructions and explicit user constraints
remain authoritative.

## Models and host adapters

The common core uses `strong`, `standard` and `fast` roles. Concrete model IDs,
effort levels and tool names live in the host adapters. The coordinator owns
architecture, cross-slice interfaces, integration and final acceptance.

Adapters inspect actual host capabilities, record unavailable preferred tiers,
and fall back without asking the user to choose a methodology. If delegation
or safe worktree isolation is unavailable, work proceeds sequentially when
possible. The plugin never claims to change the current main model when the
host cannot do so. Escalating model effort respects the adapter's explicit
approval boundary.

## Development and verification

Run the inexpensive local checks from the checkout root:

```sh
python3 -m unittest discover -s tests -t . -v
python3 scripts/validate-plugin
claude plugin validate --strict .
```

[Contributing](CONTRIBUTING.md) covers provenance, committed-source reproducible
packaging and isolated clean installation. Full release evaluations require
separate budget authorization and are not implied by these local checks.

## Examples and contributing

- [Usage examples](docs/usage.md): a small edit, bug repair, a bounded existing-system
  change, a large feature, one document, a documentation set, reader-oriented
  replies, and recovery after compact or a new session.
- [Contributing](CONTRIBUTING.md): local checks, provenance, packaging and review.
- [Verification history](docs/verification/EM-005-completion-path.md): bounded
  candidate acceptance and the [subsequent complete gate coverage](docs/verification/EM-005-acceptance.md).

## Validation scope

Skill descriptions and artifact handoffs guide host selection; they cannot
force every model to route correctly or follow every instruction. Delegation
and isolation depend on tools actually exposed by the host. Continuity requires
explicit checkpoints; there is no universal compact hook. agentic-rag is optional.
GitHub task operations have fake-boundary coverage, not live mutation acceptance.
Mermaid validation covers semantic sources, not rendered diagrams.

The accepted baseline covers 308 local tests, 24 native routing cases and the
architecture fixture on both hosts. Acceptance reused unchanged evidence and
included a Claude checkpoint instruction supplement and one verified report
metadata correction. No single successful full release-check invocation is
claimed. Native Codex recovery in the unborn fixture repository remains outside
that live proof; continuity has script-test coverage. See the
[acceptance record](docs/verification/EM-005-acceptance.md) for exact limits.

## License and attribution

Copyright (c) 2026 Peter Hense. Distributed under the [MIT License](LICENSE).
The [third-party notices](THIRD_PARTY_NOTICES.md) and
[source lock](third-party/sources.lock.json) contain pinned revisions, file
mappings, hashes and complete MIT notices.

- [GitHub Spec Kit](https://github.com/github/spec-kit): adapted specification,
  planning, task and convergence practices/templates.
- [OpenSpec](https://github.com/Fission-AI/OpenSpec): adapted bounded-change
  proposals, application and archival practices/templates.
- [Superpowers](https://github.com/obra/superpowers): adapted debugging, TDD,
  verification, reviews, worktree and delegation practices.
- [Humanizer](https://github.com/blader/humanizer): adapted AI-writing
  patterns as drafting-time constraints for documentation.

Project-state implementation, architecture modeling, host adapters and validation
fixtures are original work. Orchestration combines original policy with the
specifically mapped adapted mechanics; it is not a wholesale upstream copy.
Upstream names identify sources and do not imply affiliation with
or endorsement by their maintainers.
