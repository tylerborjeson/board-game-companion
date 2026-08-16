from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, Field

from board_game_companion.domain.enums import EventSource, EventType, Phase


class GameEvent(BaseModel):
    event_id: str = Field(default_factory=lambda: str(uuid4()))
    type: EventType
    occurred_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    round: int
    phase: Phase
    source: EventSource = EventSource.TYLER_REPORTED
    confirmed: bool = False
    payload: dict[str, Any] = Field(default_factory=dict)
