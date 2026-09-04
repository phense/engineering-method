# EM-003 Curated Workflow Skills Implementation Plan

> **For agentic workers:** Use `superpowers:subagent-driven-development` after EM-001. Adapt only the pinned files named below, preserve attribution, and test every trigger boundary before accepting a skill.

**Goal:** Build one shared skill tree whose primary lifecycles do not overlap and whose supporting quality skills have narrow, composable responsibilities.

**Architecture:** Spec Kit owns large-feature specification, planning, task generation, and convergence. OpenSpec owns bounded Brownfield deltas. Superpowers-derived skills own debugging, TDD, verification, reviews, isolation, and independent parallel work. Host syntax and model IDs are excluded from all common skills.

**Tech Stack:** Markdown Agent Skills, JSON fixtures, Python 3.11+ standard-library contract tests.

**Spec:** `docs/specs/2026-09-04-engineering-method-design.md`

## Global Constraints

- Exactly one primary lifecycle may own a request.
- Descriptions contain a positive trigger and the closest negative boundary.
- Every primary skill names its input artifact, output artifact, completion condition, one next phase, and allowed supporting skills.
- No central router, upstream CLI call, store/profile mechanism, hook framework, branch-creation command, or duplicate implementation executor.
- Lifecycle handoffs use semantic skill names; invocation syntax belongs in platform adapters.
- Planning skills never edit application code.
- Update `third-party/sources.lock.json` and `THIRD_PARTY_NOTICES.md` in the same commit as every adapted file.

## Pinned Sources

| Family | Revision | Selected source paths |
|---|---|---|
| Spec Kit | `df6b3187022ce986759bd854467e8a4bb56bb0f4` | `templates/commands/specify.md`, `plan.md`, `tasks.md`, `converge.md`; `templates/spec-template.md`, `plan-template.md`, `tasks-template.md` |
| OpenSpec | `e062b9572be933564ba3899d059377dfa1393e32` | `skills/openspec-propose/SKILL.md`, `openspec-apply-change/SKILL.md`, `openspec-archive-change/SKILL.md`, `schemas/spec-driven/templates/spec.md` |
| Superpowers | `b36e0829c6d0140e93cfef2ca599b1b07d4a7797` | Identically named selected skill folders plus `requesting-code-review/code-reviewer.md`; SDD materials are reserved for EM-004 |

### Task 1: EM-003.1 Define lifecycle contracts and artifact templates

**Files:**

- Create: `shared/policies/{authority-order,lifecycle-selection,lifecycle-handoffs,workflow-depth}.md`
- Create: `templates/spec-kit/{spec,plan,tasks}.md`
- Create: `templates/openspec/{proposal,design,tasks}.md`
- Create: `tests/test_skill_contracts.py`
- Create: `tests/fixtures/trigger-cases/matrix.json`

**Authoritative lifecycle graph:**

```text
systematic-debugging -> test-driven-development -> verification-before-completion
openspec-propose -> openspec-apply -> openspec-archive
speckit-specify -> speckit-plan -> architecture-modeling
                 -> speckit-tasks -> orchestrated-implementation
                 -> speckit-converge -> verification-before-completion
```

- [ ] Write red tests that load every future primary skill and require machine-readable headings `Trigger`, `Do not use for`, `Consumes`, `Produces`, `Completion`, `Next phase`, and `Supporting skills`.
- [ ] Test that the lifecycle graph has no second executor, no cycle, and no edge from an OpenSpec artifact to a Spec Kit phase except the formal escalation record.
- [ ] Test templates for required acceptance criteria, compatibility boundaries, interface contracts, dependencies, tests, architecture findings, and stable work IDs.
- [ ] Run `python3 -m unittest tests.test_skill_contracts -v`. Expected red result: missing policies/templates/skills.
- [ ] Write the four concise shared policies and six adapted templates. Remove Spec Kit hook/extension machinery and OpenSpec CLI/schema/store assumptions.
- [ ] Create JSON trigger cases for trivial edit, reproducible defect, bounded behavior delta, multi-component feature, architecture migration, existing artifacts, received review, independent failures, and completion without evidence.
- [ ] Re-run focused tests as far as the existing files allow; missing lifecycle skills remain the only expected failures.
- [ ] Commit with `git commit -m "feat: add lifecycle contracts and artifact templates"`.

