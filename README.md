# board-game-companion

Companion agents for board games: per-game rules and campaigns, shared play behavior, and retrieval over authorized rulebooks.

Arkham Horror: The Card Game is the first game. More games get their own folder under `games/`.

JSON is the truth of the table. Markdown is the memory of the story.

## layout

```text
assistant/soul.md          shared companion soul (inject verbatim)
games/<game>/persona.md    this game’s character (inject verbatim)
assistant/                 how the agent behaves
games/<game>/              rules, sources, and campaign data
schemas/                   valid campaign / table / session shape
sessions/<game>/           optional play logs
```

```text
games/arkham-horror/
  game.md
  sources/
  campaigns/night-of-the-zealot/
    campaign.json
    fiction.md
    scenarios/the-midnight-masks/state.json
```

## current campaign

- *The Night of the Zealot* — Roland Banks — *The Midnight Masks*
- Active table: `games/arkham-horror/campaigns/night-of-the-zealot/scenarios/the-midnight-masks/state.json`
- Next step: Enemy Phase after round 6 investigation

The physical tabletop wins if it disagrees with these files.

## direction

Companions as agents, durable campaign JSON, later retrieval over authorized sources. Do not commit rulebook PDFs, card scans, or unlicensed scenario text.
