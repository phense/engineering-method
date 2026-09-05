# Peter's Engineering Method

Risk-proportionate engineering workflows for Codex and Claude. One shared plugin
combines selected Spec Kit, OpenSpec and Superpowers practices with durable
project state, cohesive implementation slices and architecture verification.
Small edits stay small; complex changes receive the evidence they need.

Version `0.1.0` is a local pre-release candidate. The
[approved design](docs/specs/2026-09-04-engineering-method-design.md) defines the
scope; [verification records](docs/verification/EM-004-acceptance.md) distinguish
tested behavior from outstanding host-release evidence. Nothing is published
automatically.

## Installation

Requirements: Python 3.11 or newer, Git, and the supported host CLI. GitHub
integration additionally uses the authenticated `gh` CLI. No upstream Spec Kit,
OpenSpec or Superpowers CLI/plugin is required. Use the same plugin directory
on both hosts. There is no public repository URL configured yet; local
installation is the supported starting point.

From a local checkout or extracted release package:

```sh
em_plugin="$(pwd)"
codex plugin marketplace add "$em_plugin"
codex plugin add engineering-method@engineering-method
codex plugin list --json
```

Start a new Codex session after installation or updating the cached plugin.
For Claude, load the directory for the session:

```sh
claude plugin validate --strict "$em_plugin"
claude --plugin-dir "$em_plugin"
```

Run the host in the project you want to change, retaining the absolute plugin
path. See the [Codex adapter](shared/platform/codex.md) and
[Claude adapter](shared/platform/claude.md) for host mechanics and reload behavior.
Installing overlapping lifecycle plugins alongside this one can introduce
external trigger collisions; this package contains only its curated skill tree.

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

Review, TDD, worktrees and parallel dispatch activate only when their own
conditions apply. If a bounded change reveals architectural scope, its formal
escalation artifact preserves the original work and transfers ownership.

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
apply. This repository has no remote and does not create one automatically.

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

Run from the plugin root:

```sh
python3 -m unittest discover -s tests -t . -v
python3 scripts/validate-plugin
claude plugin validate --strict .
python3 -m compileall -q engineering_method scripts tests
git diff --check
```

Build and check a reproducible package, test its local installation, then run
the release gate (live evaluations require native host authentication):

```sh
python3 scripts/package-plugin --check --output /tmp/engineering-method.zip
python3 tests/e2e/test-clean-install --package /tmp/engineering-method.zip
python3 scripts/release-check --release --output-dir /tmp/em-release
```

The portable checks need no network or model credentials. Tests cover backlog
ordering, issue reconciliation through a fake GitHub boundary, compaction
recovery, exclusive lifecycle contracts, and actual checkout success and
compensation behavior. Pinned-source auditing additionally takes explicit local
upstream roots through `python3 scripts/audit-provenance --source-root ID=PATH`.

## Validation scope

Static contracts and deterministic fixtures establish the shared implementation.
Live routing and full architecture runs must separately establish behavior on
each host. Missing credentials, malformed transcripts, timeouts and absent
evidence are failures rather than successful skipped release gates.

Clean-install checks use temporary host configuration homes. Authenticated live
evaluations must identify their credential context and isolate project/settings
effects; no credentials are copied into the package or recorded in evidence.
The release gate must pass on both hosts before release readiness is claimed.
No live GitHub mutation test is implied by fake-boundary coverage.

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

Project-state implementation, architecture modeling, host adapters and validation
fixtures are original work. Orchestration combines original policy with the
specifically mapped adapted mechanics; it is not a wholesale upstream copy.
Upstream names identify sources and do not imply affiliation with
or endorsement by their maintainers.
