from __future__ import annotations

from typing import Protocol

from board_game_companion.knowledge.ingestion import CorpusUnavailableError, require_rules_corpus
from board_game_companion.knowledge.source_models import Citation, SearchHit, SourceChunk


class RulesSearch(Protocol):
    def search(self, query: str, *, limit: int = 5) -> list[SearchHit]:
        ...


class InMemoryRulesSearch:
    def __init__(self, chunks: list[SourceChunk] | None = None, *, require_disk_corpus: bool = False) -> None:
        self.chunks = chunks or []
        self.require_disk_corpus = require_disk_corpus

    def search(self, query: str, *, limit: int = 5) -> list[SearchHit]:
        if self.require_disk_corpus:
            require_rules_corpus()
        if not self.chunks:
            raise CorpusUnavailableError("no searchable rules chunks are loaded")
        needle = query.lower()
        hits: list[SearchHit] = []
        for chunk in self.chunks:
            haystack = " ".join([chunk.text, chunk.title, *chunk.topics]).lower()
            if needle in haystack or any(token in haystack for token in needle.split() if len(token) > 3):
                hits.append(
                    SearchHit(
                        chunk=chunk,
                        citation=Citation(
                            source_id=chunk.source_id,
                            title=chunk.title,
                            edition=chunk.edition,
                            page_or_section=chunk.page_or_section,
                        ),
                    )
                )
        if not hits:
            raise CorpusUnavailableError(f"no cited passage for {query!r}")
        return hits[:limit]
