from __future__ import annotations

import os
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = REPO_ROOT / "data"
SCHEMAS_DIR = REPO_ROOT / "schemas"
ARKHAM_GAME_DIR = DATA_DIR / "games" / "arkham-horror"
CAMPAIGN_DIR = DATA_DIR / "campaigns" / "night-of-the-zealot"
PERSONA_PATH = ARKHAM_GAME_DIR / "persona.md"
SOURCE_MANIFEST_PATH = ARKHAM_GAME_DIR / "sources" / "manifest.yaml"


def provider_name() -> str:
    return os.environ.get("BOARD_GAME_COMPANION_PROVIDER", "fake")
