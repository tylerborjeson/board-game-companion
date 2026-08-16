from __future__ import annotations

from board_game_companion.knowledge.citations import require_citations
from board_game_companion.knowledge.ingestion import CorpusUnavailableError
from board_game_companion.knowledge.rules_search import RulesSearch
from board_game_companion.knowledge.source_models import Citation, SearchHit


def answer_rules(query: str, search: RulesSearch) -> tuple[str, list[Citation]]:
    try:
        hits: list[SearchHit] = search.search(query)
        citations = require_citations(hits)
    except (CorpusUnavailableError, ValueError) as exc:
        return (
            f"I cannot treat that as an authoritative ruling. {exc}",
            [],
        )
    passage = hits[0].chunk.text
    return passage, citations
