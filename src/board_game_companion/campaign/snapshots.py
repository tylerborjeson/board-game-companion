from __future__ import annotations

import json
from pathlib import Path

from board_game_companion.domain.events import GameEvent
from board_game_companion.domain.models import GameState
from board_game_companion.domain.reducers import apply_events


def load_snapshot(path: Path) -> GameState:
    return GameState.model_validate_json(path.read_text())


def save_snapshot(path: Path, state: GameState) -> None:
    path.write_text(json.dumps(state.model_dump(mode="json"), indent=2) + "\n")


def rebuild_snapshot(base: GameState, events: list[GameEvent]) -> GameState:
    return apply_events(base, events)
