# State and events

## State rules

- `state.json` is the current materialized physical-table snapshot
- The physical tabletop wins over files
- Only confirmed facts enter canonical state
- Hidden deck order and unrevealed information are never invented
- Archived scenarios are immutable during live play
- Campaign-level consequences wait for Tyler's confirmation
- Story notes do not duplicate mechanical state

## Separate these

| Concept | Meaning |
| --- | --- |
| raw input | what Tyler dictated |
| interpretation | what the model thinks he meant |
| proposal | typed events suggested by the model |
| validation | deterministic legality / invariant result |
| confirmation | whether the physical result is confirmed |
| commit | event append + state reduction |

The model can propose. Local code validates and commits.

## Event envelope

```json
{
  "event_id": "uuid",
  "type": "enemy_defeated",
  "occurred_at": "2026-08-15T18:00:00+00:00",
  "round": 6,
  "phase": "investigation",
  "source": "tyler_reported",
  "confirmed": true,
  "payload": {}
}
```

Types include: `action_started`, `skill_test_declared`, `skill_test_resolved`, `card_played`, `enemy_defeated`, `clue_discovered`, `clue_spent`, `cultist_revealed`, `enemy_moved`, `enemy_attack_resolved`, `phase_advanced`, `resource_gained`, `damage_assigned`, `horror_assigned`, `physical_correction_recorded`, `session_paused`.

## Invariants

- Legal phase order: Mythos → Investigation → Enemy → Upkeep → Mythos
- Action count cannot be negative or exceed the investigation-phase allotment
- Clues, resources, damage, and horror cannot become invalid
- Engaged enemies share the investigator's location
- Defeated enemies cannot attack or move
- Agenda/act and doom fields are checked; mismatches halt for confirmation instead of being “fixed”
- Event time/order is monotonic
- Replaying confirmed events from a base snapshot reproduces the materialized state

## Physical corrections

A correction is a new event (`physical_correction_recorded`). It does not delete or edit earlier lines in `events.jsonl`.

## Bootstrap

The current Midnight Masks snapshot is a checkpoint with an empty event log. That is intentional. See `docs/migration-from-hermes.md`.
