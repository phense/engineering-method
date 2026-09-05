# Stable 0.1.0 publication

The user authorized publishing stable version `0.1.0` after the independently
accepted [EM-005 gate coverage](EM-005-acceptance.md).

The release updates public documentation and removes an obsolete pre-release
sentence from the empty feature-inventory template. Executable code, skill
instructions, host adapters, fixtures, manifests and pinned upstream sources
remain unchanged from the accepted baseline `0784c79`. Its native evidence is
reused within the recorded limits; no additional model evaluations are needed
for these documentation changes.

The distribution uses tag `v0.1.0`, asset `engineering-method-0.1.0.zip` and
`SHA256SUMS`. The earlier `v0.1.0-rc.1` tag and assets remain historical and
unchanged. Publication requires fresh local checks, deterministic packaging,
isolated installation on both hosts, and remote/download verification.

## Published and verified — 2026-09-05

- Repository: <https://github.com/phense/engineering-method> (public).
- Stable release: <https://github.com/phense/engineering-method/releases/tag/v0.1.0>.
- Tag commit: `e9f5130f3c996c36a74529a112e9142b52f492c8`.
- GitHub reports `prerelease: false`, `draft: false`; `v0.1.0` is Latest.
- Package: 190 files, SHA-256
  `d87cc0b71d1664e2c2f4ffcd78fded5459b4dbd91b4f33f5dc4d65cd61b12b82`.

Fresh checks passed: all 308 tests, portable and Claude strict validation,
three-upstream provenance audit, two byte-identical package builds, inventory
inspection, and native clean installation on both hosts. Packaged code, skill
instructions, host adapters, fixtures, manifests and source locks were compared
byte-for-byte with accepted baseline `0784c79` and matched.

The uploaded ZIP and checksum were downloaded and matched the checked local
files byte-for-byte; `shasum -a 256 -c SHA256SUMS` passed. The documented fixed-tag
clone resolved to the tag commit and matched every packaged file. Both that
checkout and the direct GitHub marketplace source installed successfully on
Claude and Codex in temporary configurations, without credentials, model requests
or active-installation changes.

Local verification artifacts: `/tmp/em007-stable-release/clean-install.json`,
`github-install.json` and `downloaded/`. The EM-005 evidence limits remain in force;
stable publication does not rewrite historical failed gates.
