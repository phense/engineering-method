# Peter's Engineering Method: Consolidated Workflow Plugin

**Date:** 2026-09-04  
**Status:** Design approved in conversation; awaiting written-spec review

## 1. Purpose

Peter's Engineering Method is a self-contained, open-source workflow plugin for Codex and Claude. It combines selected, non-overlapping parts of GitHub Spec Kit, OpenSpec, and Superpowers with project-state management and an architecture-level verification gate.

The plugin must keep small changes fast while applying deeper specification, delegation, review, UML analysis, and integration testing only when the work warrants them. Users describe the engineering outcome; they do not choose a methodology or route work manually.

## 2. Goals

- Install the same skill set directly in Codex and Claude.
- Select one primary lifecycle automatically from mutually exclusive skill descriptions and artifact state.
- Avoid overlapping brainstorming, specification, planning, and implementation controllers.
- Execute complex plans with a strong coordinating model and appropriately selected subagents.
- Fix actionable defects before completion without wasting time on repetitive, evidence-free loops.
- Survive context compaction and session recovery without repeating completed work or losing workflow state.
- Maintain a stable, blocker-first project backlog locally and migrate cleanly to GitHub Issues.
- Use architecture models and system-level integration tests to validate large features.
- Preserve project-specific gates and use agentic RAG and host memories only as supporting context.
- Be redistributable under a clear license with complete third-party attribution.

## 3. Non-goals

- Repackage the complete Spec Kit, OpenSpec, or Superpowers methodologies.
- Require any upstream CLI or plugin at runtime.
- Add a central workflow router that competes with individual skills.
- Force specs, plans, UML diagrams, worktrees, subagents, or broad test suites onto trivial changes.
- Support coding hosts other than Codex and Claude in the first release.
- Push branches, publish releases, or mutate remote repositories without the authority normally required for those actions.
- Treat memory as more authoritative than repository state, tests, specifications, or project rules.

## 4. Design Principles

1. **One responsibility per skill.** Each skill has a distinct entry condition, responsibility, output, and handoff.
2. **One primary lifecycle per request.** A feature lifecycle, Brownfield change, or bug workflow may use supporting quality skills, but two primary lifecycles never control the same work.
3. **Depth follows risk.** Reversibility, architectural reach, ambiguity, data risk, security impact, and integration surface determine the amount of process.
4. **Evidence drives retries.** A failed fix is followed by a new hypothesis, new evidence, a fresh perspective, or a stronger model—not the same attempt again.
5. **The coordinator owns integration.** Subagents complete bounded work; the strongest coordinating agent retains cross-component and acceptance responsibility.
6. **Project truth is durable.** Backlog, issues, specs, diagrams, tests, and git history carry state across sessions and context compaction.
7. **Shared core, thin adapters.** Workflow semantics remain identical across Codex and Claude; only host mechanics and model identifiers differ.
8. **Continuity is composable.** The workflow persists a host-neutral recovery contract that works alone and can feed agentic RAG or another continuity provider.

## 5. Selected Method Components

### 5.1 GitHub Spec Kit

Adapt and include:

- `specify`
- `plan`
- `tasks`
- `converge`

Do not include Spec Kit's implementation executor as a separate skill. Complex Spec Kit task execution is owned by `orchestrated-implementation`, avoiding two competing executors.

Spec Kit is the primary lifecycle for new capabilities, multi-component features, architectural changes, risky migrations, and work with substantial unresolved design.

### 5.2 OpenSpec

Adapt and include:

- `propose`
- `apply`
- `archive`

OpenSpec is the primary lifecycle for intentional, bounded changes to existing behavior. Its artifacts describe the delta rather than respecifying the existing system.

An OpenSpec change is escalated to Spec Kit if discovery reveals a new subsystem, multiple tightly coupled component boundaries, a high-risk migration, or architectural uncertainty that cannot be contained in a change delta.

### 5.3 Superpowers

Port or adapt:

- `systematic-debugging`
- `test-driven-development`
- `verification-before-completion`
- `requesting-code-review`
- `receiving-code-review`
- `using-git-worktrees`
- `dispatching-parallel-agents`
- the useful orchestration mechanics of `subagent-driven-development`

