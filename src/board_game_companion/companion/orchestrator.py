from __future__ import annotations

from dataclasses import dataclass

from board_game_companion.campaign.repository import CampaignRepository
from board_game_companion.companion.clerk import commit_confirmed, review_proposals
from board_game_companion.companion.interpreter import interpret
from board_game_companion.companion.narrator import narrate
from board_game_companion.companion.referee import answer_rules
from board_game_companion.domain.enums import TurnKind, ValidationStatus
from board_game_companion.domain.models import TurnInput, TurnOutput
from board_game_companion.knowledge.card_lookup import CardLookup, MemoryCardLookup
from board_game_companion.knowledge.rules_search import InMemoryRulesSearch, RulesSearch
from board_game_companion.model.provider import ModelProvider, ProviderError, ProviderRequest
from board_game_companion.model.prompts import load_persona, state_summary
from board_game_companion.model.response_models import ModelTurnResponse


@dataclass
class CompanionDeps:
    repository: CampaignRepository
    provider: ModelProvider
    rules_search: RulesSearch
    card_lookup: CardLookup


def default_deps(repository: CampaignRepository | None = None) -> CompanionDeps:
    return CompanionDeps(
        repository=repository or CampaignRepository(),
        provider=None,  # type: ignore[arg-type]
        rules_search=InMemoryRulesSearch(),
        card_lookup=MemoryCardLookup(),
    )


def handle_turn(turn: TurnInput, deps: CompanionDeps) -> TurnOutput:
    state = deps.repository.load_active_state()
    try:
        model = deps.provider.complete(
            ProviderRequest(
                persona=load_persona(),
                turn_text=turn.text,
                state_summary=state_summary(state),
            )
        )
    except ProviderError as exc:
        interpretation = interpret(turn, state, provider=None)
        return narrate(
            state,
            interpretation,
            error=str(exc),
            clarification_needed=True,
            state_mutated=False,
        )

    if not isinstance(model, ModelTurnResponse):
        interpretation = interpret(turn, state, provider=None)
        return narrate(
            state,
            interpretation,
            error="malformed provider output",
            clarification_needed=True,
            state_mutated=False,
        )

    interpretation = interpret(turn, state, provider=deps.provider)
    if interpretation.kind == TurnKind.RULES_QUESTION:
        rule, citations = answer_rules(turn.text, deps.rules_search)
        output = narrate(
            state,
            interpretation,
            model=model,
            rule=rule,
            citations=citations or model.citations,
            state_mutated=False,
        )
        return output

    if interpretation.needs_confirmation and not turn.confirmed_physical:
        return narrate(
            state,
            interpretation,
            model=model,
            clarification_needed=True,
            state_mutated=False,
        )

    validation, events = review_proposals(state, model.proposals)
    if validation.status != ValidationStatus.OK or not events:
        output = narrate(
            state,
            interpretation,
            model=model,
            clarification_needed=True,
            state_mutated=False,
        )
        output.validation_status = validation.status
        return output

    committed = commit_confirmed(deps.repository, events)
    output = narrate(
        committed,
        interpretation,
        model=model,
        state_mutated=True,
        committed_event_ids=[event.event_id for event in events],
    )
    output.validation_status = ValidationStatus.OK
    return output
