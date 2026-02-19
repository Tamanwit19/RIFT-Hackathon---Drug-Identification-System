# The "Big 6" PGx Genes supported by this application
SUPPORTED_GENES = ["CYP2D6", "CYP2C19", "CYP2C9", "SLCO1B1", "TPMT", "DPYD"]

# CPIC Tier 1 Drug-to-Gene Mapping
DRUG_GENE_MAP = {
    "CODEINE": "CYP2D6",
    "WARFARIN": "CYP2C9",
    "CLOPIDOGREL": "CYP2C19",
    "SIMVASTATIN": "SLCO1B1",
    "AZATHIOPRINE": "TPMT",
    "FLUOROURACIL": "DPYD"
}

def get_primary_gene(drug: str):
    """Returns the primary metabolizing gene for a given drug name."""
    return DRUG_GENE_MAP.get(drug.upper())