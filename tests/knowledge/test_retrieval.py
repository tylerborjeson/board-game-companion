from __future__ import annotations

import pytest

from board_game_companion.knowledge.card_lookup import CardNotFoundError, MemoryCardLookup
from board_game_companion.knowledge.citations import require_citations
from board_game_companion.knowledge.ingestion import CorpusUnavailableError
from board_game_companion.knowledge.rules_search import InMemoryRulesSearch
from board_game_companion.knowledge.source_models import SearchHit


def test_rules_search_returns_citation(enemy_phase_chunk) -> None:
    search = InMemoryRulesSearch([enemy_phase_chunk])
    hits = search.search("enemy phase hunters")
    assert hits
    assert hits[0].citation.source_id == "learn-to-play"
    assert hits[0].citation.page_or_section
    require_citations(hits)


def test_missing_corpus_fails_honestly() -> None:
    search = InMemoryRulesSearch([])
    with pytest.raises(CorpusUnavailableError):
        search.search("enemy phase")


def test_uncited_result_rejected() -> None:
    with pytest.raises(ValueError):
        require_citations([])


def test_card_lookup_is_separate_from_rules_search() -> None:
    cards = MemoryCardLookup({"141": {"code": "01141", "name": "Ruth Turner"}})
    search = InMemoryRulesSearch([])
    assert cards.lookup("141")["name"] == "Ruth Turner"
    with pytest.raises(CorpusUnavailableError):
        search.search("Ruth Turner")
    with pytest.raises(CardNotFoundError):
        cards.lookup("99999")