Do not include:

- `using-superpowers`
- `brainstorming`
- `writing-plans`
- `executing-plans`
- the original `subagent-driven-development` skill unchanged
- other Superpowers lifecycle controllers that overlap with Spec Kit or OpenSpec

The original subagent-driven workflow is too expensive as the default because it assigns a fresh implementer and a separate review cycle to every plan task. The adapted executor groups work into cohesive implementation slices, batches small same-shape changes, and applies reviews according to risk.

### 5.4 Original Components

Create project-specific skills for:

- `orchestrated-implementation`
- `architecture-modeling`
- `project-backlog`

The architecture skill should be written for this plugin rather than copied from the generic local UML skill. It must contain only the diagram selection, verification, and architecture-analysis guidance required by this method and must not depend on an unavailable documentation-management skill.

## 6. Automatic Skill Selection Without a Router

Automatic selection relies on discriminating frontmatter descriptions, negative boundaries, current artifacts, and explicit handoffs.

### 6.1 Primary lifecycle entry conditions

| Condition | Primary skill | Exclusions |
|---|---|---|
| Observed failure, test regression, or unexplained behavior | `systematic-debugging` | Not used for a deliberate behavior change without a defect |
| Bounded intentional change to an existing capability | `openspec-propose` | Not used for pure bug repair, a new subsystem, or architectural redesign |
| New capability, cross-component feature, architecture, or risky migration | `speckit-specify` | Not used for a localized Brownfield delta or ordinary bug |
| Existing Spec Kit artifact awaiting its next phase | Matching Spec Kit skill | Never starts an OpenSpec lifecycle for the same work |
| Existing OpenSpec change awaiting its next phase | Matching OpenSpec skill | Never starts a Spec Kit lifecycle unless formally escalated |
| Small reversible change with no behavioral contract impact | Native focused edit | No spec, plan, UML, or orchestrated implementation |

Descriptions must include both positive triggers and the closest negative boundary because model-driven skill discovery sees descriptions before it loads full instructions.

### 6.2 Supporting skills

Supporting skills do not compete for lifecycle ownership:

- TDD controls how testable behavior is implemented.
- Verification controls what evidence is required before completion claims.
- Worktrees control isolation.
- Review skills control review production and review-feedback handling.
- Parallel-agent dispatch controls independent investigations or safely isolated work.
- Project backlog controls durable task state.
- Architecture modeling is a gate invoked only by the large-feature lifecycle.

### 6.3 Handoffs

Each lifecycle skill declares:

- its required input artifact,
- the artifact it creates or updates,
- its completion condition,
- the one valid next lifecycle phase,
- the supporting skills it may invoke.

Handoffs use semantic skill names in the shared core. Host-specific syntax belongs only in the Codex and Claude adapters.

## 7. Workflow Depth

### 7.1 Small change

```text
read project gates -> create/update backlog item -> make focused change
-> targeted verification -> complete backlog item
```

No specification, plan, UML, or subagent is required. TDD applies only when the change affects behavior for which a meaningful test can be written.

### 7.2 Bugfix

```text
systematic debugging -> reproduce root cause -> create failing regression test
-> TDD fix -> targeted verification -> complete backlog item
```

Independent failure domains may be investigated in parallel. Failures that may share a root cause stay together until independence is established.

If the root cause shows that the requested result is a deliberate contract change rather than a defect, the work enters OpenSpec or Spec Kit as appropriate.

### 7.3 Bounded Brownfield change

```text
OpenSpec propose -> OpenSpec apply with TDD
-> targeted fix and verification loops -> OpenSpec archive
```

The proposal describes only changed requirements, compatibility boundaries, design choices, and executable tasks.

### 7.4 Large feature or architecture change

```text
Spec Kit specify -> Spec Kit plan -> architecture/UML analysis
-> Spec Kit tasks -> isolated orchestrated implementation
-> as-built UML reconciliation -> system integration testing
-> Spec Kit converge -> final review and verification
```

