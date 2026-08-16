from __future__ import annotations

from board_game_companion.domain.enums import TurnKind
from board_game_companion.domain.models import TurnInput, TurnInterpretation
from board_game_companion.model.provider import ModelProvider, ProviderRequest
from board_game_companion.model.prompts import load_persona, state_summary
from board_game_companion.domain.models import GameState

ACTION_MARKERS = (
    "defeated",
    "spent",
    "moved",
    "attack",
    "investigat",
    "played",
    "drew",
    "revealed",
    "advanced",
    "took a clue",
    "took the clue",
)
CORRECTION_MARKERS = ("actually", "correction", "on the table", "physical")


def classify_text(text: str) -> TurnKind:
    lowered = text.lower()
    correction = any(marker in lowered for marker in CORRECTION_MARKERS)
    action = any(marker in lowered for marker in ACTION_MARKERS)
    question = "?" in text
    if correction:
        return TurnKind.PHYSICAL_CORRECTION
    if action and question:
        return TurnKind.MIXED
    if action and lowered.count(" then ") + lowered.count(" and ") >= 1 and action:
        # long dictated turns with multiple observations
        if sum(marker in lowered for marker in ACTION_MARKERS) > 1:
            return TurnKind.MIXED
        return TurnKind.ACTION_REPORT
    if action:
        return TurnKind.ACTION_REPORT
    if question:
        return TurnKind.RULES_QUESTION
    return TurnKind.STORY_REFLECTION


def interpret(
    turn: TurnInput,
    state: GameState,
    provider: ModelProvider | None = None,
) -> TurnInterpretation:
    if provider is not None:
        response = provider.complete(
            ProviderRequest(
                persona=load_persona(),
                turn_text=turn.text,
                state_summary=state_summary(state),
            )
        )
        return TurnInterpretation(
            kind=response.kind,
            raw_text=turn.text,
            summary=response.summary,
            needs_confirmation=response.needs_confirmation,
            uncertainty=response.uncertainty,
        )
    kind = classify_text(turn.text)
    needs_confirmation = kind in {TurnKind.ACTION_REPORT, TurnKind.MIXED, TurnKind.PHYSICAL_CORRECTION}
    if "think" in turn.text.lower() or "maybe" in turn.text.lower() or "not sure" in turn.text.lower():
        needs_confirmation = True
    return TurnInterpretation(
        kind=kind,
        raw_text=turn.text,
        summary=turn.text.strip(),
        needs_confirmation=needs_confirmation and not turn.confirmed_physical,
        uncertainty="physical result is not confirmed" if needs_confirmation and not turn.confirmed_physical else None,
    )
