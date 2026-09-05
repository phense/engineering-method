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
<!-- engineering-method:backlog {"schema_version":1,"id":"EM-005","title":"Validate, document, and package the complete plugin","status":"complete","priority":"P2","parent_id":null,"depends_on":["EM-001","EM-004"],"notes":"All nine original gate criteria accepted on 0784c79 with explicit same-package evidence reuse, Claude checkpoint supplement and independently verified ownership metadata correction. Failed reports preserved; see docs/verification/EM-005-acceptance.md. Accidental Issues #1-38 removed with approval; local backlog remains canonical.","updated_at":"2026-09-05T19:11:37Z"} -->
- ✅ `EM-005` **P2** Validate, document, and package the complete plugin
  - Depends on: `EM-001`, `EM-004`
  - Notes: All nine original gate criteria accepted on 0784c79 with explicit same-package evidence reuse, Claude checkpoint supplement and independently verified ownership metadata correction. Failed reports preserved; see docs/verification/EM-005-acceptance.md. Accidental Issues #1-38 removed with approval; local backlog remains canonical.
  <!-- engineering-method:backlog {"schema_version":1,"id":"EM-005.1","title":"Finalize platform adapters and marketplace metadata.","status":"complete","priority":"P2","parent_id":"EM-005","depends_on":[],"notes":"","updated_at":"2026-09-05T11:04:23Z"} -->
  - ✅ `EM-005.1` **P2** Finalize platform adapters and marketplace metadata.
  <!-- engineering-method:backlog {"schema_version":1,"id":"EM-005.2","title":"Add Codex/Claude trigger, collision, fallback, and workflow evaluations.","status":"complete","priority":"P2","parent_id":"EM-005","depends_on":[],"notes":"All 12 routing cases passed on each host: gpt-6-astra low and claude-fable-5-1 low, package 0784c79.","updated_at":"2026-09-05T19:11:37Z"} -->
  - ✅ `EM-005.2` **P2** Add Codex/Claude trigger, collision, fallback, and workflow evaluations.
    - Notes: All 12 routing cases passed on each host: gpt-6-astra low and claude-fable-5-1 low, package 0784c79.
  <!-- engineering-method:backlog {"schema_version":1,"id":"EM-005.3","title":"Execute the large-feature architecture fixture on both hosts.","status":"complete","priority":"P2","parent_id":"EM-005","depends_on":[],"notes":"All ten architecture phases and original native-review/hash/integration assertions passed on both hosts; Claude required the documented invocation supplement and one clerical report correction. See docs/verification/EM-005-acceptance.md.","updated_at":"2026-09-05T19:11:37Z"} -->
  - ✅ `EM-005.3` **P2** Execute the large-feature architecture fixture on both hosts.
    - Notes: All ten architecture phases and original native-review/hash/integration assertions passed on both hosts; Claude required the documented invocation supplement and one clerical report correction. See docs/verification/EM-005-acceptance.md.
  <!-- engineering-method:backlog {"schema_version":1,"id":"EM-005.4","title":"Complete static, package, and clean-install validation.","status":"complete","priority":"P2","parent_id":"EM-005","depends_on":[],"notes":"308 tests, both validators, provenance, reproducible 188-file package and both native clean installs passed on 0784c79.","updated_at":"2026-09-05T19:11:37Z"} -->
  - ✅ `EM-005.4` **P2** Complete static, package, and clean-install validation.
    - Notes: 308 tests, both validators, provenance, reproducible 188-file package and both native clean installs passed on 0784c79.
  <!-- engineering-method:backlog {"schema_version":1,"id":"EM-005.5","title":"Write and verify the public README and third-party notices.","status":"complete","priority":"P2","parent_id":"EM-005","depends_on":[],"notes":"","updated_at":"2026-09-05T11:04:23Z"} -->
  - ✅ `EM-005.5` **P2** Write and verify the public README and third-party notices.
  <!-- engineering-method:backlog {"schema_version":1,"id":"EM-005.6","title":"Run the system-architect release gate.","status":"complete","priority":"P2","parent_id":"EM-005","depends_on":[],"notes":"Independent Astra low reviewer accepted complete original gate coverage with explicit evidence reuse; no unresolved Critical or Important findings. Not a successful single release-check invocation.","updated_at":"2026-09-05T19:11:37Z"} -->
  - ✅ `EM-005.6` **P2** Run the system-architect release gate.
    - Notes: Independent Astra low reviewer accepted complete original gate coverage with explicit evidence reuse; no unresolved Critical or Important findings. Not a successful single release-check invocation.
  <!-- engineering-method:backlog {"schema_version":1,"id":"EM-005.7","title":"Apply shared proportionality and an effort brake to every skill.","status":"complete","priority":"P2","parent_id":"EM-005","depends_on":[],"notes":"User-approved scope correction; see docs/verification/EM-005-completion-path.md for remaining release evidence.","updated_at":"2026-09-05T13:22:56Z"} -->
  - ✅ `EM-005.7` **P2** Apply shared proportionality and an effort brake to every skill.
    - Notes: User-approved scope correction; see docs/verification/EM-005-completion-path.md for remaining release evidence.
  <!-- engineering-method:backlog {"schema_version":1,"id":"EM-005.8","title":"Capture native Codex reviewer replies with independently confirmed scope","status":"complete","priority":"P2","parent_id":"EM-005","depends_on":[],"notes":"305 local tests, one independent bounded code review and one successful native Codex capture probe (90-second maximum). Existing release assertions unchanged; full architecture/release acceptance remains open.","updated_at":"2026-09-05T14:49:20Z"} -->
  - ✅ `EM-005.8` **P2** Capture native Codex reviewer replies with independently confirmed scope
    - Notes: 305 local tests, one independent bounded code review and one successful native Codex capture probe (90-second maximum). Existing release assertions unchanged; full architecture/release acceptance remains open.