The lifecycle may add clarification or analysis work only when concrete ambiguity or inconsistency warrants it. Those checks are internal decisions within the relevant phase, not additional competing lifecycle skills.

## 8. Orchestrated Implementation

### 8.1 Coordinator

For complex work, the main coordinator uses the strongest available model class. It owns:

- the approved specification and acceptance criteria,
- architecture and interface decisions,
- decomposition into cohesive slices,
- assignment and model selection,
- integration of subagent work,
- backlog and execution-ledger continuity,
- final system behavior.

If the host cannot change the current main model programmatically, the workflow delegates architecture-critical judgment to a `strong` agent and keeps the main context as the durable coordinator. The plugin must not falsely claim that it changed the host's selected main model.

### 8.2 Model roles

The shared workflow uses capability roles rather than hard-coded provider names:

| Role | Work |
|---|---|
| `strong` | Architecture, decomposition, difficult debugging, integration review, final review |
| `standard` | Multi-file implementation with clear interfaces, ordinary code review |
| `fast` | Mechanical edits, fully specified isolated functions, targeted test execution |

Initial platform mappings:

| Role | Codex | Claude |
|---|---|---|
| `strong` | `gpt-5.6-sol` | `claude-fable-5-1`, then `claude-opus-5` |
| `standard` | `gpt-5.6-terra` | `claude-sonnet-5` |
| `fast` | `gpt-5.6-luna` | `claude-haiku-4-5-20251001` |

Adapters resolve availability at runtime and fall back to the strongest available lower tier without asking the user to choose a method. Model mappings are versioned configuration, not duplicated throughout skills.

### 8.3 Decomposition and concurrency

- Divide plans into cohesive slices with an independently verifiable outcome.
- Batch tiny same-shape changes into one slice.
- Use subagents when context isolation, parallelism, specialization, or a lower-cost model materially helps.
- Keep tightly coupled changes with the coordinator or one implementation agent.
- Parallelize read-only exploration freely when domains are independent.
- Parallelize writes only when file ownership and interfaces do not overlap and the host provides safe isolation.
- Use worktrees for parallel implementation where supported.
- If safe isolation is unavailable, serialize writes and retain parallelism for research, test diagnosis, and review.
- Subagents do not recursively delegate unless the host explicitly supports it and the coordinator has designed a bounded delegation tree.

### 8.4 Slice loop

For every implementation slice:

1. Record the slice requirements, affected interfaces, dependencies, and acceptance evidence in a file-backed brief.
2. Assign an appropriate model and isolated workspace when needed.
3. Implement with TDD where behavior is testable.
4. Run tests targeted to the changed behavior.
5. Review the complete slice diff against requirements and code quality.
6. Fix all actionable findings.
7. Re-run the affected tests and re-review the fix diff.
8. Integrate only after the slice is clean.
9. Update the backlog and execution ledger.

A separate reviewer is required for risky or integration-bearing slices. Mechanical slices may use coordinator review rather than paying for a separate reviewer.

### 8.5 Defect-convergence loop

Actionable defects are not silently parked as minor findings. Fix rounds continue while there is a materially new hypothesis or new evidence:

1. return the precise finding to the original implementer,
2. require a root-cause explanation and covering test,
3. use a fresh agent or stronger model after two ineffective attempts,
4. invoke architecture or interface analysis when repeated local fixes fail,
5. re-run the narrowest meaningful tests after every fix,
6. broaden testing after integration-affecting fixes and at final boundaries.

The loop stops only when all actionable findings are resolved or when a concrete external blocker, missing authorization, unsafe irreversible action, or specification contradiction makes further progress guesswork. The blocker, evidence, attempts, and required next action are recorded in the canonical task system.

## 9. Architecture Modeling and System Verification

### 9.1 Activation

The architecture gate applies only to:

- large cross-component features,
- new or materially changed system boundaries,
- architectural refactors,
- substantial migrations,
- concurrency, security, or data-integrity changes whose behavior spans components.

It does not apply to small fixes, localized Brownfield changes, documentation, or mechanical refactors.

### 9.2 Design-time diagrams

Create `docs/uml/` and only the diagrams that answer a real design or verification question:

