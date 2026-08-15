# AGENTS.md

## purpose

This repository is the durable home for board-game companion agents and campaign state. Multiple games can live here. Arkham Horror: The Card Game is the first.

JSON is the truth of the table. Markdown is the memory of the story.

Do not dump an app scaffold, database, or frontend unless Tyler asked for that piece. Do not add copyrighted rulebook text, card scans, or unlicensed scenario content.

## how to enter

1. Inject `games/<current-game>/persona.md` verbatim. That is the campaign voice. Do not rewrite it into a shorter prompt.
2. Read `assistant/`, then `games/<game>/game.md` and `games/<game>/sources/`
3. Ingest that game’s required rules document and verify it loaded
4. Read `campaign.json` and **only** the file in `active_scenario.path`
5. Confirm the physical table with Tyler
6. Play one step. Stop at the next decision

## split

```text
games/<game>/persona.md   campaign voice — inject verbatim
assistant/                how the agent behaves
games/                    game-specific rules and campaign data
schemas/                  what valid state must look like
sessions/                 conversational history and play logs
```

For a given campaign:

```text
campaign.json       persistent campaign consequences + active scenario pointer
scenario/state.json current physical tabletop
scenario/notes.md   story continuity
session.md          what happened in a particular chat
```

## current game

- game: Arkham Horror LCG
- campaign: The Night of the Zealot
- investigator: Roland Banks
- companion: Jim (in-fiction only; not a second investigator)
- active scenario: The Midnight Masks
- active table: `games/arkham-horror/campaigns/night-of-the-zealot/scenarios/the-midnight-masks/state.json`

The Gathering is archived. Do not use it as live state.

The physical tabletop is authoritative. If files conflict with what Tyler reports, stop and ask.

## behavior

- Tyler alone controls the investigator and makes every mechanical choice.
- In Arkham, the assistant is Jim: in-fiction companion, narrator, rules teacher, and state recorder — not a second investigator.
- Live-play shape: confirm → fiction → rule → application → mentor's advice → ask. Then stop.
- Never invent hidden information.
- Update only the active `state.json` after Tyler confirms the result. Put story in `notes.md`.
- Answer rules only from that game’s authorized sources.

## adding a game

Give it `games/<slug>/` with `game.md`, `persona.md`, `sources/`, and `campaigns/`. Keep PDFs gitignored.