<!-- engineering-method:backlog {"schema_version":1,"id":"EM-006","title":"Publish the documented public prerelease with bounded verification","status":"complete","priority":"P2","parent_id":null,"depends_on":[],"notes":"Published phense/engineering-method and v0.1.0-rc.1 at 9ff0bdd. Verified public visibility, tag, prerelease flag, downloaded ZIP/checksum and GitHub install/update/disable/removal on both hosts. EM-005 remains incomplete; no issue migration.","updated_at":"2026-09-05T14:13:52Z"} -->
- ✅ `EM-006` **P2** Publish the documented public prerelease with bounded verification
  - Notes: Published phense/engineering-method and v0.1.0-rc.1 at 9ff0bdd. Verified public visibility, tag, prerelease flag, downloaded ZIP/checksum and GitHub install/update/disable/removal on both hosts. EM-005 remains incomplete; no issue migration.
<!-- engineering-method:backlog {"schema_version":1,"id":"EM-007","title":"Publish stable version 0.1.0 and update public documentation","status":"complete","priority":"P2","parent_id":null,"depends_on":["EM-005"],"notes":"Published v0.1.0 at e9f5130 as stable Latest with checked ZIP and SHA256SUMS. 308 tests, validators, provenance, reproducible packaging, both clean installs, downloaded bytes and GitHub/main plus fixed-tag installs verified. Prior rc.1 unchanged; no issue migration.","updated_at":"2026-09-05T19:27:21Z"} -->
- ✅ `EM-007` **P2** Publish stable version 0.1.0 and update public documentation
  - Depends on: `EM-005`
  - Notes: Published v0.1.0 at e9f5130 as stable Latest with checked ZIP and SHA256SUMS. 308 tests, validators, provenance, reproducible packaging, both clean installs, downloaded bytes and GitHub/main plus fixed-tag installs verified. Prior rc.1 unchanged; no issue migration.
