import streamlit as st
from pdf_util import extract_text_from_pdf
from vector_store import store_text_chunks
from llm_util import generate_response

st.set_page_config(page_title="Chat with Research Papers", layout="centered")

st.markdown(
    """
    <style>
    body {
        background-color: #212121;
        font-family: Arial, sans-serif;
        color: white;
    }
    .container {
        max-width: 700px;
        margin: auto;
        padding-top: 20px;
    }
    .chat-container {
        display: flex;
        flex-direction: column;
        gap: 10px;
        max-width: 700px;
        margin: auto;
    }
    .user-message {
        align-self: flex-end;
        background-color: #343541;
        color: white;
        padding: 12px 16px;
        border-radius: 16px;
        border-top-right-radius: 4px;
        max-width: fit-content;
        text-align: right;
        margin-left: auto;
    }
    .ai-message {
        align-self: flex-start;
        text-align: left;
        max-width: 90%;
    }
    @media (max-width: 600px) {
        .container, .chat-container {
            max-width: 95%;
        }
    }
</style>
    """,
    unsafe_allow_html=True
)

st.markdown('<div class="container">', unsafe_allow_html=True)
st.title("Chat with Research Papers")

uploaded_file = st.file_uploader("Upload a Research Paper (PDF)", type="pdf")

if uploaded_file:
    pdf_text = extract_text_from_pdf(uploaded_file)
    store_text_chunks(pdf_text)
    st.success("PDF Uploaded and Processed!")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for role, text in st.session_state.chat_history:
    role_class = "user-message" if role == "User" else "ai-message"
    st.markdown(f'<div class="message {role_class}">{text}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

user_query = st.chat_input("Ask me anything about the research paper...")

if user_query:
    st.session_state.chat_history.append(("User", user_query))
    st.markdown(f'<div class="message user-message">{user_query}</div>', unsafe_allow_html=True)

    with st.spinner("Thinking..."):
        response = generate_response(user_query)

    st.markdown(f'<div class="message ai-message">{response}</div>', unsafe_allow_html=True)
    st.session_state.chat_history.append(("AI", response))

st.markdown('</div>', unsafe_allow_html=True)
