## Purpose
Expose the existing Engineering Method workflows through OpenCode's native skill and instruction interfaces.

## Requirements

### Requirement: Additive OpenCode discovery
The integration SHALL expose the repository skill tree and OpenCode adapter without modifying other effective configuration values.
#### Scenario: Existing user configuration
- **WHEN** the plugin config hook runs more than once
- **THEN** all repository skills and the adapter are registered once while existing skills, instructions, permissions, models and MCP configuration remain unchanged.

### Requirement: Owned reversible installation
The installer SHALL create only its own loader and SHALL refuse foreign content or symlinked destination parents.
#### Scenario: Check and reinstall
- **WHEN** check runs before install, or install runs twice
- **THEN** check writes nothing and reinstall leaves the same loader without duplicates.
#### Scenario: Uninstall or collision
- **WHEN** uninstall finds the exact generated loader
- **THEN** it removes that loader only; foreign or modified files are refused and preserved.

### Requirement: Honest host capability mapping
The adapter MUST resolve actual OpenCode tools and model availability without inventing asynchronous control or model switches.
#### Scenario: Missing capabilities
- **WHEN** the host cannot provide the required delegation or status evidence
- **THEN** the adapter follows the existing sequential recovery boundary or records a blocker, and does not claim independent review or full lifecycle acceptance from skill discovery alone.
