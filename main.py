import warnings 
warnings.filterwarnings("ignore")
import sys
import os
sys.path.append(os.path.abspath("app"))

from rag_pipeline import full_pipeline

if __name__ == "__main__":
    question = input("💬 Ask a question: ")
    answer, docs = full_pipeline(question)

    print("\n🧠 Synthesized Answer:\n")
    print(answer)

    print("\n📚 Sources:")
    for doc in docs:
        print("-", doc.metadata.get("source", "no source"))