- system context and component diagrams,
- class or domain diagrams,
- sequence diagrams for critical end-to-end and failure flows,
- state diagrams for meaningful lifecycles,
- activity diagrams for complex workflows,
- deployment diagrams when infrastructure topology matters.

Every diagram records its purpose, source evidence, relevant requirements, and last verification date. Mermaid is the dependency-free default for GitHub rendering. PlantUML may be used when its stronger UML notation materially improves the model and an available validator can verify the source.

### 9.3 Design-time analysis

Evaluate diagrams against the plan and repository to find:

- missing ownership or responsibilities,
- contradictory interfaces,
- dependency cycles,
- invalid or unreachable states,
- unhandled failure and rollback paths,
- concurrency and ordering hazards,
- trust-boundary or authorization gaps,
- data consistency and migration gaps.

Findings become normal Spec Kit tasks before implementation begins.

### 9.4 As-built reconciliation

After implementation, update the diagrams to match actual code and verify every modeled interface and critical flow. Differences are either corrected in code, corrected in the diagrams with an explicit rationale, or added as unresolved defects. They are never ignored merely because unit tests pass.

### 9.5 System-architect integration gate

A `strong` system-architect review derives integration tests from the as-built component, sequence, state, and failure-flow models. Tests must exercise the most important cross-component success path and relevant error, rollback, or recovery paths.

Completion requires:

- unit and targeted tests appropriate to each slice,
- the system-level integration tests,
- reconciliation of UML and implementation,
- Spec Kit convergence,
- final code review,
- verification evidence from fresh command output.

## 10. Compact Continuity Contract

Workflow state must survive `/compact`, context-window replacement, agent eviction, and session resumption without relying on chat history or an in-memory todo list.

### 10.1 Durable run state

Each stateful workflow owns a stable work ID derived from its backlog ID, GitHub issue ID, Spec Kit feature ID, or OpenSpec change ID. It stores transient recovery data under:

```text
.engineering-method/
└── runs/
    └── <work-id>/
        ├── state.json
        ├── resume.md
        ├── decisions.md
        ├── agent-reports/
        └── events.jsonl
```

`state.json` uses a versioned schema and records:

- the stable work, backlog, issue, feature, or change identifier,
- active lifecycle and phase,
- current implementation slice,
- paths to the applicable spec, plan, tasks, UML, and reports,
- worktree path, base commit, and last observed head commit,
- completed, active, and pending work,
- active and completed subagent identities,
- open findings and failing checks,
- the latest successful verification command, timestamp, and output digest,
- the exact next action.

`resume.md` is a concise human- and agent-readable recovery brief. Large artifacts and command output are referenced by path and commit rather than copied into it. `decisions.md` contains architecture rulings and their rationale. Subagents write only their own report files; the main coordinator is the sole writer of `state.json`.

The run directory is local execution state and is git-ignored by default. Durable product decisions and unfinished work still belong in committed specifications, the local backlog, or canonical GitHub Issues.

### 10.2 Checkpoint boundaries

Update the run checkpoint:

- before and after every subagent dispatch,
- after every implementation slice,
- after tests, reviews, and fix rounds,
- when a blocker or architecture decision appears,
- before a long wait,
- at every transition between specification, planning, UML, task generation, implementation, convergence, and verification,
- before final handoff.

Do not checkpoint after every tool call. Checkpoints represent meaningful recovery boundaries.

### 10.3 Recovery preamble

Every stateful lifecycle and execution skill begins by:

1. discovering an active run relevant to the requested work,
2. reading `state.json` and `resume.md`,
3. checking the recorded commits, worktree, artifacts, and canonical backlog or issue state against current reality,
4. reconciling saved subagent identities with agents still available from the host,
5. preserving completed work and never redispatching it merely because conversational context was compacted,
6. reconstructing stale state from git and canonical artifacts when they disagree,
7. continuing from the validated next action.

Repository and remote evidence wins over stale checkpoint data. Recovery never silently restarts or reclassifies an active workflow.

### 10.4 Provider-neutral event stream

`events.jsonl` is an append-only, versioned stream using a small stable event vocabulary:

