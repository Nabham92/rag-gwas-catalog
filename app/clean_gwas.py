import pandas as pd
import re
import os

RAW_FILE = "data/gwas_catalog_v1.0-associations_e114_r2025-07-21.tsv"
CLEAN_FILE = "data/gwas_clean.csv"
PVAL_THRESHOLD = 5e-8


def load_and_clean_data(file_path: str, pval_threshold: float) -> pd.DataFrame:
    df = pd.read_csv(file_path, sep="\t")

    # Filter invalid or missing values
    df = df.dropna(subset=["SNPS", "MAPPED_GENE", "DISEASE/TRAIT", "P-VALUE"])
    df = df[~df["SNPS"].isin(["NR", ""])]

    # Clean fields
    df["SNPS"] = df["SNPS"].str.strip().str.upper()
    df["DISEASE/TRAIT"] = df["DISEASE/TRAIT"].str.strip()
    df["MAPPED_GENE"] = df["MAPPED_GENE"].str.upper().str.strip()
    df["MAPPED_GENE"] = df["MAPPED_GENE"].apply(lambda x: re.sub(r"[^A-Z0-9,\-\s|;/]", "", x))

    # Normalize separators
    df["GENE"] = df["MAPPED_GENE"].str.replace(r"\s*(,|;|/|\||\s-\s|\sAND\s|\s{2,})\s*", "|", regex=True)
    df["GENE"] = df["GENE"].str.split("|")
    df = df.explode("GENE")
    df["GENE"] = df["GENE"].str.strip().str.upper()
    df = df[df["GENE"] != ""]

    # Threshold filter
    df = df[df["P-VALUE"].astype(float) < pval_threshold]

    # Drop duplicates
    df = df.drop_duplicates(subset=["SNPS", "GENE", "DISEASE/TRAIT", "P-VALUE"])

    return df


def save_clean_data(df: pd.DataFrame, path: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.to_csv(path, index=False)
    print(f"✅ Cleaned data saved with {len(df)} rows to: {path}")


if __name__ == "__main__":
    df = load_and_clean_data(RAW_FILE, PVAL_THRESHOLD)
    save_clean_data(df, CLEAN_FILE)
