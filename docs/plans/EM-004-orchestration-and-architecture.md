# EM-004 Orchestration and Architecture Implementation Plan

> **For agentic workers:** Bootstrap with `superpowers:subagent-driven-development`; use the new `orchestrated-implementation` skill for its own acceptance fixture once available. A strong coordinator owns all interface and integration decisions.

**Goal:** Add efficient model-aware subagent execution, compaction-safe implementation slices, UML-based architecture analysis, and a system-architect integration gate for large work.

**Architecture:** One large-feature executor consumes Spec Kit tasks and delegates bounded slices through host adapters. EM-002 continuity state is its durable recovery layer. Architecture modeling runs before task generation and again against the as-built system before convergence.

**Tech Stack:** Agent Skills and Markdown policies/templates, Mermaid, Python 3.11+ standard-library contract and fixture tests.

**Spec:** `docs/specs/2026-09-04-engineering-method-design.md`

## Global Constraints

- `orchestrated-implementation` is the only large-feature executor.
- The strongest available coordinator retains architecture, cross-slice state, integration, and acceptance responsibility.
- Use capability roles `strong`, `standard`, and `fast`; provider IDs appear only in platform adapters.
- Parallel writes require disjoint file/interface ownership and safe isolation. Otherwise serialize writes.
- Review by a separate agent is required for risky or integration-bearing slices, not every mechanical edit.
- Actionable defects are fixed or reported as concrete blockers; they are never silently parked.
- Every dispatch, slice, review, fix, long wait, and phase transition uses EM-002 checkpoints.
- UML applies only to large features, architecture, substantial migrations, or cross-component concurrency/security/data-integrity work.

### Task 1: EM-004.1 Define model roles and host-neutral agent briefs

**Files:**

- Create: `shared/policies/{model-routing,orchestration,defect-convergence,continuity-contract}.md`
- Create: `shared/agent-roles/{implementer,debugger,reviewer,system-architect}.md`
- Create: `templates/orchestration/{slice-brief,agent-report,review-report,resume}.md`
- Create: `tests/test_orchestration_contract.py`

**Role contract:** EM-004 defines only the host-neutral `strong`, `standard`,
and `fast` semantics. The concrete Codex and Claude mappings approved in the
design are implemented exclusively by the platform adapters in EM-005.

- [ ] Write red tests requiring exactly the three semantic roles in common policies, no provider model IDs in common `skills/`, and the four agent briefs with explicit input/output contracts.
- [ ] Require every agent report to return `status`, `work_id`, `slice_id`, commits/files, tests with command and result, root-cause/fix findings, concerns, and next dependency facts.
- [ ] Define host-neutral runtime selection requirements: inspect the host's actual available models through its later adapter, choose the preferred tier, fall back once per next lower available tier, and record the fallback. Never claim the main model changed if the host cannot change it.
- [ ] Define delegation economics: use fast only for fully specified mechanical work; standard for normal multi-file work/review; strong for design judgment, difficult debugging, integration, and final review. Optimize completed-task turns rather than token price alone.
- [ ] Re-run tests and commit with `git commit -m "feat: add model roles and agent contracts"`.

### Task 2: EM-004.2 Build cohesive-slice orchestration

**Files:**

- Create: `skills/orchestrated-implementation/SKILL.md`
- Create: `scripts/{task-brief,review-package}`
- Create: `tests/test_orchestrated_implementation.py`
- Modify: `third-party/sources.lock.json`, `THIRD_PARTY_NOTICES.md`

**Pinned Superpowers references:**

- `skills/subagent-driven-development/SKILL.md`
- `implementer-prompt.md`
- `task-reviewer-prompt.md`
- `re-review-prompt.md`
- `scripts/task-brief`
- `scripts/review-package`
- `scripts/sdd-workspace`

- [ ] Write red tests that the skill consumes a Spec Kit `tasks.md`, architecture findings, work ID, and project gates; it cannot trigger for small changes or OpenSpec apply.
- [ ] Test slice grouping: adjacent tiny same-shape tasks batch; tasks sharing an interface remain serial; independent disjoint ownership may be parallel only with isolation.
- [ ] Test the review rule: mechanical slice permits coordinator review; security, migration, interface, concurrency, and cross-component slices require independent review.
- [ ] Adapt file-backed task briefs, reports, complete-range diff packages, fix/re-review mechanics, and recovery ledger concepts. Replace `.superpowers/sdd/` with `.engineering-method/runs/<work-id>/` and call the EM-002 continuity interface rather than creating duplicate state logic.
- [ ] The coordinator writes a checkpoint before and after dispatch, after implementation/test/review/fix, before long waits, and at handoff. Subagents write only their named report file.
- [ ] Do not copy the original one-agent-per-task rule, five-round breaker, parked real defects, mandatory review of every trivial task, or ban on all parallel implementation.
- [ ] Update source mappings for every adapted file and run contract plus provenance tests.
- [ ] Commit with `git commit -m "feat: add efficient orchestrated implementation"`.

### Task 3: EM-004.3 Implement evidence-driven defect convergence