- `workflow_started`
- `phase_changed`
- `slice_started`
- `decision_recorded`
- `agent_dispatched`
- `agent_completed`
- `verification_failed`
- `verification_passed`
- `workflow_completed`

Events contain identifiers, paths, hashes, timestamps, status, and concise summaries—not secrets, sensitive environment values, full prompts, or verbose tool output.

### 10.5 Downstream agentic-RAG attachment

The base workflow has no runtime dependency on agentic RAG. A separate adapter may ingest checkpoints and events into agentic RAG, including its `compact-continuity` capability, and return the active work ID plus artifact pointers after compaction.

The boundary is intentionally one-way:

- the workflow publishes durable recovery facts,
- agentic RAG indexes and recalls them,
- recalled context is validated against git, files, tests, and issues,
- agentic RAG never becomes the canonical workflow-state writer.

This lets the public plugin operate alone while allowing Peter's agentic-RAG system to attach behind it without coupling either project to the other's implementation.

## 11. Project Gates and Memory

### 11.1 Authority order

```text
explicit current user instruction
-> project-specific gates and protected controls
-> current specifications, code, tests, and repository state
-> GitHub Issues or local BACKLOG.md
-> agentic RAG
-> native host memory
```

Project gates include applicable `AGENTS.md`, `CLAUDE.md`, constitution, contribution rules, architecture decisions, CI requirements, and protected project controls. The plugin preserves them rather than rewriting them into its own generic policy.

If two authoritative project rules conflict in a way that changes the implementation, the agent surfaces the concrete conflict. Automatic methodology selection does not authorize the agent to invent a project ruling.

### 11.2 Memory adapters

- Codex uses agentic RAG plus native Codex Memories when available.
- Claude uses agentic RAG plus Claude project and auto-memory facilities when available.
- Public installations work without agentic RAG.
- Peter's local profile enables the available agentic-RAG integration automatically.
- Retrieved memory is context, not authority, and must be checked against the repository before use.
- Durable decisions that affect ongoing work are written back to project artifacts rather than left only in memory.

## 12. Backlog and GitHub Issues

### 12.1 Local canonical mode

Every coding project using the method maintains a root `BACKLOG.md` and `FEATURES.md`.

Backlog status legend:

- `⭕` open
- `🔄` in progress
- `✅` complete
- `❌` blocked

Task IDs use an automatically derived, stable uppercase project key and monotonic number, for example:

- `EM-001`
- `EM-001.1`
- `EM-001.1.1`

Priority is separate from identity:

- `P0` blocking or urgent
- `P1` next
- `P2` planned
- `P3` later

Ordering is blocker-first, then priority, then dependency order. A blocked task moves near the top for visibility; the unresolved dependency that can actually unblock work is placed before it.

Update the backlog at work start, scope change, blocker discovery, completion of a slice, and final handoff. Do not renumber existing IDs when priorities change.

When `BACKLOG.md` exceeds 500 lines, move the oldest completed top-level groups to `BACKLOG-ARCHIVE.md` until the active file is at most 350 lines. Never archive open, in-progress, or blocked work. Preserve stable IDs and dependency references.

`FEATURES.md` is the human-readable capability inventory. Update it when a user-visible or architectural capability is added, removed, or materially changed; do not use it as a second task tracker.

### 12.2 GitHub canonical mode

When a reachable GitHub remote and authenticated GitHub CLI with suitable repository permission are detected, migrate once and make GitHub Issues canonical.

- Every GitHub issue title, body, label, relationship description, and agent-authored issue comment is English regardless of the conversation or repository language.
- Preserve stable IDs in the title and an embedded machine-readable body marker.
- Map hierarchy to GitHub sub-issues.
- Map dependencies to native `blocked by` and `blocking` relationships.
- Use English priority and workflow labels.
- Transfer completed local items as closed issues so history is preserved.
- Generate root `BACKLOG.md` as a clearly marked read-only cache.
- Derive identity from embedded markers so a lost local cache cannot cause duplicates.
- Make migration and refresh idempotent.
- Do not use `BACKLOG-ARCHIVE.md` in GitHub mode; closed issues are the archive.

