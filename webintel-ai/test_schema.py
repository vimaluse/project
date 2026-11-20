
import asyncio

from google import genai
from google.genai import types
from pydantic import BaseModel

from app.config import settings


class TestResponse(BaseModel):
    brand: str
    category: str
    summary: str


async def main():

    client = genai.Client(
        api_key=settings.gemini_api_key
    )

    try:
        response = await client.aio.models.generate_content(
            model=settings.gemini_model,
            contents="Describe Apple as a technology brand.",
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=TestResponse,
                temperature=0.2,
            ),
        )

        print("STRUCTURED TEST SUCCESS")
        print(response.text)

    except Exception as e:
        print("STRUCTURED TEST FAILED")
        print(type(e).__name__)
        print(str(e))


asyncio.run(main())
