from __future__ import annotations

from board_game_companion.campaign.event_log import JsonlEventLog
from board_game_companion.campaign.snapshots import rebuild_snapshot
from board_game_companion.domain.enums import EventSource, EventType, Phase
from board_game_companion.domain.events import GameEvent
from board_game_companion.domain.models import GameState
from tests.conftest import make_event


def test_event_log_is_append_only(tmp_path, peter_fixture: dict) -> None:
    path = tmp_path / "events.jsonl"
    log = JsonlEventLog(path)
    first = make_event(EventType.ENEMY_DEFEATED, {"enemy": "Peter Warren"})
    log.append([first])
    second = make_event(EventType.CLUE_DISCOVERED, {"location": "Miskatonic University", "amount": 1})
    log.append([second])
    events = log.read()
    assert [event.event_id for event in events] == [first.event_id, second.event_id]
    assert not hasattr(log, "rewrite")
    assert not hasattr(log, "delete")


def test_physical_correction_does_not_rewrite_history(temp_campaign, peter_fixture: dict) -> None:
    state_path = temp_campaign.active_state_path()
    GameState.model_validate(peter_fixture["before"])
    state_path.write_text(
        GameState.model_validate(peter_fixture["before"]).model_dump_json(indent=2) + "\n"
    )
    defeat = make_event(EventType.ENEMY_DEFEATED, {"enemy": "Peter Warren"})
    temp_campaign.commit([defeat])
    correction = GameEvent(
        type=EventType.PHYSICAL_CORRECTION_RECORDED,
        round=6,
        phase=Phase.INVESTIGATION,
        source=EventSource.PHYSICAL_CORRECTION,
        confirmed=True,
        payload={"patch": {"investigator": {"clues": 2}}},
    )
    temp_campaign.commit([correction])
    events = temp_campaign.load_events()
    assert events[0].event_id == defeat.event_id
    assert events[1].type == EventType.PHYSICAL_CORRECTION_RECORDED
    assert temp_campaign.load_active_state().investigator.clues == 2


def test_replay_rebuilds_snapshot(peter_fixture: dict) -> None:
    base = GameState.model_validate(peter_fixture["before"])
    events = [
        make_event(EventType(item["type"]), item["payload"])
        for item in peter_fixture["events"]
    ]
    rebuilt = rebuild_snapshot(base, events)
    assert "Peter Warren" in rebuilt.victory_display
    assert rebuilt.investigator and rebuilt.investigator.clues == 1
