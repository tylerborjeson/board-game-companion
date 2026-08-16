from __future__ import annotations

from datetime import timedelta

import pytest

from board_game_companion.domain.enums import EventType, Phase
from board_game_companion.domain.events import GameEvent
from board_game_companion.domain.models import GameState
from board_game_companion.domain.phases import next_phase
from board_game_companion.domain.reducers import ReductionError, apply_event, apply_events
from board_game_companion.domain.validation import validate_event, validate_state
from tests.conftest import make_event


def test_enemy_defeated_and_clue_discovered(peter_fixture: dict) -> None:
    state = GameState.model_validate(peter_fixture["before"])
    events = [
        make_event(EventType(item["type"]), item["payload"])
        for item in peter_fixture["events"]
    ]
    result = apply_events(state, events)
    assert all(enemy.name != "Peter Warren" for enemy in result.enemies)
    assert "Peter Warren" in result.victory_display
    assert result.investigator and result.investigator.clues == 1
    assert result.locations["Miskatonic University"].clues == 0


def test_legal_phase_sequence() -> None:
    state = GameState.model_validate(
        {
            "scenario": "The Midnight Masks",
            "status": "in_progress",
            "round": 6,
            "phase": "mythos",
            "actions_remaining": 0,
            "investigator": {"name": "Roland Banks", "location": "Miskatonic University"},
            "locations": {},
            "enemies": [],
            "act": {},
            "agenda": {"doom": 0},
            "decks": {},
            "next_decision": {"type": "mythos", "prompt": "draw"},
        }
    )
    sequence = [Phase.INVESTIGATION, Phase.ENEMY, Phase.UPKEEP, Phase.MYTHOS]
    current = state
    for target in sequence:
        current = apply_event(
            current,
            make_event(
                EventType.PHASE_ADVANCED,
                {"to_phase": target.value},
                phase=current.phase or Phase.MYTHOS,
            ),
        )
    assert current.phase == Phase.MYTHOS
    assert current.round == 7
    assert next_phase(Phase.ENEMY) == Phase.UPKEEP


def test_reject_illegal_phase_action(checkpoint_state: GameState) -> None:
    event = make_event(EventType.ACTION_STARTED, {}, phase=Phase.ENEMY)
    event.phase = Phase.ENEMY
    # state is already enemy phase
    result = validate_event(checkpoint_state, event)
    assert not result.ok
    with pytest.raises(ReductionError):
        apply_event(checkpoint_state, event)


def test_unconfirmed_event_rejected(peter_fixture: dict) -> None:
    state = GameState.model_validate(peter_fixture["before"])
    event = make_event(EventType.ENEMY_DEFEATED, {"enemy": "Peter Warren"})
    event.confirmed = False
    with pytest.raises(ReductionError):
        apply_event(state, event)


def test_replay_matches_snapshot(peter_fixture: dict) -> None:
    base = GameState.model_validate(peter_fixture["before"])
    events = [
        make_event(EventType(item["type"]), item["payload"])
        for item in peter_fixture["events"]
    ]
    first = apply_events(base, events)
    second = apply_events(base, events)
    assert first.model_dump() == second.model_dump()


def test_monotonic_event_order(peter_fixture: dict) -> None:
    state = GameState.model_validate(peter_fixture["before"])
    later = make_event(EventType.ENEMY_DEFEATED, {"enemy": "Peter Warren"})
    earlier = make_event(EventType.CLUE_DISCOVERED, {"location": "Miskatonic University", "amount": 1})
    earlier.occurred_at = later.occurred_at - timedelta(minutes=1)
    with pytest.raises(ReductionError):
        apply_events(state, [later, earlier])


def test_ambiguous_doom_is_not_auto_fixed() -> None:
    from pathlib import Path

    state = GameState.model_validate_json(
        (Path(__file__).resolve().parents[1] / "fixtures" / "ambiguous-doom-state.json").read_text()
    )
    result = validate_state(state)
    assert state.doom_total_in_play == 6
    assert state.agenda and state.agenda.threshold == 6
    assert result.status.value in {"ok", "needs_confirmation"}
