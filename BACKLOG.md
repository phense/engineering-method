# Backlog
<!-- engineering-method:backlog-document {"schema_version":1,"project_key":"EM","mode":"local"} -->

This is the canonical local task register until GitHub Issues become writable and canonical.
Keep stable IDs unchanged. Order groups unblocker-first, then priority and dependency order.

## Status legend

- `⭕` Open
- `🔄` In progress
- `✅` Complete
- `❌` Blocked

## Tasks

<!-- engineering-method:backlog {"schema_version":1,"id":"EM-000","title":"Approve and commit the consolidated plugin design (`877a7ea`).","status":"complete","priority":"P0","parent_id":null,"depends_on":[],"notes":"","updated_at":"1970-01-01T00:00:00Z"} -->
- ✅ `EM-000` **P0** Approve and commit the consolidated plugin design (`877a7ea`).
<!-- engineering-method:backlog {"schema_version":1,"id":"EM-001","title":"Establish the dual-host plugin foundation and provenance controls. Blocks `EM-002` through `EM-005`.","status":"complete","priority":"P0","parent_id":null,"depends_on":[],"notes":"","updated_at":"1970-01-01T00:00:00Z"} -->
- ✅ `EM-001` **P0** Establish the dual-host plugin foundation and provenance controls. Blocks `EM-002` through `EM-005`.
  <!-- engineering-method:backlog {"schema_version":1,"id":"EM-001.1","title":"Create compatible Codex and Claude plugin manifests.","status":"complete","priority":"P0","parent_id":"EM-001","depends_on":[],"notes":"","updated_at":"1970-01-01T00:00:00Z"} -->
  - ✅ `EM-001.1` **P0** Create compatible Codex and Claude plugin manifests.
  <!-- engineering-method:backlog {"schema_version":1,"id":"EM-001.2","title":"Add the dependency-free Python validation and test scaffold.","status":"complete","priority":"P0","parent_id":"EM-001","depends_on":[],"notes":"","updated_at":"1970-01-01T00:00:00Z"} -->
  - ✅ `EM-001.2` **P0** Add the dependency-free Python validation and test scaffold.
  <!-- engineering-method:backlog {"schema_version":1,"id":"EM-001.3","title":"Pin upstream revisions and implement MIT attribution controls.","status":"complete","priority":"P0","parent_id":"EM-001","depends_on":[],"notes":"","updated_at":"1970-01-01T00:00:00Z"} -->
  - ✅ `EM-001.3` **P0** Pin upstream revisions and implement MIT attribution controls.
  <!-- engineering-method:backlog {"schema_version":1,"id":"EM-001.4","title":"Add baseline structural validation for both hosts.","status":"complete","priority":"P0","parent_id":"EM-001","depends_on":[],"notes":"","updated_at":"1970-01-01T00:00:00Z"} -->
  - ✅ `EM-001.4` **P0** Add baseline structural validation for both hosts.
<!-- engineering-method:backlog {"schema_version":1,"id":"EM-002","title":"Implement durable project state and compact continuity","status":"complete","priority":"P1","parent_id":null,"depends_on":["EM-001"],"notes":"","updated_at":"2026-09-04T14:43:50Z"} -->
- ✅ `EM-002` **P1** Implement durable project state and compact continuity
  - Depends on: `EM-001`
  <!-- engineering-method:backlog {"schema_version":1,"id":"EM-002.1","title":"Add state models and safe filesystem primitives.","status":"complete","priority":"P1","parent_id":"EM-002","depends_on":[],"notes":"","updated_at":"2026-09-04T14:43:50Z"} -->
  - ✅ `EM-002.1` **P1** Add state models and safe filesystem primitives.
  <!-- engineering-method:backlog {"schema_version":1,"id":"EM-002.2","title":"Implement stable local backlog parsing, sorting, and archiving.","status":"complete","priority":"P1","parent_id":"EM-002","depends_on":[],"notes":"","updated_at":"2026-09-04T14:43:50Z"} -->
  - ✅ `EM-002.2` **P1** Implement stable local backlog parsing, sorting, and archiving.
  <!-- engineering-method:backlog {"schema_version":1,"id":"EM-002.3","title":"Maintain the non-duplicative `FEATURES.md` capability inventory.","status":"complete","priority":"P1","parent_id":"EM-002","depends_on":[],"notes":"","updated_at":"2026-09-04T14:43:50Z"} -->
  - ✅ `EM-002.3` **P1** Maintain the non-duplicative `FEATURES.md` capability inventory.
  <!-- engineering-method:backlog {"schema_version":1,"id":"EM-002.4","title":"Add the testable GitHub boundary.","status":"complete","priority":"P1","parent_id":"EM-002","depends_on":[],"notes":"","updated_at":"2026-09-04T14:43:50Z"} -->
  - ✅ `EM-002.4` **P1** Add the testable GitHub boundary.
  <!-- engineering-method:backlog {"schema_version":1,"id":"EM-002.5","title":"Implement idempotent issue migration, relationships, cache, and offline reconciliation.","status":"complete","priority":"P1","parent_id":"EM-002","depends_on":[],"notes":"","updated_at":"2026-09-04T14:43:50Z"} -->
  - ✅ `EM-002.5` **P1** Implement idempotent issue migration, relationships, cache, and offline reconciliation.
  <!-- engineering-method:backlog {"schema_version":1,"id":"EM-002.6","title":"Implement versioned compact-continuity checkpoints and events.","status":"complete","priority":"P1","parent_id":"EM-002","depends_on":[],"notes":"","updated_at":"2026-09-04T14:43:50Z"} -->
  - ✅ `EM-002.6` **P1** Implement versioned compact-continuity checkpoints and events.
  <!-- engineering-method:backlog {"schema_version":1,"id":"EM-002.7","title":"Wire project-state commands and the `project-backlog` skill.","status":"complete","priority":"P1","parent_id":"EM-002","depends_on":[],"notes":"","updated_at":"2026-09-04T14:43:50Z"} -->
  - ✅ `EM-002.7` **P1** Wire project-state commands and the `project-backlog` skill.
