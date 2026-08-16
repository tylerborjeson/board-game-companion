from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from pydantic import BaseModel, Field

from board_game_companion.domain.enums import EventSource, EventType, Phase
from board_game_companion.domain.events import GameEvent


class CommandProposal(BaseModel):
    type: EventType
    confirmed: bool = False
    needs_confirmation: bool = False
    uncertainty: str | None = None
    payload: dict[str, Any] = Field(default_factory=dict)

    def to_event(
        self,
        *,
        round: int,
        phase: Phase,
        source: EventSource = EventSource.TYLER_REPORTED,
        occurred_at: datetime | None = None,
    ) -> GameEvent:
        return GameEvent(
            type=self.type,
            occurred_at=occurred_at or datetime.now(timezone.utc),
            round=round,
            phase=phase,
            source=source,
            confirmed=self.confirmed,
            payload=self.payload,
        )
