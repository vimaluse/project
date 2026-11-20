# Assessment Submission Checklist

- [ ] FastAPI endpoint is `POST /link-analysis`.
- [ ] Request accepts a valid public HTTP/HTTPS website URL.
- [ ] Invalid URL, private IP, unsupported content type, timeout and HTTP errors are handled.
- [ ] HTML content and metadata are extracted.
- [ ] LLM is used for all five required analysis sections.
- [ ] Exactly five search query recommendations are returned.
- [ ] Exactly five service recommendations are returned.
- [ ] Competitors are labeled as suggestions unless externally verified.
- [ ] No fabricated search volumes or rankings.
- [ ] Pydantic validates the LLM response.
- [ ] Cache and cost estimate are included.
- [ ] `.env` is excluded from Git.
- [ ] Tests pass.
- [ ] README includes setup and API instructions.
- [ ] LLM comparison includes dated official prices and a reproducible model test.
- [ ] Swagger demo and GitHub repository are ready.