### Task 2: EM-003.2 Adapt the Spec Kit lifecycle

**Files:** Create `skills/speckit-{specify,plan,tasks,converge}/SKILL.md`; modify provenance and contract tests.

**Boundaries and outputs:**

- `speckit-specify` triggers only for new capabilities, cross-component features, architecture, risky migrations, or material unresolved design. It creates `specs/<stable-feature-id>-<name>/spec.md` and must exclude defects and localized Brownfield deltas.
- `speckit-plan` consumes that spec and produces `plan.md` plus only the research, data-model, contract, and quickstart artifacts actually needed. It hands off to `architecture-modeling` for large work.
- `speckit-tasks` consumes plan plus UML findings and produces dependency-ordered, cohesive-slice-ready `tasks.md`. Architecture findings become tasks before implementation.
- `speckit-converge` consumes current code, spec, plan, tasks, as-built UML, integration results, review state, and fresh verification. It appends traceable gaps and refuses completion while actionable findings remain.

- [ ] Add failing contract tests for the four descriptions, planning-only scope, exact artifacts, prohibited hooks/CLI strings, required continuity preamble, and handoff graph.
- [ ] Adapt the pinned sources by retaining their requirement focus, technical-plan separation, dependency-aware tasks, and append-only convergence semantics. Remove `/implement`, `/analyze`, `/clarify`, task-to-Issue, extension hooks, generated-project scripts, and branch management.
- [ ] Keep `converge` read-only for application code; its only allowed write is appending missing work to `tasks.md`.
- [ ] Add one source-lock mapping per adapted command/template with upstream source hash and destination hash.
- [ ] Run the focused skill tests and `python3 scripts/validate-plugin`.
- [ ] Commit with `git commit -m "feat: add curated Spec Kit lifecycle"`.

### Task 3: EM-003.3 Adapt the OpenSpec Brownfield lifecycle

**Files:** Create `skills/openspec-{propose,apply,archive}/SKILL.md`; create `templates/openspec/escalation.md`; modify tests and provenance.

**Artifact layout:**

```text
openspec/
├── specs/<capability>/spec.md
└── changes/<change-id>/
    ├── proposal.md
    ├── design.md
    ├── tasks.md
    ├── specs/<capability>/spec.md
    └── escalation.md   # only when formally escalated
```

- [ ] Write red tests proving `propose` is planning-only, `apply` is the sole Brownfield executor, and `archive` requires completed tasks plus fresh verification.
- [ ] Test the closest negative boundaries: defects go to debugging; new subsystem, architecture, risky migration, and tightly coupled multi-component work go to Spec Kit.
- [ ] Adapt proposal/apply/archive discipline from the pinned skills while removing every `openspec` executable call, store/profile/schema selection, dynamic instructions JSON, and dependency on other OpenSpec skills.
- [ ] Formal escalation writes `escalation.md` with reason, preserved change path, new Spec Kit feature ID/path, and `status: escalated`; the OpenSpec executor then becomes inactive.
- [ ] Archive synchronizes accepted delta requirements into `openspec/specs/<capability>/spec.md`, moves the completed change under `openspec/changes/archive/YYYY-MM-DD-<change-id>/`, and never proceeds with incomplete tasks or failed verification.
- [ ] Update lock mappings and notices; run focused tests and portable validation.
- [ ] Commit with `git commit -m "feat: add bounded OpenSpec lifecycle"`.

### Task 4: EM-003.4 Port debugging, TDD, and verification

