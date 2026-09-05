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
