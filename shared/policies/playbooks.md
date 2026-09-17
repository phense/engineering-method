# Engineering Playbooks

A playbook is a scenario-bound procedure with decisions, observable outcomes and
failure paths. A task list or design explanation alone is not a playbook.
Playbooks support the current engineering lifecycle; they do not create another
controller, executor or documentation work ID. Apply [proportionality](proportionality.md).

## Decide whether one is needed

Assess these two classes independently using requirements, architecture, planned
operations and actual system evidence. A prior incident is not required.

| Class | Create when | Deadline and lifetime |
|---|---|---|
| Development | A multi-step development operation affects live systems/data, crosses coordinated actors/environments, or needs nontrivial decisions, interruption recovery or rollback. Examples: cutover, staged migration, coordinated release. | Reviewed and rehearsed to the agreed risk level before the operation; retain evidence, then archive if no longer needed. |
| System | Successful use, operation or recovery depends on a recurring or high-consequence procedure the delivered system does not fully perform itself. Examples: onboarding with decisions, import recovery, backup restoration. | Included in delivery acceptance; maintained with the system and its interfaces. |

A simple reversible edit, self-explanatory action, fully automated operation
with adequate built-in handling, or ordinary task sequence does not by itself
justify a playbook. Automation may still require an operator recovery playbook.
Do not generate speculative catalogs. Record a concise `none` with rationale in
the owning spec/plan when the assessment finds no need. Reassess when scope,
interfaces, operational risk or recovery assumptions change.

## Record the decision in the owning artifacts

Use stable playbook IDs. For each required playbook record: class, scenario and
trigger, source requirement/risk, audience, owner, canonical path, dependent
operation or delivery task, readiness deadline, acceptance criteria and required
validation level/environment. If one procedure serves both classes, record both
obligations and link one canonical procedure; the earlier deadline still applies.
A system obligation cannot be archived merely because development ended.

Follow an existing repository convention. Otherwise use
`docs/playbooks/development/<id>.md` and `docs/playbooks/system/<id>.md`, with
review and rehearsal evidence beside them as `<id>-review.md`. These are output
paths in the target project, not files inside the plugin installation.

## Lifecycle integration

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

## Evidence and acceptance

Keep three separate facts, not one overloaded status:

1. **Drafted:** source-grounded procedure exists, with unresolved facts explicit.
2. **Reviewed:** content assessed at a named artifact revision; findings recorded.
3. **Rehearsed:** authorized execution or simulation recorded with artifact and
   system revision, environment, date, method, tested branches and actual results.

A review score, valid Markdown, successful generation or an example output is
not rehearsal evidence. Never fill `last_validated` with the creation date.
Choose the required validation level during planning in proportion to risk;
a tabletop exercise does not prove a live recovery. Record untested branches
and environmental limits. If a required rehearsal is unavailable, preserve the
blocker; only an explicit acceptance-scope decision by the authorized owner can
change that requirement, and it must not be labeled as a successful test.

An applicable command, interface, permission, dependency or failure-path change
invalidates affected review/rehearsal evidence until rechecked. A prose-only edit
may reuse evidence with a recorded rationale; do not relabel it as fresh execution.

## Authority and continuity

Authoring or reviewing a playbook does not authorize executing it. A rehearsal
uses existing project permissions, target/environment checks and risk controls;
never introduce blanket reapproval where authority already exists. State any
irreversible boundary and the alternative to rollback before the relevant step.

The owning coordinator uses `project-backlog` recovery, events and checkpoints
for tracked work. Supporting skills return artifact/evidence paths and findings;
they never independently change lifecycle phase or canonical task state. On
resume, read those artifacts and current system evidence before continuing.
