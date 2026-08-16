# state management

Deprecated. Canonical layout is `data/campaigns/` and `docs/state-and-events.md`.

```text
data/campaigns/<campaign-slug>/campaign.json
data/campaigns/<campaign-slug>/scenarios/<scenario-slug>/state.json
data/campaigns/<campaign-slug>/scenarios/<scenario-slug>/events.jsonl
data/campaigns/<campaign-slug>/scenarios/<scenario-slug>/notes.md
sessions/<game>/<date>-<slug>.md
```

- `campaign.json` — persistent campaign consequences and the **active scenario pointer**
- `state.json` — current physical tabletop. Must match `schemas/scenario-state.schema.json` while `in_progress`
- `notes.md` — story continuity. Not a second state file
- `sessions/` — optional chat / play log. Not canonical

JSON is the truth of the table. Markdown is the memory of the story.

## Active scenario

`campaign.json` must name the live scenario and its path. Example:

```json
"active_scenario": {
  "slug": "the-midnight-masks",
    "path": "data/campaigns/night-of-the-zealot/scenarios/the-midnight-masks/state.json",
  "status": "in_progress"
}
```

Read and write only that `state.json` during live play. Archived scenarios stay frozen.

## Updates

- Update `state.json` only after Tyler confirms the physical result
- Do not invent hidden deck order or unrevealed information
- Do not record trauma, XP, deck changes, or campaign-log lines until Tyler confirms them
- Put fiction in `notes.md` or `fiction.md`; never copy the full JSON there
- If chat history and files disagree, ask which physical table is correct

## Live state contract

An `in_progress` scenario requires: `round`, `phase`, `actions_remaining`, `investigator`, `locations`, `enemies`, `act`, `agenda`, `decks`, `next_decision`. See `schemas/scenario-state.schema.json`.
