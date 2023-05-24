from typing import List, Optional

from pydantic import BaseModel, Field

from .models import Word


class TranslationData(BaseModel):
    word: str
    origin_language: str
    translations: List["TranslationData.Translation"]

    class Translation(BaseModel):
        sentences: List[dict]
        data: Optional[List[dict]] = Field(...)
        src: str


class PaginatedWords(BaseModel):
    total_count: int
    words: List[Word]
