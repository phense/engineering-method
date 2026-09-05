# EM-005 bounded completion path

The user approved an effort brake on 2026-09-05 after disproportionate model
usage. Further paid evaluations and reviewer dispatch are paused. No acceptance
assertion is weakened and EM-005 remains incomplete.

## Existing evidence and its limits

- EM-004 independent reviews and acceptance are recorded in
  [EM-004 acceptance](EM-004-acceptance.md).
- Both complete native routing matrices passed on `6665647`: 12 Codex and
  12 Claude cases. Private summaries are retained under
  `/tmp/em005-release-6665647/{codex-routing,claude-routing}/summary.json`.
  These results precede the proportionality instructions, not fresh proof of them.
- Claude completed the large architecture fixture on the older `753c73a`
  package. Independent inspection confirmed its retained native review evidence
  and fresh local oracle replay. This is not current-package release acceptance.
- Native clean installation passed on both hosts for `98a2822`; deterministic
  packaging and local tests have passed on later candidates.
- The `6665647` release run was deliberately stopped at architecture evaluation
  because its Codex reviewer capture was known to be insufficient. Its release
  report correctly remains failed, not release eligible.

## Remaining evidence-tool findings

The parser review identified two reproducible acceptance gaps: a partial shell
skill read counted as a full read; an echo containing checkpoint arguments counted
as the assertion command. Both were reproduced with failing local controls and
corrected: shell reads require full evaluated skill content, and checkpoints
require Python executing the exact staged assertion path for the correct project.
Quoted commands and batched Python reads remain supported. No new paid run was
needed for these corrections. Full local verification also caught and corrected
a missing visible note for the proportionality backlog entry.

Codex's simplified JSON stream omits independent reviewer responses. A bounded
non-ephemeral probe proved that its own native rollout contains genuine spawn
and completed-child events. A production bridge was proposed but not implemented;
do not grow that subsystem merely to obtain a green report.

## Cheapest defensible next steps

1. Resolve the two acceptance-parser gaps with local negative controls; use
   retained transcripts to check actual command/skill evidence. No new model run
   is needed to determine whether these parser corrections work.
2. Consolidate existing reviews and artifact evidence, preserving revision and
   scope. Keep missing Codex native reviewer proof explicit; never reconstruct
   it from coordinator claims or relabel partial acceptance as a passed gate.
3. Run inexpensive local validators and packaged clean-install checks once on
   the integrated candidate. Repeat only checks affected by subsequent changes.
4. Before additional paid execution, present its precise unresolved acceptance
   question and bounded cost/effort. The original requirement for a fully passed
   cross-host release gate has not been waived. If it cannot be met from retained
   evidence, keep the candidate unreleased until that narrow next step is approved.

The user subsequently approved integrating this reduced local release-candidate
scope into main and replacing Superpowers with Engineering Method on both hosts.
The complete automated release gate remains deferred, not passed. No remote,
GitHub issues, push or publication is authorized.

## Completed bounded verification

Candidate `cf1f5723f1e3d00f844f875eee901184368a6e3e` passed:

- All 301 Python tests (including both reproduced negative controls).
- Portable plugin validation, Python compileall and Git whitespace checks.
- Provenance audit against all three pinned upstream checkouts; upstream
  revisions and hashes remain unchanged.
- Reproducible 182-file package, SHA-256
  `1005e7dc4e8e02017becb5a8069e5c0d9f027adbd753db905582e56aa334e168`.
- Native clean installation in disposable homes on Claude and Codex, including
  Claude strict validation. No credentials or live model requests were used.

Local package: `/tmp/em005-bounded-candidate.zip`. Clean-install evidence:
`/tmp/em005-bounded-clean-install.json`. These complete steps 1 and 3 above for
this candidate. This record is a documentation-only follow-up to that revision.

The candidate is locally installable. Full original release acceptance remains
unmet: current-package live architecture/reviewer evidence on Codex and the final
independent release verdict are missing. Earlier routing and Claude architecture
results retain their stated revision limits. Do not call the complete release
gate passed or start another paid loop. Local main integration and installation
are authorized by the user's explicit reduced-scope acceptance above.

## Subsequent public pre-release authorization — 2026-09-05

The user explicitly authorized publishing `phense/engineering-method`, pushing
`main`, and creating a GitHub **pre-release** after bounded local checks. This
supersedes the earlier no-publication authorization boundary in this historical
record; it does not waive or pass the original technical release gate.
`v0.1.0-rc.1` identifies that reduced-acceptance distribution of plugin `0.1.0`.
EM-005 remains incomplete. No paid evaluation loop or issue migration is
authorized by this publication task.

## Bounded native reviewer capture correction — 2026-09-05

