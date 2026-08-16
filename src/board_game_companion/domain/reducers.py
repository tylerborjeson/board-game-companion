from __future__ import annotations

from typing import Any, Callable

from board_game_companion.domain.enums import EventType, Phase
from board_game_companion.domain.events import GameEvent
from board_game_companion.domain.models import GameState
from board_game_companion.domain.phases import INVESTIGATION_ACTIONS_SOLO, increments_round, is_legal_transition
from board_game_companion.domain.validation import validate_event


class ReductionError(ValueError):
    pass


def _deep_update(base: dict[str, Any], patch: dict[str, Any]) -> dict[str, Any]:
    for key, value in patch.items():
        if isinstance(value, dict) and isinstance(base.get(key), dict):
            base[key] = _deep_update(dict(base[key]), value)
        else:
            base[key] = value
    return base


def _require_investigator(state: GameState) -> None:
    if state.investigator is None:
        raise ReductionError("investigator is required")


def _enemy_defeated(state: GameState, event: GameEvent) -> GameState:
    name = event.payload.get("enemy") or event.payload.get("name")
    if not name:
        raise ReductionError("enemy_defeated requires payload.enemy")
    remaining = []
    found = False
    for enemy in state.enemies:
        if enemy.name == name and not enemy.defeated and not found:
            found = True
            continue
        remaining.append(enemy)
    if not found:
        raise ReductionError(f"no undefeated enemy named {name}")
    victory = list(state.victory_display)
    if name not in victory:
        victory.append(name)
    return state.model_copy(update={"enemies": remaining, "victory_display": victory})


def _clue_discovered(state: GameState, event: GameEvent) -> GameState:
    _require_investigator(state)
    amount = int(event.payload.get("amount", 1))
    location_name = event.payload.get("location")
    investigator = state.investigator.model_copy(update={"clues": state.investigator.clues + amount})
    locations = dict(state.locations)
    if location_name and location_name in locations:
        current = locations[location_name]
        if current.clues < amount:
            raise ReductionError(f"{location_name} does not have {amount} clue(s)")
        locations[location_name] = current.model_copy(update={"clues": current.clues - amount})
    return state.model_copy(update={"investigator": investigator, "locations": locations})


def _clue_spent(state: GameState, event: GameEvent) -> GameState:
    _require_investigator(state)
    amount = int(event.payload.get("amount", 1))
    if state.investigator.clues < amount:
        raise ReductionError("not enough clues")
    investigator = state.investigator.model_copy(update={"clues": state.investigator.clues - amount})
    return state.model_copy(update={"investigator": investigator})


def _phase_advanced(state: GameState, event: GameEvent) -> GameState:
    target = Phase(event.payload["to_phase"])
    if state.phase and not is_legal_transition(state.phase, target):
        raise ReductionError(f"illegal phase transition {state.phase.value} -> {target.value}")
    updates: dict[str, Any] = {"phase": target}
    if increments_round(state.phase, target) and state.round is not None:
        updates["round"] = state.round + 1
    if target == Phase.INVESTIGATION:
        updates["actions_remaining"] = INVESTIGATION_ACTIONS_SOLO
    else:
        updates["actions_remaining"] = 0
    return state.model_copy(update=updates)


def _resource_gained(state: GameState, event: GameEvent) -> GameState:
    _require_investigator(state)
    amount = int(event.payload.get("amount", 1))
    investigator = state.investigator.model_copy(update={"resources": state.investigator.resources + amount})
    return state.model_copy(update={"investigator": investigator})


def _damage_assigned(state: GameState, event: GameEvent) -> GameState:
    _require_investigator(state)
    amount = int(event.payload.get("amount", 1))
    investigator = state.investigator.model_copy(update={"damage": state.investigator.damage + amount})
    return state.model_copy(update={"investigator": investigator})


def _horror_assigned(state: GameState, event: GameEvent) -> GameState:
    _require_investigator(state)
    amount = int(event.payload.get("amount", 1))
    investigator = state.investigator.model_copy(update={"horror": state.investigator.horror + amount})
    return state.model_copy(update={"investigator": investigator})


