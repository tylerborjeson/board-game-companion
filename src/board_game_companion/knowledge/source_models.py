from __future__ import annotations

from pydantic import BaseModel, Field


class Citation(BaseModel):
    source_id: str
    title: str
    edition: str | None = None
    page_or_section: str | None = None
    locator: str | None = None


class SourceRecord(BaseModel):
    id: str
    title: str
    kind: str
    required: bool = False
    edition: str | None = None
    url: str | None = None
    pointer: str | None = None
    local_pdf: str | None = None
    normalized_dir: str | None = None
    license: str | None = None
    notes: str | None = None


class SourceChunk(BaseModel):
    source_id: str
    title: str
    edition: str | None = None
    page_or_section: str | None = None
    text: str
    topics: list[str] = Field(default_factory=list)
    license: str | None = None


class SearchHit(BaseModel):
    chunk: SourceChunk
    citation: Citation
    score: float = 1.0
