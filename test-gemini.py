
import asyncio
from google import genai
from google.genai import types

from app.config import settings
from app.schemas import Analysis

async def main():

    client = genai.Client(
        api_key=settings.gemini_api_key
    )

    try:
        response = await client.aio.models.generate_content(
            model=settings.gemini_model,
            contents="Analyze a fictional company selling software. Return a minimal valid analysis.",
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=Analysis,
                temperature=0.2,
            ),
        )

        print("STRUCTURED GENERATION SUCCESS")
        print(response.text)

        data = Analysis.model_validate_json(response.text)

        print("PYDANTIC VALIDATION SUCCESS")
        print(data)

    except Exception as e:
        print("ERROR:", type(e).__name__)
        print("DETAILS:", str(e))


asyncio.run(main())
