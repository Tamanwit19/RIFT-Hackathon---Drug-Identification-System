def resolve_diplotype(variants: list):
    """
    Translates detected star alleles into a clinical diplotype (*X/*Y).
    - If 0 variants: Assume wild-type/normal or Unknown.
    - If 1 variant: Assume Heterozygous (*1/Variant).
    - If 2 variants: Assume Compound Heterozygous or Homozygous (Variant/Variant).
    """
    if not variants:
        # In a real clinical setting, this might be *1/*1 (Normal)
        # For this hackathon, we'll mark as Unknown/Normal
        return "*1/*1" 

    # Extract the star_allele strings (e.g., ["*2", "*3"])
    stars = [v["star_allele"] for v in variants]

    if len(stars) == 1:
        # One variant found: Patient has one normal copy and one variant
        return f"*1/{stars[0]}"
    
    if len(stars) == 2:
        # Two variants found: Patient has two variant copies
        return f"{stars[0]}/{stars[1]}"
    
    # Fallback for complex cases (more than 2)
    return "/".join(stars)