<!-- engineering-method:backlog {"schema_version":1,"id":"EM-003","title":"Build the curated, non-overlapping lifecycle and quality skills","status":"complete","priority":"P1","parent_id":null,"depends_on":["EM-001"],"notes":"","updated_at":"2026-09-04T14:43:51Z"} -->
- ✅ `EM-003` **P1** Build the curated, non-overlapping lifecycle and quality skills
  - Depends on: `EM-001`
  <!-- engineering-method:backlog {"schema_version":1,"id":"EM-003.1","title":"Define exclusive lifecycle contracts and artifact templates.","status":"complete","priority":"P1","parent_id":"EM-003","depends_on":[],"notes":"","updated_at":"2026-09-04T14:43:50Z"} -->
  - ✅ `EM-003.1` **P1** Define exclusive lifecycle contracts and artifact templates.
  <!-- engineering-method:backlog {"schema_version":1,"id":"EM-003.2","title":"Adapt Spec Kit `specify`, `plan`, `tasks`, and `converge`.","status":"complete","priority":"P1","parent_id":"EM-003","depends_on":[],"notes":"","updated_at":"2026-09-04T14:43:50Z"} -->
  - ✅ `EM-003.2` **P1** Adapt Spec Kit `specify`, `plan`, `tasks`, and `converge`.
  <!-- engineering-method:backlog {"schema_version":1,"id":"EM-003.3","title":"Adapt OpenSpec `propose`, `apply`, and `archive`.","status":"complete","priority":"P1","parent_id":"EM-003","depends_on":[],"notes":"","updated_at":"2026-09-04T14:43:50Z"} -->
  - ✅ `EM-003.3` **P1** Adapt OpenSpec `propose`, `apply`, and `archive`.
  <!-- engineering-method:backlog {"schema_version":1,"id":"EM-003.4","title":"Port Superpowers debugging, TDD, and verification.","status":"complete","priority":"P1","parent_id":"EM-003","depends_on":[],"notes":"","updated_at":"2026-09-04T14:43:50Z"} -->
  - ✅ `EM-003.4` **P1** Port Superpowers debugging, TDD, and verification.
  <!-- engineering-method:backlog {"schema_version":1,"id":"EM-003.5","title":"Port review, worktree, and parallel-dispatch support.","status":"complete","priority":"P1","parent_id":"EM-003","depends_on":[],"notes":"","updated_at":"2026-09-04T14:43:50Z"} -->
  - ✅ `EM-003.5` **P1** Port review, worktree, and parallel-dispatch support.
  <!-- engineering-method:backlog {"schema_version":1,"id":"EM-003.6","title":"Integrate project-backlog support and collision acceptance.","status":"complete","priority":"P1","parent_id":"EM-003","depends_on":[],"notes":"","updated_at":"2026-09-04T14:43:51Z"} -->
  - ✅ `EM-003.6` **P1** Integrate project-backlog support and collision acceptance.
