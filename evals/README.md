# Cross-host behavioral evaluation

The shared prompts contain user requests and input files. Host-specific expected
matrices stay outside the evaluated repository and are never added to prompts.
Routing evaluations perform the first safe assessment, produce decision.md, and
require successful tool-backed skill loading as well as the selected workflow.
They do not claim that a complete feature was implemented.

Routing preambles stop after read-only prerequisite discovery: identify an
existing or absent run and its prescribed next action without initializing or
mutating canonical state. The separate architecture fixture exercises operational
phase execution. One existing-Spec-Kit evaluation timed out at 120 seconds after
correct skill reads followed by repeated initialization-related CLI discovery;
that failed evidence remains retained. This scope clarification does not raise
the routing timeout or weaken required skill-read evidence.

Adapters select the default evaluation tier: Codex routing uses fast, Claude
routing uses standard, and architectural cases use strong. In one controlled
bounded-change comparison with identical staged access, Claude's fast candidate
selected the wrong primary and omitted decision.md; the standard candidate passed.
Codex's fast candidate passed that case after prerequisite guidance was corrected.
This is limited evidence for these evaluation defaults, not a general claim about
model capability. Earlier failures remain failures; the runner does not silently
retry a different model or replace failed evidence.

Commands verified against Codex 0.153.0 and Claude Code 2.1.259:

```bash
python3 tests/e2e/run-codex-evals --output-dir /tmp/em-codex-evals
python3 tests/e2e/run-claude-evals --output-dir /tmp/em-claude-evals
```

Each invocation creates an isolated temporary Git repository and configuration
root. Existing OAuth can be used with explicit --auth-home pointing to the host's
existing configuration directory. Credentials are never read or copied by the
runner. This exception shares native authentication state, not an isolated login;
Codex ignores user configuration and uses ephemeral sessions while retaining native
safety rules. Claude omits
user/project/local settings, disables hooks and external MCP configuration, and
loads this plugin only for the invocation. --bare is unsuitable because it
disables Claude OAuth. Neither runner installs plugins globally.

Codex discovers the same skill tree through temporary .agents/skills links;
Claude uses --plugin-dir. Native package installation is a separate clean-install
gate and is not inferred from these behavioral runs.

Output directories are private. Records contain selected skills, sanitized event
types and skill paths, artifact and
transcript hashes, counts, source fingerprint, model, and explicit failure codes;
raw transcripts are retained separately with mode 0600 outside the source tree
for controlled diagnosis and are never copied into sanitized release records.
Do not publish those raw records or echo their contents without inspecting them.
Missing commands, timeout, authentication failure, malformed output, incomplete
transcripts, skill collisions, and missing tool/artifact evidence fail nonzero.
There is no success-by-skip mode. A selected --case run is a smoke, not the entire
release matrix; summary.json records requested_cases and actual results.

The matrix also contains two simulated capability observations: unavailable
subagents/worktree creation, and unavailable preferred role/optional memory/GitHub.
These test the policy response and observed absence of prohibited operations;
they do not simulate a provider outage or prove a live unavailable-model retry.
Expected fallback fields remain evaluator-only. No unavailable model request,
credential transfer, remote mutation, or global worktree change is needed.
