from __future__ import annotations

from typing import Any, Protocol

from pydantic import BaseModel, ValidationError

from board_game_companion.model.response_models import ModelTurnResponse


class ProviderError(RuntimeError):
    pass


class ProviderRequest(BaseModel):
    persona: str
    turn_text: str
    state_summary: str
    retrieved_rules: list[str] = []


class ModelProvider(Protocol):
    def complete(self, request: ProviderRequest) -> ModelTurnResponse:
        ...


def parse_model_payload(payload: Any) -> ModelTurnResponse:
    try:
        if isinstance(payload, ModelTurnResponse):
            return payload
        return ModelTurnResponse.model_validate(payload)
    except ValidationError as exc:
        raise ProviderError(f"malformed provider output: {exc}") from exc
