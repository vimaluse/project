from typing import Literal
from pydantic import BaseModel, Field, HttpUrl, ConfigDict

class LinkAnalysisRequest(BaseModel):
    url: HttpUrl

class Evidence(BaseModel):
    statement: str
    source: Literal["website", "inference", "external_research_required"]
    evidence: str = ""

class Competitor(BaseModel):
    name: str
    overview: str
    strengths: list[str] = Field(default_factory=list)
    weaknesses_or_gaps: list[str] = Field(default_factory=list)
    relationship: Literal["identified_on_website", "ai_suggested", "externally_verified"] = "ai_suggested"
    confidence: Literal["low", "medium", "high"] = "medium"

class CompetitorAnalysis(BaseModel):
    brand_overview: str
    business_category: str
    main_products_services: list[str]
    competitors: list[Competitor] = Field(default_factory=list)
    brand_strengths: list[str] = Field(default_factory=list)
    competitive_advantages: list[str] = Field(default_factory=list)
    positioning_opportunities: list[str] = Field(default_factory=list)
    evidence_notes: list[str] = Field(default_factory=list)

class SearchQuery(BaseModel):
    query: str
    platforms: list[Literal["Google", "Facebook", "Instagram", "LinkedIn", "X"]]
    intent: str
    business_relevance: str
    target_audience: str

class SEOImprovements(BaseModel):
    primary_keyword: str
    secondary_keywords: list[str]
    long_tail_keywords: list[str]
    business_keywords: list[str]
    recommended_title: str
    meta_description: str
    title_observation: str
    meta_observation: str
    supporting_content: list[str]
    seo_score: int = Field(ge=0, le=100)
    score_explanation: list[str]

class Service(BaseModel):
    service_name: str
    description: str
    target_industry: str
    target_customer: str
    main_benefit: str
    evidence_status: Literal["found_on_website", "inferred_recommendation"]

class TargetAudience(BaseModel):
    primary_audience: list[str]
    secondary_audience: list[str]
    industries: list[str]
    business_types: list[str]
    customer_profiles: list[str]
    geography: list[str]
    customer_needs: list[str]
    potential_interests: list[str]
    recommended_marketing_segments: list[str]

class Analysis(BaseModel):
    competitor_analysis: CompetitorAnalysis
    target_search_queries: list[SearchQuery] = Field(min_length=5, max_length=5)
    seo_improvements: SEOImprovements
    top_services: list[Service] = Field(min_length=5, max_length=5)
    target_audience: TargetAudience

class Brand(BaseModel):
    name: str
    category: str
    summary: str

class UsageEstimate(BaseModel):
    input_tokens_estimated: int
    output_tokens_estimated: int
    estimated_cost_usd: float
    model: str
    note: str

class LinkAnalysisResponse(BaseModel):
    success: bool = True
    website: str
    brand: Brand
    analysis: Analysis
    extraction: dict
    usage_estimate: UsageEstimate
    cached: bool = False

    model_config = ConfigDict(extra="forbid")
