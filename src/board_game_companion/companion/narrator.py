from __future__ import annotations

from board_game_companion.domain.enums import TurnKind
from board_game_companion.domain.models import GameState, TurnInterpretation, TurnOutput
from board_game_companion.knowledge.source_models import Citation
from board_game_companion.model.response_models import ModelTurnResponse


def default_fiction(state: GameState) -> str:
    location = state.investigator.location if state.investigator else "the dark"
    return (
        f"Noko stays at Roland's shoulder in {location}. "
        "The air is wet stone and old paper. Something in the quiet is still watching."
    )


def narrate(
    state: GameState,
    interpretation: TurnInterpretation,
    *,
    model: ModelTurnResponse | None = None,
    rule: str = "",
    citations: list[Citation] | None = None,
    clarification_needed: bool = False,
    state_mutated: bool = False,
    error: str | None = None,
    committed_event_ids: list[str] | None = None,
) -> TurnOutput:
    citations = citations or (model.citations if model else [])
    table = (
        model.table_summary
        if model and model.table_summary
        else f"Round {state.round}. {state.phase.value if state.phase else 'unknown'} phase."
    )
    fiction = model.fiction if model and model.fiction else default_fiction(state)
    rule_text = model.rule if model and model.rule else rule
    application = model.application if model and model.application else interpretation.summary
    advice = (
        model.mentor_advice
        if model and model.mentor_advice
        else "Confirm the physical table before we write anything down."
    )
    question = (
        model.next_question
        if model and model.next_question
        else "What do you want to do, and what does the table show?"
    )
    if interpretation.kind == TurnKind.RULES_QUESTION and not question:
        question = "Does that match the card in front of you?"
    if clarification_needed:
        question = interpretation.uncertainty or "What does the physical table show?"
        advice = "I will not guess a disputed fact."
    return TurnOutput(
        table_summary=table,
        fiction=fiction,
        rule=rule_text,
        application=application,
        mentor_advice=advice,
        next_question=question,
        citations=citations,
        interpretation=interpretation,
        proposals=model.proposals if model else [],
        validation_status=None,
        committed_event_ids=committed_event_ids or [],
        clarification_needed=clarification_needed,
        state_mutated=state_mutated,
        error=error,
    )