def _enemy_moved(state: GameState, event: GameEvent) -> GameState:
    name = event.payload.get("enemy") or event.payload.get("name")
    destination = event.payload.get("to_location") or event.payload.get("location")
    if not name or not destination:
        raise ReductionError("enemy_moved requires enemy and to_location")
    enemies = []
    found = False
    for enemy in state.enemies:
        if enemy.name == name and not found:
            if enemy.defeated:
                raise ReductionError(f"{name} is defeated and cannot move")
            enemies.append(enemy.model_copy(update={"location": destination}))
            found = True
        else:
            enemies.append(enemy)
    if not found:
        raise ReductionError(f"no enemy named {name}")
    return state.model_copy(update={"enemies": enemies})


def _cultist_revealed(state: GameState, event: GameEvent) -> GameState:
    name = event.payload.get("cultist") or event.payload.get("name")
    location = event.payload.get("location")
    if not name or not location:
        raise ReductionError("cultist_revealed requires name and location")
    extra = {
        "name": name,
        "location": location,
        "engaged_with": None,
        "ready": True,
    }
    for key in ("card", "code", "health", "fight", "evade", "damage", "horror", "victory"):
        if key in event.payload:
            extra[key] = event.payload[key]
    from board_game_companion.domain.models import EnemyState

    enemies = [*state.enemies, EnemyState.model_validate(extra)]
    return state.model_copy(update={"enemies": enemies})


def _action_started(state: GameState, event: GameEvent) -> GameState:
    remaining = 0 if state.actions_remaining is None else state.actions_remaining - 1
    if remaining < 0:
        raise ReductionError("no actions remaining")
    return state.model_copy(update={"actions_remaining": remaining})


def _physical_correction(state: GameState, event: GameEvent) -> GameState:
    patch = event.payload.get("patch") or {}
    if not isinstance(patch, dict):
        raise ReductionError("physical_correction_recorded requires payload.patch")
    data = _deep_update(state.model_dump(), patch)
    return GameState.model_validate(data)


def _passthrough(state: GameState, event: GameEvent) -> GameState:
    return state


REDUCERS: dict[EventType, Callable[[GameState, GameEvent], GameState]] = {
    EventType.ENEMY_DEFEATED: _enemy_defeated,
    EventType.CLUE_DISCOVERED: _clue_discovered,
    EventType.CLUE_SPENT: _clue_spent,
    EventType.PHASE_ADVANCED: _phase_advanced,
    EventType.RESOURCE_GAINED: _resource_gained,
    EventType.DAMAGE_ASSIGNED: _damage_assigned,
    EventType.HORROR_ASSIGNED: _horror_assigned,
    EventType.ENEMY_MOVED: _enemy_moved,
    EventType.CULTIST_REVEALED: _cultist_revealed,
    EventType.ACTION_STARTED: _action_started,
    EventType.PHYSICAL_CORRECTION_RECORDED: _physical_correction,
    EventType.ENEMY_ATTACK_RESOLVED: _passthrough,
    EventType.SKILL_TEST_DECLARED: _passthrough,
    EventType.SKILL_TEST_RESOLVED: _passthrough,
    EventType.CARD_PLAYED: _passthrough,
    EventType.SESSION_PAUSED: _passthrough,
}


def apply_event(state: GameState, event: GameEvent) -> GameState:
    if not event.confirmed:
        raise ReductionError("unconfirmed events cannot be applied")
    result = validate_event(state, event)
    if not result.ok:
        raise ReductionError("; ".join(issue.message for issue in result.issues))
    reducer = REDUCERS.get(event.type)
    if reducer is None:
        raise ReductionError(f"no reducer for {event.type.value}")
    return reducer(state.model_copy(deep=True), event)


def apply_events(state: GameState, events: list[GameEvent]) -> GameState:
    current = state
    last_occurred = None
    for event in events:
        if last_occurred and event.occurred_at < last_occurred:
            raise ReductionError("event ordering is not monotonic")
        current = apply_event(current, event)
        last_occurred = event.occurred_at
    return current
