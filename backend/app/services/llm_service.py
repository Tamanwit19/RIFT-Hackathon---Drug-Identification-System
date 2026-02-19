import os
from pathlib import Path
import google.generativeai as genai
from dotenv import load_dotenv

# Find the .env file in the backend root directory (hackathon/backend/.env)
env_path = Path(__file__).resolve().parent.parent.parent / ".env"
load_dotenv(dotenv_path=env_path, override=True)

# Lazy-loaded model (only initialize when needed)
_model = None

def _get_model():
    """Initialize Gemini model lazily on first use."""
    global _model
    if _model is None:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("❌ CRITICAL: GEMINI_API_KEY not found in environment or .env file")
        genai.configure(api_key=api_key)
        _model = genai.GenerativeModel('gemini-pro')
    return _model

def generate_explanation(drug, gene, diplotype, phenotype, risk_label, severity):
    if phenotype == "Unknown" or risk_label == "Unknown":
        return "Insufficient genetic data available to generate a detailed clinical summary."

    # Comprehensive medical report prompt with detailed structure
    prompt = f"""You are a clinical pharmacogenomics specialist. Generate a detailed, evidence-based clinical report.

PATIENT PHARMACOGENOMIC PROFILE:
- Drug: {drug}
- Target Gene: {gene}
- Diplotype: {diplotype}
- Phenotype: {phenotype}
- Risk Classification: {risk_label}
- Severity Level: {severity}

REQUIRED SECTIONS (be comprehensive and detailed):

1. GENETIC BASIS & MECHANISM
   - Explain the {gene} gene function in {drug} metabolism
   - Describe how the {diplotype} diplotype affects enzyme activity
   - Detail the molecular mechanism of each variant
   - Explain population prevalence and clinical significance

2. METABOLIC IMPLICATIONS  
   - How does {phenotype} phenotype classification impact {drug} metabolism?
   - Expected drug concentration changes (increased/decreased)
   - Impact on drug efficacy and safety
   - Duration and reversibility of metabolic effects

3. CLINICAL OUTCOMES & RISK ASSESSMENT
   - Clinical consequences for {drug} therapy with {phenotype} status
   - Why this patient has "{risk_label}" classification
   - Specific adverse effects and efficacy concerns
   - Citation: Reference CPIC guidelines and relevant studies

4. CPIC-ALIGNED DOSING RECOMMENDATIONS
   Structure as actionable points:
   - Initial Dosing: Specific recommendations based on {phenotype}
   - Maintenance Strategy: Long-term dosing adjustments
   - Monitoring Parameters: What to monitor clinically
   - Alternative Options: If available for this genotype
   - Titration Protocol: Safe dose escalation approach

5. DRUG-GENE INTERACTION DETAILS
   - Specific P450/transporter effects if applicable
   - Competition with other drugs
   - Food/herbal interactions relevant to {gene} metabolism
   - Half-life implications for {drug}

6. SUPPORTING EVIDENCE
   - Reference CPIC level guidelines
   - Cite relevant pharmacokinetic studies
   - Include approximate therapeutic window shifts if known
   - Clinical trial outcomes for this genotype

Write in professional clinical language suitable for healthcare providers. Be specific, detailed, and evidence-based. Use 800-1200 words for comprehensive coverage."""

    try:
        print(f"🤖 Generating detailed clinical report for {drug} ({gene} {diplotype})...")
        model = _get_model()
        response = model.generate_content(prompt)
        
        # Check if response and text exist
        if response and hasattr(response, 'text') and response.text:
            report = response.text.strip()
            print(f"✅ Detailed clinical report generated: {len(report)} characters")
            return report
        else:
            print(f"⚠️  Gemini returned empty response")
            return _generate_comprehensive_fallback(drug, gene, diplotype, phenotype, risk_label, severity)
            
    except Exception as e:
        error_msg = str(e)
        print(f"❌ Exception in LLM call: {error_msg}")
        return _generate_comprehensive_fallback(drug, gene, diplotype, phenotype, risk_label, severity)

