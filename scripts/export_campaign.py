#!/usr/bin/env python3
"""Export the repository campaign as a portable bundle. Does not import Hermes."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from board_game_companion.campaign.migration import export_bundle
from board_game_companion.campaign.repository import CampaignRepository


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=None)
    args = parser.parse_args()
    bundle = export_bundle(CampaignRepository())
    text = json.dumps(bundle, indent=2)
    if args.out:
        args.out.write_text(text + "\n")
    else:
        print(text)


if __name__ == "__main__":
    main()
