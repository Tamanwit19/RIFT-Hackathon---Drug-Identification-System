from app.services.drug_mapper import SUPPORTED_GENES

def parse_vcf(content: str):
    variants = []
    lines = content.splitlines()

    for line in lines:
        if line.startswith("#"):
            continue

        columns = line.split("\t")
        if len(columns) < 8:
            continue

        rsid = columns[2]
        info_field = columns[7]
        info_parts = info_field.split(";")

        gene = None
        star = None

        for part in info_parts:
            if "=" in part:
                key, value = part.split("=", 1)
                if key == "GENE":
                    gene = value
                if key == "STAR":
                    star = value

        # CRITICAL CHANGE: Only keep variant if it belongs to our 6 target genes
        if gene in SUPPORTED_GENES and star:
            variants.append({
                "rsid": rsid,
                "gene": gene,
                "star_allele": star
            })

    return variants