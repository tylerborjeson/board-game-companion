# architecture

## product

Per-game companion agents, campaign state, and retrieval over authorized rulebooks. Shared behavior is game-agnostic. Each game owns sources and campaign data.

JSON is the truth of the table. Markdown is the memory of the story.

## layers that matter now

```text
AGENTS.md
  ↓ how any agent should enter
assistant/
  ↓ how to behave, roleplay, adjudicate, and store state
games/<game>/
  ↓ character, sources, campaign.json, scenario state
schemas/
  ↓ what valid state must look like
sessions/<game>/
  ↓ what happened in a chat
```

The active scenario is explicit: `campaign.json` → `active_scenario.path`. Live `state.json` must satisfy `schemas/scenario-state.schema.json`.

## later boundary

```text
chat/web UI -> narrator adapter -> command API -> deterministic game core -> campaign store
                      ^
                      retrieval over authorized rule sources
```

Rule answers should come from retrieved source passages, not model memory. This repository stores source identifiers, not copyrighted rulebook text.
