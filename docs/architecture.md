# Architecture

The cloud model is the clever companion. The local domain core is the sober rules clerk.

## Trust boundary

```text
submitted text
  → interpreter (may call a model)
  → retrieval (local)
  → structured proposal (model)
  → validation + reducers (local, deterministic)
  → confirmation gate (Tyler / physical table)
  → event append + snapshot (local)
  → Noko response (model or template; never writes state)
```

A model response cannot write `state.json`. Only `CampaignRepository.commit` persists, and only confirmed, validated events.

## Layers

```text
interfaces/     TurnInput / TurnOutput, JSON Schema loaders
companion/      one orchestrator; referee, clerk, narrator are functions
model/          provider protocol + fake adapter
knowledge/      citations, card lookup, rules search
campaign/       repository, JSONL event log, snapshots, migration stub
domain/         typed state, events, phases, reducers, invariants
data/           persona, sources manifest, campaign files
```

Alpha uses **one orchestrator**, not an agent swarm.

## Canonical paths

| Thing | Path |
| --- | --- |
| Noko persona | `data/games/arkham-horror/persona.md` |
| Game notes / sources | `data/games/arkham-horror/` |
| Campaign | `data/campaigns/night-of-the-zealot/campaign.json` |
| Live table | `data/campaigns/night-of-the-zealot/scenarios/the-midnight-masks/state.json` |
| Event log | `.../the-midnight-masks/events.jsonl` |
| Archived Gathering | `.../the-gathering/` (immutable during live play) |
| Schemas | `schemas/` |
| Sessions | `sessions/` (never canonical) |

## Decisions

1. **Language:** Python 3.11+, Pydantic v2 models, JSON Schema files for fixtures and scripts.
2. **Event storage:** append-only JSONL. SQLite may replace the log later; the `EventLog` protocol stays.
3. **Retrieval:** exact card lookup and lexical search interfaces first. No vector DB. SQLite FTS5 is the intended lexical backend; tests use an in-memory index.
4. **Existing snapshots** may contain documented inconsistencies. Loading them is allowed. New commits are held to invariants. The clerk does not auto-correct live campaign facts.
5. **Empty event log** at migration: the current `state.json` is the bootstrap snapshot. Do not invent prior events.
6. **Physical corrections** append a `physical_correction_recorded` event. History is never rewritten.
7. **Unavailable corpus:** retrieval fails honestly. The system must not claim rules readiness from a summary.
8. **Hermes:** behavioral prototype only. No auto-merge.
9. **Companion identity:** Noko. Jim is historical.
10. **UI/voice:** clients of `handle_turn`. Not part of the domain core.

## What is not implemented yet

- Cloud provider adapters (OpenAI, etc.)
- Populated private rules corpus / FTS index
- Hermes file importer
- HTTP API and local web UI
- Real-time voice
