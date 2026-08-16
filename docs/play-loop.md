# Play loop

Noko voice and authorized sources come from `data/games/arkham-horror/`. Canonical state lives under `data/campaigns/night-of-the-zealot/`.

## Live-play shape

1. Confirm the current physical state
2. Narrate 2–5 sentences of fiction
3. Identify the phase and legal actions
4. Explain the relevant rule, with a citation
5. Apply it to this board
6. Offer mentor's advice without choosing
7. Ask one question, then stop
8. After Tyler confirms a result: append events, reduce the snapshot, put story in `notes.md`

One meaningful step. Stop at the next unresolved decision.

## Runtime loop (when using the local core)

```text
Tyler speaks into Wispr Flow
  → text is submitted to the turn boundary
  → orchestrator classifies the turn
  → retrieval supplies rules/cards
  → model proposes structured events
  → local validation
  → ambiguous or unconfirmed facts are asked, not guessed
  → confirmed events commit
  → Noko answers in spoken-friendly prose
```

## Active table

`data/campaigns/night-of-the-zealot/scenarios/the-midnight-masks/state.json`

The physical tabletop remains authoritative whenever it conflicts with stored state.

The Gathering is archived. Do not use it as live state.
