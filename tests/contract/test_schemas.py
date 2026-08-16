from __future__ import annotations

import json
from pathlib import Path

import jsonschema
import pytest

from board_game_companion.campaign.repository import CampaignRepository
from board_game_companion.config import CAMPAIGN_DIR
from board_game_companion.domain.models import GameState, TurnInput, TurnOutput
from board_game_companion.interfaces.schemas import validate_file, validate_payload

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures"


def test_load_valid_active_campaign() -> None:
    repo = CampaignRepository(CAMPAIGN_DIR)
    campaign = repo.load_campaign()
    state = repo.load_active_state()
    validate_file("campaign.schema.json", repo.campaign_path)
    validate_file("scenario-state.schema.json", repo.active_state_path())
    assert campaign.current_scenario == "The Midnight Masks"
    assert state.scenario == "The Midnight Masks"
    assert state.status.value == "in_progress"


def test_reject_invalid_state() -> None:
    payload = json.loads((FIXTURES / "invalid-state.json").read_text())
    with pytest.raises(jsonschema.ValidationError):
        validate_payload("scenario-state.schema.json", payload)


def test_checkpoint_fixture_validates() -> None:
    validate_file("scenario-state.schema.json", FIXTURES / "midnight-masks-start.json")
    validate_file("scenario-state.schema.json", FIXTURES / "ambiguous-doom-state.json")


def test_models_round_trip(checkpoint_state: GameState) -> None:
    dumped = checkpoint_state.model_dump(mode="json")
    again = GameState.model_validate(dumped)
    assert again.scenario == checkpoint_state.scenario
    assert again.investigator and again.investigator.location == "Miskatonic University"


def test_turn_contracts_serialize() -> None:
    turn = TurnInput(text="When do hunters move?")
    output = TurnOutput(
        table_summary="Round 6.",
        fiction="Noko waits.",
        rule="Enemy phase.",
        application="Hunters move first.",
        mentor_advice="Check connections.",
        next_question="What does the map show?",
    )
    validate_payload("turn-input.schema.json", json.loads(turn.model_dump_json()))
    validate_payload("turn-output.schema.json", json.loads(output.model_dump_json()))
