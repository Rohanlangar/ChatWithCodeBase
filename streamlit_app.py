import streamlit as st
import os
from clonerepo import clone_repository
from index import vectorStore
from chat import chat_with_repo
import tempfile

# Page config
st.set_page_config(
    page_title="Repository Chat Assistant",
    page_icon="🔗",
    layout="wide"
)

# Title and description
st.title("🔗 Repository Chat Assistant")
st.markdown("Clone a GitHub repository and chat with its codebase using AI")

# Initialize session state
if 'repo_cloned' not in st.session_state:
    st.session_state.repo_cloned = False
if 'vector_store_ready' not in st.session_state:
    st.session_state.vector_store_ready = False
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Sidebar for repository setup
with st.sidebar:
    st.header("📁 Repository Setup")
    
    repo_url = st.text_input(
        "GitHub Repository URL",
        placeholder="https://github.com/user/repo",
        help="Enter the full GitHub repository URL"
    )
    
    if st.button("🚀 Clone & Process Repository", type="primary"):
        if repo_url:
            with st.spinner("Cloning repository..."):
                try:
                    path = clone_repository(repo_url)
                    st.session_state.repo_cloned = True
                    st.success("✅ Repository cloned successfully!")
                except Exception as e:
                    st.error(f"❌ Error cloning repository: {str(e)}")
                    st.session_state.repo_cloned = False
            
            if st.session_state.repo_cloned:
                with st.spinner("Creating vector embeddings..."):
                    try:
                        vectorStore(path)
                        st.session_state.vector_store_ready = True
                        st.success("✅ Vector store created successfully!")
                    except Exception as e:
                        st.error(f"❌ Error creating vector store: {str(e)}")
                        st.session_state.vector_store_ready = False
        else:
            st.warning("⚠️ Please enter a repository URL")
    
    # Status indicators
    st.markdown("---")
    st.subheader("📊 Status")
    
    if st.session_state.repo_cloned:
        st.success("✅ Repository cloned")
    else:
        st.info("⏳ Repository not cloned")
    
    if st.session_state.vector_store_ready:
        st.success("✅ Vector store ready")
    else:
        st.info("⏳ Vector store not ready")

# Main chat interface
if st.session_state.vector_store_ready:
    st.header("💬 Chat with Repository")
    
    # Display chat history
    for i, (question, answer) in enumerate(st.session_state.chat_history):
        with st.container():
            st.markdown(f"**🧠 Question {i+1}:** {question}")
            st.markdown(f"**📘 Answer:** {answer}")
            st.markdown("---")
    
    # Chat input
    with st.form("chat_form", clear_on_submit=True):
        user_question = st.text_input(
            "Ask a question about the repository:",
            placeholder="What does this code do? How is authentication handled?",
            key="user_input"
        )
        
        col1, col2 = st.columns([1, 4])
        with col1:
            submit_button = st.form_submit_button("🚀 Ask", type="primary")
        with col2:
            if st.form_submit_button("🗑️ Clear History"):
                st.session_state.chat_history = []
                st.rerun()
    
    if submit_button and user_question:
        with st.spinner("🤔 Thinking..."):
            try:
                # Import the necessary components for direct QA
                from langchain_huggingface import HuggingFaceEmbeddings
                from langchain_pinecone import PineconeVectorStore
                from langchain_groq import ChatGroq
                from langchain.chains import RetrievalQA
                
                # Set up the QA chain (same as in chat.py)
                embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
                vectorstore = PineconeVectorStore.from_existing_index(index_name="code-base", embedding=embeddings)
                retriever = vectorstore.as_retriever(search_kwargs={"k": 4})
                
                llm = ChatGroq(
                    model="openai/gpt-oss-20b",  
                    temperature=0.7
                )
                
                qa = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)
                response = qa.run(user_question)
                
                # Add to chat history
                st.session_state.chat_history.append((user_question, response))
                st.rerun()
                
            except Exception as e:
                st.error(f"❌ Error processing question: {str(e)}")

else:
    st.info("👆 Please clone and process a repository first using the sidebar")
    
    # Show example
    st.markdown("### 🎯 How it works:")
    st.markdown("""
    1. **Enter a GitHub repository URL** in the sidebar
    2. **Click 'Clone & Process Repository'** to download and analyze the code
    3. **Ask questions** about the codebase once processing is complete
    
    **Example questions you can ask:**
    - "What is the main functionality of this application?"
    - "How is authentication implemented?"
    - "What are the key components and their responsibilities?"
    - "How does the database schema work?"
    """)

# Footer
st.markdown("---")
st.markdown("Built with ❤️ using Streamlit, LangChain, and Groq")