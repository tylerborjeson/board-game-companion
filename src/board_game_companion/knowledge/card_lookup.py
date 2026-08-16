from __future__ import annotations

import json
import urllib.error
import urllib.request
from typing import Any, Protocol

API = "https://arkhamdb.com/api/public"
UA = "board-game-companion (https://github.com/tylerborjeson/board-game-companion)"


class CardLookup(Protocol):
    def lookup(self, collector_number: str) -> dict[str, Any]:
        ...


class CardNotFoundError(LookupError):
    pass


def _fetch(url: str) -> Any:
    request = urllib.request.Request(url, headers={"Accept": "application/json", "User-Agent": UA})
    with urllib.request.urlopen(request) as response:
        return json.load(response)


class ArkhamDbCardLookup:
    def lookup(self, collector_number: str) -> dict[str, Any]:
        token = collector_number.strip().lstrip("#")
        if not token.isdigit():
            raise CardNotFoundError(f"expected a collector number, got {collector_number!r}")
        if len(token) >= 5:
            card = self._fetch_card(token)
            if card:
                return card
            raise CardNotFoundError(f"no card for code {token}")
        position = int(token)
        card = self._fetch_card(f"01{position:03d}")
        if card:
            return card
        for pack in ("rcore", "core"):
            card = self._find_in_pack(pack, position)
            if card:
                return card
        raise CardNotFoundError(f"no card for collector number {position}")

    def _fetch_card(self, code: str) -> dict[str, Any] | None:
        try:
            payload = _fetch(f"{API}/card/{code}")
        except urllib.error.HTTPError:
            return None
        if not isinstance(payload, dict) or not payload.get("code"):
            return None
        return payload

    def _find_in_pack(self, pack: str, position: int) -> dict[str, Any] | None:
        try:
            cards = _fetch(f"{API}/cards/{pack}")
        except urllib.error.HTTPError:
            return None
        if not isinstance(cards, list):
            return None
        matches = [card for card in cards if card.get("position") == position]
        return matches[0] if matches else None


class MemoryCardLookup:
    def __init__(self, cards: dict[str, dict[str, Any]] | None = None) -> None:
        self.cards = cards or {}

    def lookup(self, collector_number: str) -> dict[str, Any]:
        token = collector_number.strip().lstrip("#")
        card = self.cards.get(token) or self.cards.get(token.zfill(5))
        if not card:
            raise CardNotFoundError(f"no card for collector number {collector_number}")
        return card
