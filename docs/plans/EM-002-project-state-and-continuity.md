# EM-002 Project State and Continuity Implementation Plan

> **For agentic workers:** Use `superpowers:subagent-driven-development` after EM-001 is complete. Apply TDD, keep GitHub tests behind a fake runner, and checkpoint this plan in the repository backlog.

**Goal:** Deliver the local backlog and feature inventory, automatic idempotent migration to English GitHub Issues, offline reconciliation, and the provider-neutral compact-continuity contract.

**Architecture:** A Python 3.11+ standard-library package separates Markdown models, filesystem safety, GitHub transport, synchronization, continuity, and CLI adapters. Product truth lives in local Markdown before migration and GitHub Issues afterward; ignored `.engineering-method/` data is operational state only.

**Tech Stack:** Python 3.11+ standard library, `unittest`, Markdown, JSON/JSONL, `gh` through an injected subprocess boundary.

**Spec:** `docs/specs/2026-09-04-engineering-method-design.md`

## Global Constraints

- Existing backlog IDs never change when status, priority, or order changes.
- Ordering is unblocker-first, then priority, then dependency order; children remain with parents.
- Root `BACKLOG.md` is canonical in local mode and a generated read-only cache in GitHub mode.
- GitHub-authored titles, bodies, labels, relationship descriptions, and comments are English.
- Ordinary tests never need network access, credentials, an installed `gh`, or non-stdlib packages.
- JSON schemas start at `schema_version: 1`; state replacement is atomic and events are append-only.
- Never persist secrets, credentials, full prompts, environment dumps, or verbose tool output.
- Agentic RAG is downstream of the continuity contract and is not imported or called here.

## File Map and Public Interfaces

```text
engineering_method/
  __init__.py
  models.py
  files.py
  backlog.py
  features.py
  gh.py
  issues.py
  continuity.py
  cli.py
scripts/
  project-state
  backlog-to-issues
  refresh-issue-cache
  continuity-state
tests/
  fakes.py
  test_models.py
  test_backlog.py
  test_features.py
  test_issues.py
  test_continuity.py
  test_cli.py
```

Core types:

```python
class TaskStatus(StrEnum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    COMPLETE = "complete"
    BLOCKED = "blocked"

class Priority(StrEnum):
    P0 = "P0"
    P1 = "P1"
    P2 = "P2"
    P3 = "P3"

@dataclass(frozen=True)
class BacklogItem:
    id: str
    title: str
    status: TaskStatus
    priority: Priority
    parent_id: str | None
    depends_on: tuple[str, ...]
    notes: str
    updated_at: str

@dataclass(frozen=True)
class Feature:
    id: str
    name: str
    summary: str
    status: Literal["available", "changed", "removed"]
    related_backlog_ids: tuple[str, ...]
    updated_at: str
```

### Task EM-002.1: Add state models and safe filesystem primitives

**Files:** Create `engineering_method/{__init__,models,files}.py`, `tests/{fakes,test_models}.py`; modify `.gitignore`.

**Interfaces:**

```python
def derive_project_key(repository_name: str) -> str: ...
def parse_task_id(value: str) -> tuple[str, tuple[int, ...]]: ...
def next_child_id(parent_id: str, existing_ids: Iterable[str]) -> str: ...
def atomic_write_json(path: Path, payload: Mapping[str, Any]) -> None: ...
def append_jsonl(path: Path, record: Mapping[str, Any]) -> None: ...
def require_repo_relative(path: str) -> str: ...
```

- [ ] Write tests for `engineering-method -> EM`, explicit override preservation, valid nested IDs, malformed/lowercase/zero components, missing parents, duplicate IDs, repository traversal, and atomic replacement failure.
- [ ] Run `python3 -m unittest tests.test_models -v`. Expected red result: missing `engineering_method`.
- [ ] Implement frozen models, UTC RFC-3339 timestamps, ID validation, repository-relative paths, atomic JSON via sibling temporary file plus `fsync`/`os.replace`, and one-record-per-write JSONL append.
- [ ] Ensure `/.engineering-method/` is ignored while `BACKLOG.md` and `FEATURES.md` remain tracked.
- [ ] Re-run the tests. Expected: pass.
- [ ] Commit with `git commit -m "feat: add project-state core models"`.

### Task EM-002.2: Implement the canonical local backlog and archive policy

**Files:** Create `engineering_method/backlog.py`, `tests/test_backlog.py`, `templates/BACKLOG.md`; modify root `BACKLOG.md` only through tested rendering once compatibility with its existing IDs is proven.

**Interfaces:**

```python
@dataclass(frozen=True)
class BacklogDocument:
    project_key: str
    mode: Literal["local", "github-cache"]
    items: tuple[BacklogItem, ...]

def load_backlog(path: Path) -> BacklogDocument: ...
def render_backlog(document: BacklogDocument) -> str: ...
def ordered_items(items: Iterable[BacklogItem]) -> list[BacklogItem]: ...
def archive_completed_groups(document: BacklogDocument,
    *, active_line_limit: int = 500, target_line_limit: int = 350
) -> tuple[BacklogDocument, tuple[BacklogItem, ...]]: ...
```

