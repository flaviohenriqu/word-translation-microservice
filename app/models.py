from typing import List, Optional

from sqlalchemy import JSON
from sqlmodel import Column, Field, Relationship, SQLModel


class WordBase(SQLModel):
    word: str
    origin_language: str


class Word(WordBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    translations: List["Translation"] = Relationship(
        back_populates="word",
        sa_relationship_kwargs={"cascade": "all, delete", "lazy": "selectin"},
    )


class TranslateBase(SQLModel):
    word_id: int = Field(foreign_key="word.id")
    sentences: List[dict] = Field(sa_column=Column(JSON), default=[])
    data: Optional[List[dict]] = Field(sa_column=Column(JSON), default=[])
    src: str


class Translation(TranslateBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    word: Optional[Word] = Relationship(
        back_populates="translations", sa_relationship_kwargs={"lazy": "selectin"}
    )


class TranslationRead(TranslateBase):
    pass


class WordRead(WordBase):
    translations: List[TranslationRead] = []
