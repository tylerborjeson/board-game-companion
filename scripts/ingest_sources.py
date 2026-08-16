#!/usr/bin/env python3
"""Report whether the authorized Arkham corpus is actually available."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from board_game_companion.knowledge.ingestion import corpus_status, load_manifest


def main() -> None:
    print("source manifest:")
    for source in load_manifest():
        print(f"  - {source.id}: {source.title} ({source.kind})")
    print("availability:")
    status = corpus_status()
    for source_id, available in status.items():
        mark = "loaded" if available else "UNAVAILABLE"
        print(f"  - {source_id}: {mark}")
    missing = [key for key, available in status.items() if key != "arkhamdb-api" and not available]
    if missing:
        print("corpus is not ready; pointer files are not the rulebook")
        raise SystemExit(1)
    print("required corpus appears available")


if __name__ == "__main__":
    main()
