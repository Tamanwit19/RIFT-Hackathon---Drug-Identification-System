
# Standard clinical mapping for key pharmacogenomic genes
PHENOTYPE_MAP = {
    "CYP2C19": {
        "*1/*1": "NM",  # Normal Metabolizer
        "*1/*2": "IM",  # Intermediate Metabolizer
        "*2/*1": "IM",
        "*2/*2": "PM",  # Poor Metabolizer
        "*1/*3": "IM",
        "*3/*1": "IM",
        "*2/*3": "PM",
        "*3/*2": "PM",
        "*1/*17": "RM", # Rapid Metabolizer
        "*17/*17": "URM" # Ultra-rapid Metabolizer
    },
    "CYP2C9": {
        "*1/*1": "NM",
        "*1/*2": "IM",
        "*2/*1": "IM",
        "*1/*3": "IM",
        "*2/*3": "PM",
        "*3/*3": "PM"
    },
    "SLCO1B1": {
        "*1/*1": "NM",
        "*1/*5": "IM",
        "*5/*1": "IM",
        "*5/*5": "PM"
    }
}

def get_phenotype(gene: str, diplotype: str) -> str:
    """
    Translates a diplotype into a clinical phenotype code (NM, IM, PM, etc.).
    """
    gene_map = PHENOTYPE_MAP.get(gene, {})
    # Return mapping if found, otherwise default to Unknown
    return gene_map.get(diplotype, "Unknown")