# EM-014: Engineering playbook integration

## Scope

The approved change adds playbook need assessment to engineering lifecycles,
plus authoring and review support. Development playbooks are prerequisites of
critical operations; system playbooks are accepted deliverables. The existing
documentation subsystem and all application executors remain unchanged.
Requirements and implementation decisions are in
[the specification](../specs/EM-014-playbooks/spec.md) and
[the plan](../specs/EM-014-playbooks/plan.md).

## Sources and adaptation

- medzin/sre-runbook-agent-skills at `44ab3d87293788036013098868563f82a3369b81`:
  author/reviewer mechanics and procedure/evidence templates, MIT.
- testdouble/han at `19cb21bcb1154d29bf20d1f3c9ad4854a59580d2`:
  selected need, provenance and validation rules in the shared policy, MIT.

Pinned raw bytes for all six source projects were fetched into a disposable
source tree. The provenance audit checked 39 unique upstream files and the
mapped destination hashes. Full notices and mappings are in the source lock
and THIRD_PARTY_NOTICES. Existing source revisions are preserved.

The adaptation accepts planned scenarios before a first incident, supports
normal user workflows and critical development operations, preserves existing
execution authority, makes incident-specific sections conditional, and separates
content review from actual rehearsal. No upstream runtime or connector is required.

## Independent review

A reviewer independent of implementation inspected the bounded change against
AC-001 through AC-008. One Important finding was confirmed: convergence asked a
report-writing reviewer to run inside its read-only gate. The correction assigns
missing/affected review tasks to the existing executor. The reviewer checked the
correction and returned Ready with no remaining actionable findings.

The same review performed bounded instruction-level scenario probes:

| Scenario | Observed decision |
|---|---|
| New service, preventive recovery before first launch | Specify system-playbook requirements; no previous incident required. |
| Live migration with approved specification | Plan development-playbook readiness and rehearsal before cutover. |
| Trivial reversible refactor | Focused edit; no playbook or new lifecycle. |
| Direct user-facing onboarding playbook | Authoring support directly; no invented documentation lifecycle or backlog. |
| Claimed validation on generation date plus unsafe non-idempotent retry | Changes required; unsupported validation rejected, prior-state reconciliation required, rehearsal not run. |

These probes inspected instructions and decisions. They are not native-host
routing evaluations, full authored-playbook trials or operational rehearsals.

## Local verification

- Baseline on `bda1eac`: 319 tests passed.
- Targeted skill, provenance and release contracts after corrections: 78 passed.
- Full final suite: 319 tests passed in 18.636 seconds.
- Plugin validator, Claude strict validation, both skill quick validators,
  Python compilation, shell syntax and whitespace checks: passed.
- Plugin source audit: passed for all six pinned upstream roots.
- Packaging and disposable clean installation: pending committed-source check.

The first full implementation run exposed two expected integration gaps in the
new provenance declarations: notice coverage and the fixed source inventory.
Notices and test expectations were updated for the two new MIT sources. The
full-permission check now normalizes typographic quotation marks while retaining
all license words and requiring one complete permission notice per source.
Five routing fixtures were added to the existing matrix; structural fixture
checks do not establish live model behavior.

## Acceptance trace

- AC-001/002: phase-specific need assessment in Specify/Plan and OpenSpec
  proposal/design, with template prompts and a shared two-class policy.
- AC-003: task dependencies and executor obligations before operation/delivery.
- AC-004: authoring skill and playbook template; conditional normal/incident paths.
- AC-005: reviewer, evidence template and stale-evidence policy.
- AC-006: convergence/archival evidence gates; read-only convergence correction.
- AC-007: direct supporting-skill route and explicit small-edit exclusion.
- AC-008: existing directory discovery, pinned provenance and local checks.

## Limits

No remote publication, persistent host installation, paid native model evaluation
or real system operation was performed. Fixed release 0.1.1 and its historical
acceptance claims are unchanged. Review and rehearsal facts remain separate;
this feature does not guarantee compliance by every host/model.
