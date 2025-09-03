import os
import warnings
import pandas as pd

from langchain.schema import Document
from langchain.embeddings import OllamaEmbeddings
from langchain.vectorstores import Chroma

import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from build_docs import create_documents_from_raw_data
from config import FILTERED_DATA_FILE, INDEX_DIR, EMBEDDING_MODEL


# --- Suppress warnings ---
warnings.filterwarnings("ignore")

# --- Load CSV ---
def load_filtered_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    return df


# --- Build Vectorstore Index ---
def build_index(docs: list, index_dir: str) -> None:
    print(" Initializing embedding model...")
    embedding = OllamaEmbeddings(model=EMBEDDING_MODEL)

    print(f"💾 Building Chroma index in: {index_dir}")
    vectorstore = Chroma.from_documents(
        documents=docs,
        embedding=embedding,
        persist_directory=index_dir
    )

    vectorstore.persist()
    print(" Index built and persisted.")

# --- Main ---
if __name__ == "__main__":
    print(" Loading data...")
    df = load_filtered_data(FILTERED_DATA_FILE)
    print(f" Loaded {len(df)} rows.")


    print(" Creating documents...")
    documents = create_documents_from_raw_data(
    assoc_csv_path="data/processed/gwas_filtered.csv",
    abstracts_json_path="data/raw/pubmed_abstracts_top1000.json"
)

    print(f" Created {len(documents)} documents.")

    build_index(documents, index_dir=INDEX_DIR)
