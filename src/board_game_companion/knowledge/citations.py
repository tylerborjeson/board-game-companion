from __future__ import annotations

from board_game_companion.knowledge.source_models import Citation, SearchHit


class UncitedResultError(ValueError):
    pass


def require_citations(hits: list[SearchHit]) -> list[Citation]:
    citations = [hit.citation for hit in hits if hit.citation.source_id and hit.citation.title]
    if not citations:
        raise UncitedResultError("rules results must include a citation")
    return citations
