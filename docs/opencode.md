# OpenCode integration

Engineering Method exposes its shared skills through OpenCode's native skill
tool. The recorded discovery evidence covers the 17 skills of version 0.1.1;
the current main branch adds eight documentation skills that load from the same
directory. A local plugin config hook adds the skill directory and
[OpenCode adapter](../shared/platform/opencode.md) to effective configuration.
It leaves existing model, permissions, provider and MCP settings untouched.

## Install from a retained checkout

Requires Python 3.11+ and OpenCode; native validation used OpenCode 1.18.30 on
macOS. Use version 0.1.1 or newer; the earlier v0.1.0 release predates this
integration. Clone a retained checkout and install from it:

```sh
git clone --branch v0.1.1 --depth 1 https://github.com/phense/engineering-method.git
cd engineering-method
```

```sh
python3 scripts/install-opencode --check
python3 scripts/install-opencode
opencode debug skill > /private/tmp/engineering-method-skills.json
```

The installer creates only `~/.config/opencode/plugins/engineering-method.js`
and missing parent directories. It respects `XDG_CONFIG_HOME`; pass
`--config-dir /absolute/config/directory` for a custom OpenCode configuration.
If you run OpenCode with `OPENCODE_CONFIG_DIR`, pass that same directory explicitly
to the installer. Symlinked destination parents and foreign or modified loaders
are refused. On macOS use canonical `/private/tmp`, not its `/tmp` symlink, for
disposable installations. `--check` describes an action and writes nothing; a
successful check does not mean installation already exists.

The loader imports the retained source with a file URL. Keep the checkout or
extracted package at that path. Updates become effective after the OpenCode
helper restarts. Moving a source requires uninstalling its exact loader with the
old `--source-root` and installing again with the new path. Do not overwrite an
unrecognized loader. Relative resources continue to resolve within the original
skill tree; scripts operate on the user's target project.

## Use from T3 Code

Install on the machine running OpenCode (the Mac in a remote T3 environment).
Finish active work, refresh provider status and start a new thread. A cached
helper may need to be idle for at least 30 seconds or restarted before the new
plugin is loaded. T3 and standalone CLI sessions can expose different tool and
permission sets; verify the new thread can load a named skill.

For a small check, ask the model to load `verification-before-completion` with
the skill tool, execute a harmless verification command and report the observed
result. Skill discovery alone is not evidence of actual invocation. A conflicting
same-name skill may win discovery: inspect its returned source location.
OpenCode 1.18.30 can truncate large piped JSON on exit, so write `debug skill`
output directly to a file before parsing it.

## Remove

From the original source, or with its original absolute `--source-root`:

```sh
python3 scripts/install-opencode --uninstall --check
python3 scripts/install-opencode --uninstall
```

Only the byte-for-byte matching generated loader is removed. Other plugins,
configuration and project artifacts remain. Restart the helper or start a fresh
host session to remove the effective instructions.

## Scope of verification

See [EM-008 evidence](verification/EM-008-opencode.md). Native discovery and a
bounded DeepSeek skill invocation cover this adapter, not every lifecycle or
multi-agent workflow. The shared Claude/Codex skills were not modified.

Model choice remains the user's selection. The integration installs no automatic
Flash/Pro quality router or LiteLLM. Existing read-only agentic-rag MCP access is
separate; session recall, transcript ingestion and compaction hooks are not
implemented here. Do not infer those capabilities from skill installation.

## API references

Checked 2026-09-11 against the official [skills](https://opencode.ai/docs/skills/),
[plugins](https://opencode.ai/docs/plugins/) and
[configuration](https://opencode.ai/docs/config/) documentation, plus the
[v1.18.30 plugin hook interface](https://github.com/anomalyco/opencode/blob/v1.18.30/packages/plugin/src/index.ts).
