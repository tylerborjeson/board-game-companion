from __future__ import annotations

from board_game_companion.campaign.repository import CampaignRepository
from board_game_companion.domain.commands import CommandProposal
from board_game_companion.domain.enums import EventSource, ValidationStatus
from board_game_companion.domain.events import GameEvent
from board_game_companion.domain.models import GameState
from board_game_companion.domain.reducers import ReductionError
from board_game_companion.domain.validation import ValidationResult, validate_events


def proposals_to_events(state: GameState, proposals: list[CommandProposal]) -> list[GameEvent]:
    if state.round is None or state.phase is None:
        raise ReductionError("active state is missing round or phase")
    return [
        proposal.to_event(
            round=state.round,
            phase=state.phase,
            source=(
                EventSource.PHYSICAL_CORRECTION
                if proposal.type.value == "physical_correction_recorded"
                else EventSource.TYLER_REPORTED
            ),
        )
        for proposal in proposals
    ]


def review_proposals(state: GameState, proposals: list[CommandProposal]) -> tuple[ValidationResult, list[GameEvent]]:
    if any(proposal.needs_confirmation or not proposal.confirmed for proposal in proposals):
        return (
            ValidationResult(
                status=ValidationStatus.NEEDS_CONFIRMATION,
                issues=[],
            ),
            [],
        )
    events = proposals_to_events(state, proposals)
    return validate_events(state, events), events


def commit_confirmed(repository: CampaignRepository, events: list[GameEvent]) -> GameState:
    return repository.commit(events)
