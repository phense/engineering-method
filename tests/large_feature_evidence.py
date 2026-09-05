"""Executable acceptance oracle for this checkout fixture, not a workflow router.

The checked-in review covers a content digest. Fresh verification is always a
new subprocess against that same content; historical success flags are claims.
The Mermaid checks deliberately support only this fixture's small notation.
"""

from datetime import datetime, timezone
import ast
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys


COMMAND = "python3 -m unittest discover -s integration_tests -v"
TESTS = (
    "test_checkout_success_matches_success_sequence",
    "test_commit_failure_releases_inventory_and_reverses_payment",
)


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def read(path):
    require(path.is_file(), f"missing evidence: {path}")
    return path.read_text(encoding="utf-8")


def contract(path):
    match = re.search(r"```json\n(.*?)\n```", read(path), re.DOTALL)
    require(match is not None, f"missing JSON contract: {path}")
    return json.loads(match.group(1))


def evidence_digest(project: Path) -> str:
    paths = sorted(
        list(project.glob("checkout/*.py"))
        + list(project.glob("integration_tests/*.py"))
        + list(project.glob("docs/uml/*"))
    )
    payload = {str(path.relative_to(project)): hashlib.sha256(path.read_bytes()).hexdigest()
               for path in paths if path.is_file()}
    return hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()


PROBE = '''
import json, sys
from checkout import CheckoutService, Inventory, InventoryCommitError, OrderService, Payment
class States(dict):
    def __init__(self):
        super().__init__()
        self.path = []
    def __setitem__(self, key, value):
        self.path.append(value)
        super().__setitem__(key, value)
results = {}
for mode in ("success", "recovery"):
    events, calls = [], []
    inventory = Inventory(events, fail_commit=mode == "recovery")
    order = OrderService(inventory, events)
    order.states = States()
    service = CheckoutService(order, Payment(events))
    def trace(frame, event, arg):
        if event == "call":
            owner = type(frame.f_locals.get("self")).__name__
            if owner in ("OrderService", "Inventory", "Payment"):
                calls.append(owner.replace("OrderService", "Order") + "." + frame.f_code.co_name)
    sys.setprofile(trace)
    try:
        service.checkout("probe")
    except InventoryCommitError:
        if mode != "recovery":
            raise
    finally:
        sys.setprofile(None)
    results[mode] = {"calls": calls, "events": events, "states": order.states.path}
print(json.dumps(results))
'''


