#!/usr/bin/env python3
"""Rebuild a materialized snapshot from a base state plus events.jsonl."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from board_game_companion.campaign.event_log import JsonlEventLog
from board_game_companion.campaign.snapshots import load_snapshot, rebuild_snapshot


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("base_state", type=Path)
    parser.add_argument("events", type=Path)
    parser.add_argument("--write", type=Path, help="optional output path; otherwise print JSON")
    args = parser.parse_args()
    state = rebuild_snapshot(load_snapshot(args.base_state), JsonlEventLog(args.events).read())
    text = json.dumps(state.model_dump(mode="json"), indent=2)
    if args.write:
        args.write.write_text(text + "\n")
    else:
        print(text)


if __name__ == "__main__":
    main()
