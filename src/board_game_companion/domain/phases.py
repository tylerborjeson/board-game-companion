from __future__ import annotations

from board_game_companion.domain.enums import EventType, Phase

PHASE_ORDER = (Phase.MYTHOS, Phase.INVESTIGATION, Phase.ENEMY, Phase.UPKEEP)

LEGAL_TRANSITIONS: dict[Phase, Phase] = {
    Phase.MYTHOS: Phase.INVESTIGATION,
    Phase.INVESTIGATION: Phase.ENEMY,
    Phase.ENEMY: Phase.UPKEEP,
    Phase.UPKEEP: Phase.MYTHOS,
}

INVESTIGATION_ACTIONS_SOLO = 3

PHASE_RESTRICTED_EVENTS = {
    EventType.ACTION_STARTED: {Phase.INVESTIGATION},
    EventType.CARD_PLAYED: {Phase.INVESTIGATION},
    EventType.CLUE_DISCOVERED: {Phase.INVESTIGATION},
    EventType.CLUE_SPENT: {Phase.INVESTIGATION},
    EventType.CULTIST_REVEALED: {Phase.INVESTIGATION},
    EventType.ENEMY_MOVED: {Phase.ENEMY},
    EventType.ENEMY_ATTACK_RESOLVED: {Phase.ENEMY},
}


def next_phase(current: Phase) -> Phase:
    return LEGAL_TRANSITIONS[current]


def is_legal_transition(current: Phase, target: Phase) -> bool:
    return LEGAL_TRANSITIONS.get(current) == target


def increments_round(current: Phase, target: Phase) -> bool:
    return current == Phase.UPKEEP and target == Phase.MYTHOS
