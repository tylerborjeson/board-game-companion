# Retrieval and sources

Use only the authorized Arkham corpus. Do not silently substitute memory, other editions, expansions, or unauthorized scenario sources.

## Authorized corpus

Defined in `data/games/arkham-horror/sources/manifest.yaml`:

1. 2021 Revised Core Set Learn to Play
2. ArkhamDB Rules Reference
3. ArkhamDB public API — **revealed-card lookup only**

Campaign Guide and unrevealed scenario text stay out unless Tyler authorizes them.

## Alpha retrieval order

1. Exact card / collector-number lookup
2. Metadata filter (game, edition, source, card, phase, topic)
3. Lexical search (SQLite FTS5 or in-memory equivalent)
4. Optional vectors later
5. Citations on every result

Exact card lookup is a separate path from prose rules search.

## Chunk shape

Normalized private chunks (gitignored) should carry:

- source identifier
- title
- edition / scope
- page or section
- text or local reference
- card / keyword metadata
- license / provenance metadata

The repository stores identifiers and ingestion instructions. Copyrighted body text stays local.

## Honest failure

If the required corpus is not available, retrieval raises a limitation. The companion must not claim rules readiness from a summary or from model memory.

Card lookup: `scripts/arkham-card 141` or `board_game_companion.knowledge.card_lookup`. The physical card still wins if Tyler reports a conflict.