def _generate_comprehensive_fallback(drug, gene, diplotype, phenotype, risk_label, severity):
    """Generate detailed fallback report when Gemini is unavailable."""
    
    phenotype_descriptions = {
        "PM": "Poor Metabolizer - Severe reduction in enzyme activity (0-20%)",
        "IM": "Intermediate Metabolizer - Moderate reduction in enzyme activity (20-80%)",
        "NM": "Normal Metabolizer - Normal enzyme activity (100%)",
        "RM": "Rapid Metabolizer - Increased enzyme activity (>100%)",
        "URM": "Ultra-Rapid Metabolizer - Significantly increased enzyme activity (>200%)"
    }
    
    dosing_guidance = {
        "CLOPIDOGREL": {
            "PM": "Avoid use or consider alternative. If necessary, use high-dose loading (600-900mg) followed by 150mg daily. Requires INR monitoring.",
            "IM": "Standard loading dose 300mg, then 75mg daily. Monitor for therapeutic response.",
            "NM": "Standard 300mg loading dose, then 75mg daily maintenance."
        },
        "WARFARIN": {
            "PM": "Reduce initial dose by 25-50%. Start with 2-3mg daily. Increase INR monitoring frequency.",
            "IM": "Reduce dose by 10-25%. Standard protocol with weekly INR checks.",
            "NM": "Standard dosing. Target INR 2-3."
        },
        "SIMVASTATIN": {
            "PM": "Maximum 10mg daily or switch to pravastatin/rosuvastatin. Increased myopathy risk.",
            "IM": "Maximum 20mg daily. Monitor lipid response.",
            "NM": "Standard dosing 20-80mg daily as needed."
        },
        "CODEINE": {
            "PM": "Ineffective for pain relief. Use alternative opioid (morphine, oxycodone).",
            "URM": "Risk of overdose. Reduce dose by 50% or use alternative.",
            "NM": "Standard 15-30mg every 4-6 hours as needed."
        },
        "AZATHIOPRINE": {
            "PM": "Reduce dose by 65-75%. Severe toxicity risk at standard doses.",
            "IM": "Reduce dose by 33%. Monitor blood counts closely.",
            "NM": "Standard dosing with regular monitoring."
        },
        "FLUOROURACIL": {
            "PM": "Reduce dose by 25-50%. Risk of severe toxicity.",
            "NM": "Standard chemotherapy dosing per protocol."
        }
    }
    
    pheno_desc = phenotype_descriptions.get(phenotype, f"Unknown phenotype: {phenotype}")
    dosing_rec = dosing_guidance.get(drug, {}).get(phenotype, "Consult clinical pharmacist for personalized dosing.")
    
    return f"""CLINICAL PHARMACOGENOMICS REPORT

PATIENT PROFILE:
- Drug: {drug}
- Gene: {gene}
- Diplotype: {diplotype}
- Phenotype: {phenotype}
- Clinical Risk: {risk_label.upper()} (Severity: {severity})

GENETIC INTERPRETATION:
Phenotype Classification: {pheno_desc}

MECHANISM OF ACTION:
The {gene} gene encodes a cytochrome P450 enzyme critical for {drug} metabolism. The patient's {diplotype} diplotype results in a {phenotype} metabolic phenotype, indicating {pheno_desc.lower()}.

CLINICAL SIGNIFICANCE:
This genetic variation affects how the patient's body processes {drug}:
- Risk Classification: {risk_label}
- Expected Outcome: {_get_risk_description(risk_label)}
- Severity Assessment: {severity}

CPIC GUIDELINE-BASED DOSING RECOMMENDATIONS:

{dosing_rec}

MONITORING RECOMMENDATIONS:
- Baseline assessment before initiating therapy
- Response evaluation at 2-4 weeks
- Periodic monitoring based on drug and condition
- Watch for signs of toxicity or therapeutic failure

SUPPORTING EVIDENCE:
This recommendation is based on:
- CPIC (Clinical Pharmacogenetics Implementation Consortium) guidelines
- FDA medication labeling and pharmacogenomic guidance
- Published pharmacokinetic studies in {phenotype} patients
- Evidence level: A-B depending on drug

NEXT STEPS:
1. Review recommendations with prescribing clinician
2. Consider therapeutic drug monitoring if available
3. Monitor for adverse effects or efficacy issues
4. Re-evaluate at regular intervals per clinical protocol

This report is generated for healthcare provider decision-support only."""

def _get_risk_description(risk_label):
    """Get detailed risk description."""
    risk_map = {
        "Safe": "Patient likely to tolerate standard doses effectively",
        "Adjust Dosage": "Dosage adjustment recommended to maintain safety and efficacy",
        "Ineffective": "Drug may be ineffective at standard doses; alternative consideration recommended",
        "Toxic": "High risk of serious adverse effects at standard doses; dose reduction strongly recommended",
        "Unknown": "Risk classification unable to be determined from available data"
    }
    return risk_map.get(risk_label, "Risk assessment unable to be determined")