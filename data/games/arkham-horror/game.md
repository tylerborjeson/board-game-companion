# Arkham Horror: The Card Game

Game-specific package. Shared contracts live in `docs/` and `src/board_game_companion/`.

## When to use

Tyler is playing, resuming, or asking rules for Arkham Horror LCG — especially *The Night of the Zealot*.

## Companion

**Noko** follows Roland in the fiction. Full voice and Hermes boundaries: `persona.md` (inject verbatim). Tyler alone controls Roland. Noko is not a second investigator.

## Sources

Authorized corpus only — see `sources/manifest.yaml`:

1. 2021 Revised Core Set Learn to Play — `sources/learn-to-play.md`
2. ArkhamDB Rules Reference — `sources/rules-reference.md`
3. ArkhamDB public API — revealed-card lookup only; `sources/arkhamdb-api.md`

When Tyler gives a collector number, run `scripts/arkham-card <number>`. Do not ask him to read the card first. The physical card still wins if it conflicts.

Do not use the Campaign Guide or outside scenario text unless Tyler authorizes it.

New-session preflight: ingest the complete Learn to Play document, verify it loaded, then use the Rules Reference as a targeted lookup. If it cannot be loaded, stop. Do not claim readiness from a summary.

## Campaign files

- Campaign: `data/campaigns/night-of-the-zealot/campaign.json`
- Active table: the path in `campaign.json` → `active_scenario.path`
- Events: that scenario’s `events.jsonl`
- Story: that scenario’s `notes.md` and `data/campaigns/night-of-the-zealot/fiction.md`

## Jargon to explain once

action, asset, treachery, engage, exhausted, shroud, skill test
