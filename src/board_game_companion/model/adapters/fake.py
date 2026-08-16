from __future__ import annotations

from board_game_companion.model.provider import ProviderError, ProviderRequest, parse_model_payload
from board_game_companion.model.response_models import ModelTurnResponse


class FakeProvider:
    def __init__(
        self,
        scripted: dict[str, ModelTurnResponse] | None = None,
        *,
        fail: bool = False,
        malformed: bool = False,
    ) -> None:
        self.scripted = scripted or {}
        self.fail = fail
        self.malformed = malformed

    def complete(self, request: ProviderRequest) -> ModelTurnResponse:
        if self.fail:
            raise ProviderError("fake provider failure")
        if self.malformed:
            return parse_model_payload({"not": "a valid turn"})
        for needle, response in self.scripted.items():
            if needle.lower() in request.turn_text.lower():
                return response
        raise ProviderError("fake provider has no scripted response for this turn")