- [ ] Define the parse identity marker `<!-- engineering-method:backlog {"schema_version":1,...} -->` immediately before each rendered task. Presentation remains `- <emoji> \`ID\` **P#** Title` with indented children and dependency notes.
- [ ] Write failing tests for all four statuses, immutable IDs, hierarchy, cycle detection, missing dependencies, priority sorting, blocker/unblocker ordering, and children adjacent to parents.
- [ ] Add a fixture exceeding 500 rendered lines. Assert only the oldest completed top-level groups move to `BACKLOG-ARCHIVE.md`, active/blocked/open groups never move, and the active file stops at no more than 350 lines.
- [ ] Assert archive calls fail in `github-cache` mode.
- [ ] Run `python3 -m unittest tests.test_backlog -v`. Expected red result: missing module.
- [ ] Implement parsing/rendering and update the existing root backlog without changing `EM-000` through `EM-005` identities or meanings.
- [ ] Re-run tests and commit with `git commit -m "feat: add stable blocker-first backlog"`.

### Task EM-002.3: Implement the feature inventory

**Files:** Create `engineering_method/features.py`, `tests/test_features.py`, `templates/FEATURES.md`; modify root `FEATURES.md` only after parser compatibility passes.

**Interfaces:**

```python
def load_features(path: Path) -> FeatureDocument: ...
def render_features(document: FeatureDocument) -> str: ...
def upsert_feature(document: FeatureDocument, feature: Feature) -> FeatureDocument: ...
def remove_feature(document: FeatureDocument, feature_id: str, *, rationale: str) -> FeatureDocument: ...
```

- [ ] Write tests for adding, updating, and removing a capability while preserving its stable `F-NNN` identity and related backlog IDs.
- [ ] Reject backlog-only fields such as priority, dependency, implementation status, or blocker state.
- [ ] Run `python3 -m unittest tests.test_features -v`. Expected red result: missing module.
- [ ] Implement a readable inventory with hidden validated markers, preserving the honest pre-release statement until the first capability exists.
- [ ] Re-run tests and commit with `git commit -m "feat: add feature capability inventory"`.

### Task EM-002.4: Add the testable GitHub boundary

**Files:** Create `engineering_method/gh.py`, `tests/test_issues.py`; modify `tests/fakes.py`.

**Interfaces:**

```python
@dataclass(frozen=True)
class GhResult:
    returncode: int
    stdout: str
    stderr: str

class GhRunner(Protocol):
    def run(self, args: Sequence[str], *, stdin: str | None = None) -> GhResult: ...

class GitHubIssuesGateway:
    def detect_writable_repository(self) -> RepositoryRef | None: ...
    def list_method_issues(self, repository: RepositoryRef) -> list[RemoteIssue]: ...
    def create_issue(self, repository: RepositoryRef, *, title: str, body: str,
                     labels: Sequence[str]) -> RemoteIssue: ...
    def ensure_sub_issue(self, repository: RepositoryRef, parent: int, child: int) -> None: ...
    def ensure_blocked_by(self, repository: RepositoryRef, blocked: int, blocker: int) -> None: ...
```

- [ ] Implement `FakeGhRunner` as an ordered queue of expected argument arrays and results; unexpected calls fail immediately.
- [ ] Write red tests for unauthenticated/no-remote/read-only detection, writable permissions `WRITE|MAINTAIN|ADMIN`, malformed JSON, non-zero commands, and partial responses.
- [ ] Assert production subprocess calls use argument lists and never `shell=True`.
- [ ] Run the focused test group; implement one gateway containing all current `gh` request shapes; re-run to green.
- [ ] Commit with `git commit -m "feat: add GitHub Issues boundary"`.

### Task EM-002.5: Add automatic idempotent issue migration and offline reconciliation

**Files:** Create `engineering_method/issues.py`, `scripts/{backlog-to-issues,refresh-issue-cache}`; modify `engineering_method/{backlog,cli}.py`, `tests/test_issues.py`.

**Canonical markers and labels:**

```text
<!-- engineering-method:issue {"schema_version":1,"backlog_id":"EM-002"} -->
priority:p0  priority:p1  priority:p2  priority:p3
status:open  status:in-progress  status:blocked
```

