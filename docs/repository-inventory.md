# Repository inventory (Stage 1 freeze)

Recorded before the alpha rebuild so campaign facts are not silently rewritten.

## Tree at freeze

The live repository was prompt-and-file only: no `src/`, no `pyproject.toml`, no tests, no event log, no runtime validation.

```text
AGENTS.md
README.md
LICENSE
assistant/                 policy prose (not executable)
docs/architecture.md
docs/play-loop.md
examples/                  stale / stripped snapshots
games/arkham-horror/       game package + campaign JSON
schemas/                   campaign, scenario-state, thin event/command, session
scripts/arkham-card
sessions/arkham/2026-08-15-midnight-masks.md
```

Duplicate trees named `arkham/`, `arkham-horror/` (repo root), and `hermes/` were **not** present on disk. Git history still contains Hermes-era moves (`0f9ede0`, `b3bf1f6`).

## What was executable

- `scripts/arkham-card` — ArkhamDB public API lookup by collector number
- Local Learn to Play PDF at `sources/pdfs/ahc60_learn_to_play_web.pdf` (gitignored)
- JSON files that a human/agent could edit

Nothing loaded schemas at runtime. Nothing appended events. Nothing enforced phase transitions.

## Identity contradiction

Active docs and `persona.md` called the companion **Jim**. The validated Hermes experience uses **Noko**. Alpha defaults to Noko. Historical session logs are not rewritten.

## Campaign-data discrepancies (not auto-fixed)

Live table at freeze: `games/arkham-horror/campaigns/night-of-the-zealot/scenarios/the-midnight-masks/state.json` (now `data/campaigns/...`).

| Source | Claim | Action |
| --- | --- | --- |
| `state.json` | Round 6, Enemy Phase. Peter Warren in victory display. Ruth Turner at Saint Mary's. No engaged enemies. Clues 0. | Preserved as materialized snapshot |
| `notes.md` | Peter still standing, 1 health, engaged. Enemy Phase next. | Left as story memory; may lag the table |
| `fiction.md` | Peter still standing at Miskatonic | Left as story memory |
| `sessions/arkham/2026-08-15-midnight-masks.md` | Investigation complete; confirm before hunter movement and Peter's attack | Left as non-canonical log |
| `examples/arkham-midnight-masks-state.json` | Investigation phase, clues 1, empty board | Retired as a fixture label, not live state |
| `state.json` act | `cultists_in_victory_display: 0` while victory display lists Peter Warren | Surfaced, not corrected |
| `state.json` doom | Agenda doom 5, Acolyte doom 1, `doom_total_in_play` 6, threshold 6 | Preserved; treated as a confirmation-sensitive edge |

The physical tabletop still wins if Tyler reports a different board.

## Files to move, merge, rename, or archive

| Path | Disposition |
| --- | --- |
| `games/arkham-horror/{game.md,persona.md,sources/}` | Moved to `data/games/arkham-horror/` |
| `games/arkham-horror/campaigns/night-of-the-zealot/` | Moved to `data/campaigns/night-of-the-zealot/` |
| `games/` | Deprecated pointer |
| `assistant/` | Deprecated; contracts live in `docs/` and `src/.../companion/` |
| `examples/` | Deprecated; test fixtures live in `tests/fixtures/` |
| `schemas/event.schema.json`, `command.schema.json` | Replaced with typed contracts |
| `schemas/session.schema.json` | Kept; sessions remain non-canonical |
| Archived The Gathering `state.json` / `notes.md` | Moved with campaign; still immutable |
| Hermes-local campaign files | Not in this repo; see `docs/migration-from-hermes.md` |

## Tests and validation at freeze

- No `tests/` directory
- No schema-validation command
- No replay or reducer tests

## Freeze rule

No live `state.json` field was rewritten to “make it consistent.” Companion identity and file paths were updated. Event history was **not** invented; `events.jsonl` starts empty and the current snapshot is a checkpoint.
