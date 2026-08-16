from __future__ import annotations

from pathlib import Path

import yaml

from board_game_companion.config import ARKHAM_GAME_DIR, SOURCE_MANIFEST_PATH
from board_game_companion.knowledge.source_models import SourceRecord


class CorpusUnavailableError(RuntimeError):
    pass


def load_manifest(path: Path | None = None) -> list[SourceRecord]:
    manifest_path = path or SOURCE_MANIFEST_PATH
    payload = yaml.safe_load(manifest_path.read_text())
    return [SourceRecord.model_validate(item) for item in payload.get("sources", [])]


def corpus_status(sources_root: Path | None = None) -> dict[str, bool]:
    root = sources_root or (ARKHAM_GAME_DIR / "sources")
    status: dict[str, bool] = {}
    for source in load_manifest():
        available = False
        if source.normalized_dir:
            chunk_dir = root / source.normalized_dir
            available = chunk_dir.is_dir() and any(chunk_dir.glob("*.json"))
        if not available and source.local_pdf:
            available = (root / source.local_pdf).is_file()
        if source.kind == "card_lookup":
            available = True
        status[source.id] = available
    return status


def require_rules_corpus() -> None:
    status = corpus_status()
    missing = [source_id for source_id, available in status.items() if source_id != "arkhamdb-api" and not available]
    if missing:
        raise CorpusUnavailableError(
            "authorized rules corpus is not loaded: " + ", ".join(missing)
        )
