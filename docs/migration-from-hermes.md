# Migration from Hermes

Hermes is the validated **behavioral prototype**. This repository is the canonical **product source and architecture**. They are not synchronized.

## What Hermes is

The Noko voice, one-step play loop, physical-table authority, and “mentor not investigator” rules were proven in Hermes-local play. Alpha should feel like that experience.

## What this repo is not

- Not a live mirror of Hermes-local campaign files
- Not authorized to auto-merge Hermes state into Git
- Not a second competing campaign runtime once migration tooling exists

Until an import command exists and Tyler confirms a diff, treat Hermes-local files as the operational table if they are the ones actually on the physical desk. This Git snapshot is a checkpoint, not a claim of sync.

## Target import/export

Future command shape:

```text
export Hermes-local campaign
  → validate against schema
  → import into repository campaign format
  → show diff
  → Tyler confirms
  → commit snapshot/events
```

Defined bundle (not yet a Hermes reader):

```json
{
  "format": "board-game-companion.campaign-bundle/v1",
  "campaign": {},
  "scenarios": {
    "the-midnight-masks": {
      "snapshot": {},
      "events": [],
      "notes": ""
    }
  }
}
```

`src/board_game_companion/campaign/migration.py` can export this bundle and preview a diff. It refuses to commit when snapshots conflict unless Tyler explicitly confirms. It never auto-merges.

## Current campaign bootstrap

The Midnight Masks `state.json` is a **materialized checkpoint** copied from the pre-rebuild live table. `events.jsonl` is empty on purpose: prior play was not recorded as typed events. Replay of an empty log returns the checkpoint unchanged.

Do not synthesize a fake event history for Peter Warren, Ruth Turner, or doom.

## Identity

Canonical companion name is **Noko**. Jim remains only in git history and any marked historical notes.
