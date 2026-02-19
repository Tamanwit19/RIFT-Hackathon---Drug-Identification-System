
RISK_RULES = {
    "CLOPIDOGREL": {
        "PM": ("Ineffective", "high"),
        "IM": ("Adjust Dosage", "moderate"),
        "NM": ("Safe", "none")
    },
    "SIMVASTATIN": {
        "PM": ("Toxic", "critical"),
        "IM": ("Adjust Dosage", "moderate"),
        "NM": ("Safe", "none")
    },
    "CODEINE": {
        "URM": ("Toxic", "critical"),
        "PM": ("Ineffective", "high"),
        "NM": ("Safe", "none")
    },
    "WARFARIN": {
        "PM": ("Adjust Dosage", "high"),
        "IM": ("Adjust Dosage", "moderate"),
        "NM": ("Safe", "none")
    },
    "AZATHIOPRINE": {
        "PM": ("Toxic", "critical"),
        "IM": ("Adjust Dosage", "moderate"),
        "NM": ("Safe", "none")
    },
    "FLUOROURACIL": {
        "PM": ("Toxic", "critical"),
        "IM": ("Adjust Dosage", "moderate"),
        "NM": ("Safe", "none")
    }
}

def evaluate_risk(drug: str, phenotype: str, gene_found: bool):
    drug_upper = drug.upper()
    drug_rules = RISK_RULES.get(drug_upper, {})
    
    # 1.0 -> We have a specific CPIC-level rule for this Drug + Phenotype
    if phenotype in drug_rules:
        risk_label, severity = drug_rules[phenotype]
        return risk_label, severity, 1.0
    
    # 0.7 -> Phenotype known, but no specific rule for this drug
    if phenotype != "Unknown":
        return "Unknown", "none", 0.7
    
    # 0.4 -> Gene found, but phenotype couldn't be determined
    if gene_found:
        return "Unknown", "none", 0.4
    
    # 0.1 -> No variants for the target gene found at all
    return "Safe", "none", 0.1