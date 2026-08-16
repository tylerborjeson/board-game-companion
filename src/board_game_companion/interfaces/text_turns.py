from __future__ import annotations

from datetime import datetime, timezone

from board_game_companion.domain.models import TurnInput


def submit_text(text: str, *, confirmed_physical: bool = False) -> TurnInput:
    """Boundary for Wispr Flow / typed text. Audio never enters here."""
    return TurnInput(
        text=text.strip(),
        submitted_at=datetime.now(timezone.utc),
        confirmed_physical=confirmed_physical,
    )
