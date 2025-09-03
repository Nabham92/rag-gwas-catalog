import time
import json
import pandas as pd
from Bio import Entrez
import os

# --- Config ---
INPUT_FILE = "data/gwas_filtered.csv"
OUTPUT_FILE = "data/pubmed_abstracts_top1000.json"
Entrez.email = "" 
Entrez.api_key = ""  # Optionnal

# --- Step 1: Extract top PMIDs from CSV ---
def get_top_pmids(csv_path, top_n=1000):
    df = pd.read_csv(csv_path)
    df = df.dropna(subset=["PUBMEDID"])
    top_pmids = (
        df["PUBMEDID"]
        .astype(int)
        .value_counts()
        .head(top_n)
        .index
        .tolist()
    )
    return top_pmids

# --- Step 2: Fetch abstract from PubMed ---
def fetch_abstract(pmid):
    try:
        handle = Entrez.efetch(db="pubmed", id=str(pmid), rettype="abstract", retmode="text")
        abstract = handle.read().strip()
        return abstract if abstract else None
    except Exception as e:
        print(f"❌ Failed to fetch PMID {pmid}: {e}")
        return None

# --- Step 3: Download and save abstracts ---
def download_abstracts(pmids, output_path):
    abstracts = {}
    for i, pmid in enumerate(pmids):
        print(f"🔄 Fetching PMID {pmid} ({i+1}/{len(pmids)})")
        abs_text = fetch_abstract(pmid)
        if abs_text:
            abstracts[str(pmid)] = abs_text
        time.sleep(0.1)  # Respect NCBI usage policy

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(abstracts, f, indent=2)

    print(f"\n✅ {len(abstracts)} abstracts saved to {output_path}")

# --- Main ---
if __name__ == "__main__":
    print("📥 Extracting top PMIDs from GWAS data...")
    top_pmids = get_top_pmids(INPUT_FILE, top_n=1000)
    print(f"✅ {len(top_pmids)} PMIDs selected.")

    print("🚀 Downloading abstracts...")
    download_abstracts(top_pmids, OUTPUT_FILE)
