# EM-018 architecture findings

- AF-018-001 — Open. Ownership/cycle risk, FR-004/FR-005. Existing `shared/platform/*.md` links to writing policies and common playbook policy enumerates engineering phases. Move method-specific routing into each method; keep core adapter/policy usable without either consumer. Evidence: EM-018 component view and plan ownership table. Task T003.
- AF-018-002 — Open. Data-integrity/recovery risk, IC-001. Sharing via copies permits drift and accidental overwrite. Immutable blob export, explicit ownership, path/mode validation and transactional rollback must be exercised with actual files. Task T002.
- AF-018-003 — Open. Interface risk, IC-003/AC-006. Existing `scripts/install-opencode` owns one fixed filename. Derive distinct method loader identities and execute both hooks to prove coexistence without configuration loss. Task T004.

Verified 2026-11-13 against baseline d458f6a. No ownership cycle is permitted. As-built disposition and exact test evidence are required before convergence.