- [ ] Test migration of open, blocked, complete, parent, child, and dependent entries. All issues are created/upserted before sub-issue and dependency relationships; completed items finish closed.
- [ ] Test a second identical migration emits no duplicate create or relationship operation. Identity comes only from the embedded marker, never fuzzy title matching.
- [ ] Test automatic activation: on a workflow state check, a reachable GitHub remote plus authenticated writable permission migrates and switches canonical mode without a methodology question. The switch is committed only after all issue, relationship, and cache operations succeed.
- [ ] Test no remote, no authentication, or insufficient permission leaves local mode untouched and reports the factual reason without treating it as a workflow blocker.
- [ ] Test generated root `BACKLOG.md` begins `Generated GitHub Issues cache — do not edit` and cannot accept local canonical mutations.
- [ ] Test outage behavior after migration: append an idempotent mutation plus later acknowledgement to `.engineering-method/github-queue.jsonl`; never fabricate canonical completion in the cache. Reconciliation processes pending mutations in causal order and preserves failures.
- [ ] Test unknown/duplicate remote markers fail safely and do not claim unrelated issues.
- [ ] Require outbound issue operations to carry `language="en"`; reject any other declared language. Natural-language English correctness is enforced by skill instructions and host evals rather than an unreliable local language detector.
- [ ] Run `python3 -m unittest tests.test_issues -v`, implement migration/cache/queue behavior, and re-run to green.
- [ ] Commit with `git commit -m "feat: synchronize backlog with GitHub Issues"`.

### Task EM-002.6: Implement compact-continuity state and events

**Files:** Create `engineering_method/continuity.py`, `scripts/continuity-state`, `tests/test_continuity.py`; modify `engineering_method/{files,cli}.py`.

**Interfaces:**

```python
def create_run(root: Path, state: RunState, resume_markdown: str,
               decisions_markdown: str = "") -> Path: ...
def checkpoint(root: Path, work_id: str, state: RunState, resume_markdown: str) -> None: ...
def append_event(root: Path, work_id: str, event: Mapping[str, object]) -> dict[str, object]: ...
def recover_run(root: Path, work_id: str, *, git_probe: GitProbe,
                canonical_probe: CanonicalWorkProbe,
                live_agent_ids: Collection[str]) -> RecoveryResult: ...
```

- [ ] Write red tests for the exact `state.json`, `resume.md`, `decisions.md`, `agent-reports/`, and `events.jsonl` run tree.
- [ ] Test atomic checkpoints, schema v0-to-v1 upgrade, rejection of future schemas, and all nine allowed events from design §10.4.
- [ ] Reject unknown event kinds, absolute artifact paths, and case-insensitive sensitive keys `token`, `password`, `secret`, `authorization`, and `cookie` before any write.
- [ ] At every lifecycle boundary, test recovery against git head, artifact existence, canonical backlog/issue completion, and live-agent IDs. Completed slices stay completed; unavailable agents become redispatchable; stale state never overwrites canonical evidence.
- [ ] Implement `continuity-state init|checkpoint|event|status|recover`, accepting JSON from an explicit file or stdin and returning only concise paths/digests.
- [ ] Run `python3 -m unittest tests.test_continuity -v`, then commit with `git commit -m "feat: add compact continuity contract"`.

### Task EM-002.7: Wire project-state commands and acceptance flow

**Files:** Create `scripts/project-state`, `skills/project-backlog/SKILL.md`, and `tests/test_cli.py`; modify `engineering_method/cli.py`.

**CLI:**

```text
scripts/project-state backlog init|add|start|block|complete
scripts/project-state feature add|change|remove
scripts/backlog-to-issues migrate|reconcile
scripts/refresh-issue-cache
scripts/continuity-state init|checkpoint|event|status|recover
```

- [ ] Write a temporary-repository acceptance test: initialize local state, add/start/complete without ID changes, add a feature without task duplication, auto-migrate through fake GitHub, queue/reconcile an outage mutation, and recover the next action without redispatching a completed slice.
- [ ] Test concise non-zero failures for invalid priority, duplicate IDs, local mutation in GitHub-cache mode, malformed events, and future schemas.
- [ ] Implement executable wrappers that resolve the plugin root from `__file__` and do not depend on the caller's current directory.
- [ ] Add the host-neutral `project-backlog` skill. It owns state initialization, stable-ID updates, blocker sorting, feature-inventory handoff, automatic GitHub-mode checks, cache refresh, and continuity pointers; it never selects an implementation methodology.
- [ ] Run:

  ```bash
  python3 -m unittest discover -s tests -t . -v
  python3 -m compileall -q engineering_method scripts
  python3 scripts/validate-plugin
  git diff --check
  ```

- [ ] Update `BACKLOG.md`: mark `EM-002` complete only after all acceptance evidence is fresh.
- [ ] Commit with `git commit -m "feat: complete project state and continuity"`.

## EM-002 Acceptance Evidence

- Full standard-library test suite passes without live GitHub.
- Local IDs, blocker ordering, and archive thresholds are proven.
- GitHub migration is automatic, English-only by contract, relationship-aware, and idempotent.
- Offline changes remain queued without creating a second canonical truth.
- Recovery resumes the validated next action after compaction without duplicate work.
- Agentic RAG can consume events later without being a runtime dependency.