<!-- engineering-method:backlog {"schema_version":1,"id":"EM-004","title":"Add efficient subagent orchestration and the architecture gate","status":"complete","priority":"P1","parent_id":null,"depends_on":["EM-002","EM-003"],"notes":"","updated_at":"2026-09-05T10:52:23Z"} -->
- ✅ `EM-004` **P1** Add efficient subagent orchestration and the architecture gate
  - Depends on: `EM-002`, `EM-003`
  <!-- engineering-method:backlog {"schema_version":1,"id":"EM-004.1","title":"Add shared model roles, host adapters, and agent-role briefs.","status":"complete","priority":"P1","parent_id":"EM-004","depends_on":[],"notes":"","updated_at":"2026-09-05T10:52:23Z"} -->
  - ✅ `EM-004.1` **P1** Add shared model roles, host adapters, and agent-role briefs.
  <!-- engineering-method:backlog {"schema_version":1,"id":"EM-004.2","title":"Implement cohesive-slice orchestration with targeted review and evidence-driven fix loops.","status":"complete","priority":"P1","parent_id":"EM-004","depends_on":[],"notes":"","updated_at":"2026-09-05T10:52:23Z"} -->
  - ✅ `EM-004.2` **P1** Implement cohesive-slice orchestration with targeted review and evidence-driven fix loops.
  <!-- engineering-method:backlog {"schema_version":1,"id":"EM-004.3","title":"Implement evidence-driven defect convergence.","status":"complete","priority":"P1","parent_id":"EM-004","depends_on":[],"notes":"","updated_at":"2026-09-05T10:52:23Z"} -->
  - ✅ `EM-004.3` **P1** Implement evidence-driven defect convergence.
  <!-- engineering-method:backlog {"schema_version":1,"id":"EM-004.4","title":"Implement design-time and as-built UML analysis under `docs/uml/`.","status":"complete","priority":"P1","parent_id":"EM-004","depends_on":[],"notes":"","updated_at":"2026-09-05T10:52:23Z"} -->
  - ✅ `EM-004.4` **P1** Implement design-time and as-built UML analysis under `docs/uml/`.
  <!-- engineering-method:backlog {"schema_version":1,"id":"EM-004.5","title":"Add the system-architect integration-test gate.","status":"complete","priority":"P1","parent_id":"EM-004","depends_on":[],"notes":"","updated_at":"2026-09-05T10:52:23Z"} -->
  - ✅ `EM-004.5` **P1** Add the system-architect integration-test gate.
  <!-- engineering-method:backlog {"schema_version":1,"id":"EM-004.6","title":"Verify recovery across compaction and subagent lifecycle boundaries.","status":"complete","priority":"P1","parent_id":"EM-004","depends_on":[],"notes":"","updated_at":"2026-09-05T10:52:23Z"} -->
  - ✅ `EM-004.6` **P1** Verify recovery across compaction and subagent lifecycle boundaries.
<!-- engineering-method:backlog {"schema_version":1,"id":"EM-005","title":"Validate, document, and package the complete plugin","status":"in_progress","priority":"P2","parent_id":null,"depends_on":["EM-001","EM-004"],"notes":"","updated_at":"2026-09-05T11:04:23Z"} -->
- 🔄 `EM-005` **P2** Validate, document, and package the complete plugin
  - Depends on: `EM-001`, `EM-004`
  <!-- engineering-method:backlog {"schema_version":1,"id":"EM-005.1","title":"Finalize platform adapters and marketplace metadata.","status":"complete","priority":"P2","parent_id":"EM-005","depends_on":[],"notes":"","updated_at":"2026-09-05T11:04:23Z"} -->
  - ✅ `EM-005.1` **P2** Finalize platform adapters and marketplace metadata.
  <!-- engineering-method:backlog {"schema_version":1,"id":"EM-005.2","title":"Add Codex/Claude trigger, collision, fallback, and workflow evaluations.","status":"in_progress","priority":"P2","parent_id":"EM-005","depends_on":[],"notes":"","updated_at":"2026-09-05T11:04:23Z"} -->
  - 🔄 `EM-005.2` **P2** Add Codex/Claude trigger, collision, fallback, and workflow evaluations.
  <!-- engineering-method:backlog {"schema_version":1,"id":"EM-005.3","title":"Execute the large-feature architecture fixture on both hosts.","status":"in_progress","priority":"P2","parent_id":"EM-005","depends_on":[],"notes":"","updated_at":"2026-09-05T11:04:23Z"} -->
  - 🔄 `EM-005.3` **P2** Execute the large-feature architecture fixture on both hosts.
  <!-- engineering-method:backlog {"schema_version":1,"id":"EM-005.4","title":"Complete static, package, and clean-install validation.","status":"in_progress","priority":"P2","parent_id":"EM-005","depends_on":[],"notes":"","updated_at":"2026-09-05T11:04:23Z"} -->
  - 🔄 `EM-005.4` **P2** Complete static, package, and clean-install validation.
  <!-- engineering-method:backlog {"schema_version":1,"id":"EM-005.5","title":"Write and verify the public README and third-party notices.","status":"complete","priority":"P2","parent_id":"EM-005","depends_on":[],"notes":"","updated_at":"2026-09-05T11:04:23Z"} -->
  - ✅ `EM-005.5` **P2** Write and verify the public README and third-party notices.
  <!-- engineering-method:backlog {"schema_version":1,"id":"EM-005.6","title":"Run the system-architect release gate.","status":"open","priority":"P2","parent_id":"EM-005","depends_on":[],"notes":"","updated_at":"1970-01-01T00:00:00Z"} -->
  - ⭕ `EM-005.6` **P2** Run the system-architect release gate.
  <!-- engineering-method:backlog {"schema_version":1,"id":"EM-005.7","title":"Apply shared proportionality and an effort brake to every skill.","status":"complete","priority":"P2","parent_id":"EM-005","depends_on":[],"notes":"User-approved scope correction; see docs/verification/EM-005-completion-path.md for remaining release evidence.","updated_at":"2026-09-05T13:22:56Z"} -->
  - ✅ `EM-005.7` **P2** Apply shared proportionality and an effort brake to every skill.
