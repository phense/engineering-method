---
name: project-backlog
description: "Maintain stable local or GitHub-canonical backlog and feature state, including automatic writable-GitHub checks and compact-continuity pointers; do not select an implementation methodology."
---

# Project Backlog

Use this skill when work needs durable task, capability, or continuity state. It owns stable IDs, blocker-first ordering, feature-inventory handoff, state checks that automatically migrate to writable authenticated GitHub Issues, cache refresh, and recovery pointers.

Keep local `BACKLOG.md` canonical until a workflow state check finds a writable authenticated GitHub remote. Then migrate without asking a methodology question, keep GitHub-authored content in English, and treat the generated cache as read-only. Preserve IDs across every status, priority, and ordering change.

Keep capabilities in `FEATURES.md`, not as duplicate tasks. Record recovery facts in `.engineering-method/runs/` without secrets or full prompts. Follow applicable project controls before mutations and report a factual no-remote or no-authentication outcome without treating it as a workflow blocker.
