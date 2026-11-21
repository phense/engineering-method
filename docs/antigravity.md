# Antigravity integration

Engineering Method ships a native Antigravity plugin manifest at
`.antigravity-plugin/plugin.json` and bundles the shared
[Antigravity adapter](../shared/platform/antigravity.md) from Method Core.
It exposes the same 19 engineering and shared support skills used by Claude,
Codex, and OpenCode, and coexists cleanly with
[Writing Method](https://github.com/phense/writing-method).

## Install for Antigravity CLI, App, and IDE

Requires Python 3.11+, Git, and Antigravity (`agy`). Validate and install from
a local checkout or extracted release archive:

```sh
agy plugin validate --strict /absolute/path/to/engineering-method
agy plugin install /absolute/path/to/engineering-method
agy plugin list --json
```

Alternatively, install directly from GitHub:

```sh
agy plugin install https://github.com/phense/engineering-method
```

If an older imported copy (for example, an earlier `claude-code` import) is
already installed under `~/.gemini/config/plugins/engineering-method`, remove
it first with `agy plugin uninstall engineering-method` before installing the
native plugin.

Start a new Antigravity session after installing or updating so the refreshed
skill inventory is loaded.

## Install into a custom config directory or T3 Code

Hosts that launch `agy acp` with a separate `--gemini-dir` (such as T3 Code's
per-provider Antigravity directory) maintain their own `<gemini-dir>/config`
root rather than reading `~/.gemini/config/plugins/`. Use the bundled
ownership-checked installer to install or update a clean copy in any
Antigravity config directory:

```sh
python3 scripts/install-antigravity --check --config-dir /absolute/antigravity/config
python3 scripts/install-antigravity --config-dir /absolute/antigravity/config
```

The installer copies only clean plugin files (excluding `.git`, `dist`,
`__pycache__`, and local state), preserves script execute bits, and writes an
ownership marker so future updates or `--uninstall` calls never overwrite or
delete foreign or locally modified plugin directories. Existing `config.json`,
`mcp_config.json`, `hooks.json`, and other installed plugins remain untouched.

## Coexistence with Writing Method

Both `engineering-method` and `writing-method` install into the same
`<config-dir>/plugins/` directory as independent plugins. When both are active,
use the invoking method's copy of shared support skills once rather than
running duplicate copies.

## Update and remove

For standalone Antigravity (`~/.gemini/config/plugins/`):

```sh
agy plugin uninstall engineering-method
agy plugin install /absolute/path/to/engineering-method
```

For installations managed by `scripts/install-antigravity`:

```sh
# Update in place after pulling or extracting a new revision
python3 scripts/install-antigravity --config-dir /absolute/antigravity/config

# Remove only the unmodified managed copy
python3 scripts/install-antigravity --uninstall --check --config-dir /absolute/antigravity/config
python3 scripts/install-antigravity --uninstall --config-dir /absolute/antigravity/config
```

Uninstalling never removes `BACKLOG.md`, `FEATURES.md`, specs, diagrams, or
`.engineering-method/` state in target projects.

## Verification scope

Native validation (`agy plugin validate --strict`), isolated clean installation
(`agy plugin install` and `agy plugin list --json` in a disposable `HOME`),
and coexistence with Writing Method were verified with `agy` 1.5.14 on macOS.
Discovery and manifest validation do not constitute live multi-run model
routing acceptance on Antigravity.
