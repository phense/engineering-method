# Change Design: OpenCode skill integration

## Context
Baseline ff92f44 has 17 skills, Claude/Codex host adapters and 308 passing tests. A disposable native OpenCode 1.18.30 plugin config hook successfully exposes the entire repository skills directory.

## Interface contracts
A dependency-free ESM module returns a config hook. It appends absolute repository skills and adapter instruction paths, deduplicates its own entries, and preserves other configuration. Root resolution follows the actual module location.
A Python installer creates only plugins/engineering-method.js under the selected OpenCode config directory. That loader imports the source module by file URL. It supports install, check and uninstall, refuses symlink parents and foreign/modified files, and does not parse provider configuration.

## Dependencies
Python 3.11+ and an OpenCode host supporting config hooks, instructions and skills.paths. No npm dependencies. Existing Python state scripts remain usable.

## Tests
First execute installer and hook tests expecting failure before implementation. Cover real files, paths with spaces, repeated install, check without writes, foreign loader and symlink rejection, removing only owned bytes, configuration preservation and native discovery.
Use date-backed stdout files for native debug output because large piped skill JSON is truncated by the tested CLI.

## Decisions
Use a source-linked loader instead of copying skill files: this preserves relative resource paths and keeps one maintained skill tree. Load the host adapter as instructions; preserve native per-skill triggers without a central workflow router. Do not select models or permissions in the plugin.

## Risks and rollback
Retain the source path; checkout updates take effect after OpenCode restarts. Same-name skills from other packages can collide; inspect discovery and remove overlapping methodology installations deliberately. Uninstall only the exact owned loader. RAG and cloud credentials are not installer inputs.
