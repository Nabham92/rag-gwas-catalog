import os

# --- Base directory ---
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# --- Data paths ---
DATA_DIR = os.path.join(BASE_DIR, "data")
RAW_DIR = os.path.join(DATA_DIR, "raw")
PROCESSED_DIR = os.path.join(DATA_DIR, "processed")

# --- Files ---
RAW_GWAS_FILE = os.path.join(RAW_DIR, "gwas_raw.csv")
ABSTRACTS_JSON = os.path.join(RAW_DIR, "pubmed_abstracts_top1000.json")
FILTERED_DATA_FILE = os.path.join(PROCESSED_DIR, "gwas_filtered.csv")

# --- Chroma index directory ---
INDEX_DIR = os.path.join(DATA_DIR, "rag_gwas_index")

# --- Embedding model name ---
EMBEDDING_MODEL = "nomic-embed-text"

# --- Ollama LLM model name ---
LLM_MODEL = "mistral:instruct"
