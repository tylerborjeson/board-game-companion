# architecture

## boundary

The companion is split into four layers:

```text
chat/web UI -> narrator adapter -> command API -> deterministic game core -> campaign store
```

The narrator receives a structured, read-only view of the current state. It returns narration, rule explanation, advice, and a proposed command. The command is validated by the game core before persistence.

## first implementation

Start with a pure domain package and JSON persistence. Move to SQLite after the state model and event contracts stabilize.

Every accepted mutation should produce an append-only event. Snapshots may be generated for fast resume, but the event history is the audit trail.

## Arkham-specific boundary

Rule sources are configured by the user. This repository stores source identifiers and integration contracts, not copyrighted rulebook text, scans, card images, or unlicensed scenario content.
