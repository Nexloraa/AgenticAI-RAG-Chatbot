import sys
import os
# Add project root to sys.path BEFORE any imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import streamlit as st
import requests
from src.front_src.config.frontend_settings import Settings

settings = Settings()

st.set_page_config(
    page_title="StudyBuddy",
    page_icon="🤖",
    layout="centered",
)

# ---------------------- SIDEBAR ---------------------- #
with st.sidebar:
    st.title("📚 StudyBuddy")
    st.markdown(
        """
        <div style="
            font-size: 20px;
            font-weight: 700;
            color: #00E5FF;
            background: linear-gradient(90deg, #0f172a, #1e3a8a);
            padding: 10px 16px;
            border-radius: 10px;
            text-align: center;
            margin-top: -10px;
            margin-bottom: 15px;
            letter-spacing: 1px;
            box-shadow: 0 0 15px rgba(0,255,255,0.25);
        ">
            Agentic RAG Chatbot  🚀
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("### 💡 Quick Prompts")
    preset_qs = [
        "Explain reproduction in simple terms.",
        "Summarize evolution in 5 bullet points.",
        "Difference between mitosis and meiosis.",
        "Important points from ecosystem chapter.",
    ]
    for q in preset_qs:
        if st.button(q, use_container_width=True):
            st.session_state._preset_clicked = q

    st.markdown("---")
    if st.button("🧹 Clear Chat", use_container_width=True):
        st.session_state.chat_history = []
        st.experimental_rerun()

    st.markdown("---")
    st.markdown("### Backend URL")
    st.code(settings.CHAT_ENDPOINT_URL, language="bash")

# ---------------------- MAIN UI ---------------------- #
st.title("💬 StudyBuddy - Chat with your Notes")
st.caption("Ask questions from the syllabus ")

# ---------------------- CHAT HISTORY ---------------------- #
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

preset_prefill = st.session_state.pop("_preset_clicked", None) if "_preset_clicked" in st.session_state else None

for message in st.session_state.chat_history:
    role = message["role"]
    sources = message.get("sources", [])
    tool_used = message.get("tool_used")
    rationale = message.get("rationale")

    with st.chat_message(role):
        st.write(message["content"])
        if sources:
            st.markdown(f"**Sources:** {', '.join(sources)}")
        if tool_used or rationale:
            with st.expander("🔍 Details"):
                st.markdown(f"**Tool:** {tool_used}")
                st.markdown(f"**Rationale:** {rationale}")

# ---------------------- INPUT BOX ---------------------- #
user_prompt = st.chat_input(
    placeholder="Ask something like: Explain ecosystem in simple words…",
    key="chat_input",
)

if preset_prefill and not user_prompt:
    user_prompt = preset_prefill

# ---------------------- SEND MESSAGE ---------------------- #
if user_prompt:
    with st.chat_message("user"):
        st.write(user_prompt)

    st.session_state.chat_history.append({"role": "user", "content": user_prompt})

    payload = {"chat_history": st.session_state.chat_history}

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = requests.post(settings.CHAT_ENDPOINT_URL, json=payload, timeout=60)
                response.raise_for_status()
                data = response.json()

                answer = data.get("answer", "")
                sources = data.get("sources", data.get("source_files", []))
                tool_used = data.get("tool_used", "RAG")
                rationale = data.get("rationale", "")

            except Exception as e:
                answer = f"❌ Backend error: {e}"
                sources, tool_used, rationale = [], None, None

        st.write(answer)
        if sources:
            st.markdown(f"**Sources:** {', '.join(sources)}")
        if tool_used or rationale:
            with st.expander("🔍 Details"):
                st.markdown(f"**Tool:** {tool_used}")
                st.markdown(f"**Rationale:** {rationale}")

        st.session_state.chat_history.append({
            "role": "assistant",
            "content": answer,
            "sources": sources,
            "tool_used": tool_used,
            "rationale": rationale
        })
