from __future__ import annotations

from pathlib import Path

from board_game_companion.campaign.event_log import JsonlEventLog
from board_game_companion.campaign.snapshots import load_snapshot, rebuild_snapshot, save_snapshot
from board_game_companion.config import CAMPAIGN_DIR, REPO_ROOT
from board_game_companion.domain.events import GameEvent
from board_game_companion.domain.models import Campaign, GameState
from board_game_companion.domain.reducers import ReductionError
from board_game_companion.domain.validation import validate_events, validate_state


class CampaignRepository:
    def __init__(self, campaign_dir: Path | None = None) -> None:
        self.campaign_dir = campaign_dir or CAMPAIGN_DIR
        self.campaign_path = self.campaign_dir / "campaign.json"

    def load_campaign(self) -> Campaign:
        return Campaign.model_validate_json(self.campaign_path.read_text())

    def active_state_path(self) -> Path:
        campaign = self.load_campaign()
        path = Path(campaign.active_scenario.path)
        if not path.is_absolute():
            path = REPO_ROOT / path
        return path

    def active_events_path(self) -> Path:
        return self.active_state_path().with_name("events.jsonl")

    def load_active_state(self) -> GameState:
        return load_snapshot(self.active_state_path())

    def load_events(self) -> list[GameEvent]:
        return JsonlEventLog(self.active_events_path()).read()

    def commit(self, events: list[GameEvent]) -> GameState:
        if not events:
            raise ReductionError("commit requires at least one event")
        if any(not event.confirmed for event in events):
            raise ReductionError("unconfirmed events cannot be committed")
        state = self.load_active_state()
        state_check = validate_state(state)
        if state_check.status.value == "invalid":
            raise ReductionError("; ".join(issue.message for issue in state_check.issues))
        event_check = validate_events(state, events)
        if not event_check.ok:
            raise ReductionError("; ".join(issue.message for issue in event_check.issues))
        new_state = rebuild_snapshot(state, events)
        JsonlEventLog(self.active_events_path()).append(events)
        save_snapshot(self.active_state_path(), new_state)
        return new_state
