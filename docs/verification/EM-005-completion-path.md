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

Preserve the five uncommitted parser/test files separately from the policy change.
Their review identified two reproducible acceptance gaps: a partial skill read
can count as a full read; an echo containing checkpoint arguments can count as
the assertion command. Neither establishes a defect in the workflow skills,
but neither may be accepted as release proof.

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

Main stays unchanged until acceptance is complete. No remote, GitHub issues,
push or publication is authorized.
