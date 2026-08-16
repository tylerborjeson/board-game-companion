from __future__ import annotations

from board_game_companion.companion.orchestrator import CompanionDeps, handle_turn
from board_game_companion.domain.commands import CommandProposal
from board_game_companion.domain.enums import EventType, TurnKind
from board_game_companion.interfaces.text_turns import submit_text
from board_game_companion.knowledge.card_lookup import MemoryCardLookup
from board_game_companion.knowledge.rules_search import InMemoryRulesSearch
from board_game_companion.model.adapters.fake import FakeProvider
from board_game_companion.model.response_models import ModelTurnResponse
from tests.conftest import rules_provider


def _deps(temp_campaign, provider, chunk) -> CompanionDeps:
    return CompanionDeps(
        repository=temp_campaign,
        provider=provider,
        rules_search=InMemoryRulesSearch([chunk]),
        card_lookup=MemoryCardLookup(),
    )


def test_rules_question_does_not_mutate_state(temp_campaign, enemy_phase_chunk, noko_citation) -> None:
    before = temp_campaign.load_active_state()
    output = handle_turn(
        submit_text("When do hunters move in the enemy phase?"),
        _deps(temp_campaign, rules_provider(noko_citation), enemy_phase_chunk),
    )
    after = temp_campaign.load_active_state()
    assert output.state_mutated is False
    assert output.interpretation and output.interpretation.kind == TurnKind.RULES_QUESTION
    assert output.citations
    assert output.citations[0].source_id == "learn-to-play"
    assert "Noko" in output.fiction or output.fiction
    assert output.next_question
    assert before.model_dump() == after.model_dump()
    assert temp_campaign.load_events() == []


def test_confirmed_action_commits_events(temp_campaign, enemy_phase_chunk, peter_fixture) -> None:
    from board_game_companion.domain.models import GameState

    temp_campaign.active_state_path().write_text(
        GameState.model_validate(peter_fixture["before"]).model_dump_json(indent=2) + "\n"
    )
    provider = FakeProvider(
        {
            "defeated peter": ModelTurnResponse(
                kind=TurnKind.ACTION_REPORT,
                summary="Peter Warren defeated",
                needs_confirmation=False,
                proposals=[
                    CommandProposal(
                        type=EventType.ENEMY_DEFEATED,
                        confirmed=True,
                        payload={"enemy": "Peter Warren"},
                    )
                ],
                table_summary="Peter is down.",
                fiction="Noko lets out a breath he had been holding.",
                rule="When an enemy is defeated, it leaves play.",
                application="Peter Warren goes to the victory display.",
                mentor_advice="Count the remaining hunters before you relax.",
                next_question="Investigation still has an action. What now?",
            )
        }
    )
    output = handle_turn(
        submit_text("I defeated Peter Warren.", confirmed_physical=True),
        _deps(temp_campaign, provider, enemy_phase_chunk),
    )
    assert output.state_mutated is True
    assert output.committed_event_ids
    assert "Peter Warren" in temp_campaign.load_active_state().victory_display


def test_ambiguous_result_clarifies_instead_of_commit(temp_campaign, enemy_phase_chunk) -> None:
    provider = FakeProvider(
        {
            "think i took": ModelTurnResponse(
                kind=TurnKind.ACTION_REPORT,
                summary="possible clue",
                needs_confirmation=True,
                uncertainty="clue count is not confirmed",
                proposals=[
                    CommandProposal(
                        type=EventType.CLUE_DISCOVERED,
                        confirmed=False,
                        needs_confirmation=True,
                        uncertainty="maybe one clue",
                        payload={"amount": 1},
                    )
                ],
                next_question="How many clues are on Roland right now?",
            )
        }
    )
    before = temp_campaign.load_active_state()
    output = handle_turn(
        submit_text("I think I took a clue"),
        _deps(temp_campaign, provider, enemy_phase_chunk),
    )
    assert output.clarification_needed is True
    assert output.state_mutated is False
    assert temp_campaign.load_active_state().model_dump() == before.model_dump()


def test_provider_failure_does_not_mutate(temp_campaign, enemy_phase_chunk) -> None:
    before = temp_campaign.load_active_state()
    output = handle_turn(
        submit_text("I defeated Peter Warren.", confirmed_physical=True),
        _deps(temp_campaign, FakeProvider(fail=True), enemy_phase_chunk),
    )
    assert output.state_mutated is False
    assert output.error
    assert temp_campaign.load_active_state().model_dump() == before.model_dump()


def test_malformed_provider_output_rejected(temp_campaign, enemy_phase_chunk) -> None:
    before = temp_campaign.load_active_state()
    output = handle_turn(
        submit_text("I defeated Peter Warren.", confirmed_physical=True),
        _deps(temp_campaign, FakeProvider(malformed=True), enemy_phase_chunk),
    )
    assert output.state_mutated is False
    assert output.error
    assert before.model_dump() == temp_campaign.load_active_state().model_dump()


def test_noko_shaped_response(temp_campaign, enemy_phase_chunk, noko_citation) -> None:
    output = handle_turn(
        submit_text("When do hunters move in the enemy phase?"),
        _deps(temp_campaign, rules_provider(noko_citation), enemy_phase_chunk),
    )
    for field in (
        "table_summary",
        "fiction",
        "rule",
        "application",
        "mentor_advice",
        "next_question",
    ):
        assert getattr(output, field)
    assert output.citations
