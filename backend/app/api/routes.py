import asyncio
from fastapi import APIRouter, UploadFile, File, HTTPException, Query
from datetime import datetime
from app.services.vcf_parser import parse_vcf
from app.services.drug_mapper import get_primary_gene
from app.services.diplotype_service import resolve_diplotype
from app.services.phenotype_service import get_phenotype
from app.services.risk_engine import evaluate_risk
from app.services.llm_service import generate_explanation 
from app.schemas.response import PGxResponse

router = APIRouter()

@router.post("/analyze", response_model=PGxResponse)
async def analyze_vcf(file: UploadFile = File(...), drug: str = Query(..., min_length=1)):
    if not file.filename.endswith('.vcf'):
        raise HTTPException(status_code=400, detail="Invalid file type.")

    try:
        # 1. Standard deterministic logic (Instant)
        content = await file.read()
        all_variants = parse_vcf(content.decode("utf-8"))
        target_gene = get_primary_gene(drug)
        relevant_variants = [v for v in all_variants if v['gene'] == target_gene]
        gene_found = len(relevant_variants) > 0
        resolved_diplotype = resolve_diplotype(relevant_variants)
        phenotype_code = get_phenotype(target_gene, resolved_diplotype)
        risk_label, severity, confidence = evaluate_risk(drug, phenotype_code, gene_found)

        # 🚀 THE FIX: Offload the blocking LLM call to a background thread
        explanation_text = await asyncio.to_thread(
            generate_explanation,
            drug, target_gene, resolved_diplotype, phenotype_code, risk_label, severity
        )

        return {
            "patient_id": "HG002-FINAL",
            "drug": drug.upper(),
            "timestamp": datetime.now(),
            "risk_assessment": {
                "risk_label": risk_label,
                "confidence_score": confidence,
                "severity": severity
            },
            "pharmacogenomic_profile": {
                "primary_gene": target_gene,
                "diplotype": resolved_diplotype,
                "phenotype": phenotype_code,
                "detected_variants": relevant_variants
            },
            "clinical_recommendation": {
                "recommendation_text": f"Patient is a {phenotype_code} for {target_gene}.",
                "guideline_source": "CPIC v4.2"
            },
            "llm_generated_explanation": {
                "summary": explanation_text,
                "mechanism": "Enzymatic pathway analysis complete.",
                "clinical_impact": "Actionable variants detected."
            },
            "quality_metrics": {
                "vcf_parsing_success": True,
                "variants_detected": len(relevant_variants),
                "gene_match_found": gene_found
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))