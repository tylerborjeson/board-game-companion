from __future__ import annotations

from pathlib import Path

from board_game_companion.config import PERSONA_PATH
from board_game_companion.domain.models import GameState


def load_persona(path: Path | None = None) -> str:
    return (path or PERSONA_PATH).read_text()


def state_summary(state: GameState) -> str:
    investigator = state.investigator
    location = investigator.location if investigator else "unknown"
    return (
        f"{state.scenario}; round {state.round}; phase {state.phase}; "
        f"location {location}; actions {state.actions_remaining}"
    )
