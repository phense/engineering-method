# Diagram Metadata

```json
{
  "required": ["purpose", "source_evidence", "requirement_ids", "notation", "verified_on"],
  "verified_on_format": "YYYY-MM-DD"
}
```

Use these comments at the top of every `.mmd` file:

```text
%% Purpose: <one named design or verification question>
%% Source evidence: <repository paths, symbols, commands, or artifact sections>
%% Requirement IDs: <stable comma-separated IDs>
%% Notation: Mermaid <diagram kind>
%% Verified on: <YYYY-MM-DD>
```

Update evidence and date whenever the diagram changes or is reconciled. A
diagram without all five values is incomplete and cannot support a finding or
integration test.