If GitHub becomes temporarily unavailable after migration, continue from the cached state but queue mutations rather than treating the cache as a second canonical source. Reconcile queued changes before normal remote updates resume.

## 13. Repository Structure

```text
engineering-method/
├── .gitignore
├── .codex-plugin/plugin.json
├── .claude-plugin/plugin.json
├── skills/
│   ├── speckit-specify/
│   ├── speckit-plan/
│   ├── architecture-modeling/
│   ├── speckit-tasks/
│   ├── orchestrated-implementation/
│   ├── speckit-converge/
│   ├── openspec-propose/
│   ├── openspec-apply/
│   ├── openspec-archive/
│   ├── systematic-debugging/
│   ├── test-driven-development/
│   ├── verification-before-completion/
│   ├── requesting-code-review/
│   ├── receiving-code-review/
│   ├── dispatching-parallel-agents/
│   ├── using-git-worktrees/
│   └── project-backlog/
├── shared/
│   ├── platform/codex.md
│   ├── platform/claude.md
│   ├── agent-roles/
│   └── policies/
├── templates/
│   ├── BACKLOG.md
│   ├── FEATURES.md
│   ├── github-issue.md
│   ├── spec-kit/
│   └── openspec/
├── scripts/
│   ├── project-state
│   ├── backlog-to-issues
│   ├── refresh-issue-cache
│   ├── continuity-state
│   └── validate-plugin
├── third-party/sources.lock.json
├── docs/
├── README.md
├── THIRD_PARTY_NOTICES.md
└── LICENSE
```

All maintained documentation and skill instructions are English for public clarity and consistent model behavior. Runtime user communication follows the user's language except for GitHub content, which is always English.

## 14. Portability

### 14.1 Shared core

The `skills/` tree and workflow artifacts are host-neutral. Skills avoid assuming a specific invocation prefix, tool name, model identifier, or subagent API.

Shared references are resolved relative to the installed plugin root. Platform adapters contain the exact host syntax and capability detection.

### 14.2 Codex package

The Codex manifest exposes the common skill tree and valid Codex metadata. The Codex adapter describes collaboration tools, model selection from the actual spawn allowlist, worktree behavior, long-wait behavior, and native memory use.

### 14.3 Claude package

The Claude manifest exposes the same common skill tree. The Claude adapter describes the Agent tool, model aliases or full IDs, worktree isolation, plugin root variables, Claude memory, local testing, and reload behavior.

### 14.4 Capability fallback

- No subagents: execute sequentially in the coordinator.
- No worktree isolation: serialize writes in the current checkout after verifying branch safety.
- No strong preferred model: use the strongest available model and record the fallback.
- No UML renderer: retain validated text source and perform semantic review.
- No agentic RAG: continue from repository artifacts and native memory.
- No GitHub authentication: remain in local canonical backlog mode.

## 15. Licensing and Attribution

Release Peter's Engineering Method under the MIT License with:

```text
Copyright (c) 2026 Peter Hense
```

Spec Kit, OpenSpec, and Superpowers are MIT-licensed. Redistribution requirements are handled as follows:

- `LICENSE` contains the project's MIT license.
- `THIRD_PARTY_NOTICES.md` names every upstream project, copyright holder, license, repository, pinned revision, local derived files, and nature of modifications, and includes the required MIT notices.
- `third-party/sources.lock.json` records upstream URL, immutable commit SHA or release, source paths, destination paths, content hashes, license, and modification status.
- Substantial copied files retain the applicable copyright and permission notice in or adjacent to the distributed material.
- `README.md` clearly states that the plugin curates and adapts parts of GitHub Spec Kit, OpenSpec, and Superpowers and does not imply endorsement by their maintainers.
- Dependency-free original rewrites are identified as original rather than misattributed to an upstream project.

Source versions must be pinned before adaptation. Updating an upstream snapshot requires reviewing its license, diffing behavior, updating attribution and hashes, and re-running the full plugin test suite.

## 16. README Requirements

The public README must include:

