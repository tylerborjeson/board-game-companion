from __future__ import annotations

from pydantic import BaseModel, Field

from board_game_companion.domain.enums import EventType, Phase, ValidationStatus
from board_game_companion.domain.events import GameEvent
from board_game_companion.domain.models import GameState
from board_game_companion.domain.phases import (
    INVESTIGATION_ACTIONS_SOLO,
    PHASE_RESTRICTED_EVENTS,
    is_legal_transition,
)


class ValidationIssue(BaseModel):
    code: str
    message: str
    field: str | None = None


class ValidationResult(BaseModel):
    status: ValidationStatus
    issues: list[ValidationIssue] = Field(default_factory=list)

    @property
    def ok(self) -> bool:
        return self.status == ValidationStatus.OK


def _result(issues: list[ValidationIssue]) -> ValidationResult:
    if any(issue.code.startswith("invalid_") for issue in issues):
        return ValidationResult(status=ValidationStatus.INVALID, issues=issues)
    if issues:
        return ValidationResult(status=ValidationStatus.NEEDS_CONFIRMATION, issues=issues)
    return ValidationResult(status=ValidationStatus.OK)


def validate_state(state: GameState) -> ValidationResult:
    issues: list[ValidationIssue] = []
    if state.status.value != "in_progress":
        return ValidationResult(status=ValidationStatus.OK)

    if state.round is not None and state.round < 1:
        issues.append(ValidationIssue(code="invalid_round", message="round must be >= 1", field="round"))
    if state.actions_remaining is not None and state.actions_remaining < 0:
        issues.append(
            ValidationIssue(
                code="invalid_actions",
                message="actions_remaining cannot be negative",
                field="actions_remaining",
            )
        )
    if (
        state.phase == Phase.INVESTIGATION
        and state.actions_remaining is not None
        and state.actions_remaining > INVESTIGATION_ACTIONS_SOLO
    ):
        issues.append(
            ValidationIssue(
                code="invalid_actions",
                message=f"actions_remaining cannot exceed {INVESTIGATION_ACTIONS_SOLO}",
                field="actions_remaining",
            )
        )

    investigator = state.investigator
    if investigator:
        for field_name in ("clues", "resources", "damage", "horror"):
            value = getattr(investigator, field_name)
            if value < 0:
                issues.append(
                    ValidationIssue(
                        code=f"invalid_{field_name}",
                        message=f"{field_name} cannot be negative",
                        field=f"investigator.{field_name}",
                    )
                )
        for enemy in state.enemies:
            if enemy.defeated:
                continue
            if enemy.engaged_with and enemy.location != investigator.location:
                issues.append(
                    ValidationIssue(
                        code="invalid_engagement",
                        message=f"{enemy.name} is engaged but not at {investigator.location}",
                        field="enemies",
                    )
                )

    computed_doom = 0
    if state.agenda:
        computed_doom += state.agenda.doom
    computed_doom += sum(enemy.doom for enemy in state.enemies if not enemy.defeated)
    if state.doom_total_in_play is not None and state.doom_total_in_play != computed_doom:
        issues.append(
            ValidationIssue(
                code="doom_mismatch",
                message=(
                    f"doom_total_in_play is {state.doom_total_in_play} "
                    f"but computed doom is {computed_doom}"
                ),
                field="doom_total_in_play",
            )
        )

    return _result(issues)


def validate_event(state: GameState, event: GameEvent) -> ValidationResult:
    issues: list[ValidationIssue] = []
    if not event.confirmed:
        issues.append(
            ValidationIssue(
                code="needs_physical_confirmation",
                message="event is not confirmed against the physical table",
            )
        )
        return _result(issues)

    if state.phase and event.type in PHASE_RESTRICTED_EVENTS:
        allowed = PHASE_RESTRICTED_EVENTS[event.type]
        if state.phase not in allowed:
            issues.append(
                ValidationIssue(
                    code="invalid_phase_action",
                    message=f"{event.type.value} is not legal during {state.phase.value}",
                    field="phase",
                )
            )

    if event.type == EventType.PHASE_ADVANCED:
        target = event.payload.get("to_phase")
        try:
            target_phase = Phase(target)
        except ValueError:
            issues.append(
                ValidationIssue(code="invalid_phase", message=f"unknown phase {target!r}", field="payload.to_phase")
            )
        else:
            if state.phase and not is_legal_transition(state.phase, target_phase):
                issues.append(
                    ValidationIssue(
                        code="invalid_phase_transition",
                        message=f"cannot advance from {state.phase.value} to {target_phase.value}",
                        field="phase",
                    )
                )

    if event.type == EventType.ENEMY_DEFEATED:
        name = event.payload.get("enemy") or event.payload.get("name")
        match = next((enemy for enemy in state.enemies if enemy.name == name and not enemy.defeated), None)
        if name and match is None:
            issues.append(
                ValidationIssue(
                    code="invalid_enemy",
                    message=f"no undefeated enemy named {name}",
                    field="payload.enemy",
                )
            )

    if event.type == EventType.ENEMY_ATTACK_RESOLVED:
        name = event.payload.get("enemy") or event.payload.get("name")
        match = next((enemy for enemy in state.enemies if enemy.name == name), None)
        if match and match.defeated:
            issues.append(
                ValidationIssue(
                    code="invalid_enemy",
                    message=f"{name} is defeated and cannot attack",
                    field="payload.enemy",
                )
            )

    if event.type == EventType.ENEMY_MOVED:
        name = event.payload.get("enemy") or event.payload.get("name")
        match = next((enemy for enemy in state.enemies if enemy.name == name), None)
        if match and match.defeated:
            issues.append(
                ValidationIssue(
                    code="invalid_enemy",
                    message=f"{name} is defeated and cannot move",
                    field="payload.enemy",
                )
            )

    if event.type == EventType.CLUE_DISCOVERED:
        amount = int(event.payload.get("amount", 1))
        location_name = event.payload.get("location")
        if amount < 1:
            issues.append(ValidationIssue(code="invalid_clues", message="clue amount must be >= 1"))
        if location_name and location_name in state.locations:
            if state.locations[location_name].clues < amount:
                issues.append(
                    ValidationIssue(
                        code="invalid_clues",
                        message=f"{location_name} does not have {amount} clue(s)",
                        field="payload.location",
                    )
                )

    if event.type == EventType.CLUE_SPENT:
        amount = int(event.payload.get("amount", 1))
        if state.investigator and state.investigator.clues < amount:
            issues.append(
                ValidationIssue(
                    code="invalid_clues",
                    message="investigator does not have enough clues",
                    field="investigator.clues",
                )
            )

    return _result(issues)


def validate_events(state: GameState, events: list[GameEvent]) -> ValidationResult:
    issues: list[ValidationIssue] = []
    last_occurred = None
    for event in events:
        result = validate_event(state, event)
        issues.extend(result.issues)
        if last_occurred and event.occurred_at < last_occurred:
            issues.append(
                ValidationIssue(
                    code="invalid_event_order",
                    message="event occurred_at is not monotonic",
                    field="occurred_at",
                )
            )
        last_occurred = event.occurred_at
    return _result(issues)
