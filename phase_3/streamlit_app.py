"""
Nextleap RAG Chatbot - Streamlit App
A conversational AI assistant for the Nextleap Product Management Fellowship.
"""
import streamlit as st
import sys
from pathlib import Path
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from api.chatbot import NextleapChatbot

# Page configuration
st.set_page_config(
    page_title="Nextleap PM Fellowship Assistant",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for premium look
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    .stChatMessage {
        background-color: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    .stChatInputContainer {
        border-top: 1px solid rgba(255, 255, 255, 0.1);
    }
    h1 {
        color: white;
        text-align: center;
        padding: 1rem 0;
    }
    .subtitle {
        color: rgba(255, 255, 255, 0.9);
        text-align: center;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize chatbot
@st.cache_resource
def initialize_chatbot():
    """Initialize the chatbot (cached to avoid reloading)."""
    vector_db_path = Path(__file__).parent.parent / 'phase_2' / 'database' / 'vector_db'
    metadata_db_path = Path(__file__).parent.parent / 'phase_2' / 'database' / 'metadata.db'
    
    return NextleapChatbot(
        vector_db_path=str(vector_db_path),
        metadata_db_path=str(metadata_db_path)
    )

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Header
st.title("🎓 Nextleap PM Fellowship Assistant")
st.markdown('<p class="subtitle">Ask me anything about the Product Management Fellowship program!</p>', unsafe_allow_html=True)

# Sidebar with info
with st.sidebar:
    st.header("About")
    st.write("""
    This AI assistant can help you with:
    - 📚 **Curriculum**: 16-week course content
    - 👨‍🏫 **Instructors**: Faculty backgrounds
    - 🛠️ **Tools**: Technologies you'll learn
    - 📅 **Schedule**: Class timings
    - ℹ️ **General Info**: Course details
    """)
    
    st.divider()
    
    st.header("Quick Questions")
    if st.button("📖 What topics are covered?", use_container_width=True):
        st.session_state.quick_query = "What topics are covered in the curriculum?"
    if st.button("👨‍🏫 Who are the instructors?", use_container_width=True):
        st.session_state.quick_query = "Who are the instructors?"
    if st.button("📅 What is the class schedule?", use_container_width=True):
        st.session_state.quick_query = "What is the class schedule?"
    if st.button("💰 How much does it cost?", use_container_width=True):
        st.session_state.quick_query = "How much does the course cost?"
    
    st.divider()
    
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# Initialize chatbot
try:
    chatbot = initialize_chatbot()
except Exception as e:
    st.error(f"⚠️ Error initializing chatbot: {e}")
    st.info("Please ensure Phase 2 databases exist in `phase_2/database/`")
    st.stop()

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Handle quick questions from sidebar
if "quick_query" in st.session_state:
    query = st.session_state.quick_query
    del st.session_state.quick_query
    
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.write(query)
    
    # Get bot response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = chatbot.answer_query(query)
                answer = response['answer']
                st.write(answer)
                
                # Add assistant message to history
                st.session_state.messages.append({"role": "assistant", "content": answer})
            except Exception as e:
                error_msg = f"Sorry, I encountered an error: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})

# Chat input
if prompt := st.chat_input("Ask me anything about the PM Fellowship..."):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)
    
    # Get bot response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = chatbot.answer_query(prompt)
                answer = response['answer']
                st.write(answer)
                
                # Add assistant message to history
                st.session_state.messages.append({"role": "assistant", "content": answer})
            except Exception as e:
                error_msg = f"Sorry, I encountered an error: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})

# Footer
st.divider()
st.markdown(
    '<p style="text-align: center; color: rgba(255,255,255,0.6); font-size: 0.9rem;">'
    'Powered by Groq LLM • Built with Streamlit'
    '</p>',
    unsafe_allow_html=True
)
