# Engineering playbook integration

Shared policy and templates are bundled from Method Core.


- `speckit-specify`: identify system-deliverable playbooks from user and operating
  scenarios, including preventive recovery. Record scope and acceptance criteria.
- `speckit-plan` and design-time `architecture-modeling`: assess development
  operations and refine system needs against dependencies and failure modes.
  Material additions to delivery scope return to the specification owner.
- `openspec-propose`: perform both assessments in proposal/delta and design;
  include affected existing playbooks and their compatibility changes.
- `speckit-tasks` or OpenSpec tasks: add authoring, review and required rehearsal
  tasks with explicit dependencies. Development readiness blocks the operation;
  system readiness blocks delivery. Ordinary task planning remains unchanged.
- `orchestrated-implementation` and `openspec-apply`: invoke `playbook-authoring`
  for assigned artifacts and `playbook-review` before use/acceptance. Track fixes
  in the same work ID. Coordinate authorized rehearsals and preserve evidence.
- As-built `architecture-modeling`: check playbook assumptions against actual
  interfaces and relevant recovery flows; flag stale evidence for affected paths.
- `speckit-converge` and `openspec-archive`: check every required playbook against
  the need inventory, current artifact/system revision, review and required
  rehearsal evidence. Missing or stale proof blocks completion. Return findings
  to the existing executor; do not execute or repair procedures in the gate.

Direct authoring/review requests use the supporting skill without creating an
engineering lifecycle solely for a document. If the request changes system
behavior, the appropriate engineering lifecycle owns that change.

