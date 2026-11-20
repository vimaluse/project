# LLM Platform Comparison — WebIntel AI

**Research date:** 18 November 2026  
**Important:** Prices below are API token prices, not consumer chat subscriptions. Verify them again immediately before submission because providers can change model availability and pricing.

| Provider | Candidate model | Input / 1M tokens | Output / 1M tokens | Fit |
|---|---|---:|---:|---|
| Google | Gemini 2.5 Flash-Lite | $0.10 | $0.40 | Lowest-cost candidate for structured extraction and synthesis |
| Anthropic | Claude Haiku 5.5 | $0.10* | $0.50* | Fast, cost-efficient analysis candidate |
| OpenAI | GPT-6 Luna | $0.05 | $0.25 | Low-cost candidate with structured-output support; benchmark before selection |

*Anthropic Haiku 5.5 pricing depends on prompt length; the cited $0.10/$0.50 rate applies to prompts up to 100K tokens.

## Recommendation

Start with Gemini 2.5 Flash-Lite because the assessment needs a cost-efficient model for a bounded amount of extracted text and structured JSON. Do not claim it is the most accurate without a controlled evaluation. Keep provider selection configurable so another model can be substituted if its measured quality is better.

## Per-analysis cost example

Assume 5,000 input tokens and 3,500 output tokens:

- Input: 5,000 × $0.10 / 1,000,000 = $0.0005
- Output: 3,500 × $0.40 / 1,000,000 = $0.0014
- Estimated total: $0.0019 per analysis

This is a token-price calculation, not a measured bill. Actual tokenization, system prompt, provider-side reasoning, retries, and output length can change the total.

## Evaluation plan

Use the same 10 websites across all candidate models. Score each response from 1–5 for:

1. Brand facts supported by extracted evidence.
2. Competitor relevance and honest uncertainty.
3. Search query relevance.
4. SEO recommendation specificity.
5. Service and audience extraction accuracy.
6. Validity of the required JSON schema.

Report median latency from at least five runs per URL and record provider-reported token usage. Keep network fetch time separate from model generation time.

## Official sources

- Google Gemini API pricing: https://ai.google.dev/gemini-api/docs/pricing
- OpenAI API pricing: https://developers.openai.com/api/docs/pricing (GPT-6 Luna standard rates shown in the current pricing table; confirm availability for your API account).
- Anthropic model pricing: https://platform.claude.com/docs/en/about-claude/pricing
- Anthropic Haiku 5.5: https://www.anthropic.com/claude/haiku