- the efficiency-versus-depth problem the plugin solves,
- the exact automatic lifecycle boundaries,
- the large-feature architecture and integration gate,
- Codex and Claude installation instructions,
- local development and validation commands,
- backlog and GitHub Issues behavior, including the English-only rule,
- model-routing behavior and graceful fallbacks,
- context-compaction recovery and the optional downstream agentic-RAG attachment,
- third-party acknowledgements with links,
- a concise license section pointing to `LICENSE` and `THIRD_PARTY_NOTICES.md`,
- a statement that upstream project names identify sources and do not imply affiliation or endorsement.

## 17. Validation Strategy

### 17.1 Static validation

- Validate both plugin manifests with their host validators.
- Validate every `SKILL.md` frontmatter block and referenced file.
- Reject unfinished scaffold placeholders.
- Check that every referenced script and template exists.
- Check every copied or adapted file against `sources.lock.json` and `THIRD_PARTY_NOTICES.md`.
- Lint shell and structured-data files where applicable.

### 17.2 Behavioral trigger evaluation

Maintain positive, negative, and collision cases for Codex and Claude:

- trivial documentation or configuration edit,
- localized bug with a reproducible failure,
- bounded existing-behavior change,
- new multi-component feature,
- architecture migration,
- received code-review feedback,
- independent failure groups,
- completion claim without fresh evidence.

Success means exactly one primary lifecycle is selected, required supporting skills activate, and unrelated lifecycle skills remain inactive.

### 17.3 Script tests

Test:

- stable ID generation and hierarchy,
- blocker-first sorting,
- archive thresholds,
- feature inventory updates,
- GitHub English enforcement,
- idempotent issue creation,
- sub-issue and dependency mapping,
- offline mutation queue and reconciliation,
- malformed and partial remote responses,
- checkpoint schema upgrades and atomic writes,
- recovery after compaction at every lifecycle boundary,
- completed-task deduplication after recovery,
- stale checkpoint reconciliation against git,
- provider-neutral event emission without sensitive content.

Use a fake or recorded GitHub CLI boundary for normal tests. A live GitHub smoke test requires explicit suitable credentials and a designated test repository.

### 17.4 Workflow fixtures

Create temporary repositories that exercise the complete small-change, bugfix, Brownfield, and large-feature paths. The large-feature fixture includes deliberately inconsistent interfaces and failure paths so the UML analysis, task generation, subagent execution, defect loop, integration tests, convergence, and final verification all produce observable evidence.

### 17.5 Release gate

A release requires:

- all static validation and script tests passing,
- trigger collision suite passing on Codex and Claude,
- complete large-feature end-to-end fixture passing,
- a clean attribution audit,
- README installation instructions tested from a clean environment,
- no unresolved Critical or Important review findings,
- fresh final verification output.

## 18. References

- [GitHub Spec Kit documentation](https://github.github.com/spec-kit/)
- [Spec Kit Agentic SDD lifecycle](https://github.github.com/spec-kit/reference/agentic-sdd.html)
- [Spec Kit for existing projects](https://github.github.io/spec-kit/guides/existing-projects.html)
- [OpenSpec quickstart](https://openspec.dev/docs/quickstart)
- [Claude plugin guide](https://code.claude.com/docs/en/plugins)
- [Claude plugin reference](https://code.claude.com/docs/en/plugins-reference)
- [Claude subagents](https://code.claude.com/docs/en/sub-agents)
- [OpenAI GPT-5.6 Sol](https://developers.openai.com/api/docs/models/gpt-5.6-sol)
- [OpenAI model guidance](https://developers.openai.com/api/docs/guides/latest-model)
- [Claude model selection](https://platform.claude.com/docs/en/about-claude/models/choosing-a-model)
- [GitHub issue dependencies](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/creating-issue-dependencies)
- [GitHub sub-issues](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/adding-sub-issues)
- [Spec Kit MIT license](https://github.com/github/spec-kit/blob/main/LICENSE)
- [OpenSpec MIT license](https://github.com/Fission-AI/OpenSpec/blob/main/LICENSE)
- [Superpowers MIT license](https://github.com/obra/superpowers/blob/main/LICENSE)
