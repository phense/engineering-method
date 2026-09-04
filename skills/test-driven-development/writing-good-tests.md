# Writing Good Tests

A test earns maintenance cost by catching a realistic bug through observable
behavior.

## Name the break

Before the body, state the production mutation that should make the test fail.
It should be a wrong branch, missing side effect, invalid argument, boundary
error, broken contract, or unsafe default. If only an intentional wording or
private-structure decision can fail it, test the behavior that depends on that
decision instead.

Derive expected values independently with literals or hand-checked fixtures.
Never calculate the expectation with the code or helper under test.

## Exercise the real behavior

Run scripts, artifacts, and components and assert outputs, exit status, state
changes, or externally visible effects. Source-text checks prove only that text
exists. Framework internals and trivial forwarding belong to their maintainers;
test the contract this project makes at its boundary.

## Use doubles narrowly

Before replacing a dependency, list the real operation's side effects. Keep all
side effects the test relies on real and replace only the slow, destructive, or
external boundary below them. A double must mirror the complete documented data
shape and reject unexpected arguments when arguments are part of the contract.

Do not assert that a mock was rendered or called merely because it is a mock.
Assert the real component's consumer-visible result. When setup for doubles is
larger than the behavior under test, use a real-component integration test.

Test-only cleanup and helpers stay in test utilities, never in production types
unless production owns that resource lifecycle.

## Mutation check

Before finishing, mentally try the relevant mutations:

- wrong branch or argument;
- missing state change or side effect;
- empty or default return;
- missing validation for empty, zero, malformed, unauthorized, or boundary
  input;
- incorrect ordering across an observable interface.

At least one test must fail for each realistic mutation in scope. An uncaught
mutation marks behavior that is unprotected or a test that is tautological.

## Quick reference

| Situation | Test response |
|---|---|
| Expected value shares implementation logic | Replace it with a hand-derived literal |
| Assertion targets a mock | Exercise the real component or remove the assertion |
| External dependency is slow | Replace only that boundary and preserve local side effects |
| Test checks a script or document | Execute the artifact and inspect effects |
| Cleanup exists only for tests | Move it to a test utility |
| Mock setup dominates | Prefer an integration test with real components |