def assert_large_feature(project: Path) -> dict:
    evidence = json.loads(read(project / "evidence/convergence.json"))
    for field in ("as_built_reconciliation", "derived_success_test_passed",
                  "derived_recovery_test_passed", "clean_final_review", "fresh_verification"):
        require(evidence.get(field) is True, f"missing completion claim: {field}")
    paths = {}
    for field in ("reconciliation_path", "integration_plan_path", "review_path", "verification_path"):
        path = (project / evidence[field]).resolve()
        require(path.is_relative_to(project.resolve()), f"evidence outside project: {field}")
        read(path)
        paths[field] = path

    reconciliation = contract(paths["reconciliation_path"])
    require(not reconciliation["unresolved_defects"], "unresolved architecture defects")
    require({item["finding_id"]: item["disposition"] for item in reconciliation["differences"]}
            == {"AF-001": "code_corrected", "AF-002": "code_corrected"},
            "incomplete reconciliation")
    for item in reconciliation["differences"]:
        for relative in item["evidence"]:
            path = project / relative if relative.startswith("checkout/") else project / "docs/uml" / relative
            read(path)

    plan = read(paths["integration_plan_path"])
    for test in TESTS:
        require(test in plan, f"integration plan missing test mapping: {test}")
    for name in ("component", "success-sequence", "recovery-sequence", "state"):
        require(f"docs/uml/{name}.mmd" in plan, f"integration plan missing view: {name}")
        diagram = read(project / f"docs/uml/{name}.mmd")
        for label in ("Purpose", "Source evidence", "Requirement IDs", "Notation", "Verified on"):
            require(re.search(rf"^%% {label}: \S.+$", diagram, re.MULTILINE),
                    f"diagram missing metadata: {name}/{label}")
    review = read(paths["review_path"])
    require(re.search(r"^Status: clean$", review, re.MULTILINE), "final review is not clean")
    digest = evidence_digest(project)
    require(contract(paths["review_path"])["reviewed_sha256"] == digest,
            "final review is stale for current artifacts")
    require(evidence["verification_command"] == COMMAND, "incorrect verification command")
    require(f"Command: `{COMMAND}`" in read(paths["verification_path"]),
            "verification artifact does not identify the actual command")

    started = datetime.now(timezone.utc).isoformat()
    result = subprocess.run([sys.executable, "-B", "-m", "unittest", "discover", "-s", "integration_tests", "-v"],
                            cwd=project, capture_output=True, text=True, timeout=30)
    output = result.stdout + result.stderr
    require(result.returncode == 0, f"fresh integration verification failed:\n{output}")
    for test in TESTS:
        require(re.search(rf"^{test} .* \.\.\. ok$", output, re.MULTILINE),
                f"required integration test did not pass: {test}")
    require("Ran 2 tests" in output, "unexpected integration test inventory")
    probe = subprocess.run([sys.executable, "-B", "-c", PROBE], cwd=project,
                           capture_output=True, text=True, timeout=30)
    require(probe.returncode == 0, f"runtime architecture probe failed: {probe.stderr}")
    observed = json.loads(probe.stdout)
    model = json.loads(read(project / "docs/uml/as-built-model.json"))
    for relative, owner in (("ports.py", "InventoryPort"), ("order.py", "OrderService"),
                            ("inventory.py", "Inventory")):
        tree = ast.parse(read(project / "checkout" / relative))
        returns = [ast.unparse(method.returns) if method.returns else None
                   for node in tree.body if isinstance(node, ast.ClassDef) and node.name == owner
                   for method in node.body if isinstance(method, ast.FunctionDef) and method.name == "reserve"]
        require(returns == [model["component"]["reserve_returns"]] == ["Reservation"],
                f"implemented reserve contract differs from component model: {owner}")
    for mode in ("success", "recovery"):
        diagram = read(project / f"docs/uml/{mode}-sequence.mmd")
        messages = [f"{target}.{method}" for target, method in
                    re.findall(r"\w+->>(\w+): (\w+)\(", diagram)]
        require(messages == observed[mode]["calls"], f"{mode} diagram differs from executed calls")
    require(model["success_sequence"]["messages"] == observed["success"]["events"],
            "success model differs from executed events")
    recovery = model["recovery_sequence"]
    require(observed["recovery"]["events"][-5:] ==
            [recovery["failure"], recovery["transition"], *recovery["compensation"], recovery["terminal"]],
            "recovery model differs from executed events")
    state = read(project / "docs/uml/state.mmd")
    edges = set(re.findall(r"(\[\*\]|\w+) --> (\[\*\]|\w+)", state))
    actual_edges = set()
    for mode in ("success", "recovery"):
        states = ["[*]", *observed[mode]["states"], "[*]"]
        actual_edges.update(zip(states, states[1:]))
    require(edges == actual_edges, "state diagram differs from executed transitions")
    require(set(model["state"]["states"]) == {state for edge in actual_edges for state in edge} - {"[*]"},
            "state model differs from executed states")
    component = read(project / "docs/uml/component.mmd")
    for edge in ("checkout[\"CheckoutService\"] --> order[\"OrderService\"]",
                 'order -->|"InventoryPort.reserve(order_id) returns Reservation"| inventory["Inventory"]',
                 'checkout -->|"capture/reverse PaymentReceipt"| payment["Payment"]',
                 'checkout -->|"commit/release Reservation"| inventory'):
        require(edge in component, f"component diagram missing implemented relationship: {edge}")
    require(evidence_digest(project) == digest, "artifacts changed during verification")
    return {"started_at": started, "completed_at": datetime.now(timezone.utc).isoformat(),
            "verified_sha256": digest, "command": result.args, "returncode": result.returncode,
            "output": output, "observed": observed}
