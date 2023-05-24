from typing import List, Optional

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.exc import NoResultFound

from .database import get_db
from .models import Translation, Word, WordRead
from .schemas import PaginatedWords
from .utils import get_translation_data


class WordService:
    def __init__(self, database: AsyncSession = Depends(get_db)):
        self.database = database

    async def get_word(self, word: str, translated_language: str) -> Optional[WordRead]:
        # Check if the word already exists in the database
        try:
            stmt = select(Word).where(Word.word == word)
            stmt = stmt.join(Translation).filter(
                Word.translations.any(Translation.src == translated_language)
            )
            result = await self.database.execute(stmt)
            db_word = result.scalars().first()
        except NoResultFound:
            db_word = None

        # If the word is already in the database, return it
        if db_word:
            return db_word

        result = await self.database.execute(
            select(Word).where(Word.word == word).join(Translation)
        )
        word_obj = result.scalars().first()
        # Fetch translation data from Google Translate
        translation_data = await get_translation_data(word, translated_language)

        # Check if the translated language already exists in the word object
        if word_obj:
            for translation in translation_data.translations:
                word_obj.translations.append(
                    Translation(
                        src=translation.src,
                        data=translation.data,
                        sentences=translation.sentences,
                    )
                )
        else:
            # Create the Word object and populate with translation data
            word_obj = Word(word=word, origin_language=translation_data.origin_language)
            for translation in translation_data.translations:
                word_obj.translations.append(
                    Translation(
                        src=translation.src,
                        data=translation.data or [],
                        sentences=translation.sentences,
                    )
                )

        # Save the word object to the database
        self.database.add(word_obj)
        await self.database.commit()

        return word_obj

    async def get_words(
        self,
        skip: int = 0,
        limit: int = 10,
        include_translations: bool = False,
        word_filter: str = "",
    ):
        """
        Get a list of words stored in the database.

        Args:
            skip (int): Number of words to skip (for pagination).
            limit (int): Maximum number of words to retrieve (for pagination).
            include_translations (bool): Whether to include translations in the response.
            word_filter (str): Filter words based on a partial match.

        Returns:
            PaginatedWords: Paginated word response containing the total count and list of words.
        """
        query = select(Word)

        if word_filter:
            query = query.where(Word.word.ilike(f"%{word_filter}%"))

        result = await self.database.execute(query)
        total_count = len(result.all())

        if include_translations:
            query = query.join(Translation)
        query = query.offset(skip).limit(limit)
        result = await self.database.execute(query)
        words = result.scalars().all()

        return PaginatedWords(total_count=total_count, words=words)

    async def delete_word(self, word_id: int):
        """
        Delete a word from the database.

        Args:
            word_id (int): ID of the word to delete.

        Returns:
            dict: Dictionary with the deletion status message.
        """
        word = await self.database.execute(select(Word).where(Word.id == word_id))
        word = word.scalar_one_or_none()
        if word:
            await self.database.delete(word)
            await self.database.commit()
            return {"message": "Word deleted successfully"}
        else:
            return {"message": "Word not found"}
