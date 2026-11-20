from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from app.schemas import LinkAnalysisRequest, LinkAnalysisResponse
from app.services.analysis_service import analyze_website
from app.config import settings
from app.services.cache import AnalysisCache

app = FastAPI(
    title="WebIntel AI",
    description="Evidence-aware website intelligence and market analysis API",
    version="1.0.0",
)
cache = AnalysisCache(settings.cache_db)

@app.get("/health")
async def health():
    return {"status": "ok", "service": "WebIntel AI"}

@app.post("/link-analysis", response_model=LinkAnalysisResponse)
async def link_analysis(payload: LinkAnalysisRequest):
    try:
        result = await analyze_website(payload.url, cache)
        return result
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc))
    except TimeoutError:
        raise HTTPException(status_code=504, detail="The website or AI provider timed out.")
    except RuntimeError as exc:
        raise HTTPException(status_code=502, detail=str(exc))
    except Exception:
        # Avoid exposing internal exception details or secrets to API clients.
        raise HTTPException(status_code=500, detail="Unexpected analysis error. Check server logs.")
