# Change Proposal: OpenCode skill integration

## Stable work ID
- Work ID: EM-008
- Change ID: opencode-integration
- Status: Approved by the user's implementation request

## Why
OpenCode does not discover the existing Claude/Codex plugin caches. Its verified 1.18.30 config hook and skills.paths can expose the unchanged shared skill tree.

## Changed requirements
See specs/host-integration/spec.md.

## Acceptance criteria
- AC-001: Installation exposes all 17 repository skills and the OpenCode adapter.
- AC-002: Existing configuration, providers, credentials, permissions and MCP settings remain unchanged.
- AC-003: Reinstall is idempotent; check is read-only; foreign or modified loader files are refused.
- AC-004: Native discovery and a bounded real skill invocation pass; documentation distinguishes this from full workflow acceptance.

## Compatibility boundaries
Source-linked installation requires a retained checkout or extracted package. Existing Claude/Codex adapters and shared skills remain unchanged. Removing the owned loader reverses integration after the helper restarts.

## Scope
In scope: additive OpenCode loader, guarded installer, host adapter, tests and docs.
Out of scope: automatic DeepSeek quality routing, RAG lifecycle hooks, full cross-host release evaluation, remote publication.

## Escalation check
New subsystem: No. Tightly coupled multi-component reach: No. Risky migration: No. Material architecture uncertainty: No.
