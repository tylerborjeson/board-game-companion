# board-game-companion

Local-first tabletop companion: cited rules help, deterministic campaign state, append-only events, and Noko’s in-fiction voice.

Arkham Horror: The Card Game (2021 Revised Core Set / *The Night of the Zealot*) is the first game. Hermes is the behavioral prototype, not a synced runtime.

JSON is the truth of the table. Markdown is the memory of the story. The physical tabletop wins if it disagrees.

## current campaign

- Roland Banks — *The Midnight Masks*
- Active table: `data/campaigns/night-of-the-zealot/scenarios/the-midnight-masks/state.json`
- Companion: Noko
- This checkpoint is **not** claimed to match Hermes-local files

## what works now

- Product contracts in `docs/`
- Typed domain models, event log, reducers, phase checks
- One-turn orchestrator with a **fake** model provider
- Schema validation and the twelve alpha acceptance tests
- Revealed-card lookup: `scripts/arkham-card 141`

## what is not done

- Cloud model adapter
- Searchable private rules corpus (Learn to Play / Rules Reference body text stays local and gitignored)
- Local web UI or real-time voice
- Hermes import that writes campaign files
- Treating prompt files as a runtime

## layout

```text
data/games/arkham-horror/persona.md    Noko — inject verbatim
data/campaigns/night-of-the-zealot/    campaign + snapshots + events
src/board_game_companion/              local domain core
docs/                                  architecture and play contracts
schemas/                               JSON Schema
tests/                                 fixtures and acceptance tests
sessions/                              optional logs; not canonical
```

## setup

Python 3.11+.

```text
python3.11 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
python scripts/validate_campaign.py
```

Optional: copy `.env.example` to `.env`. Provider credentials never belong in git.

Wispr Flow: dictate externally, paste or type the text, submit one turn. See `docs/voice-interface.md`.

## source setup

Authorized source **identifiers** live in `data/games/arkham-horror/sources/`. Place the Learn to Play PDF under `data/games/arkham-horror/sources/pdfs/` (gitignored). Normalized chunks belong in the gitignored `chunks/` folders. `python scripts/ingest_sources.py` reports whether the corpus is actually available. It will not pretend a pointer file is the rulebook.

## example turns

See `docs/play-loop.md` and `tests/companion/test_orchestrator.py` for a rules question, a confirmed action, a mixed dictated turn, and an ambiguous result that must clarify instead of commit.
