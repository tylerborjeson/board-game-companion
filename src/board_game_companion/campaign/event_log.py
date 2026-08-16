from __future__ import annotations

from pathlib import Path
from typing import Protocol

from board_game_companion.domain.events import GameEvent


class EventLog(Protocol):
    def read(self) -> list[GameEvent]:
        ...

    def append(self, events: list[GameEvent]) -> None:
        ...


class JsonlEventLog:
    def __init__(self, path: Path) -> None:
        self.path = path

    def read(self) -> list[GameEvent]:
        if not self.path.exists() or self.path.stat().st_size == 0:
            return []
        events: list[GameEvent] = []
        for line in self.path.read_text().splitlines():
            if line.strip():
                events.append(GameEvent.model_validate_json(line))
        return events

    def append(self, events: list[GameEvent]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8") as handle:
            for event in events:
                handle.write(event.model_dump_json() + "\n")
