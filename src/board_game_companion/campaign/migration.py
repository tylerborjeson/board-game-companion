from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from board_game_companion.campaign.event_log import JsonlEventLog
from board_game_companion.campaign.repository import CampaignRepository
from board_game_companion.campaign.snapshots import load_snapshot
from board_game_companion.domain.models import Campaign, GameState


BUNDLE_FORMAT = "board-game-companion.campaign-bundle/v1"


class MigrationConflict(RuntimeError):
    pass


def export_bundle(repository: CampaignRepository) -> dict[str, Any]:
    campaign = repository.load_campaign()
    scenarios: dict[str, Any] = {}
    for scenario_dir in (repository.campaign_dir / "scenarios").iterdir():
        if not scenario_dir.is_dir():
            continue
        snapshot_path = scenario_dir / "state.json"
        if not snapshot_path.exists():
            continue
        events_path = scenario_dir / "events.jsonl"
        notes_path = scenario_dir / "notes.md"
        scenarios[scenario_dir.name] = {
            "snapshot": json.loads(snapshot_path.read_text()),
            "events": [event.model_dump(mode="json") for event in JsonlEventLog(events_path).read()],
            "notes": notes_path.read_text() if notes_path.exists() else "",
        }
    return {
        "format": BUNDLE_FORMAT,
        "campaign": campaign.model_dump(mode="json"),
        "scenarios": scenarios,
    }


def preview_import(current: GameState, incoming: GameState) -> dict[str, Any]:
    current_dump = current.model_dump(mode="json")
    incoming_dump = incoming.model_dump(mode="json")
    changed = {
        key: {"current": current_dump.get(key), "incoming": incoming_dump.get(key)}
        for key in sorted(set(current_dump) | set(incoming_dump))
        if current_dump.get(key) != incoming_dump.get(key)
    }
    return {"conflicts": changed, "can_auto_merge": False}


def commit_import(
    repository: CampaignRepository,
    incoming_state: GameState,
    *,
    confirmed: bool,
) -> None:
    current = repository.load_active_state()
    diff = preview_import(current, incoming_state)
    if diff["conflicts"] and not confirmed:
        raise MigrationConflict("refusing to auto-merge conflicting campaign state")
    raise MigrationConflict("Hermes import is defined but not enabled until Tyler confirms a reviewed diff")


def load_bundle(path: Path) -> tuple[Campaign, dict[str, GameState]]:
    payload = json.loads(path.read_text())
    if payload.get("format") != BUNDLE_FORMAT:
        raise MigrationConflict("unknown campaign bundle format")
    campaign = Campaign.model_validate(payload["campaign"])
    scenarios = {
        slug: load_snapshot_from_dict(item["snapshot"])
        for slug, item in payload.get("scenarios", {}).items()
    }
    return campaign, scenarios


def load_snapshot_from_dict(payload: dict[str, Any]) -> GameState:
    return GameState.model_validate(payload)
