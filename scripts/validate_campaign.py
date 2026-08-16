#!/usr/bin/env python3
"""Validate the active campaign and scenario snapshot against JSON Schema."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from board_game_companion.app import main

if __name__ == "__main__":
    main()
