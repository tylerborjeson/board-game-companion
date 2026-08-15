# architecture

## product

Per-game companion agents, campaign state, and retrieval over authorized rulebooks. Arkham Horror LCG is the first game. The proven loop is: confirm table state, teach the rule, advise without choosing, persist JSON after the player confirms.

## games

Each game is a self-contained package:

```text
<game>/
  skills/          companion skills (SKILL.md in the repo)
  campaigns/       durable campaign and scenario state
  pdfs/            local authorized sources (gitignored)
```

Agents read that game’s skills before play. Do not copy skills into `.cursor/skills/`; the repo copy is canonical.

## boundary

The companion is split into four layers, plus a retrieval path that is not built yet:

```text
chat/web UI -> narrator adapter -> command API -> deterministic game core -> campaign store
                      ^
                      retrieval over authorized rule sources (RAG / semantic layer)
```

The narrator receives a structured, read-only view of the current state. It returns narration, rule explanation, advice, and a proposed command. The command is validated by the game core before persistence. Rule answers should come from retrieved source passages, not model memory.

## first implementation

Start with a pure domain package and JSON persistence. Move to SQLite after the state model and event contracts stabilize.

Every accepted mutation should produce an append-only event. Snapshots may be generated for fast resume, but the event history is the audit trail.

## Arkham Horror boundary

Rule sources are configured by the user. This repository stores source identifiers and integration contracts, not copyrighted rulebook text, scans, card images, or unlicensed scenario content.
