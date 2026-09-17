# Implementation Plan: Engineering playbooks

## Stable work ID

EM-014; specification: [spec.md](spec.md).

## Summary

Add two supporting skills, shared playbook policy and two templates. Embed phase-specific need, task and acceptance handoffs in the existing engineering skills and templates. Keep lifecycle executors and runtime code unchanged.

## Project gates

English artifacts; local canonical backlog; risk-proportionate checks; independent integration review; pinned MIT provenance. Baseline: 319 tests passed on bda1eac. User approved local implementation, not publication.

## Technical context and interfaces

Markdown skills and templates; Python standard-library test and validation tooling. New skills are discovered through the existing skills directory on all hosts. The coordinator owns lifecycle state. Supporting skills return artifact paths and findings to it.

## Architecture findings

AF-001: Existing skill-discovery and supporting-skill boundaries suffice. No runtime component, storage schema, concurrency boundary or host adapter is added. A new UML cycle would not answer an additional design question; record the existing boundary here and verify handoffs directly.

## Implementation structure

- shared/policies/playbooks.md: need assessment, ownership, lifecycle handoffs, evidence states.
- skills/playbook-authoring and skills/playbook-review: adapted medzin mechanics and selected Test Double provenance/validation rules.
- templates/playbooks: operational artifact and separate review/rehearsal evidence.
- Existing Spec Kit, OpenSpec, architecture and implementation skills/templates: narrow integration sections.
- Trigger fixtures, provenance lock, notices, README/usage, backlog and feature inventory.

## Compatibility and rollback

Preserve all existing lifecycle controllers and source revisions. Pin additional sources; refresh only changed destination hashes. Reverting this feature restores the previous instruction set; no data migration exists.

## Tests

Run existing suite and validators, add routing cases for new-system need, critical development operation, authoring, review and small-change exclusion. Check supporting handoff integrity locally. Use one independent review with bounded scenario checks. No claims of native model routing or real operational execution.
