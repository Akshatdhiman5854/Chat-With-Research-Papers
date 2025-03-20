from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

embedding_model = OllamaEmbeddings(model="llama3.2")

vector_db = None

def store_text_chunks(text):
    """Splits text into optimized chunks and stores embeddings in FAISS."""
    global vector_db
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)  # Improved chunking
    text_chunks = text_splitter.split_text(text)
    
    documents = [Document(page_content=chunk) for chunk in text_chunks]
    vector_db = FAISS.from_documents(documents, embedding_model)

def retrieve_relevant_text(query):
    """Retrieves top 5 most relevant text chunks from FAISS, prioritizing the abstract if possible."""
    if vector_db is None:
        return "No document uploaded yet."

    results = vector_db.similarity_search(query, k=5)  # Increased from k=3 to k=5 for better context
    retrieved_text = "\n\n".join([doc.page_content for doc in results])

    # If abstract is found in the paper, prioritize it
    if "abstract" in retrieved_text.lower():
        abstract_index = retrieved_text.lower().find("abstract")
        retrieved_text = retrieved_text[abstract_index:]

    return retrieved_text
