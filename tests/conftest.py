from __future__ import annotations

import json
import shutil
from pathlib import Path

import pytest

from board_game_companion.campaign.repository import CampaignRepository
from board_game_companion.config import CAMPAIGN_DIR
from board_game_companion.domain.enums import EventType, Phase, TurnKind
from board_game_companion.domain.events import GameEvent
from board_game_companion.domain.models import GameState
from board_game_companion.knowledge.source_models import Citation, SourceChunk
from board_game_companion.model.adapters.fake import FakeProvider
from board_game_companion.model.response_models import ModelTurnResponse

FIXTURES = Path(__file__).parent / "fixtures"


@pytest.fixture
def checkpoint_state() -> GameState:
    return GameState.model_validate_json((FIXTURES / "midnight-masks-start.json").read_text())


@pytest.fixture
def peter_fixture() -> dict:
    return json.loads((FIXTURES / "peter-warren-defeated.json").read_text())


@pytest.fixture
def temp_campaign(tmp_path: Path) -> CampaignRepository:
    dest = tmp_path / "night-of-the-zealot"
    shutil.copytree(CAMPAIGN_DIR, dest)
    campaign_path = dest / "campaign.json"
    payload = json.loads(campaign_path.read_text())
    payload["active_scenario"]["path"] = str(
        dest / "scenarios" / "the-midnight-masks" / "state.json"
    )
    campaign_path.write_text(json.dumps(payload, indent=2) + "\n")
    return CampaignRepository(dest)


@pytest.fixture
def enemy_phase_chunk() -> SourceChunk:
    return SourceChunk(
        source_id="learn-to-play",
        title="2021 Revised Core Set Learn to Play",
        edition="2021 Revised Core Set",
        page_or_section="p. 15; Enemy phase",
        text="Enemy phase: hunters move, then engaged enemies attack.",
        topics=["enemy phase", "hunter", "attack"],
    )


@pytest.fixture
def noko_citation() -> Citation:
    return Citation(
        source_id="learn-to-play",
        title="2021 Revised Core Set Learn to Play",
        edition="2021 Revised Core Set",
        page_or_section="p. 15; Enemy phase",
    )


def make_event(event_type: EventType, payload: dict, *, phase: Phase = Phase.INVESTIGATION) -> GameEvent:
    return GameEvent(
        type=event_type,
        round=6,
        phase=phase,
        confirmed=True,
        payload=payload,
    )


def rules_provider(citation: Citation) -> FakeProvider:
    return FakeProvider(
        {
            "enemy phase": ModelTurnResponse(
                kind=TurnKind.RULES_QUESTION,
                summary="When do hunters move?",
                table_summary="Round 6. Enemy phase.",
                fiction="Noko keeps to the wall. Rain ticks on the university stone.",
                rule="Enemy phase: hunters move, then engaged enemies attack.",
                application="Ready unengaged hunters move one connecting location toward Roland.",
                mentor_advice="Confirm connections on the physical map before the Nightgaunt walks.",
                next_question="Does Northside connect to Miskatonic on your map?",
                citations=[citation],
            )
        }
    )
