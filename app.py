import streamlit as st
from pdf_util import extract_text_from_pdf
from vector_store import store_text_chunks
from llm_util import generate_response

st.title("Chat with \"Research Papers\"")

# Store chat history in session state for multi-turn conversation
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

uploaded_file = st.file_uploader("Upload a PDF", type="pdf")

if uploaded_file:
    pdf_text = extract_text_from_pdf(uploaded_file)
    store_text_chunks(pdf_text)
    st.success("PDF Uploaded and Processed!")

    user_query = st.text_input("Ask a question about the paper:")

    if user_query:
        response = generate_response(user_query)

        # Store query & response in session state
        st.session_state.chat_history.append(("User", user_query))
        st.session_state.chat_history.append(("AI", response))

        # Display chat history
        for role, text in st.session_state.chat_history:
            st.write(f"**{role}:** {text}")
