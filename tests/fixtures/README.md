# Test fixtures

Labeled examples. Not live campaign data.

- `midnight-masks-start.json` — copy of the current Midnight Masks checkpoint at rebuild time
- `ambiguous-doom-state.json` — same checkpoint; agenda doom 5 + Acolyte doom 1 = `doom_total_in_play` 6 against threshold 6. Do not invent a ruling.
- `peter-warren-defeated.json` — synthetic reducer case
- `invalid-state.json` — must fail schema / invariant checks
