---
type: reference
audience: Method maintainers reviewing the repository split
version: 1
---
# EM-018 split verification

On 2026-11-13 the split passed local package, state, recovery and native installation checks. Engineering remains a 0.3.0 source candidate for pull-request integration; this is not a tagged release or a replacement of existing global profiles.

## Verified boundaries

[Method Core](https://github.com/phense/method-core) owns 69 shared exports, including eight support skills and both playbook skills. [Engineering Method](https://github.com/phense/engineering-method) bundles 19 skills and [Writing Method](https://github.com/phense/writing-method) bundles 18. Both locks pin `255026bf88469e904514e093d06153f643ba0adb`. All repositories are public under `phense`, have their own Issues and pull requests, share `agent-methods`, and link to one another from their READMEs.

The original baseline was `d458f6aebb3887a6efca67d7fa958d2bfff6e14e` with 319 passing tests. The candidate package sources tested here are Engineering `206fbe54cee14123519b2b52553c65d77d3f2fa5`, Writing `e9eab64219fcaa03d375fc6dc9e4027c252fb45e`, and the Core revision above. Later engineering changes record evidence, backlog state and corrected integration-fixture invocation; they do not change delivered runtime or shared files.

## Full suites

Run `python3 scripts/validate-plugin` and `python3 -m unittest discover -s tests -t . -v` from each repository root. All three commands completed successfully. Counts overlap because each independent consumer tests its bundled common runtime.

| Repository | Tests | Elapsed | Captured unittest output SHA256 |
|---|---:|---:|---|
| Core | 159 | 50.513 s | `11dbc0b29d04b6bae6966b2d9c5533bf73944ff02e34613256b37f468569236d` |
| Engineering | 335 | 76.228 s | `054bf32e0009b225c4888f1ac9d65a33f246f0260d5a3b61494f70c0dbdc17ad` |
| Writing | 163 | 43.009 s | `9ef5eda8506aef6fa2e0304dab86c6c9973d4cc4a9072fb79c4f38717bf8e6c0` |

## Package and state integration

`python3 scripts/package-plugin --check --output PATH` built each archive twice from its immutable commit and produced matching bytes. Archive SHA256 values:

| Archive | SHA256 |
|---|---|
| Core | `c9e6e1c1f36439c9f91f810d544af0eae1f90bd0ef016d3a3e09ebc2590b5c99` |
| Engineering | `4af643a86bbc7610e1848b3e7ecd7e63e24bf391705c63848b676573be7c7b59` |
| Writing | `0b0d9c58d3e1e465420710b21b0bc5ff2b4897e7a202f8b2feffeac352e9d5c2` |

Run the complete success/recovery flow with:

```sh
python3 tests/e2e/test-method-split --core /path/to/method-core.zip --engineering /path/to/engineering-method.zip --writing /path/to/writing-method.zip --output .engineering-method/verification/split.json
```

It extracts each immutable archive into a separate directory, creates a local Git fixture from Core's exported source, and synchronizes both methods. Each method's actual installed wrappers initialize and start `TEST-001` in a separate project, create a continuity checkpoint and recover it. Project files stay in the target; no project state appears in either plugin.

The fixture changes two actual exported adapters, terminates each updater with exit 23 immediately after a real replacement, and requires the offline check to fail. `--recover` then restores the prior plugin snapshot, including bytes and file modes. A valid retry installs the new Core into both consumers. Both resulting locks agree across all 69 exports, and the original project files, continuity checkpoint, modes and work ID remain unchanged. The fixture revisions are local test commits, not replacement upstream pins.

## Independent review and fixes

Two read-only reviewers inspected the bounded split and the materially changed recovery interface. Their original verdicts contained actionable findings; the coordinator verified and resolved them rather than treating a conditional verdict as an unconditional acceptance.

| Finding | Resolution and current evidence |
|---|---|
| A permanently unwritable unchanged destination prevented earlier rollback | Skip unchanged snapshots, attempt every restoration, retain durable backups on failure; real POSIX permission regression passes. |
| Interrupts and process death left an unrecoverable mixed version | Catch ordinary interrupts, persist complete backups before writes, add offline `--recover`; interrupt, abrupt-exit and blocked-recovery retry tests pass. |
| Two recoveries could overwrite a newer update and remove its journal | Sync and recovery share a persistent, exclusive OS file lock; verify journal identity before atomic retirement. A real paused recovery process excludes a second recovery and an update, then permits a valid retry. |
| Writing required absent Engineering debugging/TDD skills | Shared review now treats them as optional engineering companions and checks prose against its own sources/requirements. Both consumers contain the same corrected file. |
| Shared install snippets chose Engineering's identity | Examples use the consuming manifest's identity; actual native installs exercise both identities. |

The 13 sync regression tests and the final full suites include these fixes. There are no unresolved Critical or Important review findings. Windows-specific locking behavior and live host model behavior were not independently exercised on this Linux host.

## Native installation and coexistence

`python3 scripts/clean_install.py --package PATH --output PATH` passed independently for both consumer archives with Codex CLI 0.169.0 and Claude Code 2.1.323. Each run created empty disposable configuration homes, validated and registered the local marketplace, installed the method and verified its enabled native inventory. A further disposable-home check installed both together and verified both identities in each host's inventory. No credentials were copied or used, and no model requests were sent. Existing global profiles were not modified.

Real Node-based OpenCode loader tests in the full suites prove separate loader ownership and configuration preservation. They do not constitute a new live OpenCode routing evaluation.

## Provenance and limits

All 39 original adapted-source records retain their upstream project IDs, immutable revisions, source paths and hashes across their new owners. Validators check actual destination hashes and license notices. All twelve PDF-template files match the original engineering baseline byte for byte.

No fresh PDF render or live-model authoring/routing run is claimed. The moved PDF checker and historical render evidence remain available in Writing; this host lacks `mutool`. Gemini adapter verification is deferred as `EM-019`. No release tag, default-branch merge or production/global installation is implicit in this evidence.

## Acceptance mapping

AC-001/002: native manifests, exact skill inventories, resolved resources and isolated archive execution. AC-003/004: immutable locks, ownership/drift checks and complete failure/recovery regressions. AC-005: unchanged runtime imports, CLI names and target state demonstrated end to end. AC-006: byte-identical common exports, native dual installation and OpenCode coexistence. AC-007: retained upstream records/licenses and twelve unchanged template files. AC-008: explicit separation of installation/structural evidence from unperformed live evaluations.

As-built findings AF-018-001 through AF-018-003 are resolved. Local convergence found no remaining implementation task. Core and Writing source publication is complete. The Engineering integration candidate is published as [pull request 135](https://github.com/phense/engineering-method/pull/135); the existing default branch and global installations remain separate from this source handoff. The initial ten source-handoff tasks are complete. GitHub exposed an undeclared test dependency: its Engineering runner lacked `rg`, causing one of 335 tests to error while local suites passed. Convergence task T011 installs `ripgrep` explicitly in CI. Both fresh GitHub checks passed on `bf0571f0866a7cace3133925e0f9f7af7d75728a`; the [full verification run](https://github.com/phense/engineering-method/actions/runs/43411582010) passed all 335 tests. T011 is complete. The user authorized integration of PR135 after these checks.
