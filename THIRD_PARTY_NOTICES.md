# Third-Party Notices

This plugin adapts only the files listed below from the pinned upstream revisions. Each
`LICENSE -> THIRD_PARTY_NOTICES.md` mapping is `notice-only`; adapted mappings
record both immutable source and current destination SHA-256 hashes in
`third-party/sources.lock.json`.

## Original implementation

Copyright (c) 2026 Peter Hense. MIT licensed under the repository `LICENSE`.
The Python project-state implementation, architecture-modeling and project-backlog
skills, UML templates, host adapters, evaluation and packaging tooling, and tests
are original. Shared orchestration policy is original except for the specific
adapted role, report, recovery and helper mechanics mapped below. The source lock
explicitly identifies original paths separately from adapted destinations.

Modifications replace upstream runtime dependencies with shared artifact
contracts, exclusive lifecycle boundaries, risk-proportionate depth and tested
continuity. EM-004 additionally hardens output containment, cohesive task handoffs
and architecture evidence. No upstream CLI or full methodology is redistributed.

EM-010 adds original documentation and reader-oriented writing skills, the
writing-depth and reader-oriented-output policies, the shared curse-of-knowledge
filter and the documentation templates. They were written from public style
guides and framework descriptions cited in
`docs/verification/EM-010-documentation-skills.md`; no third-party text was
copied and no upstream mapping applies.

## Spec Kit

- Repository: https://github.com/github/spec-kit.git
- Revision: `df6b3187022ce986759bd854467e8a4bb56bb0f4`
- License: MIT (`LICENSE`)
- License SHA-256: `2510b446bc1f0cf9702453075d20cd88631e20e5642658edb7325d9c1eb534f7`
- Copyright holder: GitHub, Inc.
- `LICENSE -> THIRD_PARTY_NOTICES.md: notice-only`

Adapted in EM-003:

Task 6 and its integration review further adapt the four
`skills/speckit-*/SKILL.md` destinations below to add host-observed recovery and
ordered project-state event/checkpoint handoffs.

- `templates/spec-template.md` -> `templates/spec-kit/spec.md`: adapted
- `templates/plan-template.md` -> `templates/spec-kit/plan.md`: adapted
- `templates/tasks-template.md` -> `templates/spec-kit/tasks.md`: adapted
- `templates/commands/specify.md` -> `skills/speckit-specify/SKILL.md`: adapted
- `templates/commands/plan.md` -> `skills/speckit-plan/SKILL.md`: adapted
- `templates/commands/tasks.md` -> `skills/speckit-tasks/SKILL.md`: adapted
- `templates/commands/converge.md` -> `skills/speckit-converge/SKILL.md`: adapted

MIT License

Copyright GitHub, Inc.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## OpenSpec

- Repository: https://github.com/Fission-AI/OpenSpec.git
- Revision: `e062b9572be933564ba3899d059377dfa1393e32`
- License: MIT (`LICENSE`)
- License SHA-256: `c3c7235bea1214ab62df643473975c2e8b8848f528901a976693f7d069713e64`
- Copyright holder: 2024 OpenSpec Contributors
- `LICENSE -> THIRD_PARTY_NOTICES.md: notice-only`

Adapted in EM-003:

Task 6 and its integration review further adapt the three
`skills/openspec-*/SKILL.md` destinations below to add host-observed recovery and
ordered project-state event/checkpoint handoffs.

- `skills/openspec-propose/SKILL.md` -> `templates/openspec/proposal.md`: adapted
- `skills/openspec-propose/SKILL.md` -> `templates/openspec/design.md`: adapted
- `skills/openspec-propose/SKILL.md` -> `templates/openspec/tasks.md`: adapted
- `schemas/spec-driven/templates/spec.md` -> `templates/openspec/spec.md`: adapted
- `skills/openspec-propose/SKILL.md` -> `skills/openspec-propose/SKILL.md`: adapted
- `skills/openspec-apply-change/SKILL.md` -> `skills/openspec-apply/SKILL.md`: adapted
- `skills/openspec-archive-change/SKILL.md` -> `skills/openspec-archive/SKILL.md`: adapted

Original in EM-003:

- `templates/openspec/escalation.md`: original; no upstream text was adapted

MIT License

Copyright (c) 2024 OpenSpec Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## Superpowers

- Repository: https://github.com/obra/superpowers.git
- Revision: `b36e0829c6d0140e93cfef2ca599b1b07d4a7797`
- License: MIT (`LICENSE`)
- License SHA-256: `a37e0e9697144819e1d965176ac4ae5bc3fa02d11e7812036bbcadf6dafe2400`
- Copyright holder: 2025 Jesse Vincent
- `LICENSE -> THIRD_PARTY_NOTICES.md: notice-only`

Adapted in EM-003:

Task 6 and its integration review further adapt
`skills/systematic-debugging/SKILL.md` to add host-observed recovery and ordered
project-state event/checkpoint handoffs.

- `skills/systematic-debugging/SKILL.md` -> `skills/systematic-debugging/SKILL.md`: adapted
- `skills/test-driven-development/SKILL.md` -> `skills/test-driven-development/SKILL.md`: adapted
- `skills/test-driven-development/writing-good-tests.md` -> `skills/test-driven-development/writing-good-tests.md`: adapted
- `skills/verification-before-completion/SKILL.md` -> `skills/verification-before-completion/SKILL.md`: adapted
- `skills/requesting-code-review/SKILL.md` -> `skills/requesting-code-review/SKILL.md`: adapted
- `skills/requesting-code-review/code-reviewer.md` -> `skills/requesting-code-review/code-reviewer.md`: adapted
- `skills/receiving-code-review/SKILL.md` -> `skills/receiving-code-review/SKILL.md`: adapted
- `skills/using-git-worktrees/SKILL.md` -> `skills/using-git-worktrees/SKILL.md`: adapted
- `skills/dispatching-parallel-agents/SKILL.md` -> `skills/dispatching-parallel-agents/SKILL.md`: adapted

Adapted in EM-004 from the pinned subagent-driven-development sources:

- `skills/subagent-driven-development/SKILL.md` -> `skills/orchestrated-implementation/SKILL.md`: adapted for cohesive slices, risk-proportionate review, and the EM-002 continuity seam
- `skills/subagent-driven-development/implementer-prompt.md` -> `shared/agent-roles/implementer.md`: adapted into a host-neutral role contract
- `skills/subagent-driven-development/implementer-prompt.md` -> `templates/orchestration/agent-report.md`: adapted into a durable report schema
- `skills/subagent-driven-development/implementer-prompt.md` -> `templates/orchestration/slice-brief.md`: adapted into a cohesive-slice brief
- `skills/subagent-driven-development/task-reviewer-prompt.md` -> `shared/agent-roles/reviewer.md`: adapted into a risk-proportionate reviewer role
- `skills/subagent-driven-development/re-review-prompt.md` -> `templates/orchestration/review-report.md`: adapted into a scoped review/fix report
- `skills/subagent-driven-development/scripts/task-brief` -> `scripts/task-brief`: adapted for Spec Kit slices and work-ID run paths
- `skills/subagent-driven-development/scripts/review-package` -> `scripts/review-package`: adapted for complete commit ranges and work-ID run paths
- `skills/subagent-driven-development/scripts/sdd-workspace` -> `shared/policies/continuity-contract.md`: adapted to consume the EM-002 run contract
- `skills/subagent-driven-development/scripts/sdd-workspace` -> `templates/orchestration/resume.md`: adapted into a compaction-safe recovery brief

MIT License

Copyright (c) 2025 Jesse Vincent

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
