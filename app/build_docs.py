import json
import pandas as pd
from langchain.schema import Document


def create_documents_from_raw_data(assoc_csv_path: str, abstracts_json_path: str) -> list[Document]:
    # --- Load abstracts ---
    with open(abstracts_json_path) as f:
        pmid_abstracts = json.load(f)

    # --- Load and filter associations ---
    df = pd.read_csv(assoc_csv_path)
    df = df.dropna(subset=["PUBMEDID"])
    df["PUBMEDID"] = df["PUBMEDID"].astype(int).astype(str)
    df = df[df["PUBMEDID"].isin(pmid_abstracts.keys())]

    # --- Group by study ---
    grouped = df.groupby("PUBMEDID")
    docs = []

    for pmid, group in grouped:
        abstract = pmid_abstracts.get(pmid)
        if not abstract:
            continue

        # Extract fields
        genes = sorted(set(group["GENE"].dropna()))
        mapped_genes = sorted(set(group["MAPPED_GENE"].dropna()))
        traits = sorted(set(group["DISEASE/TRAIT"].dropna()))
        snps = sorted(set(group["SNPS"].dropna()))
        chromosomes = sorted(set(map(str, group["CHR_ID"].dropna())))
        positions = sorted(set(map(str, group["CHR_POS"].dropna())))
        pvals = sorted(set(map(str, group["P-VALUE"].dropna())))
        effects = sorted(set(map(str, group["OR or BETA"].dropna())))
        ancestries = sorted(set(group["INITIAL SAMPLE SIZE"].dropna()))
        authors = sorted(set(group["FIRST AUTHOR"].dropna()))
        journals = sorted(set(group["JOURNAL"].dropna()))
        dates = sorted(set(group["DATE"].dropna()))

        # --- Build content ---
        content = (
            f"Study PMID {pmid} reports genetic associations from a GWAS.\n\n"
            f"- SNPs: {', '.join(snps)}\n"
            f"- Chromosomes: {', '.join(chromosomes)}\n"
            f"- Positions: {', '.join(positions)}\n"
            f"- Genes (Reported): {', '.join(genes)}\n"
            f"- Genes (Mapped): {', '.join(mapped_genes)}\n"
            f"- Traits: {', '.join(traits)}\n"
            f"- P-values: {', '.join(pvals)}\n"
            f"- Effect sizes (OR/Beta): {', '.join(effects)}\n"
            f"- Ancestries: {', '.join(ancestries)}\n"
            f"- Authors: {', '.join(authors)}\n"
            f"- Journal(s): {', '.join(journals)}\n"
            f"- Publication dates: {', '.join(dates)}\n\n"
            f"Abstract:\n{abstract}"
        )

        metadata = {
            "pmid": pmid,
            "snps": ", ".join(snps),
            "chromosomes": ", ".join(chromosomes),
            "positions": ", ".join(positions),
            "genes_reported": ", ".join(genes),
            "genes_mapped": ", ".join(mapped_genes),
            "traits": ", ".join(traits),
            "p_values": ", ".join(pvals),
            "effect_sizes": ", ".join(effects),
            "ancestries": ", ".join(ancestries),
            "authors": ", ".join(authors),
            "journals": ", ".join(journals),
            "publication_dates": ", ".join(dates),
            "source": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"
        }

        docs.append(Document(page_content=content, metadata=metadata))

    print(f" Created {len(docs)} unique documents (one per study)")
    return docs
