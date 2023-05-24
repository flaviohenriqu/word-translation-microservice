from typing import Optional

from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException

from . import services
from .models import WordRead

router = APIRouter()


@router.get("/word/{word}", response_model=Optional[WordRead])
async def get_word(
    word: str,
    translated_language: str,
    word_service: services.WordService = Depends(),
):
    result = await word_service.get_word(word, translated_language)
    if result is None:
        raise HTTPException(status_code=404, detail="Word not found")
    return result


@router.get("/words")
async def get_words(
    skip: int = 0,
    limit: int = 10,
    include_translations: bool = False,
    word_filter: str = "",
    word_service: services.WordService = Depends(),
):
    return await word_service.get_words(
        skip=skip,
        limit=limit,
        include_translations=include_translations,
        word_filter=word_filter,
    )


@router.delete("/word/{word_id}")
async def delete_word(
    word_id: int,
    word_service: services.WordService = Depends(),
):
    return await word_service.delete_word(word_id)
