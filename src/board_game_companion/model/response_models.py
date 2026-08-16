from __future__ import annotations

from pydantic import BaseModel, Field

from board_game_companion.domain.commands import CommandProposal
from board_game_companion.domain.enums import TurnKind
from board_game_companion.knowledge.source_models import Citation


class ModelTurnResponse(BaseModel):
    kind: TurnKind
    summary: str
    needs_confirmation: bool = False
    uncertainty: str | None = None
    proposals: list[CommandProposal] = Field(default_factory=list)
    table_summary: str = ""
    fiction: str = ""
    rule: str = ""
    application: str = ""
    mentor_advice: str = ""
    next_question: str = ""
    citations: list[Citation] = Field(default_factory=list)