EM-005.8 corrects the Codex architecture driver's missing reviewer replies.
Only architecture runs retain native session evidence; routing stays ephemeral.
The collector binds stdout's thread ID to the matching host-owned rollout and
project, then requires matching native child start/completion and final-response
identities. The reviewer confirms its scope in `review_assignment` in its own
verdict; this is explicitly child-attested scope, not decrypted spawn text.
Existing scope/hash, checkpoint and final-review ordering assertions are unchanged.
Captured evidence is private and excludes reasoning and system/user instructions.

All 305 local tests passed, including missing/wrong identity, incomplete response,
wrong project and missing scope controls. One bounded independent read-only code
review found no Critical or Important findings. A single native Codex probe
(Astra medium, 90-second maximum) passed: the separate reviewer's actual reply,
confirmed scope and independently computed file hash were captured successfully.
A local replay also verified the final evidence filtering. No full matrix ran.
This proves the capture correction, not complete architecture/release acceptance.
The published pre-release tag and its assets remain unchanged.

## Low-effort full acceptance attempts — 2026-09-05

The user authorized full acceptance using `gpt-6-astra` and
`claude-fable-5-1`, both at low effort. Invocation-only overrides now select those
models for coordinators and delegated roles without changing installed defaults.
Two executions of the unchanged ordered release gate stopped in Codex routing:

| Candidate | Result | Evidence limitation |
| --- | --- | --- |
| `e2c8276` | Failed after two routing cases passed | A complete `realpath; cat` skill read was not recognized. A regression-tested parser correction and retained-transcript replay resolved this shape. |
| `eaf1a6b` | Failed after three routing cases passed | `existing-speckit` combined discovery and complete skill reads; the supporting read's command ended with an unrelated failing Git history check. The required independently successful read evidence was absent. |

Both reports remain failed and not release eligible. Claude routing and both
architecture evaluations were not reached; there is no new Fable live result.
The second failure is an evidence-collection limitation, not an observed wrong
workflow selection. No acceptance assertion was relaxed.

Candidate `156e41ec79f0fd57907fed4db39f859168cdce12` adds a small evaluation
instruction: read each selected skill using a standalone successful `cat` or
native Read call. This instruction's live effectiveness is still unverified.
All 307 Python tests, portable and Claude strict plugin validation, native clean
installation on both hosts, deterministic packaging, clean-tree verification
and the unchanged three-upstream provenance audit passed locally. The local
release-check used explicit `--skip-live`, so its result is **development-only**,
not full acceptance. Its package SHA-256 is
`0ff1a7efbccafda6188bfcc40dfde9d6194b56e3b146017a8ba42f8824a4fb56`.

One independent Astra/low reviewer reviewed the integrated changes and focused
corrections, found no Critical or Important code findings, and explicitly refused
full release acceptance because live evidence is incomplete. The effort brake
stopped further model dispatch after the two unsuccessful full attempts.
The cheapest next step is one targeted `existing-speckit` run to establish the
prompt correction before considering another complete release gate.

Private local reports (raw host transcripts are not published):

| Report | SHA-256 |
| --- | --- |
| `/tmp/em005-release-low-e2c8276/release.json` | `2d3cbffd77ceb159e72581475cdaab7e5189166ab243c971c1df45e3b340c3ef` |
| `/tmp/em005-release-low-eaf1a6b/release.json` | `e88266f1e80c5f9b729dc34fed11ef476ac455052e6a0f31b198ee5739819ae6` |
| `/tmp/em005-local-156e41e/release.json` | `7c389887a19d433307370102b2bb3a5b46924dbf8edd4da062ab9551bfb0f676` |

EM-005 remains incomplete. The existing public pre-release and its immutable
tag/assets retain their original documented acceptance scope.

### Accidental migration during acceptance bookkeeping

The coordinator incorrectly treated `project-state backlog state-check` as
read-only. Its implementation automatically migrates when the remote is writable.
The invocation created Issues #1–#38 on `phense/engineering-method` between
15:27:44 and 15:28:34 UTC, despite the user's explicit no-migration instruction.
The local backlog was restored to canonical local mode. Read-back verified the
38 issues' origin and absence of comments; a private before-state snapshot is
retained. Automatic approval review rejected their deletion without explicit
user approval, so remote cleanup is pending. Do not invoke state-check again in
this project while migration remains unauthorized.

## Subsequent completion — 2026-09-05

The user approved deleting the accidental Issues #1–#38 and explicitly requested
finishing the fix and full acceptance. All 38 issues were removed and absence
verified. All nine original gate criteria are now covered for `0784c79`, with
independent acceptance and no unresolved Critical or Important findings. See
[the final acceptance record](EM-005-acceptance.md) for exact same-package evidence
reuse, the Claude checkpoint supplement, one independently verified ownership
metadata correction, and remaining fixture limits. The failed reports above
remain failed; no single successful full release-check invocation is claimed.
