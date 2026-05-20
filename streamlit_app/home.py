"""
Chat page for the Streamlit application.
"""

import uuid
import streamlit as st
from utils.api_client import query_backend, document_upload_rag

# Configure page settings
st.set_page_config(
    page_title="Adaptive RAG",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get help": None,
        "Report a bug": None,
        "About": None
    }
)

# Auto-generate session ID once per browser session
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=IBM+Plex+Mono:wght@400;500&family=DM+Sans:wght@300;400;500;600&display=swap');

/* ── Reset & base ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    color: #0f1f3d;
}

/* ── App background ── */
.stApp {
    background-color: #ffffff;
    background-image:
        linear-gradient(rgba(15,31,61,0.04) 1px, transparent 1px),
        linear-gradient(90deg, rgba(15,31,61,0.04) 1px, transparent 1px);
    background-size: 40px 40px;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: #f7f6f3;
    border-right: 2px solid #0f1f3d;
}
[data-testid="stSidebar"] * {
    color: #0f1f3d !important;
}

/* Sidebar brand */
.sidebar-brand {
    font-family: 'DM Serif Display', serif;
    font-size: 1.25rem;
    color: #0f1f3d !important;
    letter-spacing: 0.01em;
    margin-bottom: 0.3rem;
    padding-bottom: 1rem;
    border-bottom: 2px solid #0f1f3d;
}
.sidebar-tagline {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.62rem;
    color: #e0341a !important;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    margin-bottom: 1.5rem;
    display: block;
}

/* Sidebar caption */
.stSidebar .stCaption {
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.65rem !important;
    color: #6b7a99 !important;
    letter-spacing: 0.06em;
}

/* ── File uploader ── */
[data-testid="stFileUploader"] {
    background: #ffffff !important;
    border: 1.5px dashed #0f1f3d !important;
    border-radius: 4px !important;
    transition: border-color 0.2s ease;
}
[data-testid="stFileUploader"]:hover {
    border-color: #e0341a !important;
    border-style: solid !important;
}
[data-testid="stFileUploader"] * {
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.75rem !important;
}

/* ── Alerts ── */
[data-testid="stAlert"] {
    border-radius: 3px !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.72rem !important;
    border-left-width: 3px !important;
}

/* ── Page title area ── */
.rag-eyebrow {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.65rem;
    color: #e0341a;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    margin-bottom: 0.4rem;
}
.rag-title {
    font-family: 'DM Serif Display', serif;
    font-size: 3rem;
    color: #0f1f3d;
    line-height: 1.05;
    margin-bottom: 0.5rem;
    letter-spacing: -0.01em;
}
.rag-rule {
    width: 48px;
    height: 3px;
    background: #e0341a;
    margin-bottom: 1rem;
    border: none;
}
.rag-subtitle {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.9rem;
    color: #4a5568;
    font-weight: 300;
    margin-bottom: 2rem;
    max-width: 520px;
    line-height: 1.6;
}

/* ── Chat messages ── */
[data-testid="stChatMessage"] {
    background: #ffffff !important;
    border: 1.5px solid #e2e8f0 !important;
    border-radius: 4px !important;
    margin-bottom: 0.65rem !important;
    padding: 0.9rem 1.1rem !important;
    box-shadow: 0 1px 4px rgba(15,31,61,0.05) !important;
    font-family: 'DM Sans', sans-serif !important;
}
/* User message — navy left border */
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {
    border-left: 3px solid #0f1f3d !important;
    background: #f7f9ff !important;
}
/* Assistant message — coral left border */
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) {
    border-left: 3px solid #e0341a !important;
    background: #fff9f7 !important;
}

/* Message text */
[data-testid="stChatMessage"] p {
    color: #0f1f3d !important;
    font-size: 0.9rem !important;
    line-height: 1.65 !important;
}

