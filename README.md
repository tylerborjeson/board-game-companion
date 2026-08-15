# board-game-companion

Multi-agent workspace for board-game companions: per-game agents, campaign tracking, and retrieval over official rulebooks.

Arkham Horror: The Card Game is the first game. The repo is meant to grow into an orchestration app — different agents for different games, campaign setup, and semantic / RAG layers over rulebooks.

## direction

- **Companions as agents.** One (or more) agents per game: narrator, rules teacher, campaign recorder. The player still makes every mechanical choice.
- **Campaigns.** Durable JSON (later: events + a store) so a session can pause and resume. Arkham Horror *Night of the Zealot* is the first campaign.
- **Retrieval.** Learn how to index authorized rule sources, retrieve the right passage for the current question, and keep copyrighted PDFs off git.

Do not commit rulebook PDFs, card scans, or unlicensed scenario text. Store source identifiers and local paths only.

## current campaign (Arkham Horror LCG)

Canonical state: `arkham-horror/campaigns/night-of-the-zealot/`

- campaign: *The Night of the Zealot*
- investigator: Roland Banks
- current scenario: *The Midnight Masks*
- next step: Enemy Phase after round 6 investigation

The physical tabletop wins if it disagrees with these files. Update state only after the table result is confirmed.

Skills (behavior, stored in this repo):

- `arkham-horror/skills/campaign-guide/SKILL.md` — Noko narrates, teaches, advises; Tyler controls Roland
- `arkham-horror/skills/rules-assistant/SKILL.md` — rules lookup from authorized sources

## layout

Each game is a folder with the same contract:

```text
<game>/
  skills/          SKILL.md agents for that game
  campaigns/       durable campaign JSON
  pdfs/            local authorized rulebooks (gitignored)
```

```text
arkham-horror/    first game
docs/             architecture notes and the play loop
schemas/          campaign / command / event JSON contracts
examples/         sample campaign payload
```

## next

Next work is likely: local gitignored rulebook storage under each game, and a retrieval path that cites the source instead of answering from memory. App UI and a game core can follow once that loop is stable.
