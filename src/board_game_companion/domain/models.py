from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from board_game_companion.domain.enums import Phase, ScenarioStatus, TurnKind, ValidationStatus
from board_game_companion.knowledge.source_models import Citation


class CardRef(BaseModel):
    model_config = ConfigDict(extra="allow")

    name: str | None = None
    card: int | str | None = None


class InvestigatorState(BaseModel):
    model_config = ConfigDict(extra="allow")

    name: str
    location: str
    resources: int = 0
    clues: int = 0
    damage: int = 0
    horror: int = 0
    hand: list[Any] = Field(default_factory=list)
    in_play: list[Any] = Field(default_factory=list)
    discard: list[Any] = Field(default_factory=list)


class LocationState(BaseModel):
    model_config = ConfigDict(extra="allow")

    revealed: bool = False
    clues: int = 0
    shroud: int | None = None


class EnemyState(BaseModel):
    model_config = ConfigDict(extra="allow")

    name: str
    location: str | None = None
    engaged_with: str | None = None
    ready: bool = True
    health: int | None = None
    defeated: bool = False
    doom: int = 0


class ActState(BaseModel):
    model_config = ConfigDict(extra="allow")

    name: str | None = None
    card: int | str | None = None
    side: str | None = None


class AgendaState(BaseModel):
    model_config = ConfigDict(extra="allow")

    name: str | None = None
    card: int | str | None = None
    doom: int = 0
    threshold: int | None = None


class NextDecision(BaseModel):
    model_config = ConfigDict(extra="allow")

    type: str
    prompt: str


class ActiveScenario(BaseModel):
    model_config = ConfigDict(extra="allow")

    slug: str
    path: str
    status: ScenarioStatus


class Campaign(BaseModel):
    model_config = ConfigDict(extra="allow")

    campaign: str
    investigator: str
    companion: str | None = None
    player_count: int = 1
    scenario_order: list[str]
    current_scenario: str
    active_scenario: ActiveScenario
    rules_sources: dict[str, str] = Field(default_factory=dict)
    campaign_state: dict[str, Any] = Field(default_factory=dict)


class GameState(BaseModel):
    model_config = ConfigDict(extra="allow")

    scenario: str
    status: ScenarioStatus
    round: int | None = None
    phase: Phase | None = None
    actions_remaining: int | None = None
    investigator: InvestigatorState | None = None
    locations: dict[str, LocationState] = Field(default_factory=dict)
    enemies: list[EnemyState] = Field(default_factory=list)
    victory_display: list[str] = Field(default_factory=list)
    act: ActState | dict[str, Any] | None = None
    agenda: AgendaState | None = None
    decks: dict[str, Any] = Field(default_factory=dict)
    next_decision: NextDecision | None = None
    doom_total_in_play: int | None = None


class TurnInput(BaseModel):
    text: str
    submitted_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    confirmed_physical: bool = False
    campaign_id: str | None = None


class TurnInterpretation(BaseModel):
    kind: TurnKind
    raw_text: str
    summary: str
    needs_confirmation: bool = False
    uncertainty: str | None = None


class TurnOutput(BaseModel):
    table_summary: str
    fiction: str
    rule: str
    application: str
    mentor_advice: str
    next_question: str
    citations: list[Citation] = Field(default_factory=list)
    interpretation: TurnInterpretation | None = None
    proposals: list[Any] = Field(default_factory=list)
    validation_status: ValidationStatus | None = None
    committed_event_ids: list[str] = Field(default_factory=list)
    clarification_needed: bool = False
    state_mutated: bool = False
    error: str | None = None
