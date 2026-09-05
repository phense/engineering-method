# Installation and maintenance

Use a supported Codex CLI or Claude Code, Python 3.11+ and Git. Commands below
run in a terminal. Start a new host session after changing installed plugins.
The tested versions are Codex CLI 0.153.4 and Claude Code 2.1.259 on macOS;
installation success does not establish live model behavior on every host.

## Install from GitHub

The marketplace and plugin both use the name `engineering-method`.
These commands follow `main`:

```sh
codex plugin marketplace add phense/engineering-method
codex plugin add engineering-method@engineering-method
codex plugin list --json
```

```sh
claude plugin marketplace add phense/engineering-method
claude plugin install engineering-method@engineering-method
claude plugin list --json
```

For stable version 0.1.0 on either host, clone the release tag and register the
absolute checkout path instead of the GitHub shorthand:

```sh
git clone --branch v0.1.0 --depth 1 https://github.com/phense/engineering-method.git
cd engineering-method
em_plugin="$(pwd)"
codex plugin marketplace add "$em_plugin"
codex plugin add engineering-method@engineering-method
claude plugin marketplace add "$em_plugin"
claude plugin install engineering-method@engineering-method
```

Choose one source per marketplace name. If switching an existing local
marketplace to GitHub, uninstall this plugin and remove its marketplace using
the commands below, then register the new source. Preserve your project files.

Alternatively, download `engineering-method-0.1.0.zip` and
`SHA256SUMS` from the [0.1.0 release](https://github.com/phense/engineering-method/releases/tag/v0.1.0).
In the download directory, run `shasum -a 256 -c SHA256SUMS`, extract the archive,
and register the extracted `engineering-method` directory as above.
The plugin manifests and stable Git tag identify version `0.1.0`. The older
`v0.1.0-rc.1` pre-release remains available for historical reference.

Claude also supports a session-only load:

```sh
claude --plugin-dir "$em_plugin"
```

Run the host from your target project and retain the absolute plugin path.
Bundled scripts are resolved from the installed skill directory, then executed
with the target project as the working directory.

## Update

For a GitHub marketplace following `main`, refresh its source and replace the
installed cache. Removing this plugin does not remove your project's artifacts.

```sh
codex plugin marketplace upgrade engineering-method
codex plugin remove engineering-method@engineering-method
codex plugin add engineering-method@engineering-method
```

```sh
claude plugin marketplace update engineering-method
claude plugin update engineering-method@engineering-method
```

For a local fixed checkout/package, obtain the desired revision first, then
reinstall from that directory. Do not assume refreshing a local marketplace
pulls Git changes. Restart the session and inspect the plugin list after updates.

## Disable or uninstall

Claude provides an explicit disable command:

```sh
claude plugin disable engineering-method@engineering-method
```

In Codex, set the existing plugin entry in your user `config.toml` to
`enabled = false` (merge into the existing table; do not duplicate it):

```toml
[plugins."engineering-method@engineering-method"]
enabled = false
```

To uninstall and remove only this marketplace:

```sh
codex plugin remove engineering-method@engineering-method
codex plugin marketplace remove engineering-method
claude plugin uninstall engineering-method@engineering-method
claude plugin marketplace remove engineering-method
```

For a session-only Claude load, stop passing `--plugin-dir`. Uninstallation does
not delete `BACKLOG.md`, `FEATURES.md`, specs, diagrams or
`.engineering-method/` recovery data in your projects.

## Switch from Superpowers

Inspect each host's plugin list first and use the exact installed identity.
For example, when the listed identity is `superpowers@claude-plugins-official`:

```sh
claude plugin disable superpowers@claude-plugins-official
```

In Codex, set `enabled = false` in the existing
`[plugins."superpowers@claude-plugins-official"]` table. Keep unrelated plugins
and settings intact. Remove any separately installed overlapping lifecycle
skills only after identifying their source and confirming they are redundant.
Engineering Method adapts selected upstream practices; it does not need the
Superpowers plugin enabled. Also avoid duplicate Spec Kit/OpenSpec lifecycle
plugins. Inspect existing artifacts and continue their recorded phase rather
than converting or restarting work automatically.

## Troubleshooting

If skills are absent, check the installed/enabled inventory, Python version,
marketplace source and host version, then start a new session. A fresh temporary
host configuration can test installation without copying credentials. Loading
a plugin is distinct from authenticated model execution. See the
[Codex](../shared/platform/codex.md) and [Claude](../shared/platform/claude.md)
adapters for capability and authentication boundaries.
