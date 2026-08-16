from __future__ import annotations

from enum import Enum


class Phase(str, Enum):
    MYTHOS = "mythos"
    INVESTIGATION = "investigation"
    ENEMY = "enemy"
    UPKEEP = "upkeep"


class ScenarioStatus(str, Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETE = "complete"


class EventType(str, Enum):
    ACTION_STARTED = "action_started"
    SKILL_TEST_DECLARED = "skill_test_declared"
    SKILL_TEST_RESOLVED = "skill_test_resolved"
    CARD_PLAYED = "card_played"
    ENEMY_DEFEATED = "enemy_defeated"
    CLUE_DISCOVERED = "clue_discovered"
    CLUE_SPENT = "clue_spent"
    CULTIST_REVEALED = "cultist_revealed"
    ENEMY_MOVED = "enemy_moved"
    ENEMY_ATTACK_RESOLVED = "enemy_attack_resolved"
    PHASE_ADVANCED = "phase_advanced"
    RESOURCE_GAINED = "resource_gained"
    DAMAGE_ASSIGNED = "damage_assigned"
    HORROR_ASSIGNED = "horror_assigned"
    PHYSICAL_CORRECTION_RECORDED = "physical_correction_recorded"
    SESSION_PAUSED = "session_paused"


class EventSource(str, Enum):
    TYLER_REPORTED = "tyler_reported"
    PHYSICAL_CORRECTION = "physical_correction"
    SYSTEM = "system"


class TurnKind(str, Enum):
    RULES_QUESTION = "rules_question"
    ACTION_REPORT = "action_report"
    PHYSICAL_CORRECTION = "physical_correction"
    STORY_REFLECTION = "story_reflection"
    MIXED = "mixed"


class ValidationStatus(str, Enum):
    OK = "ok"
    INVALID = "invalid"
    NEEDS_CONFIRMATION = "needs_confirmation"
