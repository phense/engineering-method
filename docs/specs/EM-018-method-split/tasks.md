# Tasks: EM-018 method split

Specification: `spec.md`; plan: `plan.md`; architecture: `../../uml/em-018-components.md`, `../../uml/findings.md`.

## Architecture findings

AF-018-001 requires method-neutral exports; AF-018-002 transactional sync; AF-018-003 independent installation identities. Coordinator owns all implementation paths sequentially.

## Tests

Preserve the baseline green runtime contracts. Verify a failing sync behavior test before implementing new behavior. Exercise actual CLI, filesystem state, extracted packages and OpenCode hooks; source wording checks supplement behavior evidence.

## Implementation slices

### Slice S1: Shared core and safe export

- [x] T001 [US-002] [FR-004] Inventory and copy genuine shared support into `../method-core/`, preserving imports, state paths and upstream metadata. Baseline: 319 tests passed.
- [x] T002 [US-002] [IC-001] [AF-018-002] Implement `method-core/scripts/method_core.py` and sync CLI after red tests for drift, ownership, malformed paths, modes and rollback. Depends on T001.
- [x] T003 [US-003] [IC-004] [AF-018-001] Generalize shared playbooks and host adapters; keep per-method lifecycle routing out of core. Files: core shared policies/skills/platform and templates. Depends on T001.

### Slice S2: Focused method packages

- [x] T004 [US-001] [IC-003] [AF-018-003] Split writing resources and tests into `../writing-method/`, adapt engineering resources/tests, manifests, provenance and generic packaging/OpenCode tools. Depends on T002,T003.
- [x] T005 [US-001] [US-002] Document native installation, sync, rollback, namespaces and verification limits in both READMEs; preserve historical release documents. Depends on T004.

### Slice S3: Integration and review

- [x] T006 Reconcile as-built architecture and derive success/recovery integration checks from actual package boundaries. Depends on T004.
- [x] T007 Run full relevant suites, extracted-package integration and coexistence checks; resolve findings with focused regression tests. Depends on T006.
- [x] T008 Obtain independently tracked acceptance review of the bounded three-repository diff, fix actionable findings and rerun affected checks. Depends on T007.

### Slice S4: Convergence and handoff

- [x] T009 Run speckit-converge, retain exact evidence and only then complete EM-018. Depends on T005,T008.
- [x] T010 Publish new source repositories and the engineering change branch for review; preserve existing installed profiles and original default branch until explicit integration. Depends on T009.

## Dependencies

T001 precedes T002/T003; these precede T004; T004 precedes T005/T006; T006 precedes T007; T007 precedes T008; T005/T008 precede T009; T009 precedes T010. No parallel writers.

## Playbook obligations

Spec/plan assessed none for new operational procedures. Delivered generic playbook support is covered by T003/T004 and its independent content review and behavior-boundary checks.
