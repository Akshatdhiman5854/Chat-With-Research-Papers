from langchain_ollama import OllamaLLM
from vector_store import retrieve_relevant_text

llm = OllamaLLM(model="llama3.2")

def generate_response(query):
    """Generates a response using Llama 3.2 based on retrieved context from the research paper."""
    context = retrieve_relevant_text(query)

    prompt = f"""
    You are an AI assistant that helps users understand research papers.
    Answer the user's question as clearly and directly as possible using the context below.

    Context: 
    {context}

    User Question: {query}

    If the context does not contain enough information, provide an answer based on general knowledge of research papers.

    Answer:
    """

    response_text = ""
    for chunk in llm.stream(prompt):  # Streams response in real-time
        response_text += chunk

    return response_text
