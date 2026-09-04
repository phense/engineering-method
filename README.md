# Peter's Engineering Method

Peter's Engineering Method is a dual-host plugin foundation for
risk-proportionate engineering workflows: it establishes a common package
identity and the validation and provenance controls that later workflow work
will use with Codex and Claude.

## Foundation status

Version `0.1.0` is a pre-release foundation, not a complete workflow plugin.
It currently provides the Codex and Claude manifests, an empty shared
`skills/` directory, a dependency-free repository validator, tests, and locked
third-party provenance records. No lifecycle skills or workflow behavior are
included yet. Marketplace installation and public installation instructions
are not available at this stage.

The intended complete design is documented in the
[Engineering Method design specification](docs/specs/2026-09-04-engineering-method-design.md).
That specification describes planned capabilities; it is not a claim that
they are implemented by this pre-release foundation.

## Local validation

Run these commands from the repository root:

```sh
python3 -m unittest discover -s tests -t . -v
python3 scripts/validate-plugin
claude plugin validate --strict .
```

The last command is the installed Claude CLI validation invocation verified
for this foundation. For Codex, `codex plugin --help` currently exposes the
`add`, `list`, `marketplace`, and `remove` capabilities. It does not show a
local plugin-validation command, so this repository does not claim one and
does not modify any global marketplace.

## License and provenance

This project is distributed under the [MIT License](LICENSE). The
[third-party notices](THIRD_PARTY_NOTICES.md) and
[`third-party/sources.lock.json`](third-party/sources.lock.json) record the
pinned MIT-license provenance for GitHub Spec Kit, OpenSpec, and Superpowers.
At this foundation stage, no workflow text has been copied from those sources.
Their names identify provenance sources only and do not imply affiliation with
or endorsement by their maintainers.