/* ── Chat input ── */
[data-testid="stChatInput"] {
    border-top: 2px solid #0f1f3d !important;
    background: #ffffff !important;
    padding-top: 0.5rem;
}
[data-testid="stChatInput"] textarea {
    background: #ffffff !important;
    border: 1.5px solid #c8d0e0 !important;
    border-radius: 4px !important;
    color: #0f1f3d !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.88rem !important;
}
[data-testid="stChatInput"] textarea:focus {
    border-color: #0f1f3d !important;
    box-shadow: 0 0 0 2px rgba(15,31,61,0.1) !important;
}
[data-testid="stChatInput"] textarea::placeholder {
    color: #9aa5b8 !important;
    font-style: italic;
}

/* ── Empty state ── */
.empty-state {
    text-align: center;
    padding: 5rem 2rem 3rem;
}
.empty-icon {
    font-size: 2.5rem;
    margin-bottom: 1rem;
    opacity: 0.25;
}
.empty-text {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.72rem;
    color: #9aa5b8;
    letter-spacing: 0.1em;
    text-transform: uppercase;
}

/* ── Indexed docs list ── */
.doc-item {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.68rem;
    color: #4a5568;
    padding: 0.35rem 0;
    border-bottom: 1px solid #e2e8f0;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
.doc-section-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.6rem;
    color: #e0341a;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    margin: 1.2rem 0 0.5rem;
    display: block;
}

/* ── Spinner ── */
[data-testid="stSpinner"] * {
    color: #0f1f3d !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.75rem !important;
}

/* scrollbar */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: #f7f6f3; }
::-webkit-scrollbar-thumb { background: #c8d0e0; border-radius: 2px; }
::-webkit-scrollbar-thumb:hover { background: #0f1f3d; }
</style>
""", unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
        <div class="sidebar-brand">Adaptive RAG</div>
        <span class="sidebar-tagline">Knowledge Base</span>
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Upload document",
        type=["pdf", "txt"],
        label_visibility="collapsed"
    )
    st.caption("PDF or TXT · Max 200MB")

    if uploaded_file:
        if "uploaded_files" not in st.session_state:
            st.session_state.uploaded_files = {}

        file_key = uploaded_file.name

        if file_key not in st.session_state.uploaded_files:
            with st.spinner("Indexing document..."):
                success = document_upload_rag(uploaded_file)
            if success:
                st.success(f"✓ Indexed: {uploaded_file.name}")
                st.session_state.uploaded_files[file_key] = True
            else:
                st.error(f"✗ Failed: {uploaded_file.name}")
        else:
            st.info(f"Already indexed: {uploaded_file.name}")

    # Indexed files list
    if st.session_state.get("uploaded_files"):
        st.markdown('<span class="doc-section-label">— Indexed documents</span>', unsafe_allow_html=True)
        for name in st.session_state.uploaded_files:
            st.markdown(f'<div class="doc-item">↳ {name}</div>', unsafe_allow_html=True)

# ── Main area ─────────────────────────────────────────────────────────────────
st.markdown("""
    <div class="rag-eyebrow">Retrieval-Augmented Generation</div>
    <div class="rag-title">Ask your documents.</div>
    <div class="rag-rule"></div>
    <div class="rag-subtitle">Upload a PDF or TXT file to the knowledge base, then ask questions. The system retrieves relevant context and generates precise answers.</div>
""", unsafe_allow_html=True)

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Empty state
if not st.session_state.chat_history:
    st.markdown("""
    <div class="empty-state">
        <div class="empty-icon">◎</div>
        <div class="empty-text">No conversation yet — upload a document and ask a question</div>
    </div>
    """, unsafe_allow_html=True)

# Display chat history
for role, text in st.session_state.chat_history:
    st.chat_message(role).write(text)

# User input
user_input = st.chat_input("Ask a question about your documents...")

# Process user input and get response
if user_input:
    st.session_state.chat_history.append(("user", user_input))
    with st.spinner("Searching knowledge base..."):
        response = query_backend(user_input, st.session_state.session_id)
    st.session_state.chat_history.append(("assistant", response))
    st.rerun()