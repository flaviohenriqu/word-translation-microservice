import httpx

from .schemas import TranslationData


async def get_translation_data(word: str, translated_language: str):
    """
    Get translation data for a given word from Google Translate.

    Args:
        word (str): The word to fetch translation data for.
        translated_language (str): translated language

    Returns:
        dict: The translation data containing definitions, synonyms, translations, and examples.
            The dictionary structure is as follows:
            {
                "origin_language": str,
                "translations": List[Dict[str, str]],
            }
            Each item in the "translations" lists is a dictionary
            with the keys "src" and "data" representing the language of the translation and the corresponding
            translation data.
    """
    async with httpx.AsyncClient(cookies={"CONSENT": "YES+"}) as client:
        # Construct the URL for Google Translate
        base_url = "https://clients5.google.com/translate_a/single"
        url = f"{base_url}?dj=1&dt=t&dt=sp&dt=ld&dt=bd&client=dict-chrome-ex&sl=auto&tl={translated_language}&q={word}"

        try:
            # Send the HTTP request to Google Translate
            response = await client.get(url)
            response.raise_for_status()

            translation_data = response.json()
            src = translation_data["src"]
            translation_data["src"] = translated_language
            translation_data["data"] = translation_data["dict"]
            del translation_data["dict"]

            return TranslationData(
                word=word,
                origin_language=src,
                translations=[TranslationData.Translation(**translation_data)],
            )
        except httpx.RequestError as exc:
            # Handle any request errors
            print(f"An error occurred during the HTTP request: {exc}")
        except httpx.HTTPStatusError as exc:
            # Handle HTTP status errors
            print(f"Received unexpected status code: {exc.response.status_code}")

    return None
