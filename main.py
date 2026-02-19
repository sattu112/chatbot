import streamlit as st
from file_utils import extract_text
from sentence_transformers import SentenceTransformer
from transformers import pipeline
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import os
import tiktoken

st.set_page_config(page_title="The QA Bot", layout='wide')

# Custom CSS for chat-style UI
st.markdown("""
<style>
body {
    background-color: #0e1117;
    color: #fafafa;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.stButton>button {
    background: linear-gradient(135deg, #1f6feb, #0969da);
    color: white;
    height: 45px;
    border-radius: 8px;
    border: none;
    font-size: 16px;
    font-weight: bold;
    transition: all 0.3s ease;
}

.stButton>button:hover {
    background: linear-gradient(135deg, #0969da, #0550ae);
    transform: translateY(-2px);
}

.stTextInput>div>input {
    background-color: #21262d;
    border-radius: 8px;
    border: 1px solid #30363d;
    color: #fafafa;
    padding: 12px;
    font-size: 16px;
}

.upload-section {
    background: #161b22;
    border-radius: 12px;
    padding: 20px;
    border: 2px dashed #30363d;
    margin: 20px 0;
}
</style>
""", unsafe_allow_html=True)

st.title("🤖 The Q&A Chatbot")

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "document_loaded" not in st.session_state:
    st.session_state.document_loaded = False

if "chunks" not in st.session_state:
    st.session_state.chunks = []

if "chunk_embeddings" not in st.session_state:
    st.session_state.chunk_embeddings = []

# Load models (cached)
@st.cache_resource
def load_models():
    qa_pipeline = pipeline(
        "text2text-generation",
        model="google/flan-t5-xl",
        tokenizer="google/flan-t5-xl",
    )
    sentence_embedder = SentenceTransformer('all-MiniLM-L6-v2')
    return qa_pipeline, sentence_embedder

qa_pipeline, sentence_embedder = load_models()

# File upload section
st.markdown('<div class="upload-section">', unsafe_allow_html=True)
st.subheader("📄 Upload Your Document")
uploaded_file = st.file_uploader(
    "Choose any readable file", 
    type=["pdf","png","jpg","jpeg","xls","xlsx","doc","docx","ppt","pptx","txt","csv"],
    help="Supports PDF, images, Excel, Word, PowerPoint, and text files"
)
st.markdown('</div>', unsafe_allow_html=True)

if uploaded_file and not st.session_state.document_loaded:
    with st.spinner("🔄 Processing document..."):
        file_name = uploaded_file.name
        with open(file_name, "wb") as f:
            f.write(uploaded_file.getbuffer())

        text = extract_text(file_name)
        
        if not text or text.strip() == "":
            st.error("❌ No text could be extracted from the file. Please try another.")
        else:
            st.success(f"✅ Successfully processed: {file_name}")
            
            # Show extracted text preview
            with st.expander("📖 View Extracted Text", expanded=False):
                st.text_area("Extracted content:", value=text[:2000] + "..." if len(text) > 2000 else text, height=200)

            # Process and chunk the text
            paragraphs = [p for p in text.split("\n") if p.strip()]
            full_text = " ".join(paragraphs)

            # Tokenize and chunk
            enc = tiktoken.get_encoding("gpt2")
            tokens = enc.encode(full_text)
            max_tokens = 400
            stride = 50

            chunks = []
            for i in range(0, len(tokens), max_tokens - stride):
                chunk = tokens[i : i + max_tokens]
                text_chunk = enc.decode(chunk)
                chunks.append(text_chunk)

            # Cache chunks and embeddings
            st.session_state.chunks = chunks
            st.session_state.chunk_embeddings = sentence_embedder.encode(chunks)
            st.session_state.document_loaded = True

        # Clean up
        try:
            os.remove(file_name)
        except Exception:
            pass

# Chat interface
if st.session_state.document_loaded:
    st.markdown("---")
    st.subheader("💬 Ask Questions About Your Document")
    
    # Question input
    col1, col2 = st.columns([4, 1])
    with col1:
        question = st.text_input("Enter your question here:", placeholder="What is this document about?")
    with col2:
        ask_button = st.button("Ask", type="primary")
    
    # Process question
    if (question and ask_button) or (question and st.session_state.get("last_question") != question):
        st.session_state.last_question = question
        
        with st.spinner("🤔 Thinking..."):
            # Find most relevant chunk
            q_embedding = sentence_embedder.encode([question])
            sims = cosine_similarity(q_embedding, st.session_state.chunk_embeddings)[0]
            best_idx = int(np.argmax(sims))
            best_context = st.session_state.chunks[best_idx]

            # Generate answer
            prompt = (
                f"Answer the question based on the context below:\n"
                f"Context: {best_context}\n"
                f"Question: {question}\n"
                f"Answer:"
            )
            
            try:
                result = qa_pipeline(prompt, max_length=256, num_beams=5, do_sample=False)
                answer = result[0]['generated_text']
                
                # Add to chat history
                st.session_state.chat_history.append({
                    "user": question,
                    "bot": answer
                })
                
            except Exception as e:
                st.error(f"❌ Error generating answer: {str(e)}")

    # Display chat history using Streamlit's native chat components
    if st.session_state.chat_history:
        st.markdown("---")
        st.subheader("💭 Conversation History")
        
        for exchange in st.session_state.chat_history:
            # User message
            with st.chat_message("user"):
                st.write(exchange["user"])
            
            # Bot message
            with st.chat_message("assistant"):
                st.write(exchange["bot"])
        
        # Clear history button
        if st.button("🗑️ Clear Chat History"):
            st.session_state.chat_history = []
            st.rerun()

else:
    st.info("👆 Please upload a document to start asking questions!")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #8b949e; font-size: 14px; margin-top: 20px;'>
       ADHI'S BOT
    </div>
    """, 
    unsafe_allow_html=True
)
