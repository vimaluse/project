from app.config import settings
from app.schemas import LinkAnalysisResponse, Brand, UsageEstimate
from app.services.website_extractor import fetch_website
from app.services.llm_service import generate_analysis
from app.utils.validators import normalize_and_validate_url

def infer_brand_name(site: dict) -> str:
    title = site.get("title", "").strip()
    if title:
        return title.split("|")[0].split("—")[0].split("-")[0].strip()[:100]
    from urllib.parse import urlparse
    host = urlparse(site["final_url"]).hostname or "Unknown brand"
    return host.removeprefix("www.")

async def analyze_website(url: str, cache):
    safe_url = normalize_and_validate_url(url)
    site = await fetch_website(safe_url)
    key = cache.key(site["final_url"], site["text"])
    cached = cache.get(key)
    if cached:
        cached["cached"] = True
        return cached

    analysis = await generate_analysis(site)
    brand_name = infer_brand_name(site)
    summary = analysis.competitor_analysis.brand_overview
    input_tokens = max(1, (len(site["text"]) + 1200) // 4)
    output_tokens = 3500
    cost = ((input_tokens * settings.model_input_usd_per_million) +
            (output_tokens * settings.model_output_usd_per_million)) / 1_000_000

    result = LinkAnalysisResponse(
        website=site["final_url"],
        brand=Brand(name=brand_name, category=analysis.competitor_analysis.business_category, summary=summary),
        analysis=analysis,
        extraction={k:v for k,v in site.items() if k != "text"} |
                   {"content_included_in_analysis": True, "evidence_policy": "Website facts are separated from AI inference."},
        usage_estimate=UsageEstimate(
            input_tokens_estimated=input_tokens, output_tokens_estimated=output_tokens,
            estimated_cost_usd=round(cost, 8), model=settings.model_display_name,
            note="Estimate only; actual provider token usage and billing may differ."
        ),
        cached=False,
    ).model_dump()
    cache.set(key, result)
    return result
