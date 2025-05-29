import streamlit as st
import requests
import os

st.set_page_config(page_title="Empathetic AI Companion", layout="centered")
st.title("💬 Empathetic AI Companion")
st.write("A non-judgmental, empathetic friend who listens — not advises.")

# Get API key from environment variable
API_KEY = os.getenv("OPENROUTER_API_KEY")

if not API_KEY:
    st.error("⚠️ Missing OpenRouter API Key. Please set the OPENROUTER_API_KEY environment variable.")
    st.stop()

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are an empathetic AI friend who listens carefully, is non-judgmental, and never gives advice."}
    ]

# Show chat history
for msg in st.session_state.messages[1:]:  # skip system message
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
if prompt := st.chat_input("Type your thoughts..."):
    # Show user message
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # API call
    with st.chat_message("assistant"):
        try:
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {API_KEY}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": "your-app-name"  # Replace with your project name or domain
                },
                json={
                    "model": "openrouter/claude-3-haiku",  # Change model if you like
                    "messages": st.session_state.messages,
                    "temperature": 0.7
                },
                timeout=60
            )

            if response.status_code == 200:
                reply = response.json()["choices"][0]["message"]["content"]
                st.markdown(reply)
                st.session_state.messages.append({"role": "assistant", "content": reply})
            else:
                st.error(f"Error: {response.status_code} — {response.text}")
        except Exception as e:
            st.error(f"Exception: {e}")
