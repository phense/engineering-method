# Feature Specification: Engineering playbooks

## Stable work ID

- Feature ID: EM-014
- Status: Approved for implementation by the user
- Source request: Integrate the selected author and reviewer skills, with need assessment for development playbooks and playbooks delivered with a new system. Keep the existing documentation subsystem outside this change.

## User scenarios

### US-001: Identify justified playbooks (Priority: P1)

The engineering lifecycle identifies a development operation requiring a playbook and a system usage or operations scenario requiring a delivered playbook independently. A simple reversible task needs neither.

### US-002: Produce and accept usable playbooks (Priority: P1)

An author creates a source-grounded procedure and a reviewer checks it without hidden context. Acceptance distinguishes drafting, review and practical rehearsal.

## Acceptance criteria

- AC-001: Specify and OpenSpec proposal record system-deliverable needs from planned usage and risks, including preventive recovery before an incident occurs.
- AC-002: Plan and OpenSpec design assess development operations, with each required playbook linked to its owning operation and a readiness deadline.
- AC-003: Tasks and implementation require a development playbook before its operation; system playbooks are delivery tasks. Existing executor ownership is preserved.
- AC-004: Authoring covers applicability, prerequisites, decisions, expected evidence, failure handling, interruption/resume, rollback or irreversibility, escalation and completion without inventing system facts.
- AC-005: Review identifies missing evidence and separates content review from rehearsal at a named artifact/system revision and environment. Material changes invalidate affected evidence.
- AC-006: Convergence and OpenSpec archival refuse completion when required playbooks, current reviews or required rehearsals are missing; fixes return to the owning executor.
- AC-007: Small edits avoid mandatory playbooks; direct author/review requests do not start a second engineering lifecycle or execute the procedure.
- AC-008: Pinned upstream revisions, source and destination hashes, full license notices, portable discovery and existing workflows remain valid.

## Compatibility boundaries

No runtime execution engine, network publication, host installation, model-policy change or documentation-lifecycle redesign. Existing permissions govern every rehearsal; creating a procedure grants no execution authority.

## Interface contracts

The lifecycle owns need decisions, tasks and acceptance. Supporting author/reviewer skills own only the assigned playbook and evidence files. Stable playbook IDs link both artifact classes to requirements and tasks.

## Edge cases

Both classes may be required for one feature; link shared procedures without duplicating them. Unknown system facts remain explicit blockers. A content review does not certify execution. A planned system need is valid evidence before production exists.

## Success measures

All acceptance criteria have traceable instruction or fixture evidence; local validators and regression suite pass; independent review has no unresolved material findings. Native paid routing evaluation is outside this implementation acceptance.