**Files:**

- Create: `skills/systematic-debugging/` with `SKILL.md`, `root-cause-tracing.md`, `defense-in-depth.md`, and `condition-based-waiting.md` only when retained text is actually referenced.
- Create: `skills/test-driven-development/SKILL.md` and `writing-good-tests.md` only when referenced.
- Create: `skills/verification-before-completion/SKILL.md`.
- Modify: tests and provenance.

- [ ] Write red boundary tests: debugging requires observed failure; TDD applies to testable behavior but not documentation or meaningless implementation-mirroring tests; verification triggers before any pass/fix/completion claim and requires fresh output.
- [ ] Adapt root-cause-first debugging, verified red/green TDD, and evidence-before-claims from the pinned Superpowers files. Remove references to omitted Superpowers lifecycle skills and platform-specific tools.
- [ ] Require a formal handoff from debugging to OpenSpec/Spec Kit only when evidence establishes an intentional contract or architecture change.
- [ ] Update provenance for every retained/adapted file and run focused tests.
- [ ] Commit with `git commit -m "feat: add debugging TDD and verification skills"`.

### Task 5: EM-003.5 Port review, worktree, and parallel-dispatch support

**Files:**

- Create: `skills/requesting-code-review/{SKILL,code-reviewer}.md`
- Create: `skills/receiving-code-review/SKILL.md`
- Create: `skills/using-git-worktrees/SKILL.md`
- Create: `skills/dispatching-parallel-agents/SKILL.md`
- Modify: tests and provenance.

- [ ] Write red tests requiring risk-proportionate independent review, technical verification of received feedback, native-worktree preference with safe fallback, and parallel dispatch only after independence is established.
- [ ] Adapt the pinned skills. Mechanical slices may use coordinator review; risky/integration-bearing slices require an independent reviewer.
- [ ] Preserve the worktree environment checks and destructive-path guards while expressing host operations semantically.
- [ ] Permit parallel read-only investigation for independent domains. Parallel writes require disjoint ownership and safe isolation; otherwise serialize them.
- [ ] Remove calls to `finishing-a-development-branch`, `using-superpowers`, or any missing skill.
- [ ] Update provenance; run the complete skill-contract suite and plugin validator.
- [ ] Commit with `git commit -m "feat: add review isolation and parallel skills"`.

### Task 6: EM-003.6 Add the project-backlog support skill and collision acceptance

**Files:** Modify `skills/project-backlog/SKILL.md`, `tests/test_skill_contracts.py`, the trigger matrix, and `BACKLOG.md`.

- [ ] Write red tests that `project-backlog` owns only initialization, stable-ID updates, blocker ordering, `FEATURES.md` handoff, automatic GitHub-mode detection, cache refresh, and continuity pointers. It must never classify or control implementation methodology.
- [ ] Require every stateful lifecycle skill to invoke the shared recovery preamble and update backlog state at work start, scope change, blocker, completed slice, and handoff.
- [ ] Evaluate all matrix rows structurally: one primary lifecycle, expected supporting skills, prohibited controllers, and artifact-state handoffs.
- [ ] Run:

  ```bash
  python3 -m unittest tests.test_skill_contracts -v
  python3 scripts/validate-plugin
  git diff --check
  ```

- [ ] Update `BACKLOG.md`: mark `EM-003` complete only after all skill and provenance checks pass.
- [ ] Commit with `git commit -m "test: enforce non-overlapping workflow skills"`.

## EM-003 Acceptance Evidence

- All selected skills are discoverable from one shared tree.
- No primary lifecycle has overlapping positive triggers or a second implementation owner.
- Artifact-state handoffs form the approved graph.
- No common skill contains Codex/Claude invocation syntax or provider model IDs.
- No adapted skill requires an upstream CLI or omitted workflow skill.
- Every derived file has a pinned source and consistent MIT attribution.
