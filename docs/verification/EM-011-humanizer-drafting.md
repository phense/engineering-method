# EM-011 Humanizer drafting constraints

Date: 2026-09-16. Base: `4b69c08` (EM-010). Integrates blader/humanizer as a
drafting-time supporting skill for medium and large documentation.

## Source and adaptation

- Upstream: https://github.com/blader/humanizer at
  `9862685f575c65a8247f90369951df1b3416e3d6`, MIT, copyright 2025 Siqi Chen.
  Upstream inventory: `SKILL.md`, `README.md`, `AGENTS.md`, `agents/openai.yaml`,
  a validation script and plugin manifests. Only `SKILL.md` was adapted.
- Destination: `skills/human-prose-drafting/SKILL.md`, pinned in
  `third-party/sources.lock.json` with source and destination hashes and
  recorded in `THIRD_PARTY_NOTICES.md` with the full MIT notice.
- Adaptation: the upstream procedure rewrites finished text (mark tells, draft,
  check, final). The adapted skill states the same 25 patterns as constraints
  the author obeys while drafting, grouped by strength, with a per-chunk check
  for the five tells that most often survive drafting. Pasted-text, file and
  voice-matching modes were removed; documentation voice rules were added.
  Facts, steps and glossary terms are explicitly out of the skill's reach.

## Integration

- `documentation-authoring` drafts every chunk under the constraints (workflow
  step 3), explicitly reads the supporting skill before the first sentence,
  runs the chunk check before marking a chunk drafted (step 6), and
  requires it for completion.
- `documentation-review` runs a prose-tell search over the scope as check 9;
  the review template has the matching row. A finding returns to the author
  as a passage to restate, not as a request for a rewrite pass.
- `writing-depth` names the constraints in the medium and large depth rows;
  small edits keep the surrounding voice without loading another skill.
- Pattern matches are assessed in context. Required headings, templates,
  anchors, technical terms, quotations, warnings and honest uncertainty take
  precedence over style preferences. A prose check does not prematurely set
  the full chunk review timestamp.
- The documentation plan template fixes "no separate humanizing pass" as a
  convention. Trigger matrix cases for the standalone document and the
  existing plan list the skill as supporting.

## Checks

- `python3 -m unittest discover -s tests -t .`: 317 tests passed after the
  completed local EM-011 status was reconciled with F-008. Before that status
  transition, the sole failure was the inventory's completed-work invariant;
  no test assertion was weakened.
- `python3 scripts/validate-plugin`: exit 0.
- `claude plugin validate --strict .`: validation passed.
- `python3 -m compileall -q engineering_method scripts tests` and
  `bash -n scripts/task-brief scripts/review-package`: exit 0.
- `git diff --check`: exit 0.
- Retrieved `SKILL.md` and `LICENSE` from the pinned upstream revision and
  independently recomputed their SHA-256 values plus the adapted destination
  hash: all matched `third-party/sources.lock.json`. Other upstream mappings
  were unchanged; a full multi-source provenance audit was not rerun.
- Independent read-only review of the complete EM-011 diff and untracked
  skill: no Critical or Important findings. The minor finding about outdated
  small-scale evidence wording is corrected above.

## Limits

- No native host evaluation. Whether a given model actually obeys the
  constraints while drafting is a behavior claim outside these contract tests.
- The upstream word list changes with model releases; refreshing it means
  re-pinning the source revision and updating both hashes.
