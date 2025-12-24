import sys
sys.dont_write_bytecode = True
import streamlit as st
from chatbot import SupportChatbot

st.set_page_config(page_title="MCP Support Bot", layout="centered")

bot = SupportChatbot()

# --------------------
# Session state
# --------------------
if "history" not in st.session_state:
    st.session_state.history = []

if "processing" not in st.session_state:
    st.session_state.processing = False

if "input_counter" not in st.session_state:
    st.session_state.input_counter = 0

st.title("🖥️ Customer Support Chatbot")
st.caption("Powered by MCP + OpenRouter")

# --------------------
# Render chat history
# --------------------
for msg in st.session_state.history:
    if hasattr(st, "chat_message"):
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
    else:
        st.markdown(f"**{msg['role'].capitalize()}:** {msg['content']}")

# --------------------
# Input (version-safe)
# --------------------
user_input = None

if hasattr(st, "chat_input"):
    user_input = st.chat_input("Ask about monitors, printers, issues...")
else:
    # Use form to handle Enter key submission and auto-clear input
    try:
        # Try with clear_on_submit if supported
        with st.form("chat_form", clear_on_submit=True):
            user_input = st.text_input(
                "Ask about monitors, printers, issues...",
                key=f"input_text_{st.session_state.input_counter}",
            )
            submitted = st.form_submit_button("Send")
    except TypeError:
        # Fallback if clear_on_submit not supported
        with st.form("chat_form"):
            user_input = st.text_input(
                "Ask about monitors, printers, issues...",
                key=f"input_text_{st.session_state.input_counter}",
            )
            submitted = st.form_submit_button("Send")
    
    # If form was submitted (Enter key or button), process the input
    if submitted and user_input:
        # Store input for processing (form clears it automatically)
        st.session_state.pending_input = user_input
        # Increment counter to reset widget state
        st.session_state.input_counter += 1
        # Rerun to process
        if hasattr(st, "rerun"):
            st.rerun()
        else:
            st.experimental_rerun()
    
    # Check for pending input from form submission
    if "pending_input" in st.session_state:
        user_input = st.session_state.pending_input
        del st.session_state.pending_input

# --------------------
# Process message ONCE
# --------------------
if user_input and not st.session_state.processing:
    st.session_state.processing = True

    # Add user message
    st.session_state.history.append(
        {"role": "user", "content": user_input}
    )

    with st.spinner("Thinking..."):
        response = bot.handle_message(
            user_input,
            st.session_state.history[:-1],
        )

    # Add assistant message
    st.session_state.history.append(
        {"role": "assistant", "content": response}
    )

    # 🔑 RESET FLAGS
    st.session_state.processing = False

    # Rerun - use version-safe method
    if hasattr(st, "rerun"):
        st.rerun()
    else:
        st.experimental_rerun()
