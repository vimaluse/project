# WebIntel AI — Website Intelligence & Market Analysis Engine

A FastAPI application that accepts a public website URL, extracts visible website content, and uses an LLM to produce structured competitor, search-query, SEO, service, and audience insights.

## What makes this implementation different

- Evidence-aware outputs: website facts, AI inferences, and research-required claims are distinguished.
- Competitors are explicitly labeled as AI suggestions unless independently verified.
- No invented search volume, rankings, traffic, or market share.
- URL validation and basic SSRF defenses, including redirect re-validation.
- Pydantic validation of the generated analysis.
- SQLite cache to reduce repeat requests.
- Token and cost estimates, clearly labeled as estimates.
- Provider selection through environment variables.

## Requirements

- Python 3.10+
- API key for one supported provider

## Windows PowerShell setup

```powershell
cd path\to\webintel-ai
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
notepad .env
```

Add your Gemini API key to `GEMINI_API_KEY` in `.env`.

## Run

```powershell
uvicorn app.main:app --host 127.0.0.1 --port 4000 --reload
```

Open:
- Swagger: http://127.0.0.1:4000/docs
- Health: http://127.0.0.1:4000/health

## API request

`POST /link-analysis`

```json
{
  "url": "https://example.com"
}
```

## Switch provider

Set `LLM_PROVIDER` in `.env` to `gemini`, `openai`, or `anthropic`, provide the matching API key, and update the model and pricing variables. Provider SDKs are included so the same API contract can be retained.

## Run tests

```powershell
pytest -q
```

## Architecture

1. `main.py`: HTTP routes and API error mapping.
2. `schemas.py`: request and response contracts.
3. `utils/validators.py`: URL and public-IP validation.
4. `services/website_extractor.py`: bounded HTTP fetch, redirect checks, HTML cleanup and metadata extraction.
5. `services/llm_service.py`: provider adapter and structured analysis prompt.
6. `services/analysis_service.py`: orchestration, brand summary, cost estimate and cache.
7. `services/cache.py`: SQLite TTL cache.

## Security notes and production hardening

This is an assessment-ready baseline, not a fully hardened crawler. DNS validation followed by a normal HTTP connection can still leave a DNS-rebinding/time-of-check-to-time-of-use gap. A production deployment should use an egress proxy or a custom transport that pins the validated public IP while preserving TLS hostname verification. Also add per-user rate limits, request concurrency limits, structured logging, secret management, response-size limits at the reverse proxy, and monitoring. Consider disabling redirects entirely if redirect support is not required.

Website HTML is untrusted input. The prompt explicitly treats page content as data, but production systems should also test prompt-injection pages and constrain output claims.

## Important limitations

- This implementation analyzes the submitted page, not an entire multi-page site.
- Competitor names are AI-generated suggestions unless external research is added.
- Search query recommendations are semantic suggestions, not measured search-volume data.
- SEO score is a transparent heuristic based on page metadata and headings, not a Google score.
- Token counts and cost are estimates. For exact cost, record provider-reported usage metadata.
- The extractor does not execute JavaScript. Some sites may require a browser renderer such as Playwright.

## LLM model research

Create `docs/llm_model_comparison.md` with the date of your research, official pricing links, context limits, and a small repeatable evaluation. Do not describe estimated latency as measured latency. Compare output quality using the same 5–10 test URLs and a rubric for factual grounding, relevance, schema validity, and completeness.

## Suggested next improvements

1. Add an external search provider for competitor verification.
2. Add Playwright fallback for JavaScript-rendered pages.
3. Add a deterministic SEO audit score based on title/meta/H1/heading/link checks.
4. Persist analysis history and expose `GET /analyses/{id}`.
5. Add Docker, CI workflow, rate limiting, and observability.
