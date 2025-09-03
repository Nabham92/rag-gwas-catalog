# 🧬 RAG GWAS Catalog

This project implements a Retrieval-Augmented Generation (RAG) pipeline to query the GWAS Catalog using natural language.

It combines structured GWAS data with PubMed abstracts and uses a local LLM (via Ollama) to answer scientific questions like:

> "Which genes are associated with cardiovascular diseases and expressed in the kidney?"

---

## 🚀 Features

- Cleans and preprocesses GWAS Catalog data
- Fetches abstracts from PubMed (via Biopython)
- Builds structured documents combining metadata and abstracts
- Embeds documents using `nomic-embed-text` via Ollama
- Stores embeddings in a local Chroma vectorstore
- Retrieves relevant documents for a query
- Answers questions per document
- Synthesizes a final answer
- Judges factual consistency of the synthesis

---

## 📦 Dependencies

- Python 3.9+
- [LangChain](https://github.com/langchain-ai/langchain)
- [Chroma](https://www.trychroma.com/)
- [Ollama](https://ollama.com/)
- [Biopython](https://biopython.org/)
- pandas

---

## ⚙️ Installation & Setup

```bash
git clone https://github.com/Nabham92/rag-gwas-catalog.git
cd rag-gwas-catalog

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt

# 1. Clean and preprocess GWAS data
python app/clean_gwas.py

# 2. Download top PubMed abstracts
python app/get_abstracts.py

# 3. Build documents from metadata + abstracts
python app/build_docs.py

# 4. Build the Chroma vector index
python app/build_index.py

# 5. Run the full RAG pipeline
python main.py



from app.rag_pipeline import full_pipeline

question = "Which genes are associated with cardiovascular disease and expressed in the kidney?"
synthesis, docs, judgment = full_pipeline(question)

print("SYNTHESIS:\n", synthesis)
print("JUDGE:\n", judgment)



rag-gwas-catalog/
├── app/                  # Core scripts (build_index, clean_gwas, etc.)
├── data/                 # Raw and processed data
├── notebooks/            # Optional: analysis or dev notebooks
├── main.py               # Example pipeline execution
├── requirements.txt      # Python dependencies
└── README.md             # This file
