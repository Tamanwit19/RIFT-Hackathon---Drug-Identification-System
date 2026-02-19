from pydantic import BaseModel, Field
from typing import List, Literal
from datetime import datetime

class RiskAssessment(BaseModel):
    risk_label: Literal["Safe", "Adjust Dosage", "Toxic", "Ineffective", "Unknown"]
    confidence_score: float = Field(..., ge=0, le=1) # Ensures score is between 0.0 and 1.0
    severity: Literal["none", "low", "moderate", "high", "critical"]

class DetectedVariant(BaseModel):
    rsid: str
    gene: str
    star_allele: str

class PharmacogenomicProfile(BaseModel):
    primary_gene: str
    diplotype: str
    phenotype: Literal["PM", "IM", "NM", "RM", "URM", "Unknown"]
    detected_variants: List[DetectedVariant]

class ClinicalRecommendation(BaseModel):
    recommendation_text: str
    guideline_source: str

class LLMGeneratedExplanation(BaseModel):
    summary: str
    mechanism: str
    clinical_impact: str

class QualityMetrics(BaseModel):
    vcf_parsing_success: bool
    variants_detected: int
    gene_match_found: bool

class PGxResponse(BaseModel):
    """The final structured JSON output required by the frontend"""
    patient_id: str
    drug: str
    timestamp: datetime
    risk_assessment: RiskAssessment
    pharmacogenomic_profile: PharmacogenomicProfile
    clinical_recommendation: ClinicalRecommendation
    llm_generated_explanation: LLMGeneratedExplanation
    quality_metrics: QualityMetrics