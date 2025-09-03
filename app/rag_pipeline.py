import warnings
warnings.filterwarnings("ignore")

from langchain.vectorstores import Chroma
from langchain.embeddings import OllamaEmbeddings
from langchain.llms import Ollama
from langchain.prompts import PromptTemplate
from prompts import SINGLE_DOC_PROMPT, SYNTHESIS_PROMPT_TEMPLATE
INDEX_DIR = "data/rag_gwas_index"

embedding = OllamaEmbeddings(model="nomic-embed-text")
vectorstore = Chroma(persist_directory=INDEX_DIR, embedding_function=embedding)
retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
llm = Ollama(model="mistral:instruct")

def retrieve_docs(question, k=5):
    return retriever.get_relevant_documents(question)

def ask_doc(doc, question):
    prompt_text = SINGLE_DOC_PROMPT.format(context=doc.page_content, question=question)
    return llm.invoke(prompt_text).strip()

def analyze_all_docs(docs, question):
    answers = []
    for i, doc in enumerate(docs):
        answer = ask_doc(doc, question)
        pmid = doc.metadata.get("pmid", f"doc_{i+1}")
        answers.append((pmid, answer))
    return answers

def summarize_answers(question, answers):
    all_text = "\n\n".join(f"PMID {pmid}:\n{answer}" for pmid, answer in answers)
    return llm.invoke(SYNTHESIS_PROMPT_TEMPLATE).strip()

def full_pipeline(question):
    docs = retrieve_docs(question)
    answers = analyze_all_docs(docs, question)
    synthesis = summarize_answers(question, answers)
    return synthesis, docs
