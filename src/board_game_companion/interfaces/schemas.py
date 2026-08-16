from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import jsonschema

from board_game_companion.config import SCHEMAS_DIR


def load_schema(name: str) -> dict[str, Any]:
    path = SCHEMAS_DIR / name
    return json.loads(path.read_text())


def validate_payload(name: str, payload: dict[str, Any]) -> None:
    jsonschema.validate(payload, load_schema(name))


def validate_file(name: str, path: Path) -> None:
    validate_payload(name, json.loads(path.read_text()))