**Files:** Modify `skills/orchestrated-implementation/SKILL.md`, `shared/policies/defect-convergence.md`, agent briefs, and `tests/test_orchestrated_implementation.py`.

- [ ] Write red tests for this escalation sequence: precise finding to original implementer; root-cause statement and covering test; after two ineffective attempts use fresh/stronger agent; repeated local failure invokes interface/architecture analysis.
- [ ] Require every retry to add new evidence, a new hypothesis, a changed approach, or a model/perspective escalation. Reject identical retry briefs.
- [ ] Require the narrowest meaningful tests after each fix and broader tests only for integration-affecting fixes or integration boundaries.
- [ ] Define terminal conditions: all actionable findings resolved, or a recorded external blocker, missing authorization, unsafe irreversible operation, or specification contradiction that makes further action guesswork.
- [ ] Re-run focused tests and commit with `git commit -m "feat: add evidence-driven fix convergence"`.

### Task 4: EM-004.4 Create the original architecture-modeling skill

**Files:**

- Create: `skills/architecture-modeling/SKILL.md`
- Create: `shared/policies/architecture-gate.md`
- Create: `templates/uml/{README,diagram-metadata}.md`
- Create: `templates/uml/{component,sequence,state,activity,deployment}.mmd`
- Create: `tests/test_architecture_gate.py`

- [ ] Write red activation tests for the five allowed categories and negative cases for small fixes, localized Brownfield changes, docs, and mechanical refactors.
- [ ] Require only diagrams that answer a named design or verification question. Each diagram records purpose, source evidence, requirement IDs, notation, and verification date.
- [ ] Make Mermaid the dependency-free default. PlantUML is allowed only when it adds material modeling value and a validator is available; the skill has no dependency on the generic local UML skill.
- [ ] Require design-time analysis for ownership, interface mismatch, cycles, invalid/unreachable states, failure/rollback gaps, ordering/races, trust boundaries, and migration consistency.
- [ ] Before `speckit-tasks`, write findings to `docs/uml/findings.md`. After implementation, reconcile diagrams against code and record each difference as code-corrected, diagram-corrected with rationale, or unresolved defect.
- [ ] Re-run architecture tests and commit with `git commit -m "feat: add UML architecture gate"`.

### Task 5: EM-004.5 Add system-architect integration verification

**Files:**

- Modify: `skills/architecture-modeling/SKILL.md`, `shared/agent-roles/system-architect.md`
- Create: `templates/uml/integration-test-plan.md`
- Create: `tests/fixtures/large-feature/` fixture project and expected artifacts
- Create: `tests/test_large_feature_fixture.py`

**Fixture scenario:** A small checkout workflow whose order component expects `reserve(order_id) -> Reservation` while inventory initially returns `bool`, and whose payment-success/inventory-commit-failure path initially omits inventory release/payment reversal. These are the two required architecture-detectable defects.

- [ ] Create a red fixture assertion proving the initial component/sequence/state evidence exposes the interface mismatch and missing compensation path.
- [ ] Require architecture analysis to turn both findings into normal Spec Kit tasks before implementation.
- [ ] Require as-built component, success-sequence, recovery-sequence, and state diagrams to match implemented interfaces and flows.
- [ ] Require the system architect to derive at least one cross-component success integration test and one recovery/rollback integration test from those diagrams.
- [ ] Assert `speckit-converge` cannot complete without as-built reconciliation, passing derived integration tests, clean final review, and fresh verification evidence.
- [ ] Re-run the fixture and all unit tests; commit with `git commit -m "test: add architecture-led integration gate"`.

### Task 6: EM-004.6 Prove compaction and agent-lifecycle recovery

**Files:** Create `tests/test_orchestration_recovery.py`; modify orchestration/continuity contracts and `BACKLOG.md`.

- [ ] Simulate compaction after each checkpoint boundary: before dispatch, active agent, completed agent before integration, failed verification, mid-fix, post-slice, pre-converge, and final handoff.
- [ ] Assert recovery validates git/artifacts/canonical work, never redispatches a completed slice, marks unavailable active agents redispatchable, and resumes exactly the recorded next action.
- [ ] Assert downstream agentic-RAG recall can supply only a work ID and pointers; stale recalled values cannot override repository evidence.
- [ ] Run:

  ```bash
  python3 -m unittest tests.test_orchestration_contract tests.test_orchestrated_implementation tests.test_architecture_gate tests.test_large_feature_fixture tests.test_orchestration_recovery -v
  python3 scripts/validate-plugin
  git diff --check
  ```

- [ ] Update `BACKLOG.md`: mark `EM-004` complete after fresh acceptance evidence.
- [ ] Commit with `git commit -m "test: verify orchestration continuity"`.

## EM-004 Acceptance Evidence

- Complex work uses one strong coordinator and cost-appropriate subagents.
- Independent work gains parallelism without conflicting shared writes.
- Reviews are slice- and risk-proportionate.
- Defect loops require progress and do not discard actionable bugs.
- Relevant UML findings shape tasks before code and integration tests afterward.
- Recovery survives every modeled compaction boundary without duplicate execution.
