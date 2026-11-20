
import asyncio

from google import genai
from google.genai import types

from app.config import settings


async def main():

    client = genai.Client(
        api_key=settings.gemini_api_key
    )

    try:

        response = await client.aio.models.generate_content(
            model=settings.gemini_model,
            contents="Return JSON describing Apple as a technology company.",
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                temperature=0.2,
            ),
        )

        print("JSON MODE SUCCESS")
        print(response.text)

    except Exception as e:

        print("JSON MODE FAILED")
        print(type(e).__name__)
        print(str(e))


asyncio.run(main())
