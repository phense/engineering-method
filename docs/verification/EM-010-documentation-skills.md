# EM-010 documentation and reader-oriented writing skills

Date: 2026-09-16. Base: `137306c` (v0.1.1). Adds eight original skills, two
shared policies, one shared writing checklist and five templates. No upstream
file was copied; the third-party source lock and notices are unchanged.

## What was added

- Scale decision: `shared/policies/writing-depth.md` decides small, medium or
  large writing work from observable conditions and names the lifecycle per
  scale. `shared/policies/lifecycle-selection.md` gained the two documentation
  entries; `shared/policies/lifecycle-handoffs.md` gained the documentation
  nodes, a fourth executor and a review-to-authoring retry transition.
- Lifecycle skills for documentation sets: `documentation-planning`,
  `documentation-authoring`, `documentation-review`, with the shared recovery
  preamble and operational state handoffs of the other stateful lifecycles.
- Didactic supporting skills, also applied to ordinary replies through
  `shared/policies/reader-oriented-output.md`: `explaining-concepts` (Feynman
  technique, analogy before mechanism, jargon rule), `writing-procedures`
  (action-oriented reader, imperative single-action steps, three to five steps
  per block, goal, prerequisites, steps, validation), `empathic-troubleshooting`
  (symptom first, causes by likelihood, first check, fix, confirmation).
- The curse-of-knowledge filter is a shared checklist,
  `shared/writing/curse-of-knowledge-filter.md`, invoked by all three didactic
  skills rather than a competing skill.
- Structural supporting skills: `terminology-guard` (glossary as contract,
  avoid-lists, exact search) and `visual-placeholders` (standardized image
  callouts with stable IDs, alt text and capture instructions, asset manifest).
  Modular chunking lives in `documentation-planning` and the chunk template.
- Templates under `templates/documentation/`: plan, chunk, glossary, assets,
  review. Host adapters point to the reader-oriented output policy; the
  OpenCode adapter is loaded as an instruction, so the policy is active there.

## Local checks

Recorded from the commands in CONTRIBUTING after the change:

- `python3 -m unittest discover -s tests -t . -v`: 317 tests, all passed.
  The suite count is unchanged because the new coverage extends existing
  contract tests with additional subtests and matrix cases.
- `python3 scripts/validate-plugin` and `claude plugin validate --strict .`:
  passed.
- `python3 -m compileall -q engineering_method scripts tests` and
  `git diff --check`: passed.

Contract coverage added: the three documentation lifecycles are part of the
stateful-lifecycle contract tests; the trigger matrix has three new cases
(standalone document, documentation set, existing documentation plan) and all
existing cases now prohibit the documentation entries; the handoff graph test
requires the documentation executor and retry transition; bundled resource
links of all eight skills must resolve inside the installed tree.

## Limits

- No native host evaluation was run for the new routing cases. The prompts
  and expected matrices exist under `evals/` for both hosts but require paid
  execution under separate authorization.
- OpenCode discovery of the new skills was not re-verified natively; the
  adapter adds the whole skills directory, so discovery is expected but not
  proven here.
- Analogy-before-mechanism ordering in `explaining-concepts` is the plugin's
  design choice requested by the maintainer; the published Feynman-technique
  guides place analogies in a refinement step. The three-to-five-step block
  limit is stricter than Microsoft's historical seven-step guidance and
  Google's absence of a limit.

## Sources consulted

Consulted on 2026-09-16 as authoring guidance only; no text was copied, and
none becomes a runtime dependency.

- Google developer documentation style guide: procedures, jargon, images,
  word list (CC BY 4.0). https://developers.google.com/style/procedures ,
  https://developers.google.com/style/jargon , https://developers.google.com/style/images
- Google Technical Writing One, "Words". https://developers.google.com/tech-writing/one/words
- Microsoft Writing Style Guide: step-by-step instructions, describing UI
  interactions, formatting text in instructions, alternative text (CC BY 4.0).
  https://learn.microsoft.com/en-us/style-guide/procedures-instructions/writing-step-by-step-instructions
- plainlanguage.gov guidelines (public domain): active voice, address the
  user, lists, main idea before exceptions. https://github.com/GSA/plainlanguage.gov
- Steven Pinker on the curse of knowledge, APS Observer 2015.
  https://www.psychologicalscience.org/observer/the-curse-of-knowledge-pinker-describes-a-key-cause-of-bad-writing
- Heath and Heath, "The Curse of Knowledge", HBR 2006. https://hbr.org/2006/12/the-curse-of-knowledge
- Nielsen Norman Group, "Plain Language Is for Everyone, Even Experts".
  https://www.nngroup.com/articles/plain-language-experts/
- Farnam Street, "The Feynman Technique". https://fs.blog/feynman-technique/
- Diátaxis (CC BY-SA 4.0): map, compass, how to use, quality.
  https://diataxis.fr/
- OASIS DITA 1.3: task, troubleshooting, concept, reference and glossary
  topic types. https://docs.oasis-open.org/dita/dita/v1.3/os/part2-tech-content/archSpec/technicalContent/
- Red Hat Modular Documentation Reference Guide (CC BY-SA 4.0).
  https://redhat-documentation.github.io/modular-docs/
- Vale vocabularies and substitution rules. https://docs.vale.sh/keys/vocabularies.md
- ASD-STE100 Simplified Technical English FAQ. https://www.asd-ste100.org/STE_faq.html
- The Good Docs Project templates (MIT-0): troubleshooting, glossary,
  terminology system. https://www.thegooddocsproject.dev/template
- Write the Docs, documentation principles (CC BY-NC-SA 4.0).
  https://www.writethedocs.org/guide/writing/docs-principles/
- GitHub Docs, TODOCS placeholder convention.
  https://docs.github.com/en/contributing/collaborating-on-github-docs/using-the-todocs-placeholder-to-leave-notes
- Public agent skills inspected for structure only: anthropics/skills
  `doc-coauthoring`, github/awesome-copilot `documentation-writer` (MIT),
  obra/superpowers `writing-skills` (MIT), Wirasm/prp `prp-technical-writing`
  (MIT).
