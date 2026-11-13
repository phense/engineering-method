# EM-018 architecture findings

- AF-018-001 — Resolved. Core adapters and generic playbooks no longer require an absent writing or engineering lifecycle. Engineering retains its phase hooks; Writing's review/debugging companions are optional. Both independent package validators and resource/contract tests pass. Tasks T003/T004.
- AF-018-002 — Resolved. Committed export inventory, revision/hash/mode locks, ownership and drift checks protect managed files. Durable backups, explicit recovery, retained failed-restore data, stable OS serialization and journal identity checks cover interruption and concurrent recovery. Thirteen sync regressions and the complete archive/target-state recovery flow pass. Task T002.
- AF-018-003 — Resolved. Plugin manifests and archive/OpenCode identities derive from the consumer. Both native methods coexist in disposable Claude/Codex homes; real OpenCode hook tests preserve user configuration and separate loaders. Task T004.

Reconciled 2026-11-13 against Core `255026b`, Engineering candidate `206fbe5` and Writing `e9eab64`. No ownership cycle or sibling runtime dependency remains. Exact evidence and limits: [EM-018 verification](../verification/EM-018-method-split.md).
